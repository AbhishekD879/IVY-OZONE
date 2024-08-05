import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

import { RightColumnWidgetComponent } from './right-column-widget.component';

describe('LadbrokesRightColumnWidgetComponent', () => {
  let pubSubService;
  let visEventService;
  let windowRefService;
  let router;
  let routingState;
  let route;
  let deviceService;
  let germanSupportService;
  let component: RightColumnWidgetComponent;

  beforeEach(() => {
    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy().and.callFake((p1, p2, cb) => {
        cb({data: [1]});
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
    };
    visEventService = {
      checkForEventsWithAvailableVisualization: jasmine.createSpy(),
      checkPreMatchWidgetAvailability: jasmine.createSpy()
    };
    windowRefService = {
      nativeWindow: {
        addEventListener: jasmine.createSpy(),
        removeEventListener: jasmine.createSpy(),
        setTimeout: jasmine.createSpy(),
        deviceType: 'tablet'
      },
      document: {
        querySelector: jasmine.createSpy('querySelector').and.returnValue(
          {
            firstElementChild: undefined
          }
        )
      }
    };
    router = {
      events: {
        subscribe: jasmine.createSpy()
      }
    };
    routingState = {
      getRouteParam: jasmine.createSpy(),
      getCurrentSegment: jasmine.createSpy().and.returnValue('sport')
    };
    route = {
      snapshot: {}
    };
    deviceService = {
      isDesktop: false
    };

    germanSupportService = {
      isGermanUser: jasmine.createSpy().and.returnValue(false)
    };

    component = new RightColumnWidgetComponent(
      pubSubService,
      visEventService,
      windowRefService,
      router,
      routingState,
      route,
      deviceService,
      germanSupportService
    );
  });

  it('ngOnInit', () => {
    component.widgetDataStore = [];
    component.ngOnInit();
    expect(pubSubService.subscribe).toHaveBeenCalledTimes(4);
  });

  it('filterNextRacesIfGermanCustomer', () => {
    component['germanSupportService'].isGermanUser = jasmine.createSpy().and.returnValue(true);
    component.widgets = [
      {
        directiveName: 'a'
      }, {
        directiveName: 'b'
      }, {
        directiveName: 'next-races'
      }
    ] as any;
    component['filterNextRacesIfGermanCustomer']();
    expect((component.widgets  as any).length).toEqual(2);
    expect(component.widgets).toEqual([{
      directiveName: 'a'
    }, {
      directiveName: 'b'
    }] as any);
  });
});
