import React, { useState } from "react";
import axios from "axios";

export default function UploadForm() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const onSelect = (e) => {
    const img = e.target.files[0];
    setFile(img);
    setResult(null);
    setError(null);
    if (img) setPreview(URL.createObjectURL(img));
  };

  const predict = async () => {
    if (!file) return setError("⚠ Please upload an image first.");
    setLoading(true);

    const form = new FormData();
    form.append("image", file);

    try {
      const res = await axios.post("/predict", form);
      setResult(res.data);
      setError(null);
    } catch (err) {
      setError("Request failed (Server Error 500) — Check backend console");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white w-full lg:w-3/5 p-10 rounded-xl shadow-md text-center">
      <div className="flex justify-center mb-4">
        <div className="w-16 h-16 bg-green-600 text-white rounded-full flex items-center justify-center text-3xl">
          🌿
        </div>
      </div>

      <h2 className="text-2xl font-semibold mb-2">Upload Plant Leaf Image</h2>
      <p className="text-gray-600 mb-4">Drag and drop your plant image here, or click to browse</p>

      <label className="inline-block cursor-pointer bg-green-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-700 transition">
        Choose Image
        <input type="file" className="hidden" onChange={onSelect} />
      </label>

      <p className="text-gray-500 text-sm mt-4">Supported formats: JPG, PNG • Max size: 10MB</p>

      {preview && (
        <div className="mt-6 flex justify-center">
          <img src={preview} alt="preview" className="w-80 rounded-lg shadow-md" />
        </div>
      )}

      <button
        onClick={predict}
        disabled={loading}
        className="mt-6 bg-green-700 hover:bg-green-800 text-white px-6 py-3 rounded-lg"
      >
        {loading ? "Predicting..." : "Predict"}
      </button>

      {error && <p className="text-red-600 mt-3">{error}</p>}

      {result && (
        <div className="mt-6 bg-gray-50 p-4 rounded-lg shadow">
          <h3 className="text-xl font-semibold text-green-700">✅ Prediction Result</h3>
          <p className="text-gray-800 mt-1 text-lg">{result.prediction}</p>
          <p className="text-gray-600 text-sm mt-1">Confidence: {(result.confidence * 100).toFixed(2)}%</p>
        </div>
      )}
    </div>
  );
}
