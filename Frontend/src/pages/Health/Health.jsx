import React, { useState } from "react";
import "./Health.css";
// Leveraging the imported API service
import { api } from "../../services/api.js"; 

// -------------------------------------------------------------------
// ⚡️ COMPONENT LOGIC, STATE, AND API HANDLERS (TOP SECTION)
// -------------------------------------------------------------------

export default function Health() {
    // --- 1. State Declarations (Unchanged) ---
    const [section, setSection] = useState("");
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState("");
    
    // States for Symptom Analysis
    const [symptoms, setSymptoms] = useState("");
    const [age, setAge] = useState("");
    const [gender, setGender] = useState("");

    // States for Search Health Info & other queries
    const [query, setQuery] = useState("");
    const [category, setCategory] = useState("general");

    // States for additional features (First Aid, Meds, Mental, Reminder)
    const [emergencyType, setEmergencyType] = useState("");
    const [medicationName, setMedicationName] = useState("");
    const [mentalHealthConcern, setMentalHealthConcern] = useState("");
    const [reminderText, setReminderText] = useState("");
    const [reminderFrequency, setReminderFrequency] = useState("daily");


    // --- 2. Helper Function (Unchanged) ---
    const showSection = (name) => {
        setSection(name);
        setResult(""); // Clear previous result when switching sections
    };


    // --- 3. API Handling Function - **API URLs FIXED** ---
    const handleResponse = async (url, body) => {
        setLoading(true);
        setResult("");
        try {
            const res = await api.post(url, body); 
            const data = res.data || res; 
            
            // --- Error/Success Handling Logic ---
            if (data && data.success) {
                // ... (rest of logic is unchanged for brevity)
                const content = data.analysis || data.info || data.tips || data.guide || data.support || data.message || "No specific details provided.";
                let title = "AI Result";
                let links = "";

                // Customize title and links based on the specific endpoint response
                if (data.analysis) title = "🩺 Symptom Analysis";
                else if (data.info) title = `🔍 Health Info: ${data.query || query}`;
                else if (data.tips) title = `💪 Wellness Tips: ${data.category.toUpperCase()}`;
                else if (data.guide) title = `🩹 First Aid Guide: ${data.emergency_type || emergencyType}`;
                else if (data.support) {
                    title = `🧠 Mental Health Support`;
                    if (data.resources) {
                        links += `<h4>Crisis Resources:</h4><ul class="resource-list">`;
                        for (const key in data.resources) {
                            links += `<li>${key.replace('_', ' ')}: <b>${data.resources[key]}</b></li>`;
                        }
                        links += `</ul>`;
                    }
                }
                else if (data.message && data.reminder_id) title = "🔔 Reminder Created Successfully";
                
                // Collect external links if present
                if (data.webmd_url) links += `<a href="${data.webmd_url}" target="_blank">WebMD Link</a>`;
                if (data.mayo_url) links += `<a href="${data.mayo_url}" target="_blank">Mayo Clinic Link</a>`;
                if (data.drugs_url) links += `<a href="${data.drugs_url}" target="_blank">Drugs.com Link</a>`;


                setResult(`
                    <div class="result-box">
                      <h3>${title}</h3>
                      ${content.replace(/\n/g, '<br/>')}
                      ${links ? `<div class="info-links">${links}</div>` : ""}
                    </div>
                `);
            } else if (data && data.message) {
                 setResult(`<div class="result-box error">AI Error: ${data.message}</div>`);
            } else {
                 setResult(`<div class="result-box error">AI Error: An unknown error occurred on the server or the API responded with an empty body.</div>`);
            }

        } catch (err) {
            let errorMessage = "Request failed. Check if the backend server is running.";
            if (err.response && err.response.status === 404) {
                errorMessage = `Server 404: The API route "${url}" was not found on the backend.`;
            } else if (err.message) {
                 errorMessage = `Network/API Error: ${err.message}`;
            }

            setResult(`<div class="result-box error">${errorMessage}</div>`);
        } finally {
            setLoading(false);
        }
    };


    // -------------------------------------------------------------------
    // 🖥️ COMPONENT RENDERING / JSX / HTML STRUCTURE 
    // -------------------------------------------------------------------

    return (
        <div className="health-page">
            <div className="container">
                <div className="card">
                    <h1>AI Health Information Assistant</h1>

                    <div className="warning">
                        ⚠️ <b>Important Disclaimer:</b> This tool provides educational
                        information only and is **NOT medical advice**. Always consult a
                        healthcare professional for medical concerns.
                    </div>

                    {/* Category Buttons - Horizontal Display (via CSS) */}
                    <div className="form-group">
                        <label>What do you need help with?</label>
                        <div className="category-buttons">
                            
                            <div
                                className={`category-btn ${section === "symptoms" ? "active" : ""}`}
                                onClick={() => showSection("symptoms")}
                            >
                                🩺 Analyze Symptoms
                            </div>
                            <div
                                className={`category-btn ${section === "search" ? "active" : ""}`}
                                onClick={() => showSection("search")}
                            >
                                🔍 Search Health Info
                            </div>
                            <div
                                className={`category-btn ${section === "wellness" ? "active" : ""}`}
                                onClick={() => showSection("wellness")}
                            >
                                💪 Wellness Tips
                            </div>
                            <div
                                className={`category-btn ${section === "firstaid" ? "active" : ""}`}
                                onClick={() => showSection("firstaid")}
                            >
                                🩹 First Aid Guide
                            </div>
                            <div
                                className={`category-btn ${section === "medication" ? "active" : ""}`}
                                onClick={() => showSection("medication")}
                            >
                                💊 Medication Info
                            </div>
                            <div
                                className={`category-btn ${section === "mental" ? "active" : ""}`}
                                onClick={() => showSection("mental")}
                            >
                                🧠 Mental Health
                            </div>
                            <div
                                className={`category-btn ${section === "reminder" ? "active" : ""}`}
                                onClick={() => showSection("reminder")}
                            >
                                🔔 Set Reminder
                            </div>
                        </div>
                    </div>

                    {/* --- INPUT SECTIONS --- */}

                    {/* Symptom Analysis Section */}
                    {section === "symptoms" && (
                        <div className="section active-section"> {/* Added active-section class */}
                            <h3>Symptom Analysis</h3>
                            <div className="form-group">
                                <label>Describe your symptoms:</label>
                                <textarea
                                    value={symptoms}
                                    onChange={(e) => setSymptoms(e.target.value)}
                                    placeholder="Describe what you're experiencing..."
                                ></textarea>
                            </div>
                            <div className="form-row"> {/* New wrapper for inline fields */}
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
                            </div>
                            <button
                                className="btn"
                                onClick={() =>
                                    handleResponse("/health/analyze", { symptoms, age, gender }) // <<< FIXED URL
                                }
                            >
                                🤖 Analyze with AI
                            </button>
                        </div>
                    )}

                    {/* Search Health Info Section */}
                    {section === "search" && (
                        <div className="section active-section">
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
                                    handleResponse("/health/search", { query }) // <<< FIXED URL
                                }
                            >
                                🔍 Search
                            </button>
                        </div>
                    )}

                    {/* Wellness Tips Section */}
                    {section === "wellness" && (
                        <div className="section active-section">
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
                                    handleResponse("/health/wellness", { category }) // <<< FIXED URL
                                }
                            >
                                💡 Get Tips
                            </button>
                        </div>
                    )}
                    
                    {/* First Aid Section */}
                    {section === "firstaid" && (
                        <div className="section active-section">
                            <h3>First Aid Guide</h3>
                            <div className="form-group">
                                <label>Enter emergency type:</label>
                                <input
                                    type="text"
                                    value={emergencyType}
                                    onChange={(e) => setEmergencyType(e.target.value)}
                                    placeholder="e.g., severe cut, mild burn, choking"
                                />
                            </div>
                            <button
                                className="btn" 
                                onClick={() =>
                                    handleResponse("/health/firstaid", { emergency_type: emergencyType }) // <<< FIXED URL
                                }
                            >
                                🚨 Get First Aid Steps
                            </button>
                        </div>
                    )}

                    {/* Medication Info Section */}
                    {section === "medication" && (
                        <div className="section active-section">
                            <h3>Medication Information</h3>
                            <div className="form-group">
                                <label>Enter medication name:</label>
                                <input
                                    type="text"
                                    value={medicationName}
                                    onChange={(e) => setMedicationName(e.target.value)}
                                    placeholder="e.g., Aspirin, Zoloft"
                                />
                            </div>
                            <button
                                className="btn"
                                onClick={() =>
                                    handleResponse("/health/medication", { medication_name: medicationName }) // <<< FIXED URL
                                }
                            >
                                💊 Check Info
                            </button>
                        </div>
                    )}

                    {/* Mental Health Support Section */}
                    {section === "mental" && (
                        <div className="section active-section">
                            <h3>Mental Health Support</h3>
                            <div className="form-group">
                                <label>What concern are you looking for support on?</label>
                                <input
                                    type="text"
                                    value={mentalHealthConcern}
                                    onChange={(e) => setMentalHealthConcern(e.target.value)}
                                    placeholder="e.g., anxiety, coping with stress, grief"
                                />
                            </div>
                            <button
                                className="btn"
                                onClick={() =>
                                    handleResponse("/health/mentalhealth", { concern: mentalHealthConcern }) // <<< FIXED URL
                                }
                            >
                                🧠 Get Support
                            </button>
                        </div>
                    )}
                    
                    {/* Create Health Reminder Section */}
                    {section === "reminder" && (
                        <div className="section active-section">
                            <h3>Set Health Reminder</h3>
                            <div className="form-group">
                                <label>Reminder Text:</label>
                                <input
                                    type="text"
                                    value={reminderText}
                                    onChange={(e) => setReminderText(e.target.value)}
                                    placeholder="e.g., Take evening dose, Do 15 min walk"
                                />
                            </div>
                            <div className="form-group">
                                <label>Frequency:</label>
                                <select
                                    value={reminderFrequency}
                                    onChange={(e) => setReminderFrequency(e.target.value)}
                                >
                                    <option value="daily">Daily</option>
                                    <option value="weekly">Weekly</option>
                                    <option value="monthly">Monthly</option>
                                </select>
                            </div>
                            <button
                                className="btn"
                                onClick={() =>
                                    handleResponse("/health/reminder", { // <<< FIXED URL
                                        reminder_text: reminderText, 
                                        frequency: reminderFrequency 
                                    })
                                }
                            >
                                🔔 Create Reminder
                            </button>
                        </div>
                    )}


                    {/* --- RESULTS & LOADING (Unchanged) --- */}
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