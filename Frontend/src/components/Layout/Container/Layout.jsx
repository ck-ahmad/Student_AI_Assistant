import React from "react";
import { useLocation, Link } from "react-router-dom";
import { FaHome, FaBook, FaClipboard, FaNotesMedical } from "react-icons/fa";
import { PiBuildingsFill } from "react-icons/pi";
import Footer from "../../common/Footer/Footer.jsx";
import Header from '../Header/Header.jsx'

const Layout = ({ children }) => {
  const location = useLocation();
  const isHome = location.pathname === "/";

  // Map page titles & icons for non-home pages
  const pageHeaders = {
    "/quizz": { title: "Quizz", icon: <FaClipboard /> },
    "/notes": { title: "Notes", icon: <FaNotesMedical /> },
    "/health": { title: "Health", icon: <PiBuildingsFill /> },
    "/drive": { title: "Drive Manager", icon: <FaBook /> },
  };

  const currentHeader = pageHeaders[location.pathname];

  return (
    <div className="app">
      {isHome ? (
        <Header />
      ) : (
        <nav className="section-navbar">
  <Link className="nav-back" to="/">
    <FaHome aria-hidden="true" /> <span>Back to Home</span>
  </Link>

  <div className="section-title-wrapper">
    <h2 className="section-title">
      {currentHeader?.icon} {currentHeader?.title} 
    </h2>
  </div>
</nav>
      )}

      <main>{children}</main>
      <Footer />
    </div>
  );
};

export default Layout;
