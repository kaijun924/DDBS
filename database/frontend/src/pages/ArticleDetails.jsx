import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import { Container, Row, Col, Card, Button, Spinner } from "react-bootstrap";
import "./ArticleDetails.css";

function ArticleDetails() {
  const { aid } = useParams();
  const [articleData, setArticleData] = useState(null);
  const [interactionData, setInteractionData] = useState(null);
  const [articleText, setArticleText] = useState(null);
  const [articleImages, setArticleImages] = useState([]);
  const [articleVideo, setArticleVideo] = useState(null);
  const [loading, setLoading] = useState({ details: true, interactions: true, content: true });

  useEffect(() => {
    // Fetch article details
    axios
      .get(`http://localhost:8000/articles/${aid}`)
      .then((response) => {
        setArticleData(response.data);
        setLoading((prev) => ({ ...prev, details: false }));

        // Fetch text, images, and video based on article details
        // const { text, image, video } = response.data;
        // const imageList = image.split(",").filter((img) => img); // Handle multiple images
        // setArticleImages(imageList);

        // axios.get(`http://localhost:8000/hadoop/article_txt/${text}`).then((res) => {
        //   setArticleText(res.data.text);
        // });

        // if (video) setArticleVideo(`http://localhost:8000/hadoop/article_vid/${video}`);
        // setLoading((prev) => ({ ...prev, content: false }));
      })
      .catch((err) => console.error("Error fetching article details:", err));

    // Fetch interaction data
    axios
      .get(`http://localhost:8000/bereads/${aid}`)
      .then((response) => {
        setInteractionData(response.data);
        setLoading((prev) => ({ ...prev, interactions: false }));
      })
      .catch((err) => console.error("Error fetching interaction data:", err));
  }, [aid]);

  return (
  <Container className="article-detail-container my-4">
      <h1 className="text-center">Article Details</h1>

      {/* Article Details */}
      {loading.details ? (
        <div className="text-center">
          <Spinner animation="border" variant="primary" />
        </div>
      ) : (
        articleData && (
          <>
            <Card className="mb-3">
              <Card.Body>
                <Card.Title>{articleData.title}</Card.Title>
                <Card.Text>
                  <strong>Category:</strong> {articleData.category}
                </Card.Text>
                <Card.Text>
                  <strong>Abstract:</strong> {articleData.abstract}
                </Card.Text>
                <Card.Text>
                  <strong>Tags:</strong> {articleData.articleTags}
                </Card.Text>
                <Card.Text>
                  <strong>Authors:</strong> {articleData.authors}
                </Card.Text>
                <Card.Text>
                  <strong>Language:</strong> {articleData.language}
                </Card.Text>
              </Card.Body>
            </Card>
          </>
        )
      )}

      {/* Content Section */}
      {loading.content ? (
        <div className="text-center">
          <Spinner animation="border" variant="primary" />
        </div>
      ) : (
        <>
          <Row className="mb-4">
            <Col md={12}>
              <div className="article-text">
                <h3>Text</h3>
                <p>{articleText}</p>
              </div>
            </Col>
          </Row>

          <Row className="mb-4">
            <Col md={12}>
              <div className="article-images">
                <h3>Images</h3>
                {articleImages.map((img, index) => (
                  <img
                    key={index}
                    src={`http://localhost:8000/hadoop/article_img/${img}`}
                    alt={`article img ${index}`}
                    className="img-fluid mb-3"
                  />
                ))}
              </div>
            </Col>
          </Row>

          {articleVideo && (
            <Row className="mb-4">
              <Col md={12}>
                <div className="article-video">
                  <h3>Video</h3>
                  <video width="100%" controls>
                    <source src={articleVideo} type="video/mp4" />
                    Your browser does not support the video tag.
                  </video>
                </div>
              </Col>
            </Row>
          )}
        </>
      )}

      {/* Interaction Data */}
      {loading.interactions ? (
        <div className="text-center">
          <Spinner animation="border" variant="primary" />
        </div>
      ) : (
        interactionData && (
          <div className="article-interactions">
            <h3 className="text-center mb-4">Be Read Statistics</h3>
            <Row className="mb-4 text-center">
              <Col md={3}>
                <div className="count-box">
                  <strong className="count-title">Read Count:</strong>
                  <div className="count-value">{interactionData.readNum}</div>
                  <div>
                    <p>User IDs:</p>
                    <span>
                      {interactionData.readUidList.join(" | ")}
                    </span>
                  </div>
                </div>
              </Col>
              <Col md={3}>
                <div className="count-box">
                  <strong className="count-title">Comment Count:</strong>
                  <div className="count-value">{interactionData.commentNum}</div>
                  <div>
                    <p>User IDs:</p>
                    <span>
                      {interactionData.commentUidList.join(" | ")}
                    </span>
                  </div>
                </div>
              </Col>
              <Col md={3}>
                <div className="count-box">
                  <strong className="count-title">Agree Count:</strong>
                  <div className="count-value">{interactionData.agreeNum}</div>
                  <div>
                    <p>User IDs:</p>
                    <span>
                      {interactionData.agreeUidList.join(" | ")}
                    </span>
                  </div>
                </div>
              </Col>
              <Col md={3}>
                <div className="count-box">
                  <strong className="count-title">Share Count:</strong>
                  <div className="count-value">{interactionData.shareNum}</div>
                  <div>
                    <p>User IDs:</p>
                    <span>
                      {interactionData.shareUidList.join(" | ")}
                    </span>
                  </div>
                </div>
              </Col>
            </Row>
          </div>
        )
      )}
    </Container>
  );
}

export default ArticleDetails;
