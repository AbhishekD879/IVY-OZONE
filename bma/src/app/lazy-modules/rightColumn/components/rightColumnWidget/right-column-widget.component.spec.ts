import { of as observableOf } from 'rxjs';
import { NavigationEnd, NavigationStart } from '@angular/router';

import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { RightColumnWidgetComponent } from './right-column-widget.component';
import { IWidget } from '@lazy-modules/rightColumn/components/rightColumnWidget/widget.model';

describe('RightColumnWidgetComponent', () => {
  let pubSubService;
  let visEventService;
  let windowRefService;
  let router;
  let routingState;
  let route;
  let deviceService;
  let component: RightColumnWidgetComponent;

  beforeEach(() => {
    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
    };
    visEventService = {
      checkForEventsWithAvailableVisualization: jasmine.createSpy('checkForEventsWithAvailableVisualization')
        .and.returnValue(observableOf(null)),
      checkPreMatchWidgetAvailability: jasmine.createSpy('checkPreMatchWidgetAvailability')
        .and.returnValue(observableOf(null))
    };
    windowRefService = {
      nativeWindow: {
        addEventListener: jasmine.createSpy('addEventListener'),
        removeEventListener: jasmine.createSpy('removeEventListener'),
        setTimeout: jasmine.createSpy('setTimeout'),
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
        subscribe: jasmine.createSpy('subscribe')
      }
    };
    routingState = {
      getRouteParam: jasmine.createSpy('getRouteParam'),
      getCurrentSegment: jasmine.createSpy('getCurrentSegment').and.returnValue('')
    };
    route = {
      snapshot: {}
    };
    deviceService = {
      isDesktop: false
    };

    component = new RightColumnWidgetComponent(
      pubSubService,
      visEventService,
      windowRefService,
      router,
      routingState,
      route,
      deviceService
    );
  });

  describe('ngOnInit', () => {
    xit('should init component', () => {
      pubSubService.subscribe.and.callFake((p1, p2, cb) => {
        return cb({});
      });
      router.events.subscribe.and.callFake(cb => cb(new NavigationEnd(1, '/', '/')));
      windowRefService.nativeWindow.addEventListener = jasmine.createSpy('addEventListener')
        .and.callFake((type, cb) => {
          if (type === 'resize') {
            cb();
          }
        });
      component.widgetDataStore = [];
      component['updateData'] = jasmine.createSpy('updateData');
      component['filterData'] = jasmine.createSpy();
      component['filterRequest'] = jasmine.createSpy();

      component.ngOnInit();

      expect(component.isDesktop).toEqual(deviceService.isDesktop);
      expect(component.directiveArr).toEqual([]);
      expect(component.widgets).toEqual([]);
      expect(component.showMatchCentre).toBeFalsy();

      expect(component.lastCheckedId).toBe('0');
      expect(component.isAnotherPage).toBeTruthy();

      expect(component.widgets).toBe(component.widgetDataStore);
      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        'Right-Column', 'crossSellData', jasmine.any(Function)
      );

      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        component.widgetColumn, pubSubApi.SHOW_WIDGET, jasmine.any(Function)
      );

      expect(pubSubService.subscribe).toHaveBeenCalledWith(
        component.widgetColumn, pubSubApi.DISPLAY_WIDGET, jasmine.any(Function)
      );

      expect(windowRefService.nativeWindow.addEventListener).toHaveBeenCalledWith(
        'resize', jasmine.any(Function)
      );

      expect(component['updateData']).toHaveBeenCalled();
      expect(component['filterData']).toHaveBeenCalledTimes(4);
      expect(component['filterRequest']).toHaveBeenCalledTimes(2);
    });

    it('should not listen to resize event', () => {
      deviceService.isDesktop = true;
      component.widgetDataStore = [];
      pubSubService.subscribe.and.callFake((p1, p2, cb) => {
        if(p1=== 'Right-Column')
        return cb({});
      });
      component.ngOnInit();
      expect(windowRefService.nativeWindow.addEventListener).not.toHaveBeenCalled();
    });

    it('widgets for else condition', () => {
      deviceService.isDesktop = true;
      component.widgetDataStore = [];
      pubSubService.subscribe.and.callFake((p1, p2, cb) => {
        if(p1=== 'Right-Column')
        return cb(null);
      });
      component.ngOnInit();
      expect(windowRefService.nativeWindow.addEventListener).not.toHaveBeenCalled();
    });

    it('should not filter request on navigation start', () => {
      spyOn(component as any, 'filterRequest');
      router.events.subscribe.and.callFake(cb => cb(new NavigationStart(1, '/')));
      component.widgetDataStore = [];
      component.ngOnInit();
      expect(component['filterRequest']).not.toHaveBeenCalled();
    });
  });

  describe('ngOnDestroy', () => {
    it('should unsubscribe listeners', () => {
      component.locationChangeListener = { unsubscribe: jasmine.createSpy() } as any;
      windowRefService.nativeWindow.removeEventListener = jasmine.createSpy('addEventListener')
        .and.callFake((type, cb) => {
          if (type === 'resize') {
            cb();
          }
        });
      component['updateData'] = jasmine.createSpy('updateData');
      component.ngOnDestroy();
      expect(windowRefService.nativeWindow.removeEventListener).toHaveBeenCalledWith(
        'resize', jasmine.any(Function)
      );
      expect(component['updateData']).toHaveBeenCalled();
      expect(component.locationChangeListener.unsubscribe).toHaveBeenCalled();
    });

    it('should not remove resize listener', () => {
      component.isDesktop = true;
      component.ngOnDestroy();
      expect(windowRefService.nativeWindow.removeEventListener).not.toHaveBeenCalled();
    });
  });

  it('trackByDirectiveName', () => {
    const widget = { directiveName: 'name' } as IWidget;
    expect(component.trackByDirectiveName(1, widget)).toBe('name');
  });

  it('isMatchCentreWidget', () => {
    component.showMatchCentre = false;

    expect(
      component.isMatchCentreWidget({ directiveName: 'match-centre' } as any)
    ).toBe(component.showMatchCentre);

    expect(
      component.isMatchCentreWidget({ directiveName: 'match' } as any)
    ).toBe(true);
  });

  describe('filterRequest', () => {
    beforeEach(() => {
      visEventService.checkForEventsWithAvailableVisualization.and.returnValue({
        pipe: (a, b) => observableOf(null).pipe(a, b).subscribe()
      });
    });

    it('should not show mach centre', () => {
      component['filterRequest']({ name: 'match-centre' } as any);
      expect(component.showMatchCentre).toBe(false);
    });

    it('should set timeout and check events visualisation', () => {
      routingState.getRouteParam.and.returnValue('1');
      routingState.getCurrentSegment.and.returnValue(['sport', 'eventMain']);
      visEventService.checkPreMatchWidgetAvailability.and.returnValue(observableOf([[{}]]));
      component['filterRequest']({} as any);
      expect(visEventService.checkForEventsWithAvailableVisualization).toHaveBeenCalledTimes(1);
    });

    it('should not set timeout', () => {
      routingState.getRouteParam.and.returnValue('');
      routingState.getCurrentSegment.and.returnValue(['sport', 'eventMain']);
      visEventService.checkPreMatchWidgetAvailability.and.returnValue(observableOf([]));
      component['filterRequest']({} as any);
    });
  });

  describe('updateData', () => {
    beforeEach(() => {
      spyOn(component as any, 'filterData');
    });

    it('should filter data', () => {
      component.deviceType = 'mobile';
      windowRefService.nativeWindow.deviceType = 'tablet';
      component['updateData']();
      expect(component['filterData']).toHaveBeenCalledTimes(1);
    });

    it('should not filter data', () => {
      component.deviceType = 'mobile';
      windowRefService.nativeWindow.deviceType = 'mobile';
      component['updateData']();
      expect(component['filterData']).not.toHaveBeenCalled();
    });
  });

  it('filterData', () => {
    component['byColumn'] = jasmine.createSpy().and.returnValue(true);
    component['byDevice'] = jasmine.createSpy().and.returnValue(true);
    component['byShowOnRules'] = jasmine.createSpy().and.returnValue(true);
    component.widgets = [{}, {}] as any;

    component['filterData']();

    expect(component['byColumn']).toHaveBeenCalledTimes(2);
    expect(component['byDevice']).toHaveBeenCalledTimes(2);
    expect(component['byShowOnRules']).toHaveBeenCalledTimes(2);
  });

  it('byColumn', () => {
    component.widgetColumn = 'a';
    expect(
      component['byColumn']({ columns: ['a', 'b'] } as any)
    ).toBeTruthy();

    component.widgetColumn = 'c';
    expect(
      component['byColumn']({ columns: ['a', 'b'] } as any)
    ).toBeFalsy();
  });

  it('byDevice', () => {
    component.isDesktop = true;
    component.directiveArr = ['1', '2'];
    expect(
      component['byDevice']({ publishedDevices: null, directiveName: '1' } as any)
    ).toBeFalsy();

    component.isDesktop = true;
    component.directiveArr = ['1', '2'];
    expect(
      component['byDevice']({ publishedDevices: null, directiveName: '3' } as any)
    ).toBeFalsy();

    component.isDesktop = false;
    component.directiveArr = ['1', '2'];
    expect(
      component['byDevice']({ publishedDevices: ['tablet'], directiveName: '3' } as any)
    ).toBeTruthy();
  });

  it('byShowOnRules', () => {
    component['checkSegmentContainment'] = jasmine.createSpy().and.returnValue(true);
    component['checkSport'] = jasmine.createSpy().and.returnValue(true);

    expect(
      component['byShowOnRules']({ showOn: null } as any)
    ).toBeTruthy();

    expect(
      component['byShowOnRules']({ showOn: { routes: '/' } } as any)
    ).toBeTruthy();
    expect(component['checkSegmentContainment']).toHaveBeenCalled();
    expect(component['checkSport']).toHaveBeenCalled();

    (component['checkSegmentContainment'] as any).and.returnValue(false);
    expect(
      component['byShowOnRules']({ showOn: { routes: '/' } } as any)
    ).toBeFalsy();
  });

  it('checkSegmentContainment', () => {
    routingState.getCurrentSegment.and.returnValue('/home');
    expect(
      component['checkSegmentContainment'](['/', 'home'])
    ).toBeTruthy();

    routingState.getCurrentSegment.and.returnValue('/faq');
    expect(
      component['checkSegmentContainment'](['', '/home'])
    ).toBeFalsy();

    expect(routingState.getCurrentSegment).toHaveBeenCalledTimes(2);
  });

  it('checkSport', () => {
    routingState.getRouteParam.and.returnValue('football');

    expect(
      component['checkSport'](['football', 'tennis'])
    ).toBeTruthy();

    expect(
      component['checkSport'](['horse racing'])
    ).toBeFalsy();

    expect(routingState.getRouteParam).toHaveBeenCalledTimes(2);
  });
});
