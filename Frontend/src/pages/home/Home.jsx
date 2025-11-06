import React from "react";
import { FaBook, FaNotesMedical, FaSearch, FaCloudUploadAlt, FaBrain } from "react-icons/fa";
import Card from "../../components/common/Card/Card.jsx";
import "./home.css";

const features = [
  {
    icon: <FaBook />,
    title: "Smart Notes",
    desc: "Create, manage, and enhance your notes with AI. Get automatic summaries, flashcards, and answers to your questions.",
    badge: "🤖 AI Powered",
    link: "/notes",
  },
  {
    icon: <FaCloudUploadAlt />,
    title: "Drive Manager",
    desc: "Upload files, add links, and organize all your study materials. Generate AI study plans for better learning.",
    badge: "☁️ Cloud Storage",
    link: "/drive",
  },
  {
    icon: <FaSearch />,
    title: "Smart Search",
    desc: "Search the web with AI suggestions, find files on your PC, manage to-do lists, and track study time.",
    badge: "✨ AI Enhanced",
    link: "/search",
  },
  {
    icon: <FaNotesMedical />,
    title: "Health Tracker",
    desc: "Get health information, symptom analysis, wellness tips, and mental health support from AI.",
    badge: "🩺 Medical Info",
    link: "/health",
  },
  {
    icon: <FaBrain />,
    title: "Quiz Generator",
    desc: "Generate quizzes from your notes or any topic. Get instant AI feedback and track your performance.",
    badge: "📊 Performance Tracking",
    link: "/quiz",
  },
];

export default function Home() {
  return (
    <div className="home-container">
     
      <main className="home-content">
        <div className="features-grid">
          {features.map((f, i) => (
            <a href={f.link} key={i} className="feature-link">
              <Card className="feature-card">
                <div className="feature-icon">{f.icon}</div>
                <h2>{f.title}</h2>
                <p>{f.desc}</p>
                <span className="badge">{f.badge}</span>
              </Card>
            </a>
          ))}
        </div>
      </main>
    </div>
  );
}
