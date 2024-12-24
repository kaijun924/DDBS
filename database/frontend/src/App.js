import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import UserList from "./pages/UserList";
import UserDetails from "./pages/UserDetails";
import ArticleList from "./pages/ArticleList";
import ArticleDetails from "./pages/ArticleDetails";
import PopularPage from "./pages/PopularPage";
import ReadLog from "./pages/ReadLog";
import Footer from "./components/Footer";

function App() {
  return (
    <Router>
      <div>
        {/* Navigation Bar (if needed) */}
        <Routes>
          <Route path="/" element={<UserList />} />
          <Route path="/user/:id" element={<UserDetails />} />
          <Route path="/articles" element={<ArticleList />} />
          <Route path="/article/:id" element={<ArticleDetails />} />
          <Route path="/popular" element={<PopularPage />} />
          <Route path="/read-log" element={<ReadLog />} />
        </Routes>
        {/* Footer */}
        <Footer />
      </div>
    </Router>
  );
}

export default App;
