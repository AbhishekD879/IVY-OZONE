export interface ICmsConfigMessages {
  selfExclusion ?: string;
  selfExclusionEnable ?: boolean;
  playBreak ?: string;
  playBreakEnable ?: boolean;
  immediateBreak ?: string;
  immediateBreakEnable ?: boolean;
}
export interface ICmsSelfExclusionConfig {
  SelfExclusion: ICmsConfigMessages;
}
export interface IPortalWindowObj {
  endDate: string;
  startDate: string;
}
export interface IRtmsResponse {
  type: string;
  payload?: PayloadDetails;
}
export interface IInitDataResp {
  isBlocked: boolean;
  productId: string;
}
export interface IInitDataRespClosure {
  closureDetails: IInitDataResp[];
}
export interface IInitDataRespServiceClosure {
  closureDetails: IInitDataRespClosure;
}

export interface IPlayBreakDetails {
  playBreak ?: string;
}
export interface IEventDetails {
  eventName ?: string;
  data ?: IPlayBreakDetails;
}

export interface PayloadDetails {
  PreferencesObject?: FanzoneDetails
}

export interface FanzoneDetails {
  TEAM_ID: string,
  TEAM_NAME: string
}