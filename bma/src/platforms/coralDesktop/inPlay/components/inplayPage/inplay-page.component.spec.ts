import { of as observableOf, Subscription } from 'rxjs';
import { NavigationEnd } from '@angular/router';

import { InplayPageComponent } from '@coralDesktop/inPlay/components/inplayPage/inplay-page.component';

describe('InplayPageComponent', () => {
  let component: InplayPageComponent;
  let inPlayConnectionService;
  let inPlayMainService;
  let inplayStorageService;
  let router;
  let route;
  let routingState;
  let pubsubService;
  let changeDetectorRef;
  const ribbonItems = {
    data: [{categoryId: 'categoryId'}, {categoryId: 'categoryId'}]
  } as any;

  beforeEach(() => {
    inPlayConnectionService = {
      disconnectComponent: jasmine.createSpy(),
      connectComponent: jasmine.createSpy().and.returnValue(observableOf(null))
    };
    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
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

    pubsubService = {
      API: {
        SESSION_LOGIN: 'SESSION_LOGIN'
      },
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };

    routingState = {
      getRouteParam: jasmine.createSpy(),
      getPathName: jasmine.createSpy().and.returnValue('pathName')
    };

    component = new InplayPageComponent(
      inPlayConnectionService,
      inPlayMainService,
      inplayStorageService,
      router,
      route,
      routingState,
      pubsubService,
      changeDetectorRef
    );

    component['routeListener'] = new Subscription();
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should use OnPush strategy', () => {
    expect(InplayPageComponent['__annotations__'][0].changeDetection).toBe(0);
  });
});
