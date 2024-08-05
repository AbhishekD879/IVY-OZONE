import { IMarket } from '@core/models/market.model';
import { ICollection } from '@app/inPlay/models/collection.model';
import { ITypedScoreData } from '@core/services/scoreParser/models/score-data.model';

export interface IPayload {
  isDisplayed?: boolean;
  names?: INames;
  status?: string;
  displayed?: string;
  result_conf?: string;
  result?: string;
  disporder?: number;
  start_time?: string;
  start_time_xls?: INames;
  runner_num?: string;
  suspend_at?: string;
  is_off?: string;
  subject?: string;
  started?: string;
  ev_id: string;
  ev_mkt_id: string;
  race_stage?: string;
  lp_den?: string;
  lp_num?: string;
  raw_hcap?: number | string;
  hcap_values?: IHCapValues;
  mkt_disp_code?: string;
  group_names?: INames;
  cs_home?: string;
  cs_away?: string;
  mm_coll_id?: string;
  lp_avail?: string;
  sp_avail?: string;
  scores?: {
    home: {
      name: string;
      score: string;
      currentPoints: string;
    };
    away: {
      name: string;
      score: string;
      currentPoints: string;
    };
  } | ITypedScoreData;
  collections?: ICollection[];
  scoreType?: string;
  clock_seconds?: string;
  last_update?: string;
  last_update_secs?: string;
  offset_secs?: string;
  period_code?: string;
  sport?: string;
  start_time_secs?: string;
  state?: string;
  period_index?: string;
  ew_avail?: string;
  fc_avail?: string;
  tc_avail?: string;
  vod?:boolean;
}

export interface IHCapValues {
  H: string;
  A: string;
  B: string;
  L: string;
  E: string;
}

export interface ILiveServeUpd {
  id: number;
  type: string;
  channel?: string;
  msg_id?: string;
  user_id?: number;
  subject?: string;
  payload: IPayload;
  channel_type?: string;
  channel_number?: number;
  subject_type?: string;
  subject_number?: number;
}

export interface INames {
  en: string;
}

export interface IStreamProviders {
    RacingUK: boolean;
    Perform: boolean;
    AtTheRaces: boolean;
    IMG: boolean;
    RPGTV: boolean;
    iGameMedia: boolean;
}

export interface IReference {
    id: number;
    name: string;
    eventStatusCode: string;
    isActive: string;
    displayOrder: number;
    siteChannels: string;
    eventSortCode: string;
    startTime: number;
    rawIsOffCode: string;
    isStarted: string;
    classId: number;
    typeId: number;
    sportId: string;
    liveServChannels: string;
    liveServChildrenChannels: string;
    categoryId: string;
    categoryCode: string;
    categoryName: string;
    categoryDisplayOrder: string;
    className: string;
    classDisplayOrder: number;
    classSortCode: string;
    typeName: string;
    typeDisplayOrder: number;
    isOpenEvent: string;
    isLiveNowEvent: string;
    isLiveNowOrFutureEvent: string;
    drilldownTagNames: string;
    isAvailable: string;
    cashoutAvail: string;
    responseCreationTime: Date;
    localTime: string;
    originalName: string;
    isUS: boolean;
    markets: IMarket[];
    correctedDay: string;
    eventIsLive: boolean;
    liveEventOrder: number;
    liveStreamAvailable: boolean;
    streamProviders: IStreamProviders;
    liveSimAvailable: boolean;
    isUKorIRE: boolean;
    filteredTime: string;
    persistentInCache?: boolean;
}

export interface IEventData {
    path: any[];
    expire: number;
    reference: IReference;
}

export interface IEventRefence {
  eventdata: IEventData;
}
