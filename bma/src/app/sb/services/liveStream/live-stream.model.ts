export interface ILiveStreamConfigObject {
  drilldownTagNames: string;
  type: string;
  typeFlagCodes: string;
}

export interface IStreamProviders {
  AtTheRaces?: boolean;
  IMG?: boolean;
  Perform?: boolean;
  RPGTV?: boolean;
  RacingUK?: boolean;
  iGameMedia?: boolean;
}

export interface IStreamAvailable {
  liveStreamAvailable: boolean;
  streamProviders: IStreamProviders;
}
