import { fakeAsync, tick } from '@angular/core/testing';
import { RacingMyBetsComponent } from './racing-mybets.component';
import { eventMock } from '@app/racing/components/racingEventComponent/racing-event.component.mock';
import { horseracingConfig } from '@core/services/racing/config/horseracing.config';
import { of } from 'rxjs';

describe('RacingMybetsComponent', () => {
  let component: RacingMyBetsComponent;
  let windowRef;
  let timeService;
  let pubSubService;
  let nativeBridgeService;
  let ukToteService;
  let lpAvailabilityService;
  let deviceService;
  let gtmService;
  let streamTrackingService;
  let dialogService;
  let filterService;
  let localeService;
  let horseracing;
  let routingHelperService;
  let cmsService;
  let tools;
  let sbFilters;
  let router;
  let location;
  let sortByOptionsService;
  let eventEntity;
  let route;
  let pools;
  let changeDetectorRef;
  let watchRulesService;
  let seoDataService;
  let elementRef;
  let racingGaService;
  let commandService;
  let cashOutMapService;
  let CashoutWsConnectorService;
  let userService;
  let raceDataMock;
  let storageService,
  pubSubResp: string; 
  const placedBets = [
    { id: 11 },
    { id: 2, settled: 'Y' },
    { id: 3, cashoutStatus: 'BET_CASHED_OUT' },
    { id: 4, settled: 'Y', cashoutStatus: 'BET_CASHED_OUT' }
  ], 
  betsData = { placedBets: placedBets, cashoutIds: [] };
  beforeEach(() => {
    raceDataMock = [
      {
        id: 123,
        markets: [
          {
            id: '12345',
            outcomes: []
          }
        ],
        categoryId: 9337,
        typeId: 2031
      }
    ];
    pubSubResp = 'price';
    pubSubService = {
      API: {
        PIN_TOP_BAR: 'PIN_TOP_BAR',
        CLOSE_SORT_BY: 'CLOSE_SORT_BY',
        SORT_BY_OPTION: 'SORT_BY_OPTION',
        LIVE_MARKET_FOR_EDP: 'LIVE_MARKET_FOR_EDP',
        IS_NATIVE_VIDEO_STICKED: 'IS_NATIVE_VIDEO_STICKED',
        HAS_MARKET_DESCRIPTION: 'HAS_MARKET_DESCRIPTION',
        SUCCESSFUL_LOGIN: 'SUCCESSFUL_LOGIN',
        BET_PLACED: 'BET_PLACED', 
        EDIT_MY_ACCA: 'EDIT_MY_ACCA',
        EMA_UNSAVED_ON_EDP: 'EMA_UNSAVED_ON_EDP',
        CASH_OUT_BET_PROCESSED: 'CASH_OUT_BET_PROCESSED',
        UPDATE_CASHOUT_BET: 'UPDATE_CASHOUT_BET',
        MY_BETS_UPDATED: 'MY_BETS_UPDATED',
        MY_BET_PLACED: 'MY_BET_PLACED',
      },
      subscribe: jasmine.createSpy('subscribe').and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
        if (channel === 'HAS_MARKET_DESCRIPTION') {
          channelFunction(true);
        } else if (channel === 'CASH_OUT_BET_PROCESSED'){
          channelFunction(1);
        } else if (channel === 'MY_BET_PLACED'){
          channelFunction({bets: null});
        } else if (channel === 'UPDATE_CASHOUT_BET'){
          channelFunction({cashoutStatus: 'BET_SETTLED', betId: '1'});
        } else {
          channelFunction(pubSubResp);
        }
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish')
    };
    windowRef = {
      nativeWindow: {
        setInterval: jasmine.createSpy().and.callFake((fn, timer) => fn && fn()),
        clearInterval: jasmine.createSpy(),
        document: {
          querySelector: jasmine.createSpy().and.returnValue({
            style: {},
            offsetHeight: 123
          }),
          getElementById: jasmine.createSpy().and.returnValue({
            offsetWidth: 123
          }),
          addEventListener: jasmine.createSpy(),
          removeEventListener: jasmine.createSpy()
        },
        scrollTo: jasmine.createSpy(),
        requestAnimationFrame: jasmine.createSpy('requestAnimationFrame')
      }
    };
    
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('test_string')
    };

    gtmService = {
      push: jasmine.createSpy('push')
    };

    storageService = {
      set: jasmine.createSpy('set'),
      get: jasmine.createSpy('get').and.returnValue([{"eventId":"11","betIds":[3]},{"eventId":"2","betIds":[4]}])

    };

    commandService = {
      API: {
        GET_PLACED_BETS_ASYNC: 'GET_PLACED_BETS_ASYNC',
        GET_CASH_OUT_BETS_ASYNC: 'GET_CASH_OUT_BETS_ASYNC',
        GET_BETS_FOR_EVENT_ASYNC: 'GET_BETS_FOR_EVENT_ASYNC',
        OPEN_CASHOUT_STREAM: 'OPEN_CASHOUT_STREAM'
      },
      executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve(placedBets))
    };

    cashOutMapService = {
      createCashoutBetsMap: jasmine.createSpy('createCashoutBetsMap')
    };

    CashoutWsConnectorService = {
      getConnection: jasmine.createSpy('getConnection'),
      dateChangeBet: jasmine.createSpy('dateChangeBet')
    };

    userService = {
      status: true,
      currency: 'USD',
      currencySymbol: '$'
    };

    commandService.executeAsync.and.callFake(key => {
      if (key === 'GET_PLACED_BETS_ASYNC'|| key === 'OPEN_CASHOUT_STREAM') {
        return Promise.resolve(placedBets);
      } else if (key === 'GET_BETS_FOR_EVENT_ASYNC') {
        return Promise.resolve(betsData);
      }
    });
    
    changeDetectorRef = {
      detach: jasmine.createSpy(),
      detectChanges: jasmine.createSpy()
    };
    
    
    createComponent();
  
    component.eventEntity = Object.assign({}, eventMock);
    component.sportName = 'horseracing';
    component.selectedTypeName = 'selectedTypeName_string';
    component['config'] = horseracingConfig;
    component.racingTypeNames = ['racingTypeNames_string', 'racingTypeNames_string2'];
    component.racingInMeeting = [component.eventEntity];
    component.presimStopTrackInterval = 100;
    component.filter = 'filter_string';
    component.eventId = 11;
    component.images = 'images_string';
    component.onExpand = jasmine.any(Function) as any;
    component.streamControl = {
      externalControl: true,
      playLiveSim: jasmine.createSpy('playLiveSim'),
      playStream: jasmine.createSpy('playStream'),
      hideStream: jasmine.createSpy('hideStream'),
    };
    component.nativeVideoPlayerPlaceholderRef = { nativeElement: { className: 'native-video-player-placeholder'} };
    component['cashoutIds'] = <any>[{ id: 'i1' }, { id: 'i2' }];
    component['placedBets'] = <any>[{ betId: 'i1', leg: [{sportsLeg: {legPart: [{outcomeRef: {eventId: eventMock.id.toString()}}]}}] }, { betId: 'i2', leg: [{sportsLeg: {legPart: [{outcomeRef: {eventId: eventMock.id.toString()}}]}}] }];
    component['isLoggedIn'] = true;
  });
  function createComponent() {
      component = new RacingMyBetsComponent(
        windowRef,
        timeService,
        pubSubService,
        nativeBridgeService,
        ukToteService,
        lpAvailabilityService,
        deviceService,
        gtmService,
        streamTrackingService,
        dialogService,
        filterService,
        localeService,
        horseracing,
        routingHelperService,
        cmsService,
        tools,
        sbFilters,
        router,
        location,
        changeDetectorRef,
        sortByOptionsService,
        route,
        watchRulesService,
        seoDataService,
        elementRef,
        racingGaService,
        commandService,
        cashOutMapService,
        userService,
        CashoutWsConnectorService,
        storageService
      );
      (component['_raceData'] as any) = raceDataMock;
    }
    describe('ngOninit', () => {
      it('ngOnInit', () => {
        component.events = [{id: 1}, {id: 2}] as any;
        spyOn<any>(component, 'initiateCashoutBets');
        spyOn<any>(component, 'addListeners');
        component.ngOnInit();
        expect(component['initiateCashoutBets']).toHaveBeenCalled();
        expect(component['addListeners']).toHaveBeenCalled();
        expect(component['raceCardEventIds']).toEqual([1,2]);
      });

      it('ngOnInit - BYB', () => {
        component.isRaceCard = true;
        spyOn<any>(component, 'initiateCashoutBets');
        spyOn<any>(component, 'addListeners');
        component.ngOnInit();
        expect(component['initiateCashoutBets']).toHaveBeenCalled();
        expect(component['addListeners']).toHaveBeenCalled();
        expect(component['tagName']).toBe('BuildRaceCardComponent');
      });

      it('ngOnInit-load from storage when event id is defined', () => {
        component['raceCardEventIds'] = undefined;
        spyOn<any>(component, 'addListeners');
        component.ngOnInit();
        expect(component['showSignPosting']).toEqual(true);    
      });

      it('ngOnInit-load from storage when event id is unDefined', () => {
        component.events = [{id: 1}, {id: 22}] as any;
        component.eventId = undefined;
        spyOn<any>(component, 'addListeners');
        component.ngOnInit();
        expect(component['showSignPosting']).toEqual(false);    
      });
    });
    describe('ngOnDestroy', () => {
      it('ngOnDestroy', () => {
        spyOn<any>(component, 'closeCashoutStream');
        component.ngOnDestroy();
        expect(component['closeCashoutStream']).toHaveBeenCalled();
      });
    });
    describe('edp page in HR', () => {
      it('QUICKBET placed', () => {
        component.eventId = 11;
        spyOn<any>(component, 'initiateCashoutBets').and.callThrough();
        pubSubService.subscribe.and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
          if (channel === 'MY_BET_PLACED'){
            channelFunction({isquickbet: false, bets:[{ id: 4, settled: 'Y', cashoutStatus: 'BET_CASHED_OUT', type: '', leg: [ {'part':[{eventId: "11","betIds":[3]}]}] }]});
          } else if (channel === 'CASH_OUT_BET_PROCESSED') {
            channelFunction(1);
          } else if (channel === 'EDIT_MY_ACCA') {
            channelFunction();
          } else if (channel === 'EMA_UNSAVED_ON_EDP') {
            channelFunction(true);
          } else if (channel === 'SUCCESSFUL_LOGIN'){
            channelFunction();
          } else if (channel === 'UPDATE_CASHOUT_BET'){
            channelFunction({cashoutStatus: 'BET_SETTLED', betId: '1'});
          } 
        });
        component['addListeners']();
        expect(component['initiateCashoutBets']).toHaveBeenCalled();
      });
      
      it('bet BET_CASHED_OUT subscribed to UPDATE_CASHOUT_BET', () => {
        spyOn<any>(component, 'updateBets').and.callThrough();
        const bet = {
          betId: '1',
          cashoutStatus: 'BET_CASHED_OUT'
        }

        pubSubService.subscribe.and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
          if (channel === pubSubService.API.UPDATE_CASHOUT_BET){
            channelFunction(bet);
          }
        });
        component['subscribeForCashoutUpdates']();
        
        expect(component['updateBets']).toHaveBeenCalled();
      });

      it('bet BET_CASHED_OUT and show signposting false', () => {
        spyOn<any>(component, 'updateBets').and.callThrough();
        const bet = {
          betId: '1',
          cashoutStatus: 'BET_CASHED_OUT'
        }
        component['placedBets'] = [
          { id: 11, settled: 'N', cashoutStatus: 'BET_CASHED_IN', type: '', leg: [1,3,4,11] }
        ] as any;
        pubSubService.subscribe.and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
          if (channel === pubSubService.API.UPDATE_CASHOUT_BET){
            channelFunction(bet);
          }
        });
        component['subscribeForCashoutUpdates']();
        
        expect(component['updateBets']).toHaveBeenCalled();
      });

      it('bet BET_CASHED_OUT and show signposting true', () => {
        spyOn<any>(component, 'updateBets').and.callThrough();
        const bet = {
          betId: '1',
          cashoutStatus: 'BET_CASHED_OUT'
        }
        component['placedBets'] = [
          { id: 11, settled: 'N', cashoutStatus: 'BET_CASHED_IN', type: '', leg: [1,3,4,11] },
          { id: 6, settled: 'N', cashoutStatus: 'BET_CASHED_IN', type: '', leg: [1,3,4,7] }
        ] as any;
        pubSubService.subscribe.and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
          if (channel === pubSubService.API.UPDATE_CASHOUT_BET){
            channelFunction(bet);
          }
        });
        component['subscribeForCashoutUpdates']();
        
        expect(component['updateBets']).toHaveBeenCalled();
      });
  
      it('bet placed from betslip', () => {
        const placedBet = <any>{bets: [{ id: 4, settled: 'Y', cashoutStatus: 'BET_CASHED_OUT', type: '', leg: [ {'part':[{eventId: "11"}]}] }]};
        userService.status = true;
        component.eventId = 12345;
        spyOn<any>(component, 'initiateCashoutBets').and.callThrough();
        pubSubService.subscribe.and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
          if (channel === 'MY_BET_PLACED'){
            channelFunction(placedBet);
          } else if (channel === 'SUCCESSFUL_LOGIN'){
            channelFunction();
          }
        });
        component['addListeners']();
        expect(component['initiateCashoutBets']).toHaveBeenCalled();
      });

      it('bet placed from betslip when quick bet is true', () => {
        component['placedBet'] = <any>{bets: [{leg: [{sportsLeg: {legPart: [{outcomeRef: {eventId: eventMock.id.toString()}}]}}]}]};
        userService.status = true;
        component.eventId = 12345;
        component.isRaceCard = true;
        spyOn<any>(component, 'initiateCashoutBets').and.callThrough();
        pubSubService.subscribe.and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
          if (channel === 'MY_BET_PLACED'){
             
            channelFunction({isquickbet: true, id : 11,bets:[{ id: '1', leg: [{sportsLeg: {legPart: [{outcomeRef: {eventId: eventMock.id.toString()}}]}}] }]});
          } else if (channel === 'SUCCESSFUL_LOGIN'){
            channelFunction();
          }
        });
        component['addListeners']();
        expect(component['initiateCashoutBets']).toHaveBeenCalled();
      });
      
      it('bet placed from betslip - BYB - with same event bet placed', () => {
        component.isRaceCard = true;
        component.events = [{id: 1}, {id: eventMock.id}] as any;
        const placedBet = <any>{bets: [{ id: 4, settled: 'Y', cashoutStatus: 'BET_CASHED_OUT', type: '', leg: [ {'part':[{eventId: "11"}]}] }]};
        spyOn<any>(component, 'initiateCashoutBets').and.callThrough();
        pubSubService.subscribe.and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
          if (channel === 'MY_BET_PLACED'){
            channelFunction(placedBet);
          } else if (channel === 'SUCCESSFUL_LOGIN'){
            channelFunction();
          }
        });
        component['addListeners']();
        expect(component['initiateCashoutBets']).toHaveBeenCalled();
      });

      it('bet placed from betslip - BYB - with diff. event bet placed', () => {
        component.isRaceCard = true;
        component.events = [{id: 1}] as any;
        const placedBet = <any>{bets: [{ id: 4, settled: 'Y', cashoutStatus: 'BET_CASHED_OUT', type: '', leg: [ {'part':[{eventId: "11"}]}] }]};
        spyOn<any>(component, 'initiateCashoutBets').and.callThrough();
        pubSubService.subscribe.and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
          if (channel === 'MY_BET_PLACED'){
            channelFunction(placedBet);
          }
        });
        component['addListeners']();
        expect(component['initiateCashoutBets']).not.toHaveBeenCalled();
      });
  
      it('initiateCashoutBets with empty placed bets', fakeAsync(() => {
        spyOn<any>(component, 'closeCashoutStream').and.callThrough();
        commandService.executeAsync.and.callFake(key => {
            return Promise.resolve(null);
        });
        component['initiateCashoutBets']();
        tick();
        expect(component['closeCashoutStream']).toHaveBeenCalled();
      }));
  
      it('updateBetsDetails with no bets', () => {
        spyOn<any>(component, 'closeCashoutStream').and.callThrough();
        spyOn<any>(component, 'setActiveUserTab').and.callThrough();
        component['placedBets'] = [];
        component['activeUserTab'] = component['HR_TABS'].MYBETS;
        component['updateBetsDetails']();
        expect(component['myBetsAvailable']).toBeFalse();
        expect(component['closeCashoutStream']).toHaveBeenCalled();
        expect(component['setActiveUserTab']).toHaveBeenCalled()
      });
  
      it('should unsubscribe from cashout data subscription', () => {
        component['cashoutDataSubscription'] = jasmine.createSpyObj('cashoutDataSubscription', ['unsubscribe']);
        component['betsStreamOpened'] = true;
        component['closeCashoutStream']();
        expect(component['cashoutDataSubscription'].unsubscribe).toHaveBeenCalled();
        expect(commandService.executeAsync).toHaveBeenCalledWith(commandService.API.CLOSE_CASHOUT_STREAM);
        expect(component['betsStreamOpened']).toBeFalse();
      });
  
      it('should open cancel EMA popup', () => {
        component['editMyAccaUnsavedOnEdp'] = true;
        component['setActiveUserTab']('');
        expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.EMA_OPEN_CANCEL_DIALOG);
      });
  
      it('shoud set active tab and push GTM event', () => {
        component['eventEntity'] = <any>{
          id: 555,
          typeID: 1,
          categoryID: "21"
        };
        component['myBetsTabLabel'] = "My Bets(1)";
        component['editMyAccaUnsavedOnEdp'] = false;
        component['setActiveUserTab']('myBets');
        expect(component['activeUserTab']).toBe('myBets');
        expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
          eventAction: "race card",
          eventCategory: "horse racing",
          eventLabel: "My Bets(1)",
          categoryID: component.eventEntity.categoryId,
          typeID: component.eventEntity.typeId,
          eventID: component.eventEntity.id,
        });
      });
      it('should not push any gtm object if tabName is not Mybets', () => {
        component['eventEntity'] = <any>{
          id: 555,
          typeID: 1,
          categoryID: "21"
        }
        component['myBetsTabLabel'] = "My Bets(1)";
        component['setActiveUserTab']('markets');
        expect(gtmService.push).not.toHaveBeenCalledWith('trackEvent', {
          eventAction: "race card",
          eventCategory: "horse racing",
          eventLabel: "My Bets(1)",
          categoryID: component.eventEntity.categoryId,
          typeID: component.eventEntity.typeId,
          eventID: component.eventEntity.id,
        });
      });
  
      it('myBetsTabName with counter 0 ', () => {
        const tabName = component['myBetsTabName'](0);
        expect(tabName).toBe('test_string');
      });

      it('setPlacedBets - BYB', fakeAsync(() => {
        component.eventId = undefined;
        spyOn<any>(component, 'setPlacedBets').and.callThrough();
        component['raceCardEventIds'] = [1,2];
        component['initiateCashoutBets']();
        tick();
        expect(component['commandService'].executeAsync).toHaveBeenCalledWith(component['commandService'].API.GET_PLACED_BETS_ASYNC, ['1,2'], []);
        expect(component['setPlacedBets']).toHaveBeenCalled();
      }));
    }); 
    describe('@isMarketsTabAvailable', () => {
        it(`should return True if 'isLoggedIn' and 'myBetsAvailable are equal true`, () => {
          component['isLoggedIn'] = true;
          component['myBetsAvailable'] = true;

          expect(component['isMarketsTabAvailable']()).toBeTruthy();
        });

        it(`should return False if 'isLoggedIn' is equal false`, () => {
          component['isLoggedIn'] = false;
          component['myBetsAvailable'] = true;

          expect(component['isMarketsTabAvailable']()).toBeFalsy();
        });

        it(`should return False if 'myBetsAvailable' is equal false`, () => {
          component['isLoggedIn'] = true;
          component['myBetsAvailable'] = false;

          expect(component['isMarketsTabAvailable']()).toBeFalsy();
        });
    });

    it(`should call getFilteredBets()`, () => {
      component['placedBets'] = [
        { id: 4, settled: 'Y', cashoutStatus: 'BET_CASHED_OUT', type: '', leg: [1,2,3,4] }
      ] as any;
      component.eventId = 12;
      expect(component['getFilteredBets']().length).toEqual(0);
    });

    it(`should call getFilteredBets() when isRaceCard true`, () => {
      component['placedBets'] = [
        { id: 4, settled: 'N', cashoutStatus: 'BET_CASHED_IN', type: '', leg: [1,2,3,4] }
      ] as any;
      component.eventId = 12;
      component.isRaceCard = true;
      component['raceCardEventIds'] = [1,2];
      expect(component['getFilteredBets']().length).toEqual(1);
    });

    it(`should call showMybetTab()`, () => {
      component['placedBets'] = [
        { id: 4, settled: 'Y', cashoutStatus: 'BET_CASHED_OUT', type: '', leg: [1,2,3,4] }
      ] as any;
      component.eventId = 12;
      component.activeUserTab = 'myBets';
      component['showMybetTab']();
      expect(component.myBetsCounter).toEqual(0);
      
    });
    
    it(`Should call updatecashout data for Local storage`, () => {
      const localstrMock = [{"eventId":"11","betIds":[3]},{"eventId":"2","betIds":[4]}];
      storageService = {
        set: jasmine.createSpy('storageService.set'),
        get: jasmine.createSpy('storageService.get').and.returnValue(localstrMock),
      };
      component.eventId = 11;
      component['placedBets'] = [
        { id: 11, settled: 'N', cashoutStatus: 'BET_CASHED_IN', type: '', leg: [1,3,4,11] }
      ] as any;
      component['updateCashoutData']();
      expect(component['showSignPosting']).toEqual(false);  
    });

    it(`Should call updatecashout when event id is undefined`, () => {
      component.isRaceCard = true;
      component.events = [{id: 1}] as any;
      component.eventId = undefined;
      component['raceCardEventIds'] = [11,22];
      component['updateCashoutData']();
      expect(component['showSignPosting']).toEqual(false);  
    });

    it(`should call updateCashoutBets()`, () => {
      expect(component['updateCashoutBets']('test' as any, '1')).toBeUndefined();
      component['placedBets'] = [
        { id: 4, betId: '4', settled: 'Y', cashoutStatus: 'BET_CASHED_OUT', type: '', leg: [1,2,3,4] }
      ] as any;
      component['updateCashoutBets'](component['placedBets'], '4');
      expect(component['placedBets'][0].type).toEqual('placedBetsWithoutCashoutPossibility');

    });
    describe('should call updateCashoutData', () => {
      it('should call updateCashoutData', () => {
        component['placedBets'] = [];
        expect(component['updateCashoutData']()).toBeUndefined();
      });
    });
    describe('should call updateBets', () => {
      it('should call updateBets when placedBets undefined', () => {
        component['placedBets'] = undefined;
        component['updateBets']('1');
        expect(component['myBetsAvailable']).toBeFalse();
      });
    });
    describe("updateCashoutData", ()=>{
      it('should call updateCashoutData when isTempBetsAvailable length zero', () => {
        component.cashoutBets = null;
        component.tempBets = null;
        expect(component.updateCashoutData()).toBeUndefined();
      });
      it('should call updateCashoutData when isTempBetsAvailable length > zero', () => {
        component.cashoutBets = null;
        component.tempBets = [{ betId: 'i2', id: '2', leg: ['2'] }, { betId: 'i3', id: '3', leg: ['3'] }];
        CashoutWsConnectorService.getConnection.and.returnValue(false);
        component.updateCashoutData();
        expect(CashoutWsConnectorService.getConnection).toHaveBeenCalled();
      });
      it('should call updateCashoutData when connection true', () => {
        component.cashoutBets = null;
        component.tempBets = [{ betId: 'i2', id: '2', leg: ['2'] }, { betId: 'i3', id: '3', leg: ['3'] }];
        CashoutWsConnectorService.getConnection.and.returnValue(true);
        CashoutWsConnectorService.dateChangeBet.and.returnValue(of(component.tempBets));
        component.updateCashoutData();
        expect(component.cashoutBets).toEqual(component.tempBets);
      });
    })
});