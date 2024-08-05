import { InplayScoreComponent } from './inplay-score.component';

describe('InplayScoreComponent', () => {
  let component: InplayScoreComponent;
  const eventMock = {
    name: 'Man United vs Liverpool',
    initClock: {}
  };
  let sportEventHelper;

  const scoreParserService = {
    parseScores: jasmine.createSpy('parseScores'),
    getScoreType: jasmine.createSpy('getScoreType')
  } as any;

  beforeEach(() => {
    sportEventHelper = {
      isTennis: jasmine.createSpy().and.returnValue(true),
      getTennisSetScores: jasmine.createSpy(),
      isHalfTime: jasmine.createSpy(),
      isPenalties: jasmine.createSpy(),
      getOddsScore: jasmine.createSpy(),
      getEventCurrentPoints: jasmine.createSpy(),
      isEventHasOddsScores: jasmine.createSpy(),
      getTennisScoreForPlayer: jasmine.createSpy(),
      isEventHasCurrentPoints: jasmine.createSpy(),
      isLive: jasmine.createSpy(),
      getTennisSetIndex: jasmine.createSpy(),
      getCurrentPoints: jasmine.createSpy(),
    };

    component = new InplayScoreComponent(sportEventHelper, scoreParserService);
    component.event = <any>eventMock;
  });

  it('should create', () => {
    sportEventHelper.isHalfTime.and.returnValue(false);
    sportEventHelper.isPenalties.and.returnValue(false);
    component.ngOnInit();
    expect(component).toBeTruthy();
    expect(component.isTennis).toBeTruthy();
    expect(component.isHalfTime).toEqual(false);
    expect(component.isPenalties).toEqual(false);
  });

  it('tennis should not be true', () => {
    component.event.comments = {
      teams: {
        home: { name: '', score: '' },
        away: { name: '', score: '' }
      }
    };
    scoreParserService.getScoreType.and.returnValues('BoxScore');
    scoreParserService.parseScores.and.returnValues('test');

    component.ngOnInit();

    expect(scoreParserService.getScoreType).toHaveBeenCalled();
    expect(component.boxScore).toEqual('test' as any);
  });

  it('trackByIndex', () => {
    expect(component.trackByIndex(0)).toEqual(0);
  });

  it('tennisScores', () => {
    const variable = component.tennisScores;
    expect(variable).toBeUndefined();
    expect(sportEventHelper.getTennisSetScores).toHaveBeenCalledWith(eventMock);
  });

  it('getOddsScore', () => {
    component.getOddsScore('home', false);
    expect(sportEventHelper.getOddsScore).toHaveBeenCalledWith(eventMock, 'home', false);
  });

  it('getCurrentPoints', () => {
    component.getCurrentPoints('home');
    expect(sportEventHelper.getEventCurrentPoints).toHaveBeenCalledWith(eventMock, 'home');
  });

  it('isEventHasOddsScores', () => {
    component.isEventHasOddsScores();
    expect(sportEventHelper.isEventHasOddsScores).toHaveBeenCalledWith(eventMock);
  });

  it('getTennisScoreForPlayer', () => {
    component.getTennisScoreForPlayer('away');
    expect(sportEventHelper.getTennisScoreForPlayer).toHaveBeenCalledWith(eventMock, 'away');
  });

  it('isEventHasCurrentPoints', () => {
    component.isEventHasCurrentPoints();
    expect(sportEventHelper.isEventHasCurrentPoints).toHaveBeenCalledWith(eventMock);
  });

  it('isLive', () => {
    component.isLive();
    expect(sportEventHelper.isLive).toHaveBeenCalledWith(eventMock);
  });

  it('isClockAllowed', () => {
    expect(component.isClockAllowed()).toBeTruthy();
  });

  it('getTennisSetIndex', () => {
    component.getTennisSetIndex();
    expect(sportEventHelper.getTennisSetIndex).toHaveBeenCalledWith(eventMock);
  });

  it('should update time properties', () => {
    sportEventHelper.isHalfTime.and.returnValue(true);
    sportEventHelper.isPenalties.and.returnValue(false);
    component.onClockUpdate();
    expect(sportEventHelper.isHalfTime).toHaveBeenCalledWith(eventMock);
    expect(sportEventHelper.isPenalties).toHaveBeenCalledWith(eventMock);
    expect(component.isHalfTime).toEqual(true);
    expect(component.isPenalties).toEqual(false);
  });
});
