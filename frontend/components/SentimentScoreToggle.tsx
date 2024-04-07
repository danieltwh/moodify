"use client";

import { Dispatch, SetStateAction } from "react";

const SELECTED_CLASSNAME = "text-purple underline underline-offset-4";
const UNSELECTED_CLASSNAME = "text-darkPurple hover:cursor-pointer";

const SentimentScoreToggle: React.FC<{
  viewAggregatedScores: boolean;
  setViewAggregatedScores: Dispatch<SetStateAction<boolean>>;
}> = ({ viewAggregatedScores, setViewAggregatedScores }) => {
  return (
    <div>
      <text className="text-darkPurple">View sentiment for: </text>
      <text
        className={
          viewAggregatedScores ? SELECTED_CLASSNAME : UNSELECTED_CLASSNAME
        }
        onClick={() => setViewAggregatedScores(true)}
      >
        the entire video
      </text>
      <text className="text-darkPurple"> / </text>
      <text
        className={
          viewAggregatedScores ? UNSELECTED_CLASSNAME : SELECTED_CLASSNAME
        }
        onClick={() => setViewAggregatedScores(false)}
      >
        by timestamp
      </text>
    </div>
  );
};

export default SentimentScoreToggle;
