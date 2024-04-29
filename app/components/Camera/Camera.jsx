"use client";
import React, { useState, useRef, useCallback, useEffect } from "react";
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
  const [capturing, setCapturing] = useState(false);
  const [intervalId, setIntervalId] = useState(null);

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc) {
      fetch("/api", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: imageSrc }),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          if (data.image_with_tracking) {
            setProcessedImgSrc(
              "data:image/jpeg;base64," + data.image_with_tracking
            );
          }
        })
        .catch((error) => console.error("Error:", error));
    }
  }, []);

  const toggleCapture = () => {
    if (!capturing) {
      const id = setInterval(capture, 100); // Adjust time as needed
      setIntervalId(id);
      setCapturing(true);
    } else {
      clearInterval(intervalId);
      setIntervalId(null);
      setCapturing(false);
    }
  };

  const toggleCamera = () => {
    setIsActive(!isActive);
  };

  useEffect(() => {
    return () => clearInterval(intervalId);
  }, [intervalId]);

  const buttonStyle = {
    backgroundColor: capturing ? "#ff6347" : "#32cd32", // Tomato for stop, lime green for start
    color: "white",
    padding: "8px 16px",
    borderRadius: "4px",
    cursor: "pointer",
    margin: "0 8px",
  };

  return (
    <div>
      <h1 className="mb-3 text-xl">Gesture Detection</h1>

      <div
        className="rounded-lg shadow-lg flex flex-col items-center justify-center bg-gray-100"
        style={{ width: "640px", height: "360px", margin: "auto" }}
      >
        {isActive ? (
          <Webcam
            mirrored={true}
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
        <button style={buttonStyle} onClick={toggleCapture}>
          {capturing ? "Stop Capture" : "Start Capture"}
        </button>
        <button
          style={{
            backgroundColor: "#6495ed",
            color: "white",
            padding: "8px 16px",
            borderRadius: "4px",
            cursor: "pointer",
          }}
          onClick={toggleCamera}
        >
          {isActive ? "Turn Camera Off" : "Turn Camera On"}
        </button>
      </div>
      {processedImgSrc && (
        <img
          src={processedImgSrc}
          alt="Processed"
          style={{ width: "640px", height: "360px", margin: "auto" }}
          className="mt-4 rounded-lg"
        />
      )}
    </div>
  );
};
