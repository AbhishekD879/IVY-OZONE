import { YourcallProviderService } from '@yourcall/services/yourcallProvider/yourcall-provider.service';
import { fakeAsync, tick } from '@angular/core/testing';
import { of, throwError } from 'rxjs';

describe('YourcallProviderService', () => {
  let service: YourcallProviderService;
  let http: any;
  let bybApiService: any;
  let bYBHelperService: any;
  let prepareRequest: any;
  let tryMethod: any;
  let methods: any;

  beforeEach(() => {
    bybApiService = {
      prepareRequest: jasmine.createSpy('prepareRequest')
    };
    bYBHelperService = {};

    http = jasmine.createSpyObj('http', ['get', 'post']);

    service = new YourcallProviderService(bybApiService, bYBHelperService, http);

    prepareRequest = spyOn<any>(service, 'prepareRequest');
    tryMethod = spyOn(service, 'try');

    methods = {
      code: 'test-code',
      extendParams: jasmine.createSpy('extendParams'),
      getUri: jasmine.createSpy('getUri'),
      getLeagues: jasmine.createSpy('getLeagues'),
      getUpcomingLeagues: jasmine.createSpy('getUpcomingLeagues'),
      getLeagueEvents: jasmine.createSpy('getLeagueEvents'),
      getGames: jasmine.createSpy('getGames'),
      getGameInfo: jasmine.createSpy('getGameInfo'),
      getEDPMarkets: jasmine.createSpy('getEDPMarkets'),
      getPlayers: jasmine.createSpy('getPlayers'),
      getMatchMarkets: jasmine.createSpy('getMatchMarkets'),
      getStatistics: jasmine.createSpy('getStatistics'),
      getMaxExposure: jasmine.createSpy('getMaxExposure'),
      getStatValues: jasmine.createSpy('getStatValues'),
      calculateOdds: jasmine.createSpy('calculateOdds'),
      calculateAccumulatorOdds: jasmine.createSpy('calculateAccumulatorOdds'),
      getBets: jasmine.createSpy('getBets'),
      getMarketSelections: jasmine.createSpy('getMarketSelections'),
    } as any;

    service['provider'].api = methods;
  });

  it('should create', () => {
    expect(service).toBeTruthy();
  });

  describe('try', () => {
    it('should return true if provider exist', () => {
      tryMethod.and.callThrough();

      expect(service.try('BYB')).toBeTruthy();
    });

    it('should return false if provider doesn\'t exist', () => {
      expect(service.try('unknownApi')).toBeFalsy();
    });
  });

  it('getLeagues should return correct promise result', () => {
    service.getLeagues();

    expect(service['provider'].api['getLeagues']).toHaveBeenCalled();
  });

  it('getUpcomingLeagues should return correct promise result', () => {
    service.getUpcomingLeagues();

    expect(service['provider'].api['getUpcomingLeagues']).toHaveBeenCalled();
  });

  it('getLeagueEvents should return correct promise result', () => {
    service.getLeagueEvents([1, 2, 3], 'some perios' as any);

    expect(service['provider'].api['getLeagueEvents']).toHaveBeenCalledWith([1, 2, 3], 'some perios' as any);
  });

  it('getGames should return correct promise result', () => {
    service.getGames([1, 2, 3]);

    expect(service['provider'].api['getGames']).toHaveBeenCalledWith([1, 2, 3]);
  });

  it('getGameInfo should return correct promise result', () => {
    service.getGameInfo('someId');

    expect(service['provider'].api['getGameInfo']).toHaveBeenCalledWith('someId');
  });

  it('getEDPMarkets should return correct promise result', () => {
    service.getEDPMarkets();

    expect(service['provider'].api['getEDPMarkets']).toHaveBeenCalled();
  });

  it('getPlayers should return correct promise result', () => {
    service.getPlayers(1);

    expect(service['provider'].api['getPlayers']).toHaveBeenCalledWith(1);
  });

  it('getMatchMarkets should return correct promise result', () => {
    service.getMatchMarkets('someEvent' as any);

    expect(service['provider'].api['getMatchMarkets']).toHaveBeenCalledWith('someEvent' as any);
  });

  it('getStatistics should return correct promise result', () => {
    service.getStatistics('someEvent' as any);

    expect(service['provider'].api['getStatistics']).toHaveBeenCalledWith('someEvent' as any);
  });

  it('getMaxExposure should return correct promise result', () => {
    service.getMaxExposure('someParam' as any);

    expect(service['provider'].api['getMaxExposure']).toHaveBeenCalledWith('someParam');
  });

  it('getStatValues should return correct promise result', () => {
    service.getStatValues('someParam' as any);

    expect(service['provider'].api['getStatValues']).toHaveBeenCalledWith('someParam' as any);
  });

  it('calculateOdds should return correct promise result', () => {
    service.calculateOdds('someParam' as any);

    expect(service['provider'].api['calculateOdds']).toHaveBeenCalledWith('someParam');
  });

  it('calculateAccumulatorOdds should return correct promise result', () => {
    service.calculateAccumulatorOdds('someParam' as any);

    expect(service['provider'].api['calculateAccumulatorOdds']).toHaveBeenCalledWith('someParam' as any);
  });

  it('getBets should return correct promise result', () => {
    service.getBets('someParam' as any);

    expect(service['provider'].api['getBets']).toHaveBeenCalledWith('someParam' as any);
  });

  it('getMarketSelections should return correct promise result', () => {
    service.getMarketSelections('someParam' as any);

    expect(service['provider'].api['getMarketSelections']).toHaveBeenCalledWith('someParam' as any);
  });

  describe('use', () => {
    it('should return correct result if provideAPI not equal API', () => {
      tryMethod.and.returnValue('unknownProviderApi');
      service['pendingRequestsList'] = [{complete: () => 'complete'}] as any;
      service.use('providerApi');

      expect(service['pendingRequestsList'].length).toEqual(0);
    });

    it('should return correct if provideAPI equal API', () => {
      spyOnProperty(service, 'API', 'get').and.returnValue(null);
      tryMethod.and.returnValue(null);

      service['pendingRequestsList'] = [{complete: () => 'complete'}] as any;
      service.use('providerApi');

      expect(service['pendingRequestsList'].length).toEqual(1);
    });
  });

  describe('useOnce', () => {
    it('should return correct if provideAPI not equal API', () => {
      tryMethod.and.returnValue('BYB');

      const actual = service.useOnce('BYB');

      expect((actual['provider'] as any).api).toBeTruthy();
    });

    it('should return current API if providerAPI not found', fakeAsync(() => {
      tryMethod.and.returnValue(null);

      const actual = service.useOnce('BYB2');

      expect(actual['provider']).toBeFalsy();
    }));
  });

  describe('isValidResponse', () => {
    it('should return true if error exist', () => {
      expect(service.isValidResponse('some error', 'request name')).toBeTruthy();
    });

    it('should return true if error doesn\'t exist', () => {
      expect(service.isValidResponse(undefined, null)).toBeFalsy();
    });
  });

  it('helper should return true if error exist', () => {
    service['provider'].helper = 'someHelper' as any;

    expect(service.helper as any).toEqual('someHelper');
  });

  // PRIVATE METHODS
  describe('releaseRequest', () => {
    it('should return true if index more than 0', () => {
      spyOn(service['pendingRequestsList'], 'indexOf').and.returnValue(1);

      expect(service['releaseRequest'](of('some obs') as any)).toBeTruthy();
    });

    it('should return false if index less than 0', () => {
      spyOn(service['pendingRequestsList'], 'indexOf').and.returnValue(-1);

      expect(service['releaseRequest'](of('some obs') as any)).toBeFalsy();
    });
  });

  describe('releaseRequest', () => {
    let createRequest: any;

    beforeEach(() => {
      (service['provider'].api.getUri as any).and.returnValue('some-uri');
      (service['provider'].api.extendParams as any).and.returnValue('some-params');
      createRequest = spyOn<any>(service, 'createRequest').and.returnValue(of('some-obs-result'));
      prepareRequest.and.callThrough();
    });

    it('should return promise if request has promise', fakeAsync(() => {
      const actual = service['prepareRequest'](Promise.resolve('test' as any));

      tick();

      actual.then(value => {
        expect(value).toEqual('test');
      });
    }));

    it('should return new promise if request has resolve method', fakeAsync(() => {
      const actual = service['prepareRequest'](Promise as any);

      tick();

      actual.then(value => {
        expect(value).toBeTruthy();
      });
    }));

    it('should call createRequest method with correct params', () => {
      const params = {a: 1, b: 2};

      service['prepareRequest']({params, method: 'POST'} as any);

      expect(createRequest).toHaveBeenCalledWith('some-uri', 'POST', 'some-params');
    });

    it('should set request type GET as default if method is undefined', () => {
      const params = {a: 1, b: 2};

      service['prepareRequest']({params} as any);

      expect(createRequest).toHaveBeenCalledWith('some-uri', 'GET', 'some-params');
    });

    describe('createRequest', () => {
      beforeEach(() => {
        spyOn<any>(service, 'releaseRequest');
        createRequest.and.callThrough();
      });

      it('should create GET request and return correct result', fakeAsync(() => {
        const returnData = of({body: 'test'});

        http.get.and.returnValue(returnData as any);

        service['createRequest']('some-uri', 'GET', {a: 1, b: 2}).subscribe(result => {
          expect(result).toEqual('test');
          expect(service['http'].get).toHaveBeenCalled();
        });
      }));

      it('should create POST request and return correct result', fakeAsync(() => {
        const returnData = of({body: 'test'});

        http.post.and.returnValue(returnData as any);

        service['createRequest']('some-uri', 'POST', {a: 1, b: 2}).subscribe(result => {
          expect(result).toEqual('test');
          expect(service['http'].post).toHaveBeenCalled();
        });
      }));

      it('should handle error if observable throw error', () => {
        const returnData = throwError('error');

        http.post.and.returnValue(returnData);

        service['createRequest']('some-uri', 'POST', {a: 1, b: 2}).subscribe({
          error: val => expect(val).toEqual('error')
        });
      });
    });
  });

  it('getLeagueEventsWithoutPeriod should call prepareRequest', () => {
    service['provider'] = {
      api: {
        getLeagueEventsWithoutPeriod: jasmine.createSpy('getLeagueEventsWithoutPeriod')
      }
    } as any;

    service.getLeagueEventsWithoutPeriod();

    expect(prepareRequest).toHaveBeenCalledWith(service['provider'].api.getLeagueEventsWithoutPeriod());
  });

  it('showcard players get ', () => {
    service.bybPlayers = {'Ronaldo': true};

    expect(service.showCardPlayers).toEqual({'Ronaldo': true});
  });
  
  it('showcard players set ', () => {
    service.showCardPlayers = {'Ronaldo': true};

    expect(service.bybPlayers).toEqual({'Ronaldo': true});
  });
});
