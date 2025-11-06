import { useState } from 'react'
import './App.css'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from './pages/home/Home'
import Quizz from './pages/Quizz/Quizz'
import Notes from './pages/Notes/Notes'
import Health from './pages/Health/Health'
//import Search from './pages/Search/Seacrh'
import Drive from './pages/Drive/Drive'
import Layout from './components/Layout/Container/Layout';


function App() {

  return (
    <>
     
     
      <Layout>
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/quizz" element={<Quizz/>} />
          <Route path="/notes" element={<Notes/>} />
          <Route path="/health" element={<Health/>} />
          <Route path="/drive" element={<Drive/>} />
        </Routes>
      </Layout>
   
    </>
  )
}

export default App
