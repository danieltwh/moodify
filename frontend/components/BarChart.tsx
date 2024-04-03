import { useEffect, useState } from "react";
import { Progress } from "./ui/progress";
import { TimestampedSentiments } from "@/app/types";

const Bar: React.FC<{ label: string; value: number }> = ({ label, value }) => {
  return (
    <div className="flex gap-2">
      <text className="text-end text-sm w-24 h-full">{label}</text>
      <Progress className="h-full" value={value} />
    </div>
  );
};

const BarChart: React.FC<{
  label: string;
  timestampedSentiments: TimestampedSentiments;
  videoTime: number;
}> = ({ label, timestampedSentiments, videoTime }) => {
  const [outcome, setOutcome] = useState<string>("");
  const [happy, setHappy] = useState<number>(0);
  const [neutral, setNeutral] = useState<number>(0);
  const [surprised, setSurprised] = useState<number>(0);
  const [sad, setSad] = useState<number>(0);
  const [fearful, setFearful] = useState<number>(0);
  const [angry, setAngry] = useState<number>(0);

  useEffect(() => {
    setOutcome(timestampedSentiments.preds_str?.[videoTime]);
    setHappy(timestampedSentiments.interps[videoTime]?.happy);
    setNeutral(timestampedSentiments.interps[videoTime]?.neutral);
    setSurprised(timestampedSentiments.interps[videoTime]?.surprised);
    setSad(timestampedSentiments.interps[videoTime]?.sad);
    setFearful(timestampedSentiments.interps[videoTime]?.fearful);
    setAngry(timestampedSentiments.interps[videoTime]?.angry);
  }, [
    videoTime,
    timestampedSentiments.preds_str,
    timestampedSentiments.interps,
  ]);
  return (
    <div className="flex flex-col w-full gap-2">
      <div className="flex h-8">
        <text className="text-lg text-center w-1/3 bg-lightPurple">
          {label}
        </text>
        <text className="text-lg text-center w-2/3 bg-white ">{outcome}</text>
      </div>

      <div className="flex flex-col gap-2 w-full">
        <Bar label="Happy" value={happy * 100} />
        <Bar label="Neutral" value={neutral * 100} />
        <Bar label="Surprised" value={surprised * 100} />
        <Bar label="Sad" value={sad * 100} />
        <Bar label="Fearful" value={fearful * 100} />
        <Bar label="Angry" value={angry * 100} />
      </div>
    </div>
  );
};

export default BarChart;
