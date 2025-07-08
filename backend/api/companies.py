from flask import Blueprint,request,jsonify
from datetime import datetime
try:
    from ..models.company import Company
    from ..extensions import db
    from ..services.vies import check_vat
except ImportError:
    from backend.models.company import Company
    from backend.extensions import db
    from backend.services.vies import check_vat

companies_api = Blueprint("companies_api",__name__)

@companies_api.post("/full-check")
def full_check():
    data = request.json or {}
    req  = data.get("requester",{})
    cnt  = data.get("counterparty",{})
    cc=cnt.get("country_code","").upper(); vat=cnt.get("vat_number","")
    if not(cc and vat): return {"error":"country_code & vat_number required"},400
    
    # Run the VAT check - this will handle errors internally
    try:
        res = check_vat(cc, vat, req)
        valid = res.get("valid", False)
        error_message = res.get("error")
        request_id = res.get("requestIdentifier", None)
    except Exception as e:
        # Fallback in case of unexpected errors
        res = {
            "valid": False,
            "error": str(e)
        }
        valid = False
        error_message = str(e)
        request_id = None
        
    # Get or create the company record
    comp = Company.query.filter_by(country_code=cc, vat_number=vat).first()
    if not comp:
        comp = Company(country_code=cc, vat_number=vat)
        db.session.add(comp)
    
    # Update company data
    if valid:
        comp.customer_name = res.get("name") or comp.customer_name
        comp.address = res.get("address") or comp.address
        comp.email = cnt.get("email") or comp.email
        comp.bank_details = cnt.get("bank_details") or comp.bank_details
        comp.request_id = request_id
        comp.last_checked = datetime.utcnow()
        
    db.session.commit()
    
    # Prepare the response
    response = {
        "id": comp.id,
        "country_code": cc,
        "vat_number": vat,
        # Добавляем полное представление VAT номера для отображения на фронтенде
        "formatted_vat": f"{cc}{vat}",
        "valid": valid,
        "name": comp.customer_name,
        "address": comp.address,
        "email": comp.email,
        "bank_details": comp.bank_details,
        "request_id": comp.request_id,
        "last_checked": comp.last_checked.isoformat() if comp.last_checked else None,
        "check_timestamp": datetime.now().isoformat()
    }
    
    # Add error message if validation failed
    if not valid:
        response["error_message"] = error_message or "Die USt-IdNr. ist ungültig"
        
    return jsonify(response)

@companies_api.get("")
def list_companies():
    return jsonify([{
        "id":c.id,"country_code":c.country_code,"vat_number":c.vat_number,
        "customer_name":c.customer_name
    } for c in Company.query.all()])

@companies_api.get("/<int:cid>")
def get_company(cid):
    c=Company.query.get_or_404(cid)
    return jsonify({
        "id":c.id,
        "country_code":c.country_code,
        "vat_number":c.vat_number,
        "name":c.customer_name,
        "address":c.address,
        "email":c.email,
        "bank_details":c.bank_details,
        "request_id":c.request_id,
        "last_checked":c.last_checked.isoformat() if c.last_checked else None
    })
