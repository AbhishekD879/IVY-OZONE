export interface IRequestConfig {
  requestParams: IInplayLiveStreamRequestParams;
  socket: {
    sport?: ISocketRequestConfig;
    competition?: ISocketRequestConfig;
  };
  cachePrefix?: string;
  limit?: number;
}

export interface ISocketRequestConfig {
  emit: string;
  on: Function;
}

export interface IDefaultConfig {
  requestParams: {
    emptyTypes: string;
    autoUpdates: string;
    isLiveNowType: boolean;
  };
  socket: {
    structure: {
      emit: string;
      on: string;
    };
    ribbon: {
      emit: string;
      on: string;
    }
  };
}

export interface IInplayLiveStreamRequestParams {
  topLevelType?: string;
  categoryId?: number;
  sportId?: string;
  typeId?: string;
  marketSelector?: string;
  modifyMainMarkets?: boolean;
  emptyTypes?: string;
  autoUpdates?: string;
  isLiveNowType?: boolean;
}
