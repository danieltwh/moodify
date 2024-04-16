"use client";

import BarChart from "@/components/BarChart";
import SentimentScoreToggle from "@/components/SentimentScoreToggle";
import { useEffect, useRef, useState } from "react";
import mockInference from "@/_mock/sample_pred.json";
import { SentimentScores } from "@/app/types";

const Analysis: React.FC<{ params: { slug: string } }> = ({ params }) => {
  const videoId = params.slug;
  const [transcript, setTranscript] = useState<string>("");

  const [speechSentiment, setSpeechSentiment] = useState<SentimentScores>({
    preds_str: [],
    interps: [],
  });
  const [facialSentiment, setFacialSentiment] = useState<SentimentScores>({
    preds_str: [],
    interps: [],
  });

  const [aggregatedSpeechSentiment, setAggregatedSpeechSentiment] =
    useState<SentimentScores>({ preds_str: [], interps: [] });
  const [aggregatedFacialSentiment, setAggregatedFacialSentiment] =
    useState<SentimentScores>({ preds_str: [], interps: [] });

  const [videoTime, setVideoTime] = useState<number>(0);
  const [viewAggregatedScores, setViewAggregatedScores] =
    useState<boolean>(true);

  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/video/${videoId}/predictions`)
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log(data);
        setTranscript(data.text);
        setSpeechSentiment(data.speech_data);
        setFacialSentiment(data.face_emotion);
        setAggregatedSpeechSentiment(data.aggregates.speech_data);
        setAggregatedFacialSentiment(data.aggregates.face_emotion);
      });
    // setTranscript(mockInference.text);
    // setSpeechSentiment(mockInference.speech_data);
    // setFacialSentiment(mockInference.face_emotion);
    // setAggregatedSpeechSentiment(mockInference.aggregates.speech_data);
    // setAggregatedFacialSentiment(mockInference.aggregates.face_emotion);
  }, []);

  return (
    <div className="space-y-3">
      <text className="text-2xl font-semibold">Video X</text>
      <div className="flex justify-around gap-8">
        <video
          controls
          ref={videoRef}
          src={`http://127.0.0.1:5000/stream/${videoId}`}
          className="aspect-video bg-black w-full h-72"
          onTimeUpdate={() => {
            if (videoRef.current) {
              setVideoTime(Math.floor(videoRef.current.currentTime));
            }
          }}
        ></video>
      </div>
      <SentimentScoreToggle
        viewAggregatedScores={viewAggregatedScores}
        setViewAggregatedScores={setViewAggregatedScores}
      />
      <div className="flex justify-around gap-8">
        <BarChart
          label="Speech"
          timestampedSentiments={
            viewAggregatedScores ? aggregatedSpeechSentiment : speechSentiment
          }
          videoTime={viewAggregatedScores ? 0 : videoTime}
        />
        <BarChart
          label="Expression"
          timestampedSentiments={
            viewAggregatedScores ? aggregatedFacialSentiment : facialSentiment
          }
          videoTime={viewAggregatedScores ? 0 : videoTime}
        />
      </div>
      <p className="w-full text-darkPurple">{transcript}</p>
    </div>
  );
};

export default Analysis;
