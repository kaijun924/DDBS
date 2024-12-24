import React, { useState, useEffect } from "react";
import axios from "axios";
import { Container, Row, Col, Card, Button } from "react-bootstrap";
import "./ArticleList.css"; // Import custom styles
import { useNavigate } from "react-router-dom";

function ArticleList() {
  const [scienceArticles, setScienceArticles] = useState([]);
  const [technologyArticles, setTechnologyArticles] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch science articles
    axios
      .post("http://localhost:8000/articles/category?category=science&count=100&offset=0", {}, {
        headers: {
          "Content-Type": "application/json",
        },
      })
      .then((response) => setScienceArticles(response.data))
      .catch((error) => console.error("Error fetching science articles:", error));

    // Fetch technology articles
    axios
      .post("http://localhost:8000/articles/category?category=technology&count=100&offset=0", {}, {
        headers: {
          "Content-Type": "application/json",
        },
      })
      .then((response) => setTechnologyArticles(response.data))
      .catch((error) => console.error("Error fetching technology articles:", error));
  }, []);

  const handleArticleClick = (aid) => {
    navigate(`/article/${aid}`);
  };

  const renderArticle = (article) => (
    <div key={article.id} className="article-row">
      <Card className="mb-3">
        <Card.Body>
          <Card.Title>
            <div className="d-flex justify-content-between">
              <div className="article-title">{article.title}</div>
              <div className="article-icons">
                {article.text && <span className="icon text-icon">📄</span>}
                {article.image && <span className="icon image-icon">🖼️</span>}
                {article.video && <span className="icon video-icon">🎥</span>}
              </div>
            </div>
          </Card.Title>
          <Card.Text>
            <p><strong>Category:</strong> {article.category}</p>
            <p><strong>Abstract:</strong> {article.abstract}</p>
            <p><strong>Tags:</strong> {article.articleTags}</p>
            <p><strong>Authors:</strong> {article.authors}</p>
            <p><strong>Language:</strong> {article.language}</p>
          </Card.Text>
          <Button variant="primary" onClick={() => handleArticleClick(article.aid)}>
            Read More
          </Button>
        </Card.Body>
      </Card>
    </div>
  );

  return (
    <Container className="my-4">
      <Row>
        {/* Left Panel: Science */}
        <Col md={6}>
          <div className="panel">
            <h2>Science Articles</h2>
            {scienceArticles.length > 0 ? (
              scienceArticles.map((article) => renderArticle(article))
            ) : (
              <p>Loading science articles...</p>
            )}
          </div>
        </Col>

        {/* Right Panel: Technology */}
        <Col md={6}>
          <div className="panel">
            <h2>Technology Articles</h2>
            {technologyArticles.length > 0 ? (
              technologyArticles.map((article) => renderArticle(article))
            ) : (
              <p>Loading technology articles...</p>
            )}
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default ArticleList;
