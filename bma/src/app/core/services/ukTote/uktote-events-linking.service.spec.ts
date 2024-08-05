
import { of as observableOf } from 'rxjs';
import { UkToteEventsLinkingService } from './uktote-events-linking.service';
describe('UkToteEventsLinkingService', () => {
  let service: UkToteEventsLinkingService;

  let siteServerService;
  beforeEach(() => {
    siteServerService = {
      getEvent: jasmine.createSpy().and.returnValue(observableOf({}))
    };

    service = new UkToteEventsLinkingService(siteServerService);
  });

  describe('extendToteEvents:', () => {
    it('isScoop6Pool false', () => {
      service.extendToteEvents(<any>[{
        externalKeys: {
          OBEvLinkNonTote: 123456
        }
      }], false, {
        extendEvent: () => {},
        extendMarket: () => {},
        extendOutcome: () => {}
      });
      expect(siteServerService.getEvent).toHaveBeenCalledTimes(1);
      expect(siteServerService.getEvent).toHaveBeenCalledWith(
        '123456', { racingFormOutcome: true }, false
      );
    });

    it('isScoop6Pool true', () => {
      service.extendToteEvents(<any>[{
        id: 123456,
        typeName: ''
      }], true, {
        extendEvent: () => {},
        extendMarket: () => {},
        extendOutcome: () => {}
      });
      expect(siteServerService.getEvent).toHaveBeenCalledTimes(1);
      expect(siteServerService.getEvent).toHaveBeenCalledWith(
        '~ext-OBEvLinkScoop6:event:123456',
        { racingFormOutcome: true, externalKeysEvent: true },
        false
      );
    });
  });

  it('extendToteEventInfo', () => {
    const extendEvent = jasmine.createSpy();
    const extendMarket = jasmine.createSpy();
    const extendOutcome = jasmine.createSpy();
    service.extendToteEventInfo(<any>{
      markets: [{
        outcomes: [{
          name: 'Hamilton'
        }]
      }]
    }, <any>{
      markets: [{
        outcomes: [{
          name: 'Hamilton'
        }]
      }]
    }, {
      extendEvent: extendEvent,
      extendMarket: extendMarket,
      extendOutcome: extendOutcome
    });

    expect(extendEvent).toHaveBeenCalledTimes(1);
    expect(extendMarket).toHaveBeenCalledTimes(1);
    expect(extendOutcome).toHaveBeenCalledTimes(1);
  });
  it('extendToteEventInfo', () => {
    const extendEvent = jasmine.createSpy();
    const extendMarket = jasmine.createSpy();
    const extendOutcome = jasmine.createSpy();
    service.extendToteEventInfo(<any>{
      markets: [{
        outcomes: [{
          name: 'Hamilton'
        }]
      }]
    }, <any>{
      markets: [{
        outcomes: [{
          name: 'Hamilton1'
        }]
      }]
    }, {
      extendEvent: extendEvent,
      extendMarket: extendMarket,
      extendOutcome: extendOutcome
    });

    expect(extendEvent).toHaveBeenCalledTimes(1);
    expect(extendMarket).toHaveBeenCalledTimes(1);
    expect(extendOutcome).toHaveBeenCalledTimes(0);
  });

  it('extendToteEventInfo with null', () => {
    const extendEvent = jasmine.createSpy();
    const extendMarket = jasmine.createSpy();
    const extendOutcome = jasmine.createSpy();
    const data = service.extendToteEventInfo(null, null, {
      extendEvent: extendEvent,
      extendMarket: extendMarket,
      extendOutcome: extendOutcome
    });

    expect(data).toBeUndefined();
  });

  describe('compareOutcomes', () => {
    it('should return true if outcomes names match', () => {
      const outcome = {
          name: 'Diamond Express'
        },
        linkedOutocme = {
          name: 'Diamond Express'
        };
      expect(service['compareOutcomes'](<any>outcome, <any>linkedOutocme)).toBeTruthy();
    });

    it('should return true if outcomes names match (when name of' +
      ' one outcome is in camel case like in International TOTE)', () => {
      const outcome = {
          name: 'Diamond Express'
        },
        linkedOutocme = {
          name: 'DIAMOND EXPRESS'
        };
      expect(service['compareOutcomes'](<any>outcome, <any>linkedOutocme)).toBeTruthy();
    });

    it('should return false if outcomes names match', () => {
      const outcome = {
          name: 'Diamond Express'
        },
        linkedOutocme = {
          name: 'Duba Plains'
        };
      expect(service['compareOutcomes'](<any>outcome, <any>linkedOutocme)).toBeFalsy();
    });

    it('should return true if only main outcome become N/R', () => {
      const outcome = {
          name: 'Diamond Express N/R'
        },
        linkedOutocme = {
          name: 'Diamond Express'
        };
      expect(service['compareOutcomes'](<any>outcome, <any>linkedOutocme)).toBeTruthy();
    });

    it('should return true if only linked outcome become N/R', () => {
      const outcome = {
          name: 'Diamond Express'
        },
        linkedOutocme = {
          name: 'Diamond Express N/R'
        };
      expect(service['compareOutcomes'](<any>outcome, <any>linkedOutocme)).toBeTruthy();
    });

    it('should return true if only linked outcome become N/R ' +
      '(first of outcomes is in camel case like in International TOTE)', () => {
      const outcome = {
          name: 'DIAMOND EXPRESS'
        },
        linkedOutocme = {
          name: 'Diamond Express N/R'
        };
      expect(service['compareOutcomes'](<any>outcome, <any>linkedOutocme)).toBeTruthy();
    });

    it('should return true if only linked outcome become N/R ' +
      '(second of outcomes is in in camel case like in International TOTE)', () => {
      const outcome = {
          name: 'Diamond Express'
        },
        linkedOutocme = {
          name: 'DIAMOND EXPRESS N/R'
        };
      expect(service['compareOutcomes'](<any>outcome, <any>linkedOutocme)).toBeTruthy();
    });
  });

  describe('loadEventsByScoop6EventIds', () => {
    it('should call siteServerFactory.getEvent method with zero events', () => {
      expect(service['loadEventsByScoop6EventIds'](null)).toBeDefined();
      const eventIds = [];
      expect(service['loadEventsByScoop6EventIds'](eventIds)).toBeDefined();
    });
    it('should call siteServerFactory.getEvent method', () => {
      const eventIds = [111, 222],
        options = { racingFormOutcome: true, externalKeysEvent: true },
        externalIds = '~ext-OBEvLinkScoop6:event:111,~ext-OBEvLinkScoop6:event:222';
      service['loadEventsByScoop6EventIds'](eventIds);
      expect(siteServerService.getEvent).toHaveBeenCalledWith(externalIds, options, false);
    });
  });
  it('should call loadEventsByEventIds with zero events', () => {
    expect(service['loadEventsByEventIds'](null)).toBeDefined();
    const eventIds = [];
    expect(service['loadEventsByEventIds'](eventIds)).toBeDefined();
  });
  describe('getPrimaryMarket', () => {
    it('should return first market according to displayOrder property', () => {
        expect(service['getPrimaryMarket'](({
          markets: [
            {
              id: 123,
              displayOrder: 100
            },
            {
              id: 549,
              displayOrder: 0
            }
          ]
        }) as any)).toEqual(({
          id: 549,
          displayOrder: 0
        }) as any);
    });

    it('should return null market propery missed', () => {
      expect(service['getPrimaryMarket'](({}) as any)).toEqual(null);
    });
  });
  describe('extendScoop6ToteEvents', () => {
    it('should call siteServerFactory.getEvent method', () => {
      const scoop6Events = [{ "id": 25233594, "name": "2m 2 1/2f HCap Hurdle", "eventStatusCode": "A", "isActive": "true", "isDisplayed": "true", "displayOrder": 0, "siteChannels": "P,I,", "eventSortCode": "MTCH", "startTime": 1679405400000, "rawIsOffCode": "N", "classId": 321, "typeId": 2391, "sportId": "21", "raceNumber": "1", "liveServChannels": "sEVENT0025255809,", "liveServChildrenChannels": "SEVENT0025255809,", "categoryId": "21", "categoryCode": "HORSE_RACING", "categoryName": "Horse Racing", "categoryDisplayOrder": "-9971", "className": "Horse Racing - Tote Pools", "classDisplayOrder": 0, "classSortCode": "HR", "typeName": "Market Rasen (MN)", "typeDisplayOrder": 100, "isOpenEvent": "true", "isNext6HourEvent": "true", "isNext12HourEvent": "true", "isNext24HourEvent": "true", "isNext2DayEvent": "true", "isNext1WeekEvent": "true", "drilldownTagNames": "EVFLAG_HC,", "isAvailable": "true", "groupNumber": "1", "cashoutAvail": "N", "responseCreationTime": "2023-03-21T07:45:19.841Z",
       "externalKeys": { "OBEvLinkScoop6": 25233594 }, "localTime": "7:00", "originalName": "2m 2 1/2f HCap Hurdle", "isUS": false, "markets": [{ "id": "619722655", "eventId": "25255809", "templateMarketId": "206447", "templateMarketName": "Pool Betting", "marketMeaningMajorCode": "-", "marketMeaningMinorCode": "--", "name": "Pool Betting", "displayOrder": 0, "marketStatusCode": "A", "isActive": "true", "isDisplayed": "true", "siteChannels": "P,I,", "liveServChannels": "sEVMKT0619722655,", "liveServChildrenChannels": "SEVMKT0619722655,", "isPoolAvailable": "true", "isAvailable": "true", "maxAccumulators": "25", "minAccumulators": "1", "cashoutAvail": "N", "termsWithBet": "N", "outcomes": [{ "id": "1996708925", "marketId": "619722655", "name": "Unnamed Favourite", "outcomeMeaningMajorCode": "--", "outcomeMeaningMinorCode": "1", "runnerNumber": "0", "displayOrder": 0, "outcomeStatusCode": "A", "isActive": "true", "isDisplayed": "true", "siteChannels": "P,I,", "liveServChannels": "sSELCN1996708925,", "liveServChildrenChannels": "SSELCN1996708925,", "isAvailable": "true", "cashoutAvail": "N", "trapNumber": 0, "prices": [] }, { "id": "1996708991", "marketId": "619722655", "name": "Thankyourluckystar", "outcomeMeaningMajorCode": "--", "runnerNumber": "3", "displayOrder": 0, "outcomeStatusCode": "A", "isActive": "true", "isDisplayed": "true", "siteChannels": "P,I,", "liveServChannels": "sSELCN1996708991,", "liveServChildrenChannels": "SSELCN1996708991,", "isAvailable": "true", "cashoutAvail": "N", "trapNumber": 3, "prices": [{ "id": "3", "priceType": "pool", "poolId": "4319889", "poolType": "UWIN", "priceDec": 1.3, "isActive": "true", "displayOrder": "1" }, { "id": "4", "priceType": "pool", "poolId": "4319890", "poolType": "UEXA", "priceDec": 1.5, "isActive": "true", "displayOrder": "1" }] }, { "id": "1996708993", "marketId": "619722655", "name": "East End Girl", "outcomeMeaningMajorCode": "--", "runnerNumber": "4", "displayOrder": 0, "outcomeStatusCode": "A", "isActive": "true", "isDisplayed": "true", "siteChannels": "P,I,", "liveServChannels": "sSELCN1996708993,", "liveServChildrenChannels": "SSELCN1996708993,", "isAvailable": "true", "cashoutAvail": "N", "trapNumber": 4, "prices": [] }, { "id": "1996708988", "marketId": "619722655", "name": "Fiston De Becon", "outcomeMeaningMajorCode": "--", "runnerNumber": "2", "displayOrder": 0, "outcomeStatusCode": "A", "isActive": "true", "isDisplayed": "true", "siteChannels": "P,I,", "liveServChannels": "sSELCN1996708988,", "liveServChildrenChannels": "SSELCN1996708988,", "isAvailable": "true", "cashoutAvail": "N", "trapNumber": 2, "prices": [{ "id": "5", "priceType": "pool", "poolId": "4319889", "poolType": "UWIN", "priceDec": 1.9, "isActive": "true", "displayOrder": "1" }, { "id": "6", "priceType": "pool", "poolId": "4319890", "poolType": "UEXA", "priceDec": 1.5, "isActive": "true", "displayOrder": "1" }] }, { "id": "1996708987", "marketId": "619722655", "name": "Surtitle", "outcomeMeaningMajorCode": "--", "runnerNumber": "1", "displayOrder": 0, "outcomeStatusCode": "A", "isActive": "true", "isDisplayed": "true", "siteChannels": "P,I,", "liveServChannels": "sSELCN1996708987,", "liveServChildrenChannels": "SSELCN1996708987,", "isAvailable": "true", "cashoutAvail": "N", "trapNumber": 1, "prices": [] }] }], "correctedDay": "racing.dayTuesday", "correctedDayValue": "racing.today", "eventIsLive": false, "liveEventOrder": 1 }] as any;
      const extendEvent = jasmine.createSpy();
      const extendMarket = jasmine.createSpy();
      const extendOutcome = jasmine.createSpy();
      const resp = [{"id":25233599,"name":"Market Rasen","eventStatusCode":"A","isActive":"true","isDisplayed":"true","displayOrder":985,"siteChannels":"P,Q,C,G,W,I,M,","eventSortCode":"MTCH",
      "externalKeys": { "OBEvLinkScoop6": 25233594 }, "startTime":1679415900000,"rawIsOffCode":"N","classId":223,"typeId":1950,"sportId":"21",
      "liveServChannels":"sEVENT0025233599,","liveServChildrenChannels":"SEVENT0025233599,","categoryId":"21","categoryCode":"HORSE_RACING",
      "categoryName":"Horse Racing","categoryDisplayOrder":"-9971","className":"Horse Racing - Live",
      "classDisplayOrder":-9999,"classSortCode":"HR","classFlagCodes":"UF,LI,","typeName":"Market Rasen",
      "typeDisplayOrder":-31370,"typeFlagCodes":"UK,QL,RVA,","isOpenEvent":"true","isNext12HourEvent":"true",
      "isNext24HourEvent":"true","isNext2DayEvent":"true","isNext1WeekEvent":"true",
      "isLiveNowOrFutureEvent":"true","drilldownTagNames":"EVFLAG_BL,EVFLAG_RVA,",
      "isAvailable":"true","mediaTypeCodes":"VST,","cashoutAvail":"Y","raceLength":"23.073",
      "raceLengthUnit":"FR","effectiveGpStartTime":"2023-03-19T10:00:00Z",
      "responseCreationTime":"2023-03-21T07:48:05.654Z","localTime":"16:25","originalName":"16:25 Market Rasen","isUS":false,"markets":[{"id":"619184436","eventId":"25233599","templateMarketId":"136933","templateMarketName":"Win or Each Way","marketMeaningMajorCode":"-","marketMeaningMinorCode":"--","name":"Win or Each Way","isLpAvailable":"true","isSpAvailable":"true","isGpAvailable":"true","isEachWayAvailable":"true","eachWayFactorNum":"1","eachWayFactorDen":"1","eachWayPlaces":"1","isMarketBetInRun":"true","displayOrder":0,"marketStatusCode":"A","isActive":"true","isDisplayed":"true","siteChannels":"P,Q,C,G,W,I,M,","liveServChannels":"sEVMKT0619184436,","liveServChildrenChannels":"SEVMKT0619184436,","priceTypeCodes":"LP,GP,SP,","ncastTypeCodes":"SF,CF,RF,","isAvailable":"true","maxAccumulators":"25","minAccumulators":"1","cashoutAvail":"Y","termsWithBet":"N","outcomes":[{"id":"1994973282","marketId":"619184436","name":"Ripper Roo","outcomeMeaningMajorCode":"--","runnerNumber":"5","displayOrder":5,"outcomeStatusCode":"A","isActive":"true","isDisplayed":"true","siteChannels":"P,Q,C,G,W,I,M,","liveServChannels":"sSELCN1994973282,","liveServChildrenChannels":"SSELCN1994973282,","isAvailable":"true","trapNumber":5,"prices":[{"id":"1","priceType":"LP","priceNum":5,"priceDen":1,"priceDec":6,"isActive":"true","displayOrder":"1"}]},{"id":"1994973283","marketId":"619184436","name":"Unnamed 2nd Favourite","outcomeMeaningMajorCode":"--","outcomeMeaningMinorCode":"2","displayOrder":7,"outcomeStatusCode":"A","isActive":"true","isDisplayed":"true","siteChannels":"P,Q,C,G,W,I,M,","liveServChannels":"sSELCN1994973283,","liveServChildrenChannels":"SSELCN1994973283,","isAvailable":"true","prices":[]},{"id":"1994973284","marketId":"619184436","name":"Unnamed Favourite","outcomeMeaningMajorCode":"--","outcomeMeaningMinorCode":"1","displayOrder":6,"outcomeStatusCode":"A","isActive":"true","isDisplayed":"true","siteChannels":"P,Q,C,G,W,I,M,","liveServChannels":"sSELCN1994973284,","liveServChildrenChannels":"SSELCN1994973284,","isAvailable":"true","prices":[]},{"id":"1994973285","marketId":"619184436","name":"Storm Dennis N/R","outcomeMeaningMajorCode":"--","runnerNumber":"4","isResulted":"true","displayOrder":4,"outcomeStatusCode":"S","isDisplayed":"true","siteChannels":"P,Q,C,G,W,I,M,","liveServChannels":"sSELCN1994973285,","liveServChildrenChannels":"SSELCN1994973285,","isFinished":"true","trapNumber":4,"prices":[{"id":"2","priceType":"LP","priceNum":15,"priceDen":8,"priceDec":2.87,"isActive":"true","displayOrder":"1"}]},{"id":"1994973286","marketId":"619184436","name":"Bold Soldier","outcomeMeaningMajorCode":"--","runnerNumber":"3","displayOrder":3,"outcomeStatusCode":"A","isActive":"true","isDisplayed":"true","siteChannels":"P,Q,C,G,W,I,M,","liveServChannels":"sSELCN1994973286,","liveServChildrenChannels":"SSELCN1994973286,","isAvailable":"true","trapNumber":3,"prices":[{"id":"3","priceType":"LP","priceNum":6,"priceDen":4,"priceDec":2.5,"isActive":"true","displayOrder":"1"}]},{"id":"1994973287","marketId":"619184436","name":"The Kniphand","outcomeMeaningMajorCode":"--","runnerNumber":"2","displayOrder":2,"outcomeStatusCode":"A","isActive":"true","isDisplayed":"true","siteChannels":"P,Q,C,G,W,I,M,","liveServChannels":"sSELCN1994973287,","liveServChildrenChannels":"SSELCN1994973287,","isAvailable":"true","trapNumber":2,"prices":[{"id":"4","priceType":"LP","priceNum":15,"priceDen":8,"priceDec":2.87,"isActive":"true","displayOrder":"1"}]},{"id":"1994973288","marketId":"619184436","name":"Made For You","outcomeMeaningMajorCode":"--","runnerNumber":"1","displayOrder":1,"outcomeStatusCode":"A","isActive":"true","isDisplayed":"true","siteChannels":"P,Q,C,G,W,I,M,","liveServChannels":"sSELCN1994973288,","liveServChildrenChannels":"SSELCN1994973288,","isAvailable":"true","trapNumber":1,"prices":[{"id":"5","priceType":"LP","priceNum":11,"priceDen":2,"priceDec":6.5,"isActive":"true","displayOrder":"1"}]}]}],"correctedDay":"racing.dayTuesday","correctedDayValue":"racing.today","eventIsLive":false,"liveEventOrder":1}]
      siteServerService.getEvent.and.returnValue(observableOf(resp as any));
      service['extendScoop6ToteEvents'](scoop6Events, {
        extendEvent: extendEvent,
        extendMarket: extendMarket,
        extendOutcome: extendOutcome
      }).subscribe(resp => {
        console.log(resp)
        expect(resp.length).toEqual(1);
      })
    });
  });
  describe('extendGenericToteEvents', () => {
    it('should call siteServerFactory.getEvent method', () => {
      const toteEvents = [{ "id": 25233594, "name": "2m 2 1/2f HCap Hurdle", "eventStatusCode": "A", "isActive": "true", "isDisplayed": "true", "displayOrder": 0, "siteChannels": "P,I,", "eventSortCode": "MTCH", "startTime": 1679405400000, "rawIsOffCode": "N", "classId": 321, "typeId": 2391, "sportId": "21", "raceNumber": "1", "liveServChannels": "sEVENT0025255809,", "liveServChildrenChannels": "SEVENT0025255809,", "categoryId": "21", "categoryCode": "HORSE_RACING", "categoryName": "Horse Racing", "categoryDisplayOrder": "-9971", "className": "Horse Racing - Tote Pools", "classDisplayOrder": 0, "classSortCode": "HR", "typeName": "Market Rasen (MN)", "typeDisplayOrder": 100, "isOpenEvent": "true", "isNext6HourEvent": "true", "isNext12HourEvent": "true", "isNext24HourEvent": "true", "isNext2DayEvent": "true", "isNext1WeekEvent": "true", "drilldownTagNames": "EVFLAG_HC,", "isAvailable": "true", "groupNumber": "1", "cashoutAvail": "N", "responseCreationTime": "2023-03-21T07:45:19.841Z",
       "externalKeys": { "OBEvLinkNonTote": 25233594 }, "localTime": "7:00", "originalName": "2m 2 1/2f HCap Hurdle", "isUS": false, "markets": [{ "id": "619722655", "eventId": "25255809", "templateMarketId": "206447", "templateMarketName": "Pool Betting", "marketMeaningMajorCode": "-", "marketMeaningMinorCode": "--", "name": "Pool Betting", "displayOrder": 0, "marketStatusCode": "A", "isActive": "true", "isDisplayed": "true", "siteChannels": "P,I,", "liveServChannels": "sEVMKT0619722655,", "liveServChildrenChannels": "SEVMKT0619722655,", "isPoolAvailable": "true", "isAvailable": "true", "maxAccumulators": "25", "minAccumulators": "1", "cashoutAvail": "N", "termsWithBet": "N", "outcomes": [{ "id": "1996708925", "marketId": "619722655", "name": "Unnamed Favourite", "outcomeMeaningMajorCode": "--", "outcomeMeaningMinorCode": "1", "runnerNumber": "0", "displayOrder": 0, "outcomeStatusCode": "A", "isActive": "true", "isDisplayed": "true", "siteChannels": "P,I,", "liveServChannels": "sSELCN1996708925,", "liveServChildrenChannels": "SSELCN1996708925,", "isAvailable": "true", "cashoutAvail": "N", "trapNumber": 0, "prices": [] }, { "id": "1996708991", "marketId": "619722655", "name": "Thankyourluckystar", "outcomeMeaningMajorCode": "--", "runnerNumber": "3", "displayOrder": 0, "outcomeStatusCode": "A", "isActive": "true", "isDisplayed": "true", "siteChannels": "P,I,", "liveServChannels": "sSELCN1996708991,", "liveServChildrenChannels": "SSELCN1996708991,", "isAvailable": "true", "cashoutAvail": "N", "trapNumber": 3, "prices": [{ "id": "3", "priceType": "pool", "poolId": "4319889", "poolType": "UWIN", "priceDec": 1.3, "isActive": "true", "displayOrder": "1" }, { "id": "4", "priceType": "pool", "poolId": "4319890", "poolType": "UEXA", "priceDec": 1.5, "isActive": "true", "displayOrder": "1" }] }, { "id": "1996708993", "marketId": "619722655", "name": "East End Girl", "outcomeMeaningMajorCode": "--", "runnerNumber": "4", "displayOrder": 0, "outcomeStatusCode": "A", "isActive": "true", "isDisplayed": "true", "siteChannels": "P,I,", "liveServChannels": "sSELCN1996708993,", "liveServChildrenChannels": "SSELCN1996708993,", "isAvailable": "true", "cashoutAvail": "N", "trapNumber": 4, "prices": [] }, { "id": "1996708988", "marketId": "619722655", "name": "Fiston De Becon", "outcomeMeaningMajorCode": "--", "runnerNumber": "2", "displayOrder": 0, "outcomeStatusCode": "A", "isActive": "true", "isDisplayed": "true", "siteChannels": "P,I,", "liveServChannels": "sSELCN1996708988,", "liveServChildrenChannels": "SSELCN1996708988,", "isAvailable": "true", "cashoutAvail": "N", "trapNumber": 2, "prices": [{ "id": "5", "priceType": "pool", "poolId": "4319889", "poolType": "UWIN", "priceDec": 1.9, "isActive": "true", "displayOrder": "1" }, { "id": "6", "priceType": "pool", "poolId": "4319890", "poolType": "UEXA", "priceDec": 1.5, "isActive": "true", "displayOrder": "1" }] }, { "id": "1996708987", "marketId": "619722655", "name": "Surtitle", "outcomeMeaningMajorCode": "--", "runnerNumber": "1", "displayOrder": 0, "outcomeStatusCode": "A", "isActive": "true", "isDisplayed": "true", "siteChannels": "P,I,", "liveServChannels": "sSELCN1996708987,", "liveServChildrenChannels": "SSELCN1996708987,", "isAvailable": "true", "cashoutAvail": "N", "trapNumber": 1, "prices": [] }] }], "correctedDay": "racing.dayTuesday", "correctedDayValue": "racing.today", "eventIsLive": false, "liveEventOrder": 1 }] as any;
      const extendEvent = jasmine.createSpy();
      const extendMarket = jasmine.createSpy();
      const extendOutcome = jasmine.createSpy();
      const resp = [{"id":25233594,"name":"Market Rasen","eventStatusCode":"A","isActive":"true","isDisplayed":"true","displayOrder":985,"siteChannels":"P,Q,C,G,W,I,M,","eventSortCode":"MTCH",
      "externalKeys": { "OBEvLinkNonTote": 25233594 }, "startTime":1679415900000,"rawIsOffCode":"N","classId":223,"typeId":1950,"sportId":"21",
      "liveServChannels":"sEVENT0025233599,","liveServChildrenChannels":"SEVENT0025233599,","categoryId":"21","categoryCode":"HORSE_RACING",
      "categoryName":"Horse Racing","categoryDisplayOrder":"-9971","className":"Horse Racing - Live",
      "classDisplayOrder":-9999,"classSortCode":"HR","classFlagCodes":"UF,LI,","typeName":"Market Rasen",
      "typeDisplayOrder":-31370,"typeFlagCodes":"UK,QL,RVA,","isOpenEvent":"true","isNext12HourEvent":"true",
      "isNext24HourEvent":"true","isNext2DayEvent":"true","isNext1WeekEvent":"true",
      "isLiveNowOrFutureEvent":"true","drilldownTagNames":"EVFLAG_BL,EVFLAG_RVA,",
      "isAvailable":"true","mediaTypeCodes":"VST,","cashoutAvail":"Y","raceLength":"23.073",
      "raceLengthUnit":"FR","effectiveGpStartTime":"2023-03-19T10:00:00Z",
      "responseCreationTime":"2023-03-21T07:48:05.654Z","localTime":"16:25","originalName":"16:25 Market Rasen","isUS":false,"markets":[{"id":"619184436","eventId":"25233599","templateMarketId":"136933","templateMarketName":"Win or Each Way","marketMeaningMajorCode":"-","marketMeaningMinorCode":"--","name":"Win or Each Way","isLpAvailable":"true","isSpAvailable":"true","isGpAvailable":"true","isEachWayAvailable":"true","eachWayFactorNum":"1","eachWayFactorDen":"1","eachWayPlaces":"1","isMarketBetInRun":"true","displayOrder":0,"marketStatusCode":"A","isActive":"true","isDisplayed":"true","siteChannels":"P,Q,C,G,W,I,M,","liveServChannels":"sEVMKT0619184436,","liveServChildrenChannels":"SEVMKT0619184436,","priceTypeCodes":"LP,GP,SP,","ncastTypeCodes":"SF,CF,RF,","isAvailable":"true","maxAccumulators":"25","minAccumulators":"1","cashoutAvail":"Y","termsWithBet":"N","outcomes":[{"id":"1994973282","marketId":"619184436","name":"Ripper Roo","outcomeMeaningMajorCode":"--","runnerNumber":"5","displayOrder":5,"outcomeStatusCode":"A","isActive":"true","isDisplayed":"true","siteChannels":"P,Q,C,G,W,I,M,","liveServChannels":"sSELCN1994973282,","liveServChildrenChannels":"SSELCN1994973282,","isAvailable":"true","trapNumber":5,"prices":[{"id":"1","priceType":"LP","priceNum":5,"priceDen":1,"priceDec":6,"isActive":"true","displayOrder":"1"}]},{"id":"1994973283","marketId":"619184436","name":"Unnamed 2nd Favourite","outcomeMeaningMajorCode":"--","outcomeMeaningMinorCode":"2","displayOrder":7,"outcomeStatusCode":"A","isActive":"true","isDisplayed":"true","siteChannels":"P,Q,C,G,W,I,M,","liveServChannels":"sSELCN1994973283,","liveServChildrenChannels":"SSELCN1994973283,","isAvailable":"true","prices":[]},{"id":"1994973284","marketId":"619184436","name":"Unnamed Favourite","outcomeMeaningMajorCode":"--","outcomeMeaningMinorCode":"1","displayOrder":6,"outcomeStatusCode":"A","isActive":"true","isDisplayed":"true","siteChannels":"P,Q,C,G,W,I,M,","liveServChannels":"sSELCN1994973284,","liveServChildrenChannels":"SSELCN1994973284,","isAvailable":"true","prices":[]},{"id":"1994973285","marketId":"619184436","name":"Storm Dennis N/R","outcomeMeaningMajorCode":"--","runnerNumber":"4","isResulted":"true","displayOrder":4,"outcomeStatusCode":"S","isDisplayed":"true","siteChannels":"P,Q,C,G,W,I,M,","liveServChannels":"sSELCN1994973285,","liveServChildrenChannels":"SSELCN1994973285,","isFinished":"true","trapNumber":4,"prices":[{"id":"2","priceType":"LP","priceNum":15,"priceDen":8,"priceDec":2.87,"isActive":"true","displayOrder":"1"}]},{"id":"1994973286","marketId":"619184436","name":"Bold Soldier","outcomeMeaningMajorCode":"--","runnerNumber":"3","displayOrder":3,"outcomeStatusCode":"A","isActive":"true","isDisplayed":"true","siteChannels":"P,Q,C,G,W,I,M,","liveServChannels":"sSELCN1994973286,","liveServChildrenChannels":"SSELCN1994973286,","isAvailable":"true","trapNumber":3,"prices":[{"id":"3","priceType":"LP","priceNum":6,"priceDen":4,"priceDec":2.5,"isActive":"true","displayOrder":"1"}]},{"id":"1994973287","marketId":"619184436","name":"The Kniphand","outcomeMeaningMajorCode":"--","runnerNumber":"2","displayOrder":2,"outcomeStatusCode":"A","isActive":"true","isDisplayed":"true","siteChannels":"P,Q,C,G,W,I,M,","liveServChannels":"sSELCN1994973287,","liveServChildrenChannels":"SSELCN1994973287,","isAvailable":"true","trapNumber":2,"prices":[{"id":"4","priceType":"LP","priceNum":15,"priceDen":8,"priceDec":2.87,"isActive":"true","displayOrder":"1"}]},{"id":"1994973288","marketId":"619184436","name":"Made For You","outcomeMeaningMajorCode":"--","runnerNumber":"1","displayOrder":1,"outcomeStatusCode":"A","isActive":"true","isDisplayed":"true","siteChannels":"P,Q,C,G,W,I,M,","liveServChannels":"sSELCN1994973288,","liveServChildrenChannels":"SSELCN1994973288,","isAvailable":"true","trapNumber":1,"prices":[{"id":"5","priceType":"LP","priceNum":11,"priceDen":2,"priceDec":6.5,"isActive":"true","displayOrder":"1"}]}]}],"correctedDay":"racing.dayTuesday","correctedDayValue":"racing.today","eventIsLive":false,"liveEventOrder":1}]
      siteServerService.getEvent.and.returnValue(observableOf(resp as any));
      service['extendGenericToteEvents'](toteEvents, {
        extendEvent: extendEvent,
        extendMarket: extendMarket,
        extendOutcome: extendOutcome
      }).subscribe(resp => {
        console.log(resp)
        expect(resp.length).toEqual(1);
      })
    });
  });
});
