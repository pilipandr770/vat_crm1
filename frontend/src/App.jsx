import { Routes,Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard.jsx";
export default ()=>(
  <Routes>
    <Route path="/" element={<Dashboard/>}/>
  </Routes>);
