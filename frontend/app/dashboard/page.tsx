"use client";

import BarChart from "@/components/BarChart";
import SentimentScoreToggle from "@/components/SentimentScoreToggle";
import { useEffect, useRef, useState } from "react";
import mockInference from "@/_mock/sample_pred.json";
import { TimestampedSentiments } from "@/app/types";

const Analysis: React.FC = () => {
  const [transcript, setTranscript] = useState("");
  const [speechSentiment, setSpeechSentiment] = useState<TimestampedSentiments>(
    { preds_str: [], interps: [] }
  );
  const [facialSentiment, setFacialSentiment] = useState<TimestampedSentiments>(
    { preds_str: [], interps: [] }
  );
  const [overallSentiment, setOverallSentiment] =
    useState<TimestampedSentiments>({ preds_str: [], interps: [] });
  const [videoTime, setVideoTime] = useState<number>(0);
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    setTranscript(mockInference?.text);
    setSpeechSentiment(mockInference?.speech_data);
    setFacialSentiment(mockInference?.face_emotion);
    setOverallSentiment(mockInference?.overall);
  }, []);
  return (
    <div className="space-y-2">
      <div className="flex justify-around gap-8">
        <video
          controls
          ref={videoRef}
          src="speech.mp4"
          className="aspect-video bg-black w-7/12 h-72"
          onTimeUpdate={() => {
            if (videoRef.current) {
              setVideoTime(Math.floor(videoRef.current.currentTime));
            }
          }}
        ></video>
        <p className="w-5/12 text-darkPurple text-justify">{transcript}</p>
      </div>
      <SentimentScoreToggle />
      <div className="flex justify-around gap-8 w-full">
        <BarChart
          label="Speech"
          timestampedSentiments={speechSentiment}
          videoTime={videoTime}
        />
        <BarChart
          label="Expression"
          timestampedSentiments={facialSentiment}
          videoTime={videoTime}
        />
        <BarChart
          label="Overall"
          timestampedSentiments={overallSentiment}
          videoTime={videoTime}
        />
      </div>
    </div>
  );
};

export default Analysis;
