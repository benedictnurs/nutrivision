"use client"
import React, { useState, useRef, useCallback } from "react";
import Webcam from "react-webcam";

const videoConstraints = {
  width: 1280,
  height: 720,
  facingMode: "user",
};

export const Camera = () => {
  const webcamRef = useRef(null);
  const [processedImgSrc, setProcessedImgSrc] = useState(null);
  const [isActive, setIsActive] = useState(true);

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc) {
      fetch("/api", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: imageSrc }),
      })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        if (data.image_with_line) {
          // Set the processed image with the line drawn on it
          setProcessedImgSrc('data:image/jpeg;base64,' + data.image_with_line);
        }
      })
      .catch(error => console.error("Error:", error));
    }
  }, []);

  const toggleCamera = () => setIsActive(prevIsActive => !prevIsActive);

  const consistentStyle = {
    width: "640px",
    height: "360px",
    margin: "auto",
  };

  return (
    <div>
      <div
        className="rounded-lg shadow-lg flex flex-col items-center justify-center bg-gray-100"
        style={consistentStyle}
      >
        {isActive ? (
          <Webcam
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            videoConstraints={videoConstraints}
            className="w-full h-full rounded-lg"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-lg text-gray-500">
            Camera Off
          </div>
        )}
      </div>
      <div className="flex justify-center space-x-4 my-5">
        <button className="bg-blue-500 hover:bg-blue-700 text-white py-2 px-4 rounded" onClick={capture}>
          Capture Photo
        </button>
        <button className="bg-red-500 hover:bg-red-700 text-white py-2 px-4 rounded" onClick={toggleCamera}>
          {isActive ? "Turn Camera Off" : "Turn Camera On"}
        </button>
      </div>
      {processedImgSrc && (
        <img
          src={processedImgSrc}
          alt="Processed"
          style={consistentStyle}
          className="mt-4 rounded-lg"
        />
      )}
    </div>
  );
};
