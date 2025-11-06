import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);
  const toggleMenu = () => setMenuOpen(!menuOpen);

  const navItems = [
    { label: "Notes", path: "/notes" },
    { label: "Drive", path: "/drive" },
    { label: "Health", path: "/health" },
    { label: "Quiz", path: "/quiz" },
    { label: "Search", path: "/search" },
  ];

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-logo">Student AI</div>

        <button className="navbar-toggle" onClick={toggleMenu}>
          ☰
        </button>

        <div className={`navbar-links ${menuOpen ? "active" : ""}`}>
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                isActive ? "nav-link active" : "nav-link"
              }
            >
              {item.label}
            </NavLink>
          ))}
        </div>
      </div>
    </nav>
  );
}
