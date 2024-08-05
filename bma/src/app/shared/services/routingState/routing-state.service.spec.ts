import { fakeAsync, tick } from '@angular/core/testing';
import { Observable, of } from 'rxjs';
import { ActivationStart, NavigationEnd, RoutesRecognized } from '@angular/router';
import { RoutingState } from '@shared/services/routingState/routing-state.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

const MOCK_HISTORY = ['/', 'some', 'mock', 'url'];
const MOCK_SEGMENT_HISTORY = [MOCK_HISTORY[2], MOCK_HISTORY[3]];
const MOCK_ACTIVATED_ROUTE_SNAPSHOTS: any = [{}, {}, { route: 'test' }, {}];
const MOCK_SEGMENT = 'newUrlSegment';

describe('RoutingState', () => {
  let pubSubService;
  let service: RoutingState,
    rendererService,
    windowRefService,
    route;
  let activatedSnapshot: ({ }: any) => any;
  let mouseEvent;

  beforeAll(() => {
    activatedSnapshot = ({
      getResult = MOCK_SEGMENT,
      getResultFirstChild = null,
    }) => ({
      data: { test: 'test' },
      firstChild: {
        children: {
          length: 2
        },
        paramMap: {
          get() {
            return getResultFirstChild;
          }
        },
      },

      paramMap: {

        get() {
          return getResult;
        }
      },
    });
  });

  beforeEach(() => {
    const router = jasmine.createSpyObj('router', ['events', 'navigateByUrl'], ['url']);
    route = {
      firstChild: {
        firstChild: {
          snapshot: {
            data: {
              segment: 'home'
            }
          }
        }
      },
      snapshot: jasmine.createSpy('snapshot')
    };
    rendererService = {
      renderer: {
        addClass: jasmine.createSpy(),
        removeClass: jasmine.createSpy()
      }
    };
    windowRefService = {
      document: {
        querySelector: jasmine.createSpy('querySelector')
      }
    };
    pubSubService = {
      publish: jasmine.createSpy('pubish'),
      API: pubSubApi
    };

    service = new RoutingState(router, route, rendererService, windowRefService, pubSubService);
  });

  it('should create', () => {
    expect(service).toBeTruthy();
  });

  it('getHistory', () => {
    service['history'] = ['/'];

    expect(service.getHistory()).toEqual(service['history']);
  });
  it('setHistory', () => {
    service.setHistory(['/']);

    expect(service.getHistory()).toEqual(['/']);
  });

  it('getSegmentHistory', () => {
    service['segmentHistory'] = ['/'];

    expect(service.getSegmentHistory()).toEqual(service['segmentHistory']);
  });

  it('setCurrentUrl', () => {
    service['history'] = ['/'];

    service.setCurrentUrl(MOCK_SEGMENT);
    expect(service['history'].pop()).toEqual(MOCK_SEGMENT);
  });

  describe('getCurrentSegment', () => {
    it('Should return segment if segmentHistory not empty', () => {
      const expected = 'newSegmentUrl';

      service['segmentHistory'] = [...MOCK_SEGMENT_HISTORY, expected];
      const actual = service.getCurrentSegment();

      expect(expected).toEqual(actual);
    });

    it('Should return empty string if segmentHistory is empty', () => {
      service['segmentHistory'] = [];

      const expected = '';
      const actual = service.getCurrentSegment();

      expect(expected).toEqual(actual);
    });
  });

  describe('getPreviousSegment', () => {
    it('Should return previous segment if segmentHistory has more than one element', () => {
      const expected = MOCK_SEGMENT_HISTORY[MOCK_SEGMENT_HISTORY.length - 2];

      service['segmentHistory'] = [...MOCK_SEGMENT_HISTORY];
      const actual = service.getPreviousSegment();

      expect(expected).toEqual(actual);
    });

    it('Should return empty string if segmentHistory has less than two element', () => {
      service['segmentHistory'] = [MOCK_SEGMENT_HISTORY[0]];

      expect(service.getPreviousSegment()).toEqual('');
    });
  });

  describe('getPreviousUrl', () => {
    it('Should return previous segment if history has more than one element', () => {
      const expected = MOCK_HISTORY[MOCK_HISTORY.length - 2];

      service['history'] = [...MOCK_HISTORY];

      expect(service.getPreviousUrl()).toEqual(expected);
    });

    it('Should return / if history has more less than two element', () => {
      service['history'] = [MOCK_HISTORY[0]];

      expect('/').toEqual(service.getPreviousUrl());
    });
  });

  describe('getCurrentUrl', () => {
    it('Should return last segment if history has more than one element', () => {
      const expected = MOCK_HISTORY[MOCK_HISTORY.length - 1];

      service['history'] = [...MOCK_HISTORY];

      expect(expected).toEqual(service.getCurrentUrl());
    });

    it('Should return / if history has more less than two element', () => {
      expect(service.getCurrentUrl()).toEqual('/');
    });
  });

  describe('getPathName', () => {
    it('Should return string if history array not empty', () => {
      const expected = MOCK_HISTORY[MOCK_HISTORY.length - 1];

      service['history'] = [...MOCK_HISTORY];

      expect(expected).toEqual(service.getPathName());
    });

    it('Should return empty string if history array empty', () => {
      service['history'] = [MOCK_HISTORY[0]];

      expect('').toEqual(service.getPathName());
    });
  });

  describe('getPreviousRouteSnapshot', () => {
    it('Should return previous route snapshot if routeParamsHistory has more than one items', () => {
      const expected = MOCK_ACTIVATED_ROUTE_SNAPSHOTS[MOCK_ACTIVATED_ROUTE_SNAPSHOTS.length - 2];

      service['routeParamsHistory'] = [...MOCK_ACTIVATED_ROUTE_SNAPSHOTS] as any;

      expect(expected.route).toEqual((service.getPreviousRouteSnapshot() as any).route);
    });
  });

  describe('getRouteParam', () => {
    it('Should return string param if paramName matched', () => {
      expect(MOCK_SEGMENT).toEqual(service.getRouteParam(MOCK_SEGMENT, activatedSnapshot({})));
    });

    it('Should return firstChild string param if paramName matched in firstChild', () => {
      expect('test').toEqual(service.getRouteParam('test', activatedSnapshot({
        getResultFirstChild: 'test',
        getResult: null
      })));
    });

    it('Should return getRouteParam result if firstChild is not empty and has length of children', () => {
      spyOn(service, 'getRouteParam').and.returnValue(MOCK_SEGMENT);

      expect(MOCK_SEGMENT).toEqual(service.getRouteParam(MOCK_SEGMENT, activatedSnapshot({
        getResultFirstChild: null,
        getResult: null
      })));
    });

    it('Should return null if param not matched', () => {
      expect(null).toEqual(service.getRouteParam(MOCK_SEGMENT, activatedSnapshot({
        getResultFirstChild: null,
        getResult: null
      })));
    });
  });

  describe('getRouteSegment', () => {
    it('Should return empty string if routeSnapshot is null or undefined', () => {
      expect('').toEqual(service.getRouteSegment(MOCK_SEGMENT, null));
    });

    it('Should make recursion and return string result', () => {
      const snapshot: any = { firstChild: { data: {} } };

      expect('').toEqual(service.getRouteSegment(MOCK_SEGMENT, snapshot));
    });

    it('Should data property value if firstChild doesn\'t exist', () => {
      const activatedSnapshotResult = activatedSnapshot({});

      activatedSnapshotResult.firstChild = null;

      expect('test').toEqual(service.getRouteSegment('test', activatedSnapshotResult));
    });

    it('Should return empty string if firstChild and data null or undefined', () => {
      const activatedSnapshotResult = activatedSnapshot({});

      activatedSnapshotResult.firstChild = null;
      activatedSnapshotResult.data = {};

      expect('').toEqual(service.getRouteSegment('test', activatedSnapshotResult));
    });
  });

  describe('getPreviousRouteParam', () => {
    it('Should return getRouteParam result if getPreviousRouteSnapshot return result', () => {
      spyOn(service, 'getPreviousRouteSnapshot').and.returnValue('some string' as any);
      spyOn(service, 'getRouteParam').and.returnValue('test');

      expect('test').toEqual(service.getPreviousRouteParam('test'));
    });

    it('Should return null if getPreviousRouteSnapshot return undefined or null value', () => {
      spyOn(service, 'getPreviousRouteSnapshot').and.returnValue(null);

      expect(null).toEqual(service.getPreviousRouteParam('test'));
    });
  });

  describe('loadRouting', () => {
    it('Should change history and routeParamHistory if event is NavigationEnd', fakeAsync(() => {
      const urlAfterRedirects = 'http://test.com/second';
      service['navigationEndEventListener'] = jasmine.createSpy('navigationEndEventListener');

      const navigationEnd = new NavigationEnd(0, 'http://test.com/first', urlAfterRedirects);

      service['router'] = {
        events: of(navigationEnd)
      } as any;

      service.loadRouting();

      tick();

      expect(service['navigationEndEventListener']).toHaveBeenCalledWith(navigationEnd);

    }));

    it('Should call getRouteSegment method if event is RoutesRecognized', fakeAsync(() => {
      const urlAfterRedirects = 'http://test.com/second';

      const routesRecognized = new RoutesRecognized(0, 'http://test.com/first', urlAfterRedirects, {} as any);

      service['router'] = {
        events: of(routesRecognized)
      } as any;

      spyOn(service, 'getRouteSegment');

      service.loadRouting();

      tick();

      expect(service.getRouteSegment).toHaveBeenCalled();
    }));

    it('Should update segmentHistory if last segment not equal to getCurrentSegment result', fakeAsync(() => {
      const urlAfterRedirects = 'http://test.com/second';

      const routesRecognized = new RoutesRecognized(0, 'http://test.com/first', urlAfterRedirects, {} as any);

      service['router'] = {
        events: of(routesRecognized)
      } as any;

      spyOn(service, 'getRouteSegment').and.returnValue(MOCK_SEGMENT);
      spyOn(service, 'getCurrentSegment').and.returnValue(`new-${MOCK_SEGMENT}`);

      service.loadRouting();

      tick();

      expect(service['segmentHistory'][0]).toEqual(MOCK_SEGMENT);
    }));

    it('Should not update segmentHistory if last segment is equal to getCurrentSegment result', fakeAsync(() => {
      const urlAfterRedirects = 'http://test.com/second';

      const routesRecognized = new RoutesRecognized(0, 'http://test.com/first', urlAfterRedirects, {} as any);

      service['router'] = {
        events: of(routesRecognized)
      } as any;

      spyOn(service, 'getRouteSegment').and.returnValue(MOCK_SEGMENT);
      spyOn(service, 'getCurrentSegment').and.returnValue(MOCK_SEGMENT);


      service.loadRouting();

      tick();

      expect(service['segmentHistory'][0]).toBeUndefined();
    }));

    it('Should not execute listeners if other route events', fakeAsync(() => {
      (service['routerEventsReplaySubject'] as any) = {
        next: jasmine.createSpy('next')
      };
      const activateionStart = new ActivationStart(null);
      service['navigationEndEventListener'] = jasmine.createSpy('navigationEndEventListener');

      service['router'] = {
        events: of(activateionStart)
      } as any;


      service.loadRouting();

      tick();

      expect(service['navigationEndEventListener']).not.toHaveBeenCalled();
      expect(service['routerEventsReplaySubject'].next).toHaveBeenCalled();
    }));
  });

  describe('navigationEndEventListener', () => {
    it('should update history', () => {
      service['history'] = ['test0'];
      service['routeParamsHistory'] = [];

      const activatedSnapshotResult = activatedSnapshot({});

      activatedSnapshotResult.firstChild = null;
      activatedSnapshotResult.snapshot = null;

      service['route'] = activatedSnapshotResult;

      const event = {
        urlAfterRedirects: 'test'
      };

      service['navigationEndEventListener'](event);

      expect(service['history'][service['history'].length - 1]).toEqual('test');
      expect(service['routeParamsHistory'][0]).toEqual(null);
      expect(rendererService.renderer.removeClass).toHaveBeenCalled();
    });
  });
  describe('toggleVanillaScoping', () => {
    it('should apply scoping class if vanilla path', () => {
      service['toggleVanillaScoping'](true);
      const body = window.document.body;
      expect(service['rendererService'].renderer.addClass).toHaveBeenCalledWith(body, 'vn-scope');
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.VANILLA_SCOPE_CHANGE, true);
    });

    it('should remove scoping class if not vanilla path', () => {
      service['toggleVanillaScoping'](false);
      const body = window.document.body;
      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.VANILLA_SCOPE_CHANGE, false);
      expect(service['rendererService'].renderer.removeClass).toHaveBeenCalledWith(body, 'vn-scope');
    });
  });

  describe('toggleBmaScoping', () => {
    it('should apply remove bma class if vanilla path', () => {
      const el = {};
      windowRefService.document.querySelector.and.returnValue(el);
      service['toggleBmaScoping'](true);
      expect(service['rendererService'].renderer.addClass).toHaveBeenCalledWith(el, 'vn-bma');
    });

    it('should add bma class if not vanilla path', () => {
      const el = {};
      windowRefService.document.querySelector.and.returnValue(el);
      service['toggleBmaScoping'](false);
      expect(service['rendererService'].renderer.removeClass).toHaveBeenCalledWith(el, 'vn-bma');
    });

    it('should not add or remove bma class', () => {
      service['toggleBmaScoping'](true);
      expect(service['rendererService'].renderer.addClass).not.toHaveBeenCalled();
    });
  });
  describe('togglePortalSwitch', () => {
    it('should apply vanilla class and remove bma if vanilla path', () => {
      service['toggleBmaScoping'] = jasmine.createSpy();
      service['getCurrentSegment'] = jasmine.createSpy().and.returnValue('test');
      service['toggleVanillaScoping'] = jasmine.createSpy();
      service['route'].firstChild.firstChild.snapshot.data.segment = 'vanilla';
      service['togglePortalSwitch']();

      expect(service['toggleBmaScoping']).toHaveBeenCalledWith(true);
      expect(service['toggleVanillaScoping']).toHaveBeenCalledWith(false);
    });

    it('should remove vanilla class and add bma if not vanilla path', () => {
      service['toggleBmaScoping'] = jasmine.createSpy();
      service['getCurrentSegment'] = jasmine.createSpy().and.returnValue('vanilla');
      service['toggleVanillaScoping'] = jasmine.createSpy();
      service['togglePortalSwitch']();

      expect(service['toggleBmaScoping']).toHaveBeenCalledWith(false);
      expect(service['toggleVanillaScoping']).toHaveBeenCalledWith(true);
    });
  });

  describe('#navigateUri', () => {
    beforeEach(() => {
      mouseEvent = {
        preventDefault: jasmine.createSpy()
      } as any;
    })
    it('should not call navigateByUrl when sportName is horseracing and tab is featured', () => {
      service['router'] = {
        navigateByUrl: jasmine.createSpy(),
        url: '/horse-racing'
      } as any;
      service.navigateUri(mouseEvent, '/horse-racing/featured', 'horseracing', '');
      expect(service['router'].navigateByUrl).not.toHaveBeenCalled();
    });
    it('should not call navigateByUrl when sportName is greyhound and tab is today', () => {
      service['router'] = {
        navigateByUrl: jasmine.createSpy(),
        url: '/greyhound-racing'
      } as any;
      service.navigateUri(mouseEvent, '/greyhound-racing/today', 'greyhound', 'today');
      expect(service['router'].navigateByUrl).not.toHaveBeenCalled();
    });
    it('should not call navigateByUrl when sportName is greyhound and tab is races', () => {
      service['router'] = {
        navigateByUrl: jasmine.createSpy(),
        url: '/greyhound-racing'
      } as any;
      service.navigateUri(mouseEvent, '/greyhound-racing/races/next', 'greyhound', 'races');
      expect(service['router'].navigateByUrl).not.toHaveBeenCalled();
    });
    it('should call navigateByUrl when sport is other than races', () => {
      service.navigateUri(mouseEvent, '/football','football', '');
      expect(service['router'].navigateByUrl).toHaveBeenCalled();
    });
  });

  it('#replayRouterEvents should return an instance of ReplaySubject', () => {
    expect(service.replayRouterEvents).toEqual(jasmine.any(Observable));
  });

  it('#loadRoutingHandler should emit event', () => {
    (service['routerEventsReplaySubject'] as any) = {
      next: jasmine.createSpy('next')
    };
    service['loadRoutingHandler'](new NavigationEnd(0, '/', '/'));
    expect(service['routerEventsReplaySubject'].next).toHaveBeenCalledWith(new NavigationEnd(0, '/', '/'));
  });
});
