interface Interp {
  happy: number;
  neutral: number;
  surprised: number;
  sad: number;
  fearful: number;
  angry: number;
}

export interface TimestampedSentiments {
  preds_str: string[];
  interps: Interp[];
}

export interface PastUpload {
  title: string;
  uploadDate: string;
  status: string;
  speechSentiment: string;
  expressionSentiment: string;
}
