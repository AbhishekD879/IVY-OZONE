export interface IEuroDisplayMessages {
  CONGRATULATIONS_MSG: ICongrats;
  FREEBET: IFreebets;
}

export interface ICongrats {
  CONGRATS: string;
  EARNED: string;
  STAMP: string;
  FREEBET: string;
  NEXT_DAY: string;
  MORE_STAMPS: string;
}

export interface IFreebets {
  REWARD: string;
  QUALIFYING_SINGLE_BET: string;
  QUALIFYING_MULTIPLE_BET: string;
}

export interface IEuroMessages {
  TITLE: string;
  HOW_IT_WORKS: string;
  FULL_TERMS_AND_COND: string;
  TERMS_AND_COND: string;
  ERROR_MESSAGE: string;
  ERROR_USER_MESSAGE: string;
  HOW_IT_WORKS_DIALOG: string;
  EURO_BADGE: string;
  FREE_BET: string;
  MOBILE_BADGES_EACH_ROW: number;
  DESKTOP_BADGES_EACH_ROW: number;
  ERROR_HOWITWORKS: string;
  PROMOTIONS: string;
  DEFAULT_TOKEN: string;
  TOTAL_BADGES: number;
}

export interface IBadgePath {
  BALL_0: string;
  BALL_1: string;
  BALL_2: string;
  BALL_EMPTY: string;
}

export interface IBadgeRewards {
  badgeType: string;
  yellowHighlight: boolean;
  message: string[];
  freeBetToken: string;
}
