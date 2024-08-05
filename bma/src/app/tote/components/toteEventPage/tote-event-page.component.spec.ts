import { fakeAsync, tick } from '@angular/core/testing';
import { NavigationEnd } from '@angular/router';
import { of, throwError } from 'rxjs';
import * as _ from 'underscore';
import { ToteEventPageComponent } from '@app/tote/components/toteEventPage/tote-event-page.component';
import { IPool, IToteEvent } from '@app/tote/models/tote-event.model';
import { IPoolBetsModels } from '@app/tote/models/pool-bet.model';

describe('ToteEventPageComponent', () => {
  const title = 'toteEventPage';

  let component: ToteEventPageComponent;
  let toteService;
  let pubSubService;
  let gtmService;
  let betErrorHandlingService;
  let toteBetSlipService;
  let raceOutcomeDetailsService;
  let user;
  let cmsService;
  let route;
  let router;
  let toteCurrencyService;
  let sbFiltersService;
  let windowRef;
  let accountUpgradeLinkService;
  let lpAvailabilityService;
  let filtersService;
  let domTools;

  beforeEach(() => {
    toteService = {
      unSubscribeEDPForUpdates: jasmine.createSpy('unSubscribeEDPForUpdates'),
      getToteEvent: jasmine.createSpy('getToteEvent').and.returnValue(of([{
        typeName: 'someName',
        pools: [{
          id: 1,
          currencyCode: 'USD'
        }], markets: [{
          outcomes: []
        }]
      }])),
      getToteEvents: jasmine.createSpy('getToteEvents').and.returnValue(of({ events: [], meetings: [] })),
      getGuidesData: jasmine.createSpy('getGuidesData').and.returnValue(Promise.resolve({})),
      getPoolStakes: jasmine.createSpy('getPoolStakes').and.returnValue({}),
      subscribeEDPForUpdates: jasmine.createSpy('subscribeEDPForUpdates'),
      getEventsTabsDataByMeeting: jasmine.createSpy('getEventsTabsDataByMeeting').and.returnValue([{}]),
      collapsedSummaries: jasmine.createSpy('collapsedSummaries')
    };
    gtmService = jasmine.createSpyObj('GtmService', ['push']);
    betErrorHandlingService = jasmine.createSpyObj(
      'BetErrorHandlingService',
      [
      'checkTotalStake',
      'getTotalStakeErrorMsg', 'clearBetErrors',
      'buildErrors',
      'generateEventError',
      'clearLineBetErrors',
      'buildPoolStakeError',
      'isMarketsHasErrors',
      'getTotalStakeErrorMsg',
      'generateServiceError'
    ]
    );
    toteBetSlipService = jasmine.createSpyObj('ToteBetSlipService', [
      'placeBets',
      'isUserLoggedIn',
      'getPoolBetsInstance',
      'getCurrency'
    ]);
    raceOutcomeDetailsService = jasmine.createSpyObj('RaceOutcomeDetailsService', [
      'isGenericSilk',
      'isNumberNeeded',
      'isValidSilkName'
    ]);
    user = {
      isInShopUser: () => false,
      currencySymbol: '$'
    };
    toteCurrencyService = {
      getCurrencyCalculator: jasmine.createSpy('getCurrencyCalculator').and.returnValue(of({})),
    };
    cmsService = {
      getFeatureConfig: jasmine.createSpy('getFeatureConfig').and.returnValue(of({})),
      getItemSvg: jasmine.createSpy('getItemSvg').and.returnValue(of([]))
    };
    route = {
      params: of([]),
      events: of([])
    } as any;
    router = {
      navigate: jasmine.createSpy('navigate'),
      navigateByUrl: jasmine.createSpy('navigateByUrl'),
      events: {
        subscribe: jasmine.createSpy('subscribe').and.callFake(cb => cb())
      }
    } as any;
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe')
        .and.callFake((a: string, b: string[] | string, fn: Function) => fn()),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish'),
      API: {
        TOTE_BET_PLACED: 'TOTE_BET_PLACED',
        USER_INTERACTION_REQUIRED: 'USER_INTERACTION_REQUIRED',
        LOGIN_POPUPS_END: 'LOGIN_POPUPS_END',
        SUCCESSFUL_LOGIN: 'SUCCESSFUL_LOGIN'
      }
    };
    sbFiltersService = jasmine.createSpyObj('sbFiltersService', ['orderOutcomeEntities']);
    accountUpgradeLinkService = {
      inShopToMultiChannelLink: () => false
    };
    windowRef = {
      nativeWindow: {
        location: {
          href: ''
        },
        document: {
          querySelectorAll: jasmine.createSpy('querySelectorAll')
        }
      }
    };
    lpAvailabilityService = {
      check: jasmine.createSpy('check')
    };
    filtersService = {
      orderBy: jasmine.createSpy('orderBy'),
      distance: jasmine.createSpy('distance'),
      removeLineSymbol: jasmine.createSpy('removeLineSymbol')
    };
    domTools = {
      scrollTop: jasmine.createSpy('scrollTop'),
      getScrollTopPosition: jasmine.createSpy('getScrollTopPosition'),
      innerHeight: jasmine.createSpy('innerHeight')
    };
    spyOnProperty(document, 'scrollingElement').and.returnValue(null);

    component = new ToteEventPageComponent(
      betErrorHandlingService,
      raceOutcomeDetailsService,
      pubSubService,
      toteService,
      user,
      toteBetSlipService,
      toteCurrencyService,
      gtmService,
      lpAvailabilityService,
      sbFiltersService,
      filtersService,
      domTools,
      router,
      route,
      cmsService,
      windowRef,
      accountUpgradeLinkService
    );
    component['subscribedChannelsId'] = '';
    component['locationChangeListener'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
  });

  describe('upgrade account dialog', () => {
    let betsReceiptData;

    beforeEach(() => {
      betsReceiptData = {
        failedBets: [],
        successBets: []
      };
      component.isTotalStakeError = jasmine.createSpy('isTotalStakeError').and.returnValue(false);
      component.userIsLoggedIn = true;
      toteBetSlipService.placeBets.and.returnValue(of(betsReceiptData));
      component['clearExactaOrTrifectaData'] = jasmine.createSpy('clearExactaOrTrifectaData');
      component['scrollToTopErrorStakeBox'] = jasmine.createSpy('scrollToTopErrorStakeBox');
      component['poolBetsInstance'] = {
        totalStake: 0,
        clearBets: () => {
        }
      } as IPoolBetsModels;
    });

    it('redirect in-shop user to upgrade page', fakeAsync(() => {
      Object.defineProperty(component['accountUpgradeLinkService'], 'inShopToMultiChannelLink', { get: () => 'http://ffs.com' });
      component['user'].isInShopUser = () => true;

      component.placeBets();
      tick();
      expect(toteBetSlipService.placeBets).not.toHaveBeenCalled();
      expect(component['windowRef'].nativeWindow.location.href).toEqual('http://ffs.com');
    }));

    it('do not show if user in online or multichannel', fakeAsync(() => {
      component.eventData = {} as IToteEvent;
      component.poolStakes = {} as IPool;

      component.placeBets();
      tick();
      expect(toteBetSlipService.placeBets).toHaveBeenCalledWith(jasmine.anything());
      expect(betErrorHandlingService.clearBetErrors).toHaveBeenCalledWith(component.eventData);
      expect(pubSubService.publish).toHaveBeenCalledWith('TOTE_BET_PLACED');
    }));

    it('should show login dialog if user is not logged in', fakeAsync(() => {
      component.userIsLoggedIn = false;

      component.placeBets();
      tick();
      expect(toteBetSlipService.placeBets).not.toHaveBeenCalled();
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.OPEN_LOGIN_DIALOG, { placeBet: 'tote', moduleName: 'tote' });
      expect(component.loginAndPlaceBets).toBeTruthy();
    }));

    it('should handle error with total stake', () => {
      component.isTotalStakeError = jasmine.createSpy('isTotalStakeError').and.returnValue(true);

      component.placeBets();

      expect(betErrorHandlingService.getTotalStakeErrorMsg).toHaveBeenCalled();
    });

    it('should handle bet placement error', fakeAsync(() => {
      betsReceiptData.failedBets = [{}];

      component.placeBets();
      tick();

      expect(betErrorHandlingService.buildErrors).toHaveBeenCalled();
    }));

    it('should handle if betSuccessfullyPlaced', fakeAsync(() => {
      toteBetSlipService.placeBets.and.returnValue(of({
        failedBets: [],
        successBets: [{}]
      }));

      component.placeBets();
      tick();

      expect(component['scrollToTopErrorStakeBox']).not.toHaveBeenCalled();
    }));

    describe('toteBetSlipService error handler', () => {
      it('should handle service error', fakeAsync(() => {
        toteBetSlipService.placeBets.and.returnValue(throwError({error: 'Error!'}));

        component.placeBets();
        tick();

        expect(betErrorHandlingService.buildErrors).toHaveBeenCalled();
      }));

      it('should generate general error', fakeAsync(() => {
        toteBetSlipService.placeBets.and.returnValue(throwError({}));

        component.placeBets();
        tick();

        expect(betErrorHandlingService.generateServiceError).toHaveBeenCalled();
      }));
    });
  });

  it('OnDestroy should unsubscribe', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith(title);
    expect(toteService.unSubscribeEDPForUpdates).toHaveBeenCalled();
    expect(component['locationChangeListener'].unsubscribe).toHaveBeenCalled();
  });

  it('filterGuides', () => {
    const pools = [{
      guides: [{
        id: '1',
        poolValue: 'poolValue test'
      }]
    }] as any;

    expect(component['filterGuides'](pools)).toEqual([pools[0].guides[0].poolValue]);
  });

  describe('initLiveStream', () => {
    it('should subscribe on events', () => {
      component.eventData = {
        liveStreamAvailable: true
      } as any;
      component.streamControl = {
        hideStream: jasmine.createSpy('hideStream')
      } as any;
      component.isStreamPlaying = false;
      component['initLiveStream']();
      expect(pubSubService.subscribe).toHaveBeenCalledWith(title, ['TOTE_BET_PLACED', 'SUCCESSFUL_LOGIN'], jasmine.any(Function));
      expect(component.streamControl.hideStream).toHaveBeenCalled();
      expect(component.isStreamPlaying).toBe(false);
    });

    it('no streamControl', () => {
      component.eventData = {
        liveStreamAvailable: true
      } as any;
      component.isStreamPlaying = true;
      component['initLiveStream']();
      expect(component.isStreamPlaying).toBe(false);
    });

    it('no liveStreamAvailable', () => {
      component.eventData = {
        liveStreamAvailable: false
      } as any;
      component['initLiveStream']();
      expect(pubSubService.subscribe).not.toHaveBeenCalled();
    });

    it('should init playStream method', () => {
      component.eventData = {
        liveStreamAvailable: true
      } as any;

      component['initLiveStream']();

      expect(component.playStream).toBeDefined();

      component.isStreamPlaying = true;

      component.playStream({ preventDefault: jasmine.createSpy() });

      expect(component.isStreamPlaying).toBeFalsy();
    });
  });

  describe('ngOnInit', () => {
    it('should subscribe for updates', fakeAsync(() => {
      component['initLiveStream'] = jasmine.createSpy('initLiveStream');
      component['initPools'] = jasmine.createSpy('initPools');
      component['initPoolBets'] = jasmine.createSpy('initPoolBets');
      component['getOrderedOutcomes'] = jasmine.createSpy('getOrderedOutcomes');
      component['showDistance'] = jasmine.createSpy('showDistance');
      component.placeBets = jasmine.createSpy('placeBets');
      component.loginAndPlaceBets = true;
      toteService.getToteEvents.and.returnValue(of({ events: [], meetings: [{ name: 'someName' }] }));
      component.ngOnInit();
      tick();

      expect(pubSubService.subscribe).toHaveBeenCalledWith('toteEventPage', 'LOGIN_POPUPS_END', jasmine.any(Function));
      expect(pubSubService.subscribe).toHaveBeenCalledWith(title, 'SUCCESSFUL_LOGIN', jasmine.any(Function));
      expect(toteService.subscribeEDPForUpdates).toHaveBeenCalled();
      expect(component.placeBets).toHaveBeenCalled();
    }));

    it('should leave eventTabs empty', () => {
      toteService.getToteEvents.and.returnValue(of({ events: [], meetings: [{ name: 'test' }] }));

      component.ngOnInit();

      expect(component.eventTabs).toBe(undefined);
    });

    it('should go to "/"', () => {
      route.params = of({ sport: 'test' });

      component.ngOnInit();

      expect(router.navigateByUrl).toHaveBeenCalledWith('/');
    });

    it('should init filter with params', () => {
      route.params = of({ filter: 'by-time' });

      component.ngOnInit();

      expect(component.filter).toBe('by-time');
    });

    it('should subscribe to the router events', () => {
      router.events.subscribe.and.callFake(cb => cb(new NavigationEnd(1, '/', '/')));
      component.ngOnInit();

      expect(betErrorHandlingService.clearBetErrors).toHaveBeenCalled();
    });

    it('should handle error', () => {
      toteService.getToteEvents.and.returnValue(throwError('error'));
      component.goToDefaultPage = jasmine.createSpy('goToDefaultPage');

      component.ngOnInit();

      expect(component.goToDefaultPage).toHaveBeenCalled();
    });

    it('should get tote cms configurations', () => {
      component.ngOnInit();

      expect(cmsService.getFeatureConfig).toHaveBeenCalledWith('totePoolsDescriptions');
      expect(cmsService.getFeatureConfig).toHaveBeenCalledWith('toteBetErrors');
    });
  });

  it('trackByEvent', () => {
    const result = component.trackByEvent(1, { id: 1 } as any);

    expect(result).toBe('11');
  });

  it('trackByOutcome', () => {
    const result = component.trackByOutcome(1, { id: 1 } as any);

    expect(result).toBe('11');
  });

  it('trackByMarket', () => {
    const result = component.trackByMarket(1, { id: 1 } as any);

    expect(result).toBe('11');
  });


  it('goToDefaultPage', () => {
    component.goToDefaultPage();

    expect(router.navigateByUrl).toHaveBeenCalledWith('/tote');
  });

  describe('getOrderedMeetingNames', () => {
    it('should return sorted meetingsNames', () => {
      component.meetingsNames = ['a', 'b', 'd', 'c','c','abc','#123'];
      const result = component.getOrderedMeetingNames();
      expect(result).toBe(result.sort());
    });

    it('should not call sort method', () => {
      component.meetingsNames = [];

      const result = component.getOrderedMeetingNames();

      expect(result).toEqual(component.meetingsNames);
    });
  });

  it('getOrderedMarkets', () => {
    component.eventData = {
      markets: []
    } as IToteEvent;
    component.getOrderedMarkets();

    expect(filtersService.orderBy).toHaveBeenCalled();
  });

  it('getOrderedOutcomes', () => {
    const outcomes = [];
    component.getOrderedOutcomes(outcomes);

    expect(sbFiltersService.orderOutcomeEntities).toHaveBeenCalledWith(outcomes, false, true, true);
  });

  it('isValidSilkName', () => {
    component.isValidSilkName({ silkName: '' });

    expect(raceOutcomeDetailsService.isValidSilkName).toHaveBeenCalled();
  });

  describe('isTotalStakeError', () => {
    beforeEach(() => {
      component.totalStakeError = {
        totalMax: false,
        totalMin: false,
        stakeIncrementFactor: false
      } as any;
    });

    it('should return false', () => {
      component.totalStakeError = null;

      expect(component.isTotalStakeError()).toBeFalsy();
    });

    it('should return true and check totalStakeError.totalMax', () => {
      component.totalStakeError.totalMax = true;

      expect(component.isTotalStakeError()).toBeTruthy();
    });

    it('should return true and check totalStakeError.totalMin', () => {
      component.totalStakeError.totalMin = true;

      expect(component.isTotalStakeError()).toBeTruthy();
    });

    it('should return true and check totalStakeError.totalMin', () => {
      component.totalStakeError.stakeIncrementFactor = true;

      expect(component.isTotalStakeError()).toBeTruthy();
    });
  });

  it('displayStakeErrors', () => {
    const data = {
      outcomeId: '',
      value: '',
      poolData: {} as any
    };

    component.displayStakeErrors(data);

    expect(component.totalStakeError).toBeNull();
    expect(betErrorHandlingService.clearLineBetErrors).toHaveBeenCalledWith(component.eventData, data.outcomeId);
    expect(betErrorHandlingService.buildPoolStakeError).toHaveBeenCalledWith(component.eventData, data);
    expect(betErrorHandlingService.isMarketsHasErrors).toHaveBeenCalledWith(component.eventData);
  });

  describe('isPoolSuspended', () => {
    beforeEach(() => {
      component.eventData = {
        pools: []
      } as any;
    });

    it('should call _.find', () => {
      spyOn(_, 'find');

      component.isPoolSuspended();

      expect(_.find).toHaveBeenCalled();
    });

    it('should return false', () => {
      component.eventData.pools = [{
        isActive: true,
        type: 'AA'
      } as any];
      component.betFilter = 'AA';

      expect(component.isPoolSuspended()).toBeFalsy();
    });

    it('should return false', () => {
      component.eventData.pools = [{
        isActive: false,
        type: 'AA'
      } as any];
      component.betFilter = 'AA';

      expect(component.isPoolSuspended()).toBeTruthy();
    });
  });

  describe('getStopBettingValue', () => {
    beforeEach(() => {
      component.isSuspended = jasmine.createSpy('isSuspended');
      component.isPoolSuspended = jasmine.createSpy('isPoolSuspended');
    });

    it('should return isSuspended()', () => {
      const outcome = { nonRunner: false } as any;
      (component.isSuspended as jasmine.Spy).and.returnValue(true);

      expect(component.getStopBettingValue(outcome)).toBeTruthy();
    });

    it('should return nonRunner', () => {
      const outcome = { nonRunner: true } as any;
      (component.isSuspended as jasmine.Spy).and.returnValue(false);

      expect(component.getStopBettingValue(outcome)).toBeTruthy();
    });

    it('should return isPoolSuspended()', () => {
      const outcome = { nonRunner: false } as any;
      (component.isSuspended as jasmine.Spy).and.returnValue(false);
      (component.isPoolSuspended as jasmine.Spy).and.returnValue(true);

      expect(component.getStopBettingValue(outcome)).toBeTruthy();
    });
  });

  describe('findGuideValue', () => {
    beforeEach(() => {
      component.eventData = { pools: [] } as any;
      component.eventData = {
        pools: [{
          id: '222',
          poolType: 'WN'
        }]
      } as any;
      component.guides = [{
        id: '111',
        poolId: '222',
        runnerNumber1: '1',
        value: 'test'
      }] as any;

      spyOn(_, 'contains').and.callThrough();
      spyOn(_, 'find').and.callThrough();
    });

    it('should return guide value', () => {
      expect(component.findGuideValue('1', 'TR')).toBe('test');
    });

    it('should not return guide value', () => {
      component.guides = [];
      expect(component.findGuideValue('1', 'SH')).not.toBe('test');
    });
  });

  describe('getGeneralError', () => {
    beforeEach(() => {
      component['eventStartedError'] = jasmine.createSpy('eventStartedError');
      component['marketSuspendedError'] = jasmine.createSpy('marketSuspendedError');
      component['eventSuspendedError'] = jasmine.createSpy('eventSuspendedError');
    });

    it('should call eventStartedError', () => {
      const errorData = 'from method  eventStartedError';
      (component['eventStartedError'] as jasmine.Spy).and.returnValue(errorData);

      const result = component.getGeneralError();

      expect(component['eventStartedError']).toHaveBeenCalled();
      expect(result).toBe(errorData);
    });

    it('should call marketSuspendedError', () => {
      const errorData = 'from method  marketSuspendedError';
      (component['marketSuspendedError'] as jasmine.Spy).and.returnValue(errorData);

      const result = component.getGeneralError();

      expect(component['marketSuspendedError']).toHaveBeenCalled();
      expect(result).toBe(errorData);
    });

    it('should call eventSuspendedError', () => {
      const errorData = 'from method  eventSuspendedError';
      (component['eventSuspendedError'] as jasmine.Spy).and.returnValue(errorData);

      const result = component.getGeneralError();

      expect(component['eventSuspendedError']).toHaveBeenCalled();
      expect(result).toBe(errorData);
    });
  });

  describe('betNowDisabled', () => {
    beforeEach(() => {
      component.placeBetsPending = false;
      component.isLineError = false;
      component.totalStake = jasmine.createSpy('totalStake');
      component.isSuspended = jasmine.createSpy('isSuspended');
      component['exactaOrTrifecta'] = jasmine.createSpy('exactaOrTrifecta');
    });

    it('should return placeBetsPending', () => {
      component.placeBetsPending = true;

      expect(component.betNowDisabled()).toBe(component.placeBetsPending);
      expect(component.totalStake).not.toHaveBeenCalled();
      expect(component['exactaOrTrifecta']).not.toHaveBeenCalled();
    });

    it('should return totalStake()', () => {
      (component.totalStake as jasmine.Spy).and.returnValue(false);

      component.betNowDisabled();
      expect(component.totalStake).toHaveBeenCalled();
      expect(component.isSuspended).not.toHaveBeenCalled();
      expect(component['exactaOrTrifecta']).not.toHaveBeenCalled();
    });

    it('should return isSuspended()', () => {
      (component.totalStake as jasmine.Spy).and.returnValue(true);
      (component.isSuspended as jasmine.Spy).and.returnValue(true);

      component.betNowDisabled();

      expect(component.isSuspended).toHaveBeenCalled();
      expect(component['exactaOrTrifecta']).not.toHaveBeenCalled();
    });

    it('should return isLineError', () => {
      (component.totalStake as jasmine.Spy).and.returnValue(true);
      (component.isSuspended as jasmine.Spy).and.returnValue(false);
      component.isLineError = true;

      expect(component.betNowDisabled()).toBe(component.isLineError);
    });

    it('should call exactaOrTrifecta and return true', () => {
      (component.totalStake as jasmine.Spy).and.returnValue(true);
      (component['exactaOrTrifecta'] as jasmine.Spy).and.returnValue(true);
      component.selectedPlaces = { status: false };

      const result = component.betNowDisabled();

      expect(component['exactaOrTrifecta']).toHaveBeenCalled();
      expect(result).toBeTruthy();
    });

    it('should call exactaOrTrifecta and return false', () => {
      (component.totalStake as jasmine.Spy).and.returnValue(true);
      (component['exactaOrTrifecta'] as jasmine.Spy).and.returnValue(true);
      component.selectedPlaces = { status: true };

      const result = component.betNowDisabled();

      expect(component['exactaOrTrifecta']).toHaveBeenCalled();
      expect(result).toBeFalsy();
    });
  });

  describe('selectEvent', () => {
    beforeEach(() => {
      component.eventsData = {
        meetings: [{
          id: 0,
          name: 'test',
          events: [{
            id: 1,
            eventStatusCode: 'P'
          }, {
            id: 2,
            eventStatusCode: 'A'
          }]
        }]
      } as any;
    });

    it('should call gtmService.push', () => {

      component.selectEvent('test');

      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: component.gtmCategoryName,
        eventAction: 'select meeting',
        eventLabel: 'test'
      });
    });

    it('should call router.navigate', () => {
      component.selectEvent('test');

      expect(router.navigate).toHaveBeenCalledWith(['tote', 'event', 2]);
    });

    it('should take redirectId from selectedMeeting', () => {
      component.eventsData.meetings[0].events.splice(1, 1);
      component.selectEvent('test');

      expect(router.navigate).toHaveBeenCalledWith(['tote', 'event', 1]);
    });
  });

  describe('convertedTotalStake', () => {
    it('should return converted value', () => {
      component.currencyCalculator = {
        currencyExchange: jasmine.createSpy('currencyExchange').and.returnValue(1)
      } as any;
      component.totalStake = jasmine.createSpy('totalStake');

      component.convertedTotalStake();

      expect(component.convertedTotalStake()).toBe('$1');
      expect(component.currencyCalculator.currencyExchange).toHaveBeenCalled();
    });

    it('should not return converted value', () => {
      component.currencyCalculator = null;

      expect(component.convertedTotalStake()).toBe('$null');
    });
  });

  describe('isSuspended', () => {
    beforeEach(() => {
      component['isEventStarted'] = jasmine.createSpy('isEventStarted').and.returnValue(false);
      component['isEventSuspended'] = jasmine.createSpy('isEventSuspended').and.returnValue(false);
      component['isMarketSuspended'] = jasmine.createSpy('isMarketSuspended').and.returnValue(false);
    });

    it('should return isEventStarted()', () => {
      (component['isEventStarted'] as jasmine.Spy).and.returnValue(true);

      expect(component.isSuspended()).toBeTruthy();
    });

    it('should return isEventSuspended()', () => {
      (component['isEventSuspended'] as jasmine.Spy).and.returnValue(true);

      expect(component.isSuspended()).toBeTruthy();
    });

    it('should return isMarketSuspended()', () => {
      (component['isMarketSuspended'] as jasmine.Spy).and.returnValue(true);

      expect(component.isSuspended()).toBeTruthy();
    });

    it('should check outcome', () => {
      const outcome = { outcomeStatusCode: 'S' } as any;

      expect(component.isSuspended(outcome)).toBeTruthy();
    });
  });

  describe('onExpand', () => {
    beforeEach(() => {
      component.expandedSummary = {
        0: { 0: false }
      };
    });

    describe('gtmService.push', () => {
      it('should call gtmService.push with eventAction: "show summary"', () => {
        component.onExpand(null, 0, 0);

        expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
          eventCategory: component.gtmCategoryName,
          eventAction: 'show summary'
        });
      });

      it('should call gtmService.push with eventAction: "hide summary"', () => {
        component.expandedSummary[0][0] = true;

        component.onExpand(null, 0, 0);

        expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
          eventCategory: component.gtmCategoryName,
          eventAction: 'hide summary'
        });
      });

      it('should ...', () => {
        component.expandedSummary[0][1] = true;
        component.activeSummary = {
          market: 0,
          outcome: 0
        } as any;

        component.onExpand({ 0: {} }, 0, 1);

        expect(component.expandedSummary[0][1]).toBeFalsy();
      });
    });
  });

  it('onBetReceiptContinue', () => {
    component.betsReceiptData = { successBets: [] } as any;

    component.onBetReceiptContinue();

    expect(domTools.scrollTop).toHaveBeenCalled();
  });

  it('isLpAvailable', () => {
    component.isLpAvailable({} as any);

    expect(lpAvailabilityService.check).toHaveBeenCalled();
  });

  describe('genEventDetailsUrl', () => {
    it('should return eventEntity.url', () => {
      const eventEntity = { url: '/test', isResulted: false } as any;

      expect(component.genEventDetailsUrl(eventEntity)).toBe(eventEntity.url);
    });

    it('should return RESULTS_URL', () => {
      const eventEntity = { url: '/test', isResulted: true } as any;

      expect(component.genEventDetailsUrl(eventEntity)).toBe(component.RESULTS_URL);
    });
  });

  describe('scrollToBetReceipt', () => {
    beforeEach(() => {
      spyOn(document, 'querySelector').and.returnValue({
        getBoundingClientRect: jasmine.createSpy('getBoundingClientRect').and.returnValue({
          top: jasmine.createSpy('top')
        })
      } as any);
    });

    it('should call domTools.scrollTop', () => {
      // spyOnProperty(document, 'scrollingElement').and.returnValue(null);
      component.scrollToBetReceipt();

      expect(document.querySelector).toHaveBeenCalled();
      expect(domTools.scrollTop).toHaveBeenCalled();
    });

    it('should not call domTools.scrollTop', () => {
      (document.querySelector as jasmine.Spy).and.returnValue(undefined);

      component.scrollToBetReceipt();

      expect(document.querySelector).toHaveBeenCalled();
      expect(domTools.scrollTop).not.toHaveBeenCalled();
    });
  });

  it('filterDistance', () => {
    component.filterDistance('');

    expect(filtersService.distance).toHaveBeenCalled();
  });

  it('removeLineSymbol', () => {
    component.removeLineSymbol('');

    expect(filtersService.removeLineSymbol).toHaveBeenCalled();
  });

  it('toggleSummary', () => {
    component.summary = true;

    component.toggleSummary();

    expect(component.summary).toBeFalsy(component.summary);
  });

  describe('isEventSuspended', () => {
    it('should return true', () => {
      component.eventData = { eventStatusCode: 'S' } as any;

      expect(component['isEventSuspended']()).toBeTruthy();
    });

    it('should return false', () => {
      component.eventData = { eventStatusCode: 'P' } as any;
      expect(component['isEventSuspended']()).toBeFalsy();
    });
  });

  describe('isEvenisMarketSuspendedtSuspended', () => {
    it('should return true', () => {
      component.eventData = {
        markets: [{ marketStatusCode: 'S' }]
      } as any;
      expect(component['isMarketSuspended']()).toBeTruthy();
    });

    it('should return false', () => {
      component.eventData = {
        markets: [{ marketStatusCode: 'P' }]
      } as any;

      expect(component['isMarketSuspended']()).toBeFalsy();
    });
  });

  it('isEventStarted', () => {
    component.eventData = { eventIsLive: true } as any;

    expect(component['isEventStarted']()).toBeTruthy();
  });

  describe('eventStartedError', () => {
    it('should return true', () => {
      component['isEventStarted'] = jasmine.createSpy('isEventStarted').and.returnValue(true);
      component.eventStartedErrorMsg = { type: '', msg: 'error' };

      const result = component['eventStartedError']();

      expect(component['isEventStarted']).toHaveBeenCalled();
      expect(result).toBe(component.eventStartedErrorMsg);
    });

    it('should return false', () => {
      component['isEventStarted'] = jasmine.createSpy('isEventStarted').and.returnValue(false);

      const result = component['eventStartedError']();

      expect(component['isEventStarted']).toHaveBeenCalled();
      expect(result).toBeFalsy();
    });
  });

  describe('marketSuspendedError', () => {
    it('should return true', () => {
      component['isMarketSuspended'] = jasmine.createSpy('isMarketSuspended').and.returnValue(true);
      component.marketSuspendedErrorMsg = { type: '', msg: 'error' };

      const result = component['marketSuspendedError']();

      expect(component['isMarketSuspended']).toHaveBeenCalled();
      expect(result).toBe(component.marketSuspendedErrorMsg);
    });

    it('should return false', () => {
      component['isMarketSuspended'] = jasmine.createSpy('isMarketSuspended').and.returnValue(false);

      const result = component['marketSuspendedError']();

      expect(component['isMarketSuspended']).toHaveBeenCalled();
      expect(result).toBeFalsy();
    });
  });

  describe('eventSuspendedError', () => {
    it('should return true', () => {
      component['isEventSuspended'] = jasmine.createSpy('isMarketSuspended').and.returnValue(true);
      component.eventSuspendedErrorMsg = { type: '', msg: 'error' };

      const result = component['eventSuspendedError']();

      expect(component['isEventSuspended']).toHaveBeenCalled();
      expect(result).toBe(component.eventSuspendedErrorMsg);
    });

    it('should return false', () => {
      component['isEventSuspended'] = jasmine.createSpy('isMarketSuspended').and.returnValue(false);

      const result = component['eventSuspendedError']();

      expect(component['isEventSuspended']).toHaveBeenCalled();
      expect(result).toBeFalsy();
    });
  });


  describe('exactaOrTrifecta', () => {
    it('should return true if exacta', () => {
      component.betFilter = 'EX';

      expect(component['exactaOrTrifecta']()).toBeTruthy();
    });

    it('should return true if trifects', () => {
      component.betFilter = 'TR';

      expect(component['exactaOrTrifecta']()).toBeTruthy();
    });

    it('should return false', () => {
      expect(component['exactaOrTrifecta']()).toBeFalsy();
    });
  });

  describe('clearExactaOrTrifectaData', () => {
    beforeEach(() => {
      component['generateCheckboxMap'] = jasmine.createSpy('generateCheckboxMap');
      component.eventData = {
        markets: [{
          outcomes: []
        }]
      } as any;
    });

    it('should clear checkbox map', () => {
      component['exactaOrTrifecta'] = jasmine.createSpy('exactaOrTrifecta').and.returnValue(true);

      component['clearExactaOrTrifectaData']();

      expect(component['generateCheckboxMap']).toHaveBeenCalled();
    });

    it('should not clear checkbox map', () => {
      component['exactaOrTrifecta'] = jasmine.createSpy('exactaOrTrifecta').and.returnValue(false);

      component['clearExactaOrTrifectaData']();

      expect(component['generateCheckboxMap']).not.toHaveBeenCalled();
    });
  });

  describe('initPools', () => {
    beforeEach(() => {
      component.eventData = {
        poolsTypesOrdered: []
      } as any;
      spyOn(_, 'map').and.callThrough();
      component['initPoolBets'] = jasmine.createSpy('initPoolBets');
      component['clearExactaOrTrifectaData'] = jasmine.createSpy('clearExactaOrTrifectaData');
    });

    it('should escape if !this.eventData.defaultPoolType', () => {
      component['initPools']();

      expect(component.betFilter).not.toBeDefined();
      expect(component.viewByBetFilters).not.toBeDefined();
      expect(_.map).not.toHaveBeenCalled();
      expect(component.switchers).not.toBeDefined();
    });

    it('should init switchers directive config', () => {
      component.eventData = {
        poolsTypesOrdered: ['WN', 'PL', 'SH'],
        defaultPoolType: 'PL'
      } as any;
      component.switchers = [];

      component['initPools']();

      expect(component.betFilter).toBeDefined();
      expect(component.viewByBetFilters).toBeDefined();
      expect(_.map).toHaveBeenCalled();
      expect(component.switchers).toBeDefined();

      component.switchers[0].onClick();

      expect(toteService.collapsedSummaries).toHaveBeenCalled();
      expect(toteService.getPoolStakes).toHaveBeenCalled();
      expect(component['initPoolBets']).toHaveBeenCalled();
      expect(component['clearExactaOrTrifectaData']).toHaveBeenCalled();
      expect(betErrorHandlingService.clearBetErrors).toHaveBeenCalled();
    });
  });

  describe('initPoolBets', () => {
    let toteBetSlipServiceMockedMethods;

    beforeEach(() => {
      component.eventData = {
        pools: [
          { id: '111', type: 'TR' },
          { id: '222', type: 'EX' }
        ]
      } as any;
      toteBetSlipServiceMockedMethods = {
        fieldsControls: [],
        currencySymbol: '$',
        totalStake: jasmine.createSpy('totalStake').and.returnValue(1),
        stakeValue: jasmine.createSpy('stakeValue').and.returnValue(1),
        changeValue: jasmine.createSpy('changeValue'),
        clearBets: jasmine.createSpy('clearBets')
      } as any;
      toteBetSlipService.getPoolBetsInstance.and.returnValue(toteBetSlipServiceMockedMethods);
      toteBetSlipService.getCurrency.and.returnValue('$');
    });

    it('should init pool bets', () => {
      component['initPoolBets']('TR');

      expect(component.fieldControls).toBeDefined();
      expect(component.totalStake()).toBe(component['poolBetsInstance'].totalStake);
      expect(component.currencySymbol).toBeDefined();
      expect(component.changeValue).toBeDefined();
      expect(component.stakeValue).toBeDefined();
      expect(component.stakeValue()).toEqual(1);
      expect(component.clearBets).toBeDefined();
    });

    it('should handle if not poolBetsAvailable', () => {
      toteBetSlipService.getPoolBetsInstance.and.returnValue(undefined);

      component['initPoolBets']('TR');

      expect(component.fieldControls).not.toBeDefined();
      expect(component.currencySymbol).not.toBeDefined();
      expect(component.totalStake).not.toBeDefined();
      expect(component.changeValue).not.toBeDefined();
      expect(component.stakeValue).not.toBeDefined();
      expect(component.clearBets).not.toBeDefined();
    });

    it('should handle if poolBetsInstance.stakeValue not defined', () => {
      toteBetSlipServiceMockedMethods.stakeValue = undefined;
      toteBetSlipService.getPoolBetsInstance.and.returnValue(toteBetSlipServiceMockedMethods);

      component['initPoolBets']('TR');
      expect(component.stakeValue).toBeDefined();
      expect(component.stakeValue()).not.toEqual(1);
    });

    describe('clearBets', () => {
      let mousesEvent;
      beforeEach(() => {
        mousesEvent = {
          preventDefault: jasmine.createSpy('preventDefault')
        };
        component['clearExactaOrTrifectaData'] = jasmine.createSpy('clearExactaOrTrifectaData');
      });

      it('should clear bets', () => {
        component['initPoolBets']('TR');

        component.clearBets(mousesEvent);

        expect(gtmService.push).toHaveBeenCalled();
        expect(component['poolBetsInstance'].clearBets).toHaveBeenCalled();
        expect(betErrorHandlingService.clearBetErrors).toHaveBeenCalled();
        expect(component['clearExactaOrTrifectaData']).toHaveBeenCalled();
      });

      it('should handle case if there are placeBetsPending', () => {
        component.placeBetsPending = true;

        component['initPoolBets']('TR');

        component.clearBets(mousesEvent);

        expect(gtmService.push).not.toHaveBeenCalled();
        expect(component['poolBetsInstance'].clearBets).not.toHaveBeenCalled();
        expect(betErrorHandlingService.clearBetErrors).toHaveBeenCalled();
        expect(component['clearExactaOrTrifectaData']).toHaveBeenCalled();
      });
    });
  });

  it('showDistance', () => {
    const event = {
      showDistance: false,
      racingFormEvent: {
        distance: '500m'
      }
    } as any;

    component['showDistance'](event);

    expect(event.showDistance).toBeTruthy();
  });

  it('scrollToPosition', () => {
    const element = {
      scrollTop: jasmine.createSpy('scrollTop')
    };
    windowRef.nativeWindow.document.querySelectorAll.and.returnValue([element]);

    component['scrollToPosition'](100);

    expect(windowRef.nativeWindow.document.querySelectorAll).toHaveBeenCalled();
  });

  describe('scrollToTopErrorStakeBox', () => {
    beforeEach(() => {
      component['scrollToPosition'] = jasmine.createSpy('scrollToBetReceipt');
    });

    it('should call scrollToPosition', fakeAsync(() => {
      spyOn(document, 'querySelector').and.returnValue({
        getBoundingClientRect: jasmine.createSpy('getBoundingClientRect').and.returnValue({
          top: jasmine.createSpy('top')
        })
      } as any);

      component['scrollToTopErrorStakeBox']();
      tick(component['timeOutDelay']);

      expect(component['scrollToPosition']).toHaveBeenCalled();
    }));

    it('should not call scrollToPosition', fakeAsync(() => {
      spyOn(document, 'querySelector').and.returnValue(null);

      component['scrollToTopErrorStakeBox']();
      tick(100);

      expect(component['scrollToPosition']).not.toHaveBeenCalled();
    }));
  });

  describe('generateCheckboxMap', () => {
    let outcomes;

    beforeEach(() => {
      outcomes = [
        { id: '0' }
      ] as any;
    });

    it('should return empty object', () => {
      expect(component['generateCheckboxMap'](outcomes, 'AA')).toEqual({});
    });

    it('should return result for poolType === EX', () => {
      const expectedResult = { 0: ['enabled', 'enabled'] };

      expect(component['generateCheckboxMap'](outcomes, 'EX')).toEqual(expectedResult);
    });

    it('should return result for poolType === TR', () => {
      const expectedResult = { 0: ['enabled', 'enabled', 'enabled'] };

      expect(component['generateCheckboxMap'](outcomes, 'TR')).toEqual(expectedResult);
    });
  });
});
