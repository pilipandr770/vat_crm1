from datetime import datetime
try:
    from ..extensions import db
except ImportError:
    from backend.extensions import db

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(2), nullable=False)
    vat_number    = db.Column(db.String(14), nullable=False)
    customer_name = db.Column(db.String(256))
    address       = db.Column(db.Text)
    email         = db.Column(db.String(256))
    bank_details  = db.Column(db.Text)
    request_id    = db.Column(db.String(50))
    last_checked  = db.Column(db.DateTime)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint("country_code","vat_number"),)
