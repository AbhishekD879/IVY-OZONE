import { of as observableOf, of, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { BetReceiptService } from './bet-receipt.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { overaskPlaceBets, prePlayPlaceBets, inPlayPlaceBets, events } from '@betslip/services/betReceipt/bet-receipt.service.mock';


import { betReceiptsMock, receiptDataMock, receiptDataMock2, receiptDataMock3, receiptDataMock4, receiptDataMock5, betsRacingMock } from '@betslip/services/betReceipt/bet-receipt.service.mock';
import { betslipReceiptBannerData } from '@app/betslip/components/betslipContainer/mockData/betslip-receipt-banner-data.mock';

describe('BetReceiptService', () => {
  let component: FiltersService;
  let service: BetReceiptService;
  let storageService;
  let bppService;
  let siteServerService;
  let pubSubService;
  let fracToDecService;
  let filtersService;
  let deviceService;
  let betslipStorageService;
  let addToBetslipService;
  let coreToolsService;
  let gtmTrackingService;
  let mockServiceData;
  let betslipDataService;
  let userService;
  let localeService;
  let templateService;
  let timeService;
  let sportsConfigService;
  let awsService;
  let gtmService;
  let http;
  let nativeBridgeService;
  let betslipService;
  let vanillaApiService;
  let cmsService;
  let scorecastDataService;

  const mockUuid = '123';

  beforeEach(() => {
    storageService = jasmine.createSpyObj('storageService', ['get','remove']);
    bppService = jasmine.createSpyObj('bppService', ['send']);
    siteServerService = {
      getEventsByOutcomeIds: jasmine.createSpy('getEventsByOutcomeIds').and.returnValue(Promise.resolve([])),
      getEvent: jasmine.createSpy('getEvent').and.returnValue(observableOf({})),
      isValidFzSelection: jasmine.createSpy('isValidFzSelection').and.returnValue(true)
    };
    pubSubService = jasmine.createSpyObj('pubSubService', ['publish']);
    fracToDecService = jasmine.createSpyObj('fracToDecService', ['getDecimal', 'decToFrac']);
    filtersService = {
      clearEventName: jasmine.createSpy('clearEventName').and.returnValue('clearName'),
      makeHandicapValue: jasmine.createSpy('makeHandicapValue'),
      setCurrency : jasmine.createSpy('setCurrency').and.returnValue('£235.00')
    };
    deviceService = { isMobile: false };
    betslipStorageService = jasmine.createSpyObj('betslipStorageService', ['restore']);
    addToBetslipService = jasmine.createSpyObj('addToBetslipService', ['addToBetSlip', 'reuseSelections']);
    coreToolsService = jasmine.createSpyObj('coreToolsService', ['uuid', 'deepClone']);

    pubSubService.API = pubSubApi;
    mockServiceData = JSON.parse(JSON.stringify(betReceiptsMock));
    fracToDecService.getDecimal.and.callFake((priceNum, priceDen) => (1 + (priceNum / priceDen)).toFixed(2));
    coreToolsService.uuid.and.returnValue(mockUuid);
    coreToolsService.deepClone.and.callFake(d => JSON.parse(JSON.stringify(d)));
    gtmTrackingService = {
      getBetOrigin: jasmine.createSpy().and.returnValue({
        location: 'testLocation',
        module: 'testModule',
        betType: ''
      }),
      restoreGtmTracking: jasmine.createSpy()
    };
    betslipDataService = {
      placedBets: {
        bets: [
          {
            id: 10,
            claimedOffers: [{ status: 'qualified', offerCategory: 'test' }]
          },
          {
            id: 12
          },
          {
            id: 14,
            claimedOffers: [{ status: 'qualified', offerCategory: 'Acca Insurance' }]
          }
        ]
      },
      readBets: {}
    };
    userService = {
      oddsFormat: 'frac',
      currencySymbol: '$'
    };

    localeService = {
      getString: jasmine.createSpy('getString')
    };

    templateService = {
      genEachWayPlaces: jasmine.createSpy('genEachWayPlaces').and.returnValue('1-2-3-4')
    };

    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern').and.returnValue('12:35')
    };

    sportsConfigService = {
      getSport: jasmine.createSpy('getSport').and.returnValue(observableOf({
        sportConfig: {
          config: {
            request: {
              categoryId: '16'
            }
          }
        }
      }))
    };

    awsService = {
      addAction: jasmine.createSpy('addAction')
    };

    gtmService = {
      getSBTrackingData: jasmine.createSpy('getSBTrackingData').and.returnValue([{GTMObject: {betData:{dimension94:1}}, outcomeId:  ['381480']}]),
      removeSBTrackingItem: jasmine.createSpy('removeSBTrackingItem'),
      push: jasmine.createSpy('push')
    };

    http = {
      post: jasmine.createSpy().and.returnValue(observableOf({ body: {} }))
    };

    nativeBridgeService = {
      betPlaceSuccessful: jasmine.createSpy('betPlaceSuccessful')
    };

    betslipService = {
      placeBetResponse: of({"bet": [{id: 1, stake: {freebetOfferCategory: 'Bet Pack'}}]} as any),
      betKeyboardData: [
        "All_single_quickStake-11,22",
        "singlestake-11",
        "singlestake-55",
        "singlestake-381480"
      ]
    }

    vanillaApiService = {
      get: jasmine.createSpy('vanillaApiService.get').and.returnValue(observableOf(betslipReceiptBannerData)),
      post: jasmine.createSpy('vanillaApiService.post').and.returnValue(observableOf([]))
    };

    cmsService = {
      systemConfiguration: { LuckyBonus: { BetSlipPopUpHeader: 'betslip header', BetSlipPopUpMessage: 'popup messge',
              BetReceiptPopUpHeader: 'bet receipt header', BetReceiptPopUpMessage: 'bet receipt popup message' } }
    };

    scorecastDataService = {
      setScorecastData: (data)=> { return data},
      getScorecastData: ()=> { 
        return {
          name: 'name',
          eventLocation: 'scorecast',
          teamname: 'teamname',
          playerName: 'playerName',
          result: '24',
          dimension64: '64'
        }
      },
    };
    spyOn(console, 'warn');

    service = new BetReceiptService(
      storageService,
      bppService,
      siteServerService,
      pubSubService,
      fracToDecService,
      filtersService,
      deviceService,
      betslipStorageService,
      addToBetslipService,
      coreToolsService,
      gtmTrackingService,
      betslipDataService,
      userService,
      localeService,
      templateService,
      timeService,
      sportsConfigService,
      awsService,
      gtmService,
      http,
      nativeBridgeService,
      betslipService,
      vanillaApiService,
      cmsService,
      scorecastDataService
    );
  });

  it('should return valid object with eventsInReceipt after getActiveSportsEvents call', () => {
    const receiptEventsMock = Object.assign({}, mockServiceData.receiptEventsMock);

    const actualEvents = service.getActiveSportsEvents(receiptEventsMock);

    expect(actualEvents.length).toEqual(mockServiceData.eventsInReceipt.length);
    actualEvents.forEach(el => expect(mockServiceData.eventsInReceipt).toContain(jasmine.objectContaining(el)));
  });

  it('getBetReceiptSiteCoreBanners', () => {
    service.getBetReceiptSiteCoreBanners().subscribe((bsReceiptBannerData) => {
      expect(bsReceiptBannerData).toEqual(betslipReceiptBannerData)
    });
  })

  describe('getBetReceipts method', () => {
    beforeEach(() => {
      const receiptData = Object.assign({}, mockServiceData.receiptData);
      const events = Object.assign({}, mockServiceData.events);

      bppService.send.and.returnValue(observableOf(receiptData));
      siteServerService.getEvent.and.returnValue(Promise.resolve(events));
    });

    it('should call getBetDetail as it is overask scenario', fakeAsync(() => {
      // service.betslipDataService.placedBets.bets = overaskPlaceBets;
      betslipDataService.placedBets.bets = overaskPlaceBets;
      spyOn<any>(service, 'mergeAndModifyResponseData').and.returnValue(observableOf());
      const filters = {
        includeUndisplayed: true,
        outcomesIds: ['449905491', '449905612', '449905491', '449905612']
      };
      service.ids = mockServiceData.ids;
      service.getBetReceipts().subscribe(() => {
        expect(bppService.send).toHaveBeenCalledWith('getBetDetail', {
          betId: mockServiceData.ids,
          returnPartialCashoutDetails: 'Y'
        });
      });
      expect(service['mergeAndModifyResponseData']).toHaveBeenCalled();
      tick();
    }));

    it('should call getBetDetail as it is overask scenario but with empty IDs', fakeAsync(() => {
      // service.betslipDataService.placedBets.bets = overaskPlaceBets;
      betslipDataService.placedBets.bets = overaskPlaceBets;
      spyOn<any>(service, 'mergeAndModifyResponseData').and.returnValue(observableOf());
      service.ids = null;
      service.getBetReceipts().subscribe(() => {
        expect(bppService.send).not.toHaveBeenCalledWith('getBetDetail', {
          betId: mockServiceData.ids,
          returnPartialCashoutDetails: 'Y'
        });
      });
      tick();
    }));

    it('should call mergeAndModifyResponseData, in pre-play scenario', fakeAsync(() => {
      // service.betslipDataService.placedBets.bets = prePlayPlaceBets;
      betslipDataService.placedBets.bets = prePlayPlaceBets;
      spyOn<any>(service, 'mergeAndModifyResponseData').and.returnValue(observableOf());
      service.getBetReceipts().subscribe(() => { });
      expect(service['mergeAndModifyResponseData']).toHaveBeenCalled();
      tick();
    }));

    it('should call mergeAndModifyResponseData, in In-play scenario', fakeAsync(() => {
      prePlayPlaceBets[0].isConfirmed = 'N';
      // service.betslipDataService.placedBets.bets = prePlayPlaceBets;
      // service.betslipDataService.readBets.bets = inPlayPlaceBets;
      betslipDataService.placedBets.bets = prePlayPlaceBets;
      betslipDataService.readBets.bets = inPlayPlaceBets;
      spyOn<any>(service, 'mergeAndModifyResponseData').and.returnValue(observableOf());
      service.getBetReceipts().subscribe(() => { });
      expect(service['mergeAndModifyResponseData']).toHaveBeenCalled();

      service.getBetReceipts().subscribe(() => { });
      expect(service['mergeAndModifyResponseData']).toHaveBeenCalled();
      tick();
    }));
  });

  describe('mergeAndModifyResponseData', () => {
    it('should call mergeEventsWithReceipts and others', fakeAsync(() => {
      const bets =  prePlayPlaceBets;
      const filters = {
        includeUndisplayed: true,
        outcomesIds: ['449905491']
      };
      spyOn<any>(service, 'mergeEventsWithReceipts');
      spyOn<any>(service, 'markFootballReceipts');
      spyOn<any>(service, 'markBoostedReceipts');
      spyOn<any>(service, 'extendWithAccaInsuranceData');
      spyOn<any>(service, 'markForeCastTricastReceipts');
      spyOn<any>(service, 'updateVirtualEventNames');
      spyOn<any>(service, 'markBogReceipts');
      spyOn<any>(service, 'setFreebetOfferCategory');
      spyOn<any>(service, 'checkForHorseRacingReceipts');
      spyOn<any>(service, 'divideOnSinglesAndMultiples');
      
      siteServerService.getEventsByOutcomeIds.and.returnValue(Promise.resolve([events]));
      service['mergeAndModifyResponseData'](bets).subscribe(() => {
        expect(siteServerService.getEventsByOutcomeIds).toHaveBeenCalledWith(filters, false);
      })
      tick();
    }));

    it('should call mergeEventsWithReceipts and with multiple leg.parts', fakeAsync(() => {
      const leg = [
      {
        part: [{
          outcome: '449905491',
          priceNum: '1',
          priceDen: '2',
          handicap: '',
          eventId: '6702230',
          event:{categoryName: 'test'}
        }]
      },
      {
        part: [{
          outcome: '449905492',
          priceNum: '1',
          priceDen: '2',
          handicap: '',
          eventId: '6702230',
          event:{categoryName: 'test'}
        }]
      }];
      const copiedPrePlayPlaceBets = [...prePlayPlaceBets];
      copiedPrePlayPlaceBets[0].leg = leg;
      const bets = copiedPrePlayPlaceBets;
      const filters = {
        includeUndisplayed: true,
        outcomesIds: ['449905491', '449905492']
      };
      spyOn<any>(service, 'mergeEventsWithReceipts');
      spyOn<any>(service, 'markFootballReceipts');
      spyOn<any>(service, 'markBoostedReceipts');
      spyOn<any>(service, 'extendWithAccaInsuranceData');
      spyOn<any>(service, 'markForeCastTricastReceipts');
      spyOn<any>(service, 'updateVirtualEventNames');
      spyOn<any>(service, 'markBogReceipts');
      spyOn<any>(service, 'setFreebetOfferCategory');
      spyOn<any>(service, 'checkForHorseRacingReceipts');
      spyOn<any>(service, 'divideOnSinglesAndMultiples');
      
      siteServerService.getEventsByOutcomeIds.and.returnValue(Promise.resolve([events]));
      service['mergeAndModifyResponseData'](bets).subscribe(() => {
        expect(siteServerService.getEventsByOutcomeIds).toHaveBeenCalledWith(filters, false);
      })
      tick();
    }));

    it('should call mergeEventsWithReceipts and getEvent is Failed', fakeAsync(() => {
      const bets =  prePlayPlaceBets;
      const filters = {
        includeUndisplayed: true,
        outcomesIds: ['449905491']
      };
      siteServerService.getEventsByOutcomeIds.and.returnValue(throwError({ url: 'http://someurl.com' }));
      service['mergeAndModifyResponseData'](bets).subscribe(() => {
      }, (error) => {
        expect(error.url).toEqual('http://someurl.com');
        expect(awsService.addAction).toHaveBeenCalled();
      });
      tick();
    }));
  });

  describe('getGtmObject method', () => {
    it('', () => {
      const data = mockServiceData.receiptEventsMock.singles[1];
      data.betId = '001',
      data.receipt = 'O/11';
      mockServiceData.receiptEventsMock.singles.push(mockServiceData.receiptEventsMock.singles[1]);
      service.getGtmObject(mockServiceData.receiptEventsMock, 5)
    });
    it('data', () => {
      const data = mockServiceData.receiptEventsMock.singles[1];
      data.betId = '001',
      data.receipt = 'O/11';
      mockServiceData.receiptEventsMock.singles.push(mockServiceData.receiptEventsMock.singles[1]);
      service.getGtmObject(mockServiceData.receiptEventsMock, 5)
    });
    
    it('virtual', () => {
      const retVal = service['getBetGtmObject']({bet: {leg: [{part: [{event: {categoryId: '39'}}]}]},
      isMultiple: 'true',
      multText: 'multText',
      outcomeIds: ['11','22'],
      betOrigin: {},odds: 'odds', isSameCategory: true, isSameType: true, isSameMarket: true })
      expect(retVal.dimension180).toBe('scorecast;teamname;playerName;24')
    });

    it('getGtmObject reuse', () => {
      service.isLuckyBonusAvailable = true
      const retVal = service['getBetGtmObject']({bet: {leg: [{part: [{event: {categoryId: '39'}}]}]},
      isMultiple: 'true',
      multText: 'multText',
       outcomeIds: ['11','22'],
      betOrigin: {betType: 'reuse'},odds: 'odds', isSameCategory: true, isSameType: true, isSameMarket: true})
      expect(retVal.dimension166).toBe('reuse')
    })
  });

  describe('reuse', () => {
    it('reuse (outcomes availalbe)', fakeAsync(() => {
      const outcomesIds = ['1'];
      service['getOutcomeIds'] = () => outcomesIds;
      service['sortByOutcomeIds'] = jasmine.createSpy().and.returnValue(() => null);
      siteServerService.getEventsByOutcomeIds.and.returnValue(Promise.resolve(true));
      addToBetslipService.reuseSelections.and.returnValue(observableOf(null));

      expect(service.reuse()).toEqual(jasmine.any(Promise));

      expect(siteServerService.getEventsByOutcomeIds).toHaveBeenCalledWith(
        { outcomesIds }
      );
      tick();
      expect(service['sortByOutcomeIds']).toHaveBeenCalledWith(outcomesIds);
      expect(addToBetslipService.reuseSelections).toHaveBeenCalledTimes(1);
      expect(gtmTrackingService.restoreGtmTracking).toHaveBeenCalledWith(outcomesIds);
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubApi.HOME_BETSLIP);
      expect(pubSubService.publish).toHaveBeenCalledWith('REUSE_OUTCOME');
      expect(service.message).toEqual({ type: undefined, msg: undefined });
    }));

    it('reuse (no outcomes)', () => {
      service['getOutcomeIds'] = () => [];
      expect(service.reuse()).toEqual(jasmine.any(Promise));
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubApi.HOME_BETSLIP);
      expect(pubSubService.publish).toHaveBeenCalledWith('REUSE_OUTCOME');
      expect(service.message).toEqual({ type: undefined, msg: undefined });
    });

    it('reuse (warn)', () => {
      const outcomesIdsList = ['1'];

      siteServerService.getEventsByOutcomeIds.and.returnValue(Promise.reject('error'));

      service.reuse(<any>outcomesIdsList).then(() => {
      }, () => {
        expect(console.warn).toHaveBeenCalledWith('Error while getEventsByOutcomeIds (BetReceiptService.getEventsByOutcomeIds)', 'error');
      });
    });

  });

  describe('buildGtmObject', () => {
    let bet;

    beforeEach(() => {
      bet = {
        betTypeName: 'Bet Type Name',
        eventMarket: 'Event Market',
        receipt: '0000/12345678',
        stake: {amount: '15'},
        potentialPayout: '30',
        odds: {
          dec: '1.20'
        },
        numLegs: '0',
        numLines: '0',
        tokenValue: '15',
        leg: [{
          part: [{
            event: {
              id: 111,
              name: 'EventName',
              categoryId: '555',
              typeId: '666',
              isStarted: true
            },
            eventMarketDesc: 'Test Market'
          }]
        }]
      };
      spyOn<any>(service, 'getOutcomeIds').and.returnValue(['55']);
    });

    it('should get bet origin for multiple', () => {
      service['buildGtmObject']([bet], true);
      expect(gtmTrackingService.getBetOrigin).toHaveBeenCalled();
    });

    it('should get bet origin for single', () => {
      service['buildGtmObject']([bet], false);
      expect(gtmTrackingService.getBetOrigin).toHaveBeenCalledWith('55');
    });

    it('should build GTM object for started event with number odds and price and freebet', () => {
      const result = service['buildGtmObject']([bet], false);

      expect(result).toEqual([{
        name: 'name',
        id: bet.receipt,
        price: 15,
        category: '555',
        variant: '666',
        brand: 'Match Betting',
        dimension60: '111',
        dimension61: '55',
        dimension62: 1,
        dimension63: 0,
        dimension64: '64',
        dimension65: 'edp',
        dimension66: 0,
        dimension67: 1.2,
        dimension86: 0,
        metric1: 15,
        quantity: 1,
        dimension166: 'normal',
        dimension180: 'scorecast;teamname;playerName;24',
        dimension181: 'keyboard predefine stake'
      }]);
    });

    it('should build GTM object for not started event with SP odds and without price and freebet', () => {
      bet.stake = null;
      bet.odds.dec = 'SP';
      bet.tokenValue = null;
      bet.leg[0].part[0].event.isStarted = false;

      const result = service['buildGtmObject']([bet], false);

      expect(result).toEqual([{
        name: 'name',
        id: bet.receipt,
        price: 0,
        category: '555',
        variant: '666',
        brand: 'Match Betting',
        dimension60: '111',
        dimension61: '55',
        dimension62: 0,
        dimension63: 0,
        dimension64: '64',
        dimension65: 'edp',
        dimension66: 0,
        dimension67: 'SP',
        dimension86: 0,
        metric1: 0,
        quantity: 1,
        dimension166: 'normal',
        dimension180: 'scorecast;teamname;playerName;24',
        dimension181: 'keyboard predefine stake'
      }]);
    });

    it('should build GTM object for multiple bets', () => {
      const result = service['buildGtmObject']([bet], true);
      expect(result).toEqual([{
        name: 'name',
        id: bet.receipt,
        price: 15,
        dimension60: 'multiple',
        dimension61: '55',
        dimension62: 1,
        dimension63: 0,
        dimension64: '64',
        dimension65: 'edp',
        dimension66: 0,
        dimension67: 2,
        dimension86: 0,
        metric1: 15,
        category: '555',
        variant: '666',
        brand: 'Match Betting',
        quantity: 1,
        dimension166: 'normal',
        dimension180: 'scorecast;teamname;playerName;24',
        dimension181: 'keyboard predefine stake'
      }]);
    });

    it('multiple bet and !isSameCategory !isSameType !isSameMarket', () => {
      spyOn<any>(service, 'compareAndSetBetOrigin').and.returnValue({
        location: 'testLocation',
        module: 'testModule',
        betType: ''
      });
      bet.leg.push({
        part: [{
          event: {
            id: 111,
            name: 'EventName',
            categoryId: '521',
            typeId: '616',
            isStarted: true
          },
          eventMarketDesc: 'Test Markets'
        }]
      })
      service['buildGtmObject']([bet], true);
      expect(service['compareAndSetBetOrigin']).toHaveBeenCalled();
    });

    it('should build GTM object for multiple bets for SP odds', () => {
      let result;

      bet.potentialPayout = 'NOT_AVAILABLE';
      result = service['buildGtmObject']([bet], true);
      expect(result[0].dimension67).toEqual('SP');

      delete bet.potentialPayout;
      result = service['buildGtmObject']([bet], true);
      expect(result[0].dimension67).toEqual('SP');
    });
  });

  describe('compareAndSetBetOrigin', () => {

    it('bettype reuse multi bet', () => {
      service['gtmTrackingService']['getBetOrigin'] = jasmine.createSpy().and.returnValue({
        location: 'testLocation',
        module: 'testModule',
        betType: 'reuse'
      });
      service['compareAndSetBetOrigin'](['55', '56'], 'multiple');
      expect(gtmTrackingService.getBetOrigin).toHaveBeenCalled();
    });

    it('bettype null multi bet', () => {
      service['gtmTrackingService']['getBetOrigin'] = jasmine.createSpy().and.returnValue({
        location: 'testLocation',
        module: 'testModule',
        betType: ''
      });
      const result = service['compareAndSetBetOrigin'](['55', '56'], 'multiple');
      expect(result.location).toBe('testLocation');
      expect(result.module).toBe('testModule');
      expect(gtmTrackingService.getBetOrigin).toHaveBeenCalled();
    });

    it('bettype null multi bet different location and module', () => {
      service['gtmTrackingService']['getBetOrigin'] = jasmine.createSpy().and.returnValues({
        location: 'testLocation',
        module: 'testModule',
        betType: ''
      }, {
        location: 'testLocations',
        module: 'testModules',
        betType: ''
      });
      spyOn<any>(service, 'removeDuplicates').and.returnValue('testLocation,testLocations');
      const result = service['compareAndSetBetOrigin'](['55', '56'], 'multiple');
      expect(result.location).toBe('testLocation,testLocations');
      expect(result.module).toBe('multiple');
      expect(service['removeDuplicates']).toHaveBeenCalled();
      expect(gtmTrackingService.getBetOrigin).toHaveBeenCalled();
    });

    it('bettype null and single bet', () => {
      service['gtmTrackingService']['getBetOrigin'] = jasmine.createSpy().and.returnValue({
        location: 'testLocation',
        module: 'testModule',
        betType: ''
      });
      service['compareAndSetBetOrigin'](['55'], 'multiple');
      expect(gtmTrackingService.getBetOrigin).toHaveBeenCalled();
    });

    it('bettype reuse and single bet', () => {
      service['gtmTrackingService']['getBetOrigin'] = jasmine.createSpy().and.returnValue({
        location: 'testLocation',
        module: 'testModule',
        betType: 'reuse'
      });
      service['compareAndSetBetOrigin'](['55'], 'multiple');
      expect(gtmTrackingService.getBetOrigin).toHaveBeenCalled();
    });

  });

  describe('removeDuplicates', () => {
    it('remove duplicate strings', () => {
      const str =['abc', 'abc' ]
      const res = service['removeDuplicates'](str);
      expect(res).toBe('abc');
    });
  })

  describe('buildGtmObject and call getBetGTMObject', () => {
    let bet;
    
    beforeEach(() => {
      bet = {
        betTypeName: 'Bet Type Name',
        eventMarket: 'Event Market',
        receipt: '0000/12345678',
        stake: {amount: '15'},
        potentialPayout: '30',
        odds: {
          dec: '1.20'
        },
        numLegs: '0',
        numLines: '0',
        tokenValue: '15',
        leg: [{
          part: [{
            event: {
              id: 111,
              name: 'EventName',
              categoryId: '555',
              typeId: '666',
              isStarted: true
            },
            eventMarketDesc: 'Test Market'
          }]
        }]
      };
      spyOn<any>(service, 'getOutcomeIds').and.returnValue([381480]);
    });

    it('should get bet origin and assign dimension90,94', () => {
      service['buildGtmObject']([bet], true);
      expect(gtmService.removeSBTrackingItem).toHaveBeenCalled();
      expect(gtmTrackingService.getBetOrigin).toHaveBeenCalled();
    });
  });

  it('should extendWithAccaInsuranceData', () => {
    const receiptBets = [
      { betId: '10' },
      { betId: '12' },
      { betId: '13' },
      { betId: '14' }
    ];
    service['extendWithAccaInsuranceData'](receiptBets as any);
    expect(receiptBets[0].hasOwnProperty('claimedOffers')).toEqual(false);
    expect(receiptBets[1].hasOwnProperty('claimedOffers')).toEqual(false);
    expect(receiptBets[2].hasOwnProperty('claimedOffers')).toEqual(false);
    expect(receiptBets[3].hasOwnProperty('claimedOffers')).toEqual(true);
  });

  it('should get freeBetStake', () => {
    service['receipts'] = <any>[{ tokenValue: '2' }];
    expect(service.freeBetStake).toEqual('2.00');
  });

  it('should get totalStake', () => {
    service['receipts'] = <any>[{
      provider: 'betLottery',
      potentialPayout: '100',
      lines: {number: 1},
      leg: [
        {
          lotteryLeg: {
            picks: "15|24|37",
            subscription: {
              "number": 1,
            }
          },
        }
      ],
      stake: {
        stakePerLine: "0.10",
        amount: "0.10",
      },
      numLines:1
    }
    ];
    expect(service.totalStake).toEqual('0.10');
  });

  it('should get totalEstimatedReturns', () => {
    service['receipts'] = <any>[{ stakePerLine: '2', numLines: '2' }];
    expect(service.totalEstimatedReturns).toEqual('N/A');
  });
  describe('awsLogs', () => {
    it('should not call addAction', () => {
      const config = {
        sportConfig: {
          config: {
            request: {
              categoryId: '16'
            }
          }
        }
      };
      service['awsLogs'](config as any);
      expect(awsService.addAction).not.toHaveBeenCalled();
    });
    it('should call addAction without categoryId', () => {
      const config = {
        sportConfig: {
          config: {
            request: {
            }
          }
        }
      };
      service['awsLogs'](config as any);
      expect(awsService.addAction).toHaveBeenCalled();
    });
    it('should call addAction with empty config', () => {
      const config = {};
      service['awsLogs'](config as any);
      expect(awsService.addAction).toHaveBeenCalled();
    });
  });
  describe('done', () => {
    it('should trigger publish if desktop', () => {
      deviceService.isMobile = false;
      service.done();

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.HOME_BETSLIP);
    });

    it('should clear message', () => {
      service.message.msg = 'Error';

      service.done();

      expect(service.message).toEqual({ type: undefined, msg: undefined });
    });

    it('should trigger done (mobile)', () => {
      deviceService.isMobile = true;
      service.done();
      expect(pubSubService.publish).toHaveBeenCalledWith('show-slide-out-betslip', false);
    });

    it('should trigger done (outcomesIds)', fakeAsync(() => {
      storageService.get.and.returnValue(['1', '2']);
      siteServerService.getEventsByOutcomeIds.and.returnValue(Promise.resolve([]));

      service.done();
      expect(siteServerService.getEventsByOutcomeIds).toHaveBeenCalledWith(jasmine.objectContaining({
        outcomesIds: ['1', '2']
      }));
    }));
  });

  it('should getActiveFootballEvents', () => {
    const receiptsEntity = {
      singles: [
        {
          isFootball: true,
          leg: [{ part: [{ event: {} }] }]
        },
        {
          isFootball: false
        }
      ],
      multiples: [
        {
          leg: [
            { part: [{ event: {}, isFootball: true }] },
            { part: [{ isFootball: false }] }
          ]
        }
      ]
    };
    expect(service.getActiveFootballEvents(<any>receiptsEntity).length).toEqual(2);
  });

  it('should parseBetsFromReceipt (no data)', () => {
    const receipt = {};
    expect(service['parseBetsFromReceipt'](<any>receipt)).toEqual([]);
  });

  it('should getTotalReturns', () => {
    const betReceipts = <any>[{
      provider: 'betLottery',
      potentialPayout: '100',
      leg: [
        {
          lotteryLeg: {
            picks: "15|24|37",
            subscription: {
              "number": 1,
            }
          },
        }
      ],
      stake: {
        stakePerLine: "0.10",
        amount: "0.10",
      },
      numLines:1
    }
    ];
    expect(service['getTotalReturns'](<any>betReceipts)).toEqual('100.00');
  });

  describe('markFootballReceipts', () => {
    it('should markFootballReceipts (SGL)', () => {
      const receiptsEntity = [{ betType: 'SGL', isFootball: false, leg: [{ part: [{ event: {} }] }] }];
      service['markFootballReceipts'](<any>receiptsEntity);
      expect(receiptsEntity[0].isFootball).toEqual(false);
    });

    it('should markFootballReceipts (SGL) w/o configuration', () => {
      const receiptsEntity = [{ betType: 'SGL', isFootball: false, leg: [{ part: [{ event: {} }] }] }];
      service['footballConfig'] = undefined;
      service['markFootballReceipts'](<any>receiptsEntity);
      expect(receiptsEntity[0].isFootball).toEqual(false);
    });
    it('should markFootballReceipts (SGL) w/o configuration without categoryId', () => {
      const receiptsEntity = [{ betType: 'SGL', isFootball: false, leg: [{ part: [{ event: {} }] }] }];
      service['footballConfig'] = { config: { request: { categoryId: '' } } };
      service['markFootballReceipts'](<any>receiptsEntity);
      expect(receiptsEntity[0].isFootball).toEqual(false);
    });
    it('should markFootballReceipts', () => {
      const receiptsEntity = [{ betType: 'DBL', leg: [{ part: [{ event: {}, isFootball: false }] }] }];
      service['markFootballReceipts'](<any>receiptsEntity);
      expect(receiptsEntity[0].leg[0].part[0].isFootball).toEqual(false);
    });
    it('should markFootballReceipts (DBL) w/o configuration', () => {
      const receiptsEntity = [{ betType: 'DBL', isFootball: false, leg: [{ part: [{ event: {} }] }] }];
      service['footballConfig'] = undefined;
      service['markFootballReceipts'](<any>receiptsEntity);
      expect(receiptsEntity[0].isFootball).toEqual(false);
    });
    it('should markFootballReceipts (DBL) w/o configuration && isSpecialEvent returns true', () => {
      const receiptsEntity = [{ betType: 'DBL', isFootball: false, leg: [{ part: [{ event: { categoryId: '16' } }] }] }];
      service['footballConfig'] = undefined;
      spyOn<any>(service, 'isSpecialEvent').and.returnValue(true);
      service['markFootballReceipts'](<any>receiptsEntity);
      expect(receiptsEntity[0].isFootball).toEqual(false);
    });
    it('should markFootballReceipts (DBL) w/o configuration && isSpecialEvent returns false', () => {
      const receiptsEntity = [{ betType: 'DBL', isFootball: false, leg: [{ part: [{ event: {} }] }] }];
      service['footballConfig'] = undefined;
      spyOn<any>(service, 'isSpecialEvent').and.returnValue(false);
      service['markFootballReceipts'](<any>receiptsEntity);
      expect(receiptsEntity[0].isFootball).toEqual(false);
    });
    it('should markFootballReceipts (DBL) w/o configuration && isSpecialEvent returns false', () => {
      const receiptsEntity = [{ betType: 'DBL', isFootball: false, leg: [{ part: [{ event: { categoryId: '16' } }] }] }];
      service['footballConfig'] = undefined;
      spyOn<any>(service, 'isSpecialEvent').and.returnValue(false);
      service['markFootballReceipts'](<any>receiptsEntity);
      expect(receiptsEntity[0].isFootball).toEqual(false);
    });
    it('should markFootballReceipts (DBL) with footballconfig && recieptEntity w/o categoryId && isSpecialEvent returns true', () => {
      const receiptsEntity = [{ betType: 'DBL', isFootball: false, leg: [{ part: [{ event: {} }] }] }];
      service['footballConfig'] = { config: { request: { categoryId: '16' } } };
      spyOn<any>(service, 'isSpecialEvent').and.returnValue(true);
      service['markFootballReceipts'](<any>receiptsEntity);
      expect(receiptsEntity[0].isFootball).toEqual(false);
    });
    it('should markFootballReceipts (DBL) with footballconfig && isSpecialEvent returns true', () => {
      const receiptsEntity = [{ betType: 'DBL', isFootball: false, leg: [{ part: [{ event: { categoryId: '16' }, isFootball: false }] }] }];
      service['footballConfig'] = { config: { request: { categoryId: '16' } } };
      spyOn<any>(service, 'isSpecialEvent').and.returnValue(true);
      service['markFootballReceipts'](<any>receiptsEntity);
      expect(receiptsEntity[0].leg[0].part[0].isFootball).toEqual(false);
    });
    it('should markFootballReceipts (DBL) with footballconfig and recieptsEntity categoryId  && isSpecialEvent returns true', () => {
      const receiptsEntity = [{ betType: 'DBL', isFootball: false, leg: [{ part: [{ event: { categoryId: '16' }, isFootball: false }] }] }];
      service['footballConfig'] = { config: { request: { categoryId: '16' } } };
      spyOn<any>(service, 'isSpecialEvent').and.returnValue(false);
      service['markFootballReceipts'](<any>receiptsEntity);
      expect(receiptsEntity[0].leg[0].part[0].isFootball).toEqual(true);
    });
    it('should markFootballReceipts (DBL) w/o configuration  && isSpecialEvent returns false', () => {
      const receiptsEntity = [{ betType: 'DBL', isFootball: false, leg: [{ part: [{ event: {}, isFootball: false }] }] }];
      service['footballConfig'] = { config: { request: { categoryId: '16' } } };
      spyOn<any>(service, 'isSpecialEvent').and.returnValue(false);
      service['markFootballReceipts'](<any>receiptsEntity);
      expect(receiptsEntity[0].leg[0].part[0].isFootball).toEqual(false);
    });
    it('should markFootballReceipts (DBL) w/o configuration having not categortId', () => {
      const receiptsEntity = [{ betType: 'DBL', isFootball: false, leg: [{ part: [{ event: {} }] }] }];
      service['footballConfig'] = { config: { request: { categoryId: '' } } };
      service['markFootballReceipts'](<any>receiptsEntity);
      expect(receiptsEntity[0].isFootball).toEqual(false);
    });
    it('should markFootballReceipts (SGL) with specialTypeIds', () => {
      const receiptsEntity = [{ betType: 'SGL', isFootball: false, leg: [{ part: [{ event: { categoryId: '16' } }] }] }];
      service['footballConfig'] = { config: { request: { categoryId: '16' } }, specialsTypeIds: [1234, 2345] };
      service['markFootballReceipts'](<any>receiptsEntity);
      expect(receiptsEntity[0].isFootball).toEqual(true);
    });
    it('should markFootballReceipts (SGL) with specialTypeIds and categoryId with event', () => {
      const receiptsEntity = [{ betType: 'SGL', isFootball: false, leg: [{ part: [{ event: { categoryId: '16', typeId: '1234' } }] }] }];
      service['footballConfig'] = { config: { request: { categoryId: '16' } }, specialsTypeIds: [1234, 2345] };
      service['markFootballReceipts'](<any>receiptsEntity);
      expect(receiptsEntity[0].isFootball).toEqual(false);
    });
    it('should markFootballReceipts (SGL) with specialTypeIds and categoryId with event', () => {
      const receiptsEntity = [{ betType: 'SGL', isFootball: false, leg: [{ part: [{ event: { categoryId: '16', typeId: '1284' } }] }] }];
      service['footballConfig'] = { config: { request: { categoryId: '16' } } };
      service['markFootballReceipts'](<any>receiptsEntity);
      expect(receiptsEntity[0].isFootball).toEqual(true);
    });
    it('should markFootballReceipts (SGL) with footballConfig undefined', () => {
      const receiptsEntity = [{ betType: 'SGL', isFootball: false, leg: [{ part: [{ event: { categoryId: '16' } }] }] }];
      service['footballConfig'] = undefined;
      service['markFootballReceipts'](<any>receiptsEntity);
      expect(receiptsEntity[0].isFootball).toEqual(true);
    });
    it('should markFootballReceipts (SGL) with footballConfig has footballId', () => {
      const receiptsEntity = [{ betType: 'SGL', isFootball: false, leg: [{ part: [{ event: { categoryId: '16' } }] }] }];
      service['footballConfig'] = { config: { request: { categoryId: '16' } } };
      service['markFootballReceipts'](<any>receiptsEntity);
      expect(receiptsEntity[0].isFootball).toEqual(true);
    });
  });

  it('should markBoostedReceipts', () => {
    const receiptsEntity = [{
      oddsBoosted: false,
      betTermsChange: [{ reasonCode: 'ODDS_BOOST' }, { reasonCode: 'PRICE_BOOST' }]
    }];
    service['markBoostedReceipts'](<any>receiptsEntity);
    expect(receiptsEntity[0].oddsBoosted).toEqual(true);
  });

  it('should sortByOutcomeIds', () => {
    const outcomesIds = ['1', '2', '3', '4'];
    const data = [
      {
        markets: [{
          outcomes: [
            { id: '2' },
            { id: '1' },
            { id: '3' },
            { id: '4' },
            { id: '5' }]
        }]
      }
    ];
    expect(service['sortByOutcomeIds'](<any>outcomesIds)(data as any)[0].markets[0].outcomes[0].id).toEqual('1');
    expect(service['sortByOutcomeIds'](<any>outcomesIds)(data as any)[0].markets[0].outcomes[2].id).toEqual('3');
  });

  it('should setOutcomeNames', () => {
    const receiptsEntity = [{
      name: 'receipt',
      leg: [
        {
          part: [
            { handicap: [] },
            { handicap: [{}], description: 'test' }
          ]
        }
      ]
    }];
    filtersService.makeHandicapValue.and.returnValue(1);
    service['setOutcomeNames'](<any>receiptsEntity);
    expect(receiptsEntity[0].leg[0].part[1].description).toEqual('test1');
    expect(receiptsEntity[0].name).toEqual('receipt1');
  });

  it('should getOutcomesInBetSlip', () => {
    betslipStorageService.restore.and.returnValue([{ outcomesIds: ['1', '2'] }, { outcomesIds: ['3', '4'] }]);
    expect(service['getOutcomesInBetSlip']()).toEqual(['3', '4', '1', '2']);
  });

  it('should getOutcomeIds', () => {
    const outcome = '4';
    const source = [
      {
        leg: [
          {
            part: [
              { outcome: outcome },
              { outcome: outcome }
            ]
          }
        ]
      }
    ];
    expect(service['getOutcomeIds'](<any>source, true)).toEqual([outcome+'']);
  });

  describe('getOutcomeIds', () => {
    it('should getOutcomeIds (!LP)', () => {
      const part = {
        priceNum: ''
      };
      expect(service['getOdds'](<any>part)).toEqual(jasmine.objectContaining({
        frac: 'SP',
        dec: 'SP'
      }));
    });

    it('should getOutcomeIds (!part)', () => {
      expect(service['getOdds'](null)).toEqual(jasmine.objectContaining({
        frac: '',
        dec: ''
      }));
    });
  });

  describe('getCleanBet', () => {
    it('should getCleanBet', () => {
      const betsReceipts = [
        {
          potentialPayout: 0,
          leg: []
        }
      ];
      expect(service['getCleanBet'](<any>betsReceipts)[0].potentialPayout).toEqual('N/A');
    });
  
    it('should getCleanBet with 1 leg and part data', () => {
      const betsReceipts = [
        {
          potentialPayout: 0,
          leg: [{
            part: [{
              outcome: '449905491',
              priceNum: '1',
              priceDen: '2',
              handicap: '',
              eventId: '6702230',
              description: '|Way Of Life|',
              eventDesc: '|13:05 Lingfield| - Paying 3 Places instead of 2',
              eventMarketDesc: '|Win or Each Way|'
            }]
          }]
        }
      ];
      const cleanPartEventDataSpy = spyOn<any>(service, 'cleanPartEventData');
      spyOn<any>(service, 'getNameOfEvent');
      spyOn<any>(service, 'getEventDesc');
      spyOn<any>(service, 'getEventMarket');
      spyOn<any>(service, 'getOdds');
      service['getCleanBet'](<any>betsReceipts);
      expect(cleanPartEventDataSpy).toHaveBeenCalled();
    });
  
    it('should getCleanBet with 2 legs and part data', () => {
      const betsReceipts = [
        {
          potentialPayout: 0,
          leg: [{
            part: [{
              outcome: '449905491',
              priceNum: '1',
              priceDen: '2',
              handicap: '',
              eventId: '6702230',
              description: '|Way Of Life|',
              eventDesc: '|13:05 Lingfield| - Paying 3 Places instead of 2',
              eventMarketDesc: '|Win or Each Way|'
            }]
          },
          {
            part: [{
              outcome: '449905492',
              priceNum: '1',
              priceDen: '3',
              handicap: '',
              eventId: '6702231',
              description: '|Way Of water|',
              eventDesc: '|13:15 Lingfield| - Paying 5 Places instead of 2',
              eventMarketDesc: '|Win|'
            }]
          }]
        }
      ];
      const cleanPartEventDataSpy = spyOn<any>(service, 'cleanPartEventData');
      spyOn<any>(service, 'getOdds');
      spyOn<any>(service, 'getEventMarket');
      service['getCleanBet'](<any>betsReceipts);
      expect(cleanPartEventDataSpy).toHaveBeenCalled();
      expect(service['getEventMarket']).not.toHaveBeenCalled();
    });
  });

  describe('#getStakeMulti', () => {
    it('should call getStakeMulti method', () => {
      expect(service.getStakeMulti({
        stakePerLine: '2',
        numLines: '3',
        tokenValue: '3'
      } as any)).toEqual(3);
    });
  });

  describe('#hasStake', () => {
    it('should call hasStake method when token value more than 0 and stake less than token', () => {
      expect(service.hasStake({
        stake: '2',
        tokenValue: '3'
      } as any)).toEqual(false);
    });

    it('should call hasStake method when token value more than 0', () => {
      expect(service.hasStake({
        stake: '5',
        tokenValue: '3'
      } as any)).toEqual(true);
    });

    it('should call hasStake method when token value is 0', () => {
      expect(service.hasStake({
        stake: '2',
        tokenValue: '0'
      } as any)).toEqual(false);
    });
  });

  describe('#getStake', () => {
    it('should call getStake method', () => {
      expect(service.getStake({
        stake: '6',
        tokenValue: '3'
      } as any)).toEqual(3);
    });
  });

  describe('#getReceiptOdds', () => {
    it('should call getReceiptOdds method', () => {
      expect(service.getReceiptOdds({
        odds: {
          frac: '1/2'
        }
      } as any)).toEqual('1/2');
    });
  });

  describe('#setToggleSwitchId', () => {
    it('should call setToggleSwitchId method', () => {
      expect(service.setToggleSwitchId({
        betId: '22341241241241'
      } as any)).toEqual('toggle-switch-betslip-22341241241241');
    });
  });

  describe('#getFormattedPrice', () => {
    it('getFormattedPrice frac', () => {
      userService.oddsFormat = 'frac';
      fracToDecService.decToFrac.and.returnValue('15.61');
      const result = service.getFormattedPrice({
        leg: [
          {
            odds: {
              frac: '4/9'
            }
          }, {
            odds: {
              frac: '18/5'
            }
          }, {
            odds: {
              frac: '6/4'
            }
          }
        ]
      } as any);

      expect(fracToDecService.decToFrac).toHaveBeenCalledWith(16.61111111111111, true);
      expect(result).toEqual('15.61');
    });

    it('getFormattedPrice frac', () => {
      userService.oddsFormat = 'dec';
      const result = service.getFormattedPrice({
        leg: [
          {
            odds: {
              frac: '4/9'
            }
          }, {
            odds: {
              frac: '18/5'
            }
          }, {
            odds: {
              frac: '6/4'
            }
          }
        ]
      } as any);

      expect(fracToDecService.decToFrac).not.toHaveBeenCalled();
      expect(result).toEqual('16.61');
    });
  });

  describe('#hasStakeMulti', () => {
    it('should call hasStakeMulti method when token value is more than 0', () => {
      expect(service.hasStakeMulti({
        stakePerLine: '2',
        numLines: '3',
        tokenValue: '3'
      } as any)).toEqual(true);
    });

    it('should call hasStakeMulti method when token value is more than 0 and numLines less than token', () => {
      expect(service.hasStakeMulti({
        stakePerLine: '2',
        numLines: '1',
        tokenValue: '3'
      } as any)).toEqual(false);
    });

    it('should call hasStakeMulti method when token value is 0', () => {
      expect(service.hasStakeMulti({
        stakePerLine: '2',
        numLines: '3',
        tokenValue: '0'
      } as any)).toEqual(false);
    });
  });

  describe('#getStakeTotal', () => {
    it('should call getStakeTotal method', () => {
      expect(service.getStakeTotal({
        stakePerLine: '2',
        numLines: '3'
      } as any)).toEqual(6);
    });
  });

  describe('#getEWTerms', () => {
    it('should call getEWTerms method', () => {
      const legPart = {
        eachWayNum: '1',
        eachWayDen: '2'
      } as any;
      service.getEWTerms(legPart);

      expect(localeService.getString).toHaveBeenCalledWith('bs.oddsAPlaces', {
        num: '1',
        den: '2',
        arr: '1-2-3-4'
      });
      expect(templateService.genEachWayPlaces).toHaveBeenCalledWith(legPart, true);
    });
  });

  describe('#getLinesPerStake', () => {
    it('should call getLinesPerStake method', () => {
      const receipt = {
        numLines: '1',
        stakePerLine: '2'
      } as any;
      service.getLinesPerStake(receipt);

      expect(localeService.getString).toHaveBeenCalledWith('bs.linesPerStake', {
        lines: '1',
        currency: '$',
        stake: '2.00'
      });
    });
  });

  describe('#updateVirtualEventNames', () => {
    it('updateVirtualEventNames', () => {
      const receipts = [
        {
          leg: [
            {
              part: [
                {
                  eventDesc: 'test',
                  event: {
                    sportId: '10'
                  }
                }
              ]
            },
            {
              part: [
                {
                  eventDesc: 'test',
                  event: {
                    sportId: '39'
                  }
                }
              ]
            }
          ]
        }
      ];
      service['updateVirtualEventNames'](receipts as any);
      expect(receipts[0].leg[0].part[0].eventDesc).toEqual('test');
      expect(receipts[0].leg[1].part[0].eventDesc).toEqual('12:35 clearName');
    });
  });

  describe('divideOnSinglesAndMultiples', () => {

    beforeEach(() => {
      service['getCleanBet'] = jasmine.createSpy('getCleanBet').and.callFake((data) => data);
      service['setOutcomeNames'] = jasmine.createSpy('setOutcomeNames').and.callFake((data) => data);
      service['sendEgBetslipTransactions'] = jasmine.createSpy('sendEgBetslipTransactions');
      spyOn<any>(service, 'isBetCanceled').and.callThrough();
    });

    it('should divide single and multiples and active and non active', () => {
      const data = [
        { betId: 1, betType: 'SGL', status: 'A' },
        { betId: 2, betType: 'SGL', status: 'X' },
        { betId: 11, betType: 'DBL', status: 'A' },
        { betId: 12, betType: 'DBL', status: 'X' },
        { betId: 13, betType: 'DBL', status: 'A', asyncAcceptStatus: 'T' }
      ] as any;

      const result = service['divideOnSinglesAndMultiples'](data);

      expect(service['setOutcomeNames']).toHaveBeenCalledWith(data);
      expect(service['isBetCanceled']).toHaveBeenCalled();
      expect(service['receipts']).toEqual([data[0], data[2]]);
      expect(result).toEqual([{
        singles: [data[0], data[1]],
        multiples: [data[2], data[3], data[4]]
      }, {
        singles: [data[0]],
        multiples: [data[2]]
      }]);
    });
  });

  describe('getTotalReturns', () => {
    beforeEach(()=> {
      spyOn<any>(service, 'checkForStraightMultiples').and.returnValue(true);
    });
    it('should return potentialPayout as is', () => {
      const betReceipts = [{ potentialPayout: '100' }];
      expect(service['getTotalReturns'](betReceipts as any)).toEqual('100.00');
    });

    it('should return 0', () => {
      const betReceipts = [{ potentialPayout: '100' }];
      expect(service['getTotalReturns'](betReceipts as any)).toEqual('100.00');
    });

    it('should return potentialPayout - tokenValue', () => {
      const betReceipts = [{ potentialPayout: '100', tokenValue: '50' }];
      expect(service['getTotalReturns'](betReceipts as any)).toEqual('100.00');
    });

    it('should return N/A if no potentialPayout', () => {
      const betReceipts = [{ tokenValue: '50' }];
      expect(service['getTotalReturns'](betReceipts as any)).toEqual('N/A');
    });

    it('should return N/A if potentialPayout is N/A', () => {
      const betReceipts = [{ tokenValue: '50', potentialPayout: 'N/A' }];
      expect(service['getTotalReturns'](betReceipts as any)).toEqual('N/A');
    });

  describe('checkForStraightMultiples', () => {
    it('should return true if it is a single selection', () => {
      expect(service['checkForStraightMultiples']([{
        betType: 'SGL', betId: 1 ,
      }] as any)).toBe(true);
    });
    it('should return false for all singles', () => {
      expect(service['checkForStraightMultiples']([{
        betType: 'SGL', betId: 1 ,
      }, {
        betType: 'SGL', betId: 2,
      }] as any)
    ).toBe(true);
    });

    it('should return true when DBL/TBL/ACC bets has line number 1', () => {
      expect(service['checkForStraightMultiples']([{
        betType: 'DBL', numLines: 1
      }, {
        betType: 'SGL', numLines: 1,
      }] as any)
      ).toBe(true);

      expect(service['checkForStraightMultiples']([{
        betType: 'DBL', numLines: 2,
      }, {
        betType: 'TBL', numLines: 2,legType:"E"
      }] as any)
      ).toBe(true);

      expect(service['checkForStraightMultiples']([{
        betType: 'DBL', numLines: 6,
      }, {
        betType: 'TBL', numLines: 2,
      }, {
        betType: 'ACC4', numLines: 1,
      }] as any)
      ).toBe(true);
    });

    it('should have return false when it\'s not straight multiple', () => {
      expect(service['checkForStraightMultiples']([{
        betType: 'DBL', numLines: 2,
      }, {
        betType: 'SGL', numLines: 1,
      }, {
        betType: 'SGL', numLines: 1,
      }] as any)
      ).toBe(true);

      expect(service['checkForStraightMultiples']([{
        betType: 'DBL', numLines: 2,
      }, {
        betType: 'PAT', numLines: 1,
      }, {
        betType: 'l15', numLines: 1,
      }] as any)
      ).toBe(true);
    });

    it('should return true if it is a lottoBet', () => {
      expect(service['checkForStraightMultiples']([{
        provider: 'betLottery'
      }] as any)
    ).toBe(true);
    });
  });

 
    it('should return totalStake fo lotto', () => {
      const betReceipts = [{
        provider: 'OpenBetLottery',
        potentialPayout: '100',
        leg: [
          {
            lotteryLeg: {
              picks: "15|24|37",
              gameRef: {
                id: "17508"
              },       
              subscription: {
                number: 1,            
              }
            },
          
          }
        ],
        stake: {
          stakePerLine: "0.10",
          amount: "0.10",
          // currencyRef: {
          //   id: "GBP"
          // }
        }
      }
      ];
      service['getTotalStake'](betReceipts as any);
      const value = service['getTotalReturns'](betReceipts as any);
      expect(value).toEqual('100.00');
      
    });
   
    it('should return potentialPayout for lotto', () => {
      const betReceipts = [{
        provider: 'OpenBetLottery',
        potentialPayout: '100',
        leg: [
          {
            lotteryLeg: {
              picks: "15|24|37",
              gameRef: {
                id: "17508"
              },
              subscription: {
                number: 1,
              }
            },
          }
        ],
        lines :{number : "1"},
        stake: {
          stakePerLine: "0.10",
          amount: "0.10",  
        }
      }
      ];
      const value = service['getTotalReturns'](betReceipts as any);
      expect(value).toEqual('100.00');
    });

    it('should return totalStake/estReturns for isLotto false ', () => {
      const betReceipts = [{
        provider: 'test',
        potentialPayout: '100',
        leg: [
          {
            lotteryLeg: {
              picks: "15|24|37",
              subscription: {
                "number": 1,
              }
            },
          }
        ],
        stake: {
          stakePerLine: "0.10",
          amount: "0.10",
        }
      }
      ];
      service['getTotalStake'](betReceipts as any);
      const value = service['getTotalReturns'](betReceipts as any);
      expect(value).toEqual('100.00');
      
    });
  });

  describe('getTotalReturns', () => {
    it('should call getTotalReturns return NA', () => {
      spyOn<any>(service, 'checkForStraightMultiples').and.returnValue(false);
      const betReceipts = [{ potentialPayout: '' }];
      service.isbetSlipHaveEst = false;
      expect(service['getTotalReturns'](betReceipts as any)).toEqual('N/A');
    });
    it('should call getTotalReturns with returns', () => {
      spyOn<any>(service, 'checkForStraightMultiples').and.returnValue(true);
      const betReceipts = [{ potentialPayout: '' }];
      service.isbetSlipHaveEst = true;
      expect(service['getTotalReturns'](betReceipts as any)).toEqual('N/A');
    });
    });

  it('@clearMessage: should clear message', () => {
    service.message.msg = 'Error msg';

    service.clearMessage();
    expect(service.message).toEqual({ type: undefined, msg: undefined });
  });

  describe('Test isBogFromPriceType()', () => {
    beforeEach(() => {
      service['filtersService']['isGreyhoundsEvent'] = jasmine.createSpy().and.returnValue(false);
    });

    it('should call isBogFromPriceType() and check if priceType: "G" ', () => {
      const receipts: any = [
        {
          isFootball: true,
          leg: [{ part: [{ event: {}, priceType: 'G', eventCategoryId: '1' }] }]
        },
        {
          isFootball: true,
          leg: [{ part: [{ event: {}, priceType: 'SP,LP', eventCategoryId: '1' }] }]
        }];

      service['markBogReceipts'](receipts);

      expect(receipts[0].leg[0].part[0].isBog).toBe(true);
      expect(receipts[1].leg[0].part[0].isBog).toBe(false);
    });

    it('should call isBogFromPriceType() and check if priceType: "GP"', () => {
      const receipts: any = [
        {
          isFootball: true,
          leg: [{ part: [{ event: {}, priceType: 'SL,SP', eventCategoryId: '1' }] }]
        },
        {
          leg: [
            { part: [{ event: {}, isFootball: true, priceType: 'GP,F', eventCategoryId: '1' }] },
            { part: [{ isFootball: false }] }
          ]
        }];

      service['markBogReceipts'](receipts);

      expect(receipts[0].leg[0].part[0].isBog).toBeFalsy(false);
      expect(receipts[1].leg[0].part[0].isBog).toBe(true);
      expect(receipts[1].leg[1].part[0].isBog).toBeFalsy(false);
    });

    it('should call isBogFromPriceType() and check priceType', () => {
      const receipts: any = [
        {
          isFootball: true,
          leg: [{ part: [{ event: {}, priceType: 'SL,LP', eventCategoryId: '1' }] }]
        },
        {
          leg: [
            { part: [{ event: {}, isFootball: true, priceType: 'LP,S', eventCategoryId: '1' }] },
            { part: [{ isFootball: false }] }
          ]
        }];

      service['markBogReceipts'](receipts);

      expect(receipts[0].leg[0].part[0].isBog).toBeFalsy(false);
      expect(receipts[1].leg[0].part[0].isBog).toBeFalsy(false);
      expect(receipts[1].leg[1].part[0].isBog).toBeFalsy(false);
    });

    it('should call isBogFromPriceType(), check priceType and eventCategoryId', () => {
      const receipts: any = [
        {
          isFootball: true,
          leg: [{ part: [{ event: {}, priceType: 'G,GP', eventCategoryId: '19' }] }]
        },
        {
          leg: [
            { part: [{ event: {}, isFootball: true, priceType: 'G,GP', eventCategoryId: '19' }] },
            { part: [{ isFootball: false }] }
          ]
        }];
      service['filtersService']['isGreyhoundsEvent'] = jasmine.createSpy().and.returnValue(true);

      service['markBogReceipts'](receipts);

      expect(receipts[0].leg[0].part[0].isBog).toBeFalsy(false);
      expect(receipts[1].leg[0].part[0].isBog).toBeFalsy(false);
      expect(receipts[1].leg[1].part[0].isBog).toBeFalsy(false);
    });

    it('should return excluded DrillDownTagNames for unnamed favourites', () => {
      const result1 = service.getExcludedDrillDownTagNames('radom name');

      expect(result1).toEqual('');

      const result2 = service.getExcludedDrillDownTagNames('unnamed favourite');
      expect(result2).toEqual('MKTFLAG_EPR, EVFLAG_EPR');

      const result3 = service.getExcludedDrillDownTagNames('Unnamed 2nd FaVouRiTe');
      expect(result3).toEqual('MKTFLAG_EPR, EVFLAG_EPR');
    });
  });

  describe('cleanPartEventData', () => {
    it('should remove pipes from string data', () => {
      const leg = {
        part: [{
          outcome: '449905491',
          priceNum: '1',
          priceDen: '2',
          handicap: '',
          eventId: '6702230',
          description: '|Way Of Life|',
          eventDesc: '|13:05 Lingfield| - Paying 3 Places instead of 2',
          eventMarketDesc: '|Win or Each Way|'
        }]
      };
      service['cleanPartEventData'](leg as any);
      expect(leg.part[0].description).toBe('Way Of Life');
      expect(leg.part[0].eventDesc).toBe('13:05 Lingfield - Paying 3 Places instead of 2');
      expect(leg.part[0].eventMarketDesc).toBe('Win or Each Way');
    });
  });

  describe('checkMaxPayOut', () => {
    it('if max payout true', () => {
      spyOn<any>(service, 'sendGTMData');
      service['checkMaxPayOut'](receiptDataMock.bet);
      expect(service.maxPayOutFlag).toBe(true);
      expect(service.betReceipt).toBe(true);
    });
    it('if max payout false when no bet tags', () => {
      service['checkMaxPayOut'](receiptDataMock2.bet);
      expect(service.maxPayOutFlag).toBe(false);
    });
    it('if max payout false when no bet tag', () => {
      service['checkMaxPayOut'](receiptDataMock3.bet);
      expect(service.maxPayOutFlag).toBe(false);
    });
    it('if max payout false when no tag name', () => {
      service['checkMaxPayOut'](receiptDataMock4.bet);
      expect(service.maxPayOutFlag).toBe(false);
    });
  });

  describe('isLuckySignType',()=>{
    const luckydata=[{
      betTypeRef:{
        id:'L15'
      },
      availableBonuses :{
        availableBonus:[
          {multiplier:'2'}
        ]
      },
      leg:[{
        sportsLeg:{price:{priceTypeRef:{id:'1'}}}         
      }]
    }]
    it('luckyreceipts length',()=>{
      expect(service['isLuckySignType'](luckydata)).toBe(true);
    });
    it('luckyreceipt',()=>{
      const data = {
        betTypeRef:{
          id:'L15'
        },
        availableBonuses :{
          availableBonus:[
            {multiplier:'2'}
          ]
        },
        leg:[{
          sportsLeg:{price:{priceTypeRef:{id:'1'}}}         
        }]
      };
      expect(service['isLuckySignType'](data)).toBe(true);
    });
  });

  describe('isSP',()=>{
    const SPleg=[{
      betTypeRef:{
        id:'L15'
      },
      availableBonuses :{
        availableBonus:{
          multiplier:'2'
        }
      },
      leg:[{
        sportsLeg:{price:{priceTypeRef:{id:'1'}}}         
      }]
    }];
    const LPleg=[{
      betTypeRef:{
        id:'L15'
      },
      availableBonuses :{
        availableBonus:{
          multiplier:'2'
        }
      },
      leg:[{
        sportsLeg:{price:{priceTypeRef:{id:'SP'}}}         
      }]
    }];
    it('check SP selection',()=>{
      expect(service['isSP'](SPleg)).toBe(false);
    });
   
    it('check LP selection',()=>{
      expect(service['isSP'](LPleg)).toBe(true);
    });
  });

  describe('#isLuckyAvailable',()=>{
    it('#isLuckyAvailable with bets',()=>{
    const betsdata={bets:[{
      betTypeRef:{
        id:'L15'
      },
      availableBonuses :{
        availableBonus:[{
          num_win:'4'
        }]
      },
    }]}
    expect(service['isLuckyAvailable'](betsdata)).toEqual({response: betsdata.bets[0], type: betsdata.bets[0].availableBonuses.availableBonus});
  });
    it('#isLuckyAvailable without bets',()=>{
      const betsdata={bets:[{
        betTypeRef:{
          id:'L1'
        },
        betType: 'L31',
        availableBonuses :{
          availableBonus:[{
            num_win:'5'
          }]
        },
      }]}
      expect(service['isLuckyAvailable'](betsdata)).toEqual({response: betsdata.bets[0], type: betsdata.bets[0].availableBonuses.availableBonus});
  });
    it('#isLuckyAvailable with eventSource',()=>{
    const betsdata={eventSource: {
      betTypeRef:{
        id:'L63'
      },
      availableBonuses :{
        availableBonus:[{
          num_win:'6'
        }]
      },
    }};
    expect(service['isLuckyAvailable'](betsdata)).toEqual({response: betsdata.eventSource, type: betsdata.eventSource.availableBonuses.availableBonus});
  });
  });

  describe('#luckyAllWinnersBonus',()=>{
    it('#luckyAllWinnersBonus with bets', () => {
      spyOn(service, 'isLuckyAvailable').and.returnValue({ type: [{ multiplier: 2 }] });
      const estReturn = 235;
      service.currencySymbol = userService.currencySymbol;
      const betsdata = {
        bets: [{
          betTypeRef: {
            id: 'L15'
          },
          availableBonuses: {
            availableBonus: [{
              num_win: '4'
            }]
          },
        }]
      };
      service['luckyAllWinnersBonus'](betsdata, estReturn);
      expect(filtersService.setCurrency).toHaveBeenCalledWith(235, userService.currencySymbol);
    });
    it('#luckyAllWinnersBonus without bets', () => {
      spyOn(service, 'isLuckyAvailable').and.returnValue({ type: [{ multiplier: undefined }], response: {potentialPayout: undefined}});
      const estReturn = 235;
      service.currencySymbol = userService.currencySymbol;
      const betsdata = {  
          betTypeRef: {
            id: 'L15'
          },
          availableBonuses: {
            availableBonus: [{
              num_win: '4'
            }]
          },
      };
      const resp = service['luckyAllWinnersBonus'](betsdata, estReturn);
      expect(resp).toBeUndefined();
    });
  });


  // describe('#setCurrency', () => {
  //   it('setCurrency, val: "val"', () => {
  //     component.setCurrency('val');
  //     expect(filtersService.setCurrency).toHaveBeenCalledWith('val', '$');
  //   });
  // });

  it('sendGTMData', () => {
    const gtmData = {
      'eventAction': 'rendered',
      'eventCategory': 'maximum returns',
      'eventLabel': 'bet receipt'
    };
    service['sendGTMData']();
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', gtmData);
  });
  it('if bet receipt is null', () => {
    spyOn<any>(service, 'sendGTMData');
    service['checkMaxPayOut'](receiptDataMock5.bet);
    expect(service.betReceipt).toBe(false);
  });

    it('checkForHorseRacingReceipts', () => {
   
      service.checkForHorseRacingReceipts(betsRacingMock as any)
   
      expect(service.horseRacingReceiptCheck).toBe(true);
  });

  describe('setFreebetOfferCategory', ()=>{
    const receiptBets: any = [
      {
        betId: 1,
        stake:{freebetOfferCategory:"Bet Pack"},
      },
      {
        betId: 2,
        stake:{freebetOfferCategory:"Bet Pack"}
      }
    ];
    it('should set freebet Offer Category', ()=>{
      service['setFreebetOfferCategory'](receiptBets);
      expect(receiptBets[0].freebetOfferCategory).toEqual('Bet Pack');
    });

    it('should set freebet Offer Category when bets object is given', ()=>{
      betslipService = {placeBetResponse : of({"bets": [{id: 1, stake: {freebetOfferCategory: 'Bet Pack'}}]} as any)}
      
      service = new BetReceiptService(
        storageService,
        bppService,
        siteServerService,
        pubSubService,
        fracToDecService,
        filtersService,
        deviceService,
        betslipStorageService,
        addToBetslipService,
        coreToolsService,
        gtmTrackingService,
        betslipDataService,
        userService,
        localeService,
        templateService,
        timeService,
        sportsConfigService,
        awsService,
        gtmService,
        http,
        nativeBridgeService,
        betslipService,
        vanillaApiService,
        cmsService,
        scorecastDataService
      );
      service['setFreebetOfferCategory'](receiptBets);
      expect(receiptBets[0].freebetOfferCategory).toEqual('Bet Pack');
    });
  });

  it('should call isSP', () => {
    const selection = [{
      betTypeRef: {
        id: 'L15'
      },
      availableBonuses: {
        availableBonus: [
          { multiplier: 2 }
        ]
      },
      leg: [{
        sportsLeg: {
          price: {
            priceTypeRef: {
              id: 'SP'
            }
          }
        }
      }]
    }];
    let resp = service.isSP(selection);
    expect(resp).toEqual(true);
    const selection1 = {
      betTypeRef: {
        id: 'L15'
      },
      availableBonuses: {
        availableBonus: [
          { multiplier: 2 }
        ]
      },
      leg: [{
        sportsLeg: {
          price: {
            priceTypeRef: {
              id: 'SP'
            }
          }
        }
      }]
    };
    resp = service.isSP(selection1);
    expect(resp).toEqual(true);
    const selection2 = {
      betTypeRef: {
        id: 'L15'
      },
      availableBonuses: {
        availableBonus: [
          { multiplier: 2 }
        ]
      },
      legs: [{
        sportsLeg: {
          price: {
            priceTypeRef: {
              id: 'SP'
            }
          }
        }
      }]
    };
    resp = service.isSP(selection2);
    expect(resp).toEqual(true);
    const selection3 = {
      betTypeRef: {
        id: 'L15'
      },
      availableBonuses: {
        availableBonus: [
          { multiplier: 2 }
        ]
      }
    };
    resp = service.isSP(selection3);
    expect(resp).toEqual(false);
  });
  it('should call returnAllWinner', () => {
    let resp = service['returnAllWinner'](0);
    expect(resp).toEqual(0);
    resp = service['returnAllWinner']('12');
    expect(resp).toEqual('12');
  });
  describe('#isAllWinnerOnlyApplicable', () => {
    it('should call isAllWinnerOnlyApplicable with betType L15', () => {
      const luckydata = {
        betType: 'L15',
        availableBonuses: {
          availableBonus: [
            {multiplier: 2, num_win: '4'}
          ]
        }
      };
      const resp = service['isAllWinnerOnlyApplicable'](luckydata);
      expect(resp).toEqual(true);
    });
    it('should call isAllWinnerOnlyApplicable with betType L31', () => {
      const luckydata = {
        betType: 'L31',
        availableBonuses: {
          availableBonus: [
            {multiplier: 2, num_win: '5'}
          ]
        }
      };
      const resp = service['isAllWinnerOnlyApplicable'](luckydata);
      expect(resp).toEqual(true);
    });
    it('should call isAllWinnerOnlyApplicable with betType L63', () => {
      const luckydata = {
        betTypeRef: {
          id: 'L63'
        },
        availableBonuses: {
          availableBonus: [
            {multiplier: 2, num_win: '6'}
          ]
        }
      };
      const resp = service['isAllWinnerOnlyApplicable'](luckydata);
      expect(resp).toEqual(true);
    });
  });
});
