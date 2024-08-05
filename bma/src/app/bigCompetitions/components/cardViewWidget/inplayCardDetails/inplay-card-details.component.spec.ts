import {
  InplayCardDetailsComponent
} from '@app/bigCompetitions/components/cardViewWidget/inplayCardDetails/inplay-card-details.component';
import { IBigCompetitionSportEvent } from '@app/bigCompetitions/models/big-competitions.model';

describe('InplayCardDetailsComponent', () => {

  let component;

  const teams = {
    away: {
      eventId: 'eventId1',
      id: 'id1',
      currentPoints: 0,
      score: {},
      name: 'name1',
      role: 'role1',
      roleCode: 'roleCode1',
      type: 'type1'
    },
    home: {
      eventId: 'eventId2',
      id: 'id2',
      currentPoints: 0,
      score: {},
      name: 'name2',
      role: 'role2',
      roleCode: 'roleCode2',
      type: 'type2'
    }
  };

  const event = {
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
    markets: [],
    racingFormEvent: {
      class: ''
    },
    startTime: '',
    initClock: {
      period_code: 'EXTRA_TIME_FIRST_HALF'
    },
    comments: {
      teams,
    }
  } as IBigCompetitionSportEvent;

  beforeEach(() => {
    component = new InplayCardDetailsComponent();
    component.event = event;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit when event.clock = false', () => {
    component.ngOnInit();
    expect(component.PERIOD_CODE).toBe(event.initClock.period_code);
    expect(component.teams).toBe(teams);
  });

  it('#ngOnInit when event.clock = true', () => {
    component.event.clock = true;
    component.ngOnInit();
    expect(component.PERIOD_CODE).toBe(event.clock.period_code);
    expect(component.teams).toBe(teams);
  });


  it('should set correct match time when PERIOD_CODE is EXTRA_TIME_FIRST_HALF', () => {
    component.PERIOD_CODE = 'EXTRA_TIME_FIRST_HALF';
    component['setPeriodLabel']();
    expect(component.matchTime).toBe('ET');
    expect(component.isPenalty).toBeFalsy();
  });

  it('should set correct match time when PERIOD_CODE is EXTRA_TIME_SECOND_HALF', () => {
    component.PERIOD_CODE = 'EXTRA_TIME_SECOND_HALF';
    component['setPeriodLabel']();
    expect(component.matchTime).toBe('ET');
    expect(component.isPenalty).toBeFalsy();
  });

  it('should set correct match time when PERIOD_CODE is EXTRA_TIME_HALF_TIME', () => {
    component.PERIOD_CODE = 'EXTRA_TIME_HALF_TIME';
    component['setPeriodLabel']();
    expect(component.matchTime).toBe('ET');
    expect(component.isPenalty).toBeFalsy();
  });

  it('should set correct match time when PERIOD_CODE is PENALTIES', () => {
    component.PERIOD_CODE = 'PENALTIES';
    component['setPeriodLabel']();
    expect(component.matchTime).toBe('AET');
    expect(component.isPenalty).toBeTruthy();
  });

  it('should set empty string as default value for match time', () => {
    component.PERIOD_CODE = '';
    component['setPeriodLabel']();
    expect(component.matchTime).toBe('');
    expect(component.isPenalty).toBeFalsy();
  });
});
