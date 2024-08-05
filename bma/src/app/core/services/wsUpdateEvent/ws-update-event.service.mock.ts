export const wsliveUpdate = {
  mockPriceUpdate: {
    event: {
      eventId: 7451432,
      market: {
        outcome: {
          outcomeId: 561070138,
          price: {
            lp_num: '1',
            lp_den: '9'
          }
        }
      }
    },
    publishedDate: 'Jun 22, 2017 9:57:17 AM',
    type: 'PRICE'
  },
  mockPriceSuspend: {
    event: {
      eventId: 7451432,
      market: {
        outcome: {
          outcomeId: 561070138,
          price: {
            status: 'S',
            lp_num: '1',
            lp_den: '9'
          }
        }
      }
    },
    publishedDate: 'Jun 22, 2017 9:57:17 AM',
    type: 'PRICE'
  },

  mockEventS: {
    event: {
      'names': {
        'en': 'Tzu-Ying Tai v Ratchanok Intanon'
      },
      'status': 'S',
      'displayed': 'Y',
      'result_conf': 'N',
      'disporder': 0,
      'start_time': '2017-06-22 10:40:00',
      'start_time_xls': {
        'en': '22nd of Jun 2017  10:40 am'
      },
      'suspend_at': '',
      'is_off': 'Y',
      'started': 'Y',
      'race_stage': '',
      'eventId': 7451432,
      'market': {
        'outcome': {}
      }
    },
    publishedDate: 'Jun 22, 2017 9:57:17 AM',
    type: 'EVENT'
  },
  mockEventA: {
    event: {
      'names': {
        'en': 'Tzu-Ying Tai v Ratchanok Intanon'
      },
      'status': 'A',
      'displayed': 'Y',
      'result_conf': 'N',
      'disporder': 0,
      'start_time': '2017-06-22 10:40:00',
      'start_time_xls': {
        'en': '22nd of Jun 2017  10:40 am'
      },
      'suspend_at': '',
      'is_off': 'Y',
      'started': 'Y',
      'race_stage': '',
      'eventId': 7451432,
      'market': {
        'outcome': {}
      }
    },
    publishedDate: 'Jun 22, 2017 9:57:17 AM',
    type: 'EVENT'
  },
  mockEventUndisplayed: {
    event: {
      'names': {
        'en': 'Tzu-Ying Tai v Ratchanok Intanon'
      },
      'status': 'A',
      'displayed': 'N',
      'result_conf': 'N',
      'disporder': 0,
      'start_time': '2017-06-22 10:40:00',
      'start_time_xls': {
        'en': '22nd of Jun 2017  10:40 am'
      },
      'suspend_at': '',
      'is_off': 'Y',
      'started': 'Y',
      'race_stage': '',
      'eventId': 7451432,
      'market': {
        'outcome': {}
      }
    },
    publishedDate: 'Jun 22, 2017 9:57:17 AM',
    type: 'EVENT'
  },

  mockMarketA: {
    event: {
      'eventId': 7451432,
      'market': {
        'names': {
          'en': '1st Round Leader'
        },
        'group_names': {
          'en': 'Outright'
        },
        'ev_oc_grp_id': '471853',
        'mkt_disp_layout_columns': '0',
        'mkt_disp_layout_order': 'DFLT',
        'status': 'A',
        'displayed': 'Y',
        'disporder': 0,
        'raw_hcap': '',
        'hcap_values': {},
        'ew_avail': 'Y',
        'ew_places': '3',
        'ew_fac_num': '1',
        'ew_fac_den': '4',
        'bet_in_run': 'Y',
        'lp_avail': 'Y',
        'sp_avail': 'N',
        'mm_coll_id': '2816',
        'suspend_at': '',
        'collections': [{
          'collection_id': '2147'
        }],
        'marketId': 174859496,
        'outcome': {}
      }
    },
    publishedDate: 'Jun 22, 2017 9:57:17 AM',
    type: 'EVMKT'
  },
  mockMarketS: {
    event: {
      'eventId': 7451432,
      'market': {
        'names': {
          'en': '1st Round Leader'
        },
        'group_names': {
          'en': 'Outright'
        },
        'ev_oc_grp_id': '471853',
        'mkt_disp_layout_columns': '0',
        'mkt_disp_layout_order': 'DFLT',
        'status': 'S',
        'displayed': 'Y',
        'disporder': 0,
        'raw_hcap': '',
        'hcap_values': {},
        'ew_avail': 'Y',
        'ew_places': '3',
        'ew_fac_num': '1',
        'ew_fac_den': '4',
        'bet_in_run': 'Y',
        'lp_avail': 'Y',
        'sp_avail': 'N',
        'mm_coll_id': '2816',
        'suspend_at': '',
        'collections': [{
          'collection_id': '2147'
        }],
        'marketId': 174859496,
        'outcome': {}
      }
    },
    publishedDate: 'Jun 22, 2017 9:57:17 AM',
    type: 'EVMKT'
  },
  mockMarketUndisplayed: {
    'publishedDate': 'Jun 23, 2017 7:36:09 AM',
    'type': 'EVMKT',
    'event': {
      'eventId': 7451432,
      'market': {
        'names': {
          'en': 'Match Result'
        },
        'group_names': {
          'en': 'Match Betting'
        },
        'ev_oc_grp_id': '37241',
        'mkt_disp_code': 'MR',
        'mkt_disp_layout_columns': '3',
        'mkt_disp_layout_order': 'FBRESULT',
        'mkt_type': '-',
        'mkt_sort': 'MR',
        'mkt_grp_flags': '',
        'status': 'A',
        'displayed': 'N',
        'disporder': -1,
        'bir_index': '',
        'raw_hcap': '',
        'hcap_values': {},
        'ew_avail': 'N',
        'ew_places': '',
        'ew_fac_num': '',
        'ew_fac_den': '',
        'bet_in_run': 'Y',
        'lp_avail': 'Y',
        'sp_avail': 'N',
        'mm_coll_id': '1297',
        'suspend_at': '',
        'collections': [{
          'collection_id': '619'
        }, {
          'collection_id': '4920'
        }],
        'marketId': 174859496,
        'outcome': {}
      }
    }
  }
};

export const eventMock = {
  eventMockDefault: {
    id: '7451432',
    eventStatusCode: 'A',
    markets: [{
      marketStatusCode: 'A',
      id: '174859496',
      outcomes: [
        {
          outcomeStatusCode: 'A',
          id: '561070138',
          prices: [
            {
              priceDec: '14.00',
              priceDen: '1',
              priceNum: '13',
              priceType: 'LP'
            }
          ]
        }
      ]
    }
    ]
  },
  eventMockSuspended: {
    id: '7451432',
    eventStatusCode: 'S',
    markets: [{
      marketStatusCode: 'S',
      id: '174859496',
      outcomes: [
        {
          outcomeStatusCode: 'S',
          id: '561070138',
          prices: [
            {
              priceDec: '14.00',
              priceDen: '1',
              priceNum: '13',
              priceType: 'LP'
            }
          ]
        }
      ]
    }
    ]
  }
};
