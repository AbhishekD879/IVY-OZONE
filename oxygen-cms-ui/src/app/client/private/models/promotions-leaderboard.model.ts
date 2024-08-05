export interface Leaderboard {
  brand?: string;
  name: string;
  topX: any;
  individualRank?: boolean;
  filePath: string;
  genericTxt: string;
  status?: boolean;
  columns: ColumnsConfig[];
}

export class ColumnsConfig {
  originalName: string;
  displayName: string;
  subtitle?: string;
  style?: string;
  applyMasking?: boolean;
}

export interface PromoLeaderboard extends Leaderboard {
  id: string;
  createdBy: string;
  createdByUserName: string;
  updatedBy: string;
  updatedByUserName: string;
  createdAt: string;
  updatedAt: string;
}

export interface PromotionsLeaderboard {
  id: string;
  name: string;
  brand: string;
  navGIds: string;
  status: boolean;
  updatedAt: string;
}

export interface Leaderboards {
  id: string;
  name: string;
}
