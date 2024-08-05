import { PoolBetHistoryComponent } from './pool-bet-history.component';
import { of, throwError } from 'rxjs';
import quadpodBet from './../../mocks/quadpotBet.mock';
import trifectaBet from './../../mocks/trifectaBet.mock';

describe('PoolBetHistoryComponent', () => {
  let component: PoolBetHistoryComponent;

  let localeService;
  let userService;
  let betHistoryMainService;
  let timeService;
  let cashoutMapIndexService;
  let cashOutLiveUpdatesSubscribeService;
  let sbFiltersService;
  let currencyPipe;
  let toteBetsExtendingService;
  let pubsub;
  let cmsService;
  let deviceService;

  beforeEach(() => {

    localeService = {
      getString: jasmine.createSpy('getString').and.callFake(x => x)
    };
    userService = {};
    betHistoryMainService = {
      generateBetsMap: jasmine.createSpy('generateBetsMap').and.returnValue([]),
      getBetStatus: jasmine.createSpy('getBetStatus'),
      getCelebrationBanner: jasmine.createSpy('getCelebrationBanner').and.returnValue({})
    };
    timeService = {
      getLocalDateFromString: jasmine.createSpy().and.returnValue('2019-03-04T16:30:45.000Z')
    };
    cashoutMapIndexService = {};
    cashOutLiveUpdatesSubscribeService = {
      addWatch: jasmine.createSpy('addWatch'),
      unsubscribeFromLiveUpdates: jasmine.createSpy('unsubscribeFromLiveUpdates')
    };
    sbFiltersService = {
      orderOutcomeEntities: jasmine.createSpy('orderOutcomeEntities').and.callFake(x => x)
    };
    currencyPipe = {
      transform: jasmine.createSpy('transform').and.callFake((value, currencySymbol) => `${value}${currencySymbol}`)
    };
    toteBetsExtendingService = {
      extendToteBetsWithEvents: jasmine.createSpy('extendToteBetsWithEvents').and.returnValue(of([]))
    };
    pubsub = {
      API: {
        RELOAD_COMPONENTS: '',
      } as Record<string, string>,
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish')
    };
    cmsService = {
      getItemSvg: jasmine.createSpy('getItemSvg').and.returnValue(of({
        svg: 'svg',
        svgId: 'svgId'
      }))
    };

    deviceService = {
      getDeviceViewType: jasmine.createSpy('getDeviceViewType')
    }

    component = new PoolBetHistoryComponent(
      localeService,
      userService,
      betHistoryMainService,
      timeService,
      cashoutMapIndexService,
      cashOutLiveUpdatesSubscribeService,
      sbFiltersService,
      currencyPipe,
      toteBetsExtendingService,
      pubsub,
      cmsService,
      deviceService
    );

    component.poolBets = [
      quadpodBet as any,
      trifectaBet as any,
      {
        poolType: 'unknown'
      } as any
    ];
    component.isBetHistoryTab = true;
  });

  describe('constructor', () => {
    it('should define properties from super class', () => {
      expect(component.isUsedFromWidget).toEqual(false);
    });
  });

  describe('#subscirbeForLiveUpdates', () => {
    it('should call subscirbeForLiveUpdates success', () => {
      component['subscirbeForLiveUpdates']();

      expect(toteBetsExtendingService.extendToteBetsWithEvents).toHaveBeenCalledWith([]);
      expect(betHistoryMainService.generateBetsMap).toHaveBeenCalledWith([]);
      expect(toteBetsExtendingService.extendToteBetsWithEvents).toHaveBeenCalledWith([]);
    });

    it('should call subscirbeForLiveUpdates error', () => {
      toteBetsExtendingService.extendToteBetsWithEvents.and.returnValue(throwError('error'));
      component['subscirbeForLiveUpdates']();

      expect(betHistoryMainService.generateBetsMap).toHaveBeenCalledWith([]);
      expect(toteBetsExtendingService.extendToteBetsWithEvents).toHaveBeenCalledWith([]);
      expect(cashOutLiveUpdatesSubscribeService.addWatch).not.toHaveBeenCalled();
    });
  });

  describe('ngOnDestroy', () => {
    it('should unsubscribe clear comonent subscriptions', () => {
      component.ngOnDestroy();
      expect(cashOutLiveUpdatesSubscribeService.unsubscribeFromLiveUpdates).toHaveBeenCalled();
      expect(pubsub.unsubscribe).toHaveBeenCalledWith('PoolBetHistoryComponent');
    });
  });

  describe('CongratsBanner', () => {
    let bet;
    beforeEach(() => {
      component.celebration = {
        displayCelebrationBanner: true,
        duration: 240000000000,
        winningMessage: 'You have won {amount}!!',
        cashoutMessage: 'You have cashedout {amount}!!'
      };
      bet = {
        totalReturns: '6.00',
        stake: '5.00',
        bet: {
          settledAt: '2019-03-04 11:00:45',
          winnings: {
            value: '6.00'
          }
        },
        currency: '£'
      };
    });
    it('isCongratsBannerShown with bet', () => {
      expect(component.isCongratsBannerShown(bet)).toBeTrue();
    });
    it('isCongratsBannerShown with celebration as null', () => {
      component.celebration = null;
      expect(component.isCongratsBannerShown(bet)).toBe(undefined);
    });
    it('getReturnValue', () => {
      expect(component.getReturnValue(bet)).toBe('You have won 6.00£!!');
    });
    it('getReturnValue with celebration as null', () => {
      component.celebration = null;
      expect(component.getReturnValue(bet)).toBe(undefined);
    });
    it('getCashoutReturnValue', () => {
      expect(component.getCashoutReturnValue(bet)).toBe('You have cashedout 6.00£!!');
    });
    it('getCashoutReturnValue', () => {
      component.celebration = null;
      expect(component.getCashoutReturnValue(bet)).toBe(undefined);
    });
  });

  it('trackByBet should return unique identifier for bet object', () => {
    const bet = {
      id: 159,
      receipt: 'r/p121234234',
      isSuspended: true
    };
    expect(component.trackByBet(3, bet as any)).toEqual('3159r/p121234234true');
  });
  describe('ngOnInit',() => {
    it('should set noBetsMessage for Bet History tab', () => {
      component.isBetHistoryTab = true;
      component.ngOnInit();
      expect(component.noBetsMessage).toEqual('bethistory.noHistoryInfo');
    });
    it('should set noBetsMessage for Open Bets tab', () => {
      component.isBetHistoryTab = false;
      component.ngOnInit();
      expect(component.noBetsMessage).toEqual('bethistory.noOpenBets');
    });
  });
  describe('ngOnChanges', () => {
    it('ngOnChanges souldn`t init comopnent if no bets received', () => {
      spyOn(component as any, 'initializeBets');
      component.ngOnChanges({} as any);
      expect(component['initializeBets']).not.toHaveBeenCalled();
    });
    it('ngOnChanges sould init comopnent if bets received', () => {
      spyOn(component as any, 'initializeBets');
      component.ngOnChanges({ poolBets: {} } as any);
      expect(component['initializeBets']).toHaveBeenCalled();
    });
  });

  describe('generatePoolHistory', () => {
    it('initialize poolHistory with bet models', () => {
      expect(component.poolHistory.length).toEqual(0);
      component['generatePoolHistory']();
      expect(component.poolHistory.length).toEqual(2);
      expect(component.poolHistory[0].constructor.name).toEqual('TotePotPoolBetClass');
      expect(component.poolHistory[1].constructor.name).toEqual('TotePoolBet');
    });
    it('initialize poolHistory with bet models', () => {
      expect(component.poolHistory.length).toEqual(0);
      cmsService.getItemSvg.and.returnValue(of({}));
      component['generatePoolHistory']();
    });
  });
  describe('setSportIcon', () => {
    it('poolEntity as null', () => {
      component.poolHistory = [null];
      component.setSportIcon();
      expect(component.poolHistory).toEqual([null]);
    });
    it('poolEntity leg as null', () => {
      component.poolHistory = [{leg: null}] as any;
      component.setSportIcon();
      expect(component.poolHistory).toEqual([{leg: null}] as any);
    });
    it('poolEntity leg object as null', () => {
      component.poolHistory = [{leg: [null]}] as any;
      component.setSportIcon();
      expect(component.poolHistory).toEqual([{leg: [null]}] as any);
    });
    it('poolEntity leg part as null', () => {
      component.poolHistory = [{leg: [{part: [null]}]}] as any;
      component.setSportIcon();
      expect(component.poolHistory).toEqual([{leg: [{part: [null]}]}] as any);
    });
    it('poolEntity leg part outcome as null', () => {
      component.poolHistory = [{leg: [{part: [{outcome: null}]}]}] as any;
      component.setSportIcon();
      expect(component.poolHistory).toEqual([{leg: [{part: [{outcome: null}]}]}] as any);
    });
    it('poolEntity leg part outcome eventCategory as null', () => {
      component.poolHistory = [{leg: [{part: [{outcome: {eventCategory: null}}]}]}] as any;
      component.setSportIcon();
      expect(component.poolHistory).toEqual([{leg: [{part: [{outcome: {eventCategory: null}}]}]}] as any);
    });
  });
  describe('initializeBets', () => {
    it('should reinitialize component', () => {
      spyOn(component as any, 'generatePoolHistory');
      spyOn(component as any, 'unsubcribeFromLiveUpdates');
      spyOn(component as any, 'subscirbeForLiveUpdates');
      cmsService.getItemSvg.and.returnValue(of({}));
      component['initializeBets']();
      expect(component['generatePoolHistory']).toHaveBeenCalled();
      expect(component['unsubcribeFromLiveUpdates']).toHaveBeenCalled();
      expect(component['subscirbeForLiveUpdates']).toHaveBeenCalled();
    });
  });
  it('should call showFreeBetsToggle', () => {
    expect(component.showFreeBetsToggle('12')).toBeTrue();
  });

  it('should call getClassName', () => {
    expect(component.getClassName(true, false)).toEqual('single-left single-left-inline');
    expect(component.getClassName(true, true)).toEqual('single-left');
    expect(component.getClassName(false, true)).toEqual('single-left single-left-inline');
  });
});
