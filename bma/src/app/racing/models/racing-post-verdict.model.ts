export interface IRacingPostVerdict {
  starRatings: IStarRating[];
  tips: IRacingPostTip[];
  verdict: string;
  imgUrl: string;
  isFilled: boolean;
  mostTipped: IMostTipped[];
}

export interface IStarRating {
  name: string;
  rating: number;
}

export interface IRacingPostTip {
  name: string;
  value: string;
  outcome?: any;
  rpSelectionUid?: number;
  saddleNo?: string;
}

export interface IMostTipped  {
  name: string;
  value: string;
  tips: string;
}
