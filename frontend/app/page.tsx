"use client";

import BarChart from "@/components/BarChart";
import SentimentScoreToggle from "@/components/SentimentScoreToggle";

const Home: React.FC = () => {
  return (
    <main className="flex min-h-screen flex-col space-y-6 items-center p-10 py-4">
      <text className="text-5xl font-medium">Moodify</text>
      <div className="flex justify-around gap-8">
        <video
          controls
          src="speech.mp4"
          className="aspect-video bg-black w-7/12 h-72"
        ></video>
        <p className="w-5/12 text-darkPurple text-justify">
          Lorem Ipsum is simply dummy text of the printing and typesetting
          industry. Lorem Ipsum has been the industry`s standard dummy text ever
          since the 1500s, when an unknown printer took a galley of type and
          scrambled it to make a type specimen book. It has survived not only
          five centuries, but also the leap into electronic typesetting,
          remaining essentially unchanged. It was popularised in the 1960s with
          the release of Letraset sheets containing Lorem Ipsum passages, and
          more recently with desktop publishing software like Aldus PageMaker
          including versions of Lorem Ipsum.
        </p>
      </div>
      <SentimentScoreToggle />
      <div className="flex justify-around gap-8 w-full">
        <BarChart label="Speech" outcome="Happy" />
        <BarChart label="Expression" outcome="Surprised" />
        <BarChart label="Overall" outcome="Happy" />
      </div>
    </main>
  );
};

export default Home;
