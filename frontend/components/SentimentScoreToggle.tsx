"use client";

import { useState } from "react";

const SELECTED_CLASSNAME = "text-purple underline underline-offset-4";
const UNSELECTED_CLASSNAME = "text-darkPurple hover:cursor-pointer";

const SentimentScoreToggle: React.FC<{}> = () => {
  const [videoSelected, setVideoSelected] = useState(false);
  return (
    <div className="text-center">
      <text className="text-darkPurple">View sentiment for: </text>
      <text
        className={videoSelected ? SELECTED_CLASSNAME : UNSELECTED_CLASSNAME}
        onClick={() => setVideoSelected(true)}
      >
        the entire video
      </text>
      <text className="text-darkPurple"> / </text>
      <text
        className={videoSelected ? UNSELECTED_CLASSNAME : SELECTED_CLASSNAME}
        onClick={() => setVideoSelected(false)}
      >
        by timestamp
      </text>
    </div>
  );
};

export default SentimentScoreToggle;
