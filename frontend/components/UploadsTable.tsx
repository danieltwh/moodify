"use client";
import { useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./ui/table";
// import mockPastUploads from "@/_mock/past_uploads.json";
import { PastUpload } from "@/app/types";
import { useRouter } from "next/navigation";

const UploadsTable: React.FC = () => {
  const router = useRouter();
  const [pastUploads, setPastUploads] = useState<PastUpload[]>();

  useEffect(() => {
    fetch("http://127.0.0.1:5000/video-metadata")
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        setPastUploads(data);
      });
    // setPastUploads(mockPastUploads);
  }, []);

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead></TableHead>
          <TableHead>Upload Date</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Speech Sentiment</TableHead>
          <TableHead>Expression Sentiment</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {pastUploads?.map((pastUpload, idx) => {
          return (
            <TableRow key={idx}>
              <TableCell
                className={
                  pastUpload.status == "completed"
                    ? "bg-lightPurple hover:cursor-pointer"
                    : "bg-lightPurple"
                }
                onClick={() => {
                  if (pastUpload.status != "completed") {
                    return;
                  }
                  router.push(`/dashboard/${pastUpload.id}`);
                }}
              >
                {pastUpload.title}
              </TableCell>
              <TableCell>{pastUpload.uploadDate}</TableCell>
              <TableCell>{pastUpload.status}</TableCell>
              <TableCell>{pastUpload.speechSentiment}</TableCell>
              <TableCell>{pastUpload.expressionSentiment}</TableCell>
            </TableRow>
          );
        })}
      </TableBody>
    </Table>
  );
};

export default UploadsTable;
