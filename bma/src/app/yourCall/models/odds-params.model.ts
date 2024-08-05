export interface IOddsParams {
  obEventId?: number;
  selectionIds?: number[];
  outcomeIds?: number[];
  selectionType?: string;
  playerSelections?: IPlayerSelections[];
}

interface IPlayerSelections {
  statId: number;
  playerId: number;
  line: string | number;
}
