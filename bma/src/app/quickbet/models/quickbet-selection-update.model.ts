import { IQuickbetDeltaHandicap } from '@app/quickbet/models/quickbet-delta-object.model';

interface IQuickbetUpdateChannel {
  id: number;
  name: string;
  type: string;
}

interface IQuickbetUpdateEvent {
  id: number;
}

interface IQuickbetUpdateMessage {
  is_off?: string;
  lp_den?: string;
  lp_num?: string;
  bet_in_run?: string;
  bir_index?: string;
  collections?: IQuickbetUpdateMessageCollections[];
  displayed?: string;
  disporder?: number;
  ev_id?: number;
  ev_oc_grp_id?: string;
  ew_avail?: string;
  ew_fac_den?: string;
  ew_fac_num?: string;
  ew_places?: string;
  group_names?: IQuickbetUpdateLang;
  hcap_values?: IQuickbetDeltaHandicap;
  lp_avail?: string;
  mkt_disp_code?: string;
  mkt_disp_layout_columns?: string;
  mkt_disp_layout_order?: string;
  mkt_grp_flags?: string;
  mkt_sort?: string;
  mkt_type?: string;
  mm_coll_id?: string;
  names?: IQuickbetUpdateLang;
  raw_hcap?: string;
  race_stage?: string;
  result_conf?: string;
  start_time?: string;
  start_time_xls?: IQuickbetUpdateLang;
  sp_avail?: string;
  status?: string;
  suspend_at?: string;
}

interface IQuickbetUpdateMessageCollections {
  collection_id: string;
}

interface IQuickbetUpdateLang {
  en: string;
}

interface IQuickbetUpdateSubChannel {
  id: number;
  name: string;
  type: string;
}

export interface IQuickbetSelectionUpdateModel {
  channel: IQuickbetUpdateChannel;
  event: IQuickbetUpdateEvent;
  message: IQuickbetUpdateMessage;
  subChannel: IQuickbetUpdateSubChannel;
  type: string;
}
