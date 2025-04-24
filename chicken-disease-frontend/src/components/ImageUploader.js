import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";

function ImageUploader() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  // Map numerical predictions to disease names with descriptions
  const DISEASE_CLASSES = [
    {
      name: "Healthy",
      description: "No signs of disease detected.",
      icon: "bi-check-circle-fill"
    },
    {
      name: "Salmonella",
      description: "Bacterial infection causing digestive issues.",
      icon: "bi-bug-fill"
    },
    {
      name: "Coccidiosis",
      description: "Parasitic disease affecting the intestines.",
      icon: "bi-bug-fill"
    },
    {
      name: "New Castle Disease",
      description: "Highly contagious viral disease affecting respiratory and nervous systems.",
      icon: "bi-virus"
    }
  ];

  const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000/predict";

  const handleImageChange = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Validate file type
    const allowedTypes = ["image/jpeg", "image/png"];
    if (!allowedTypes.includes(file.type)) {
      setError("Please select a valid image file (.jpg, .jpeg, .png).");
      return;
    }

    // Validate file size (5MB limit)
    if (file.size > 5 * 1024 * 1024) {
      setError("File size exceeds 5MB limit.");
      return;
    }

    setSelectedImage(file);
    setPreviewUrl(URL.createObjectURL(file));
    setPrediction(null);
    setError(null);
  };

  const handleUpload = async () => {
    if (!selectedImage) {
      setError("Please select an image first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedImage);

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `Server error: ${response.status}`);
      }

      const data = await response.json();

      if (data.prediction && data.prediction.probabilities) {
        const probabilities = data.prediction.probabilities;
        const predictionResult = DISEASE_CLASSES.map((disease, index) => ({
          ...disease,
          probability: probabilities[index],
          percentage: (probabilities[index] * 100).toFixed(2)
        })).sort((a, b) => b.probability - a.probability);

        setPrediction(predictionResult);
      } else {
        throw new Error("Unexpected prediction format.");
      }
    } catch (error) {
      console.error("Error uploading image:", error);
      setError(`Error: ${error.message || "Unable to connect to the server."}`);
      setPrediction(null);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setPreviewUrl(null);
    setPrediction(null);
    setError(null);
    document.getElementById("image-upload").value = null;
  };

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-lg-8">
          <div className="card shadow">
            <div className="card-header bg-primary text-white">
              <h1 className="h4 mb-0 text-center">Chicken Health Analyzer</h1>
            </div>
            <div className="card-body">
              <div className="text-center mb-4">
                <p className="lead">
                  Upload an image of your chicken to detect potential diseases.
                </p>
              </div>

              <div className="mb-4">
                <div className="d-flex flex-column flex-md-row gap-3 justify-content-center align-items-center">
                  <div className="custom-file-upload">
                    <input
                      type="file"
                      onChange={handleImageChange}
                      accept="image/jpeg,image/png"
                      id="image-upload"
                      className="d-none"
                    />
                    <label
                      htmlFor="image-upload"
                      className="btn btn-outline-primary btn-lg"
                    >
                      <i className="bi bi-cloud-arrow-up me-2"></i>
                      {selectedImage ? "Change Image" : "Select Image"}
                    </label>
                  </div>
                  <button
                    onClick={handleUpload}
                    disabled={!selectedImage || loading}
                    className="btn btn-success btn-lg"
                  >
                    {loading ? (
                      <>
                        <span
                          className="spinner-border spinner-border-sm me-2"
                          role="status"
                          aria-hidden="true"
                        ></span>
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <i className="bi bi-search me-2"></i>
                        Analyze Image
                      </>
                    )}
                  </button>
                  {selectedImage && (
                    <button
                      onClick={handleReset}
                      className="btn btn-secondary btn-lg"
                    >
                      <i className="bi bi-arrow-repeat me-2"></i>
                      Reset
                    </button>
                  )}
                </div>
              </div>

              {error && (
                <div className="alert alert-danger mt-3">
                  <i className="bi bi-exclamation-triangle-fill me-2"></i>
                  {error}
                </div>
              )}

              {previewUrl && (
                <div className="text-center mt-4">
                  <div className="mb-3">
                    <h3 className="h5">Image Preview</h3>
                  </div>
                  <img
                    src={previewUrl}
                    alt="Preview"
                    className="img-fluid rounded shadow"
                    style={{ maxHeight: "300px" }}
                  />
                </div>
              )}

              {prediction && (
                <div className="mt-5">
                  <div className="text-center mb-4">
                    <h2 className="h4">Analysis Results</h2>
                    <p className="text-muted">
                      Based on our AI analysis of your chicken's image.
                    </p>
                  </div>

                  <div className="alert alert-success">
                    <div className="d-flex align-items-center">
                      <div className="flex-shrink-0">
                        <i className={`bi ${prediction[0].icon} fs-4`}></i>
                      </div>
                      <div className="flex-grow-1 ms-3">
                        <h5 className="alert-heading mb-1">
                          Most Likely: {prediction[0].name}
                        </h5>
                        <p className="mb-0 small">
                          Confidence: {prediction[0].percentage}% - {prediction[0].description}
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="mt-4">
                    <h5 className="mb-3">Detailed Probabilities:</h5>
                    <div className="list-group">
                      {prediction.map((item, index) => (
                        <div
                          key={index}
                          className={`list-group-item ${index === 0 ? "active" : ""}`}
                          aria-current={index === 0}
                        >
                          <div className="d-flex w-100 justify-content-between">
                            <h6 className="mb-1">
                              <i className={`bi ${item.icon} me-2`}></i>
                              {item.name}
                            </h6>
                            <small>{item.percentage}%</small>
                          </div>
                          <p className="mb-1 small">{item.description}</p>
                          <div className="progress mt-2" style={{ height: "8px" }}>
                            <div
                              className={`progress-bar ${index === 0 ? "bg-success" : "bg-info"}`}
                              role="progressbar"
                              style={{ width: `${item.percentage}%` }}
                              aria-valuenow={item.percentage}
                              aria-valuemin="0"
                              aria-valuemax="100"
                            ></div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
            <div className="card-footer text-muted text-center small">
              <p className="mb-0">
                Note: Consult a veterinarian for professional diagnosis.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ImageUploader;