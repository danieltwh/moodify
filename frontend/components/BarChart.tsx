import { useEffect, useState } from "react";
import { Progress } from "./ui/progress";
import { SentimentScores } from "@/app/types";

const Bar: React.FC<{ label: string; value: number }> = ({ label, value }) => {
  return (
    <div className="flex gap-2">
      <text className="text-end text-sm w-24 h-full">{label}</text>
      <Progress className="h-full" value={value} />
      <text className="text-end text-sm w-12 h-full">
        {value ? (value / 100).toFixed(2) : "0.00"}
      </text>
    </div>
  );
};

const BarChart: React.FC<{
  label: string;
  timestampedSentiments: SentimentScores;
  videoTime: number;
}> = ({ label, timestampedSentiments, videoTime }) => {
  const [outcome, setOutcome] = useState<string>("");
  const [positive, setPositive] = useState<string>("0.00");
  const [neutral, setNeutral] = useState<string>("0.00");
  const [negative, setNegative] = useState<string>("0.00");

  useEffect(() => {
    setOutcome(timestampedSentiments.preds_str?.[videoTime]);
    setPositive(timestampedSentiments.interps[videoTime]?.positive.toFixed(2));
    setNeutral(timestampedSentiments.interps[videoTime]?.neutral.toFixed(2));
    setNegative(timestampedSentiments.interps[videoTime]?.negative.toFixed(2));
  }, [
    videoTime,
    timestampedSentiments.preds_str,
    timestampedSentiments.interps,
  ]);
  return (
    <div className="flex flex-col w-full gap-2">
      <div className="flex h-8">
        <text className="text-lg w-1/3 bg-lightPurple">{label}</text>
        {outcome == "neutral" && (
          <text className="text-lg w-2/3 bg-white">{outcome}</text>
        )}
        {outcome == "positive" && (
          <text className="text-lg w-2/3 bg-[#BDE7BD] ">{outcome}</text>
        )}
        {outcome == "negative" && (
          <text className="text-lg w-2/3 bg-[#FFB6B3]">{outcome}</text>
        )}
      </div>

      <div className="flex flex-col gap-2 w-full">
        <Bar label="Positive" value={parseFloat(positive) * 100} />
        <Bar label="Neutral" value={parseFloat(neutral) * 100} />
        <Bar label="Negative" value={parseFloat(negative) * 100} />
      </div>
    </div>
  );
};

export default BarChart;
