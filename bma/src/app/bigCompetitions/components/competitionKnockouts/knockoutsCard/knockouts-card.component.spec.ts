import {
  KnockoutsCardComponent
} from '@app/bigCompetitions/components/competitionKnockouts/knockoutsCard/knockouts-card.component';
import { IOutcome } from '@core/models/outcome.model';
import {
  ICompetitionMatchResult,
  IKnockoutEvent
} from '@app/bigCompetitions/services/bigCompetitions/big-competitions.model';

describe('KnockoutsCardComponent', () => {

  let component: KnockoutsCardComponent;

  let outcomeTemplateHelperService;
  let routingHelperService;
  let coreToolsService;
  let filterService;

  let cardEvent;
  let stage;
  const outcomes = [];

  beforeEach(() => {
    cardEvent = {
      eventId: 79,
      homeTeam: 'homeTeam',
      awayTeam: 'awayTeam',
      homeTeamRemark: 'homeTeamRemark',
      awayTeamRemark: 'awayTeamRemark',
      venue: '',
      startTime: '2019-01-30T09:44:06.550Z',
      round: '',
      abbreviation: 'F1',
      resulted: true,
      result: {
        score: [],
        aet: [],
        pen: []
      },
      eventName: 'eventName',
      obEvent: {
        cashoutAvail: '',
        categoryCode: '',
        categoryId: '',
        categoryName: 'Football',
        displayOrder: 0,
        drilldownTagNames: '',
        eventIsLive: true,
        eventSortCode: '',
        eventStatusCode: '',
        id: 10,
        isUS: true,
        liveServChannels: '',
        liveServChildrenChannels: '',
        liveStreamAvailable: true,
        typeId: '',
        typeName: '',
        name: '',
        originalName: '',
        responseCreationTime: '',
        marketsCount: 10,
        markets: [
          { outcomes: [{ name: '' }] }
        ],
        racingFormEvent: {
          class: ''
        },
        startTime: ''
      },
      participants: {
        HOME: {
          name: '',
          abbreviation: ''
        },
        AWAY: {
          name: '',
          abbreviation: ''
        }
      },
      marketsCount: 10
    };

    stage = [
      {
        obEvent: {
          markets: [
            { outcomes: [{ name: '' }] }
          ],
        },
      }
    ];

    outcomeTemplateHelperService = {
      setOutcomeMeaningMinorCode: jasmine.createSpy('setOutcomeMeaningMinorCode')
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy().and.returnValue('url')
    };
    coreToolsService = {
      getDaySuffix: jasmine.createSpy().and.returnValue('st')
    };
    filterService = {
      orderBy: jasmine.createSpy().and.returnValue(outcomes)
    };

    component = new KnockoutsCardComponent(
      outcomeTemplateHelperService,
      routingHelperService,
      coreToolsService,
      filterService
    );

    component.cardEvent = cardEvent;
    component.stage = stage;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should call correct method', () => {
      component['filterDate'] = jasmine.createSpy().and.returnValue('date');
      component['setCorrectedOutcomeMeaningMinorCode'] = jasmine.createSpy();
      component['setScores'] = jasmine.createSpy();
      component['isAnyOutcomesOnStage'] = jasmine.createSpy();
      component['setWaitingWinnerStatus'] = jasmine.createSpy();
      component.ngOnInit();
      expect(component.isFinal).toBeTruthy();
      expect(component['filterDate']).toHaveBeenCalledWith(component.cardEvent.startTime);
      expect(component.startTime).toBe('date');
      expect(component.marketsCount).toBe(component.cardEvent.obEvent.marketsCount - 1);
      expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith(component.cardEvent.obEvent);
      expect(component.EDPpath).toBe('/url');
      expect(component.market).toBe(component.cardEvent.obEvent.markets[0]);
      expect(filterService.orderBy).toHaveBeenCalledWith(component.market.outcomes, ['outcomeMeaningMinorCode']);
      expect(component.outcomes).toBe(outcomes);
      expect(component['setCorrectedOutcomeMeaningMinorCode']).toHaveBeenCalled();
      expect(component.isFlagPresentHome).toBeFalsy();
      expect(component.homeWinner).toBeFalsy();
      expect(component.isFlagPresentAway).toBeFalsy();
      expect(component.awayWinner).toBeFalsy();
      expect(component.isResulted).toBeTruthy();
      expect(component['setScores']).toHaveBeenCalledWith(component.cardEvent.result);
      expect(component['isAnyOutcomesOnStage']).toHaveBeenCalled();
      expect(component['setWaitingWinnerStatus']).toHaveBeenCalled();
    });

    it('should call method when cardEvent is empty', () => {
      component.cardEvent = {} as IKnockoutEvent;

      component['setCorrectedOutcomeMeaningMinorCode'] = jasmine.createSpy();
      component['filterDate'] = jasmine.createSpy();
      component['setScores'] = jasmine.createSpy();

      component['isAnyOutcomesOnStage'] = jasmine.createSpy();
      component['setWaitingWinnerStatus'] = jasmine.createSpy();
      component.ngOnInit();
      expect(component['filterDate']).not.toHaveBeenCalled();
      expect(component.startTime).toBeUndefined();
      expect(component.marketsCount).toBeUndefined();
      expect(routingHelperService.formEdpUrl).not.toHaveBeenCalled();
      expect(component.EDPpath).toBeUndefined();
      expect(component.market).toBeUndefined();
      expect(filterService.orderBy).not.toHaveBeenCalled();
      expect(component.outcomes).toEqual([]);
      expect(component['setCorrectedOutcomeMeaningMinorCode']).not.toHaveBeenCalled();
      expect(component.isFlagPresentHome).toBeFalsy();
      expect(component.homeWinner).toBeFalsy();
      expect(component.isFlagPresentAway).toBeFalsy();
      expect(component.awayWinner).toBeFalsy();
      expect(component.isResulted).toBeFalsy();
      expect(component['setScores']).not.toHaveBeenCalled();

      expect(component['isAnyOutcomesOnStage']).toHaveBeenCalled();
      expect(component['setWaitingWinnerStatus']).toHaveBeenCalled();
    });
  });


  it('should return correct result', () => {
    const outcome = { id: '15' } as IOutcome;
    const index = 7;
    expect(component.trackById(index, outcome)).toBe('715');
  });

  it('should set correct values', () => {
    const result = {
      score: []
    } as ICompetitionMatchResult;
    component['setScores'](result);
    expect(component.score).toBe(result.score);
  });

  it('should set correct values', () => {
    const result = {
      pen: [],
      aet: []
    } as ICompetitionMatchResult;
    component['setScores'](result);
    expect(component.score).toBe(result.aet);
    expect(component.pen).toBe(result.pen);
  });

  it('should set correct values', () => {
    const result = {
      score: ['1', '1'],
      aet: ['3', '2']
    } as ICompetitionMatchResult;
    component['setScores'](result);
    expect(component.aet).toEqual(jasmine.arrayContaining([2, 1]));
  });

  it('should set correct value', () => {
    const event = { ...cardEvent, eventId: null, homeTeamRemark: '' };
    component.cardEvent = event;
    component['setWaitingWinnerStatus']();
    expect(component.waitingWinner).toBeTruthy();
    expect(component.winnerAwayFlagLabel).toBe(component.cardEvent.awayTeam);
  });

  it('should set correct value', () => {
    const event = { ...cardEvent, eventId: null, awayTeamRemark: '' };
    component.cardEvent = event;
    component['setWaitingWinnerStatus']();
    expect(component.waitingWinner).toBeTruthy();
    expect(component.winnerHomeFlagLabel).toBe(component.cardEvent.homeTeam);
  });

  it('should set incorrect value', () => {
    const event = { ...cardEvent, eventId: 11, awayTeamRemark: '' };
    component.cardEvent = event;
    component['setWaitingWinnerStatus']();
    expect(component.waitingWinner).toBeFalsy();
    expect(component.winnerHomeFlagLabel).toBeUndefined();
    expect(component.winnerAwayFlagLabel).toBeUndefined();
  });

  it('should set correct value', () => {
    const defaultTeamLabel = '?';
    const event = {
      ...cardEvent,
      eventId: null,
      homeTeamRemark: 'home',
      awayTeamRemark: 'away',
      awayTeam: '',
      homeTeam: ''
    };
    component.cardEvent = event;
    component['setWaitingWinnerStatus']();
    expect(component.waitingWinner).toBeTruthy();
    expect(component.winnerHomeFlagLabel).toBe(defaultTeamLabel);
    expect(component.winnerAwayFlagLabel).toBe(defaultTeamLabel);
  });

  it('should call correct methods and set correct property', () => {
    component.outcomes = [
      { id: '10' }
    ] as IOutcome[];
    component['setCorrectedOutcomeMeaningMinorCode']();
    expect(outcomeTemplateHelperService.setOutcomeMeaningMinorCode)
      .toHaveBeenCalledWith(component.cardEvent.obEvent.markets, component.cardEvent.obEvent);
  });

  it('should return correct result', () => {
    const dateStr = '2019-07-01T09:44:06.550Z';
    const result = component['filterDate'](dateStr);
    expect(result).toBe('1st July');
  });

  it('should isAnyOutcomesOnStage call', () => {
    component['isAnyOutcomesOnStage']();
    expect(component.isOutcomeOnStage).toBe(component.stage[0].obEvent.markets[0].outcomes.length);
  });

  it('should isAnyOutcomesOnStage call else case', () => {
    stage = [
      { obEvent: {} },
      {
        obEvent: {
          markets: [
            { outcomes: [{ name: '' }] }
          ],
        },
      }
    ];
    component.stage = stage;
    component['isAnyOutcomesOnStage']();
    expect(component.isOutcomeOnStage).toBe(component.stage[1].obEvent.markets[0].outcomes.length);
  });

  it('should isAnyOutcomesOnStage call any cases', () => {
    stage = [
      { obEvent: {} },
      { obEvent: {} }
    ];
    component.stage = stage;
    component['isAnyOutcomesOnStage']();
    expect(component.isOutcomeOnStage).toBeFalsy();
  });
});
