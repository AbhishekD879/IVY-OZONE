import { of } from 'rxjs';

import { OddsCardEnhancedMultiplesComponent } from './odds-card-enhanced-multiples.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { oddsCardConstant } from '@app/shared/constants/odds-card-constant';
describe('OddsCardEnhancedMultiplesComponent', () => {
  let component: OddsCardEnhancedMultiplesComponent;
  let eventService;
  let marketTypeService;
  let templateService;
  let timeService;
  let filtersService;
  let routingHelperService;
  let router;
  let sportsConfigHelperService, seoDataService;
  let pubSubService;
  let changeDetectorRef;
  let gtmService;
  beforeEach(() => {
    eventService = {
      isLiveStreamAvailable: jasmine.createSpy()
    };
    marketTypeService = {};
    templateService = {
      getTemplate: jasmine.createSpy(),
      isMultiplesEvent: jasmine.createSpy(),
      isListTemplate: (selectedMarket: string)=>{
        return oddsCardConstant.LIST_TEMPLATES.indexOf(selectedMarket) !== -1;
       }
    };
    timeService = {
      getLocalHourMin: jasmine.createSpy(),
      getEventTime: jasmine.createSpy()
    };
    filtersService = {
      getTeamName: jasmine.createSpy()
    };
    routingHelperService = seoDataService = {};
    router = {};
    sportsConfigHelperService = {
      getSportPathByCategoryId: jasmine.createSpy('getSportPathByCategoryId').and.returnValue(of(''))
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb) => { cb(); }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    component = new OddsCardEnhancedMultiplesComponent(
      eventService,
      marketTypeService,
      templateService,
      timeService,
      filtersService,
      routingHelperService,
      router,
      sportsConfigHelperService,
      seoDataService,
      gtmService,
      pubSubService,
      changeDetectorRef
    );
  });

  it('ngOnInit', () => {
    templateService.getTemplate.and.returnValue({});
    component.event = { markets: [] } as any;
    component.racingData = {};
    component['isStreamAvailable'] = (() => {}) as any;
    component['getSelectedMarket'] = (() => {}) as any;

    component.ngOnInit();
    component.nameOverride = null;
    component.featured = component.eventName = null;
    expect(component.nameOverride).toBeFalsy();

    component.ngOnInit();
    component.nameOverride = 'test';
    expect(component.nameOverride).toBe('test');

    expect(pubSubService.subscribe).toHaveBeenCalledWith(component['tagName'], 'WS_EVENT_UPDATE', jasmine.any(Function));
    expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();

    expect(pubSubService.unsubscribe).toHaveBeenCalled();
  });

  it('trackById', () => {
    expect(
      component.trackById({ id: '1' } as any)
    ).toBe('1');
  });

  it('nameOfEvent', () => {
    component.nameOverride = 'abc';
    expect( component.nameOfEvent({} as any) ).toBe('abc');

    component. nameOverride = '';
    expect( component. nameOfEvent({ name: 'xyz' } as any) ).toBe('xyz');
  });

  it('filterOutcomes', () => {
    component.limitSelections = null;
    expect(
      component.filterOutcomes([{}, {}, {}] as any)
    ).toEqual([{}, {}, {}] as any);

    component.limitSelections = 1;
    expect(
      component.filterOutcomes([{}, {}, {}] as any)
    ).toEqual([{}] as any);
  });
});
