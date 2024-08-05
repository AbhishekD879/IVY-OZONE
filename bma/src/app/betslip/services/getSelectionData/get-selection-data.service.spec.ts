import { tick, fakeAsync } from '@angular/core/testing';
import { GetSelectionDataService } from './get-selection-data.service';
import { of } from 'rxjs';
import { BETSLIP_VALUES } from '@betslip/constants/bet-slip.constant';
import { IOutcomeDetailsResponse } from '@bpp/services/bppProviders/bpp-providers.model';

describe('GetSelectionDataService', () => {
  let service: GetSelectionDataService;
  let localeService;
  let siteServerService;
  let eventsData;
  let betslipStorageService;
  let filter;
  let time;
  let fracToDecService;

  beforeEach(() => {
    eventsData = [{
      liveServChannels: '',
      eventStatusCode: 'S',
      markets: [{
        isLpAvailable: true,
        isSpAvailable: true,
        liveServChannels: '',
        outcomes: [{
          liveServChannels: '',
          outcomeMeaningMinorCode: '3',
          prices: []
        }]
      }]
    }, {
      liveServChannels: '',
      markets: [{
        isLpAvailable: true,
        isSpAvailable: true,
        liveServChannels: '',
        marketStatusCode: 'S',
        outcomes: [{
          liveServChannels: '',
          outcomeMeaningMinorCode: '2',
          prices: []
        }]
      }]
    }, {
      liveServChannels: '',
      markets: [{
        liveServChannels: '',
        isEachWayAvailable: true,
        isLpAvailable: true,
        isSpAvailable: false,
        outcomes: [{
          outcomeStatusCode: 'S',
          liveServChannels: '',
          prices: []
        }]
      }]
    }, {
      isStarted: true,
      liveServChannels: '',
      markets: [{
        liveServChannels: '',
        priceTypeCodes: 'SP',
        outcomes: [{
          liveServChannels: '',
          prices: []
        }]
      }]
    }, {
      liveServChannels: '',
      markets: [{
        liveServChannels: '',
        priceTypeCodes: 'LP',
        outcomes: [{
          liveServChannels: '',
          prices: [{ priceNum: 1, priceDen: 2 }]
        }]
      }]
    }];

    localeService = {
      getString: jasmine.createSpy('getString')
    };
    siteServerService = {
      getEventsByOutcomeIds: jasmine.createSpy('getEventsByOutcomeIds').and.returnValue(Promise.resolve(eventsData)),
      outcomeForOutcomeData: []
    };
    betslipStorageService = {
      useEventToBetslipObservable: jasmine.createSpy('useEventToBetslipObservable').and.returnValue(of({})),
      eventToBetslipObservable: null
    };

    filter = {
      removeLineSymbol: jasmine.createSpy('removeLineSymbol').and.callFake(name => name),
      getTimeFromName: jasmine.createSpy('getTimeFromName').and.returnValue('21:00'),
      clearEventName: jasmine.createSpy('clearEventName').and.callFake(name => name),
      makeHandicapValue: jasmine.createSpy('makeHandicapValue').and.returnValue('(+1.0)'),
      date: jasmine.createSpy('date').and.returnValue('21:00')
    };
    time = {
      getLocalHourMin: jasmine.createSpy('getLocalHourMin').and.returnValue('13:45'),
      parseDateTime: jasmine.createSpy('parseDateTime').and.returnValue('21:00')
    };
    fracToDecService = {
      fracToDec: jasmine.createSpy('fracToDec').and.returnValue('2')
    };

    service = new GetSelectionDataService(
      localeService,
      siteServerService,
      betslipStorageService,
      filter,
      time,
      fracToDecService
    );
  });

  describe('getOutcomeData', () => {
    it('should return outcome data', fakeAsync(() => {
      service.getOutcomeData(['1']).subscribe();
      tick();
      expect(siteServerService.getEventsByOutcomeIds).toHaveBeenCalledWith({
        outcomesIds: [1], racingFormOutcome: true
      });
      expect(localeService.getString).toHaveBeenCalledTimes(4);
    }));

    it('should return outcomeForOutcomeData', fakeAsync(() => {
      const outcomeForOutcomeData = {
        "liveServChannels": "",
        "eventStatusCode": "S",
        "markets": [
            {
                "isLpAvailable": true,
                "isSpAvailable": true,
                "liveServChannels": "",
                "outcomes": [
                    {
                        "liveServChannels": "",
                        "outcomeMeaningMinorCode": "3",
                        "prices": []
                    }
                ]
            }
        ]
    }
      siteServerService.outcomeForOutcomeData= [1,2,3];
      service = new GetSelectionDataService(
        localeService,
        siteServerService,
        betslipStorageService,
        filter,
        time,
        fracToDecService
      );
      const myPrivateSpy = spyOn<any>(service, 'getSelectionRelatedData').and.callThrough();
      myPrivateSpy.call(service, outcomeForOutcomeData);
      expect(service.outcomeData.length).toEqual(3);
    }));

    it('should handle error', fakeAsync(() => {
      siteServerService.getEventsByOutcomeIds.and.returnValue(Promise.reject(null));
      service.getOutcomeData(['1']).subscribe(null, () => {});
      tick();
      expect(localeService.getString).not.toHaveBeenCalled();
    }));

    it('should use event observable', fakeAsync(() => {
      betslipStorageService.eventToBetslipObservable = of({});
      service.getOutcomeData(['1']).subscribe();
      tick();

      expect(betslipStorageService.useEventToBetslipObservable).toHaveBeenCalled();
    }));

    it('should not use event observable', fakeAsync(() => {
      service.getOutcomeData(['1']).subscribe();
      tick();

      expect(betslipStorageService.useEventToBetslipObservable).not.toHaveBeenCalled();
    }));
  });

  describe('eachwayCheckboxOptionByDetails', () => {
    it('should return null', () => {
      expect(service['eachwayCheckboxOptionByDetails']({eachWayPlaces: false} as any)).toEqual(null);
    });

    it('should return EW params', () => {
      const params = {
        eachWayPlaces: true,
        eachWayNum: 1,
        eachWayDen: 2,
      };
      expect(service['eachwayCheckboxOptionByDetails'](params as any)).toEqual({
        eachwayPriceNum: 1,
        eachwayPriceDen: 2
      });
    });
  });

  it('getErrorCodeByOutcomeDetail', () => {
    expect(service['getErrorCodeByOutcomeDetail']({eventStatusCode: 'S'} as any)).toEqual(BETSLIP_VALUES.ERRORS.SELECTION_SUSPENDED);
    expect(service['getErrorCodeByOutcomeDetail']({marketStatusCode: 'S'} as any)).toEqual(BETSLIP_VALUES.ERRORS.MARKET_SUSPENDED);
    expect(service['getErrorCodeByOutcomeDetail']({outcomeStatusCode: 'S'} as any)).toEqual(BETSLIP_VALUES.ERRORS.OUTCOME_SUSPENDED);
    expect(service['getErrorCodeByOutcomeDetail']({isStarted: true, isMarketBetInRun: false} as any))
      .toEqual(BETSLIP_VALUES.ERRORS.EVENT_STARTED);
    expect(service['getErrorCodeByOutcomeDetail']({isStarted: false, isMarketBetInRun: false} as any)).toEqual(null);
    expect(service['getErrorCodeByOutcomeDetail']({isStarted: true, isMarketBetInRun: true} as any)).toEqual(null);
    expect(service['getErrorCodeByOutcomeDetail']({} as any)).toEqual(null);
  });

  describe('createOutcomeData', () => {
    let expected, outcomeDetail, selection;

    beforeEach(() => {
      expected = {
        id: '115960500',
        name: 'Auto test Port Janice',
        marketId: '32307094',
        prices: [{ priceNum: 3, priceDen: 7, priceDec: '2', priceType: 'LP'}],
        liveServChannels: 'outcome.liveServChannels',
        outcomeStatusCode: 'A',
        marketStatusCode: 'A',
        errorMsg: undefined,
        outcomeMeaningMinorCode: 'H',
        details: {
          info: {
            sport: 'FOOTBALL',
            event: 'Auto test Port Janice v Auto test Lake Brett',
            time: '10:00',
            localTime: '21:00',
            market: 'Match Betting',
            sportId: 90,
            className: 'Football Auto Test',
            isStarted: false
          },
          isRacing: false,
          outcomeStatusCode: 'A',
          marketStatusCode: 'A',
          eventStatusCode: 'A',
          classId: '16291',
          categoryId: '16',
          typeId: '3756',
          eventId: '826180',
          marketId: '32307094',
          outcomeId: '115960500',
          handicap: '',
          market: 'Match Betting',
          markets: [
            {
              id: '32307094',
              name: 'Match Betting',
              drilldownTagNames: 'market.drilldownTagNames',
              cashoutAvail: false,
              rawHandicapValue: undefined
            }
          ],
          selectionName: 'Auto test Port Janice',
          prices: { priceNum: 3, priceDen: 7, priceDec: '2', priceType: 'LP'},
          pricesAvailable: true,
          isEachWayAvailable: false,
          eachWayPlaces:'',
          previousOfferedPlaces:'',
          eachwayCheckbox: null,
          isSPLP: false,
          isGpAvailable: false,
          drilldownTagNames: 'event.drilldownTagNames',
          cashoutAvail: false,
          eventliveServChannels: 'event.liveServChannels',
          marketliveServChannels: 'market.liveServChannels',
          outcomeliveServChannels: 'outcome.liveServChannels',
          isMarketBetInRun: true,
        }
      };
      outcomeDetail = {
        id: '115960500',
        priceNum: '3',
        priceDen: '7',
        startPriceNum: '',
        startPriceDen: '',
        fbResult: 'H',
        eventMarketSort: 'MR',
        handicap: '',
        eachWayNum: '',
        eachWayDen: '',
        eachWayPlaces: '',
        previousOfferedPlaces:'',
        name: 'Auto test Port Janice',
        marketId: '32307094',
        marketDesc: 'Match Betting',
        eventId: '826180',
        eventDesc: 'Auto test Port Janice v Auto test Lake Brett',
        typeId: '3756',
        typeDesc: 'Autotest Premier League',
        classId: '16291',
        className: 'Football Auto Test',
        categoryId: '16',
        category: 'FOOTBALL',
        marketDrilldownTagNames: 'tag1, tag2',
        status: 'A',
        birIndex: '',
        accMin: '1',
        accMax: '25'
      };
      selection = {
        price: {
          priceNum: 1,
          priceDen: 2,
          priceType: 'LP'
        },
        details: {
          eventDrilldownTagNames: 'event.drilldownTagNames',
          marketDrilldownTagNames: 'market.drilldownTagNames',
          isAvailable: false,
          cashoutAvail: false,
          marketCashoutAvail: false,
          isMarketBetInRun: true,
          eventliveServChannels: 'event.liveServChannels',
          marketliveServChannels: 'market.liveServChannels',
          outcomeliveServChannels: 'outcome.liveServChannels',
          outcomeMeaningMinorCode: 'H',
          isSPLP: false,
          isGpAvailable: false,
          isEachWayAvailable: false,
          marketPriceTypeCodes: '',
          info: {
            sportId: 90,
            time: '10:00',
            isStarted: false
          }
        }
      };
    });

    it('should create outcome details and update price', () => {
      const result = service.createOutcomeData(outcomeDetail, selection as any);

      expect(result).toEqual(expected);
      expect(filter.removeLineSymbol).toHaveBeenCalledTimes(5);
    });

    it('should create outcome details and not update price for selection with SP price type', () => {
      selection.price.priceType = 'SP';
      expected.prices = [{
        priceNum: 1,
        priceDen: 2,
        priceType: 'SP'
      }];
      expected.details.prices = {
        priceNum: 1,
        priceDen: 2,
        priceType: 'SP'
      };
      const result = service.createOutcomeData(outcomeDetail, selection as any);

      expect(result).toEqual(expected);
      expect(filter.removeLineSymbol).toHaveBeenCalledTimes(5);
    });


    it('should create suspended outcome', () => {
      outcomeDetail.eventStatusCode = 'S';
      outcomeDetail.marketStatusCode = 'S';
      outcomeDetail.outcomeStatusCode = 'S';
      expected.outcomeStatusCode = 'S';
      expected.marketStatusCode = 'S';
      expected.details.outcomeStatusCode = 'S';
      expected.details.marketStatusCode = 'S';
      expected.details.eventStatusCode = 'S';
      const result = service.createOutcomeData(outcomeDetail, selection as any);

      expect(result).toEqual(expected);
    });

    it('should create outcome with handicap', () => {
      outcomeDetail.handicap = '1.0';
      expected.name = `${expected.name} (+${outcomeDetail.handicap})`;
      expected.details.handicap = outcomeDetail.handicap;
      expected.prices[0].handicapValueDec = outcomeDetail.handicap;
      expected.prices[0].rawHandicapValue = outcomeDetail.handicap;
      expected.details.prices.handicapValueDec = outcomeDetail.handicap;
      expected.details.prices.rawHandicapValue = outcomeDetail.handicap;
      expected.details.markets[0].rawHandicapValue = outcomeDetail.handicap;
      const result = service.createOutcomeData(outcomeDetail, selection as any);

      expect(result).toEqual(expected);
    });

    it('should create outcome with handicap and format handicap value', () => {
      outcomeDetail.handicap = '1.0000';
      expected.name = `${expected.name} (+1.0)`;
      const result = service.createOutcomeData(outcomeDetail, selection as any);

      expect(result.details.handicap).toEqual('1.0');
      expect(result.name).toEqual(expected.name);
    });

    it('should create outcome with userLocalTime', () => {
      filter.getTimeFromName.and.returnValue('');
      expected.details.info.localTime = '13:45';
      const result = service.createOutcomeData(outcomeDetail, selection as any);

      expect(result).toEqual(expected);
    });

    it('should create outcome without name',  () => {
      delete outcomeDetail.name;
      expected.details.selectionName = undefined;
      expected.name = undefined;
      const result = service.createOutcomeData(outcomeDetail, selection as any);

      expect(result).toEqual(expected);
    });

    it('should parse selection time',  () => {
      selection.details.info.time = '26 May 2020 00:12:00 GMT';
      expected.details.info.time = 1590451920000;
      const result = service.createOutcomeData(outcomeDetail, selection as any);

      expect(result).toEqual(expected);
    });

    it('should create outcome data with outcome price type', function () {
      outcomeDetail.priceType = 'LP';
      outcomeDetail.isGpAvailable = false;
      const result = service.createOutcomeData(outcomeDetail, selection as any);

      expect(result).toEqual(expected);
    });

    it('should create outcome data with correct isGpAvailable', function () {
      outcomeDetail.priceType = 'LP';
      outcomeDetail.isGpAvailable = true;
      expected.details.isGpAvailable = true;
      const result = service.createOutcomeData(outcomeDetail, selection as any);

      expect(result).toEqual(expected);
    });
  });

  describe('@getCorrectDecRawHandicapValue', () => {
    it('should return handicap value with same sign as is', () => {
      const outcomeDetail = { handicap: '1.0', fbResult: 'H' } as IOutcomeDetailsResponse;
      const actualResult = service['getCorrectDecRawHandicapValue'](outcomeDetail);

      expect(actualResult).toEqual('1.0');
    });

    it('should return handicap value with opposite sign when handicap selection is away team', () => {
      const outcomeDetail = { handicap: '1.0', fbResult: 'A' } as IOutcomeDetailsResponse;
      const actualResult = service['getCorrectDecRawHandicapValue'](outcomeDetail);

      expect(actualResult).toEqual('-1.0');
    });
  });

  it('@formatHandicapValue - should convert handicap value to x.y format', () => {
    const actualResult = service['formatHandicapValue'](-2.0000);

    expect(actualResult).toEqual('-2.0');
  });

  describe('@restrictedRacecard', () => {
    const eventDetails = {
      id: "222618797",
      typeName: "Kempton",
      startTime: "2023-02-10T21:00:00Z",
      responseCreationTime: "2023-02-10T21:00:00Z",
      categoryId: "21",
      categoryName: "Horse Racing",
        market: {
          id: "222618797",
          maxAccumulators: "1",
          minAccumulators: "1",
          outcomeDetails: [{
            eventId: "222618797",
            categoryId: '21',
            accMax: "1",
            accMin: "1",
            marketId:"222618797",
            name: 'abc'
          }]
        }
     }
     const restricted:any = {
      restrictedRaces: ['Kempton - 21:00'],
      eventIdDetails: ["222618797"],
      horseNames: []
    }
    it('should return restricted object',()=>{
      const returnObject = service.restrictedRacecardAndSelections(eventDetails.market, eventDetails, eventDetails.market.outcomeDetails);
      expect(returnObject).toEqual(restricted)
    });
    it('should return responseCreationTime',()=>{
      eventDetails.startTime = null;
      const returnObject = service.restrictedRacecardAndSelections(eventDetails.market, eventDetails, eventDetails.market.outcomeDetails);
      expect(returnObject).toEqual(restricted)
    });
    it('should not return restricted object',()=>{
      const eventDetails = {
        id: "222618797",
        typeName: "Kempton",
        startTime: "2023-02-10T21:00:00Z",
        responseCreationTime: "2023-02-10T21:00:00Z",
        categoryId: "21",
        categoryName: "Horse Racing",
          market: {
            id: "222618797",
            maxAccumulators: "21",
            minAccumulators: "1",
            outcomeDetails: [{
              eventId: "222618797",
              categoryId: '21',
              accMax: "1",
              accMin: "1",
              marketId:"222618797",
              name: 'abc'
            }]
          }
       }
       const restricted:any = {
        restrictedRaces: [],
        eventIdDetails: [ "222618797"],
        horseNames: ['abc']
       } 
       const returnObject = service.restrictedRacecardAndSelections(eventDetails.market, eventDetails, eventDetails.market.outcomeDetails);
       expect(returnObject).toEqual(restricted);
    });

    it('should return restricted object with out time',()=>{
      filter.getTimeFromName = jasmine.createSpy('getTimeFromName').and.returnValue(null);
      const restrictedRace:any = {
        restrictedRaces: ['Kempton'],
        eventIdDetails: ["222618797"],
        horseNames: []
      }
      const returnObject = service.restrictedRacecardAndSelections(eventDetails.market, eventDetails, eventDetails.market.outcomeDetails);
      expect(returnObject).toEqual(restrictedRace)
    });

    it('should return restricted object with catergory id not HR',()=>{
      eventDetails.market.outcomeDetails[0]['categoryId'] = '19';
      eventDetails.market.outcomeDetails['categoryId'] = '19';
      const returnObject = service.restrictedRacecardAndSelections(eventDetails.market, eventDetails, eventDetails.market.outcomeDetails);
      expect(returnObject.eventIdDetails.length).toBe(0)
    });

    it('should return restricted object',()=>{
      eventDetails.market.outcomeDetails[0]['categoryId'] = '19';
      eventDetails.market.outcomeDetails['categoryId'] = '19';
      eventDetails.market.outcomeDetails.push({
        eventId: "222618796",
        categoryId: '21',
        accMax: "1",
        accMin: "1",
        marketId:"222618796",
        name: 'abc'
      });
      const returnObject = service.restrictedRacecardAndSelections(eventDetails.market, eventDetails, eventDetails.market.outcomeDetails);
      expect(returnObject.eventIdDetails.length).toBe(2)
    });


  });
});
