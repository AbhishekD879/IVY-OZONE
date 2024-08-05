export const ILiveServeUpdMock = {
  lsOutcome: {
    subject_number: 446334653,
    ev_mkt_id: '116106848',
    names: { en: 'test' },
    fb_result: 'H',
    disporder: '0',
    status: 'A',
    subject: 'sTEST0446334653',
    lp_num: '1',
    lp_den: '9',
    cs_home: '1',
    cs_away: '1',
  },
  lsMarket: {
    subject_number: 446334653,
    ev_id: '6589319',
    group_names: { en: 'testName' },
    ev_oc_grp_id: '71141',
    ev_oc_grp_name: 'First Goalscorer',
    mkt_sort: 'FS',
    hcap_values: {
      H: '+1.0',
      A: '-1.0'
    },
    mkt_disp_code: '0',
    mm_coll_id: '255, 35',
    collections: [
      { collection_id: '1367, 619' },
      { collection_id: '1333, 400' }
    ],
    mkt_type: '',
    names: { en: 'test' },
    lp_avail: true,
    bet_in_run: true,
    disporder: '0',
    status: 'A',
    subject: 'sTEST0446334653',
    channel: 'SEVMKT0116106848',
    raw_hcap: 'rawHandicapValue',
    displayed: true
  },
  commonProperties: {
    id: '446334653',
    displayOrder: '0',
    liveServChannels: 'sTEST0446334653',
    name: 'test'
  },
  resultOutcome: {
    id: '446334653',
    displayOrder: '0',
    liveServChannels: 'sTEST0446334653',
    name: 'test',
    marketId: '116106848',
    outcomeMeaningMinorCode: 'H',
    outcomeStatusCode: 'A',
    prices: [{ priceNum: 1, priceDen: 9, priceType: 'LP', priceDec: 1.11 }],
    outcomeMeaningScores: '1,1,'
  },
  resultMarket: {
    id: '446334653',
    displayOrder: '0',
    liveServChannels: 'sTEST0446334653',
    name: 'test',
    eventId: '6589319',
    templateMarketId: '71141',
    dispSortName: '0',
    marketMeaningMajorCode: '',
    handicapValues: {
      H: '+1.0',
      A: '-1.0'
    },
    marketMeaningMinorCode: 'FS',
    isLpAvailable: true,
    isMarketBetInRun: true,
    marketStatusCode: 'A',
    liveServChildrenChannels: 'SEVMKT0116106848',
    rawHandicapValue: 'rawHandicapValue',
    displayed: true,
    templateMarketName: 'testName',
    collectionIds: '255, 35,1367, 619,1333, 400,'
  }
};
