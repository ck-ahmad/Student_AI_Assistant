import React, { useState } from "react";
import Card from "../../components/common/Card/Card";
import Button from "../../components/common/Button/Button";
import Input from "../../components/common/Input/Input";
import "./notes.css";

export default function Notes() {
  const [topic, setTopic] = useState("");
  const [noteText, setNoteText] = useState("");
  const [useAI, setUseAI] = useState(true);

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null); // { type: 'success'|'error', text }
  const [notes, setNotes] = useState([]);
  const [notesVisible, setNotesVisible] = useState(false);
  const [aiResponseHTML, setAiResponseHTML] = useState("");

  const showMessage = (text, type = "success") => {
    setMessage({ text, type });
    window.clearTimeout(showMessage._t);
    showMessage._t = setTimeout(() => setMessage(null), 4500);
  };

  /* -------- API actions (replace endpoints later) -------- */

  const addNote = async () => {
    const trimmedTopic = topic.trim();
    const trimmedNote = noteText.trim();
    if (!trimmedTopic || !trimmedNote) return showMessage("Please enter both topic and note", "error");

    setLoading(true);
    try {
      const res = await fetch("/api/notes/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: trimmedTopic, note: trimmedNote, use_ai: useAI }),
      });
      const data = await res.json();
      if (data.success) {
        showMessage(data.message || "Note added", "success");
        setNoteText("");
        // If API returned enhanced note, optionally show short preview message
        if (useAI && data.enhanced_note) {
          showMessage("AI Enhanced: " + data.enhanced_note.slice(0, 120) + "...", "success");
        }
        await viewNotes(); // refresh list
      } else {
        showMessage(data.message || "Failed to add note", "error");
      }
    } catch (err) {
      showMessage("Error adding note: " + err.message, "error");
    } finally {
      setLoading(false);
    }
  };

  const viewNotes = async () => {
    const trimmedTopic = topic.trim();
    if (!trimmedTopic) return showMessage("Please enter a topic name", "error");

    setLoading(true);
    try {
      const res = await fetch("/api/notes/view", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: trimmedTopic }),
      });
      const data = await res.json();
      if (data.success) {
        setNotes(Array.isArray(data.notes) ? data.notes : []);
        setNotesVisible(true);
      } else {
        showMessage(data.message || "Failed to load notes", "error");
      }
    } catch (err) {
      showMessage("Error viewing notes: " + err.message, "error");
    } finally {
      setLoading(false);
    }
  };

  const deleteNote = async (id) => {
    const trimmedTopic = topic.trim();
    if (!trimmedTopic) return showMessage("Please enter a topic name", "error");
    if (!window.confirm("Are you sure you want to delete this note?")) return;

    setLoading(true);
    try {
      const res = await fetch("/api/notes/delete", {
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
    const trimmedTopic = topic.trim();
    if (!trimmedTopic) return showMessage("Please enter a topic name", "error");

    const newText = window.prompt("Enter the updated note:");
    if (!newText) return;

    const enhance = window.confirm("Enhance with AI?");
    setLoading(true);
    try {
      const res = await fetch("/api/notes/edit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: trimmedTopic, note_id: id, new_text: newText, use_ai: enhance }),
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
    const trimmedTopic = topic.trim();
    if (!trimmedTopic) return showMessage("Please enter a topic name", "error");
    const keyword = window.prompt("Enter keyword to search:");
    if (!keyword) return;

    setLoading(true);
    try {
      const res = await fetch("/api/notes/search", {
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

  /* -------- AI features -------- */

  const summarizeNotes = async () => {
    const trimmedTopic = topic.trim();
    if (!trimmedTopic) return showMessage("Please enter a topic name", "error");
    setLoading(true);
    try {
      const res = await fetch("/api/notes/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: trimmedTopic }),
      });
      const data = await res.json();
      if (data.success) {
        setAiResponseHTML(`<div class="ai-response"><h3>📋 Summary</h3>${data.summary}</div>`);
        showMessage("Summary generated!", "success");
      } else {
        showMessage(data.message || "Summary failed", "error");
      }
    } catch (err) {
      showMessage("Error: " + err.message, "error");
    } finally {
      setLoading(false);
    }
  };

  const askAI = async () => {
    const trimmedTopic = topic.trim();
    if (!trimmedTopic) return showMessage("Please enter a topic name", "error");
    const question = window.prompt("Ask a question about your notes:");
    if (!question) return;

    setLoading(true);
    try {
      const res = await fetch("/api/notes/ask-ai", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: trimmedTopic, question }),
      });
      const data = await res.json();
      if (data.success) {
        setAiResponseHTML(
          `<div class="ai-response"><h3>💬 AI Answer</h3><p><strong>Q:</strong> ${escapeHtml(
            question
          )}</p><p><strong>A:</strong> ${data.answer}</p></div>`
        );
        showMessage("AI answered your question!", "success");
      } else {
        showMessage(data.message || "AI failed", "error");
      }
    } catch (err) {
      showMessage("Error: " + err.message, "error");
    } finally {
      setLoading(false);
    }
  };

  const generateFlashcards = async () => {
    const trimmedTopic = topic.trim();
    if (!trimmedTopic) return showMessage("Please enter a topic name", "error");
    setLoading(true);
    try {
      const res = await fetch("/api/notes/flashcards", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: trimmedTopic }),
      });
      const data = await res.json();
      if (data.success) {
        const flashcardsHTML = Array.isArray(data.flashcards)
          ? data.flashcards
              .map(
                (card, i) =>
                  `<div class="flashcard"><strong>Card ${i + 1}</strong><br><strong>Front:</strong> ${escapeHtml(
                    card.front
                  )}<br><strong>Back:</strong> ${escapeHtml(card.back)}</div>`
              )
              .join("")
          : "<div>No flashcards returned</div>";
        setAiResponseHTML(`<div class="ai-response"><h3>📇 Flashcards Generated</h3>${flashcardsHTML}</div>`);
        showMessage("Flashcards generated!", "success");
      } else {
        showMessage(data.message || "Flashcards generation failed", "error");
      }
    } catch (err) {
      showMessage("Error: " + err.message, "error");
    } finally {
      setLoading(false);
    }
  };

  /* helper: escape for safe injection of small strings (we still use result HTML returned by API as-is) */
  const escapeHtml = (str) =>
    String(str)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");

  return (
    <div className="notes-page">
      <nav className="navbar">
        <a href="/">← Back to Home</a>
        <h2>📝 AI-Powered Smart Notes</h2>
      </nav>

      <div className="container">
        <Card className="card main-card">
          <h1>
            Manage Your Notes <span className="ai-badge">🤖 AI Powered by Gemini</span>
          </h1>

          {message && <div className={`message ${message.type}`}>{message.text}</div>}

          <div className="form-group">
            <label htmlFor="topic">📚 Topic Name:</label>
            <Input id="topic" value={topic} onChange={(e) => setTopic(e.target.value)} placeholder="Enter topic (e.g., Python, Biology, History)" />
          </div>

          <div className="form-group">
            <label htmlFor="note">✍️ Note Content:</label>
            <textarea id="note" value={noteText} onChange={(e) => setNoteText(e.target.value)} placeholder="Enter your note here..." />
          </div>

          <div className="checkbox-group">
            <input id="useAI" type="checkbox" checked={useAI} onChange={(e) => setUseAI(e.target.checked)} />
            <label htmlFor="useAI" style={{ margin: 0 }}>
              🤖 Enhance with AI (improve grammar, formatting, and clarity)
            </label>
          </div>

          <div className="button-group">
            <Button onClick={addNote} disabled={loading}>
              ✅ Add Note
            </Button>
            <Button variant="secondary" onClick={viewNotes} disabled={loading}>
              👁️ View Notes
            </Button>
            <Button variant="secondary" onClick={searchNotes} disabled={loading}>
              🔍 Search
            </Button>
          </div>

          {loading && (
            <div className="loading" role="status" aria-live="polite">
              <div className="spinner" />
              <p>AI is working...</p>
            </div>
          )}
        </Card>

        <Card className="card notes-card" style={{ display: notesVisible ? "block" : "none" }}>
          <h2>Your Notes</h2>
          <div className="notes-list">
            {notes.length === 0 ? (
              <p style={{ textAlign: "center", color: "var(--text-secondary, #666)" }}>No notes found for this topic.</p>
            ) : (
              notes.map((n) => (
                <div className="note-item" key={n.id}>
                  <div className="note-text">{n.text}</div>
                  <div className="note-actions">
                    <Button onClick={() => editNote(n.id)}>✏️ Edit</Button>
                    <Button variant="danger" onClick={() => deleteNote(n.id)}>
                      🗑️ Delete
                    </Button>
                  </div>
                </div>
              ))
            )}
          </div>
        </Card>

        <Card className="card ai-section-card">
          <h2>🤖 AI Features</h2>
          <div className="button-group">
            <Button className="btn-ai" onClick={summarizeNotes} disabled={loading}>
              📋 Summarize All Notes
            </Button>
            <Button className="btn-ai" onClick={askAI} disabled={loading}>
              💬 Ask AI About Notes
            </Button>
            <Button className="btn-ai" onClick={generateFlashcards} disabled={loading}>
              📇 Generate Flashcards
            </Button>
          </div>

          <div id="aiResponse" dangerouslySetInnerHTML={{ __html: aiResponseHTML }} />
        </Card>
      </div>
    </div>
  );
}
