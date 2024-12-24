import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

function ArticleList() {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/articles")
      .then((response) => setArticles(response.data))
      .catch((error) => console.error(error));
  }, []);

  return (
    <div>
      <h1>Article List</h1>
      <ul>
        {articles.map(article => (
          <li key={article.id}>
            <Link to={`/article/${article.id}`}>{article.title}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ArticleList;
