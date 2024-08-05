import { CorrectScoreComponent } from '@edp/components/markets/correctScore/correct-score.component';
import { eventOutcomesMock, groupeddata } from '@edp/mocks/correct-score.mock';
describe('CorrectScoreComponent', () => {
  let component: CorrectScoreComponent;

  let correctScoreService;
  let filterService;

  const outcome = {
    id: '123456',
    name: 'Outcome name'
  };
  const teamsMock = {
    teamA: {
      name: 'teamA name',
      score: 3
    },
    teamH: {
      name: 'teamH name',
      score: 5
    }
  };

  beforeEach(() => {
    correctScoreService = {
      getCombinedOutcome: jasmine.createSpy('getCombinedOutcome').and.returnValue(outcome),
      getMaxScoreValues: jasmine.createSpy('getMaxScoreValues'),
      getTeams: jasmine.createSpy('getTeams').and.returnValue(teamsMock),
    };
    filterService = {
      getScoreFromName: jasmine.createSpy('getScoreFromName'),
      groupBy: jasmine.createSpy('groupBy').and.returnValue([])
    };
    component = new CorrectScoreComponent(
      correctScoreService,
      filterService
    );
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  describe('isMarketOrEventSuspended', () => {
    beforeEach(() => {
      component.eventEntity = {
        eventStatusCode: ''
      } as any;
      component.market = {
        marketStatusCode: ''
      } as any;
    });

    it('to be true for not S status code', () => {
      expect(component.isMarketOrEventSuspended()).toEqual(false);
    });

    it('to be true for eventEntity eventStatusCode S', () => {
      component.eventEntity.eventStatusCode = 'S';
      expect(component.isMarketOrEventSuspended()).toEqual(true);
    });

    it('to be true for market marketStatusCode S', () => {
      component.market.marketStatusCode = 'S';
      expect(component.isMarketOrEventSuspended()).toEqual(true);
    });
  });

  describe('isButtonDisabled', () => {
    beforeEach(() => {
      component.isMarketOrEventSuspended = jasmine.createSpy().and.returnValue(false);
      component.combinedOutcome = {
        outcome: {
          outcomeStatusCode: 'any',
          prices: [{}]
        }
      } as any;
    });

    it('to be falsy', () => {
      expect(component.isButtonDisabled()).toBeFalsy();
    });

    it('to be truthy if isMarketOrEventSuspended', () => {
      component.isMarketOrEventSuspended = jasmine.createSpy().and.returnValue(true);
      expect(component.isButtonDisabled()).toBeTruthy();
    });

    it('to be truthy if for outcomeStatusCode S', () => {
      component.combinedOutcome.outcome.outcomeStatusCode = 'S';
      expect(component.isButtonDisabled()).toBeTruthy();
    });

    it('to be truthy if no outcome.prices', () => {
      delete (component.combinedOutcome.outcome.prices);
      expect(component.isButtonDisabled()).toBeTruthy();
    });

    it('to be truthy if outcome.prices empty', () => {
      component.combinedOutcome.outcome.prices = [];
      expect(component.isButtonDisabled()).toBeTruthy();
    });
  });

  describe('toggleShow', () => {
    beforeEach(() => {
      component.allShown = undefined;
    });

    it('should toggle allShown to false', () => {
      component.filterValueType = 'all';
      component.toggleShow();

      expect(component.filterValueType).toEqual('main');
      expect(component.allShown).toEqual(false);
    });

    it('should toggle allShown to true', () => {
      component.filterValueType = 'main';
      component.toggleShow();

      expect(component.filterValueType).toEqual('all');
      expect(component.allShown).toEqual(true);
    });
  });

  describe('isShowAllButton', () => {
    beforeEach(() => {
      component.eventEntity = {
        eventStatusCode: '',
        categoryId: 10
      } as any;
      component.groupedOutcomes = [[undefined, undefined, undefined, undefined, undefined], [undefined, undefined, undefined, undefined, undefined], [undefined, undefined, undefined, undefined, undefined]];
    });

    it('isShowAllButton should be false when outcomes is undefined', () => {
      component.groupedOutcomes = undefined;
      expect(component.isShowAllButton()).toEqual(undefined);
    });
    it('isShowAllButton should be false when home, draw and away team is present', () => {
      component.groupedOutcomes = [[undefined], [undefined], [undefined]];
      expect(component.isShowAllButton()).toEqual(false);
    });
    it('isShowAllButton should be false when home and away team is present', () => {
      component.groupedOutcomes = [[undefined], [undefined]];
      expect(component.isShowAllButton()).toEqual(false);
    });
    it('isShowAllButton should be false when home team is present', () => {
      component.groupedOutcomes = [[undefined]];
      expect(component.isShowAllButton()).toEqual(false);
    });
    it('isShowAllButton should be false when nothing is present', () => {
      component.groupedOutcomes = [undefined];
      expect(component.isShowAllButton()).toEqual(false);
    });
    it('isShowAllButton should be true when outcomes length is greater than 4', () => {
      expect(component.isShowAllButton()).toEqual(true);
    });
    it('isShowAllButton should be true when sport id is 22', () => {
      component.eventEntity = {
        eventStatusCode: '',
        categoryId: 22
      } as any;
      expect(component.isShowAllButton()).toEqual(true);
    });
    it('isShowAllButton should be true when sport id is 16', () => {
      component.eventEntity = {
        eventStatusCode: '',
        categoryId: 16
      } as any;
      expect(component.isShowAllButton()).toEqual(true);
    });
  });
    
  describe('onScoreChange', () => {
    let teamsObg;
    let eventEntity;

    beforeEach(() => {
      teamsObg = {
        teams: {
          teamA: {}
        }
      };
      component['marketOutcomes'] = [{
        id: '123'
      }] as any;
      eventEntity = {
        id: 56789
      };

      component.teamsObg = teamsObg as any;
      component.market = {outcomes: component['marketOutcomes']} as any;
      component.eventEntity = eventEntity as any;
    });

    it('should set score for team', () => {
      component.onScoreChange(5, 'teamA');

      expect(component.teamsObg.teams['teamA'].score).toEqual(5);
    });

    it('should set combinedOutcome from service', () => {
      component.onScoreChange();

      // eslint-disable-next-line max-len
      expect(correctScoreService.getCombinedOutcome).toHaveBeenCalledWith(teamsObg.teams, component['marketOutcomes'], eventEntity, component.market);
      expect(component.combinedOutcome.outcome).toEqual(outcome as any);
    });
  });

  it('getMaxValues', () => {
    component['marketOutcomes'] = [{
        id: '123'
      }] as any;
    component.getMaxValues();

    expect(correctScoreService.getMaxScoreValues).toHaveBeenCalledWith(component['marketOutcomes']);
  });

  it('filteredName if ', () => {
    const entity = {
     name: 'some name',
     outcomeMeaningScores: '1,2'
    } as any;
    component.filteredName(entity);

    expect(filterService.getScoreFromName).toHaveBeenCalledWith(entity.name);
  });

  it('filteredName else ', () => {
    const entity = {
     name: 'some name',
     outcomeMeaningScores: null
    } as any;
   const result =  component.filteredName(entity);
   expect(result).toEqual(entity.name);
  });

  it('trackByIndex', () => {
    const index = 1;
    const result = component.trackByIndex(index);
    expect(result).toBe(index);
  });

  it('ngOnInit', () => {
    component.marketGroup = {} as any;
    component['anyOtherMarkets'] = [{
      outcomeMeaningScores: null,
      originalOutcomeMeaningMinorCode:'O',
      outcomeMeaningMinorCode: NaN
    }] as any;
    component.market = { outcomes: [{
      outcomeMeaningScores: '2,0'
    }, {
      outcomeMeaningScores: '0,2'
    }, {}] } as any;
    filterService.groupBy.and.returnValue(groupeddata);
    spyOn(component, 'onScoreChange');
    spyOn(component, 'getMaxValues').and.returnValue({
      teamH: [{} as any],
      teamA: [{} as any]
    });
    component['getScoredOutcome'] = jasmine.createSpy('getScoredOutcome').and.returnValue(component.market.outcomes);
    component['getDefaultArray'] = jasmine.createSpy('getDefaultArray');
    component.ngOnInit();
    expect(component.groupedOutcomes.length).not.toBe(0);
    expect(component.market).not.toBeNull();
    expect(component['getScoredOutcome']).toHaveBeenCalled();
    expect(component.filterValueType).toEqual('main');
    expect(correctScoreService.getTeams).toHaveBeenCalledWith(component.marketGroup);
    expect(component.getMaxValues).toHaveBeenCalledTimes(4);
  });

  it('ngOnInit', () => {
    component.marketGroup = {} as any;
    component['anyOtherMarkets'] = [{
      outcomeMeaningScores: null,
      originalOutcomeMeaningMinorCode:'H',
      outcomeMeaningMinorCode: 1
    }] as any;
    component.market = { outcomes: [{
      outcomeMeaningScores: '2,0'
    }, {
      outcomeMeaningScores: '0,2'
    }, {}] } as any;
    filterService.groupBy.and.returnValue(groupeddata);
    spyOn(component, 'onScoreChange');
    spyOn(component, 'getMaxValues').and.returnValue({
      teamH: [{} as any],
      teamA: [{} as any]
    });
    component['getScoredOutcome'] = jasmine.createSpy('getScoredOutcome').and.returnValue(component.market.outcomes);
    component['getDefaultArray'] = jasmine.createSpy('getDefaultArray');
    component.ngOnInit();
    // @ts-ignore
    expect(component.groupedOutcomes.length).not.toBe(0);
  });

  it('ngOnInit grouped object', () => {
    component.marketGroup = {} as any;
    component['anyOtherMarkets'] = [] as any;
    component['marketOutcomes'] = [] as any;
    component.market = { outcomes: [{
      outcomeMeaningScores: '2,0'}, {  outcomeMeaningScores: '0,2'  }, {}] } as any;
    filterService.groupBy.and.returnValue({1:[],2:[], 3:[]});
    spyOn(component, 'onScoreChange');
    spyOn(component, 'getMaxValues').and.returnValue({
      teamH: [{} as any],
      teamA: [{} as any]
    });
    component['getScoredOutcome'] = jasmine.createSpy('getScoredOutcome').and.returnValue(component.market.outcomes);
    component['getDefaultArray'] = jasmine.createSpy('getDefaultArray');
    component.ngOnInit();
    // @ts-ignore
    expect(component.groupedOutcomes.length).toBe(0);
  });

  it('should test changeAccordionState state changings', () => {
    component.changeAccordionState(true);
    expect(component.isExpanded).toBeTruthy();
    component.changeAccordionState(false);
    expect(component.isExpanded).toBeFalsy();
  });

  it('#getScoredOutcome', () => {
    component.market = eventOutcomesMock;
    const filters: string[] = ['H','D','A','O'];
    component['getScoredOutcome'](component.market.outcomes);
    expect(component.market.outcomes.length).not.toBe(0);
  });

  it('#getDefaultArray', () => {
    component.defaultOutcomes = [];
    component['getDefaultArray']([eventOutcomesMock.outcomes]);
    expect(component.defaultOutcomes.length).not.toBe(0);
  });

});
