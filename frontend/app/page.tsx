"use client";

import BarChart from "@/components/BarChart";
import SentimentScoreToggle from "@/components/SentimentScoreToggle";
import { useEffect, useRef, useState } from "react";
import mockInference from "@/_mock/sample_pred.json";
import { TimestampedSentiments } from "./types";

const Home: React.FC = () => {
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
    <main className="flex min-h-screen flex-col space-y-6 items-center p-10 py-4">
      <text className="text-5xl font-medium">Moodify</text>
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
    </main>
  );
};

export default Home;
