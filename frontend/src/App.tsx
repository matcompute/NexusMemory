import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import MemoryPage from './pages/MemoryPage'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MemoryPage />} />
      </Routes>
    </Router>
  )
}

export default App
