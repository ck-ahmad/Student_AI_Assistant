import React, { useState } from "react";
import Card from "../../components/common/Card/Card";
import Button from "../../components/common/Button/Button";
import Input from "../../components/common/Input/Input";
import { marked } from 'marked'; 
import {
  FiPlus,
  FiEye,
  FiSearch,
  FiEdit2,
  FiTrash2,
  FiBookOpen,
  FiMessageSquare,
  FiLayers,
  FiMic, 
} from "react-icons/fi";
import "./notes.css";

// Helper for safe HTML injection (as seen in your original code)
const escapeHtml = (str) =>
  String(str)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

// --- Helper function to render consolidated notes ---
const renderConsolidatedNotes = (notes, topic, editNote, deleteNote) => {
    if (notes.length === 0) {
        return (
            <p style={{ textAlign: "center", color: "#666" }}>
                No notes found for this topic.
            </p>
        );
    }
    
    // 1. Join all note texts into one long string, separated by two newlines
    const fullNoteText = notes
        .map(n => n.text)
        .join('\n\n'); 

    // 2. Clean up the combined text (timestamp and extra spaces)
    const contentWithoutTimestamps = fullNoteText.replace(/\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} - /g, '').trim();
    const cleanedContent = contentWithoutTimestamps.replace(/\* {3,}/g, '* ').trim();

   
    return (
        <div className="note-item" key="consolidated-note">
            <div 
                className="note-text"
                dangerouslySetInnerHTML={{ __html: marked.parse(cleanedContent) }}
            />
            
            {/* Action buttons (linked to the first note's ID for CRUD operations) */}
            <div className="note-actions">
                <Button 
                    onClick={() => editNote(notes[0].id)}>
                    <FiEdit2 /> Edit
                </Button>
                <Button 
                    onClick={() => deleteNote(notes[0].id)} 
                    variant="danger">
                    <FiTrash2 /> Delete
                </Button>
            </div>
        </div>
    );
};
// ---------------------------------------------------


