import { fakeAsync, tick } from '@angular/core/testing';
import { PrivateMarketsComponent } from '@coralDesktop/desktop/components/privateMarkets/private-markets.component';
import { of, throwError } from 'rxjs';

describe('PrivateMarketsComponent', () => {
  let component: PrivateMarketsComponent, pubSubService, userService, privateMarketsService, sessionService;

  beforeEach(() => {
    pubSubService = {
      API: {
        SUCCESSFUL_LOGIN: 'SUCCESSFUL_LOGIN',
        LIVE_SERVE_MS_UPDATE: 'LIVE_SERVE_MS_UPDATE',
        SESSION_LOGOUT: 'SESSION_LOGOUT'
      },
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };

    userService = {
      status: true
    };

    sessionService = {
      whenUserSession: jasmine.createSpy('whenUserSession').and.returnValue(of({}))
    };

    privateMarketsService = jasmine.createSpyObj('PrivateMarketsService', ['markets', 'subscribe', 'unsubscribe']);

    component = new PrivateMarketsComponent(pubSubService, userService, privateMarketsService, sessionService);
  });

  describe('ngOnInit', () => {

    beforeEach(() => {
      component['sessionService'].whenUserSession = jasmine.createSpy('whenUserSession').and.returnValue(of(null));
      component['loadPrivateMarkets'] = jasmine.createSpy('loadPrivateMarkets');
    });

    it('should call loadPrivateMarkets', () => {
      pubSubService.subscribe.and.callFake((name, method, cb) => {
        if (method.indexOf(pubSubService.API.SUCCESSFUL_LOGIN) >= 0) {
          cb();
        }
      });

      component.ngOnInit();

      expect(component['sessionService'].whenUserSession).toHaveBeenCalled();
      expect(component['loadPrivateMarkets']).toHaveBeenCalledTimes(2);
    });

    it('should send an error message into the console', () => {
      component['sessionService'].whenUserSession = jasmine.createSpy('whenUserSession').and.returnValue(throwError('error'));
      spyOn(console, 'error');

      component.ngOnInit();

      expect(console.error).toHaveBeenCalledWith('error');
    });

    it('should check nothing', () => {
      component['checkOutcomes'] = jasmine.createSpy('checkOutcomes').and.returnValue(true);
      component.events = [];
      pubSubService.subscribe.and.callFake((name, method, cb) => {
        if (method.indexOf(pubSubService.API.LIVE_SERVE_MS_UPDATE) >= 0) {
          cb();
        }
      });

      component.ngOnInit();

      expect(component.events).toEqual([]);
    });

    it('should unsubscribe and set an empty array into events', () => {
      component['privateMarketsService'].unsubscribe = jasmine.createSpy('privateMarketsService');
      const events= [{
        markets: []
      } as any];
      component.events = events;
      pubSubService.subscribe.and.callFake((name, method, cb) => {
        if (method.indexOf(pubSubService.API.SESSION_LOGOUT) >= 0) {
          cb();
        }
      });

      component.ngOnInit();

      expect(component['privateMarketsService'].unsubscribe).toHaveBeenCalledWith(events);
      expect(component.events).toEqual([]);
    });
  });

  describe('limitTo', () => {
    it('should slice outcomes', () => {
      const market = {
        allShown: false
      } as any, outcomes = [{}, {}, {}, {}, {}] as any;

      expect(component.limitTo(market, outcomes)).toEqual([{}, {}, {}] as any);
    });

    it('should not slice outcomes', () => {
      const market = {
        allShown: true
      } as any, outcomes = [{}, {}, {}, {}, {}] as any;

      expect(component.limitTo(market, outcomes)).toEqual(outcomes);
    });
  });

  it('trackByEvents should create value for tracking', () => {
    const event = {
      id: 123,
      categoryId: 'categoryId'
    } as any;

    expect(component.trackByEvents(1, event)).toEqual(`${event.id}_${event.categoryId}`);
  });

  it('trackByMarkets should create value for tracking', () => {
    const market = {
      id: 'id',
    } as any;

    expect(component.trackByMarkets(1, market)).toEqual(market.id);
  });

  it('trackByOutcomes should create value for tracking', () => {
    const outcome = {
      id: 'id',
    } as any;

    expect(component.trackByOutcomes(1, outcome)).toEqual(outcome.id);
  });

  it('ngOnDestroy should unsubscribe from services', () => {
    component.events = [];

    component.ngOnDestroy();

    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('PrivateMarketsComponent');
    expect(privateMarketsService.unsubscribe).toHaveBeenCalledWith(component.events);
  });

  describe('checkOutcomes', () => {
    it('should return true', () => {
      component.events = [{
        markets: [{
          outcomes: [{
            isDisplayed: false
          }]
        }]
      } as any];

      expect(component['checkOutcomes']()).toEqual(true);
    });
  });

  describe('loadPrivateMarkets', () => {
    it('should call .markets() and receive events', fakeAsync(() => {
      const events = [{} as any];
      privateMarketsService.markets.and.returnValue(of(events));

      component['loadPrivateMarkets']();

      expect(privateMarketsService.markets).toHaveBeenCalled();
      tick();
      expect(privateMarketsService.subscribe).toHaveBeenCalledWith(events);
      expect(component.events).toEqual(events);
    }));

    it('should do nothing', () => {
      component['userService'] = { status: false } as any;
      privateMarketsService.markets.and.returnValue(Promise.resolve([{}]));

      component['loadPrivateMarkets']();

      expect(privateMarketsService.markets).not.toHaveBeenCalled();
      expect(privateMarketsService.subscribe).not.toHaveBeenCalled();
    });
  });
});
