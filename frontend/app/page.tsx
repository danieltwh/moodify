"use client";

import UploadsTable from "@/components/UploadsTable";
import { Button } from "@/components/ui/button";
import { useRef } from "react";

const Home: React.FC = () => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  return (
    <div className="space-y-6 w-full">
      <text className="text-5xl font-medium">Moodify</text>
      <p className="text-darkPurple text-xl">
        Find out how your investors feel. Uncover hidden insights
        <br></br>
        from their voices and expressions.
      </p>
      <Button onClick={() => fileInputRef.current?.click()}>
        Upload Video
      </Button>
      <input
        ref={fileInputRef}
        type="file"
        className="hidden"
        onChange={(e) => console.log(e.target.files?.[0])}
      ></input>
      <div className="pt-10">
        <UploadsTable />
      </div>
    </div>
  );
};

export default Home;
