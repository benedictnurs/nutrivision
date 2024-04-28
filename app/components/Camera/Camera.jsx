"use client";
import React from "react";
import Webcam from "react-webcam";

const videoConstraints = {
  width: 1280,  // This will be overridden by CSS to maintain aspect ratio
  height: 720,  // This will be overridden by CSS to maintain aspect ratio
  facingMode: "user",
};

export const Camera = () => {
  const webcamRef = React.useRef(null);
  const [imgSrc, setImgSrc] = React.useState(null);
  const [isActive, setIsActive] = React.useState(true);

  const capture = React.useCallback(() => {
    const imageSrc = webcamRef.current?.getScreenshot();
    setImgSrc(imageSrc);
  }, [webcamRef, setImgSrc]);

  const toggleCamera = () => {
    setIsActive(!isActive);
  };

  return (
    <div className="flex flex-col items-center justify-center w-full">
      
      <div className="w-[50%] h-auto flex flex-col items-center justify-center relative bg-gray-100 rounded-lg shadow-lg">
        {isActive && (
          <Webcam
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            videoConstraints={videoConstraints}
            className="w-full h-full rounded-lg"
          />
        )}
      </div>
              <div className="flex justify-center space-x-4 absolute bottom-4 left-1/2 transform -translate-x-1/2">
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
          className="mt-4 rounded-lg w-[50%] h-auto"
        />
      )}
    </div>
  );
};
