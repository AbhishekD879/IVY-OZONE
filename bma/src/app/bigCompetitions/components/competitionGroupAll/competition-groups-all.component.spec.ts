import {
  CompetitionGroupAllComponent
} from '@app/bigCompetitions/components/competitionGroupAll/competition-groups-all.component';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IGroupTeam } from '@app/bigCompetitions/models/big-competitions.model';
import * as _ from 'underscore';

describe('CompetitionGroupAllComponent', () => {
  let component: CompetitionGroupAllComponent;

  let bigCompetitionLiveUpdatesService;

  let moduleConfig;
  let events;

  beforeEach(() => {
    moduleConfig = {
      id: 'id',
      name: 'name',
      type: '',
      maxDisplay: 10,
      viewType: 'inplay',
      aemPageName: '',
      isExpanded: false,
      markets: [],
      specialModuleData: {
        typeIds: [],
        eventIds: [],
        linkUrl: ''
      },
      groupModuleData: {
        sportId: 12,
        areaId: 32,
        competitionId: 34,
        seasonId: 43,
        numberQualifiers: 11,
        details: null,
        data: [
          {
            competitionId: 32,
            seasonId: 32443,
            tableId: 43,
            tableName: '',
            teams: [],
            ssEvents: []
          }
        ]
      },
      events: [],
      errors: [],
      results: []
    };
    events = [
      {
        markets : [
          {
            id: '1',
            templateMarketName : 'Match Betting',
            outcomes : [1, 2, 3] as any
          },
          {
            id: '2',
            templateMarketName : 'To Win To Nil',
            outcomes : [1, 2, 3] as any
          },
          {
            id: '3',
            templateMarketName : 'Draw No Bet',
            outcomes : [1, 2, 3] as any
          },
          {
            id: '4',
            templateMarketName : 'Match Betting',
            outcomes : [1, 2] as any
          },
        ]
      },
      {
        markets : [
          {
            id: '1',
            templateMarketName : 'Match Betting',
            outcomes : [1, 2, 3] as any
          },
          {
            id: '2',
            templateMarketName : 'To Win To Nil',
            outcomes : [1, 2, 3] as any
          },
          {
            id: '3',
            templateMarketName : 'Draw No Bet',
            outcomes : [1, 2, 3] as any
          },
          {
            id: '4',
            templateMarketName : 'Match Betting',
            outcomes : [1, 2] as any
          },
        ]
      }
    ] as ISportEvent[];

    bigCompetitionLiveUpdatesService = {
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy()
    };

    component = new CompetitionGroupAllComponent(bigCompetitionLiveUpdatesService);
    component.moduleConfig = moduleConfig;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
    expect(component.id).toContain('GroupAllComponent-');
  });



  describe('#ngOnInit', () => {
    it('should call the main methods and initialise props', () => {
      component.ngOnInit();
      expect(component.moduleConfig.isExpanded).toBeTruthy();
      expect(component.numberQualifiers).toBe(moduleConfig.groupModuleData.numberQualifiers);
      expect(component.group).toBe(moduleConfig.groupModuleData.data[0]);
      expect(component.events).toBe(component.group.ssEvents);
    });

    it('should set [] to markets and set nothing to events', () => {
      component.moduleConfig.groupModuleData.data = [{}] as any;
      spyOn(_, 'pluck').and.returnValue({} as any);
      spyOn(_, 'flatten').and.returnValue(undefined);

      component.ngOnInit();
      expect(component.events).toBe(undefined);
      expect(component.markets).toEqual([]);
    });
  });

  it('should return correct class name', () => {
    component.numberQualifiers = 5;
    const index = 2;
    const className = component.getQualifiedClass(index);
    expect(className).toBe('team-qualified');
  });

  it('should return correct class name', () => {
    component.numberQualifiers = 5;
    const index = 5;
    const className = component.getQualifiedClass(index);
    expect(className).toBe('');
  });

  it('should return correct result', () => {
    const element = {
      id: '1',
      templateMarketName : 'Match Betting',
      outcomes : [1, 2, 3] as any
    };
    const i = 5;
    expect(component.trackByMarket(i, element as IMarket)).toBe('5_1');
  });

  it('should return correct result', () => {
    const element = {
      name: 'name',
      obName: 'obName'
    } as IGroupTeam;
    const i = 3;
    expect(component.trackByTeam(i, element)).toBe('3_name');
  });

  it('should return true', () => {
    const market = {
      outcomes: [{ name: '' }],
      isDisplayed: true
    } as IMarket;
    const event = { ...events[0], isDisplayed: true };
    const index = 5;
    component.getSeln = jasmine.createSpy().and.returnValue({ isDisplayed: true });
    expect(component.isSelnDisplayed(event, market, index)).toBeTruthy();
    expect(component.getSeln).toHaveBeenCalledWith(market, index);
  });

  it('should return false', () => {
    const market = {
      outcomes: null,
      isDisplayed: true
    } as IMarket;
    const event = { ...events[0], isDisplayed: true };
    const index = 5;
    component.getSeln = jasmine.createSpy().and.returnValue({ isDisplayed: true });
    expect(component.isSelnDisplayed(event, market, index)).toBeFalsy();
  });

  it('should return corresponding outcome', () => {
    const market = {
      outcomes: [
        { name: 'name0' },
        { name: 'name1' },
        { name: 'name2' },
        { name: 'name3' }
      ],
      isDisplayed: true
    } as IMarket;
    const group = {
      competitionId: 32,
      seasonId: 12,
      tableId: 43,
      tableName: 'tableName',
      teams: [
        {
          name: 'name1',
          obName: 'obName1'
        },
        {
          name: 'name2',
          obName: 'obName2'
        }
      ],
      ssEvents: []
    };
    component.group = group;
    const result = component.getSeln(market, 1);
    expect(result).toBe(market.outcomes[2]);
  });

  it('should toggle isExpanded property and call correct methods', () => {
    component.events = events;
    component.moduleConfig.isExpanded = false;
    component.accordionHandler();
    expect(component.moduleConfig.isExpanded).toBeTruthy();
    expect(bigCompetitionLiveUpdatesService.subscribe).toHaveBeenCalledWith(component.events);
  });

  it('should toggle isExpanded property and call correct methods', () => {
    component.events = events;
    component.moduleConfig.isExpanded = true;
    component.accordionHandler();
    expect(component.moduleConfig.isExpanded).toBeFalsy();
    expect(bigCompetitionLiveUpdatesService.unsubscribe).toHaveBeenCalledWith(component.events);
  });
});