export default function Notes() {
  const BASE_URL = "http://127.0.0.1:5000"; // Flask backend

  const [topic, setTopic] = useState("");
  const [noteText, setNoteText] = useState("");
  const [useAI, setUseAI] = useState(true);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [notes, setNotes] = useState([]);
  const [notesVisible, setNotesVisible] = useState(false);
  const [aiResponseHTML, setAiResponseHTML] = useState("");

  const showMessage = (text, type = "success") => {
    setMessage({ text, type });
    window.clearTimeout(showMessage._t);
    showMessage._t = setTimeout(() => setMessage(null), 4500);
  };

  /* -------- API actions: CRUD & Search (Your existing logic) -------- */

  const viewNotes = async () => {
    const trimmedTopic = topic.trim();
    if (!trimmedTopic)
      return showMessage("Please enter a topic name to view notes", "error");

    setLoading(true);
    try {
      const res = await fetch(`${BASE_URL}/api/notes/view`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: trimmedTopic }),
      });
      const data = await res.json();
      if (data.success) {
        setNotes(Array.isArray(data.notes) ? data.notes : []);
        setNotesVisible(true);
        showMessage(`Loaded ${data.notes.length} notes for topic: ${trimmedTopic}`, "success");
      } else {
        showMessage(data.message || "Failed to load notes", "error");
      }
    } catch (err) {
      showMessage("Error viewing notes: Check if backend is running and CORS is enabled.", "error");
    } finally {
      setLoading(false);
    }
  };

  const addNote = async () => {
    // ... (addNote logic remains the same)
    const trimmedTopic = topic.trim();
    const trimmedNote = noteText.trim();
    if (!trimmedTopic || !trimmedNote)
      return showMessage("Please enter both topic and note content", "error");

    setLoading(true);
    try {
      const res = await fetch(`${BASE_URL}/api/notes/create`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          topic: trimmedTopic,
          note: trimmedNote,
          use_ai: useAI,
        }),
      });
      const data = await res.json();
      if (data.success) {
        showMessage(data.message || "Note added", "success");
        setNoteText("");
        if (useAI && data.enhanced_note) {
          // Display the first part of the AI-enhanced note
          setAiResponseHTML(
            `<div class="ai-response ai-info">
                <h3>📝 Enhanced Note Preview</h3>
                ${data.enhanced_note.slice(0, 500)}...
            </div>`
          );
        }
        await viewNotes(); // Refresh the list of notes
      } else {
        showMessage(data.message || "Failed to add note", "error");
      }
    } catch (err) {
      showMessage("Error adding note: " + err.message, "error");
    } finally {
      setLoading(false);
    }
  };
  
  const deleteNote = async (id) => {
    // ... (deleteNote logic remains the same)
    const trimmedTopic = topic.trim();
    if (!trimmedTopic)
      return showMessage("Please enter a topic name", "error");
    if (!window.confirm("Are you sure you want to delete this note?")) return;

    setLoading(true);
    try {
      const res = await fetch(`${BASE_URL}/api/notes/delete`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: trimmedTopic, note_id: id }),
      });
      const data = await res.json();
      if (data.success) {
        showMessage(data.message || "Note deleted", "success");
        await viewNotes();
      } else {
        showMessage(data.message || "Delete failed", "error");
      }
    } catch (err) {
      showMessage("Error deleting note: " + err.message, "error");
    } finally {
      setLoading(false);
    }
  };

  const editNote = async (id) => {
    // ... (editNote logic remains the same)
    const trimmedTopic = topic.trim();
    if (!trimmedTopic)
      return showMessage("Please enter a topic name", "error");

    const newText = window.prompt("Enter the updated note:");
    if (!newText) return;

    const enhance = window.confirm("Enhance with AI? (Recommended)");
    setLoading(true);
    try {
      const res = await fetch(`${BASE_URL}/api/notes/edit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          topic: trimmedTopic,
          note_id: id,
          new_text: newText,
          use_ai: enhance,
        }),
      });
      const data = await res.json();
      if (data.success) {
        showMessage(data.message || "Note updated", "success");
        await viewNotes();
      } else {
        showMessage(data.message || "Update failed", "error");
      }
    } catch (err) {
      showMessage("Error editing note: " + err.message, "error");
    } finally {
      setLoading(false);
    }
  };

  const searchNotes = async () => {
    // ... (searchNotes logic remains the same)
    const trimmedTopic = topic.trim();
    if (!trimmedTopic)
      return showMessage("Please enter a topic name", "error");
    const keyword = window.prompt("Enter keyword to search:");
    if (!keyword) return;

    setLoading(true);
    try {
      const res = await fetch(`${BASE_URL}/api/notes/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: trimmedTopic, keyword }),
      });
      const data = await res.json();
      if (data.success) {
        setNotes(Array.isArray(data.notes) ? data.notes : []);
        setNotesVisible(true);
        showMessage(`Found ${data.notes.length} note(s)`, "success");
      } else {
        showMessage(data.message || "Search failed", "error");
      }
    } catch (err) {
      showMessage("Error searching notes: " + err.message, "error");
    } finally {
      setLoading(false);
    }
  };

  /* -------- AI features (Completed from your draft) -------- */

  const summarizeNotes = async () => {
    // ... (summarizeNotes logic remains the same)
    const trimmedTopic = topic.trim();
    if (!trimmedTopic)
      return showMessage("Please enter a topic name", "error");
    setLoading(true);
    try {
      const res = await fetch(`${BASE_URL}/api/notes/summarize`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: trimmedTopic }),
      });
      const data = await res.json();
      if (data.success) {
        setAiResponseHTML(
          `<div class="ai-response ai-summary"><h3>📋 Summary for ${trimmedTopic}</h3>${marked.parse(data.summary)}</div>`
        );
        showMessage("Summary generated!", "success");
      } else {
        showMessage(data.message || "Summary failed", "error");
      }
    } catch (err) {
      showMessage("Error summarizing notes: " + err.message, "error");
    } finally {
      setLoading(false);
    }
  };

  const askAI = async () => {
    // ... (askAI logic remains the same)
    const trimmedTopic = topic.trim();
    if (!trimmedTopic)
      return showMessage("Please enter a topic name", "error");
    const question = window.prompt("Ask a question about your notes:");
    if (!question) return;

    setLoading(true);
    try {
      const res = await fetch(`${BASE_URL}/api/notes/ask-ai`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: trimmedTopic, question }),
      });
      const data = await res.json();
      if (data.success) {
        setAiResponseHTML(
          `<div class="ai-response ai-question">
            <h3>💬 AI Answer on ${trimmedTopic}</h3>
            <p><strong>Q:</strong> ${escapeHtml(question)}</p>
            <div class="ai-answer-content">${marked.parse(data.answer)}</div>
           </div>`
        );
        showMessage("AI answered your question!", "success");
      } else {
        showMessage(data.message || "AI failed", "error");
      }
    } catch (err) {
      showMessage("Error asking AI: " + err.message, "error");
    } finally {
      setLoading(false);
    }
  };

  const generateFlashcards = async () => {
    // ... (generateFlashcards logic remains the same)
    const trimmedTopic = topic.trim();
    if (!trimmedTopic)
      return showMessage("Please enter a topic name", "error");
    setLoading(true);
    try {
      const res = await fetch(`${BASE_URL}/api/notes/flashcards`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: trimmedTopic }),
      });
      const data = await res.json();
      if (data.success) {
        // Flashcard data is structured, no need for marked.parse here, 
        // but we ensure the output is safe.
        const flashcardsHTML = Array.isArray(data.flashcards)
          ? data.flashcards
              .map(
                (card, i) =>
                  `<div class="flashcard">
                    <strong>Card ${i + 1}:</strong>
                    <p><strong>Front:</strong> ${escapeHtml(card.front)}</p>
                    <p><strong>Back:</strong> ${escapeHtml(card.back)}</p>
                  </div>`
              )
              .join("")
          : "<div style='text-align:center;'>No flashcards returned</div>";
        setAiResponseHTML(
          `<div class="ai-response ai-flashcards">
            <h3>📇 Flashcards for ${trimmedTopic}</h3>
            ${flashcardsHTML}
          </div>`
        );
        showMessage("Flashcards generated!", "success");
      } else {
        showMessage(data.message || "Flashcards generation failed", "error");
      }
    } catch (err) {
      showMessage("Error generating flashcards: " + err.message, "error");
    } finally {
      setLoading(false);
    }
  };

  /* -------- Voice Note (Requires a new type of connection - currently disabled) -------- */
  const recordVoiceNote = () => {
    showMessage("Voice Note feature requires complex file/audio handling and is not yet implemented on the frontend.", "warning");
    // To implement this, you would need to use a library to access the user's microphone
    // and send the resulting audio file to a dedicated file upload endpoint on the backend.
  };

  /* -------- Render Method (UI) -------- */
  return (
    <div className="notes-page">

      <div className="container">
        <Card className="card main-card">
          <h1>
            Manage Your Notes{" "}
            <span className="ai-badge">🤖 AI Powered by Gemini</span>
          </h1>

          {message && (
            <div className={`message ${message.type}`}>{message.text}</div>
          )}

          <div className="form-group">
            <label htmlFor="topic">📚 Topic Name:</label>
            <Input
              id="topic"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Enter topic (e.g., Python, Biology, History)"
            />
          </div>

          <div className="form-group">
            <label htmlFor="note">✍️ Note Content:</label>
            <textarea
              id="note"
              value={noteText}
              onChange={(e) => setNoteText(e.target.value)}
              placeholder="Enter your note here..."
            />
          </div>

          <div className="checkbox-group">
            <input
              id="useAI"
              type="checkbox"
              checked={useAI}
              onChange={(e) => setUseAI(e.target.checked)}
            />
            <label htmlFor="useAI" style={{ margin: 0 }}>
              🤖 Enhance with AI (improve grammar, formatting, and clarity)
            </label>
          </div>

          <div className="button-group main-actions">
            <Button onClick={addNote} disabled={loading}>
              <FiPlus /> Add Note
            </Button>
            <Button variant="secondary" onClick={viewNotes} disabled={loading}>
              <FiEye /> View Notes
            </Button>
            <Button variant="secondary" onClick={searchNotes} disabled={loading}>
              <FiSearch /> Search Notes
            </Button>
          </div>
          
          <hr style={{ margin: '15px 0', borderTop: '1px dashed #ddd' }} />
          
          <div className="button-group ai-actions">
             <Button variant="info" onClick={summarizeNotes} disabled={loading}>
                <FiBookOpen /> Summarize
            </Button>
            <Button variant="info" onClick={askAI} disabled={loading}>
                <FiMessageSquare /> Ask AI
            </Button>
            <Button variant="info" onClick={generateFlashcards} disabled={loading}>
                <FiLayers /> Flashcards
            </Button>
            {/* Disabled until complex file upload logic is added */}
            <Button variant="warning" onClick={recordVoiceNote} disabled={loading}> 
                <FiMic /> Voice Note (TBD)
            </Button>
          </div>

          {loading && (
            <div className="loading" role="status" aria-live="polite">
              <div className="spinner" />
              <p>AI is working...</p>
            </div>
          )}
        </Card>

        {aiResponseHTML && (
            <Card className="card ai-result-card">
                <div dangerouslySetInnerHTML={{ __html: aiResponseHTML }} />
            </Card>
        )}

       <Card
          className="card notes-card"
          style={{ display: notesVisible ? "block" : "none" }}
        >
          <h2>Your Notes for {topic}</h2>
          <div className="notes-list">
            {/* 🛑 FIX: Call the helper function to render notes, 
                   instead of putting logic directly in JSX */}
            {renderConsolidatedNotes(notes, topic, editNote, deleteNote)}
          </div>
        </Card>
        
        
      </div> 
    </div>
  );
}