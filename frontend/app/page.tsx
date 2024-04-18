"use client";

import UploadsTable from "@/components/UploadsTable";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/use-toast";
import { useRef, useState } from "react";

const Home: React.FC = () => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();
  const [seed, setSeed] = useState<number>(1);
  return (
    <div className="space-y-6 w-full pb-6">
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
        onChange={(e) => {
          const videoFile = e.target.files?.[0];
          const formData = new FormData();
          if (videoFile) {
            formData.append("file", videoFile);
            fetch("http://127.0.0.1:5000/upload", {
              method: "POST",
              body: formData,
            }).then(() => {
              toast({
                title: "Upload success!",
              });
              setSeed(Math.random());
            });
          }
        }}
      ></input>
      <div className="pt-10">
        <UploadsTable key={seed} />
      </div>
    </div>
  );
};

export default Home;
