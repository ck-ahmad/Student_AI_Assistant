// ==================== Search.jsx ====================
import React, { useState, useEffect } from 'react';
import { api } from "../../services/api.js"; 
import './search.css'; 

import Card from '../../components/common/Card/Card'
import Button from '../../components/common/Button/Button'

// --- Component ---
const Search = () => {
    const [activeTab, setActiveTab] = useState('web');
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedEngine, setSelectedEngine] = useState({ engine: 'google', feature: 'search' });
    const [aiSuggestions, setAiSuggestions] = useState(null);
    const [newTask, setNewTask] = useState('');
    const [tasks, setTasks] = useState([]);
    const [taskSuggestions, setTaskSuggestions] = useState(null);
    const [timerDisplay, setTimerDisplay] = useState(null);

    // Timer Settings
    const [workDuration, setWorkDuration] = useState(25);
    const [breakDuration, setBreakDuration] = useState(5);
    const [sessions, setSessions] = useState(4);


    // --- General Handlers ---
    const switchTab = (tab) => {
        setActiveTab(tab);
        setAiSuggestions(null); 
        setTaskSuggestions(null);
        setTimerDisplay(null);
    };

    const selectEngine = (engine, feature) => {
        setSelectedEngine({ engine, feature });
    };

    // --- Web Search Handlers ---
    const getAISuggestions = async () => {
        if (!searchQuery) {
            alert('Please enter a search query');
            return;
        }
        
        try {
            const response = await api.post('/search/suggestions', { query: searchQuery });
            
            if (response.data.success) {
                setAiSuggestions(response.data);
            } else {
                alert('Error getting AI suggestions: ' + response.data.message);
            }
        } catch (error) {
            alert('API Error during suggestions request. See console for details.');
            console.error(error);
        }
    };

    const webSearch = async () => {
        if (!searchQuery) {
            alert('Please enter a search query');
            return;
        }

        const body = {
            query: searchQuery,
            engine: selectedEngine.engine,
            feature: selectedEngine.feature,
        };
        
        try {
            const response = await api.post('/search/web', body);
            const result = response.data;

            if (result.success && result.url) {
                window.open(result.url, '_blank');
            } else {
                alert('Error performing web search: ' + result.message);
            }
        } catch (error) {
            alert('API Error during web search request. See console for details.');
            console.error(error);
        }
    };

    // --- To-Do List Handlers ---
    const loadTasks = async () => {
        try {
            const response = await api.post('/todo/manage', { action: 'list' });
            const data = response.data;

            if (data.success) {
                const sortedTasks = data.tasks.sort((a, b) => (a.completed === b.completed ? 0 : a.completed ? 1 : -1));
                setTasks(sortedTasks);
            }
        } catch (error) {
            console.error('API Error loading tasks:', error);
        }
    };

    useEffect(() => {
        loadTasks();
    }, []);

    const addTask = async () => {
        if (!newTask) {
            alert('Please enter a task');
            return;
        }

        try {
            const response = await api.post('/todo/manage', { 
                action: 'add', 
                task: newTask 
            });
            
            if (response.data.success) {
                setNewTask('');
                loadTasks();
            } else {
                alert('Error adding task: ' + response.data.message);
            }
        } catch (error) {
            alert('API Error adding task. See console for details.');
            console.error(error);
        }
    };

    const completeTask = async (taskId) => {
        try {
            const response = await api.post('/todo/manage', { 
                action: 'complete', 
                task_id: taskId 
            });
            
            if (response.data.success) {
                loadTasks();
            } else {
                alert('Error completing task: ' + response.data.message);
            }
        } catch (error) {
            alert('API Error completing task. See console for details.');
            console.error(error);
        }
    };

    const deleteTask = async (taskId) => {
        if (!window.confirm('Delete this task?')) return;
        
        try {
            const response = await api.post('/todo/manage', { 
                action: 'delete', 
                task_id: taskId 
            });
            
            if (response.data.success) {
                loadTasks();
            } else {
                alert('Error deleting task: ' + response.data.message);
            }
        } catch (error) {
            alert('API Error deleting task. See console for details.');
            console.error(error);
        }
    };
    
    // Function to get AI Prioritization
    const getTaskSuggestions = async () => {
        const pendingCount = tasks.filter(t => !t.completed).length;

        if (pendingCount === 0) {
            alert('Add some *pending* tasks first to get AI suggestions!');
            return;
        }
        
        try {
            // Call the dedicated /api/todo/prioritize route with an empty body
            const response = await api.post('/todo/prioritize', {}); 
            const aiResult = response.data;

            if (aiResult.success) {
                setTaskSuggestions(aiResult);
            } else {
                alert('Error getting AI task suggestions: ' + aiResult.message);
            }
        } catch (error) {
            alert('API Error getting task suggestions. Check if Flask server is running and API Key is valid.');
            console.error(error);
        }
    }

    // --- Study Timer Handlers ---
    const startTimer = () => {
        setTimerDisplay({
            workMinutes: workDuration,
            breakMinutes: breakDuration,
            sessions: sessions
        });
    };

    // --- JSX Renderers ---

    const renderWebSearchTab = () => (
        <div id="web-tab" className={`tabContent ${activeTab === 'web' ? 'active' : ''}`}>
            <div className="searchBox"> 
                <input
                    type="text"
                    id="search-query"
                    className="searchInput" 
                    placeholder="What do you want to search for?"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    onKeyPress={(e) => { if (e.key === 'Enter') webSearch(); }}
                />
                <Button onClick={webSearch}>🔍 Search</Button>
                <Button onClick={getAISuggestions} variant="secondary">💡 AI Suggestions</Button>
            </div>

            <div className="formGroup"> 
                <label>Search Engine & Type:</label>
                <div className="engineSelector"> 
                    {[
                        { engine: 'google', feature: 'search', label: '🔍 Google Search' },
                        { engine: 'google', feature: 'scholar', label: '🎓 Google Scholar' },
                        { engine: 'google', feature: 'images', label: '🖼️ Google Images' },
                        { engine: 'google', feature: 'videos', label: '📺 YouTube' },
                        { engine: 'bing', feature: 'search', label: '🔍 Bing Search' },
                    ].map((item, index) => (
                        <div
                            key={index}
                            className={`engineBtn ${selectedEngine.engine === item.engine && selectedEngine.feature === item.feature ? 'active' : ''}`} 
                            onClick={() => selectEngine(item.engine, item.feature)}
                        >
                            {item.label}
                        </div>
                    ))}
                </div>
            </div>

            {aiSuggestions && (
                <div id="suggestions-container">
                    <div className="suggestionBox"> 
                        <h3>🤖 AI Search Suggestions</h3>
                        <div style={{ whiteSpace: 'pre-wrap' }}>{aiSuggestions.suggestions}</div> 
                        <hr style={{ margin: '15px 0', border: 'none', borderTop: '1px solid #ccc' }} />
                        <p><strong>Quick Links:</strong></p>
                        <div style={{ marginTop: '10px' }}>
                            <Button variant="primary" onClick={() => window.open(aiSuggestions.google_url, '_blank')} style={{ marginRight: '10px' }}>Google</Button>
                            <Button variant="secondary" onClick={() => window.open(aiSuggestions.scholar_url, '_blank')} style={{ marginRight: '10px' }}>Scholar</Button>
                            <Button variant="secondary" onClick={() => window.open(aiSuggestions.youtube_url, '_blank')}>YouTube</Button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );

    const renderToDoTab = () => (
        <div id="todo-tab" className={`tabContent ${activeTab === 'todo' ? 'active' : ''}`}> 
            <h2>📝 Task Manager</h2>
            <p style={{ color: '#666', marginBottom: '20px' }}>Organize your study tasks and assignments</p>
            
            <div className="searchBox"> 
                <input
                    type="text"
                    id="new-task"
                    className="searchInput" 
                    placeholder="Add a new task..."
                    value={newTask}
                    onChange={(e) => setNewTask(e.target.value)}
                    onKeyPress={(e) => { if (e.key === 'Enter') addTask(); }}
                />
                <Button onClick={addTask}>➕ Add Task</Button>
            </div>


<div className="todoControls" style={{ marginBottom: '20px' }}>
    <Button variant="secondary" onClick={loadTasks} style={{ marginRight: '10px' }}>🔄 Refresh</Button>
    <Button variant="secondary" onClick={getTaskSuggestions}>💡 AI Prioritization</Button>
</div>

            <div id="tasks-container" style={{ marginTop: '20px' }}>
                {tasks.length === 0 ? (
                    <p style={{ textAlign: 'center', color: '#666', padding: '20px' }}>No tasks yet. Add some tasks to get started!</p>
                ) : (
                    tasks.map(task => (
                        <div key={task.id} 
                            className={`todoItem ${task.completed ? 'completed' : ''}`}> 
                            <div>
                                <strong>{task.task}</strong>
                                <div style={{ fontSize: '0.9em', color: '#666', marginTop: '5px' }}>
                                    Added: {new Date(task.created_at).toLocaleString()}
                                </div>
                            </div>
                            <div className="todoActions"> 
                                {!task.completed && (
                                    <Button variant="primary" onClick={() => completeTask(task.id)}>✓ Complete</Button>
                                )}
                                <Button variant="secondary" onClick={() => deleteTask(task.id)}>🗑️ Delete</Button>
                            </div>
                        </div>
                    ))
                )}
            </div>
            
            {taskSuggestions && (
                <div id="task-suggestions">
                    <div className="suggestionBox" style={{ marginTop: '20px' }}> 
                        <h3>💡 AI Task Prioritization</h3>
                        <div style={{ whiteSpace: 'pre-wrap' }}>{taskSuggestions.suggestions}</div>
                    </div>
                </div>
            )}
        </div>
    );

    const renderTimerTab = () => (
        <div id="timer-tab" className={`tabContent ${activeTab === 'timer' ? 'active' : ''}`}> 
            <h2>⏱️ Pomodoro Study Timer</h2>
            <p style={{ color: '#666', marginBottom: '20px' }}>Use the Pomodoro Technique to boost your productivity</p>

            <div className="formGroup"> 
                <label htmlFor="work-duration">Work Duration (minutes):</label>
                <select id="work-duration" value={workDuration} onChange={(e) => setWorkDuration(e.target.value)}>
                    <option value="15">15 minutes</option>
                    <option value="25">25 minutes (Classic Pomodoro)</option>
                    <option value="30">30 minutes</option>
                    <option value="45">45 minutes</option>
                    <option value="50">50 minutes</option>
                </select>
            </div>

            <div className="formGroup"> 
                <label htmlFor="break-duration">Break Duration (minutes):</label>
                <select id="break-duration" value={breakDuration} onChange={(e) => setBreakDuration(e.target.value)}>
                    <option value="5">5 minutes (Short Break)</option>
                    <option value="10">10 minutes</option>
                    <option value="15">15 minutes (Long Break)</option>
                    <option value="20">20 minutes</option>
                </select>
            </div>

            <div className="formGroup"> 
                <label htmlFor="sessions">Number of Sessions:</label>
                <select id="sessions" value={sessions} onChange={(e) => setSessions(e.target.value)}>
                    <option value="1">1 session</option>
                    <option value="2">2 sessions</option>
                    <option value="3">3 sessions</option>
                    <option value="4">4 sessions (Full Pomodoro Cycle)</option>
                    <option value="6">6 sessions</option>
                </select>
            </div>

            <Button onClick={startTimer} variant="primary" className="btnLg">▶️ Start Study Session</Button> 

            {timerDisplay && (
                <div id="timer-display" className="timerDisplay"> 
                    <h2>⏱️</h2>
                    <h2>Study Timer Started!</h2>
                    {/* The text will now be clearly readable due to CSS fix */}
                    <p style={{ fontSize: '1.2em', margin: '20px 0' }}>
                        {timerDisplay.sessions} session(s) × {timerDisplay.workMinutes} min work + {timerDisplay.breakDuration} min break
                    </p>
                    <hr style={{ margin: '20px 0', border: 'none', borderTop: '1px solid rgba(0,0,0,0.2)' }} />
                    <p style={{ marginTop: '20px' }}>
                        💡 <strong>Tip:</strong> Use a dedicated timer app for accurate timing
                    </p>
                    <p style={{ marginTop: '10px' }}>
                        Recommended: 
                        <a href="https://pomofocus.io" target="_blank" rel="noopener noreferrer">Pomofocus.io</a>
                        or your phone's timer
                    </p>
                </div>
            )}

            <div className="suggestionBox" style={{ marginTop: '30px' }}> 
                <h3>💡 Pomodoro Technique Tips:</h3>
                <ul style={{ marginLeft: '20px', marginTop: '10px', lineHeight: '2' }}>
                    <li>✅ Eliminate all distractions before starting</li>
                    <li>📱 Put your phone on silent or in another room</li>
                    <li>🎯 Focus on **ONE** task during each session</li>
                    <li>☕ Use breaks to rest your eyes and move around</li>
                    <li>🏆 After 4 sessions, take a longer break (15-30 min)</li>
                    <li>📊 Track what you accomplished in each session</li>
                </ul>
            </div>
        </div>
    );

    return (
        <>
           

            <div className="componentContainer"> 
                <Card title="AI-Powered Search & Study Tools">
                    <div className="tabs"> 
                        <button className={`tab ${activeTab === 'web' ? 'active' : ''}`} onClick={() => switchTab('web')}>🌐 Web Search</button> 
                        <button className={`tab ${activeTab === 'todo' ? 'active' : ''}`} onClick={() => switchTab('todo')}>📝 To-Do List</button> 
                        <button className={`tab ${activeTab === 'timer' ? 'active' : ''}`} onClick={() => switchTab('timer')}>⏱️ Study Timer</button> 
                    </div>

                    {renderWebSearchTab()}
                    {renderToDoTab()}
                    {renderTimerTab()}
                </Card>
            </div>
        </>
    );
};

export default Search;