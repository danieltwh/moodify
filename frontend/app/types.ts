interface Interp {
  positive: number;
  neutral: number;
  negative: number;
}

export interface SentimentScores {
  preds_str: string[];
  interps: Interp[];
}

export interface PastUpload {
  title: string;
  uploadDate: string;
  status: string;
  speechSentiment: string;
  expressionSentiment: string;
  id: string;
}
