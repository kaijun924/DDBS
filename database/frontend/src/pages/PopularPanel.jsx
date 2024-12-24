import React, { useState } from "react";
import "./PopularPanel.css"; // Import custom styles

const PopularPanel = ({ title, data, loading }) => {
  const [showMoreIndex, setShowMoreIndex] = useState({});

  const handleShowMore = (id) => {
    setShowMoreIndex((prev) => ({ ...prev, [id]: true }));
  };

  const handleArticleClick = (aid) => {
    window.location.href = `/article/${aid}`; // Navigate to article details page
  };

  return (
    <div className="popular-panel">
      <h2 className="text-center mb-3">{title}</h2>
      {loading ? (
        <p>Loading {title.toLowerCase()}...</p>
      ) : (
        data.map((entry) => {
          const showAll = showMoreIndex[entry.id];
          const formattedTimestamp = new Date(parseInt(entry.timestamp))
            .toISOString()
            .split("T")[0]; // Convert to YYYY-MM-DD format

          return (
            <div key={entry.id} className="mb-4">
              <div className="card mb-3">
                <div className="card-header bg-primary text-white">
                  <strong>Date:</strong> {formattedTimestamp}
                </div>
                <div className="card-body">
                  <ul className="list-group">
                    {(showAll
                      ? entry.articleAidList
                      : entry.articleAidList.slice(0, 5)
                    ).map((aid, index) => (
                      <li
                        key={aid}
                        className="list-group-item list-group-item-action"
                        onClick={() => handleArticleClick(aid)}
                        style={{ cursor: "pointer" }}
                      >
                        {index + 1}. Article ID: {aid}
                      </li>
                    ))}
                  </ul>
                  {!showAll && entry.articleAidList.length > 5 && (
                    <button
                      className="btn btn-primary btn-sm mt-3"
                      onClick={() => handleShowMore(entry.id)}
                    >
                      Show More
                    </button>
                  )}
                </div>
              </div>
            </div>
          );
        })
      )}
    </div>
  );
};

export default PopularPanel;
