import { of as observableOf, Observable, Subscription, BehaviorSubject, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { NavigationEnd } from '@angular/router';
import { InplayPageComponent } from '@app/inPlay/components/inplayPage/inplay-page.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('InplayPageComponent', () => {
  let component: InplayPageComponent;
  let inPlayConnectionService;
  let inPlayMainService;
  let inplayStorageService;
  let router;
  let route;
  let routingState;
  let pubsubService;
  let changeDetector;

  const ribbonItems = {
    data: [{ categoryId: 'categoryId' }, { categoryId: 'categoryId' }]
  } as any;

  beforeEach(fakeAsync(() => {
    inPlayConnectionService = {
      disconnectComponent: jasmine.createSpy(),
      connectComponent: jasmine.createSpy().and.returnValue(observableOf(null))
    };
    inPlayMainService = {
      initSportsCache: jasmine.createSpy(),
      setSportUri: jasmine.createSpy(),
      getSportUri: jasmine.createSpy(),
      unsubscribeForUpdates: jasmine.createSpy(),
      getRibbonData: jasmine.createSpy().and.returnValue(observableOf(ribbonItems)),
    };
    inplayStorageService = {
      destroySportsCache: jasmine.createSpy()
    };
    router = {
      events: observableOf( new NavigationEnd(0, '', ''))
    };
    route = {};
    routingState = {
      getRouteParam: jasmine.createSpy(),
      getPathName: jasmine.createSpy().and.returnValue('pathName')
    };

    pubsubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };

    changeDetector = {
      detectChanges: jasmine.createSpy('detectChanges'),
    };

    component = new InplayPageComponent(inPlayConnectionService, inPlayMainService,
      inplayStorageService, router, route, routingState, pubsubService, changeDetector);

    component['routeListener'] = new Subscription();
  }));

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should use OnPush strategy', () => {
    expect(InplayPageComponent['__annotations__'][0].changeDetection).toBe(0);
  });

  describe('#ngOnInit', () => {
    beforeEach(() => {
      component.updateActiveTab = jasmine.createSpy();
    });
    it('should set handlers', () => {
      const updatedRibbonItems = ribbonItems;
      component.ngOnInit();
      expect(inPlayConnectionService.connectComponent).toHaveBeenCalled();
      expect(inPlayMainService.initSportsCache).toHaveBeenCalled();
      expect(component.menuItems).toEqual(updatedRibbonItems);
      expect(inPlayMainService.getRibbonData()).toEqual(jasmine.any(Observable));
      expect(pubsubService.subscribe).toHaveBeenCalledWith('inplayPage', 'SESSION_LOGIN', jasmine.any(Function));
      expect(component.updateActiveTab).toHaveBeenCalled();
      expect(inPlayMainService.getRibbonData).toHaveBeenCalled();
      expect(component.sportsAvailable).toBeTruthy();
      expect(changeDetector.detectChanges).toHaveBeenCalled();
    });

    it('routeListener when getRouteParam is present', () => {
      component['routingState'].getPathName = jasmine.createSpy().and.returnValue('somePathName');
      component['routingState'].getRouteParam = jasmine.createSpy().and.returnValue('someRouteParam');
      component.ngOnInit();

      expect(inPlayMainService.setSportUri).toHaveBeenCalledWith('someRouteParam');
    });

    it('routeListener when getSportUri is present', () => {
      component['routingState'].getRouteParam = jasmine.createSpy().and.returnValue(null);
      component['inPlayMainService'].getSportUri = jasmine.createSpy().and.returnValue('someSportUri');
      component.ngOnInit();
      expect(inPlayMainService.setSportUri).toHaveBeenCalledWith('someSportUri');
    });

    it('routeListener when watchlive', () => {
      component['routingState'].getPathName = jasmine.createSpy().and.returnValue('watchlive');
      component.ngOnInit();

      expect(inPlayMainService.setSportUri).toHaveBeenCalledWith('watchlive');
    });

    it('error response', fakeAsync(() => {
      inPlayConnectionService.connectComponent.and.returnValue(throwError('some error'));
      component.ngOnInit();
      tick();
      expect(inPlayConnectionService.connectComponent).toHaveBeenCalled();
      expect(component.state).toEqual({ loading: false, error: true });
      expect(changeDetector.detectChanges).toHaveBeenCalled();
    }));

    it('should not update active tab if event is not NavigationEnd', fakeAsync(() => {
      router.events = observableOf({});
      component.updateActiveTab = jasmine.createSpy('updateActiveTab').and.callThrough();
      component.ngOnInit();
      tick();
      expect(component.updateActiveTab).toHaveBeenCalledTimes(1);
      expect(changeDetector.detectChanges).toHaveBeenCalled();
    }));
  });

  it('updateActiveTab', () => {
    spyOn<any>(component, 'unsbscribeFromMS');
    component.updateActiveTab();

    expect(component.activeMenuItemUri).toEqual('pathName');
    expect(changeDetector.detectChanges).toHaveBeenCalled();
  });

  it('unsbscribeFromMS', () => {
    component['unsbscribeFromMS']();
    expect(inplayStorageService.destroySportsCache).toHaveBeenCalled();
    expect(inPlayMainService.unsubscribeForUpdates).toHaveBeenCalled();
    expect(inPlayConnectionService.disconnectComponent).toHaveBeenCalled();
  });

  it(`should unsubscribe from 'getRibbonData' stream`, fakeAsync(() => {
    const res = { data: [{ categoryId: 'Subject' }] } as any;
    const stream$ = new BehaviorSubject(ribbonItems);
    inPlayMainService.getRibbonData.and.returnValue(stream$ as any);
    spyOn<any>(component, 'unsbscribeFromMS');

    component.ngOnInit();
    component['connectSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;

    expect(component.menuItems).toEqual(ribbonItems);

    component.ngOnDestroy();
    stream$.next(res);

    tick();
    expect(component.menuItems).toBeDefined();
    expect(component.menuItems).toEqual(res);
    expect(component['connectSubscription'].unsubscribe).toHaveBeenCalled();
    expect(pubsubService.unsubscribe).toHaveBeenCalled();
    expect(component['unsbscribeFromMS']).toHaveBeenCalled();
  }));

  it('should run ngOnDestroy when in ribbon there is only 1 element and it is with targetUriCopy: watchlive', () => {
    component['inPlayMainService'].getRibbonData = jasmine.createSpy()
      .and.returnValue(observableOf({ data: [ { targetUriCopy: 'watchlive' } ] } ));

    spyOn<any>(component, 'ngOnDestroy');

    component.updateActiveTab = jasmine.createSpy();

    component.ngOnInit();

    expect(component.updateActiveTab).not.toHaveBeenCalled();
    expect(component.state.loading).toBeFalsy();
    expect(component.sportsAvailable).toBeFalsy();
    expect(component.ngOnDestroy).toHaveBeenCalled();
  });

  it('should run ngOnDestroy when in ribbon there are no sportsAvailable for inPlayPage', () => {
    component['inPlayMainService'].getRibbonData = jasmine.createSpy()
      .and.returnValue(observableOf({ data: [] } ));

    spyOn<any>(component, 'ngOnDestroy');

    component.updateActiveTab = jasmine.createSpy();

    component.ngOnInit();

    expect(component.updateActiveTab).not.toHaveBeenCalled();
    expect(component.state.loading).toBeFalsy();
    expect(component.sportsAvailable).toBeFalsy();
    expect(component.ngOnDestroy).toHaveBeenCalled();
  });
});
