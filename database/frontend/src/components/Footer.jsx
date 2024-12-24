import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import "./Footer.css";

function Footer() {
  return (
    <footer className="bg-light py-4">
      <Container>
        <Row className="text-center">
          <Col>
            <p className="h5">Important Links:</p>
            <ul className="list-inline">
              <li className="list-inline-item mx-3">
                <a href="http://localhost:9870/dfshealth.html#tab-datanode" target="_blank" rel="noopener noreferrer">
                  Hadoop
                </a>
              </li>
              <li className="list-inline-item mx-3">
                <a href="http://localhost:9864" target="_blank" rel="noopener noreferrer">
                  Datanode1
                </a>
              </li>
              <li className="list-inline-item mx-3">
                <a href="http://localhost:9865" target="_blank" rel="noopener noreferrer">
                  Datanode2
                </a>
              </li>
              <li className="list-inline-item mx-3">
                <a href="http://localhost:9866" target="_blank" rel="noopener noreferrer">
                  Datanode3
                </a>
              </li>
              <li className="list-inline-item mx-3">
                <a href="http://localhost:9090" target="_blank" rel="noopener noreferrer">
                  Prometheus
                </a>
              </li>
              <li className="list-inline-item mx-3">
                <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer">
                  Backend
                </a>
              </li>
              <li className="list-inline-item mx-3">
                <a href="http://localhost:3333" target="_blank" rel="noopener noreferrer">
                  Grafana
                </a>
              </li>
            </ul>
          </Col>
        </Row>
      </Container>
    </footer>
  );
}

export default Footer;
