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
