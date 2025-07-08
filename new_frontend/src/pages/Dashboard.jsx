import { useState } from "react";
import axios from "axios";
import { API_BASE_URL } from "../config";

const EU_COUNTRIES = [
  { code: "AT", name: "Österreich" },
  { code: "BE", name: "Belgien" },
  { code: "BG", name: "Bulgarien" },
  { code: "HR", name: "Kroatien" },
  { code: "CY", name: "Zypern" },
  { code: "CZ", name: "Tschechien" },
  { code: "DK", name: "Dänemark" },
  { code: "EE", name: "Estland" },
  { code: "FI", name: "Finnland" },
  { code: "FR", name: "Frankreich" },
  { code: "DE", name: "Deutschland" },
  { code: "GR", name: "Griechenland" },
  { code: "HU", name: "Ungarn" },
  { code: "IE", name: "Irland" },
  { code: "IT", name: "Italien" },
  { code: "LV", name: "Lettland" },
  { code: "LT", name: "Litauen" },
  { code: "LU", name: "Luxemburg" },
  { code: "MT", name: "Malta" },
  { code: "NL", name: "Niederlande" },
  { code: "PL", name: "Polen" },
  { code: "PT", name: "Portugal" },
  { code: "RO", name: "Rumänien" },
  { code: "SK", name: "Slowakei" },
  { code: "SI", name: "Slowenien" },
  { code: "ES", name: "Spanien" },
  { code: "SE", name: "Schweden" }
];

