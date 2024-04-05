"use client";

import { Button } from "@/components/ui/button";
import { useRef } from "react";

const Home: React.FC = () => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  return (
    <div className="text-center space-y-6">
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
    </div>
  );
};

export default Home;
