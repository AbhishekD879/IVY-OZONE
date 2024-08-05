import { MarketsGroupComponent } from '@edp/components/marketsGroup/markets-group.component';
import { of as observableOf } from 'rxjs';

describe('MarketsGroupComponent', () => {
  let component: MarketsGroupComponent;
  let pubSubService;
  let changeDetectorRef;
  let cmsService;

  beforeEach(() => {
    pubSubService = {
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      API: {
        OUTCOME_UPDATED: 'OUTCOME_UPDATED'
      }
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        FootballAggregationMarkets: {
          marketNames: ['test']
        }
      }))
    };

    component = new MarketsGroupComponent(
      pubSubService,
      changeDetectorRef,
      cmsService
    );

    component.marketsGroup = { header: [{ sortOrder: 1 }, { sortOrder: 2 }] } as any;
  });

  describe('selectPeriod', () => {
    const periodIndex = 100;

    beforeEach(() => {
      component.periodIndex = undefined;
      component['marketCount'] = undefined;
      component.isAllShow = undefined;
      component.limitCount = undefined;
    });

    it('should not set isAllShow and limitCount', () => {
      component['selectPeriod'](periodIndex);

      expect(component.periodIndex).toBe(periodIndex);
      expect(component.isAllShow).toBeUndefined();
      expect(component.limitCount).toBeUndefined();
    });

    it('should set isAllShow and limitCount', () => {
      component['marketCount'] = 5;
      component['selectPeriod'](periodIndex);

      expect(component.periodIndex).toBe(periodIndex);
      expect(component.isAllShow).toEqual(false);
      expect(component.limitCount).toEqual(component['marketCount']);
    });
  });

  it('trackByFn', () => {
    const index = 5;
    expect(component.trackByFn(index)).toBe(index);
  });

  it('should test changeAccordionState state changings', () => {
    component.changeAccordionState(true);
    expect(component.isExpanded).toBeTruthy();
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();

    component.changeAccordionState(false);
    expect(component.isExpanded).toBeFalsy();
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
  });

  describe('toggleShow', () => {
    beforeEach(() => {
      spyOn(component, 'marketsLength').and.returnValue(10);
      component['marketCount'] = 5;
    });

    it('should toggle isAllShow from true to false', () => {
      component.isAllShow = false;
      component.toggleShow();
      expect(component.isAllShow).toEqual(true);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should toggle isAllShow from false to true', () => {
      component.isAllShow = true;
      component.toggleShow();
      expect(component.isAllShow).toEqual(false);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should limitCount as marketCount', () => {
      component.isAllShow = true;
      component.toggleShow();
      expect(component.limitCount).toEqual(5);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });

    it('should limitCount as marketsLength', () => {
      component.isAllShow = false;
      component.toggleShow();
      expect(component.limitCount).toEqual(10);
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  describe('marketsLength', () => {
    let marketPeriodsItem;
    let marketPeriods;
    let marketsGroupItem;
    let marketsGroup;

    beforeEach(() => {
      marketPeriodsItem = {
        outcomes: [{}, {}]
      };
      marketPeriods = [{
        markets: [marketPeriodsItem, {}]
      }];

      marketsGroupItem = {
        outcomes: [{}, {}, {}]
      };
      marketsGroup = {
        markets: [marketsGroupItem, {}, {}],
        periods: marketPeriods as any
      };

      component['marketsGroup'] = marketsGroup as any;
      component.periodIndex = 0;
      component.isMarketHeader = false;
    });

    describe('if is NOT isMarketHeader', () => {
      it('should return marketPeriods[periodIndex].markets[0].outcomes.length', () => {
        const result = component.marketsLength();

        expect(result).toBe(marketPeriodsItem.outcomes.length);
      });

      it('should return marketsGroup.markets[0].outcomes.length', () => {
        component.marketsGroup.periods = null;
        const result = component.marketsLength();

        expect(result).toBe(marketsGroupItem.outcomes.length);
      });
    });

    describe('if is isMarketHeader', () => {
      beforeEach(() => {
        component.isMarketHeader = true;
        component['marketNoGoal'] = {} as any;
      });

      it('and is marketNoGoal should return marketPeriods[0].markets.length + 1', () => {
        const result = component.marketsLength();

        expect(result).toBe(marketPeriods[0].markets.length + 1);
      });

      it('and is marketNoGoal should return marketsGroup.markets.length + 1', () => {
        component.marketsGroup.periods = null;
        const result = component.marketsLength();

        expect(result).toBe(marketsGroup.markets.length + 1);
      });

      it('and is no marketNoGoal should return marketPeriods[0].markets.length', () => {
        component['marketNoGoal'] = null;
        const result = component.marketsLength();

        expect(result).toBe(marketPeriods[0].markets.length);
      });

      it('and is no marketNoGoal should return marketsGroup.markets.length', () => {
        component.marketsGroup.periods = null;
        component['marketNoGoal'] = null;
        const result = component.marketsLength();

        expect(result).toBe(marketsGroup.markets.length);
      });
    });
  });

  describe('selectedOutcomes', () => {
    let outcomes;

    beforeEach(() => {
      outcomes = [{ id: 1 }, { id: 2 }, { id: 3 }, { id: 4 }] as any;
    });

    it('should be equal input parameter', () => {
      component['marketCount'] = 0;
      const result = component.selectedOutcomes(outcomes);

      expect(result).toEqual(outcomes);
    });

    it('should slice outcomes by marketCount', () => {
      component['marketCount'] = 2;
      component.limitCount = 0;
      const result = component.selectedOutcomes(outcomes);

      expect(result.length).toEqual(2);
    });

    it('should slice outcomes by limitCount', () => {
      component['marketCount'] = 2;
      component.limitCount = 3;
      const result = component.selectedOutcomes(outcomes);

      expect(result.length).toEqual(3);
    });
  });

  describe('selectedOutcomes', () => {
    let marketPeriodsItem;
    let marketPeriods;
    let marketsGroupItem;
    let marketsGroup;

    beforeEach(() => {
      marketPeriodsItem = {
        outcomes: [{}, {}]
      };
      marketPeriods = [{
        markets: [marketPeriodsItem, {}, {}, {}, {}, {}, {}, {}]
      }];

      marketsGroupItem = {
        outcomes: [{}, {}, {}]
      };
      marketsGroup = {
        markets: [marketsGroupItem, {}, {}],
        periods: marketPeriods as any
      };

      component['marketsGroup'] = marketsGroup as any;
    });

    describe('if not hasMarketCount', () => {
      beforeEach(() => {
        component['marketCount'] = 0;
        component.isMarketHeader = false;
      });

      it('should be marketPeriods[0].markets', () => {
        const result = component.selectedMarkets(0);

        expect(result).toEqual(marketPeriods[0].markets);
      });

      it('should be marketsGroup.markets', () => {
        component.marketsGroup.periods = null;
        const result = component.selectedMarkets(0);

        expect(result).toEqual(marketsGroup.markets);
      });
    });

    describe('if hasMarketCount', () => {
      beforeEach(() => {
        component['marketCount'] = 1;
        component.isMarketHeader = true;
      });

      it('should be sliced by marketCount', () => {
        component['marketCount'] = 2;
        component.limitCount = 0;
        const result = component.selectedMarkets(0);

        expect(result.length).toEqual(2);
      });

      it('should be should be sliced by limitCount', () => {
        component['marketCount'] = 2;
        component.limitCount = 3;
        const result = component.selectedMarkets(0);

        expect(result.length).toEqual(3);
      });
    });

    describe('if hasMarketCount', () => {
      beforeEach(() => {
        component['marketCount'] = 0;
        component.isMarketHeader = false;
      });

      it('should not be sliced', () => {
        const result = component.selectedMarkets(0);
        expect(result.length).toEqual(marketPeriods[0].markets.length);
      });

      it('should not be sliced if no marketCount but only isMarketHeader', () => {
        component['marketCount'] = 1;
        const result = component.selectedMarkets(0);

        expect(result.length).toEqual(marketPeriods[0].markets.length);
      });

      it('should not be sliced if not isMarketHeader but only marketCount', () => {
        component.isMarketHeader = true;
        const result = component.selectedMarkets(0);

        expect(result.length).toEqual(marketPeriods[0].markets.length);
      });

      it('should be sliced', () => {
        component['marketCount'] = 1;
        component.limitCount = 3;
        component.isMarketHeader = true;
        const result = component.selectedMarkets(0);

        expect(result.length).toEqual(3);
      });
    });
  });

  it('trackById', () => {
    const result = component.trackById(0, { id: '111' } as any);
    expect(result).toBe(111);
  });

  describe('getMarketOutcomes', () => {
    let market;

    beforeEach(() => {
      market = {
        outcomes: [{ id: 111 }, { id: 222 }]
      };
      component.marketsGroup = {
        localeName: 'any local name'
      } as any;
    });

    it('should not reverse markets if no index', () => {
      spyOn<any>(component, 'removeUnusedFakes').and.returnValue(market.outcomes);

      expect(component.getMarketOutcomes(market, 0)).toEqual(market.outcomes);

      expect(component.getMarketOutcomes(market, 1)).toEqual(market.outcomes);

      component.marketsGroup.localeName = 'playerToScoreResult';
      expect(component.getMarketOutcomes(market, 0)).toEqual(market.outcomes);

      component.marketsGroup.localeName = 'playerToScoreFirst';
      expect(component.getMarketOutcomes(market, 0)).toEqual(market.outcomes);
    });

    it('should reverse markets', () => {
      spyOn<any>(component, 'removeUnusedFakes').and.returnValue(market.outcomes.slice().reverse());

      component.marketsGroup.localeName = 'playerToScoreResult';
      expect(component.getMarketOutcomes(market, 1)).toEqual(market.outcomes.slice().reverse());

      component.marketsGroup.localeName = 'playerToScoreResult';
      expect(component.getMarketOutcomes(market, 1)).toEqual(market.outcomes.slice().reverse());
    });
  });

  describe('showLessButton', () => {

    it('should be true', () => {
      spyOn(component, 'marketsLength').and.returnValue(100);
      component['marketCount'] = 5;
      expect(component.showLessButton).toBe(true);
    });

    it('should be false', () => {
      spyOn(component, 'marketsLength').and.returnValue(100);

      component['marketCount'] = 200;
      expect(component.showLessButton).toBe(false);

      component['marketCount'] = 100;
      expect(component.showLessButton).toBe(false);

      component['marketCount'] = 0;
      expect(component.showLessButton).toBe(false);
    });
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('MarketsGroupComponent');
  });

  describe('ngOnInit', () => {
    let marketsGroup;

    beforeEach(() => {
      marketsGroup = {
        header: {},
        template: 'cardHeader',
        periods: [],
        type: 'teams',
        noGoalscorer: null,
        lessCount: 10
      };

      component.marketsGroup = marketsGroup as any;
    });

    it('should define fields', () => {
      component.ngOnInit();

      expect(component.isMarketHeader).toBeDefined();
      expect(component.marketNoGoal).toBeDefined();
      expect(component.marketsGroup.periods).toBeDefined();
      expect(component.isMarketCard).toBeDefined();
      expect(component.isMarketRow).toBeDefined();
      expect(component['isMarketTeams']).toBeDefined();
      expect(component['marketCount']).toBeDefined();
    });

    describe('isMarketHeader should be', () => {
      it('true for cardHeader template and header', () => {
        component.ngOnInit();
        expect(component.isMarketHeader).toEqual(true);
      });

      it('falsy if no header', () => {
        component.marketsGroup.header = null;
        component.ngOnInit();

        expect(component.isMarketHeader).toBeFalsy();
      });

      it('falsy for not cardHeader template', () => {
        component.marketsGroup.template = 'any';
        component.ngOnInit();

        expect(component.isMarketHeader).toBeFalsy();
      });

      it('marketName from CMS', () => {
        component.marketsGroup.header = [{name: 'header1', sortOrder: 1},{name: 'header2', sortOrder: 1}];
        component.marketsGroup.name = 'test';
        cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
          FootballAggregationMarkets: {marketNames:['test']}
        }));
        component.ngOnInit();
        expect(component['marketNames']).toEqual(['test']);
      });
    });

    describe('isMarketCard should be', () => {
      it('true for card template', () => {
        component.marketsGroup.template = 'card';
        component.ngOnInit();
        expect(component.isMarketCard).toEqual(true);
      });

      it('false for not card template', () => {
        component.marketsGroup.template = 'any';
        component.ngOnInit();

        expect(component.isMarketCard).toEqual(false);
      });
    });

    describe('isMarketRow should be', () => {
      it('true for row template', () => {
        component.marketsGroup.template = 'row';
        component.ngOnInit();
        expect(component.isMarketRow).toEqual(true);
      });

      it('false for not row template', () => {
        component.marketsGroup.template = 'any';
        component.ngOnInit();

        expect(component.isMarketRow).toEqual(false);
      });
    });

    describe('isMarketTeams should be', () => {
      it('true for teams type', () => {
        component.marketsGroup.type = 'teams';
        component.ngOnInit();
        expect(component['isMarketTeams']).toEqual(true);
      });

      it('falsy for teamSwitch type', () => {
        component.marketsGroup.type = 'teamSwitch';
        component.ngOnInit();
        expect(component['isMarketTeams']).toEqual(true);
      });

      it('falsy if type not teams|teamSwitch', () => {
        component.marketsGroup.type = 'group';
        component.ngOnInit();
        expect(component['isMarketTeams']).toBeFalsy();
      });

      it('falsy if no type', () => {
        component.marketsGroup.type = undefined;
        component.ngOnInit();
        expect(component['isMarketTeams']).toBeFalsy();
      });
    });

    describe('marketCount should be', () => {
      it('equal lessCount', () => {
        component.marketsGroup.noGoalscorer = null;
        component.ngOnInit();
        expect(component['marketCount']).toEqual(marketsGroup.lessCount);
      });

      it('equal lessCount - 1', () => {
        component.marketsGroup.noGoalscorer = {} as any;
        component.ngOnInit();
        expect(component['marketCount']).toEqual(marketsGroup.lessCount - 1);
      });
    });

    it('should call subscribe on pubSubService', () => {
      component.ngOnInit();
      expect(pubSubService.subscribe)
        .toHaveBeenCalledWith('MarketsGroupComponent', pubSubService.API.OUTCOME_UPDATED, jasmine.any(Function));
    });

    it('should not fill switchers', () => {
      component.marketsGroup.periods = null;
      component.ngOnInit();
      expect(component.switchers.length).toEqual(0);
    });

    it('should fill switchers from periods with localeName', () => {
      component.marketsGroup.periods = [{ localeName: 'Market #1' }, {}] as any;
      component.ngOnInit();
      expect(component.switchers.length).toEqual(1);
    });

    it('should update outcomes status', () => {
      const market: any = { outcomes: [{}], marketStatusCode: 'A' };
      pubSubService.subscribe.and.callFake((p1, p2, cb) => cb(market));
      component.ngOnInit();
      expect(market.outcomes[0].marketStatusCode).toEqual(market.marketStatusCode);
    });

    it('should not update outcomes status', () => {
      const market: any = {};
      pubSubService.subscribe.and.callFake((p1, p2, cb) => cb(market));
      component.ngOnInit();
      expect(market.outcomes).not.toBeDefined();
    });

    it('should select perido when switcher clicked', () => {
      spyOn(component as any, 'selectPeriod');
      component.marketsGroup.type = '';
      component.marketsGroup.periods = [{ localeName: 'mkt' }] as any;
      component.ngOnInit();
      component.switchers[0].onClick();
      expect(component['selectPeriod']).toHaveBeenCalledTimes(1);
    });
  });

  it('should filter removeUnusedFakes', () => {
    const outcomes = [{ sortOrder: 1 }, { sortOrder: 3 }, { sortOrder: 1 }, { sortOrder: 3 }, { sortOrder: 2 }] as any;

    expect(component['removeUnusedFakes'](outcomes).length).toEqual(3);
  });

  describe('ShowHeaders:', () => {
    it('With marketName: header for aggregation markets, if 2 or less markets', () => {
      component.marketsGroup.header = [{name: 'header1', sortOrder: 1},{name: 'header2', sortOrder: 1}];
      component.marketsGroup.name = 'test';
      component['marketNames'] = ['test'];
      expect(component.showHeader()).toBeTruthy();
    });
    it('Without marketName:No header for aggregation markets, if 2 or less markets', () => {
      component.marketsGroup.header = [{name: 'header1', sortOrder: 1},{name: 'header2', sortOrder: 1}];
      component.marketsGroup.name = 'test';
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        FootballAggregationMarkets: {}
      }));
      expect(component.showHeader()).toBeFalsy();
    });
    it('Without marketName#2:No header for aggregation markets, if 2 or less markets', () => {
      component.marketsGroup.header = [{name: 'header1', sortOrder: 1},{name: 'header2', sortOrder: 1}];
      component.marketsGroup.name = 'test';
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        FootballAggregationMarkets: {}
      }));
      component['marketNames'] = undefined;
      expect(component.showHeader()).toBeFalsy();
    });
    it('Without marketName#3:No header for aggregation markets, if 2 or less markets', () => {
      component.marketsGroup.header = [{name: 'header1', sortOrder: 1},{name: 'header2', sortOrder: 1}];
      component.marketsGroup.name = 'test';
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        FootballAggregationMarkets: {}
      }));
      component['marketNames'] = null;
      expect(component.showHeader()).toBeFalsy();
    }); 
    
    it('Without Header attributes:No header for aggregation markets', () => {
      component.marketsGroup.header = undefined;
      component.marketsGroup.name = 'test';
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        FootballAggregationMarkets: {marketNames: ['test']}
      }));
      component['marketNames'] = ['test'];
      expect(component.showHeader()).toBeFalsy();
    });
  });
});
