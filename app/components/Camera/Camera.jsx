"use client";
import React from "react";
import Webcam from "react-webcam";

const videoConstraints = {
  width: 1280, // High resolution for better quality
  height: 720, // Standard HD resolution for good image quality
  facingMode: "user",
};

export const Camera = () => {
  const webcamRef = React.useRef(null);
  const [imgSrc, setImgSrc] = React.useState(null);
  const [isActive, setIsActive] = React.useState(true);

  const capture = React.useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      setImgSrc(imageSrc);
    }
  }, [webcamRef]);

  const toggleCamera = () => {
    setIsActive(!isActive);
  };

  // Defined style for maintaining consistency
  const consistentStyle = {
    width: "640px", // Set a fixed width
    height: "360px", // Height to maintain a 16:9 aspect ratio based on the width
    margin: "auto", // Center the container
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <div
        className="rounded-lg shadow-lg flex flex-col items-center justify-center relative bg-gray-100"
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
      <div className="flex justify-center space-x-4 mt-4">
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          onClick={capture}
        >
          Capture Photo
        </button>
        <button
          className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
          onClick={toggleCamera}
        >
          {isActive ? "Turn Camera Off" : "Turn Camera On"}
        </button>
      </div>
      <div className="mt-8">
        {" "}
        {imgSrc && (
          <img
            src={imgSrc}
            alt="Captured"
            style={consistentStyle} // Ensuring the image also adheres to the fixed dimensions
            className="mt-4 rounded-lg"
          />
        )}
      </div>
    </div>
  );
};
