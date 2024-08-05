interface ILiveClockUpdate {
  event: {
    clock: {
      clock_seconds: string;
      last_update: string;
      last_update_secs: string;
      offset_secs: string;
      period_code: string;
      period_index: string;
      start_time_secs: string;
      state: string;
    };
    eventId: number;
  };
  publishedDate: string;
  type: string;
}

interface IEventUpdate {
  event: {
    displayed: string;
    disporder: number;
    eventId: number;
    is_off: string;
    market: {
      outcome: {}
    };
    names: {
      en: string;
    };
    race_stage: string;
    result_conf: string;
    start_time: string;
    start_time_xls: {
      en: string;
    };
    started: string;
    status: string;
    suspend_at: string;
  };
  publishedDate: string;
  type: string;
}

interface IMarketUpdate {
  event: {
    market: {
      bet_in_run: string;
      bir_index: string;
      collections: {
        collection_id: string;
      }[];
      displayed: string;
      disporder: number;
      ev_id: number;
      ev_oc_grp_id: string;
      ew_avail: string;
      ew_fac_den: string;
      ew_fac_num: string;
      ew_places: string;
      group_names: {
        en: string;
      };
      hcap_values: {};
      lp_avail: string;
      marketId: number;
      mkt_disp_code: string;
      mkt_disp_layout_columns: string;
      mkt_disp_layout_order: string;
      mkt_grp_flags: string;
      mkt_sort: string;
      mkt_type: string;
      mm_coll_id: string;
      names: {
        en: string;
      };
      outcome: {};
      raw_hcap: string;
      sp_avail: string;
      status: string;
      suspend_at: string;
    };
    eventId: number;
  };
  publishedDate: string;
  type: string;
}

interface IOutcomeUpdate {
  event: {
    market: {
      marketId: number;
      outcome: {
        cs_away: string;
        cs_home: string;
        displayed: string;
        disporder: number;
        fb_result: string;
        lp_den: string;
        lp_num: string;
        names: {
          en: string;
        };
        outcomeId: number;
        price: {
          lp_den: string;
          lp_num: string;
        };
        result: string;
        runner_num: string;
        settled: string;
        status: string;
        unique_id: string;
      }
    };
    eventId: number;
  };
  publishedDate: string;
  type: string;
}

interface ILIvePriceUpdate {
  event: {
    market: {
      outcome: {
        outcomeId: number;
        price: {
          lp_den: string;
          lp_num: string;
        }
      }
    };
    eventId: number;
  };
  publishedDate: string;
  type: string;
}

interface IScoreBoardUpdate {
  event: {
    scoreboard: {
      ALL: {
        role_code: string;
        value: string;
      }[];
      CURRENT: {
        role_code: string;
        value: string;
      }[];
    };
    eventId: number;
  };
  publishedDate: string;
  type: string;
}


export type IWSLiveUpdate = ILiveClockUpdate | IEventUpdate |IMarketUpdate | IOutcomeUpdate | ILIvePriceUpdate | IScoreBoardUpdate;
