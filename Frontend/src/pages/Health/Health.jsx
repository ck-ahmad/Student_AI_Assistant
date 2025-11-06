import React, { useState } from "react";
import "./Health.css";

export default function Health() {
  const [section, setSection] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState("");
  const [symptoms, setSymptoms] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("");
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("general");

  const showSection = (name) => {
    setSection(name);
    setResult("");
  };

  const handleResponse = async (url, body) => {
    setLoading(true);
    setResult("");
    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      if (data.success) {
        setResult(`
          <div class="result-box">
            <h3>${data.title || "AI Result"}</h3>
            ${data.analysis || data.info || data.tips || ""}
          </div>
        `);
      } else {
        setResult(`<div class="result-box error">${data.message}</div>`);
      }
    } catch (err) {
      setResult(`<div class="result-box error">${err.message}</div>`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="health-page">

      <div className="container">
        <div className="card">
          <h1>AI Health Information Assistant</h1>

          <div className="warning">
            ⚠️ <b>Important Disclaimer:</b> This tool provides educational
            information only and is NOT medical advice. Always consult a
            healthcare professional for medical concerns.
          </div>

          {/* Category Buttons */}
          <div className="form-group">
            <label>What do you need help with?</label>
            <div className="category-buttons">
              <div
                className={`category-btn ${
                  section === "symptoms" ? "active" : ""
                }`}
                onClick={() => showSection("symptoms")}
              >
                🩺 Analyze Symptoms
              </div>
              <div
                className={`category-btn ${
                  section === "search" ? "active" : ""
                }`}
                onClick={() => showSection("search")}
              >
                🔍 Search Health Info
              </div>
              <div
                className={`category-btn ${
                  section === "wellness" ? "active" : ""
                }`}
                onClick={() => showSection("wellness")}
              >
                💪 Wellness Tips
              </div>
            </div>
          </div>

          {/* Sections */}
          {section === "symptoms" && (
            <div className="section">
              <h3>Symptom Analysis</h3>
              <div className="form-group">
                <label>Describe your symptoms:</label>
                <textarea
                  value={symptoms}
                  onChange={(e) => setSymptoms(e.target.value)}
                  placeholder="Describe what you're experiencing..."
                ></textarea>
              </div>
              <div className="form-group">
                <label>Age (optional):</label>
                <input
                  type="number"
                  value={age}
                  onChange={(e) => setAge(e.target.value)}
                  placeholder="Your age"
                />
              </div>
              <div className="form-group">
                <label>Gender (optional):</label>
                <select
                  value={gender}
                  onChange={(e) => setGender(e.target.value)}
                >
                  <option value="">Select</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <button
                className="btn"
                onClick={() =>
                  handleResponse("/api/health/analyze", { symptoms, age, gender })
                }
              >
                🤖 Analyze with AI
              </button>
            </div>
          )}

          {section === "search" && (
            <div className="section">
              <h3>Search Health Information</h3>
              <div className="form-group">
                <label>What would you like to know about?</label>
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="e.g., diabetes, flu, anxiety"
                />
              </div>
              <button
                className="btn"
                onClick={() =>
                  handleResponse("/api/health/search", { query })
                }
              >
                🔍 Search
              </button>
            </div>
          )}

          {section === "wellness" && (
            <div className="section">
              <h3>Wellness Tips</h3>
              <div className="form-group">
                <label>Choose a category:</label>
                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                >
                  <option value="general">General Wellness</option>
                  <option value="nutrition">Nutrition & Diet</option>
                  <option value="exercise">Exercise & Fitness</option>
                  <option value="mental">Mental Health</option>
                  <option value="sleep">Sleep Hygiene</option>
                  <option value="hydration">Hydration</option>
                </select>
              </div>
              <button
                className="btn"
                onClick={() =>
                  handleResponse("/api/health/wellness", { category })
                }
              >
                💡 Get Tips
              </button>
            </div>
          )}

          {loading && (
            <div className="loading">
              <div className="spinner"></div>
              <p>Getting AI-powered information...</p>
            </div>
          )}

          {result && (
            <div
              className="result"
              dangerouslySetInnerHTML={{ __html: result }}
            ></div>
          )}
        </div>
      </div>
    </div>
  );
}
