export interface IPrize {
  cash?: string;
  totalPrizes?: string;
  prizeMap?: {
    [key: string]: IPriceRecord[];
  };
}

export interface IPriceRecord {
  id?: string;
  createdBy?: string;
  createdByUserName?: string;
  updatedBy?: string;
  updatedByUserName?: string;
  createdAt?: string;
  updatedAt?: string;
  contestId?: string;
  type?: string;
  value?: string;
  text?: string;
  icon?: IPrizeImg;
  signPosting?: IPrizeImg;
  percentageOfField?: string;
  numberOfEntries?: string;
  brand?: string;
  [key: string]: any;
}

export interface IPrizeImg {
  filename?: string;
  originalname?: string;
  path?: string;
  size?: string;
  filetype?: string;
  [key: string]: any;
}


export interface IPrizeTypeDesc {
  cash?: string;
  freebet?: string;
  ticket?: string;
  voucher?: string;
}
