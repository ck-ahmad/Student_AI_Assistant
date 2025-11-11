import React, { useState, useRef, useEffect } from "react";
import {
  FaUpload,
  FaLink,
  FaSync,
  FaBook,
  FaTrashAlt,
  FaFileAlt,
  FaDownload,
} from "react-icons/fa";
import Card from "../../components/common/Card/Card";
import Button from "../../components/common/Button/Button";
import Input from "../../components/common/Input/Input";
import { api } from "../../services/api.js";
import "./drive.css";

export default function Drive() {
  const TABS = [
    { id: "upload", label: "Upload File", icon: <FaUpload /> },
    { id: "link", label: "Add Link", icon: <FaLink /> },
    { id: "view", label: "View Files", icon: <FaSync /> },
    { id: "predefined", label: "Course Materials", icon: <FaBook /> },
  ];

  const [activeTab, setActiveTab] = useState("upload");
  const [message, setMessage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [files, setFiles] = useState([]);
  const [filterSemester, setFilterSemester] = useState("");
  const fileInputRef = useRef(null);

  const [uploadMeta, setUploadMeta] = useState({
    semester: "",
    degree: "",
    subject: "",
    description: "",
    useCloud: true,
  });

  const [linkMeta, setLinkMeta] = useState({
    url: "",
    filename: "",
    semester: "",
    degree: "",
    subject: "",
    description: "",
  });

  const [predef, setPredef] = useState({ semester: "", subject: "" });

  useEffect(() => {
    if (activeTab === "view") loadFiles();
  }, [activeTab]);

  const showMessage = (text, type = "success") => {
    setMessage({ text, type });
    setTimeout(() => setMessage(null), 4500);
  };

  // ✅ Upload file handler (unchanged)
  const uploadFile = async () => {
    const file = fileInputRef.current?.files?.[0];
    const { semester, degree, subject, description, useCloud } = uploadMeta;

    if (!file) return showMessage("Please select a file to upload.", "error");
    if (!semester || !degree || !subject)
      return showMessage("Please fill semester, degree and subject.", "error");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("semester", semester);
    formData.append("degree", degree);
    formData.append("subject", subject);
    formData.append("description", description);
    formData.append("use_cloud", useCloud);

    try {
      setLoading(true);
      const { data } = await api.post("/drive/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      if (data.success) {
        showMessage(data.message || "Upload successful", "success");
        if (fileInputRef.current) fileInputRef.current.value = "";
        setUploadMeta({
          semester: "",
          degree: "",
          subject: "",
          description: "",
          useCloud: true,
        });
      } else {
        showMessage(data.message || "Upload failed", "error");
      }
    } catch (err) {
      showMessage("Error uploading file: " + err.message, "error");
    } finally {
      setLoading(false);
    }
  };

  // ✅ Add link handler
  const addLink = async () => {
    const { url, filename, semester, degree, subject, description } = linkMeta;
    if (!url || !semester || !degree || !subject)
      return showMessage("Please fill required fields for link.", "error");

    try {
      setLoading(true);
      const { data } = await api.post("/drive/add-link", {
        link: url,
        filename,
        semester,
        degree,
        subject,
        description,
      });

      if (data.success) {
        showMessage(data.message || "Link added", "success");
        setLinkMeta({
          url: "",
          filename: "",
          semester: "",
          degree: "",
          subject: "",
          description: "",
        });
      } else {
        showMessage(data.message || "Failed to add link", "error");
      }
    } catch (err) {
      showMessage("Error adding link: " + err.message, "error");
    } finally {
      setLoading(false);
    }
  };

  // ✅ Load files
  const loadFiles = async (semester = filterSemester) => {
    try {
      setLoading(true);
      const { data } = await api.post("/drive/list", {
        semester: semester || null,
      });
      if (data.success) {
        setFiles(Array.isArray(data.files) ? data.files : []);
      } else {
        showMessage(data.message || "Failed to load files", "error");
      }
    } catch (err) {
      showMessage("Error loading files: " + err.message, "error");
    } finally {
      setLoading(false);
    }
  };

  // ✅ Delete file
  const deleteFile = async (fileId) => {
    if (!window.confirm("Are you sure you want to delete this file?")) return;
    try {
      setLoading(true);
      const { data } = await api.post("/drive/delete", { file_id: fileId });
      if (data.success) {
        showMessage(data.message || "Deleted", "success");
        loadFiles();
      } else {
        showMessage(data.message || "Delete failed", "error");
      }
    } catch (err) {
      showMessage("Error deleting file: " + err.message, "error");
    } finally {
      setLoading(false);
    }
  };

  // ✅ Predefined materials
  const getPredefinedLink = async () => {
    const { semester, subject } = predef;
    if (!semester || !subject)
      return showMessage("Please select semester and subject", "error");

    try {
      setLoading(true);
      const { data } = await api.post("/drive/predefined", {
        semester,
        subject,
      });
      if (data.success && data.link) {
        window.open(data.link, "_blank");
        showMessage("Opening course materials...", "success");
      } else {
        showMessage(data.message || "Materials not available", "error");
      }
    } catch (err) {
      showMessage("Error: " + err.message, "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="drive-page">
      <main className="drive-container container">
        <Card>
          <header className="drive-header">
            <h1>Manage Your Study Materials</h1>
            <p className="drive-subtitle">
              Upload files, add links, and organize everything in one place.
            </p>
          </header>

          {message && (
            <div className={`message ${message.type}`}>{message.text}</div>
          )}

          {/* ✅ TABS */}
          <div className="tabs" role="tablist">
            {TABS.map((t) => (
              <button
                key={t.id}
                className={`tab ${activeTab === t.id ? "active" : ""}`}
                onClick={() => setActiveTab(t.id)}
              >
                <span className="tab-icon">{t.icon}</span>
                <span className="tab-label">{t.label}</span>
              </button>
            ))}
          </div>

          {/* ✅ UPLOAD TAB */}
             <section className={`tab-panel ${activeTab === "upload" ? "active" : ""}`}>
  <h3>Upload File to Cloud</h3>

  <div className="form-grid">
    <div className="form-group">
      <label>Select File</label>
      <input ref={fileInputRef} type="file" />
    </div>

    <div className="form-group">
      <label>Semester</label>
      <select
        value={uploadMeta.semester}
        onChange={(e) =>
          setUploadMeta((s) => ({ ...s, semester: e.target.value }))
        }
      >
        <option value="">Select Semester</option>
        {[...Array(8)].map((_, i) => (
          <option key={i + 1} value={i + 1}>
            Semester {i + 1}
          </option>
        ))}
      </select>
    </div>

    <div className="form-group">
      <label>Degree</label>
      <select
        value={uploadMeta.degree}
        onChange={(e) =>
          setUploadMeta((s) => ({ ...s, degree: e.target.value }))
        }
      >
        <option value="">Select Degree</option>
        <option value="CS">Computer Science</option>
        <option value="SE">Software Engineering</option>
        <option value="AI">Artificial Intelligence</option>
        <option value="EE">Electrical Engineering</option>
      </select>
    </div>

    <Input
      label="Subject Code"
      placeholder="e.g., PF, OOP, DSA"
      value={uploadMeta.subject}
      onChange={(e) =>
        setUploadMeta((s) => ({ ...s, subject: e.target.value }))
      }
    />

    <div className="form-group full">
      <label>Description (optional)</label>
      <textarea
        rows="3"
        value={uploadMeta.description}
        onChange={(e) =>
          setUploadMeta((s) => ({
            ...s,
            description: e.target.value,
          }))
        }
      />
    </div>

    <div className="form-group checkbox-group">
      <input
        id="use-cloud"
        type="checkbox"
        checked={uploadMeta.useCloud}
        onChange={(e) =>
          setUploadMeta((s) => ({
            ...s,
            useCloud: e.target.checked,
          }))
        }
      />
      <label htmlFor="use-cloud">
        Upload to Cloud Storage (recommended)
      </label>
    </div>
  </div>

  <div className="form-actions">
    <Button onClick={uploadFile}>
      <FaUpload /> Upload File
    </Button>
    <Button
      variant="secondary"
      onClick={() => {
        if (fileInputRef.current) fileInputRef.current.value = "";
      }}
    >
      Clear
    </Button>
  </div>
</section>


          {/* ✅ ADD LINK TAB */}
          <section
            className={`tab-panel ${activeTab === "link" ? "active" : ""}`}
          >
            <h3>Add a Study Link</h3>
            <div className="form-grid">
              <Input
                label="Link URL"
                placeholder="https://example.com/resource"
                value={linkMeta.url}
                onChange={(e) =>
                  setLinkMeta((s) => ({ ...s, url: e.target.value }))
                }
              />
              <Input
                label="File Name (optional)"
                placeholder="Example: Lecture Notes"
                value={linkMeta.filename}
                onChange={(e) =>
                  setLinkMeta((s) => ({ ...s, filename: e.target.value }))
                }
              />
              <select
                value={linkMeta.semester}
                onChange={(e) =>
                  setLinkMeta((s) => ({ ...s, semester: e.target.value }))
                }
              >
                <option value="">Select Semester</option>
                {[...Array(8)].map((_, i) => (
                  <option key={i + 1} value={i + 1}>
                    Semester {i + 1}
                  </option>
                ))}
              </select>
              <select
                value={linkMeta.degree}
                onChange={(e) =>
                  setLinkMeta((s) => ({ ...s, degree: e.target.value }))
                }
              >
                <option value="">Select Degree</option>
                <option value="CS">Computer Science</option>
                <option value="SE">Software Engineering</option>
                <option value="AI">Artificial Intelligence</option>
                <option value="EE">Electrical Engineering</option>
              </select>
              <Input
                label="Subject Code"
                placeholder="e.g., PF, OOP, DSA"
                value={linkMeta.subject}
                onChange={(e) =>
                  setLinkMeta((s) => ({ ...s, subject: e.target.value }))
                }
              />
              <div className="form-group full">
                <label>Description (optional)</label>
                <textarea
                  rows="3"
                  value={linkMeta.description}
                  onChange={(e) =>
                    setLinkMeta((s) => ({
                      ...s,
                      description: e.target.value,
                    }))
                  }
                />
              </div>
            </div>

            <div className="form-actions">
              <Button onClick={addLink}>
                <FaLink /> Add Link
              </Button>
              <Button
                variant="secondary"
                onClick={() =>
                  setLinkMeta({
                    url: "",
                    filename: "",
                    semester: "",
                    degree: "",
                    subject: "",
                    description: "",
                  })
                }
              >
                Clear
              </Button>
            </div>
          </section>

          {/* ✅ VIEW FILES TAB */}
          <section
            className={`tab-panel ${activeTab === "view" ? "active" : ""}`}
          >
            <h3>All Uploaded Files</h3>
            <div className="form-group">
              <label>Filter by Semester</label>
              <select
                value={filterSemester}
                onChange={(e) => setFilterSemester(e.target.value)}
              >
                <option value="">All Semesters</option>
                {[...Array(8)].map((_, i) => (
                  <option key={i + 1} value={i + 1}>
                    Semester {i + 1}
                  </option>
                ))}
              </select>
            </div>

            <Button onClick={() => loadFiles(filterSemester)}>
              <FaSync /> Refresh
            </Button>

            {loading ? (
              <p>Loading files...</p>
            ) : (
              <div className="file-list">
                {files.length === 0 ? (
                  <p>No files available.</p>
                ) : (
                  files.map((f) => (
                    <div key={f.id} className="file-item">
                      <div className="file-info">
                        <div className="file-name">
                          <FaFileAlt /> {f.filename}
                        </div>
                        <div className="file-meta">
                          {f.degree} | Semester {f.semester} | {f.subject}
                        </div>
                        {f.description && (
                          <div className="file-description">
                            {f.description}
                          </div>
                        )}
                      </div>
                      <div className="file-actions">
                        <Button
                          variant="secondary"
                          onClick={() => window.open(f.link, "_blank")}
                        >
                          <FaDownload /> Download
                        </Button>
                        <Button
                          variant="danger"
                          onClick={() => deleteFile(f.id)}
                        >
                          <FaTrashAlt /> Delete
                        </Button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </section>

          {/* ✅ COURSE MATERIALS TAB */}
          <section
            className={`tab-panel ${activeTab === "predefined" ? "active" : ""}`}
          >
            <h3>Access Course Materials</h3>
            <div className="form-grid">
              <div className="form-group">
                <label>Semester</label>
                <select
                  value={predef.semester}
                  onChange={(e) =>
                    setPredef((s) => ({ ...s, semester: e.target.value }))
                  }
                >
                  <option value="">Select Semester</option>
                  {[...Array(8)].map((_, i) => (
                    <option key={i + 1} value={i + 1}>
                      Semester {i + 1}
                    </option>
                  ))}
                </select>
              </div>
              <Input
                label="Subject Code"
                placeholder="e.g., DSA"
                value={predef.subject}
                onChange={(e) =>
                  setPredef((s) => ({ ...s, subject: e.target.value }))
                }
              />
            </div>

            <Button onClick={getPredefinedLink}>
              <FaBook /> Get Materials
            </Button>
          </section>
        </Card>
      </main>
    </div>
  );
}
