import React, { useState, useEffect } from "react";
import {
  FiBookOpen,
  FiLoader,
  FiCheckCircle,
  FiXCircle,
  FiArrowRight,
  FiRepeat,
  FiSend,
} from "react-icons/fi";
import "./Quizz.css";

export default function Quiz() {
  const [step, setStep] = useState("setup"); // setup | loading | quiz | result
  const [topic, setTopic] = useState("");
  const [difficulty, setDifficulty] = useState("medium");
  const [numQuestions, setNumQuestions] = useState(5);
  const [questions, setQuestions] = useState([]);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState({});
  const [score, setScore] = useState(0);

  // Mock API call
  const generateQuiz = async () => {
    setStep("loading");
    await new Promise((res) => setTimeout(res, 1200)); // mock delay
    const mockData = Array.from({ length: numQuestions }).map((_, i) => ({
      id: i,
      question: `Question ${i + 1}: What does "${topic}" mean in AI context?`,
      options: ["Definition A", "Definition B", "Definition C", "Definition D"],
      correct: Math.floor(Math.random() * 4),
    }));
    setQuestions(mockData);
    setStep("quiz");
  };

  const handleAnswer = (qId, index) => {
    setAnswers({ ...answers, [qId]: index });
  };

  const nextQuestion = () => {
    if (current < questions.length - 1) {
      setCurrent(current + 1);
    } else {
      showResults();
    }
  };

  const showResults = () => {
    let total = 0;
    questions.forEach((q) => {
      if (answers[q.id] === q.correct) total++;
    });
    setScore(total);
    setStep("result");
  };

  const restartQuiz = () => {
    setStep("setup");
    setTopic("");
    setAnswers({});
    setQuestions([]);
    setCurrent(0);
    setScore(0);
  };

  return (
    <div className="quiz-page">
      <div className="quiz-header">
        <h2>
          <FiBookOpen className="icon-accent" /> AI Quiz Generator
        </h2>
      </div>
      <div className="card">
            {step === "setup" && (
        <div className="quiz-section">
          <h3>🎯 Generate a New Quiz</h3>
          <div className="form-group">
            <label>Topic</label>
            <input
              type="text"
              placeholder="e.g., Machine Learning, Neural Networks"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label>Difficulty</label>
            <select
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
            >
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>

          <div className="form-group">
            <label>Number of Questions</label>
            <input
              type="number"
              min="1"
              max="20"
              value={numQuestions}
              onChange={(e) => setNumQuestions(Number(e.target.value))}
            />
          </div>

          <button
            className="btn primary"
            disabled={!topic.trim()}
            onClick={generateQuiz}
          >
            <FiSend /> Generate Quiz
          </button>
        </div>
      )}

      {step === "loading" && (
        <div className="quiz-loading">
          <FiLoader className="spin icon-accent" size={40} />
          <p>Generating your quiz...</p>
        </div>
      )}

      {step === "quiz" && questions.length > 0 && (
        <div className="quiz-section">
          <h3>{questions[current].question}</h3>
          <div className="options">
            {questions[current].options.map((opt, i) => (
              <button
                key={i}
                className={`option-btn ${
                  answers[questions[current].id] === i ? "selected" : ""
                }`}
                onClick={() => handleAnswer(questions[current].id, i)}
              >
                {opt}
              </button>
            ))}
          </div>
          <div className="quiz-controls">
            <button className="btn primary" onClick={nextQuestion}>
              {current === questions.length - 1 ? "Finish" : "Next"}{" "}
              <FiArrowRight />
            </button>
          </div>
          <p className="progress">
            Question {current + 1} of {questions.length}
          </p>
        </div>
      )}

      {step === "result" && (
        <div className="quiz-section result">
          <h3>
            {score >= questions.length / 2 ? (
              <FiCheckCircle className="icon-success" />
            ) : (
              <FiXCircle className="icon-error" />
            )}{" "}
            Quiz Completed
          </h3>
          <p>
            Your Score:{" "}
            <strong>
              {score}/{questions.length}
            </strong>
          </p>
          <button className="btn secondary" onClick={restartQuiz}>
            <FiRepeat /> Try Again
          </button>
        </div>
      )}
      </div>

      
    </div>
  );
}
