import React from "react";

function Footer() {
  return (
    <footer style={{ marginTop: "20px", padding: "10px", background: "#f8f9fa", textAlign: "center" }}>
      <p>Important Links:</p>
      <ul style={{ listStyleType: "none", padding: 0 }}>
        <li><a href="https://example.com/about" target="_blank" rel="noopener noreferrer">About</a></li>
        <li><a href="https://example.com/contact" target="_blank" rel="noopener noreferrer">Contact</a></li>
        <li><a href="https://example.com/help" target="_blank" rel="noopener noreferrer">Help</a></li>
      </ul>
    </footer>
  );
}

export default Footer;
