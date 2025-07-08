# =============================================================================
# populate_vatcrm.ps1  записує повний код VAT CRM (бекенд + фронт + Docker)
# =============================================================================
param()
Stop = 'Stop'
function WriteFile([string],[string]){
    =[IO.Path]::GetDirectoryName()
    if( -and -not(Test-Path )){ New-Item -ItemType Directory -Path  -Force | Out-Null }
     | Set-Content -Path  -Encoding UTF8
}

# ---------- backend ----------------------------------------------------------
WriteFile 'backend/requirements.txt' @'
Flask[async]==3.1.1
SQLAlchemy==2.0.41
alembic==1.16.2
python-dotenv==1.1.1
httpx==0.28.1
zeep==4.2.1
'@

WriteFile 'backend/app.py' @'
from flask import Flask
from .config import settings
from .extensions import db
from .api import api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    db.init_app(app)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/ping")
    def ping():
        return {"status": "pong"}

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
'@

WriteFile 'backend/config.py' @'
import os, dotenv, pathlib
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
dotenv.load_dotenv(BASE_DIR / ".env", override=True)
class settings:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///local.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
'@

WriteFile 'backend/extensions.py' 'from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()'

WriteFile 'backend/models/__init__.py' ''

WriteFile 'backend/models/company.py' @'
from datetime import datetime
from ..extensions import db

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(2), nullable=False)
    vat_number    = db.Column(db.String(14), nullable=False)
    customer_name = db.Column(db.String(256))
    address       = db.Column(db.Text)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint("country_code", "vat_number"),)
'@

WriteFile 'backend/services/vies.py' @'
import httpx, zeep
WSDL = "https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"

async def check_vat(cc: str, vat: str, requester: dict | None = None) -> dict:
    async with httpx.AsyncClient(timeout=30) as c:
        transport = zeep.AsyncTransport(client=c)
        ws = zeep.AsyncClient(WSDL, transport=transport)
        res = await ws.service.checkVat(countryCode=cc, vatNumber=vat)
        return dict(res)
'@

WriteFile 'backend/api/__init__.py' @'
from flask import Blueprint
from .companies import companies_api
api_bp = Blueprint("api", __name__)
api_bp.register_blueprint(companies_api, url_prefix="/companies")
'@

WriteFile 'backend/api/companies.py' @'
from flask import Blueprint, request, jsonify
from ..models.company import Company
from ..extensions import db
from ..services.vies import check_vat
import asyncio

companies_api = Blueprint("companies_api", __name__)

@companies_api.post("/full-check")
def full_check():
    payload = request.json or {}
    req = payload.get("requester", {})
    cnt = payload.get("counterparty", {})

    cc = cnt.get("country_code", "").upper()
    vat = cnt.get("vat_number", "")
    if not (cc and vat):
        return {"error": "country_code & vat_number required"}, 400

    res = asyncio.run(check_vat(cc, vat, req))
    comp = Company.query.filter_by(country_code=cc, vat_number=vat).first()
    if not comp:
        comp = Company(country_code=cc, vat_number=vat)
        db.session.add(comp)

    comp.customer_name = res.get("name") or comp.customer_name
    comp.address       = res.get("address") or comp.address
    db.session.commit()

    return jsonify({
        "id": comp.id,
        "country_code": cc,
        "vat_number": vat,
        "valid": res["valid"],
        "customer_name": comp.customer_name,
        "address": comp.address
    })
'@

# ---------- frontend ---------------------------------------------------------
WriteFile 'frontend/package.json' @'
{
  "name": "vatcrm-frontend",
  "private": true,
  "scripts": { "dev": "vite", "build": "vite build" },
  "dependencies": {
    "axios": "^1.6.8",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.22.3"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.2.0"
  }
}
'@

WriteFile 'frontend/vite.config.js' @'
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
export default defineConfig({
  plugins: [react()],
  server: { port: 5173, proxy: { "/api": "http://localhost:8000" } }
});
'@

WriteFile 'frontend/index.html' '<!doctype html><div id="root"></div><script type="module" src="/src/main.jsx"></script>'

WriteFile 'frontend/src/main.jsx' @'
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App.jsx";
ReactDOM.createRoot(document.getElementById("root")).render(
  <BrowserRouter><App/></BrowserRouter>
);
'@

WriteFile 'frontend/src/App.jsx' @'
import { Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard.jsx";
export default () => (
  <Routes>
    <Route path="/" element={<Dashboard/>}/>
  </Routes>
);
'@

WriteFile 'frontend/src/pages/Dashboard.jsx' @'
import { useState } from "react";
import axios from "axios";
export default function Dashboard(){
  const [me,setMe]=useState({requester_country_code:"",requester_vat:""});
  const [cp,setCp]=useState({country_code:"",vat_number:""});
  const [out,setOut]=useState(null);

  const run=()=>axios.post("/api/companies/full-check",
    {requester:me,counterparty:cp}).then(r=>setOut(r.data))
    .catch(e=>alert(e.response?.data?.error||e.message));

  return(
    <div style={{display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:16,padding:16}}>
      <div>
        <h3>Ihre Daten</h3>
        <input placeholder="Land" value={me.requester_country_code}
          onChange={e=>setMe({...me,requester_country_code:e.target.value})}/>
        <input placeholder="USt-IdNr" value={me.requester_vat}
          onChange={e=>setMe({...me,requester_vat:e.target.value})}/>
      </div>
      <div>
        <h3>Daten des Partners</h3>
        <input placeholder="Land" value={cp.country_code}
          onChange={e=>setCp({...cp,country_code:e.target.value})}/>
        <input placeholder="VAT" value={cp.vat_number}
          onChange={e=>setCp({...cp,vat_number:e.target.value})}/>
        <button onClick={run}>Prüfen</button>
      </div>
      <div>
        <h3>Ergebnis</h3>
        <pre>{out?JSON.stringify(out,null,2):""}</pre>
      </div>
    </div>
  );
}
'@

# ---------- docker -----------------------------------------------------------
WriteFile 'docker-compose.yml' @'
version: "3.9"
services:
  backend:
    build: ./docker
    volumes: ["./backend:/app/backend"]
    ports: ["8000:8000"]
  frontend:
    image: node:20
    working_dir: /app
    command: sh -c "npm install && npm run dev"
    volumes: ["./frontend:/app"]
    ports: ["5173:5173"]
'@

WriteFile 'docker/Dockerfile.backend' @'
FROM python:3.10-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend /app/backend
CMD ["python","-m","backend.app"]
'@

Write-Host "
 Код заповнено. Далі:
1) cd backend ; python -m venv venv ; .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   flask db init ; flask db migrate -m init ; flask db upgrade
   python -m backend.app
2) нова вкладка  cd frontend ; npm install ; npm run dev
3) перевірити  http://localhost:5173"
