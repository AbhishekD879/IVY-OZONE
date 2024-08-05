import { of as observableOf, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { commandApi } from '@core/services/communication/command/command-api.constant';
import { BetFinderResultComponent } from './bet-finder-result.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import * as _ from 'underscore';

describe('BetFinderResultComponent', () => {
  let component: BetFinderResultComponent;

  let storageService;
  let deviceService;
  let cmsService;
  let betSlipSelectionsDataService;
  let changeDetRef;
  let commandService;
  let windowRefService;
  let localeService;
  let filtersService;
  let domToolsService;
  let pubSubService;
  let gtm;
  let betFinderHelperService;
  let runnersData;
  let userService;
  let raceOutcomeDetailsService;

  beforeEach(() => {
    runnersData = [{
      horseName: 'Borys2',
      time: '3:20',
      number: '01',
      decimalOdds: 5,
      odds: '3/2'
    }, {
      horseName: 'Borys',
      time: '1:20',
      number: '01',
      decimalOdds: 7,
      odds: '6/1'
    },
    {
      horseName: 'Borys',
      time: '1:30',
      number: '01',
      decimalOdds: 0,
      odds: ''
    }] as any;
    storageService = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set')
    };
    deviceService = {
      isMobile: true
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf({
        Betslip: {
          maxBetNumber: 10
        }
      }))
    };
    betSlipSelectionsDataService = {
      count: jasmine.createSpy().and.returnValue(1),
      getSelectionsByOutcomeId: jasmine.createSpy().and.returnValue([1, 2, 3])
    };
    changeDetRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
      detach: jasmine.createSpy('detach'),
    };
    commandService = {
      executeAsync: jasmine.createSpy().and.returnValue(Promise.resolve()),
      API: commandApi
    };
    windowRefService = {
      nativeWindow: {
        setInterval: jasmine.createSpy('setInterval').and.callFake((fn) => fn && fn()),
        clearInterval: jasmine.createSpy('clearInterval'),
        pageYOffset: 0,
        frameElement: {
          nodeName: 'IFRAME'
        },
      },
      document: {
        documentElement: {
          querySelector: jasmine.createSpy('querySelector').and.returnValue({})
        },
        body: {},
      }
    };
    localeService = {
      getString: jasmine.createSpy().and.returnValue('test locale')
    };
    filtersService = {
      removeLineSymbol: jasmine.createSpy('removeLineSymbol').and.callFake(v => v)
    };
    domToolsService = {
      hasClass: jasmine.createSpy('hasClass').and.returnValue(false),
      css: jasmine.createSpy('css'),
      addClass: jasmine.createSpy('addClass'),
      removeClass: jasmine.createSpy('removeClass'),
      getOffset: jasmine.createSpy('getOffset').and.returnValue(true)
    };
    pubSubService = {
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    gtm = {
      push: jasmine.createSpy()
    };
    betFinderHelperService = {
      getRunners: jasmine.createSpy().and.returnValue(observableOf(runnersData))
    };
    userService = {
      oddsFormat: 'dec'
    };
    raceOutcomeDetailsService = {
      getSilkStyle: jasmine.createSpy('getSilkStyle')
    };

    component = new BetFinderResultComponent(
      storageService,
      deviceService,
      cmsService,
      betSlipSelectionsDataService,
      commandService,
      windowRefService,
      localeService,
      filtersService,
      domToolsService,
      pubSubService,
      gtm,
      betFinderHelperService,
      changeDetRef,
      userService,
      raceOutcomeDetailsService
    );
  });

  it('should create component with document as body', () => {
    windowRefService.document.documentElement = null;
    windowRefService.document.body = {};
    const cmp = new BetFinderResultComponent(
      storageService,
      deviceService,
      cmsService,
      betSlipSelectionsDataService,
      commandService,
      windowRefService,
      localeService,
      filtersService,
      domToolsService,
      pubSubService,
      gtm,
      betFinderHelperService,
      changeDetRef,
      userService,
      raceOutcomeDetailsService
    );
    expect(cmp['document']).toBe(windowRefService.document.body);
  });

  describe('default init flow', () => {
    it('ngOnInit', fakeAsync(() => {
      component.ngOnInit();
      tick(component['intervalValue']);

      expect(changeDetRef.detach).toHaveBeenCalled();
      expect(changeDetRef.detectChanges).toHaveBeenCalled();
      expect(storageService.get).toHaveBeenCalledTimes(1);
      expect(storageService.get).toHaveBeenCalledWith('bfResultsSorting');
      expect(betFinderHelperService.getRunners).toHaveBeenCalledTimes(1);
      expect(component.sortingOrder).toEqual('time');
      expect(component.runners[0].oddsToDisplay).toBe('7.00');
    }));

    it('ngOnDestroy', () => {
      component['timeOutListener'] = () => {};
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalledTimes(1);
      expect(pubSubService.unsubscribe).toHaveBeenCalledWith('bet_finder');
      expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalledWith(component['timeOutListener']);
    });

    it('onWindowScroll', () => {
      component.onWindowScroll();
      expect(windowRefService.document.documentElement.querySelector).toHaveBeenCalledTimes(1);
      expect(windowRefService.document.documentElement.querySelector).toHaveBeenCalledWith('.bet-animation');
      expect(domToolsService.removeClass).toHaveBeenCalledWith(jasmine.anything(), 'bet-visible');
    });

    it('trackByIndex', () => {
      expect(component.trackByIndex(1)).toEqual(1);
    });

    it('animation', () => {
      const eventMock = {
        currentTarget: {}
      };
      component.maxBetsAmount = 2;

      component['animation'](<any>eventMock, '123456');

      expect(domToolsService.addClass).toHaveBeenCalledTimes(2);
    });

    it('initializeBreadcrumbs', () => {
      const breadcrumbsItems = [{
        name: 'test locale',
        targetUri: '/horse-racing'
      }, {
        name: 'test locale'
      }];
      component['initializeBreadcrumbs']();
      expect(component.breadcrumbsItems).toEqual(breadcrumbsItems);
    });
  });

  describe('update silk aggregated styles', () => {
    it('should NOT call corresponding outer service method', () => {
      component['init']();

      expect(raceOutcomeDetailsService.getSilkStyle).not.toHaveBeenCalled();
    });

    it('should call corresponding outer service method', () => {
      const data = runnersData;
      data[0] = Object.assign({}, runnersData[0], { silkID: 'Silk.gif'});

      betFinderHelperService.getRunners = jasmine.createSpy().and.returnValue(observableOf(data));

      component['init']();
      expect(raceOutcomeDetailsService.getSilkStyle).toHaveBeenCalled();
    });
  });

  it('init - should handle error', () => {
    betFinderHelperService.getRunners = jasmine.createSpy().and.returnValue(throwError(null));
    component['init']();

    expect(component.state.loading).toEqual(false);
    expect(component.state.error).toEqual(true);
  });

  it('init', () => {
    const runnersResult = _.sortBy(runnersData, 'time') as any;
    component.sortingOrder = 'time';

    component['init']();
    runnersResult[0].oddsToDisplay = '7.00';
    runnersResult[1].oddsToDisplay = '5.00';
    runnersResult[2].oddsToDisplay = 'SP';

    expect(component.runnersData).toEqual(runnersData);
    expect(component.runners).toEqual(runnersResult);
  });

  it('triggerSortResults', () => {
    const runnersResult = _.sortBy(runnersData, 'time') as any;
    component.runnersData = runnersData;

    component['triggerSortResults']('time');

    runnersResult[0].oddsToDisplay = '7.00';
    runnersResult[1].oddsToDisplay = '5.00';
    runnersResult[2].oddsToDisplay = 'SP';

    expect(component.runners).toEqual(runnersResult);
  });

  describe('custom init flow', () => {
    it('should set oddsToDisplay in fractional format', () => {
      (component['userService'].oddsFormat as any) = 'frac';

      component.ngOnInit();

      expect(component.runners[0].oddsToDisplay).toBe('6/1');
      expect(component.runners[1].oddsToDisplay).toBe('SP');
      expect(component.runners[2].oddsToDisplay).toBe('3/2');
    });
  });

  describe('addToBetSlip', () => {
    beforeEach(() => {
      component['animation'] = () => observableOf({});
      spyOn(window.parent, 'postMessage');
    });

    it('should not add to betslip (no data)', fakeAsync(() => {
      component['animation'] = () => observableOf(null);
      component.addToBetSlip({} as any, '1');
      tick();
      expect(pubSubService.publish).not.toHaveBeenCalled();
      expect(window.parent.postMessage).not.toHaveBeenCalled();
    }));

    it('should add to betslip (via pubsub)', fakeAsync(() => {
      windowRefService.nativeWindow.frameElement = null;
      component.addToBetSlip({} as any, '1');
      tick();
      expect(pubSubService.publish).toHaveBeenCalledWith('ADD_TO_BETSLIP_BY_SELECTION', {});
      expect(window.parent.postMessage).not.toHaveBeenCalled();
    }));

    it('should add to betslip (via post message)', fakeAsync(() => {
      component.addToBetSlip({} as any, '1');
      tick();
      expect(pubSubService.publish).not.toHaveBeenCalled();
      expect(window.parent.postMessage).toHaveBeenCalledWith('iFrame:bet:{}', '*' as any);
    }));
  });

  describe('applyButtonClasses', () => {
    beforeEach(() => {
      betSlipSelectionsDataService.getSelectionsByOutcomeId.and.callFake(id => id === '1' ? [{}] : []);
    });

    it('should return active class', () => {
      expect(component.applyButtonClasses('1')).toBe('active');
    });

    it('should return empty class', () => {
      expect(component.applyButtonClasses('2')).toBe('');
    });
  });

  describe('sortResults', () => {
    it('shoud set order in storage and track gtm event', () => {
      component.sortingOrder = 'time';
      component.sortResults('odds');
      expect(storageService.set).toHaveBeenCalledWith('bfResultsSorting', 'odds');
      expect(gtm.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'bet finder',
        eventAction: 'sorting',
        eventLabel: `sort - by odds`
      });
    });

    it('shoud not set order in storage and track gtm event', () => {
      component.sortingOrder = 'time';
      component.sortResults('time');
      expect(storageService.set).not.toHaveBeenCalled();
      expect(gtm.push).not.toHaveBeenCalled();
    });
  });

  describe('init', () => {
    it('should set max bets amount', fakeAsync(() => {
      component['init']();
      tick();
      expect(component.maxBetsAmount).toBe(10);
    }));

    it('should not set max bets amount', fakeAsync(() => {
      cmsService.getSystemConfig.and.returnValue(observableOf({}));
      component['init']();
      tick();
      expect(component.maxBetsAmount).not.toBeDefined();
    }));
  });

  describe('setResultsNumber', () => {
    beforeEach(() => {
      localeService.getString.and.callFake(v => v);
    });

    it('should set no result message', () => {
      component['setResultsNumber'](0);
      expect(component.foundResult).toBe(' bf.noresults');
    });

    it('should set results message', () => {
      component['setResultsNumber'](1);
      expect(component.foundResult).toBe('1 bf.results');
    });
  });

  describe('animation', () => {
    it('should remove active class', () => {
      domToolsService.hasClass.and.returnValue(true);
      const event: any = { currentTarget: {} };
      component['animation'](event, '1');
      expect(domToolsService.removeClass).toHaveBeenCalledWith(event.currentTarget, 'active');
    });

    it('should call addGTMObject', fakeAsync(() => {
      commandService.executeAsync.and.returnValue( Promise.resolve([{}]) );
      spyOn(component as any, 'addGTMObject').and.callThrough();

      component['animation']({} as any, '1').subscribe();
      tick();

      expect(component['addGTMObject']).toHaveBeenCalledWith(
        { GTMObject: { selectionID: '1' } } as any, '1' );
    }));

    it('should not call addGTMObject', fakeAsync(() => {
      commandService.executeAsync.and.returnValue( Promise.resolve(null) );
      spyOn(component as any, 'addGTMObject');

      component['animation']({} as any, '1').subscribe();
      tick();

      expect(component['addGTMObject']).not.toHaveBeenCalled();
    }));
  });
});
