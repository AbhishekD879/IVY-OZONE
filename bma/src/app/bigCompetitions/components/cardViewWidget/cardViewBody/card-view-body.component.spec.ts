import {
  CardViewBodyComponent
} from '@app/bigCompetitions/components/cardViewWidget/cardViewBody/card-view-body.component';
import { IBigCompetitionSportEvent } from '@app/bigCompetitions/models/big-competitions.model';

describe('CardViewBodyComponent', () => {

  let component: CardViewBodyComponent;

  let sportEventHelperService;
  let routingHelperService;
  let routingState;
  let route;
  let router;

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
    startTime: ''
  } as IBigCompetitionSportEvent;

  beforeEach(() => {
    sportEventHelperService = {
      isFootball: jasmine.createSpy().and.returnValue(true),
      getMarketsCount: jasmine.createSpy().and.returnValue('3'),
      isStreamAvailable: jasmine.createSpy().and.returnValue(true),
      showMarketsCount: jasmine.createSpy().and.returnValue(true)
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy().and.returnValue('EDPpath')
    };
    routingState = {
      getRouteParam: jasmine.createSpy().and.returnValue('someLocation')
    };
    route = {
      snapshot: 'snapshot'
    };
    router = {
      navigate: jasmine.createSpy()
    };

    component = new CardViewBodyComponent(sportEventHelperService, router, routingHelperService, routingState, route);
    component.event = event;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', () => {
    component.ngOnInit();
    expect(sportEventHelperService.isFootball).toHaveBeenCalledWith(component.event);
    expect(sportEventHelperService.getMarketsCount).toHaveBeenCalledWith(component.event);
    expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith(component.event);
    expect(component.sportName).toBe('football');
    expect(component.isFootball).toBeTruthy();
    expect(component.marketsCount).toBe('+3');
    expect(component.EDPpath).toBe('/EDPpath');
  });

  it('stream should be available', () => {
    expect(component.isStreamAvailable()).toBeTruthy();
    expect(sportEventHelperService.isStreamAvailable).toHaveBeenCalledWith(component.event);
  });

  it('should show markets count', () => {
    expect(component.showMarketsCount()).toBeTruthy();
    expect(sportEventHelperService.showMarketsCount).toHaveBeenCalledWith(component.event);
  });

  it('should return current location correctly', () => {
    expect(component.getLocation()).toBe('someLocation');
    expect(routingState.getRouteParam).toHaveBeenCalledWith('name', 'snapshot');
  });

  it('isInPlay should return true', () => {
    component.viewType = 'inplay';
    expect(component.isInPlay).toBeTruthy();
  });

  it('isInPlay should return false', () => {
    component.viewType = '';
    expect(component.isInPlay).toBeFalsy();
  });

  it('goToEvent should call router.navigate and redirect to proper path', () => {
    const mouseEvent = jasmine.createSpyObj('mouseEvent', ['preventDefault']);
    component.EDPpath = '/test';

    component.goToEvent(mouseEvent);

    expect(mouseEvent.preventDefault).toHaveBeenCalled();
    expect(router.navigate).toHaveBeenCalledWith(['/test']);
  });
});
