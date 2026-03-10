import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import Dashboard from "../pages/Dashboard";
import HelloPage from "../pages/HelloPage";
import Page from "../pages/sample";


export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/api/test" element={<Page />} />
      </Routes>
    </BrowserRouter>
  );
}