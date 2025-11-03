import Footer from "./components/Footer/Footer";
import Hero from "./components/Main/Hero";
import Nav from "./components/Navbar/Nav";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Chatbot from "./components/ChatInterface/Chatbot";
import Admin from "./components/Admin/Admin";
import NyayLens from "./components/NyayLens/NyayLens";
import NyayShala from "./components/NyayShala/NyayShala";
function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <div className="flex-1">
          <Routes>
            <Route path="/" element={<Hero />} />
            <Route path="/chatbot" element={<Chatbot />} />
            <Route path="/nyaylens" element={<NyayLens />} />
            <Route path="/nyayshala" element={<NyayShala />} />
            <Route path="/admin" element={<Admin />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
