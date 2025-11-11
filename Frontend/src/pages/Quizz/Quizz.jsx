import React, { useState } from "react";
import {
  FiLoader,
  FiCheckCircle,
  FiXCircle,
  FiArrowRight,
  FiRepeat,
  FiSend,
  FiChevronDown,
  FiChevronUp,
} from "react-icons/fi";
// Assuming Card is a common component
import Card from '../../components/common/Card/Card.jsx' 
import { api } from "../../services/api.js"; 
import "./Quizz.css";




export default function Quiz() {
  const [step, setStep] = useState("setup"); // setup | loading | quiz | result
  const [topic, setTopic] = useState("");
  const [difficulty, setDifficulty] = useState("medium");
  const [numQuestions, setNumQuestions] = useState(5);
  const [generatedQuizData, setGeneratedQuizData] = useState(null); 
  const [questions, setQuestions] = useState([]);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState({}); // Stores the index of the option chosen (e.g., {0: 1, 1: 3})
  const [evaluationResult, setEvaluationResult] = useState(null); 
  const [showDetails, setShowDetails] = useState(false); // State for result UI enhancement

  // --- Reset Function ---
  const restartQuiz = () => {
    setStep("setup");
    setTopic("");
    setAnswers({});
    setQuestions([]);
    setGeneratedQuizData(null);
    setEvaluationResult(null);
    setCurrent(0);
    setNumQuestions(5);
    setDifficulty("medium");
    setShowDetails(false);
  };

  // --- API Function: GENERATE QUIZ ---
  const generateQuiz = async () => {
    if (!topic.trim()) return;
    setStep("loading");
    setEvaluationResult(null);

    try {
      const response = await api.post('/quiz/generate-from-topic', {
          topic,
          num_questions: numQuestions,
          difficulty,
          quiz_type: 'mcq'
      });
      
      const data = response.data;

      if (data.success) {
        setGeneratedQuizData(data); 
        // Ensure questions are formatted with a simple ID (index) for answer tracking
        const indexedQuestions = data.questions.map((q, index) => ({
            ...q, 
            id: index // Use index as the unique ID for the frontend answer mapping
        }));
        setQuestions(indexedQuestions);
        setStep("quiz");
      } else {
        console.error("Quiz generation failed:", data.message);
        alert(`Failed to generate quiz: ${data.message}`);
        setStep("setup");
      }
    } catch (error) {
      console.error("API error during generation:", error);
      alert("Network error. Could not connect to the quiz server.");
      setStep("setup");
    }
  };

  // --- Local Functions ---
  const handleAnswer = (qIndex, optionIndex) => {
    setAnswers({ ...answers, [qIndex]: optionIndex });
  };

  const nextQuestion = () => {
    if (current < questions.length - 1) {
      setCurrent(current + 1);
    } else {
      showResults();
    }
  };
  
  // --- API Function: EVALUATE QUIZ ---
  const showResults = async () => {
    setStep("loading");

    // Map the user's selected option index back to the actual text option
    const userAnswersText = questions.map((q, index) => {
        const selectedOptionIndex = answers[index];
        
        // Find the text of the selected option
        return selectedOptionIndex !== undefined && q.options 
            ? q.options[selectedOptionIndex] 
            : ''; 
    });

    try {
      const response = await api.post('/quiz/evaluate', {
          questions: questions, 
          answers: userAnswersText,
          topic: generatedQuizData.topic 
      });

      const data = response.data;
      
      if (data.success) {
        setEvaluationResult(data);
        setStep("result");
      } else {
        console.error("Quiz evaluation failed:", data.message);
        alert(`Failed to evaluate quiz: ${data.message}`);
        setStep("quiz");
      }
    } catch (error) {
      console.error("API error during evaluation:", error);
      alert("Network error. Could not evaluate the quiz.");
      setStep("quiz");
    }
  };

  const hasAnswered = answers[current] !== undefined;

  // --- Render Logic (JSX) ---
  return (
    <div className="quiz-page">
      
      
      <div className="quiz-container"> 
        <Card>
          
          {/* Section Titles */}
          {step === "setup" && (
              <div className="quiz-header">
                <h2>Generate Your Quiz</h2>
                <p className="subtitle">Create AI-powered quizzes from your notes or any topic</p>
              </div>
          )}
          
          {/* STEP: SETUP */}
          {step === "setup" && (
            <div className="quiz-section setup-form">
              <div className="form-group">
                <label>Topic</label>
                <input
                  type="text"
                  placeholder="e.g., Python Programming, Biology, History"
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
                className="btn primary btn-action" 
                disabled={!topic.trim()}
                onClick={generateQuiz}
              >
                <FiSend /> Generate Quiz
              </button>
            </div>
          )}

          {/* STEP: LOADING */}
          {step === "loading" && (
            <div className="quiz-loading">
              {/* Added 'spin' class for animation */}
              <FiLoader className="spin icon-accent" size={40} /> 
              <p>Generating or evaluating your quiz...</p>
            </div>
          )}

          {/* STEP: QUIZ */}
          {step === "quiz" && questions.length > 0 && (
            <div className="quiz-section">
              <h3>{questions[current].question}</h3> 
              <div className="options">
                {questions[current].options.map((opt, i) => (
                  <button
                    key={i}
                    className={`option-btn ${
                      answers[current] === i ? "selected" : "" 
                    }`}
                    onClick={() => handleAnswer(current, i)} 
                  >
                    {opt}
                  </button>
                ))}
              </div>
              <div className="quiz-controls">
                <button 
                  className="btn primary btn-action" 
                  onClick={nextQuestion}
                  disabled={!hasAnswered}
                >
                  {current === questions.length - 1 ? "Finish" : "Next"}{" "}
                  <FiArrowRight />
                </button>
              </div>
              <p className="progress">
                Question {current + 1} of {questions.length}
              </p>
            </div>
          )}

          {/* STEP: RESULT - ENHANCED UI */}
          {step === "result" && evaluationResult && (
            <div className="quiz-section result">
              
              {/* === SCORE SUMMARY === */}
              <div className="score-summary">
                  <h3>
                      {evaluationResult.percentage >= 50 ? (
                          <FiCheckCircle className="icon-success" />
                      ) : (
                          <FiXCircle className="icon-error" />
                      )}{" "}
                      Quiz Completed
                  </h3>
                  <p className="score-text">
                      Your Final Score:{" "}
                      <strong className="score-value">
                          {evaluationResult.score}/{evaluationResult.total}
                      </strong>
                  </p>
                  <p className="percentage-text">
                      Percentage: **{evaluationResult.percentage.toFixed(1)}%**
                  </p>
              </div>

              {/* === OVERALL FEEDBACK === */}
              <div className="overall-feedback-box">
                  <h4>💡 AI Performance Review</h4>
                  <p>{evaluationResult.overall_feedback}</p> 
              </div>
              
              {/* === DETAILED REVIEW TOGGLE === */}
              <div className="review-toggle" onClick={() => setShowDetails(!showDetails)}>
                  <h4>
                      {showDetails ? '▲ Hide Review Details' : '▼ Review All Questions and Feedback'}
                      {showDetails ? <FiChevronUp /> : <FiChevronDown />}
                  </h4>
              </div>

              {/* === DETAILED REVIEW SECTION (CONDITIONAL) === */}
              {showDetails && (
                  <div className="detailed-results">
                      {evaluationResult.results.map((r, index) => (
                          <div key={index} className={`result-item ${r.is_correct ? 'correct' : 'incorrect'}`}>
                              
                              <div className="status-icon">
                                  {r.is_correct ? <FiCheckCircle /> : <FiXCircle />}
                              </div>

                              <div className="result-content">
                                  <h5>Q{index + 1}: {r.question} 
                                      <span className="q-type">[{r.type}]</span>
                                  </h5>
                                  
                                  <p className="user-answer">
                                      **Your Answer:** {r.user_answer || '*No Answer*'}
                                  </p>
                                  
                                  {!r.is_correct && (
                                      <p className="correct-answer">
                                          **Correct Answer:** {r.correct_answer}
                                      </p>
                                  )}
                                  
                                  <div className="feedback-box">
                                      **Feedback:** {r.feedback}
                                  </div>
                              </div>
                          </div>
                      ))}
                  </div>
              )}
              
              <button 
                className="btn secondary btn-action" 
                onClick={restartQuiz}
              >
                <FiRepeat /> Try Another Quiz
              </button>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}