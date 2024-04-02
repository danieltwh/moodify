import { Progress } from "./ui/progress";

const Bar: React.FC<{ label: string; value: number }> = ({ label, value }) => {
  return (
    <div className="flex gap-2">
      <text className="text-end text-sm w-24 h-full">{label}</text>
      <Progress className="h-full" value={value} />
    </div>
  );
};

const BarChart: React.FC<{ label: string; outcome: string }> = ({
  label,
  outcome,
}) => {
  return (
    <div className="flex flex-col w-full gap-2">
      <div className="flex h-8">
        <text className="text-lg text-center w-1/3 bg-lightPurple">
          {label}
        </text>
        <text className="text-lg text-center w-2/3 bg-white ">{outcome}</text>
      </div>

      <div className="flex flex-col gap-2 w-full">
        <Bar label="Happy" value={75} />
        <Bar label="Neutral" value={66} />
        <Bar label="Surprised" value={42} />
        <Bar label="Sad" value={15} />
        <Bar label="Fearful" value={8} />
        <Bar label="Angry" value={2} />
      </div>
    </div>
  );
};

export default BarChart;
