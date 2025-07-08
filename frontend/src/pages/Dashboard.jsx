import {useState} from "react";
import axios from "axios";

export default function Dashboard(){
  const [req,setReq]=useState({requester_country_code:"",requester_vat:""});
  const [cnt,setCnt]=useState({country_code:"",vat_number:""});
  const [res,setRes]=useState(null);

  const check=()=>axios.post("/api/companies/full-check",
    {requester:req,counterparty:cnt}).then(r=>setRes(r.data))
    .catch(e=>alert(e.response?.data?.error||e.message));

  return(<div style={{display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:16,padding:16}}>
    <div><h3>Ihre Daten</h3>
      <input placeholder="Land" value={req.requester_country_code}
        onChange={e=>setReq({...req,requester_country_code:e.target.value})}/>
      <input placeholder="USt-IdNr" value={req.requester_vat}
        onChange={e=>setReq({...req,requester_vat:e.target.value})}/>
    </div>
    <div><h3>Daten des Partners</h3>
      <input placeholder="Land" value={cnt.country_code}
        onChange={e=>setCnt({...cnt,country_code:e.target.value})}/>
      <input placeholder="VAT" value={cnt.vat_number}
        onChange={e=>setCnt({...cnt,vat_number:e.target.value})}/>
      <button onClick={check}>Prüfen</button>
    </div>
    <div><h3>Ergebnis</h3>
      <pre>{res?JSON.stringify(res,null,2):""}</pre>
    </div>
  </div>);
}
