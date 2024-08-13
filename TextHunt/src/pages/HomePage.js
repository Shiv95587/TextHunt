import React, { useState } from "react";
import axios from "axios";
import "../temp.css";

import pdfIcon from "../pdf-icon.png";
import imageIcon from "../image-icon.png"; // Add path to document icon image
import dragDropIcon from "../drag-drop-icon.png"; // Add path to drag-drop icon image
import { useNavigate } from "react-router-dom";

export default function FileUpload() {
  const [files, setFiles] = useState([]);

  const navigate = useNavigate();
  const handleFiles = (event) => {
    const selectedFiles = Array.from(event.target.files);
    setFiles((files) => [...files, ...selectedFiles]);
    // setFiles(selectedFiles);
  };

  const getFileType = (file) => {
    if (file.name.split(".")[1] === "pdf") {
      return pdfIcon;
    } else {
      return imageIcon;
    }
  };

  const handleRemoveFile = (indexToRemove) => {
    setFiles(files.filter((_, index) => index !== indexToRemove));
  };

  const Upload = async () => {
    try {
      const formData = new FormData();
      files.forEach((file) => {
        formData.append("file", file);
      });

      const response = await axios.post(
        "http://localhost:5000/members",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      console.log(response.data);

      navigate("/search");
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div className="homepage">
      <header>
        <nav>
          <div className="container">
            <h1>TextHunt</h1>
          </div>
        </nav>
        <div className="header-content">
          <p className="tagline">Intelligent Document Search & Highlighting</p>
          {/* <p className="description">
            Effortlessly find and highlight relevant text across multiple
            document formats (.jpeg, .jpg, .png, .pdf) with precision. Enter
            your query and let TextHunt deliver the best results, making it
            easier to locate key information in your documents.
          </p> */}
        </div>
      </header>
      <div className="file-upload-container">
        <div className="upload-section">
          <div className="upload-box">
            <input
              type="file"
              id="fileInput"
              accept=".pdf,.png,.jpg,.jpeg"
              multiple
              onChange={handleFiles}
              hidden
            />
            <label htmlFor="fileInput" className="upload-label">
              <img
                src={dragDropIcon}
                alt="Drag and Drop"
                className="drag-drop-icon"
              />
              <p>Browse Files (pdf, .png, .jpeg)</p>
              {/* <button className="browse-button">Browse Files</button> */}
            </label>
          </div>
        </div>

        <div className="uploaded-files">
          {files.map((file, index) => (
            <div key={index} className="file-item">
              <img
                src={getFileType(file)}
                alt="file"
                className="file-thumbnail"
              />
              <div className="file-info">
                <span className="file-name">{file.name}</span>
                <button
                  className="remove-button"
                  onClick={() => handleRemoveFile(index)}
                >
                  Remove
                </button>
              </div>
            </div>
          ))}
        </div>

        {files.length > 0 && (
          <button className="upload-button" onClick={Upload}>
            Upload Files
          </button>
        )}
      </div>
    </div>
  );
}
