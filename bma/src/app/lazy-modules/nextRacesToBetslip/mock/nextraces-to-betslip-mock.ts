
export const mostTippedHorsesEventsMock = [
  {
    cashoutAvail: 'Y',
    categoryCode: 'HORSE_RACING',
    categoryDisplayOrder: '4',
    categoryId: '21',
    eventStatusCode: 'A',
    id: 1024863,
    isActive: true,
    localTime: '12:00',
    typeName:'test',
    startTime: 'Wed Jul 15 2020 11:51:57 GMT+0530',
    name: 'Southwell',
    nameOverride: 'test over',
    horses: [
      {
        horseName: 'a',
        isMostTipped: true,
        silk: '123.png',
      },
      {
        horseName: 'b',
        isMostTipped: false,
        silk: '123.png',

      },
    ],
    powerHorse: {
      horseName: 'Sancta Sedes',
      silk: '123.png',
      trainer: 'a',
      jockey: '1',
      isBeatenFavourite: true
    },
    markets: [
      {
        cashoutAvail: 'N',
        correctPriceTypeCode: 'SP',
        displayOrder: 0,
        eachWayFactorDen: '4',
        eachWayFactorNum: '1',
        eachWayPlaces: '3',
        eventId: '1024863',
        id: '35033769',
        children: [
          {
            outcome: {
              displayOrder: 1,
              icon: false,
              id: '125825053',
              name: 'Sancta Sedes',
              silkName: '123.png',
              prices: [{
                priceNum: '9',
                priceDen: '2'
              }
            ]
            }

          }
        ],
        priceTypeCodes: 'SP,',
      },
    ],
    isMostPowerHorse: true
  }
];
