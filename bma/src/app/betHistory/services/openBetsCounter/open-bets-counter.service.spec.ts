import { Observable, of, throwError } from 'rxjs';

import { IFilteredPageBets } from '@app/betHistory/models/bet-history.model';

import {
  OpenBetsCounterService as OpenBetsCounterBaseService,
  OpenBetsCounterService
} from '@app/betHistory/services/openBetsCounter/open-bets-counter.service';

describe('OpenBetsCounterService', () => {
  let service: OpenBetsCounterService;
  let pubSubService;
  let userService;
  let sessionService;
  let betHistoryMainService;
  const filter = '';
  const betType = 'open';
  let authService;
  let observer;
  beforeEach(() => {
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        BETS_COUNTER_PLACEBET: 'BETS_COUNTER_PLACEBET',
        BETS_COUNTER_OPEN_BETS: 'BETS_COUNTER_OPEN_BETS',
        SESSION_LOGOUT: 'SESSION_LOGOUT',
        SESSION_LOGIN: 'SESSION_LOGIN'
      }
    };
    userService = {
      isInShopUser: jasmine.createSpy().and.returnValue(false)
    };
    sessionService = {
      whenUserSession: jasmine.createSpy('whenUserSession').and.returnValue(of({})),
      whenProxySession: jasmine.createSpy('whenProxySession').and.returnValue(of(null))
    };
    betHistoryMainService = {
      getBetsCountForYear: jasmine.createSpy('getBetsCountForYear').and.returnValue(of({ betCount: '' } as any))
    };
    authService = {
      sessionLoggedIn: of(null)
    };
    service = new OpenBetsCounterService(pubSubService, userService, sessionService, betHistoryMainService, authService);
  });

  it('#constructor', () => {
    expect(service).toBeTruthy();
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'BetsCounter',
      'BETS_COUNTER_PLACEBET',
      jasmine.any(Function)
    );
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'BetsCounter',
      'BETS_COUNTER_OPEN_BETS',
      jasmine.any(Function)
    );
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'BetsCounter',
      undefined,
      jasmine.any(Function)
    );
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'BetsCounter',
      'SESSION_LOGOUT',
      jasmine.any(Function)
    );
  });

  describe('#init', () => {
    beforeEach(() => {
      authService.sessionLoggedIn = Observable.create(o => observer = o);
      service['getOpenBetsCount'] = jasmine.createSpy('getOpenBetsCount');
      spyOn(OpenBetsCounterBaseService.prototype as any, 'loadData');
    });
    it('should subscribe to authService.sessionLoggedIn', () => {
      service.init();
      observer.next(null);

      expect(sessionService.whenUserSession).toHaveBeenCalled();
      expect(service['loadData']).toHaveBeenCalled();
    });

    it('should not call loadData', () => {
      sessionService.whenUserSession.and.returnValue(of(throwError(null)));
      service.init();
      expect(sessionService.whenUserSession).not.toHaveBeenCalled();
      expect(service['loadData']).not.toHaveBeenCalled();
    });
  });

  it('#unsubscribeBetsCounter', () => {
    service.unsubscribeBetsCounter();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('BetsCounter');
  });

  describe('#handleMyBetsCounter', () => {
    let getValue;
    let next;

    beforeEach(() => {
      getValue = jasmine.createSpy('getValue').and.returnValue({ count: 10, moreThanTwenty: false });
      next = jasmine.createSpy('next');

      service['openBetsCount$'] = { getValue, next } as any;
    });

    it('handleMyBetsCounter call without params', () => {
      service['handleMyBetsCounter']();
      expect(next).toHaveBeenCalledWith({ count: 11, moreThanTwenty: false });
    });

    it('handleMyBetsCounter call without params less than 20', () => {
      service['handleMyBetsCounter'](2);
      expect(next).toHaveBeenCalledWith({ count: 12, moreThanTwenty: false });
    });

    it('handleMyBetsCounter call without params more than 20', () => {
      service['handleMyBetsCounter'](22);
      expect(next).toHaveBeenCalledWith({ count: 20, moreThanTwenty: true });
    });

    afterEach(() => {
      expect(getValue).toHaveBeenCalled();
    });
  });

  describe('#handleBetsCunterOpenBets', () => {
    let pageBets;
    let next;

    beforeEach(() => {
      next = jasmine.createSpy('next');
      pageBets = {
        data: {
          // eslint-disable-next-line prefer-spread
          bets: Array.apply(null, Array(22)).map(() => {}),
          pageToken: 'dsdda'
        },
        filter: 'bet'
      };
      service['openBetsCount$'] = { next } as any;
    });

    it('should call next with count = 20', () => {
      service['handleBetsCunterOpenBets'](pageBets as IFilteredPageBets);

      expect(service['openBetsCount$'].next).toHaveBeenCalledWith({ count: 20, moreThanTwenty: true });
    });

    it('should call next with count = 20', () => {
      pageBets = {
        data: {
          // eslint-disable-next-line prefer-spread
          bets: Array.apply(null, Array(22)).map(() => {}),
          pageToken: ''
        },
        filter: 'bet'
      };
      service['handleBetsCunterOpenBets'](pageBets as IFilteredPageBets);

      expect(service['openBetsCount$'].next).toHaveBeenCalledWith({ count: 20, moreThanTwenty: true });
    });

    it('should call next with count = 10', () => {
      pageBets = {
        data: {
          // eslint-disable-next-line prefer-spread
          bets: Array.apply(null, Array(10)).map(() => {}),
          pageToken: ''
        },
        filter: 'bet'
      };
      service['handleBetsCunterOpenBets'](pageBets as IFilteredPageBets);

      expect(service['openBetsCount$'].next).toHaveBeenCalledWith({ count: 10, moreThanTwenty: false });
    });

    it('should call next with count = 0', () => {
      pageBets = {
        data: {
          bets: [],
          pageToken: ''
        },
        filter: 'bet'
      };
      service['handleBetsCunterOpenBets'](pageBets as IFilteredPageBets);

      expect(service['openBetsCount$'].next).toHaveBeenCalledWith({ count: 0, moreThanTwenty: false });
    });

    it('should not call next', () => {
      pageBets = {
        data: {
          bets: [],
          pageToken: ''
        },
        filter: ''
      };

      expect(service['openBetsCount$'].next).not.toHaveBeenCalled();
    });

    it('should not call next', () => {
      pageBets = {
        data: {
          // eslint-disable-next-line prefer-spread
          bets: Array.apply(null, Array(10)).map(() => {}),
          pageToken: ''
        },
        filter: ''
      };
      service['handleBetsCunterOpenBets'](pageBets as IFilteredPageBets);

      expect(service['openBetsCount$'].next).not.toHaveBeenCalled();
    });

    it('should not call next', () => {
      pageBets = {};
      service['handleBetsCunterOpenBets'](pageBets as IFilteredPageBets);

      expect(service['openBetsCount$'].next).not.toHaveBeenCalled();
    });
  });

  describe('#handleCashoutBet', () => {
    let next;

    beforeEach(() => {
      service['decreaseCount'] = jasmine.createSpy('decreaseCount');
      next = jasmine.createSpy('next');
      service['openBetsCount$'] = {
        getValue: jasmine.createSpy('getValue').and.returnValue({ count: 10, moreThanTwenty: false }),
        next
      } as any;
      service['loadData'] = jasmine.createSpy('loadData');
    });

    it('should call decreaseCount', () => {
      service['handleCashoutBet']();

      expect(service['decreaseCount']).toHaveBeenCalledWith(10);
      expect(service['loadData']).not.toHaveBeenCalled();
    });

    it('should call loadData', () => {
      service['openBetsCount$'] = {
        getValue: jasmine.createSpy('getValue').and.returnValue({ count: 20, moreThanTwenty: true }),
        next
      } as any;
      service['handleCashoutBet']();

      expect(service['decreaseCount']).not.toHaveBeenCalled();
      expect(service['loadData']).toHaveBeenCalled();
    });

    it('should not call loadData or decreaseCount', () => {
      service['openBetsCount$'] = {
        getValue: jasmine.createSpy('getValue').and.returnValue({ count: 0, moreThanTwenty: false }),
        next
      } as any;
      service['handleCashoutBet']();

      expect(service['decreaseCount']).not.toHaveBeenCalled();
      expect(service['loadData']).not.toHaveBeenCalled();
    });

    afterEach(() => {
      expect(service['openBetsCount$'].getValue).toHaveBeenCalled();
    });
  });

  describe('#decreaseCount', () => {
    beforeEach(() => {
      service['openBetsCount$'] = {
        next: jasmine.createSpy('next')
      } as any;
    });

    it('should return count = 0', () => {
      service['decreaseCount'](1);

      expect(service['openBetsCount$'].next).toHaveBeenCalledWith({ count: 0, moreThanTwenty: false });
    });

    it('should return count = 3', () => {
      service['decreaseCount'](4);

      expect(service['openBetsCount$'].next).toHaveBeenCalledWith({ count: 3, moreThanTwenty: false });
    });
  });

  it('#getOpenBetsCount', () => {
    const asObservable = jasmine.createSpy('asObservable');

    service['openBetsCount$'] = { asObservable } as any;
    service['getOpenBetsCount']();

    expect(asObservable).toHaveBeenCalled();
  });

  describe('#handleLogOut', () => {
    let next;
    let unsubscribeSpy;

    beforeEach(() => {
      next = jasmine.createSpy('next');
      unsubscribeSpy = jasmine.createSpy('unsubscribeSpy');

      service['openBetsCount$'] = { next } as any;
    });

    it('should call next and unsubscribe', () => {
      service['loadDataSub'] = { unsubscribe: unsubscribeSpy } as any;
      service['handleLogOut']();

      expect(unsubscribeSpy).toHaveBeenCalledTimes(1);
    });

    it('should call next', () => {
      service['handleLogOut']();
      expect(unsubscribeSpy).not.toHaveBeenCalled();
    });

    afterEach(() => {
      expect(service['openBetsCount$'].next).toHaveBeenCalledWith({ count: 0, moreThanTwenty: false });
    });
  });

  describe('#loadData', () => {
    let next;
    let unsubscribeSpy;

    beforeEach(() => {
      next = jasmine.createSpy('next');
      unsubscribeSpy = jasmine.createSpy('unsubscribeSpy');
    });

    it('should unsubscribe from loadData subscription', () => {
      service['loadDataSub'] = { unsubscribe: unsubscribeSpy } as any;
      service['openBetsCount$'] = { next } as any;
      service['loadData']();

      expect(unsubscribeSpy).toHaveBeenCalledTimes(1);
      expect(sessionService.whenProxySession).toHaveBeenCalled();
      expect(betHistoryMainService.getBetsCountForYear).toHaveBeenCalled();
      expect(service['openBetsCount$'].next).toHaveBeenCalledWith({ count: 0, moreThanTwenty: false });
    });

    it('should not unsubscribe from loadData subscription', () => {
      service['loadData']();

      expect(unsubscribeSpy).not.toHaveBeenCalled();
    });

    it('should return count=0 for in-shop user', () => {
      (userService.isInShopUser as any).and.returnValue(true);
      service['openBetsCount$'] = { next } as any;

      service['loadData']();
      expect(service['openBetsCount$'].next).toHaveBeenCalledWith({ count: 0, moreThanTwenty: false });
      expect(betHistoryMainService.getBetsCountForYear).not.toHaveBeenCalled();
      expect(sessionService.whenProxySession).not.toHaveBeenCalled();
    });

    it('should return { count: 20, moreThanTwenty: true }', () => {
      betHistoryMainService.getBetsCountForYear.and.returnValue(of({ betCount: '20+' }));
      service['openBetsCount$'] = { next } as any;
      service['loadData']();

      expect(sessionService.whenProxySession).toHaveBeenCalled();
      expect(betHistoryMainService.getBetsCountForYear).toHaveBeenCalledWith(filter, betType);
      expect(next).toHaveBeenCalledWith({ count: 20, moreThanTwenty: true });
    });

    it('should return { count: 15, moreThanTwenty: false }', () => {
      betHistoryMainService.getBetsCountForYear.and.returnValue(of({ betCount: '15' }));
      service['openBetsCount$'] = { next } as any;
      service['loadData']();

      expect(sessionService.whenProxySession).toHaveBeenCalled();
      expect(betHistoryMainService.getBetsCountForYear).toHaveBeenCalledWith(filter, betType);
      expect(next).toHaveBeenCalledWith({ count: 15, moreThanTwenty: false });
    });

    it('should not call next', () => {
      betHistoryMainService.getBetsCountForYear.and.returnValue(of(null));
      service['openBetsCount$'] = { next } as any;
      service['loadData']();

      expect(sessionService.whenProxySession).toHaveBeenCalled();
      expect(betHistoryMainService.getBetsCountForYear).toHaveBeenCalledWith(filter, betType);
      expect(service['openBetsCount$'].next).not.toHaveBeenCalled();
    });

    it('should not call next2', () => {
      sessionService.whenProxySession.and.returnValue(of());
      betHistoryMainService.getBetsCountForYear.and.returnValue(of(null));
      service['openBetsCount$'] = { next } as any;
      service['loadData']();

      expect(sessionService.whenProxySession).toHaveBeenCalled();
      expect(betHistoryMainService.getBetsCountForYear).not.toHaveBeenCalled();
      expect(service['openBetsCount$'].next).not.toHaveBeenCalled();
    });

    it('should return { count: 0, moreThanTwenty: false }', () => {
      service['openBetsCount$'] = { next } as any;
      service['loadData']();

      expect(sessionService.whenProxySession).toHaveBeenCalled();
      expect(betHistoryMainService.getBetsCountForYear).toHaveBeenCalledWith(filter, betType);
      expect(service['openBetsCount$'].next).toHaveBeenCalledWith({ count: 0, moreThanTwenty: false });
    });
  });
});
