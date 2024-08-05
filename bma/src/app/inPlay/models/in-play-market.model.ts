import { ICollection } from './collection.model';
import { IName } from './name.model';
import { IOutcome } from './in-play-outcome.model';
import { IHcapValues } from './handicap-values.model';

export interface IMarket {
    outcome: IOutcome;
    marketId: number;
    names: IName;
    group_names: IName;
    ev_oc_grp_id: string;
    mkt_disp_code: string;
    mkt_disp_layout_columns: string;
    mkt_disp_layout_order: string;
    mkt_type: string;
    mkt_sort: string;
    mkt_grp_flags: string;
    ev_id: number;
    status: string;
    displayed: string;
    disporder: number;
    bir_index: string;
    raw_hcap: string;
    hcap_values: IHcapValues;
    ew_avail: string;
    ew_places: string;
    ew_fac_num: string;
    ew_fac_den: string;
    bet_in_run: string;
    lp_avail: string;
    sp_avail: string;
    mm_coll_id: string;
    suspend_at: string;
    collections: ICollection[];
}
