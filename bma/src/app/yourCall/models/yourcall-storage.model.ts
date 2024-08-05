export interface IYourcallStorage {
  [key: number]: IYourcallStorageBet;
  v: number;
}

export interface IYourcallStorageBet {
  lastModified?: number;
  markets: IYourcallStorageMarkets;
  startTime: number;
}

export interface IYourcallStorageMarkets {
  [key: string]: {
    [key: string]: {
      isRestored?: boolean;
      selections?: string[] | IYourcallStorageCustomSelection[];
    };
  };
}

export interface IYourcallStorageCustomSelection {
  playerName: string;
  statisticTitle: string;
  value: number;
}
