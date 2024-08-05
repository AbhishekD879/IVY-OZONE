export const sportEventMock = {
  cashoutAvail: 'Y',
  categoryCode: 'HORSE_RACING',
  categoryDisplayOrder: '4',
  categoryId: '21',
  categoryName: 'Horse Racing',
  classDisplayOrder: -50,
  classFlagCodes: 'UF,LI,',
  classId: 223,
  className: 'Horse Racing - Live',
  classSortCode: 'HR',
  correctedDay: 'racing.dayWednesday',
  displayOrder: 975,
  drilldownTagNames: 'EVFLAG_RVA,',
  eventIsLive: false,
  eventSortCode: 'MTCH',
  eventStatusCode: 'A',
  id: 9458938,
  isActive: 'true',
  isAvailable: 'true',
  isNext24HourEvent: 'true',
  isOpenEvent: 'true',
  isUS: false,
  liveEventOrder: 1,
  liveServChannels: 'sEVENT0009458938,',
  liveServChildrenChannels: 'SEVENT0009458938,',
  liveStreamAvailable: true,
  localTime: '16:15',
  lpAvailable: undefined,
  markets: [{
    cashoutAvail: 'Y',
    collectionIds: '4158,',
    collectionNames: 'Win or Each Way,',
    displayOrder: 0,
    eachWayFactorDen: '4',
    eachWayFactorNum: '1',
    eachWayPlaces: '4',
    eventId: '9458938',
    id: '140377392',
    isActive: 'true',
    isAvailable: 'true',
    isEachWayAvailable: 'true',
    isSpAvailable: 'true',
    liveServChannels: 'sEVMKT0140377392,',
    liveServChildrenChannels: 'SEVMKT0140377392,',
    marketMeaningMajorCode: '-',
    marketMeaningMinorCode: '--',
    marketStatusCode: 'A',
    maxAccumulators: '25',
    minAccumulators: '1',
    name: 'Win or Each Way',
    ncastTypeCodes: 'CT,SF,CF,RF,TC,'
  }],
  name: 'CagnesSurMer',
  originalName: '16:15 CagnesSurMer',
  raceLength: '7.455',
  raceLengthUnit: 'FR',
  rawIsOffCode: 'N',
  responseCreationTime: '2019-01-30T12:47:11.781Z',
  siteChannels: 'P,Q,C,I,M,',
  sportId: '21',
  startTime: 1548864900000,
  streamProviders: {RacingUK: true, Perform: false, AtTheRaces: false, IMG: false, RPGTV: false, iGameMedia: false},
  typeDisplayOrder: 0,
  typeFlagCodes: 'GVA,RVA,INT,',
  typeId: 1904,
  typeName: 'Cagnessurmer'
};

export const filteredEventsDataMock = {
  groupedByMeetings: {
    Cagnessurmer:  sportEventMock
  },
  groupedByFlagAndData: [
    {
      flag: 'UK',
      data: [
        {
          meeting: 'Cagnessurmer',
          events:  sportEventMock
        }
      ]}
  ]
};
