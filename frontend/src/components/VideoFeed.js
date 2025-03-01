import React from "react";

const VideoFeed = () => {
  return (
    <div style={{ textAlign: "center", marginTop: "20px" }}>
      <h2>Live Person Detection</h2>
      <img
        src="http://localhost:8000/video-feed/"
        alt="Live Feed"
        style={{ width: "640px", height: "480px", border: "2px solid black" }}
      />
    </div>
  );
};

export default VideoFeed;
