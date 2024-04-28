"use client";
import React from "react";
import Webcam from "react-webcam";

const videoConstraints = {
  width: 1280,  // Setting this to a high resolution for better quality
  height: 720,  // Standard HD resolution to maintain good image quality
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



  return (
    <div className="flex flex-col items-center justify-center w-full min-h-screen">
      <div className="w-full max-w-xl p-4 bg-gray-100 rounded-lg shadow-lg flex flex-col items-center justify-center relative">
        {isActive ? (
          <Webcam
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            videoConstraints={videoConstraints}
            className="w-full h-full rounded-lg"
          />
        ) : (
          <div className="w-full h-full bg-gray-300 rounded-lg flex items-center justify-center text-lg text-gray-500">
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
      {imgSrc && (
        <img
          src={imgSrc}
          alt="Captured"
          className="mt-4 rounded-lg"
        />
      )}
    </div>
  );
};