export default function Dashboard() {
  const [me, setMe] = useState({ 
    requester_country_code: "DE",
    requester_vat: "",
    smtp_host: "",
    smtp_user: "",
    smtp_password: "",
    opencorporates_api_key: ""
  });
  
  const [cp, setCp] = useState({ 
    country_code: "DE",
    vat_number: "",
    address: "",
    email: "",
    bank_details: ""
  });
  
  const [out, setOut] = useState(null);
  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);

  const checkVat = () => {
    setLoading(true);
    setOut(null);
    
    // Validate that we have the minimum required fields
    if (!cp.country_code || !cp.vat_number) {
      alert("Bitte geben Sie mindestens das Land und die USt-IdNr des Geschäftspartners ein.");
      setLoading(false);
      return;
    }
    
    // Create payload - empty requester fields won't impact the API
    const payload = { 
      requester: me, 
      counterparty: cp 
    };
    
    axios.post(`${API_BASE_URL}/api/companies/full-check`, payload)
      .then(response => {
        setOut(response.data);
        setCurrentStep(3);
      })
      .catch(error => {
        // Handle error and show user-friendly message
        const errorMsg = error.response?.data?.error || 
                        "Fehler bei der Überprüfung der USt-IdNr. Bitte versuchen Sie es später erneut.";
        alert(errorMsg);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const goToStep = (step) => {
    if (step === 3 && !out) {
      // If trying to go to step 3 without validation data
      checkVat();
    } else {
      setCurrentStep(step);
    }
  };

  const formatAddress = (address) => {
    if (!address) return "";
    
    // Split the address by newlines or commas
    const parts = address.split(/[\n,]+/).map(part => part.trim()).filter(Boolean);
    
    return parts.map((part, index) => (
      <span key={index}>
        {part}
        {index < parts.length - 1 && <br />}
      </span>
    ));
  };

  return (
    <div className="container">
      <header className="header">
        <a href="#" className="back-button">
          <i className="fas fa-arrow-left"></i> Zurück
        </a>
        <h1>VAT CRM Schnellprüfung</h1>
        <div className="auth-links">
          <a href="#"><i className="fas fa-user"></i> Anmelden</a>
        </div>
      </header>

      <div className="card-container">
        {/* Step 1: Your Information */}
        <div className={`card ${currentStep === 1 ? 'active' : ''}`}>
          <h2><span className="step-number">1</span> Ihre Angaben</h2>
          
          <div className="form-group">
            <label htmlFor="requester_country">Land</label>
            <select 
              id="requester_country" 
              value={me.requester_country_code}
              onChange={e => setMe({ ...me, requester_country_code: e.target.value })}
            >
              {EU_COUNTRIES.map(country => (
                <option key={country.code} value={country.code}>
                  {country.name} ({country.code})
                </option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="requester_vat">USt-IdNr (optional)</label>
            <input 
              id="requester_vat" 
              type="text" 
              value={me.requester_vat}
              onChange={e => setMe({ ...me, requester_vat: e.target.value })}
              placeholder="z.B. DE123456789"
            />
            <small className="help-text">Eingabe optional für einfache Prüfung</small>
          </div>
          
          <div className="form-group">
            <label htmlFor="smtp_host">SMTP Host (optional)</label>
            <input 
              id="smtp_host" 
              type="text" 
              value={me.smtp_host}
              onChange={e => setMe({ ...me, smtp_host: e.target.value })}
              placeholder="smtp.beispiel.de"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="smtp_user">SMTP Benutzername (optional)</label>
            <input 
              id="smtp_user" 
              type="text" 
              value={me.smtp_user}
              onChange={e => setMe({ ...me, smtp_user: e.target.value })}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="smtp_password">SMTP Passwort (optional)</label>
            <input 
              id="smtp_password" 
              type="password" 
              value={me.smtp_password}
              onChange={e => setMe({ ...me, smtp_password: e.target.value })}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="opencorporates_api_key">OpenCorporates API Key (optional)</label>
            <input 
              id="opencorporates_api_key" 
              type="text" 
              value={me.opencorporates_api_key}
              onChange={e => setMe({ ...me, opencorporates_api_key: e.target.value })}
            />
          </div>
          
          <button onClick={() => goToStep(2)}>
            Weiter <i className="fas fa-arrow-right"></i>
          </button>
        </div>

        {/* Step 2: Business Partner Data */}
        <div className={`card ${currentStep === 2 ? 'active' : ''}`}>
          <h2><span className="step-number">2</span> Daten des Geschäftspartners</h2>
          
          <div className="form-group">
            <label htmlFor="cp_country">Land</label>
            <select 
              id="cp_country" 
              value={cp.country_code}
              onChange={e => setCp({ ...cp, country_code: e.target.value })}
            >
              {EU_COUNTRIES.map(country => (
                <option key={country.code} value={country.code}>
                  {country.name} ({country.code})
                </option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="cp_vat">USt-IdNr</label>
            <input 
              id="cp_vat" 
              type="text" 
              value={cp.vat_number}
              onChange={e => setCp({ ...cp, vat_number: e.target.value })}
              placeholder="z.B. FR123456789"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="cp_address">Lieferadresse (optional)</label>
            <textarea 
              id="cp_address" 
              value={cp.address}
              onChange={e => setCp({ ...cp, address: e.target.value })}
              rows="3"
              placeholder="Straße, Hausnummer
PLZ, Stadt
Land"
            ></textarea>
          </div>
          
          <div className="form-group">
            <label htmlFor="cp_email">E-Mail (optional)</label>
            <input 
              id="cp_email" 
              type="email" 
              value={cp.email}
              onChange={e => setCp({ ...cp, email: e.target.value })}
              placeholder="kontakt@beispiel.de"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="cp_bank">Bankverbindung (optional)</label>
            <input 
              id="cp_bank" 
              type="text" 
              value={cp.bank_details}
              onChange={e => setCp({ ...cp, bank_details: e.target.value })}
              placeholder="IBAN: DE12 3456 7890 1234 5678 90"
            />
          </div>
          
          <div className="button-group">
            <button onClick={() => goToStep(1)} className="back-button">
              <i className="fas fa-arrow-left"></i> Zurück
            </button>
            <button onClick={checkVat} disabled={loading} className="primary-button">
              {loading ? <i className="fas fa-spinner fa-spin"></i> : <i className="fas fa-check"></i>} 
              Prüfen
            </button>
          </div>
        </div>

        {/* Step 3: Results */}
        <div className={`card ${currentStep === 3 ? 'active' : ''}`}>
          <h2><span className="step-number">3</span> Ergebnis</h2>
          
          {loading && (
            <div className="loading">
              <i className="fas fa-spinner fa-spin"></i> Prüfung läuft...
            </div>
          )}
          
          {!loading && out && (
            <div className="results">
              <div className="valid-status">
                {out.valid ? (
                  <><i className="fas fa-check-circle check-icon"></i> USt-IdNr. ist gültig</>
                ) : (
                  <><i className="fas fa-times-circle" style={{ color: 'var(--error-color)' }}></i> USt-IdNr. ist ungültig</>
                )}
              </div>
              
              {out.valid && (
                <div className="company-info">
                  <div className="form-group">
                    <label>Firmenname</label>
                    <div className="info-value">{out.name || "Nicht verfügbar"}</div>
                  </div>
                  
                  <div className="form-group">
                    <label>Adresse</label>
                    <div className="info-value">
                      {out.address ? formatAddress(out.address) : "Nicht verfügbar"}
                    </div>
                  </div>
                  
                  <div className="form-group">
                    <label>Anfragedatum</label>
                    <div className="info-value">
                      {new Date().toLocaleDateString('de-DE')}
                    </div>
                  </div>
                  
                  <div className="form-group">
                    <label>Anfrage-ID</label>
                    <div className="info-value">{out.request_id || "-"}</div>
                  </div>
                </div>
              )}
              
              {!out.valid && (
                <div className="error-message">
                  <p>Die angegebene USt-IdNr. konnte nicht validiert werden.</p>
                  {out.error ? (
                    <p>Fehler: {out.error}</p>
                  ) : (
                    <p>Hinweis: Diese USt-IdNr. existiert nicht oder ist ungültig.</p>
                  )}
                  
                  <div className="vat-info">
                    <p><strong>Eingegebene USt-IdNr:</strong> {out.formatted_vat || `${out.country_code}${out.vat_number}`}</p>
                    <p><strong>Überprüft am:</strong> {new Date().toLocaleString('de-DE')}</p>
                  </div>
                </div>
              )}
            </div>
          )}
          
          {!loading && !out && (
            <div className="no-result">
              <p>Keine Prüfung durchgeführt.</p>
            </div>
          )}
          
          <div className="button-group">
            <button onClick={() => goToStep(2)} className="back-button">
              <i className="fas fa-arrow-left"></i> Zurück
            </button>
            <button onClick={checkVat} disabled={loading} className="primary-button">
              {loading ? <i className="fas fa-spinner fa-spin"></i> : <i className="fas fa-refresh"></i>} 
              Erneut prüfen
            </button>
          </div>
        </div>
      </div>
      
      <footer className="footer">
        <a href="#">Datenschutz</a>
        <a href="#">Impressum</a>
        <a href="#">Hilfe</a>
      </footer>
    </div>
  );
}
