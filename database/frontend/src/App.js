import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import UserList from "./pages/UserList";
import UserDetails from "./pages/UserDetails";
import ArticleList from "./pages/ArticleList";
import ArticleDetails from "./pages/ArticleDetails";
import PopularPage from "./pages/PopularPage";
import Footer from "./components/Footer";
import NavBar from "./components/NavBar";

function App() {
  return (
    <Router>
      <div>
        <NavBar />
        <Routes>
          <Route path="/" element={<UserList />} />
          <Route path="/users" element={<UserList />} />
          <Route path="/user/:uid" element={<UserDetails />} />
          <Route path="/articles" element={<ArticleList />} />
          <Route path="/article/:aid" element={<ArticleDetails />} />
          <Route path="/popular" element={<PopularPage />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
