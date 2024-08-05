import { BetslipService } from '@betslip/services/betslip/betslip.service';
import { fakeAsync, tick } from '@angular/core/testing';
import { throwError, of, Subscriber } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';

import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { BETSLIP_VALUES } from '@betslip/constants/bet-slip.constant';

describe('BetslipService', () => {
  let service,
    bsDocService,
    betSelectionService,
    betSelectionsService,
    betStakeService,
    legFactoryService,
    freeBetService,
    getSelectionDataService,
    bppService,
    placeBetDocService,
    buildBetDocService,
    cmsServcie,
    birService,
    localeService,
    deviceService,
    overAskService,
    accaService,
    sessionService,
    pubsub,
    fracToDecService,
    dialogService,
    toteBetSlipService,
    user,
    betslipDataService,
    betslipStorageService,
    awsService,
    dynamicComponentLoader,
    clientUserAgentService,
    gtmTrackingService,
    commandService,
    timeSyncService,
    nativeBridgeService,
    windowRefService,
    ssRequestHelper,
    storageService,
    fbService,
    lottoBuildBetDocService,
    fanzoneStorageService,
    sessionStorageService;
    const betObject = {
      bet: [{
        "documentId": "1",
        "betTypeRef": {
          "id": "SGL"
        },
        "stake": {
          "amount": 1,
          "stakePerLine": 1,
          "freebet": 1,
          "currencyRef": {
            "id": "GBP"
          }
        },
        "lines": {
          "number": 1
        },
        "freebet": {
          "id": "41121365"
        },
        "legRef": [{
          "documentId": "1"
        }]
      }]
    };

  const betdata = {
    multiples: [
      {
        betTypeName: 'Double',
        betType: 'SGL',
        receipt: 'O/11',
        numLines: '1',
        stake: '5.00',
        numLegs: '1',
        odds: {
          frac: '5/23',
          dec: '3.2',
        },
        potentialPayout: '5.00',
        leg: [
          {
            part: [{ event: { id: 1, }, marketId: '123123' }],
            odds: {
              frac: '5/2',
              dec: '3.50',
            }
          }
        ]
      }
    ]
  };
  const HORSE_RACING_CATEGORY_ID = environment.HORSE_RACING_CATEGORY_ID;
  beforeEach(() => {
    bsDocService = {
      el: jasmine.createSpy('el')
    };
    betSelectionService = {
      construct: jasmine.createSpy('construct').and.returnValue({ id: 1 }),
      restoreSelections: jasmine.createSpy('restoreSelections')
    };
    betSelectionsService = {
      data: [],
      findById: jasmine.createSpy('findById').and.returnValue(false),
      count: jasmine.createSpy('count').and.returnValue(0),
      addSelection: jasmine.createSpy('addSelection'),
      removeSelection: jasmine.createSpy('removeSelection'),
      removeMultiSelection : jasmine.createSpy('removeMultiSelection'),
      construct: jasmine.createSpy('construct'),
      updateSelection: jasmine.createSpy('updateSelection')
    };
    betStakeService = {
      construct: jasmine.createSpy('construct').and.returnValue({
        amount: 1,
        currency: '$',
        lines: 1,
        max: '1',
        min: '1',
        perLine: '1'
      })
    };
    legFactoryService = {
      constructLegs: jasmine.createSpy('constructLegs')
    };
    freeBetService = {
      construct: jasmine.createSpy('construct'),
      parseOne: jasmine.createSpy('parseOne').and.returnValue({}),
    };
    getSelectionDataService = {
      getOutcomeData: jasmine.createSpy().and.returnValue(of(null))
    };
    bppService = {
      send: jasmine.createSpy('send').and.returnValue(of(null)),
      showErrorPopup: jasmine.createSpy('showErrorPopup')
    };
    placeBetDocService = {
      buildRequest: jasmine.createSpy('buildRequest')
    };
    buildBetDocService = {
      buildRequest: jasmine.createSpy('buildRequest'),
      setResponse: jasmine.createSpy('setResponse')
    };
    cmsServcie = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({
        Betslip: { maxBetNumber: 0 }
      }))
    };
    birService = {
      exectuteBIR: jasmine.createSpy('exectuteBIR')
    };
    localeService = {
      getString: jasmine.createSpy('getString')
       .withArgs('bs.betPacks').and.returnValue('BetPacks')
       .withArgs('bs.fanZone').and .returnValue('Fanzone')
       .withArgs('bs.freeBets').and.returnValue('FreeBets').withArgs('sb.allSports').and.returnValue('All Sports')
    };
    deviceService = {
      isOnline: jasmine.createSpy('isOnline').and.returnValue(true)
    };
    overAskService = {
      isOverask: jasmine.createSpy('isOverask'),
      execute: jasmine.createSpy('execute'),
      isBetPlaced: jasmine.createSpy('isBetPlaced').and.returnValue(true),
      setSuspended: jasmine.createSpy('setSuspended')
    };
    accaService = {
      getFreeBetOffer: jasmine.createSpy('getFreeBetOffer').and.returnValue(of(null))
    };
    sessionService = {
      whenProxySession: jasmine.createSpy('whenProxySession').and.returnValue(Promise.resolve())
    };
    pubsub = {
      API: pubSubApi,
      publish: jasmine.createSpy('publish'),
      publishSync: jasmine.createSpy('publishSync')
    };
    fracToDecService = {
      getDecimal: jasmine.createSpy('getDecimal'),
      decToFrac: jasmine.createSpy('decToFrac')
    };
    dialogService = {
      openDialog: jasmine.createSpy('openDialog')
    };
    toteBetSlipService = {
      isToteBetPresent: jasmine.createSpy('isToteBetPresent')
    };
    user = {
      currency: '$',
      status: true,
      set: jasmine.createSpy(),
      username: 'test'
    };
    betslipDataService = {
      placedBets: { bets: {} },
      betslipData: { params: {} },
      clearMultiplesStakes: jasmine.createSpy('clearMultiplesStakes'),
      checkPrices: jasmine.createSpy('checkPrices'),
      storeBets: jasmine.createSpy('storeBets'),
      setDefault: jasmine.createSpy('setDefault')
    };
    betslipStorageService = {
      restore: jasmine.createSpy('restore'),
      getOutcomesIds: jasmine.createSpy('getOutcomesIds'),
      filterSelections: jasmine.createSpy('filterSelections'),
      store: jasmine.createSpy('store'),
      setFreeBet: jasmine.createSpy('setFreeBet'),
      updateStorage: jasmine.createSpy('updateStorage'),
      storeSuspended: jasmine.createSpy('storeSuspended'),
      syncWithNative: jasmine.createSpy('syncWithNative'),
      betslipStorageService: jasmine.createSpy('betslipStorageService'),
      removeFanzoneSelections: jasmine.createSpy('removeFanzoneSelections'),
    };
    awsService = {
      addAction: jasmine.createSpy()
    };
    dynamicComponentLoader = {
      loadModule: jasmine.createSpy().and.returnValue(Promise.resolve({
        componentFactoryResolver: {
          resolveComponentFactory: () => ({})
        }
      }))
    };
    clientUserAgentService = {
      getId: jasmine.createSpy('getId')
    };
    gtmTrackingService = {
      collectPlacedBets: jasmine.createSpy()
    };
    commandService = {
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve({})),
      API: {
        ODDS_BOOST_SETTLE_TOKEN: 'ODDS_BOOST_SETTLE_TOKEN'
      }
    };
    timeSyncService = {
      ip: '192.168.3.1'
    };
    nativeBridgeService = {
      betSlipCloseAnimationDuration: 500,
    };
    fanzoneStorageService = {
      get: jasmine.createSpy('get').and.returnValue({teamId: '7yx5dqhhphyvfisohikodajhv,'})
    }
    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy('setTimeout'),
        location: {
          reload: jasmine.createSpy('reload')
        }
      }
    };
    ssRequestHelper = {
      getEventsByOutcomes: jasmine.createSpy('getEventsByOutcoes').and.returnValue('')
    };
    storageService = {
      get: jasmine.createSpy('storageService.get').and.returnValue(undefined),
      set: jasmine.createSpy('storageService.set')
    };
    fbService = {
      getBetLevelName: jasmine.createSpy('getBetLevelName'),
      isBetPack:jasmine.createSpy('isBetPack'),
      isFanzone:jasmine.createSpy('isFanzone')
    };

    lottoBuildBetDocService = {
      constructPlaceBetObj: jasmine.createSpy('constructPlaceBetObj')
    };

    sessionStorageService = {
      get: jasmine.createSpy('get'),
      remove: jasmine.createSpy('remove')
    };
    service = new BetslipService(bsDocService, betSelectionService, betSelectionsService, betStakeService,
      legFactoryService, freeBetService, getSelectionDataService, bppService,
      placeBetDocService, buildBetDocService, cmsServcie, birService, localeService, deviceService, overAskService,
      accaService, sessionService, pubsub, fracToDecService, dialogService, toteBetSlipService,
      user, betslipDataService, betslipStorageService, awsService, dynamicComponentLoader, clientUserAgentService,
      gtmTrackingService, commandService, timeSyncService, nativeBridgeService, windowRefService, ssRequestHelper,
      storageService,fbService,lottoBuildBetDocService,fanzoneStorageService,sessionStorageService);
  });

  it('init', () => {
    expect(service).toBeDefined();
  });

  it('get betData', () => {
    service['_betData'] = betdata;
    expect(service.betData).toEqual(betdata);
  });

  it('set betData', () => {
    service.betData = betdata as any;
    expect(service['betData']).toBe(betdata);
  });

  it('set getPlaceBetPending ',()=>{
    service.getPlaceBetPending =false 
  });

  it('set getPlaceBetPending ',()=>{
    service.getPlaceBetPending =true 
  });

  it('set selections ',()=>{
    service.betSelectionsService.data = [{}] 
  });

  it('should return BetSlip object', () => {
    const params = {
      bets: [
        {
          stake: {
            amount: 1
          },
          disabled: false
        }
      ],
      docId: 1,
      legs: [],
      errs: []
    };
    const actualResult = service['construct'](<any>params);

    expect(actualResult).toEqual(jasmine.objectContaining({
      docId: 1,
      stake: {},
      bets: [{ stake: { amount: 1 }, disabled: false }],
      legs: [],
      errs: [],
      doc: jasmine.any(Function)
    }));
  });

  it('sortOddsBoosts with oddsboosts', fakeAsync(() => {
    const date = [{ params: { oddsBoosts: [{}] } }] as any;
    user.status = false;

    service['sortOddsBoosts'](date).subscribe(res => {
      expect(res).toEqual(date);
      expect(commandService.executeAsync).not.toHaveBeenCalled();
    });

    tick();
  }));

  it('sortOddsBoosts without oddsboosts', fakeAsync(() => {
    const date = [{ params: { oddsBoosts: [] } }] as any;

    service['sortOddsBoosts'](date).subscribe(res => {
      expect(res).toEqual(date);
      expect(commandService.executeAsync).not.toHaveBeenCalled();
    });

    tick();
  }));

  it('sortOddsBoosts without oddsboosts', fakeAsync(() => {
    const date = [{ params: { oddsBoosts: null } }] as any;

    service['sortOddsBoosts'](date).subscribe(res => {
      expect(res).toEqual(date);
      expect(commandService.executeAsync).not.toHaveBeenCalled();
    });

    tick();
  }));

  it('remove fanzone selections on logout', fakeAsync(() => {
    const mockOutcomesData = [{"id": "240480151", "marketId": "52637000", "name": "Fulham", "teamExtIds": "7yx5dqhhphyvfisohikodajhv,"}];
    const response = {SSResponse: {children: mockOutcomesData}};
    ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
    service.mapOutComes = jasmine.createSpy('mapOutComes').and.returnValue(mockOutcomesData);
    betslipStorageService.getOutcomesIds = jasmine.createSpy('').and.returnValue(['240480151']);
    betslipStorageService.restore = jasmine.createSpy('').and.returnValue({});
    service.removeFzSelectionsOnLogout();
    tick();
    expect(betslipStorageService.removeFanzoneSelections).not.toHaveBeenCalled();
  }));

  it('remove fanzone selections on logout when restore has selections', fakeAsync(() => {
    const mockOutcomesData = [{"id": "240480151", "marketId": "52637000", "name": "Fulham", "teamExtIds": "7yx5dqhhphyvfisohikodajhv,", "isFanzoneMarket": true}];
    const response = {SSResponse: {children: mockOutcomesData}};
    ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
    service.mapOutComes = jasmine.createSpy('mapOutComes').and.returnValue(mockOutcomesData);
    betslipStorageService.getOutcomesIds = jasmine.createSpy('').and.returnValue(['240480151']);
    betslipStorageService.restore = jasmine.createSpy('').and.returnValue([{id:'12345'}]);
    sessionStorageService.get = jasmine.createSpy('RemoteBS').and.returnValue({outcomes: [{id: "240480151", name: "Home", outcomeMeaningMajorCode: "--", outcomeMeaningMinorCode: null}]});
    service.getBSFzMarket = jasmine.createSpy('getBSFzMarket').and.returnValue(true);
    user.status = false;
    service.removeFzSelectionsOnLogout();
    tick();
    expect(sessionStorageService.remove).toHaveBeenCalledWith('RemoteBS');
    expect(betslipStorageService.removeFanzoneSelections).toHaveBeenCalled();
  }));

  it('remove fanzone selections on logout when restore has selections in remote BS', fakeAsync(() => {
    const mockOutcomesData = [{"id": "240480151", "marketId": "52637000", "name": "Fulham", "teamExtIds": "7yx5dqhhphyvfisohikodajhv,", "isFanzoneMarket": true}];
    const response = {SSResponse: {children: mockOutcomesData}};
    ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
    service.mapOutComes = jasmine.createSpy('mapOutComes').and.returnValue(mockOutcomesData);
    betslipStorageService.getOutcomesIds = jasmine.createSpy('').and.returnValue(['240480151']);
    betslipStorageService.restore = jasmine.createSpy('').and.returnValue([{id:'12345'}]);
    sessionStorageService.get = jasmine.createSpy('RemoteBS').and.returnValue({details: {marketDrilldownTagNames: 'MKTFLAG_FZ'},outcomes: [{id: "240480152", name: "Home", outcomeMeaningMajorCode: "--", outcomeMeaningMinorCode: null}]});
    service.getBSFzMarket = jasmine.createSpy('getBSFzMarket').and.returnValue(true);
    user.status = true;
    service.removeFzSelectionsOnLogout();
    tick();
    expect(sessionStorageService.remove).toHaveBeenCalledWith('RemoteBS');
    expect(betslipStorageService.removeFanzoneSelections).toHaveBeenCalled();
  }));

  it('getBSFzMarket for fanzone market', (() => {
    const remoteBS = {details: {marketDrilldownTagNames: 'MKTFLAG_FZ'},outcomes: [{id: "240480152", name: "Home", outcomeMeaningMajorCode: "--", outcomeMeaningMinorCode: null}]};
    const result = service['getBSFzMarket'](remoteBS);
    expect(result).toBe(true);
  }));
  
  it('getBSFzMarket when market is not fanzone', (() => {
    const remoteBS = {details: {marketDrilldownTagNames: 'MKTFLAG_FLZ'},outcomes: [{id: "240480152", name: "Home", outcomeMeaningMajorCode: "--", outcomeMeaningMinorCode: null}]};
    const result = service['getBSFzMarket'](remoteBS);
    expect(result).toBe(false);
  }));

  it('remove betslip for quickbet', fakeAsync(() => {
    const mockOutcomesData = [{"id": "240480151", "marketId": "52637000", "name": "Fulham", "teamExtIds": "7yx5dqhhphyvfisohikodajhv,"}];
    const response = {SSResponse: {children: mockOutcomesData}};
    ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
    betslipStorageService.getOutcomesIds = jasmine.createSpy('').and.returnValue([]);
    betslipStorageService.restore = jasmine.createSpy('').and.returnValue({});
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue({teamId: '7yx5dqhhphyvfisohikodajhv'})
    deviceService.isMobile = true;
    sessionStorageService.get = jasmine.createSpy('RemoteBS').and.returnValue({outcomes: [{id: "240480151", name: "Home", outcomeMeaningMajorCode: "--", outcomeMeaningMinorCode: null}]});
    service.removeFzSelectionsOnLogout();
    tick();
  }));


  it('remove betslip for quickbet when outcomes is empty', fakeAsync(() => {
    const mockOutcomesData = [{"id": "240480151", "marketId": "52637000", "name": "Fulham", "teamExtIds": "7yx5dqhhphyvfisohikodajhv,"}];
    const response = {SSResponse: {children: mockOutcomesData}};
    ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
    betslipStorageService.getOutcomesIds = jasmine.createSpy('').and.returnValue(mockOutcomesData);
    betslipStorageService.restore = jasmine.createSpy('').and.returnValue({});
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue({teamId: '7yx5dqhhphyvfisohikodajhv'})
    deviceService.isMobile = true;
    user.status = true;
    service.mapOutComes = jasmine.createSpy('mapOutComes').and.returnValue(mockOutcomesData);
    sessionStorageService.get = jasmine.createSpy('RemoteBS').and.returnValue({selectionData: {outcomes: mockOutcomesData}});
    service.removeFzSelectionsOnLogout();
    tick();
  }));

  it('remove fanzone selections on logout when reuse selections', fakeAsync(() => {
    const mockOutcomesData = [{"id": "240480151", "marketId": "52637000", "name": "Fulham", "teamExtIds": "7yx5dqhhphyvfisohikodajhv,"}];
    const response = {SSResponse: {children: mockOutcomesData}};
    ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
    user.status = true;
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue({teamId: '7yx5dqhhphyvfisohikodajhv'})
    service.mapOutComes = jasmine.createSpy('mapOutComes').and.returnValue(mockOutcomesData);
    betslipStorageService.restore = jasmine.createSpy('').and.returnValue([{id:'12345'}]);
    betslipStorageService.getOutcomesIds = jasmine.createSpy('').and.returnValue(['240480151']);
    service.removeFzSelectionsOnLogout();
    tick();
    expect(betslipStorageService.removeFanzoneSelections).not.toHaveBeenCalled();
  }));

  it('remove fanzone selections on logout when reuse selections for no value', fakeAsync(() => {
    const mockOutcomesData = [{"id": "240480151", "marketId": "52637000", "name": "Fulham", "teamExtIds": "7yx5dqhhphyvfisohikodajhv,"}];
    const response = {SSResponse: {children: mockOutcomesData}};
    ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
    user.status = true;
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(undefined)
    service.mapOutComes = jasmine.createSpy('mapOutComes').and.returnValue(mockOutcomesData);
    betslipStorageService.restore = jasmine.createSpy('').and.returnValue([{id:'12345'}]);
    betslipStorageService.getOutcomesIds = jasmine.createSpy('').and.returnValue(['240480151']);
    service.removeFzSelectionsOnLogout();
    tick();
    expect(betslipStorageService.removeFanzoneSelections).not.toHaveBeenCalled();
  }));

  it('remove fanzone selections on logout when reuse selections', fakeAsync(() => {
    const mockOutcomesData = [{"id": "240480151", "marketId": "52637000", "name": "Fulham", "teamExtIds": "7yx5dqhhphyvfisohikodajhv,"}];
    const response = {SSResponse: {children: mockOutcomesData}};
    ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
    user.status = true;
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue({teamId: '7yx5dqhhphyvfisohikodajhv'})
    service.mapOutComes = jasmine.createSpy('mapOutComes').and.returnValue(mockOutcomesData);
    betslipStorageService.restore = jasmine.createSpy('').and.returnValue([{id:'12345'}]);
    betslipStorageService.getOutcomesIds = jasmine.createSpy('').and.returnValue(['240480151']);
    service.removeFzSelectionsOnLogout();
    tick();
    expect(betslipStorageService.removeFanzoneSelections).not.toHaveBeenCalled();
  }));

  it('dont remove fanzone selections as storage is null', fakeAsync(() => {
    const mockOutcomesData = [{"id": "240480151", "marketId": "52637000", "name": "Fulham", "teamExtIds": "7yx5dqhhphyvfisohikodajhv,"}];
    const response = {SSResponse: {children: mockOutcomesData}};
    ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
    user.status = true;
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(null);
    service.mapOutComes = jasmine.createSpy('mapOutComes').and.returnValue(mockOutcomesData);
    betslipStorageService.getOutcomesIds = jasmine.createSpy('').and.returnValue(['240480151']);
    betslipStorageService.restore = jasmine.createSpy('').and.returnValue([{id:'12345'}]);
    service.removeFzSelectionsOnLogout();
    tick();
    expect(betslipStorageService.removeFanzoneSelections).not.toHaveBeenCalled();
  }));

  it('dont remove fanzone selections as storage is undefined', fakeAsync(() => {
    const mockOutcomesData = [{"id": "240480151", "marketId": "52637000", "name": "Fulham", "teamExtIds": "7yx5dqhhphyvfisohikodajhv,"}];
    const response = {SSResponse: {children: mockOutcomesData}};
    ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
    user.status = true;
    fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(undefined);
    service.mapOutComes = jasmine.createSpy('mapOutComes').and.returnValue(mockOutcomesData);
    betslipStorageService.restore = jasmine.createSpy('').and.returnValue([{id:'12345'}]);
    betslipStorageService.getOutcomesIds = jasmine.createSpy('').and.returnValue(['240480151']);
    service.removeFzSelectionsOnLogout();
    tick();
    expect(betslipStorageService.removeFanzoneSelections).not.toHaveBeenCalled();
  }));

  it('mapOutcomes', fakeAsync(() => {
    const mockOutcomesData = [{ "id": "1318944369", isFanzoneMarket: false},{"id": "1318944369", isFanzoneMarket: false},{"id": "1318944369", isFanzoneMarket: false}]
    const response = {SSResponse: {"children": [{"event": { "id": "2746917", "children": [{"market": {"children": [{"outcome": {"id": "1318944369"}},{"outcome": {"id": "1318944369"}}, {"outcome": {"id": "1318944369"}}] }}]}}]}};
    ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
    const res = service.mapOutComes(response);
    tick();
    expect(res).toEqual(mockOutcomesData);
  }));

  it('mapOutcomes outcome data for fanzone market flag', fakeAsync(() => {
    const mockOutcomesData = [{ "id": "1318944369", isFanzoneMarket: true},{"id": "1318944369", isFanzoneMarket: true},{"id": "1318944369", isFanzoneMarket: true}]
    const response = {SSResponse: {"children": [{"event": { "id": "2746917", "children": [{"market": {"drilldownTagNames":"MKTFLAG_FZ", "children": [{"outcome": {"id": "1318944369"}},{"outcome": {"id": "1318944369"}}, {"outcome": {"id": "1318944369"}}] }}]}}]}};
    ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
    const res = service.mapOutComes(response);
    tick();
    expect(res).toEqual(mockOutcomesData);
  }));

  it('sortOddsBoosts check lottoData condition', fakeAsync(() => {
    const date = [{ params: { oddsBoosts: [], lottoData: {isLotto : false} } }] as any;

    service['sortOddsBoosts'](date).subscribe(res => {
      expect(res).toEqual(date);
      expect(commandService.executeAsync).not.toHaveBeenCalled();
    });

    tick();
  }));

  it('sortOddsBoosts without oddsboosts', fakeAsync(() => {
    const data = [
      { 
        params: { 
          lottoData: {isLotto: true} 
        } 
      }] as any;

    service['sortOddsBoosts'](data).subscribe(res => {
      expect(res).toEqual(data);
      expect(commandService.executeAsync).not.toHaveBeenCalled();
    });

    tick();
  }));

  it('sortOddsBoosts without oddsboosts', fakeAsync(() => {
    const data = [
      { 
        params: { 
        } 
      }] as any;

    service['sortOddsBoosts'](data).subscribe(res => {
      expect(res).toEqual(data);
      expect(commandService.executeAsync).not.toHaveBeenCalled();
    });

    tick();
  }));

  it('sortOddsBoosts session true', fakeAsync(() => {
    const date = [{ params: { oddsBoosts: [{}] } }] as any;

    service['sortOddsBoosts'](date).subscribe(() => {
      expect(commandService.executeAsync).toHaveBeenCalledWith(commandService.API.ODDS_BOOST_SETTLE_TOKEN, [date]);
    });
    tick();
  }));

  describe('placeBetsResult', () => {
    it('has errors', () => {
      service.placeBetsResult({
        betError: [{
          betRef: [{}]
        }]
      });

      expect(awsService.addAction).toHaveBeenCalledWith(
        'BetSlip=>placeBetRequest=>Success', jasmine.any(Object)
      );
      expect(storageService.set).toHaveBeenCalledWith('tooltipsSeen', { 'receiptViewsCounter-test': 1 });
      expect(gtmTrackingService.collectPlacedBets).toHaveBeenCalledTimes(1);
    });

    it('counter more than 1', () => {
      storageService.get = jasmine.createSpy().and.returnValue({ 'receiptViewsCounter-test': 2 });
      service.placeBetsResult({
        betError: [{
          betRef: [{}]
        }]
      });

      expect(awsService.addAction).toHaveBeenCalledWith(
        'BetSlip=>placeBetRequest=>Success', jasmine.any(Object)
      );
      expect(storageService.set).toHaveBeenCalledWith('tooltipsSeen', { 'receiptViewsCounter-test': 3 });
      expect(gtmTrackingService.collectPlacedBets).toHaveBeenCalledTimes(1);
    });

    it('OpenBetBir provider', () => {
      service.placeBetsResult({
        bet: [{
          lines: {}, provider: 'OpenBetBir'
        }]
      });
      expect(birService.exectuteBIR).toHaveBeenCalledTimes(1);
    });

    it('overask', () => {
      overAskService.isOverask.and.returnValue(true);
      service.placeBetsResult({});
      expect(overAskService.execute).toHaveBeenCalledTimes(1);
    });

    it('place bet ok', () => {
      service.placeBetsResult({});
      expect(birService.exectuteBIR).not.toHaveBeenCalled();
      expect(overAskService.execute).not.toHaveBeenCalled();
    });

    it('place bet ok isBPMPFreeBetTokenUsed is true', () => {
      service.isBPMPFreeBetTokenUsed = true;
      service.placeBetsResult({});
      expect(overAskService.isBPMPFreeBetTokenUsed).toBeTrue();
    });

    it('place bet ok isBPMPFreeBetTokenUsed is false', () => {
      service.isBPMPFreeBetTokenUsed = false;
      service.placeBetsResult({});
      expect(overAskService.isBPMPFreeBetTokenUsed).toBeFalse();
    });

    it('add lottoData to placeBetResponse', () => {
      const betResponse = [{
        lines: { number: '1' }, provider: 'BetLottery', id: '12345',
        leg: [{ documentId:'1', lotteryLeg: { gameRef: { id: 1234 }, subscription: { number: 1 } } }]
      }];
      const lottoData = [{ id: '12345', details: { lottoName: 'Daily Million', draws: [{}] } }];
      const expectedObj = { ...betResponse[0], ...lottoData[0] };
      service.isBPMPFreeBetTokenUsed = false;
      const data = service.placeBetsResult({ bet: betResponse }, lottoData, {leg:[{documentId:'1'}]});

      data.subscribe(res => {
        expect(res.bets[0]).toEqual(expectedObj);
      });
      expect(overAskService.isBPMPFreeBetTokenUsed).toBeFalse();
    });
  });

  describe('placeBetsRequest', () => {
    beforeEach(() => {
      placeBetDocService.buildRequest.and.returnValue(betObject);
    });

    it('checkBPMPFreeBetTokenIsUsed and isBPMPFreeBetTokenUsed to be true', fakeAsync(() => {
      storageService.get.and.returnValue(JSON.stringify([{
        freebetTokenId: "41121365",
        freebetOfferCategories: {
          freebetOfferCategory: "Bet Pack"
        }
      }]));
      service.placeBetsRequest().subscribe(null, () => { });
      tick();
      expect(service.isBPMPFreeBetTokenUsed).toBeTrue();
    }));

    it('error occured (device online)', fakeAsync(() => {
      bppService.send.and.returnValue(throwError({}));

      service.placeBetsRequest().subscribe(null, () => { });
      tick();

      expect(placeBetDocService.buildRequest).toHaveBeenCalledTimes(1);
      expect(bppService.send).toHaveBeenCalledTimes(1);
      expect(bppService.showErrorPopup).toHaveBeenCalledTimes(1);
    }));

    it('error occured (device offline)', fakeAsync(() => {
      deviceService.isOnline.and.returnValue(false);
      bppService.send.and.returnValue(throwError({}));

      service.placeBetsRequest().subscribe(null, () => { });
      tick();

      expect(bppService.showErrorPopup).not.toHaveBeenCalled();
    }));

    it('error occured (status code 4016)', fakeAsync(() => {
      bppService.send.and.returnValue(throwError({ code: '4016' }));

      service.placeBetsRequest().subscribe(null, () => { });
      tick();

      expect(pubsub.publish).toHaveBeenCalledWith(pubSubApi.SHOW_LOCATION_RESTRICTED_BETS_DIALOG);
    }));

    it('check max count of lottobets and limit to 20', () => {
      service.betData = [{stake: {currency:'EUR'}}]
      const lottoObj = {isLotto: true, lottoData:[{accaBets:[{stake:0.1, betType:"SGL_S", lines: {number:21}}]}]}
      const req = service.placeBetsRequest(lottoObj);
      req.subscribe(()=>{}, err =>  expect(err).toEqual('Maximum number of bets limit reached'));
    });

    it('check max count of lottobets and create req headers', fakeAsync(() => {
      deviceService.isOnline.and.returnValue(false);
      bppService.send.and.returnValue(throwError({}));
      service.betData = [{stake: {currency:'EUR'}}]
      const lottoObj = {
        isLotto: true,
        lottoData: [
          { accaBets: [{ stake: 0.1, BetType: "SGL_S", lines: { number: 3 } }] },
          { accaBets: [{ stake: 0.1, BetType: "DBL", lines: { number: 1 } }] }
        ]
      }
      service.placeBetsRequest(lottoObj).subscribe(null, () => { });
      tick();

      expect(lottoBuildBetDocService.constructPlaceBetObj).toHaveBeenCalled();
      expect(bppService.showErrorPopup).not.toHaveBeenCalled();
    }));
  });

  it('getSelections', () => {
    expect(service.getSelections).toEqual([]);
  });

  it('getPlaceBetPending, setPlaceBetPending', () => {
    expect(service.getPlaceBetPending).toBeFalsy();
    service.setPlaceBetPending(true);
    expect(service.getPlaceBetPending).toBeTruthy();
  });

  it('constructFreeBet', () => {
    service.constructFreeBet(<any>{});
    expect(freeBetService.construct).toHaveBeenCalledTimes(1);
    expect(freeBetService.parseOne).toHaveBeenCalledTimes(1);
  });

  describe('isSuspended', () => {
    it('OUTCOME_SUSPENDED', () => {
      expect(service.isSuspended('OUTCOME_SUSPENDED')).toBeTruthy();
    });
    it('MARKET_SUSPENDED', () => {
      expect(service.isSuspended('MARKET_SUSPENDED')).toBeTruthy();
    });
    it('EVENT_SUSPENDED', () => {
      expect(service.isSuspended('EVENT_SUSPENDED')).toBeTruthy();
    });
    it('SELECTION_SUSPENDED', () => {
      expect(service.isSuspended('SELECTION_SUSPENDED')).toBeTruthy();
    });
  });

  describe('toggleSelection', () => {
    it('should open max stake dialog', fakeAsync(() => {
      service.toggleSelection({}, true).subscribe(null, () => { });
      tick();

      expect(betSelectionService.construct).toHaveBeenCalledTimes(1);
      expect(betSelectionsService.findById).toHaveBeenCalledTimes(1);
      expect(dynamicComponentLoader.loadModule).toHaveBeenCalledTimes(1);
      expect(pubsub.publishSync).toHaveBeenCalledWith('BETSLIP_UPDATED');
      expect(dialogService.openDialog).toHaveBeenCalledWith(
        'maxStakeDialog', jasmine.any(Object), true, jasmine.any(Object)
      );
    }));

    it('should not open max stake dialog', fakeAsync(() => {
      cmsServcie.getSystemConfig.and.returnValue(of(throwError('Error in Betslip.getConfig error')));
      service.toggleSelection({}, false).subscribe(null, () => { });
      tick();
      expect(dynamicComponentLoader.loadModule).not.toHaveBeenCalled();
    }));

    it('should handle new bet', fakeAsync(() => {
      cmsServcie.getSystemConfig.and.returnValue(of({
        Betslip: { maxBetNumber: 20 }
      }));

      service.toggleSelection({}, false).subscribe();
      tick();

      expect(betSelectionsService.addSelection).toHaveBeenCalledTimes(1);
    }));

    it('should remove existing bet', fakeAsync(() => {
      cmsServcie.getSystemConfig.and.returnValue(of({
        Betslip: { maxBetNumber: 20 }
      }));
      betSelectionsService.findById.and.returnValue({});

      service.toggleSelection({}, false).subscribe();
      tick();

      expect(betslipDataService.clearMultiplesStakes).toHaveBeenCalledTimes(1);
      expect(betSelectionsService.removeSelection).toHaveBeenCalledTimes(1);
      expect(betslipStorageService.store).toHaveBeenCalledTimes(1);
    }));

    it('should not remove existing bet', fakeAsync(() => {
      cmsServcie.getSystemConfig.and.returnValue(of({
        Betslip: { maxBetNumber: 20 }
      }));
      betSelectionsService.findById.and.returnValue({});

      service.toggleSelection({}, true).subscribe();
      tick();

      expect(betSelectionsService.removeSelection).not.toHaveBeenCalled();
    }));

    it('should edit existing bet', fakeAsync(() => {
      cmsServcie.getSystemConfig.and.returnValue(of({
        Betslip: { maxBetNumber: 20 }
      }));
      const existing: any = { price: {} };
      betSelectionsService.findById.and.returnValue(existing);
      betSelectionsService.data = [{
        id: '1', price: { priceType: 'SP' }
      }];
      betSelectionService.construct.and.returnValue({
        id: '1', price: { priceType: 'LP' }, data: {priceId:''}
      });

      service.toggleSelection({
        id: '1', price: { priceType: 'LP' }, data: {priceId:''} 
      }).subscribe();
      tick();

      expect(existing.price.priceType).toBe('LP');
    }));

    it('should throw error in case of luckydip selection added', fakeAsync(() => {
      service.toggleSelection({details: {
        marketDrilldownTagNames : ['MKTFLAG_LD']
      }}, true).subscribe(()=>{},(error) => { 
        expect(error).toBe(BETSLIP_VALUES.ERRORS.INVALID_LUCKYDIP_SELECTION);
      });
    }));

    it('should handle in case of selection not available', fakeAsync(() => {
      spyOn(service, 'whenCanBeAdded').and.returnValue(of({}));
      betSelectionService.construct.and.returnValue({
        id: '1', price: { priceType: 'LP' }, data: {priceId:''}
      });
      service.toggleSelection(null, true).subscribe();
      tick();
      expect(service.whenCanBeAdded).toHaveBeenCalled();
    }));

    it('should handle in case of selection details not available', fakeAsync(() => {
      spyOn(service, 'whenCanBeAdded').and.returnValue(of({}));
      betSelectionService.construct.and.returnValue({
        id: '1', price: { priceType: 'LP' }, data: {priceId:''}
      });
      service.toggleSelection({}, true).subscribe();
      tick();
      expect(service.whenCanBeAdded).toHaveBeenCalled();
    }));

    it('should handle in case of selection marketDrilldownTagNames not available', fakeAsync(() => {
      spyOn(service, 'whenCanBeAdded').and.returnValue(of({}));
      betSelectionService.construct.and.returnValue({
        id: '1', price: { priceType: 'LP' }, data: {priceId:''}
      });
      service.toggleSelection({details: {name:'test'}}, true).subscribe();
      tick();
      expect(service.whenCanBeAdded).toHaveBeenCalled();
    }));
  });

  it('setConfig', () => {
    const config = {};
    service.setConfig(config);
    expect(service.betSlipConfigs).toBe(config);
  });

  it('placeBets', () => {
    placeBetDocService.buildRequest.and.returnValue(betObject);
    service.placeBets();
    expect(betslipDataService.checkPrices).toHaveBeenCalled();
  });

  it('placeBets should subscribe to response', () => {
    service['placeBetsRequest'] = jasmine.createSpy('placeBetsRequest').and.
    returnValue(of({test: 'test'}));
    service.placeBets().subscribe(response => {
      expect(response).toEqual({test: 'test'});
    });
  });

  it('exucuteOverask', () => {
    const data = {};
    service.exucuteOverask(data);
    expect(overAskService.execute).toHaveBeenCalledWith(data);
    expect(betslipDataService.checkPrices).toHaveBeenCalled();
  });

  describe('setAmount', () => {
    it('should store bets', () => {
      betSelectionsService.data = [{
        id: 'SGL|1',
        params: { outcomesIds: ['1'] }
      }, {
        id: 'FORECAST|1|2',
        params: { outcomesIds: ['1', '2'] }
      }, {
        id: 'SGL|3',
        params: { outcomesIds: ['3'] }
      }, {
        id: 'SGL|3',
        params: { outcomesIds: undefined }
      }];

      service.setAmount({
        Bet: { clearErr: () => { } },
        outcomeId: '1',
        stake: {
          perLine: '7'
        },
        outcomeIds: ['1']
      } as any);

      expect(betSelectionsService.data[0].userStake).toEqual('7');
      expect(betSelectionsService.data[1].userStake).toEqual(undefined);
      expect(betSelectionsService.data[2].userStake).toEqual(undefined);
      expect(betSelectionsService.data[3].userStake).toEqual(undefined);

      service.setAmount({
        Bet: { 
        legs :['1'],clearErr: () => { } , id: 'SGL|3',},
        combiName: 'FORECAST',
        outcomeId: '1|2',
        stake: {
          perLine: '9'
        },
        outcomeIds: ['1', '2']
      } as any);

      expect(betSelectionsService.data[1].userStake).toEqual('9');
      expect(betslipStorageService.store).toHaveBeenCalledTimes(2);

      service.setAmount({
        Bet: { clearErr: () => { } },
        outcomeId: '1|2',
        stake: {
          perLine: '12'
        },
        outcomeIds: undefined
      } as any);

      expect(betSelectionsService.data[0].userStake).toEqual('7');
      expect(betSelectionsService.data[1].userStake).toEqual('9');
      expect(betSelectionsService.data[2].userStake).toEqual(undefined);
      expect(betSelectionsService.data[3].userStake).toEqual(undefined);
      betSelectionsService.data[0].params.outcomeIds = [1,4,3,3,2];
      service.setAmount({
        Bet: { clearErr: () => { } },
        outcomeId: '1|2',
        stake: {
          perLine: '12'
        },
        outcomeIds: [1,4,3,3,2]
      } as any);
      expect(betSelectionsService.data[3].userStake).toEqual(undefined);
    });

    it('should not store bets', () => {
      service.setAmount({ disabled: true });
      expect(betslipStorageService.store).not.toHaveBeenCalled();
    });
  });
  describe('setAmount', () => {
    it('should store bets', () => {
      betSelectionsService.data = [ {
        id: 'SGL|3',
        params: { outcomesIds: ['3'] }
      }];

      service.setAmount({
        Bet: { 
          legs :['1'],
          clearErr: () => { },
          params: {
            lottoData: {
              isLotto: true,
              id: 'SGL|3',
              accaBets: [{
                userStake: 10,
                stake: 10
              }],
              details: {stake: 0.1}
            }
          }
        },
        outcomeId: '1',
        stake: {
          perLine: '7'
        },
        outcomeIds: ['1']
      } as any);

      expect(betSelectionsService.data[0].userStake).toEqual(0.1);

      service.setAmount({
        Bet: { legs :['1'],clearErr: () => { } },
        combiName: 'FORECAST',
        outcomeId: '1|2',
        stake: {
          perLine: '9'
        },
        outcomeIds: ['1', '2']
      } as any);
    });

  });

  describe('fetch', () => {
    it('no outcome ids', () => {
      service.fetchWithSS = jasmine.createSpy('fetchWithSS');
      betslipStorageService.getOutcomesIds.and.returnValue([]);
      betslipStorageService.restore.and.returnValue([
        {
          isVirtual: true,
          outcomesIds: [],
          details: []
        }
      ]);
      service.cleanDataSync = jasmine.createSpy();

      service.fetch();

      expect(service.fetchWithSS).toHaveBeenCalledTimes(1);
      expect(betslipStorageService.restore).toHaveBeenCalledTimes(1);
    });

    it('success flow', fakeAsync(() => {
      const storedData = {
        betOffers: [],
        bets: [
          {
            legs: [
              { docId: 1 }
            ]
          }
        ],
        errs: [],
        legs: [{ docId: 2 }, { docId: 1 }]
      };
      betslipStorageService.restore.and.returnValue([
        {
          isVirtual: false,
          outcomesIds: [{}],
          details: []
        }
      ]);
      legFactoryService.constructLegs.and.returnValue([{ docId: 1 }]);
      betslipStorageService.getOutcomesIds.and.returnValue(['1']);
      service.extendSelections = jasmine.createSpy();
      service.buildBetsRequest = jasmine.createSpy().and.returnValue(of({
        bets: [
          { legs: [{}] },
          { legs: [{}] }
        ]
      }));
      service.buildBetsRequestByStoredData = jasmine.createSpy().and.returnValue(of(storedData));
      service.filterNotRequestedScoreCast = jasmine.createSpy().and.returnValue(storedData);
      service.getAccaOffer = jasmine.createSpy().and.returnValue(of(null));
      service.getStoredBets = jasmine.createSpy();
      service.sortOddsBoosts = jasmine.createSpy().and.returnValue(of(null));
      service.count = jasmine.createSpy();

      service.fetch().subscribe();
      tick();

      expect(betslipStorageService.restore).toHaveBeenCalledTimes(1);
      expect(service.filterNotRequestedScoreCast).toHaveBeenCalledTimes(1);
      expect(service.getAccaOffer).toHaveBeenCalledTimes(1);
      expect(service.getStoredBets).toHaveBeenCalledTimes(1);
      expect(service.sortOddsBoosts).toHaveBeenCalledTimes(1);
      expect(service.count).toHaveBeenCalledTimes(1);
      expect(pubsub.publishSync).toHaveBeenCalledTimes(2);
    }));

    it('failed flow', fakeAsync(() => {
      betslipStorageService.restore.and.returnValue([
        {
          isVirtual: false,
          outcomesIds: [],
          details: []
        }
      ]);
      legFactoryService.constructLegs.and.returnValue([{ docId: 1 }]);
      betslipStorageService.getOutcomesIds.and.returnValue(['1']);
      getSelectionDataService.getOutcomeData.and.returnValue(throwError('Test error'));
      service.count = jasmine.createSpy();

      service.fetch().subscribe(null, () => { });
      tick();

      expect(betslipStorageService.restore).toHaveBeenCalledTimes(1);
      expect(service.count).toHaveBeenCalledTimes(1);
      expect(pubsub.publishSync).toHaveBeenCalledTimes(2);
    }));

    it('should clean data sync if no legs_data', () => {
      service.cleanDataSync = jasmine.createSpy('cleanDataSync');
      betslipStorageService.restore.and.returnValue([
        {
          isVirtual: false,
          outcomesIds: [],
          details: []
        }
      ]);
      legFactoryService.constructLegs.and.returnValue([]);
      service.fetch();

      expect(service.cleanDataSync).toHaveBeenCalledTimes(1);
    });

      it('success flow', fakeAsync(() => {
      betslipStorageService.restore.and.returnValue([
        {
          isLotto: true,
          isVirtual: false,
          outcomesIds: [{}],
          details: {
            name: '492',
            draws: [{}],
            selections: 1|2|3,
            priceId: '49S'
          }
        }
      ]);
      legFactoryService.constructLegs.and.returnValue([{ docId: 1 }]);
      betslipStorageService.getOutcomesIds.and.returnValue(['1']);
      service.extendSelections = jasmine.createSpy();
      service.buildBetsRequest = jasmine.createSpy().and.returnValue(of({
        bets: [
          { legs: [{}] },
          { legs: [{}] }
        ]
      }));
      const lottoData = {
        bets:[{ params: {lottoData: {isLotto:true, selections:'1|2|3', details: {draws:[{}], name:'49s'}}}}]}
        ;
      service.buildBetsRequestByStoredData = jasmine.createSpy().and.returnValue(of(lottoData));
      service.filterNotRequestedScoreCast = jasmine.createSpy().and.returnValue(lottoData);
      service.getAccaOffer = jasmine.createSpy().and.returnValue(of(null));
      service.getStoredBets = jasmine.createSpy();
      service.sortOddsBoosts = jasmine.createSpy().and.returnValue(of(null));
      service.count = jasmine.createSpy();

      service.fetch().subscribe();
      tick();

      expect(betslipStorageService.restore).toHaveBeenCalledTimes(1);
      expect(service.filterNotRequestedScoreCast).toHaveBeenCalledTimes(1);
      expect(service.getAccaOffer).toHaveBeenCalledTimes(1);
      expect(service.getStoredBets).toHaveBeenCalledTimes(1);
      expect(service.sortOddsBoosts).toHaveBeenCalledTimes(1);
      expect(service.count).toHaveBeenCalledTimes(1);
      expect(pubsub.publishSync).toHaveBeenCalledTimes(2);
    }));
  });

  describe('fetchWithSS', () => {
    beforeEach(() => {
      service.cleanDataSync = jasmine.createSpy('service');
    });

    it('should fetch wit SS', fakeAsync(() => {
      betslipStorageService.getOutcomesIds.and.returnValue([1]);
      betslipStorageService.restore.and.returnValue([
        {
          isVirtual: true,
          outcomesIds: [1, 2],
          details: []
        }
      ]);
      betslipStorageService.getOutcomesIds.and.returnValue([1, 2]);
      betslipStorageService.filterSelections.and.returnValue(of([1]));
      service.extendSelections = jasmine.createSpy().and.returnValue(of({}));
      service.buildBetsRequest = jasmine.createSpy().and.returnValue(of({ bets: [{ legs: [{ docId: 1 }] }] }));
      service.filterNotRequestedScoreCast = jasmine.createSpy().and.returnValue(of({}));
      service.getAccaOffer = jasmine.createSpy().and.returnValue(of({}));
      service.fetchWithSS().subscribe(null, () => { });
      tick();
      expect(service.cleanDataSync).not.toHaveBeenCalled();
      expect(pubsub.publish).toHaveBeenCalled();
      expect(pubsub.publishSync).toHaveBeenCalledWith('BETSLIP_COUNTER_UPDATE', 0);
      expect(pubsub.publishSync).toHaveBeenCalledWith('ADDTOBETSLIP_PROCESS_FINISHED');
    }));
    it('should clean data if no outcomes', fakeAsync(() => {
      betslipStorageService.getOutcomesIds.and.returnValue([]);
      betslipStorageService.restore.and.returnValue([
        {
          isVirtual: true,
          outcomesIds: [],
          details: []
        }
      ]);
      service.fetchWithSS();
      expect(service.cleanDataSync).toHaveBeenCalled();
    }));
    it('should return error', fakeAsync(() => {
      betslipStorageService.getOutcomesIds.and.returnValue([1]);
      betslipStorageService.restore.and.returnValue([
        {
          isVirtual: true,
          outcomesIds: [1, 2],
          details: []
        }
      ]);
      spyOn(console, 'warn');
      betslipStorageService.filterSelections.and.returnValue(throwError(null));
      service.fetchWithSS().subscribe(null, () => { });
      expect(console.warn).toHaveBeenCalled();
      expect(pubsub.publishSync).toHaveBeenCalledWith('BETSLIP_COUNTER_UPDATE', 0);
      expect(pubsub.publishSync).toHaveBeenCalledWith('ADDTOBETSLIP_PROCESS_FINISHED');
    }));
  });

  describe('buildBetsRequestByStoredData', () => {
    let buildBetResponceData;
    let response;
    let legs, storedRacingSelection, storedSportSelection, storedSelections, details;
    let event, market, outcome;
    beforeEach(() => {
      service.cleanData = jasmine.createSpy('cleanData');
      service.updateEWFlagInStoredSelection = jasmine.createSpy('updateEWFlagInStoredSelection');
      getSelectionDataService.createOutcomeData = jasmine.createSpy('createOutcomeData').and.returnValue({
        data: {}
      });
      service.extendSelections = jasmine.createSpy('extendSelections');
      service.setSelectionErrors = jasmine.createSpy('setSelectionErrors');
      buildBetDocService.setResponse.and.returnValue({ bets: [] });
      spyOn(Subscriber.prototype, 'error');
      outcome = {
        outcomeStatusCode: 'test',
        id: 1,
        children: [
          { price: { priceType: 'SP' } }
        ]
      };
      market = {
        marketStatusCode: 'test',
        isLpAvailable: false,
        isSpAvailable: true,
        isGpAvailable: false,
        priceTypeCodes: 'SP',
        drilldownTagNames: 'tag1',
        id: '123',
        children: [{ outcome }]
      };
      event = {
        id: 1,
        eventStatusCode: 'test',
        isStarted: true,
        isMarketBetInRun: true,
        drilldownTagNames: 'tag2',
        children: [{ market }]
      };
      response = {
        SSResponse: {
          children: [{ event }]
        }
      };
      buildBetResponceData = {
        betErrors: [{ outcomeRef: { id: 1 } }],
        outcomeDetails: [
          {
            id: 1,
            eventId: 1,
            marketId: '123'
          }
        ]
      };
      legs = [{}];
      storedRacingSelection = {
        outcomesIds: [1, 2],
        details: {
          marketId: '123',
          eventId: 1,
          info: {
            sportId: '12'
          }
        }
      };
      storedSportSelection = {
        outcomesIds: [111, 222],
        details: {
          marketId: '123',
          eventId: 1,
          info: {
            sportId: '159'
          }
        }
      };
      storedSelections = [storedRacingSelection, storedSportSelection];
      details = {
        id: 1,
        eventId: 1,
        marketId: '123',
        eventStatusCode: 'test',
        isStarted: false,
        isMarketBetInRun: false,
        marketStatusCode: 'test',
        outcomeStatusCode: 'test',
        priceType: 'SP',
        isLpAvailable: false,
        isSpAvailable: true,
        isGpAvailable: false,
        outcomeMeaningMinorCode: undefined,
        marketDrilldownTagNames: 'tag1',
        eventDrilldownTagNames: 'tag2'
      };
    });
    it('should catch error', fakeAsync(() => {
      bppService.send.and.returnValue(of(buildBetResponceData));
      ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.reject('error'));
      service.buildBetsRequestByStoredData(legs, storedSelections).subscribe();
      tick();
      expect(bppService.send).toHaveBeenCalled();
      expect(service.cleanData).not.toHaveBeenCalled();
    }));
    it('should clean data if no outcome details', () => {
      buildBetResponceData.outcomeDetails = [];
      legs = [{}];
      storedSelections = [];
      bppService.send.and.returnValue(of(buildBetResponceData));
      ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
      service.buildBetsRequestByStoredData(legs, storedSelections).subscribe();
      expect(bppService.send).toHaveBeenCalled();
    });
    it('should clean data if no legs_data received', () => {
      legs = [];
      storedSelections = [];
      service.buildBetsRequestByStoredData(legs, storedSelections);
      expect(bppService.send).not.toHaveBeenCalled();
      expect(service.cleanData).toHaveBeenCalled();
    });
    it('should call bpp service', fakeAsync(() => {
      user.bppToken = 'token';
      bppService.send.and.returnValue(of(buildBetResponceData));
      ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.resolve(response));

      service.buildBetsRequestByStoredData(legs, storedSelections).subscribe();
      tick();

      expect(bppService.send).toHaveBeenCalled();
      expect(ssRequestHelper.getEventsByOutcomes).toHaveBeenCalledWith({ outcomesIds: [1], isValidFzSelection: true });
      expect(getSelectionDataService.createOutcomeData).toHaveBeenCalledWith(details, storedRacingSelection);
      expect(service.extendSelections).toHaveBeenCalled();
      expect(service.buildBetDocService.setResponse).toHaveBeenCalledWith(buildBetResponceData);
      expect(service.setSelectionErrors).toHaveBeenCalled();
      expect(service.cleanData).not.toHaveBeenCalled();
    }));

    it('should call bpp service and set priceType as LP for details object', fakeAsync(() => {
      response.SSResponse.children[0].event.children[0].market.priceTypeCodes = 'LP, SP';
      user.bppToken = 'token';
      bppService.send.and.returnValue(of(buildBetResponceData));
      ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
      details.priceType = 'LP';

      service.buildBetsRequestByStoredData(legs, storedSelections).subscribe();
      tick();

      expect(bppService.send).toHaveBeenCalled();
      expect(getSelectionDataService.createOutcomeData).toHaveBeenCalledWith(details, storedRacingSelection);
    }));

    it('should call bpp service: no events case', fakeAsync(() => {
      response.SSResponse.children = <any>[{}];
      buildBetResponceData.outcomeDetails = [{ id: 1, eventId: 1 }];
      bppService.send.and.returnValue(of(buildBetResponceData));
      ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
      service.buildBetsRequestByStoredData(legs, storedSelections).subscribe();
      tick();
      expect(bppService.send).toHaveBeenCalled();
      expect(getSelectionDataService.createOutcomeData).toHaveBeenCalledWith({ eventId: 1, id: 1, }, storedRacingSelection);
    }));

    it('should call bpp service: no markets case', fakeAsync(() => {
      response.SSResponse.children = [
        {
          event: {
            id: 1,
            eventStatusCode: 'test',
            isStarted: true,
            isMarketBetInRun: true,
            children: <any>[{}]
          }
        }
      ];
      buildBetResponceData.outcomeDetails = [{ id: 1, eventId: 1 }];
      bppService.send.and.returnValue(of(buildBetResponceData));
      ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
      service.buildBetsRequestByStoredData(legs, storedSelections).subscribe();
      tick();
      expect(bppService.send).toHaveBeenCalled();
      expect(getSelectionDataService.createOutcomeData).toHaveBeenCalledWith({ eventId: 1, id: 1, }, storedRacingSelection);

      response.SSResponse.children = [
        {
          event: <any>{
            id: 1,
            eventStatusCode: 'test',
            isStarted: true,
            isMarketBetInRun: true
          }
        }
      ];
      ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
      service.buildBetsRequestByStoredData(legs, storedSelections).subscribe();
      tick();
      expect(bppService.send).toHaveBeenCalled();
      expect(getSelectionDataService.createOutcomeData).toHaveBeenCalledWith({ eventId: 1, id: 1, }, storedRacingSelection);
    }));

    it('should call bpp service: no outcomes case', fakeAsync(() => {
      response.SSResponse.children = [
        {
          event: {
            id: 1,
            eventStatusCode: 'test',
            isStarted: true,
            isMarketBetInRun: true,
            children: [
              {
                market: {
                  marketStatusCode: 'test',
                  children: [{}]
                }
              }
            ]
          }
        }
      ];
      buildBetResponceData.outcomeDetails = [{ id: 1, eventId: 1 }];
      bppService.send.and.returnValue(of(buildBetResponceData));
      ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
      service.buildBetsRequestByStoredData(legs, storedSelections).subscribe();
      tick();
      expect(bppService.send).toHaveBeenCalled();
      expect(getSelectionDataService.createOutcomeData).toHaveBeenCalledWith({ eventId: 1, id: 1 }, storedRacingSelection);

      response.SSResponse.children = [
        {
          event: {
            id: 1,
            eventStatusCode: 'test',
            isStarted: true,
            isMarketBetInRun: true,
            children: [{ market: { marketStatusCode: 'test' } }]
          }
        }
      ];
      ssRequestHelper.getEventsByOutcomes.and.returnValue(Promise.resolve(response));
      service.buildBetsRequestByStoredData(legs, storedSelections).subscribe();
      tick();
      expect(bppService.send).toHaveBeenCalled();
      expect(getSelectionDataService.createOutcomeData).toHaveBeenCalledWith({ eventId: 1, id: 1, }, storedRacingSelection);
    }));

    it('should not get events by outcomes', fakeAsync(() => {
      buildBetResponceData.betErrors = [];
      bppService.send.and.returnValue(of(buildBetResponceData));
      service.buildBetsRequestByStoredData(legs, storedSelections).subscribe();
      tick();
      expect(ssRequestHelper.getEventsByOutcomes).not.toHaveBeenCalled();

      buildBetResponceData.betErrors = <any>[{ outcomeRef: {} }];
      bppService.send.and.returnValue(of(buildBetResponceData));
      service.buildBetsRequestByStoredData(legs, storedSelections).subscribe();
      tick();
      expect(ssRequestHelper.getEventsByOutcomes).not.toHaveBeenCalled();

      storedRacingSelection = {
        outcomesIds: [1, 2],
        details: {
          info: {
            sportId: '19'
          }
        }
      };
      storedSelections = [storedRacingSelection];
      betslipStorageService.eventToBetslipObservable = {};
      service.buildBetsRequestByStoredData(legs, storedSelections).subscribe();
      expect(ssRequestHelper.getEventsByOutcomes).not.toHaveBeenCalled();
    }));

    it('should not get events by outcomes is undefined', fakeAsync(() => {
      bppService.send.and.returnValue(of({}));
      service.buildBetsRequestByStoredData(legs, storedSelections).subscribe();
      tick();
      expect(ssRequestHelper.getEventsByOutcomes).not.toHaveBeenCalled();
    }))

      it('should get lottoData with accas', () => {
      const storedSElection = {
        id:123,
        isLotto: true,
        details: {
          priceId: '49s',
          selections: 'SGL|1|2|3'
        }
      };
      storedSelections = [storedSElection];
      buildBetResponceData = [
        {priceId:'49s', picks:'SGL|1|2|3', lotteryIds: [123,456], bets:[{}]}
      ];

      const lottoData = [{isLotto: true, id:'SGL|1|2|3', details:{selections:'SGL|1|2|3'}}];
      service.extendSelections = jasmine.createSpy().and.returnValue(lottoData);
      bppService.send.and.returnValue(of(buildBetResponceData));
      service['buildBetsRequestByStoredData'](lottoData, storedSelections).subscribe(res => 
        expect(res).toEqual({bets: []}));
    });

    it('should get lottoData with accas using lottobuildbetlogged', () => {
      const storedSElection = {
        id:123,
        isLotto: true,
        details: {
          priceId: '49s',
          selections: 'SGL|1|2|3'
        }
      };
      service['user'].bppToken = true;
      storedSelections = [storedSElection];
      buildBetResponceData = [
        {priceId:'49s', picks:'SGL|1|2|3', lotteryIds: [123,456], bets:[{}]}
      ];

      const lottoData = [{isLotto: true, id:'SGL|1|2|3', details:{selections:'SGL|1|2|3'}}];
      service.extendSelections = jasmine.createSpy().and.returnValue(lottoData);
      bppService.send.and.returnValue(of(buildBetResponceData));
      service['buildBetsRequestByStoredData'](lottoData, storedSelections);
      expect(bppService.send).toHaveBeenCalled();
  });
    it('should get events by outcomes for racing selections and selections with error codes', () => {
      storedRacingSelection = {
        outcomesIds: [1, 2],
        details: {
          info: {
            sportId: '19'
          }
        }
      };
      storedSelections = [storedRacingSelection];
      buildBetResponceData.betErrors = <any>[
        {
          outcomeRef: {
            id: 1
          }
        },
        {
          outcomeRef: {
            id: 11
          }
        },
        {
          outcomeRef: {
            id: 111
          }
        }
      ];
      bppService.send.and.returnValue(of(buildBetResponceData));
      deviceService.isDesktop = true;
      service.buildBetsRequestByStoredData(legs, storedSelections).subscribe();
      expect(service.updateEWFlagInStoredSelection).toHaveBeenCalled();
      expect(ssRequestHelper.getEventsByOutcomes).toHaveBeenCalledWith(
        { outcomesIds: [1, 11, 111, 2], isValidFzSelection: true }
      );
    });

    it('should get events by outcomes for racing selections and selections with error codes', () => {
      storedRacingSelection = { outcomesIds: [1, 2], details: { info: { sportId: '19'  } } };
      storedSelections = [storedRacingSelection];
      buildBetResponceData.betErrors = <any>[{outcomeRef: {  id: 1 } }, { outcomeRef: {  id: 11 } },  { outcomeRef: {  id: 111 } }];
      bppService.send.and.returnValue(of(buildBetResponceData));
      deviceService.isDesktop = false;
      service.buildBetsRequestByStoredData(legs, storedSelections).subscribe();
      expect(service.updateEWFlagInStoredSelection).not.toHaveBeenCalled();
      expect(ssRequestHelper.getEventsByOutcomes).toHaveBeenCalledWith(
        { outcomesIds: [1, 11, 111, 2], isValidFzSelection: true}
      );
    });
  });

  describe('winOrEachWay', () => {
    beforeEach(() => {
      betSelectionsService.data = [{
        outcomes: [{ id: '1' }]
      }, {
        outcomes: [{ id: '2' }]
      }, {
        outcomes: [{ id: '2' }, { id: '2' }]
      }];
    });

    it('winOrEachWay', () => {
      betSelectionsService.data = [{
        outcomes: [{ id: '1' }]
      }, {
        outcomes: [{ id: '2' }]
      }, {
        outcomes: [{ id: '2' }, { id: '2' }]
      }];
      service.winOrEachWay({
        price: {},
        outcomeId: '1',
        Bet: { isEachWay: true, price: {} }
      });

      expect(betSelectionsService.data[0].userEachWay).toEqual(true);
      expect(betSelectionsService.data[1].userEachWay).toEqual(undefined);
      expect(betSelectionsService.data[2].userEachWay).toEqual(undefined);

      service.winOrEachWay({
        outcomeId: '2',
        Bet: { isEachWay: false }
      });

      expect(betSelectionsService.data[0].userEachWay).toEqual(true);
      expect(betSelectionsService.data[1].userEachWay).toEqual(false);
      expect(betSelectionsService.data[2].userEachWay).toEqual(undefined);

      expect(betslipStorageService.setFreeBet).toHaveBeenCalledTimes(2);
      expect(betslipStorageService.store).toHaveBeenCalledTimes(2);
    });

    it(`should Not set 'userEachWay' for selection with couple outcomes`, () => {
      service.winOrEachWay({
        outcomeId: '1',
        Bet: { isEachWay: true }
      });

      expect(betSelectionsService.data[1].userEachWay).toBeUndefined();
    });

    it(`should outcome id is undefined`, () => {
      service.winOrEachWay({
        Bet: { isEachWay: false }
      });
      expect(betslipStorageService.setFreeBet).toHaveBeenCalledTimes(1);
      expect(betslipStorageService.store).toHaveBeenCalledTimes(1);
    });

    it(`should outcome id is does not match with the betSelectionsService outcomes id`, () => {
      const betData = {
        outcomeId: '3',
        Bet: { isEachWay: true }
      };
      service.winOrEachWay(betData);
      expect(betData.Bet.isEachWay).toBe(true);
      expect(betslipStorageService.setFreeBet).toHaveBeenCalledTimes(1);
      expect(betslipStorageService.store).toHaveBeenCalledTimes(1);
    });

    it(`should stop iteration when found outcome`, () => {
      betSelectionsService.data.unshift({
        outcomes: [{ id: '1' }]
      });

      service.winOrEachWay({
        outcomeId: '1',
        Bet: { isEachWay: true }
      });

      expect(betSelectionsService.data[0].userEachWay).toBeTruthy();
      expect(betSelectionsService.data[1].userEachWay).toBeUndefined();
      expect(betSelectionsService.data[2].userEachWay).toBeUndefined();
      expect(betSelectionsService.data[3].userEachWay).toBeUndefined();
    });
  });

  describe('removeReUseSelections', () => {
    it('when no reuse bets found', () => {
      storageService.get.and.returnValue({
        '333': {
          location: 'testlocation',
          module: 'testModule',
          betType: 'reuse'
        }
      });
      service.removeReUseSelections('222');
      expect(storageService.get).toHaveBeenCalled();
    });
    it('when reuse bets found', () => {
      storageService.get.and.returnValue({
        '333': {
          location: 'testlocation',
          module: 'testModule',
          betType: 'reuse'
        }
      });
      service.removeReUseSelections('333');
      expect(storageService.get).toHaveBeenCalled();
    });
  });

  it('removeByOutcomeId', () => {
    service.removeByOutcomeId({ outcomeId: '1' });
    expect(pubsub.publish).toHaveBeenCalledWith('REMOVE_VS_STORAGE', '1');
    expect(betSelectionsService.findById).toHaveBeenCalledWith('SGL|1');

    service.removeByOutcomeId({ outcomeId: '2|3', combiName: 'FORECAST' });
    expect(pubsub.publish).toHaveBeenCalledWith('REMOVE_VS_STORAGE', '2|3');
    expect(betSelectionsService.findById).toHaveBeenCalledWith('FORECAST|2|3');
  });

  it('removeByOutcomeIds', () => {
    service.removeByOutcomeIds([{ outcomeId: '1' }]);
    expect(pubsub.publish).toHaveBeenCalledWith('REMOVE_VS_STORAGE', '1');
    expect(betSelectionsService.findById).toHaveBeenCalledWith('SGL|1');

    service.removeByOutcomeIds([{ outcomeId: '2|3', combiName: 'FORECAST' }]);
    service.removeMulti([{ outcomeId: '1' }]);
    expect(pubsub.publish).toHaveBeenCalledWith('REMOVE_VS_STORAGE', '2|3');
    expect(betSelectionsService.findById).toHaveBeenCalledWith('FORECAST|2|3');
  });

  it('removeByOutcomeIdHandler for Lotto', () => {
    service.removeByOutcomeId({ isLotto: true, id:'SGL|1' });
    expect(pubsub.publish).toHaveBeenCalledWith('REMOVE_VS_STORAGE', 'SGL|1');
    expect(betSelectionsService.findById).toHaveBeenCalledWith('SGL|1');
  });

  it('setPriceType', () => {
    betSelectionsService.data = [{
      outcomes: [{ id: '1' }]
    }, {
      outcomes: [{ id: '2' }]
    }];

    service.setPriceType({
      outcomeId: '1', price: { priceType: 'SP' },
      Bet: { price: {} }
    } as any);

    service.setPriceType({
      outcomeId: '2', price: {},
      Bet: { price: {} }
    } as any);

    expect(pubsub.publish).toHaveBeenCalledTimes(1);
    expect(pubsub.publishSync).toHaveBeenCalledWith('BETSLIP_UPDATED');
    expect(betslipStorageService.store).toHaveBeenCalledTimes(2);
  });

  it('updateSelection', () => {
    betslipDataService.bets = [{
      info: () => ({ outcomeId: '1', price: {} }),
      update: jasmine.createSpy('update'),
      legs: []
    }];

    const updateData = {};
    service.updateSelection(0, updateData, '');

    expect(betslipDataService.bets[0].update).toHaveBeenCalledWith(updateData, '');
    expect(betslipStorageService.updateStorage).toHaveBeenCalledWith(updateData, '1');
    expect(pubsub.publishSync).toHaveBeenCalledWith('BETSLIP_UPDATED', [betslipDataService.bets]);
    expect(pubsub.publishSync).toHaveBeenCalledWith(pubSubApi.BS_SELECTION_LIVE_UPDATE, betslipDataService.bets[0]);
  });


  it('edit Selection in storage', () => {
    service.edit({id:123, isLotto: true}, {id:123, isLotto: true});
    expect(betSelectionsService.updateSelection).toHaveBeenCalled();
  })

  it('edit/update Selection in storage', () => {
    service.edit({id:1, price:{priceType: 1}}, {id:123, price:{priceType: 2}});
    expect(betSelectionsService.updateSelection).not.toHaveBeenCalled();
  })
  describe('showSuspendedOutcomeErr', () => {
    const suspendedMessage = 'suspendedMessage';

    beforeEach(() => {
      service.getSuspendedMessage = jasmine.createSpy('getSuspendedMessage').and.returnValue(suspendedMessage);
    });

    it('should not return any messages if no suspended bets', () => {
      overAskService.isInProcess = false;
      const singles = [{ betId: 888, disabled: false, eventIds: { outcomeIds: [1] } }] as any;
      const multiples = [{ betId: 999, eventIds: { outcomeIds: [1] }, stake: { perLine: null } }] as any;

      const result = service.showSuspendedOutcomeErr(singles, multiples);

      expect(multiples[0].disabled).toEqual(false);
      expect(service.getSuspendedMessage).not.toHaveBeenCalled();
      expect(overAskService.setSuspended).not.toHaveBeenCalled();
      expect(result).toEqual({
        multipleWithDisableSingle: false,
        disableBet: false,
        msg: null
      });
    });

    describe('for betslip flow', () => {
      beforeEach(() => {
        overAskService.isInProcess = false;
      });

      it('should check disabled single and disabled multiples', () => {
        const singles = [{ betId: 888, disabled: true, eventIds: { outcomeIds: [1] }, combiType: 'FORECAST', outcomes: [{details: { markets: [{ncastTypeCodes: 'CF'}]}}] }] as any;
        const multiples = [{ betId: 999, eventIds: { outcomeIds: [1] }, stake: { perLine: null } }] as any;

        const result = service.showSuspendedOutcomeErr(singles, multiples);

        expect(multiples[0].disabled).toEqual(false);
        expect(service.getSuspendedMessage).toHaveBeenCalledWith(1);
        expect(overAskService.setSuspended).not.toHaveBeenCalled();
        expect(overAskService.isBetPlaced).not.toHaveBeenCalled();
        expect(result).toEqual({
          multipleWithDisableSingle: true,
          disableBet: false,
          msg: suspendedMessage
        });
      });

      it('should check disabled single and disabled multiples with stake', () => {
        const singles = [{ betId: 888, disabled: true, eventIds: { outcomeIds: [1] }, combiType: 'TRICAST', outcomes: [{details: { markets: [{ncastTypeCodes: 'CT'}]}}] }] as any;
        const multiples = [{ betId: 999, eventIds: { outcomeIds: [1] }, stake: { perLine: 5 } }] as any;

        const result = service.showSuspendedOutcomeErr(singles, multiples);

        expect(multiples[0].disabled).toEqual(false);
        expect(service.getSuspendedMessage).toHaveBeenCalledWith(1);
        expect(overAskService.setSuspended).not.toHaveBeenCalled();
        expect(overAskService.isBetPlaced).not.toHaveBeenCalled();
        expect(result).toEqual({
          multipleWithDisableSingle: true,
          disableBet: true,
          msg: suspendedMessage
        });
      });
      it('should check disabled single and disabled multiples with stake when TRICAST outcomes as null', () => {
        const singles = [{ betId: 888, disabled: true, eventIds: { outcomeIds: [1] }, combiType: 'TRICAST' }] as any;
        const multiples = [{ betId: 999, eventIds: { outcomeIds: [1] }, stake: { perLine: 5 } }] as any;

        const result = service.showSuspendedOutcomeErr(singles, multiples);
      });
      it('should check disabled single and disabled multiples with stake when TRICAST markets as null', () => {
        const singles = [{ betId: 888, disabled: true, eventIds: { outcomeIds: [1] }, combiType: 'TRICAST', outcomes: [{details: { markets: [{}]}}] }] as any;
        const multiples = [{ betId: 999, eventIds: { outcomeIds: [1] }, stake: { perLine: 5 } }] as any;

        const result = service.showSuspendedOutcomeErr(singles, multiples);
      });
      it('should check disabled single and disabled multiples with stake when TRICAST ncastTypeCodes as null', () => {
        const singles = [{ betId: 888, disabled: true, eventIds: { outcomeIds: [1] }, combiType: 'TRICAST', outcomes: [{details: { markets: []}}] }] as any;
        const multiples = [{ betId: 999, eventIds: { outcomeIds: [1] }, stake: { perLine: 5 } }] as any;

        const result = service.showSuspendedOutcomeErr(singles, multiples);
      });
      it('should check disabled single and disabled multiples with stake when TRICAST ncastTypeCodes as null', () => {
        const singles = [{ betId: 888, disabled: true, eventIds: { outcomeIds: [1] }, combiType: 'TRICAST', outcomes: [{}] }] as any;
        const multiples = [{ betId: 999, eventIds: { outcomeIds: [1] }, stake: { perLine: 5 } }] as any;

        const result = service.showSuspendedOutcomeErr(singles, multiples);
      });
      it('should check disabled single and disabled multiples with stake when FORECAST outcomes as null', () => {
        const singles = [{ betId: 888, disabled: true, eventIds: { outcomeIds: [1] }, combiType: 'FORECAST' }] as any;
        const multiples = [{ betId: 999, eventIds: { outcomeIds: [1] }, stake: { perLine: 5 } }] as any;

        const result = service.showSuspendedOutcomeErr(singles, multiples);
      });
      it('should check disabled single and disabled multiples with stake when FORECAST markets as null', () => {
        const singles = [{ betId: 888, disabled: true, eventIds: { outcomeIds: [1] }, combiType: 'FORECAST', outcomes: [{details: { markets: [{}]}}] }] as any;
        const multiples = [{ betId: 999, eventIds: { outcomeIds: [1] }, stake: { perLine: 5 } }] as any;

        const result = service.showSuspendedOutcomeErr(singles, multiples);
      });
      it('should check disabled single and disabled multiples with stake when FORECAST ncastTypeCodes as null', () => {
        const singles = [{ betId: 888, disabled: true, eventIds: { outcomeIds: [1] }, combiType: 'FORECAST', outcomes: [{details: { markets: []}}] }] as any;
        const multiples = [{ betId: 999, eventIds: { outcomeIds: [1] }, stake: { perLine: 5 } }] as any;

        const result = service.showSuspendedOutcomeErr(singles, multiples);
      });
      it('should check disabled single and disabled multiples with stake when FORECAST ncastTypeCodes as null', () => {
        const singles = [{ betId: 888, disabled: true, eventIds: { outcomeIds: [1] }, combiType: 'FORECAST', outcomes: [{}] }] as any;
        const multiples = [{ betId: 999, eventIds: { outcomeIds: [1] }, stake: { perLine: 5 } }] as any;

        const result = service.showSuspendedOutcomeErr(singles, multiples);
      });
      it('should check disabled single and but not multiples', () => {
        const singles = [{ betId: 888, disabled: true, eventIds: { outcomeIds: [1] } }] as any;
        const multiples = [{ betId: 999, eventIds: { outcomeIds: [2] }, stake: { perLine: 5 } }] as any;

        const result = service.showSuspendedOutcomeErr(singles, multiples);

        expect(multiples[0].disabled).toEqual(false);
        expect(service.getSuspendedMessage).toHaveBeenCalledWith(1);
        expect(overAskService.setSuspended).not.toHaveBeenCalled();
        expect(overAskService.isBetPlaced).not.toHaveBeenCalled();
        expect(result).toEqual({
          multipleWithDisableSingle: false,
          disableBet: false,
          msg: suspendedMessage
        });
      });
    });

    describe('for overask flow', () => {
      beforeEach(() => {
        overAskService.isInProcess = true;
      });

      it('should not check disabled single and disabled multiples if not placed', () => {
        overAskService.isBetPlaced.and.returnValue(false);
        const singles = [{ betId: 888, disabled: true, eventIds: { outcomeIds: [1] } }] as any;
        const multiples = [{ betId: 999, eventIds: { outcomeIds: [1] }, stake: { perLine: 5 } }] as any;

        const result = service.showSuspendedOutcomeErr(singles, multiples);

        expect(multiples[0].disabled).toEqual(false);
        expect(service.getSuspendedMessage).not.toHaveBeenCalled();
        expect(overAskService.setSuspended).toHaveBeenCalledWith([]);
        expect(overAskService.isBetPlaced).toHaveBeenCalledTimes(2);
        expect(result).toEqual({
          multipleWithDisableSingle: false,
          disableBet: false,
          msg: null
        });
      });

      it('should check disabled single and disabled multiples if placed', () => {
        overAskService.isBetPlaced.and.returnValue(true);
        const singles = [{ betId: 888, disabled: true, eventIds: { outcomeIds: [1] } }] as any;
        const multiples = [{ betId: 999, eventIds: { outcomeIds: [1] }, stake: { perLine: 5 } }] as any;

        const result = service.showSuspendedOutcomeErr(singles, multiples);

        expect(multiples[0].disabled).toEqual(true);
        expect(service.getSuspendedMessage).toHaveBeenCalledWith(2);
        expect(overAskService.setSuspended).toHaveBeenCalledWith([888, 999]);
        expect(overAskService.isBetPlaced).toHaveBeenCalledTimes(2);
        expect(result).toEqual({
          multipleWithDisableSingle: true,
          disableBet: true,
          msg: suspendedMessage
        });
      });

      it('should check disabled placed single not disableds multiple', () => {
        overAskService.isBetPlaced.and.returnValue(true);
        const singles = [{ betId: 888, disabled: true, eventIds: { outcomeIds: [1] } }] as any;
        const multiples = [{ betId: 999, eventIds: { outcomeIds: [5] }, stake: { perLine: 5 } }] as any;

        const result = service.showSuspendedOutcomeErr(singles, multiples);

        expect(multiples[0].disabled).toEqual(false);
        expect(service.getSuspendedMessage).toHaveBeenCalledWith(1);
        expect(overAskService.setSuspended).toHaveBeenCalledWith([888]);
        expect(overAskService.isBetPlaced).toHaveBeenCalledTimes(1);
        expect(result).toEqual({
          multipleWithDisableSingle: false,
          disableBet: false,
          msg: suspendedMessage
        });
      });
    });
  });

  describe('areBetsWithStakes', () => {
    it('check mocked', () => {
      expect(
        service.areBetsWithStakes([{
          stake: { perLine: 1 }
        }], true)
      ).toBeTruthy();

      expect(
        service.areBetsWithStakes([{
          stake: {}, selectedFreeBet: {}
        }], true)
      ).toBeTruthy();

      expect(
        service.areBetsWithStakes([{
          stake: {}
        }], true)
      ).toBeFalsy();
    });

    it('not mocked', () => {
      expect(
        service.areBetsWithStakes([{
          stake: { perLine: 1 }
        }], false)
      ).toBeTruthy();

      expect(
        service.areBetsWithStakes([{
          stake: {}, selectedFreeBet: {}
        }], false)
      ).toBeTruthy();

      expect(
        service.areBetsWithStakes([{
          stake: {}
        }], false)
      ).toBeFalsy();
    });

    it('areBets with Lotto Stakes', () => {
      expect(
        service.areBetsWithStakes([{
          isLotto:true,
          accaBets:[{stake:0.1}],
          details:{}
        }], false)
      ).toBeTruthy();
    });
  });


  it('countSuspendedOutcomes', () => {
    expect(
      service.countSuspendedOutcomes([
        { disabled: true }, {}
      ])
    ).toBe(1);
  });

  it('suspendedIndexFromSelection', () => {
    expect(
      service.suspendedIndexFromSelection([
        { disabled: true }, {}
      ])
    ).toEqual([{ disabled: true }]);
  });

  it('findSuspendedBetsId', () => {
    service.findSuspendedBetsId([
      { outcomeId: '1', error: 'OUTCOME_SUSPENDED' }, { outcomeId: '2' }
    ]);
    expect(betslipStorageService.storeSuspended).toHaveBeenCalledWith(['1']);
  });

  it('isMultipleFreeBetSelected', () => {
    expect(
      service.isMultipleFreeBetSelected([{ selectedFreeBet: {} }])
    ).toBeTruthy();
    expect(
      service.isMultipleFreeBetSelected([{}])
    ).toBeFalsy();
  });

  describe('setSelectionErrors', () => {
    it('bets with erros', () => {
      const betslipData = {
        bets: [{
          info: () => ({ outcomeId: '1' })
        }, {
          info: () => ({ outcomeId: '1|2' })
        }, {
          info: () => ({ outcomeId: '3' })
        }],
        errs: [{ outcomeId: '1' }, { outcomeId: '1' }, { outcomeId: '1|2' }]
      };

      betSelectionsService.data = [{
        outcomes: [{ id: '1' }, { id: '2' }]
      }];
      service['setSelectionErrors'](betslipData);

      expect(betSelectionsService.data[0].errs).toBeTruthy();
    });

    it('no errors', () => {
      betSelectionsService.data = { bets: [] };
      expect(service['setSelectionErrors']([])).toBeFalsy();
    });
  });

  describe('count', () => {
    it('should return 1 if tote bet present', () => {
      toteBetSlipService.isToteBetPresent.and.returnValue(true);
      expect(service.count()).toBe(1);
    });

    it('should get bets count from betSelectionsService', () => {
      betSelectionsService.count.and.returnValue(5);
      expect(service.count()).toBe(5);
    });
  });

  it('getBetslipBetByResponseBet', () => {
    const bet = {
      legRef: [{ documentId: 1 }, { documentId: 2 }],
      betTypeRef: { id: 'SGL' },
      stake: { stakePerLine: 1 }
    };
    const legs = [{
      documentId: 1,
      sportsLeg: {
        legPart: [{
          outcomeRef: { id: 1 }
        }]
      }
    }, {
      documentId: 2,
      sportsLeg: {
        legPart: [{
          outcomeRef: { id: 2 }
        }]
      }
    }];
    const allBets = [{
      type: 'SGL',
      Bet: {
        legs: [{
          parts: [{
            outcome: { id: 1 }
          }, {
            outcome: { id: 2 }
          }]
        }]
      },
      stake: { placement: 1 }
    }, {
      type: 'DBL'
    }];

    expect(
      service.getBetslipBetByResponseBet(bet, legs, allBets)
    ).toBeTruthy();

    bet.stake.stakePerLine = 0;
    expect(
      service.getBetslipBetByResponseBet(bet, legs, allBets)
    ).toBeFalsy();
  });

  describe('getMultiplePotentialPayout', () => {
    it('odds changed by trader', () => {
      expect(
        service.getMultiplePotentialPayout({
          traderChangedOdds: true, potentialPayout: 10, stake: { perLine: 2 }
        })
      ).toBe(5);
    });

    it('odds the same', () => {
      const result = service.getMultiplePotentialPayout({
        outcomes: [{
          price: { priceNum: 14, priceDen: 9 }
        }, {
          price: { priceNum: 3, priceDen: 4 }
        }]
      });
      expect(result).toEqual(4.472222222222221);
    });
  });

  it('isSinglesHasOldPrice', () => {
    expect(
      service.isSinglesHasOldPrice({
        Bet: {
          legs: [{
            parts: [{ outcome: { oldModifiedPrice: 1 } }]
          }]
        }
      })
    ).toBeTruthy();

    expect(
      service.isSinglesHasOldPrice({
        Bet: {
          legs: [{
            parts: [{ outcome: {} }]
          }]
        }
      })
    ).toBeFalsy();
  });

  describe('buildPotentialPayoutObj', () => {
    it('should build potential payout object', () => {
      expect(
        service.buildPotentialPayoutObj(1, 'frac', 2)
      ).toEqual(jasmine.any(Object));
      expect(
        service.buildPotentialPayoutObj(2, 'dec', 1)
      ).toEqual(jasmine.any(Object));
      expect(fracToDecService.decToFrac).toHaveBeenCalledTimes(1);
    });
    it('should build potential payout object for missed old price', () => {
      expect(
        service.buildPotentialPayoutObj(undefined, 'frac', 2)
      ).toEqual(jasmine.any(Object));
      expect(
        service.buildPotentialPayoutObj(undefined, 'dec', 1)
      ).toEqual(jasmine.any(Object));
      expect(fracToDecService.decToFrac).not.toHaveBeenCalled();
    });
  });

  it('getConfig should return cached config', fakeAsync(() => {
    service.betSlipConfigs = {};
    service.preventSystemCache = false;
    service.getConfig().subscribe();
    tick();
    expect(cmsServcie.getSystemConfig).not.toHaveBeenCalled();
  }));

  it('getConfig should return error', fakeAsync(() => {
    cmsServcie.getSystemConfig.and.returnValue(of(throwError('Error in Betslip.getConfig')));
    service.betSlipConfigs = {};
    service.preventSystemCache = false;
    service.getConfig().subscribe(null, (err) => expect(err).toBe('Error in Betslip.getConfig'));
    tick();
  }));

  it('updateLegsWithPriceChange', () => {
    const legs = [{
      winPlace: ''
    }, {
      winPlace: 'WIN'
    }, {
      winPlace: 'WIN',
      price: {}
    }, {
      winPlace: 'EACH_WAY',
      price: {
        num: 1, den: 2,
        props: {}
      },
      firstOutcomeId: 1
    }, {
      winPlace: 'WIN',
      price: {
        num: 3, den: 4,
        props: {}
      },
      firstOutcomeId: 2
    }];
    betslipDataService.betslipData = { legs };

    service.updateLegsWithPriceChange({ lp_num: 11, lp_den: 22 }, 1);
    service.updateLegsWithPriceChange({ lp_num: 3, lp_den: 4 }, 2);

    expect(legs[3].price.props).toEqual({ priceNum: 11, priceDen: 22 } as any);
    expect(legs[4].price.props).toEqual({});
  });

  describe('construct', () => {
    it('should construct build bet request', () => {
      betSelectionsService.data = [{}];
      service['construct']({});
      expect(betStakeService.construct).toHaveBeenCalledWith(jasmine.any(Object));
    });

    it('doc() should convert request to json element', () => {
      betStakeService.construct.and.returnValue({ doc: () => { } });

      const request = service['construct']({
        bets: [
          { stake: {} },
          { stake: { amount: 1 } },
          { stake: { freeBetAmount: 10 } }
        ]
      });
      request.doc();

      expect(clientUserAgentService.getId).toHaveBeenCalledWith(false, false);
      expect(bsDocService.el).toHaveBeenCalledWith('betslip', jasmine.any(Object), jasmine.any(Array));
      expect(bsDocService.el).toHaveBeenCalledWith('slipPlacement', jasmine.any(Object), jasmine.any(Array));
    });
  });

  it('getTotalAmount', () => {
    expect(
      service.getTotalAmount([
        { stake: {} },
        { stake: { amount: 1 } },
        { stake: { amount: 1 }, disabled: true }
      ])
    ).toBe('1.00');
  });

  it('getStoredBets', () => {
    const data = [];
    service.getStoredBets(data);
    expect(betslipDataService.storeBets).toHaveBeenCalledWith(data);
  });

  describe('getAccaOffer', () => {
    it('super acca disabled', fakeAsync(() => {
      cmsServcie.getSystemConfig.and.returnValue(of({
        Betslip: { superAcca: false }
      }));
      service.getAccaOffer({}).subscribe();
      tick();
      expect(accaService.getFreeBetOffer).not.toHaveBeenCalled();
    }));

    it('super acca enabled', fakeAsync(() => {
      cmsServcie.getSystemConfig.and.returnValue(of({
        Betslip: { superAcca: true }
      }));
      service.getAccaOffer({}).subscribe();
      tick();
      expect(sessionService.whenProxySession).toHaveBeenCalledTimes(1);
      expect(accaService.getFreeBetOffer).toHaveBeenCalledTimes(1);
    }));

    it('error', fakeAsync(() => {
      cmsServcie.getSystemConfig.and.returnValue(of({
        Betslip: { superAcca: true }
      }));
      sessionService.whenProxySession.and.returnValue(Promise.reject(null));
      service.getAccaOffer({}).subscribe(null, () => { });
      tick();
      expect(accaService.getFreeBetOffer).not.toHaveBeenCalled();
    }));
  });

  it('extendSelections', () => {
    betSelectionService.restoreSelections.and.returnValue([{ outcomes: [] }, { outcomes: [{}] }]);

    expect(service.extendSelections([]).length).toBe(1);

    expect(betslipStorageService.restore).toHaveBeenCalledTimes(1);
    expect(betSelectionService.restoreSelections).toHaveBeenCalledTimes(1);
    expect(betslipStorageService.store).toHaveBeenCalledTimes(1);
  });

  it('extendSelections for lotto', () => {
    betSelectionService.restoreSelections.and.returnValue([{isLotto:true}], {});

    expect(service.extendSelections([]).length).toBe(1);

    expect(betslipStorageService.restore).toHaveBeenCalledTimes(1);
    expect(betSelectionService.restoreSelections).toHaveBeenCalledTimes(1);
    expect(betslipStorageService.store).toHaveBeenCalledTimes(1);
  });

  describe('buildBetsRequest', () => {
    it('no legs', () => {
      service.buildBetsRequest([]);
      expect(bppService.send).not.toHaveBeenCalled();
    });

    it('bet placement error', fakeAsync(() => {
      bppService.send.and.returnValue(throwError(null));
      user.bppToken = 'blablabla';

      service.buildBetsRequest([{}]).subscribe();
      tick();

      expect(bppService.showErrorPopup).toHaveBeenCalledWith('betPlacementError');
    }));

    it('no bets with errors', fakeAsync(() => {
      bppService.send.and.returnValue(of({}));
      buildBetDocService.setResponse.and.returnValue({ bets: [] });

      service.buildBetsRequest([{}]).subscribe();
      tick();

      expect(bppService.send).toHaveBeenCalledTimes(1);
    }));

    it('some bets has errors (existing selections with errors)', fakeAsync(() => {
      bppService.send.and.returnValue(of({}));
      buildBetDocService.setResponse.and.returnValue({
        bets: [{
          errs: [{}], info: () => ({ outcomeId: '1' })
        }]
      });
      betSelectionsService.data = [{
        outcomes: [{ id: '1' }]
      }, {
        outcomes: [{ id: '2 ' }], errs: []
      }];

      service.buildBetsRequest([{}]).subscribe();
      tick();

      expect(bppService.send).toHaveBeenCalledTimes(1);
      expect(buildBetDocService.setResponse).toHaveBeenCalledTimes(1);
    }));

    it('some bets has errors (existing selections without errors)', fakeAsync(() => {
      bppService.send.and.returnValue(of({}));
      buildBetDocService.setResponse.and.returnValue({
        bets: [{
          errs: [{}], info: () => ({ outcomeId: '1' })
        }]
      });
      betSelectionsService.data = [{
        outcomes: [{ id: '1' }], errs: [{}]
      }];

      service.buildBetsRequest([{}]).subscribe();
      tick();

      expect(bppService.send).toHaveBeenCalledTimes(1);
      expect(legFactoryService.constructLegs).not.toHaveBeenCalled();
      expect(buildBetDocService.setResponse).toHaveBeenCalledTimes(1);
    }));

    it('second send request with error', fakeAsync(() => {
      let sendCount = 0;
      bppService.send.and.callFake(() => {
        sendCount += 1;
        return sendCount === 1 ? of({}) : throwError({});
      });
      buildBetDocService.setResponse.and.returnValue({
        bets: [{
          errs: [{}], info: () => ({ outcomeId: '1' })
        }]
      });
      betSelectionsService.data = [{
        outcomes: [{ id: '1' }]
      }, {
        outcomes: [{ id: '2 ' }], errs: []
      }];

      service.buildBetsRequest([{}]).subscribe();
      tick();

      expect(bppService.send).toHaveBeenCalledTimes(1);
      expect(buildBetDocService.setResponse).toHaveBeenCalledTimes(1);
    }));
  });

  it('filterNotRequestedScoreCast', () => {
    betSelectionsService.data = [
      { id: 'SCORECAST|1|2' }, { id: 'SGL|2' }
    ];

    const betslipData = {
      bets: [{
        info: () => ({
          combiName: 'SCORECAST',
          eventIds: { outcomeIds: [1, 2] }
        })
      }, {
        info: () => ({
          combiName: 'SCORECAST',
          eventIds: { outcomeIds: [1, 2] }
        })
      }, {
        info: () => ({})
      }]
    };

    service.filterNotRequestedScoreCast(betslipData);
  });

  it('filterNotRequestedScoreCast return if Lotto', () => {
    const betslipData = {
      bets: [ {isLotto: true}]
    };

    expect(service.filterNotRequestedScoreCast(betslipData)).toEqual(betslipData);
  });

  it('filterNotRequestedScoreCast return if Lotto', () => {
    const betslipData = {
      bets: []
    };
    expect(service.filterNotRequestedScoreCast(betslipData)).toEqual(betslipData);
  });

  describe('cleanDataSync', () => {
    it('clean data, set dafault and update counter', () => {
      service.cleanDataSync();
      expect(pubsub.publishSync).toHaveBeenCalledWith(pubSubApi.ADDTOBETSLIP_PROCESS_FINISHED);
      expect(betslipDataService.setDefault).toHaveBeenCalledTimes(1);
      expect(pubsub.publishSync).toHaveBeenCalledWith(pubSubApi.BETSLIP_COUNTER_UPDATE, 0);
    });

    it('should not set default and update counter', () => {
      toteBetSlipService.isToteBetPresent.and.returnValue(true);
      service.updating = true;

      service.cleanDataSync();

      expect(betslipDataService.setDefault).not.toHaveBeenCalled();
      expect(pubsub.publishSync).not.toHaveBeenCalledWith(pubSubApi.BETSLIP_COUNTER_UPDATE, 0);
    });
  });

  describe('getSuspendedMessage', () => {
    it('should getSuspendedMessage', () => {
      localeService.getString = jasmine.createSpy('getString');
      service.getSuspendedMessage(1);
      expect(localeService.getString).toHaveBeenCalledWith('bs.singleDisabled');
    });

    it('should getSuspendedMessage', () => {
      localeService.getString = jasmine.createSpy('getString');
      service.getSuspendedMessage(500);
      expect(localeService.getString).toHaveBeenCalledWith('bs.multipleDisabled');
    });
  });
  describe('updateAvailableFreeBetstest', () => {
    beforeEach(() => {

      fbService = {
        isBetPack: jasmine.createSpy('isBetPack'),
        isFanzone: jasmine.createSpy('isFanzone')
      }
      sessionStorageService = {
        get: jasmine.createSpy('get'),
        remove: jasmine.createSpy('remove')
      }
      service = new BetslipService(bsDocService, betSelectionService, betSelectionsService, betStakeService,
        legFactoryService, freeBetService, getSelectionDataService, bppService,
        placeBetDocService, buildBetDocService, cmsServcie, birService, localeService, deviceService, overAskService,
        accaService, sessionService, pubsub, fracToDecService, dialogService, toteBetSlipService,
        user, betslipDataService, betslipStorageService, awsService, dynamicComponentLoader, clientUserAgentService,
        gtmTrackingService, commandService, timeSyncService, nativeBridgeService, windowRefService, ssRequestHelper,
        storageService, fbService, lottoBuildBetDocService,fanzoneStorageService,sessionStorageService);

    });


    const betslipBets: any[] = [
      {
        disabled: false,
        Bet: { freeBets: [] },
        selectedFreeBet: { id: 2 },
      },
      {
        disabled: false,
        Bet: {},
        selectedFreeBet: { id: 2 },
      },
      {
        disabled: false,
        Bet: {
          freeBets: [
            {
              id: 3,
              freeBetValue: 1,
              freeBetExpireAt: 421,
              freeBetOfferCategories: {
                freebetOfferCategory: "Bet Pack4"
              },
            }, {
              id: 13,
              freeBetValue: 1,
              freeBetExpireAt: 501,
              freeBetOfferCategories: {
                freebetOfferCategory: "Bet Pack4"
              },
            }
          ]
        },
        selectedFreeBet: { id: 2 },
      }
      , {
        disabled: false,
        Bet: {
          freeBets: [
            {
              id: 4,
              freeBetValue: 1,
              freeBetExpireAt: 422,
              freeBetOfferCategories: {
                freebetOfferCategory: "Bet Pack"
              },
            }
          ]
        },
        selectedFreeBet: { id: 2 },
      },
      {
        disabled: false,
        Bet: {
          freeBets: [
            {
              id: 5,
              freeBetValue: 1,
              freeBetExpireAt: 422,
              freeBetOfferCategories: null
            }
          ]
        },
        selectedFreeBet: { id: 2 },
      }, {
        disabled: false,
        Bet: {
          freeBets: [
            {
              id: 5,
              freeBetValue: 1,
              freeBetExpireAt: 422,
              freeBetOfferCategories: {
                freebetOfferCategory: "Fanzone"
              }
            }
          ]
        },
        selectedFreeBet: { id: 2 },
      },
      {
        disabled: true,
        Bet: {
          freeBets: [
            {
              id: 4,
              freeBetValue: 1,
              freeBetExpireAt: 422,
              freeBetOfferCategories: {
                freebetOfferCategory: "Bet Pack"
              },
            }
          ]
        },
        selectedFreeBet: { id: 2 },
      },
      {
        disabled: true,
        Bet: {
          freeBets: [
            {
              id: 5,
              freeBetValue: 1,
              freeBetExpireAt: 422,
              freeBetOfferCategories: null
            }
          ]
        },
        selectedFreeBet: { id: 2 },
      },
      {
        disabled: true,
        Bet: {
          freeBets: [
            {
              id: 5,
              freeBetValue: 1,
              freeBetExpireAt: 422,
              freeBetOfferCategories: {
                freebetOfferCategory: "Fanzone"
              }
            }
          ]
        },
        selectedFreeBet: { id: 2 },
      }
    ];

    localeService = {
      getString: jasmine.createSpy('getString')
        .withArgs('bs.betPacks').and.returnValue('BetPacks')
        .withArgs('bs.fanZone').and.returnValue('Fanzone')
        .withArgs('bs.freeBets').and.returnValue('FreeBets')
    };
    it('should updateAvailableFreeBets', () => {
      fbService.isBetPack.and.returnValues(false, false, true, false, false, true, false, false);
      fbService.isFanzone.and.returnValues(false, false, false, false, true, false, false, true);
      service.updateAvailableFreeBets(betslipBets);
    });
    it(' filter and sort betdata', () => {
      const freelist: any[] = [
        { name: 'fb1', id: 1, freeBetExpireAt: 123 },
        { name: 'fb2', id: 2, freeBetExpireAt: 234, freeBetOfferCategories: { freebetOfferCategory: 'Fan Zone' } },
        { name: 'fb3', freeBetExpireAt: 345, id: '3', freeBetOfferCategories: { freebetOfferCategory: 'Fan Zone' } }
      ];
      fbService.isBetPack.and.returnValue(false);
      fbService.isFanzone.and.returnValue(true);
      service.filterAndSort(freelist, [1], 2);
      expect(service.filterAndSort(freelist, [], true)).not.toBe(freelist[0]);
    });
    it(' filter and sort betdata', () => {
      const betlist: any[] = [
        { name: 'fb1', id: 1, freeBetExpireAt: 123 },
        { name: 'fb2', id: 2, freeBetExpireAt: 234, freeBetOfferCategories: { freebetOfferCategory: 'BetPack' } },
      ];
      fbService.isBetPack.and.returnValue(true);
      service.filterAndSort(betlist, [1], 1);
      expect(service.filterAndSort(betlist, [], 1)).not.toBe(betlist[0]);
    });
    it(' filter and sort betdata', () => {
      const sortData: any[] = [
        { name: 'fb2', id: 2, freeBetExpireAt: 234, freebetOfferCategories: 'abc', freeBetOfferCategories: { freebetOfferCategory: 'OddsBoost' } },
        { name: 'fb3', freeBetExpireAt: 345, id: '3', freebetOfferCategories: 'abc', freeBetOfferCategories: { freebetOfferCategory: 'Bet Pack' } }
      ];
      fbService.isBetPack.and.returnValues(false, true);
      fbService.isFanzone.and.returnValue(false);
      service.filterAndSort(sortData, [1], 0);
      expect(service.filterAndSort(sortData, [], 0)).not.toBe(sortData[0]);
    });
  });
 
  describe('getOverlayLiveUpdateMessage', () => {
    let bet;

    beforeEach(() => {
      bet = {
        history: {
          isStarted: jasmine.createSpy('isStarted'),
          isSuspended: jasmine.createSpy('isSuspended'),
          isPriceChanged: jasmine.createSpy('isPriceChanged'),
          isPriceChangedAndMarketUnsuspended: jasmine.createSpy('isPriceChangedAndMarketUnsuspended')
        }
      };
    });

    it('event started', () => {
      localeService.getString = jasmine.createSpy('getString');
      bet.history.isStarted.and.returnValue(true);
      service.getOverlayLiveUpdateMessage(bet, false);
      expect(localeService.getString).toHaveBeenCalledWith('bs.EVENT_STARTED');
    });

    it('bet suspended', () => {
      betslipDataService.bets = [{
        info: () => ({ disabled: true })
      }];
      localeService.getString = jasmine.createSpy('getString');
      bet.history.isSuspended.and.returnValue(true);
      service.getOverlayLiveUpdateMessage(bet, false);
      expect(localeService.getString).toHaveBeenCalledWith('bs.singleDisabled');
    });

    it('price changed', () => {
      localeService.getString = jasmine.createSpy('getString');
      bet.history.isPriceChanged.and.returnValue(true);
      service.getOverlayLiveUpdateMessage(bet, false);
      expect(localeService.getString).toHaveBeenCalledWith('bs.priceChangeBannerMsg');
    });

    it('price changed (boost active)', () => {
      localeService.getString = jasmine.createSpy('getString');
      bet.history.isPriceChanged.and.returnValue(true);
      service.getOverlayLiveUpdateMessage(bet, true);
      expect(localeService.getString).toHaveBeenCalledWith('bs.reboostPriceChangeOverlayMsg');
    });

    it('price changed and market unsuspended', () => {
      localeService.getString = jasmine.createSpy('getString');
      bet.history.isPriceChangedAndMarketUnsuspended.and.returnValue(true);
      service.getOverlayLiveUpdateMessage(bet, false);
      expect(localeService.getString).toHaveBeenCalledWith('bs.priceChangeBannerMsg');
    });

    it('no message to show', () => {
      service.getOverlayLiveUpdateMessage(bet, false);
      expect(localeService.getString).not.toHaveBeenCalled();
    });
  });

  it('findBetForFreeBetTooltip', () => {
    let singles;
    let acca;
    let multiples;

    singles = [{ availableFreeBets: [{}] }];
    acca = [{ availableFreeBets: [{}] }];
    multiples = [{ availableFreeBets: [{}] }];
    service.findBetForFreeBetTooltip(singles, acca, multiples);
    expect(singles[0].freeBetTooltipAvailable).toBeTruthy();
    expect(acca[0].freeBetTooltipAvailable).toBeFalsy();
    expect(multiples[0].freeBetTooltipAvailable).toBeFalsy();

    singles = [{ availableFreeBets: [] }];
    acca = [{ availableFreeBets: [] }];
    multiples = [{ availableFreeBets: [] }];
    service.findBetForFreeBetTooltip(singles, acca, multiples);
    expect(singles[0].freeBetTooltipAvailable).toBeFalsy();
    expect(acca[0].freeBetTooltipAvailable).toBeFalsy();
    expect(multiples[0].freeBetTooltipAvailable).toBeFalsy();
  });

  describe('isSingleDisabled', () => {
    it('should return false if bet not disabled', () => {
      const bet = { disabled: false };
      overAskService.isInProcess = false;
      expect(service['isSingleDisabled'](bet as any)).toEqual(false);
    });

    it('should return false if overask is in progress', () => {
      const bet = { disabled: true };
      overAskService.isInProcess = true;
      expect(service['isSingleDisabled'](bet as any)).toEqual(false);
    });

    it('should return true if bet is disabled and overask is not in progress', () => {
      const bet = { disabled: true };
      overAskService.isInProcess = false;
      expect(service['isSingleDisabled'](bet as any)).toEqual(true);
    });
  });

  describe('#isFreeBetValid', () => {
    it('case when freebet amount / lines > 0.01', () => {
      const bet = {
        stake: {
          lines: 99
        }
      } as any;
      expect(service.isFreeBetValid(1, bet)).toEqual(true);
    });
    it('case when freebet amount / lines < 0.01', () => {
      const bet = {
        stake: {
          lines: 101
        }
      } as any;
      expect(service.isFreeBetValid(1, bet)).toEqual(false);

    });
    it('case when freebet amount / lines === 0.01', () => {
      const bet = {
        stake: {
          lines: 100
        }
      } as any;
      expect(service.isFreeBetValid(1, bet)).toEqual(true);
    });
  });

  it('updateSelectionLiveUpdateHistory', () => {
    betslipDataService.bets = [{
      history: {
        update: jasmine.createSpy('update')
      }
    }];
    service.updateSelectionLiveUpdateHistory(0, {} as any);
    expect(betslipDataService.bets[0].history.update).toHaveBeenCalledTimes(1);
  });

  describe('closeNativeBetslipAndWaitAnimation', () => {
    it('should close betslip and set timeout', () => {
      deviceService.isWrapper = true;
      service.closeNativeBetslipAndWaitAnimation(() => { });
      expect(pubsub.publish).toHaveBeenCalledWith('show-slide-out-betslip', false);
      expect(windowRefService.nativeWindow.setTimeout).toHaveBeenCalledWith(
        jasmine.any(Function), nativeBridgeService.betSlipCloseAnimationDuration);
    });

    it('should NOT close betslip and set timeout', () => {
      deviceService.isWrapper = false;
      service.closeNativeBetslipAndWaitAnimation(() => { });
      expect(pubsub.publish).not.toHaveBeenCalled();
      expect(windowRefService.nativeWindow.setTimeout).not.toHaveBeenCalled();
    });
  });

  it('isBetNotPermittedError', () => {
    const result = {
      errs: [{ errorDesc: 'This bet is not permitted for your account' }]
    };
    expect(service.isBetNotPermittedError(result)).toBeTruthy();
  });

  it('getBetNotPermittedError', () => {
    localeService.getString = jasmine.createSpy('getString');
    service.getBetNotPermittedError();
    expect(localeService.getString).toHaveBeenCalledWith('bs.BET_NOT_PERMITTED');
  });

  describe('handleNotAllowedBets', () => {
    it('should publish event', () => {
      betSelectionsService.count.and.returnValue(2);
      service['handleNotAllowedBets']({ errs: [{ desc: 'this bet is not permitted for your account' }] });
      expect(pubsub.publish).toHaveBeenCalledWith('BS_BET_NOT_ALLOWED');
    });

    it('should not publish event', () => {
      betSelectionsService.count.and.returnValue(1);
      service['handleNotAllowedBets']({ errs: [] });
      expect(pubsub.publish).not.toHaveBeenCalled();
    });
  });

  it('showBetslipLimitationPopup', fakeAsync(() => {
    service['showBetslipLimitationPopup']();
    tick();

    expect(dynamicComponentLoader.loadModule).toHaveBeenCalledWith(service['modulePath']);
    expect(dialogService.openDialog).toHaveBeenCalledWith(
      'betslipLimitationDialog', jasmine.any(Object), true
    );
  }));

  describe('updateEWFlagInStoredSelection', () => {
    it('should update EW flag value when outcomes matches', () => {
      betSelectionsService.data = [{
        id: '1',
        price: { priceType: 'SP' },
        details: {
          info: {
            sportId: '21'
          }
        },
        outcomes: [{ id: 1 }]
      }] as any;
      const buildBetResponseData = {
        bets: [{ id: '1234', eachWayAvailable: 'Y', betTypeRef: { id: 'SGL' }, legRef: [{ documentId: 1 }] }], 
        outcomeDetails: [ { id: 1, categoryId: '21' }], 
        legs: [{
          documentId: 1,
          sportsLeg: {
            legPart: [{
              outcomeRef: { id: 1 }
            }]
          }
        }, {
          documentId: 2,
          sportsLeg: {
            legPart: [{
              outcomeRef: { id: 2 }
            }]
          }
        }]
      } as any;
      const storedSelections = [{ outcomesIds: [1, 2],  details: { id: '123', isEachWayAvailable: false }}];
      service.updateEWFlagInStoredSelection(buildBetResponseData);
      expect(betslipStorageService.store).toHaveBeenCalled();
    });
    it('legRef as null', () => {
      betSelectionsService.data = [{
        id: '1',
        price: { priceType: 'SP' },
        details: {
          info: {
            sportId: '21'
          }
        },
        outcomes: [{ id: 1 }]
      }] as any;
      const buildBetResponseData = {
        bets: [{ id: '1234', eachWayAvailable: 'Y', betTypeRef: { id: 'SGL' }, legRef: null }], 
        outcomeDetails: [ { id: 1, categoryId: '21' }], 
        legs: [{
          documentId: 1,
          sportsLeg: {
            legPart: [{
              outcomeRef: { id: 1 }
            }]
          }
        }, {
          documentId: 2,
          sportsLeg: {
            legPart: [{
              outcomeRef: { id: 2 }
            }]
          }
        }]
      } as any;
      const storedSelections = [{ outcomesIds: [1, 2],  details: { id: '123', isEachWayAvailable: false }}];
      service.updateEWFlagInStoredSelection(buildBetResponseData);
      expect(betslipStorageService.store).not.toHaveBeenCalled();
    });
    it('selection as null', () => {
      betSelectionsService.data = [ null ] as any;
      const buildBetResponseData = {} as any;
      service.updateEWFlagInStoredSelection(buildBetResponseData);
      expect(betslipStorageService.store).not.toHaveBeenCalled();
    });
    it('selection details as null', () => {
      betSelectionsService.data = [{ 
        id: '1',
        price: { priceType: 'SP' },
        details: null,
        outcomes: [{ id: 1 }]
       }] as any;
      const buildBetResponseData = {} as any;
      service.updateEWFlagInStoredSelection(buildBetResponseData);
      expect(betslipStorageService.store).not.toHaveBeenCalled();
    });
    it('selection outcomes as null', () => {
      betSelectionsService.data = [{ 
        id: '1',
        price: { priceType: 'SP' },
        details: {
          info: {
            sportId: '21'
          }
        },
        outcomes: null
       }] as any;
      const buildBetResponseData = {} as any;
      service.updateEWFlagInStoredSelection(buildBetResponseData);
      expect(betslipStorageService.store).not.toHaveBeenCalled();
    });
    it('buildBetResponseData outcomeDetails as null', () => {
      betSelectionsService.data = [{
        id: '1',
        price: { priceType: 'SP' },
        details: {
          info: {
            sportId: '21'
          }
        },
        outcomes: [{ id: 1 }]
      }] as any;
      const buildBetResponseData = {
        bets: [{ id: '1234', eachWayAvailable: 'Y', betTypeRef: { id: 'SGL' }, legRef: [{ documentId: 1 }] }], 
        outcomeDetails: null, 
        legs: [{
          documentId: 1,
          sportsLeg: {
            legPart: [{
              outcomeRef: { id: 1 }
            }]
          }
        }, {
          documentId: 2,
          sportsLeg: {
            legPart: [{
              outcomeRef: { id: 2 }
            }]
          }
        }]
      } as any;
      service.updateEWFlagInStoredSelection(buildBetResponseData);
      expect(betslipStorageService.store).not.toHaveBeenCalled();
    });
    it('outcome as null', () => {
      betSelectionsService.data = [{
        id: '1',
        price: { priceType: 'SP' },
        details: {
          info: {
            sportId: '21'
          }
        },
        outcomes: [{ id: 3 }]
      }] as any;
      const buildBetResponseData = {
        bets: [{ id: '1234', eachWayAvailable: 'Y', betTypeRef: { id: 'SGL' }, legRef: [{ documentId: 1 }] }], 
        outcomeDetails: [ { id: 1, categoryId: '21' }], 
        legs: null
      } as any;
      service.updateEWFlagInStoredSelection(buildBetResponseData);
      expect(betslipStorageService.store).not.toHaveBeenCalled();
    });
    it('legs as null', () => {
      betSelectionsService.data = [{
        id: '1',
        price: { priceType: 'SP' },
        details: {
          info: {
            sportId: '21'
          }
        },
        outcomes: [{ id: 1 }]
      }] as any;
      const buildBetResponseData = {
        bets: [{ id: '1234', eachWayAvailable: 'Y', betTypeRef: { id: 'SGL' }, legRef: [{ documentId: 1 }] }], 
        outcomeDetails: [{ id: 1, categoryId: '21' }], 
        legs: null
      } as any;
      service.updateEWFlagInStoredSelection(buildBetResponseData);
      expect(betslipStorageService.store).not.toHaveBeenCalled();
    });
    it('leg as null', () => {
      betSelectionsService.data = [{
        id: '1',
        price: { priceType: 'SP' },
        details: {
          info: {
            sportId: '21'
          }
        },
        outcomes: [{ id: 1 }]
      }] as any;
      const buildBetResponseData = {
        bets: [{ id: '1234', eachWayAvailable: 'Y', betTypeRef: { id: 'SGL' }, legRef: [{ documentId: 1 }] }], 
        outcomeDetails: [{ id: 1, categoryId: '21' }], 
        legs: [ null ]
      } as any;
      service.updateEWFlagInStoredSelection(buildBetResponseData);
      expect(betslipStorageService.store).not.toHaveBeenCalled();
    });
    it('bets as null', () => {
      betSelectionsService.data = [{
        id: '1',
        price: { priceType: 'SP' },
        details: {
          info: {
            sportId: '21'
          }
        },
        outcomes: [{ id: 1 }]
      }] as any;
      const buildBetResponseData = {
        bets: null, 
        outcomeDetails: [{ id: 1, categoryId: '21' }, { id: 2, categoryId: '21' }], 
        legs: [{
          documentId: 1,
          sportsLeg: {
            legPart: [{
              outcomeRef: { id: 1 }
            }]
          }
        }]
      } as any;
      service.updateEWFlagInStoredSelection(buildBetResponseData);
      expect(betslipStorageService.store).not.toHaveBeenCalled();
    });
    it('legPart object as null', () => {
      betSelectionsService.data = [{
        id: '1',
        price: { priceType: 'SP' },
        details: {
          info: {
            sportId: '21'
          }
        },
        outcomes: [{ id: 1 }]
      }] as any;
      const buildBetResponseData = {
        bets: null, 
        outcomeDetails: [{ id: 1, categoryId: '21' }, { id: 2, categoryId: '21' }], 
        legs: [{
          documentId: 1,
          sportsLeg: {
            legPart: [null]
          }
        }]
      } as any;
      service.updateEWFlagInStoredSelection(buildBetResponseData);
      expect(betslipStorageService.store).not.toHaveBeenCalled();
    });
    it('bet as null', () => {
      betSelectionsService.data = [{
        id: '1',
        price: { priceType: 'SP' },
        details: {
          info: {
            sportId: '21'
          }
        },
        outcomes: [{ id: 1 }]
      }] as any;
      const buildBetResponseData = {
        bets: [ null, { betTypeRef: null } ], 
        outcomeDetails: [{ id: 1, categoryId: '21' }, { id: 2, categoryId: '21' }], 
        legs: [{
          documentId: 1,
          sportsLeg: {
            legPart: [{
              outcomeRef: { id: 1 }
            }]
          }
        }]
      } as any;
      service.updateEWFlagInStoredSelection(buildBetResponseData);
      expect(betslipStorageService.store).not.toHaveBeenCalled();
    });
  });

  it('isPriceTypeToggling', () => {
    betSelectionsService.data = [{id: 'SGL|1|2'}];
    expect(service.isPriceTypeToggling({isLotto: true, id: 'SGL|1|2'})).toEqual({id: 'SGL|1|2'})
  });

  it('should filter lotto betData', () => {
    const data = [{accaBets:[{stake:''}]}];
    const responseData = service['filterByLottoStake'](data as any);
    expect(responseData.length).toEqual(0);
  });
  describe('betkeyBoardData',()=>{
    const data=['All_single_quickStake-00000','singlestake-000000']
    it('set BetKeyBoard Data',()=>{
      service.betKeyboardData='All_single_quickStake-00000'
      expect(service['_betKeyboardData']).toEqual(['All_single_quickStake-00000','singlestake-00000']);
  
    })
    it('get BetKeyBoard Data',()=>{
      service['_betKeyboardData']=data
      expect(service.betKeyboardData).toEqual(['All_single_quickStake-00000','singlestake-000000']);
    });
    it('get BetKeyBoard Data nodata',()=>{
      service['_betKeyboardData']=[]
      expect(service.betKeyboardData).toEqual([]);
    });
    it('get BetKeyBoard Data storage ',()=>{
      storageService.get = jasmine.createSpy().and.returnValue(['All_single_quickStake-00000','singlestake-00000']);
      service['_betKeyboardData']=[]
      expect(service.betKeyboardData).toEqual(['All_single_quickStake-00000','singlestake-00000']);
  
    });
    it('get BetKeyBoard Data storage ',()=>{
      service['_betKeyboardData']=data
      service.filterKyeBoardData='singlestake-000000'
      expect(service.betKeyboardData).toEqual(['All_single_quickStake-00000']);
  
    });
  });
});
