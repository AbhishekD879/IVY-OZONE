export interface IQuickbetRequestModel {
  additional?: {
    scorecastMarketId: number;
  };
  outcomeIds?: number[];
  selectionType?: string;
  gtmTracking?: any;
  token?: string;
  templateMarketName?: string;
  isStreamBet?: boolean;
  oddsBoost?:boolean;
  fanzoneTeamId?: string;
}
