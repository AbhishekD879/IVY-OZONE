import { HttpParams } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';

import { SiteServerRequestHelperService } from './site-server-request-helper.service';

describe('SiteServerRequestHelperService', () => {
  let http;
  let service: SiteServerRequestHelperService;

  beforeEach(() => {
    http = {
      get: jasmine.createSpy()
    };

    service = new SiteServerRequestHelperService(http);
  });

  function createPerformRequestSpy() {
    service['performRequest'] = jasmine.createSpy().and.returnValue(of({}));
  }

  describe('getOutrightsByTypeIds', () => {
    it('it should sent request without childCount', () => {
      createPerformRequestSpy();

      const params = { typeId: '1', simpleFilters: 'status=online' };
      service.getOutrightsByTypeIds(params);

      expect(service['performRequest']).toHaveBeenCalledWith(
        `${service['SSEndpoint']}/EventToOutcomeForType/${params.typeId}?${params.simpleFilters}`,
        jasmine.any(HttpParams)
      );
    });

    it('it should sent request with childCount', () => {
      createPerformRequestSpy();

      const params = { typeId: '1', simpleFilters: 'status=online', childCount: true };
      service.getOutrightsByTypeIds(params);

      expect(service['performRequest']).toHaveBeenCalledWith(
        `${service['SSEndpoint']}/EventToOutcomeForType/${params.typeId}?${params.simpleFilters}`,
        jasmine.any(HttpParams)
      );
    });
  });

  it('getCouponsByIds', () => {
    createPerformRequestSpy();

    const params = { couponsIds: '1', simpleFilters: 'status=online' };
    service.getCouponsByIds(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/CouponToOutcomeForCoupon/${params.couponsIds}?${params.simpleFilters}`
    );
  });

  it('getCouponsList', () => {
    createPerformRequestSpy();

    const params = { simpleFilters: 'status=online' };
    service.getCouponsList(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/Coupon?${params.simpleFilters}`
    );
  });

  it('getOutcomeByExternalId', () => {
    createPerformRequestSpy();

    const params = { id: '1' };
    service.getOutcomeByExternalId(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/EventToOutcomeForOutcome/~ext-ExternalOutcome:outcome:${params.id}`
    );
  });

  it('getOutcomeByExternalIds', () => {
    createPerformRequestSpy();

    const params = { ids: '1,2' };
    service.getOutcomeByExternalIds(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/EventToOutcomeForOutcome/${params.ids}`, jasmine.any(HttpParams)
    );
  });

  it('getEvent', () => {
    createPerformRequestSpy();

    const params = { eventId: 1 };
    service.getEvent(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/Event/${params.eventId}`, jasmine.any(HttpParams)
    );
  });

  it('getEventByIds', () => {
    createPerformRequestSpy();

    const params = { eventsIds: '1,2', simpleFilters: 'vip=1' };
    service.getEventByIds(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/EventToOutcomeForEvent/${params.eventsIds}?${params.simpleFilters}`,
      jasmine.any(HttpParams)
    );
  });

  it('getEventToOutcomeForOutcome', () => {
    createPerformRequestSpy();

    const params = { outcomesIds: '1,2' };
    service.getEventToOutcomeForOutcome(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/EventToOutcomeForOutcome/${params.outcomesIds}`
    );
  });

  it('getEventsByOutcomes', () => {
    createPerformRequestSpy();

    const params = { outcomesIds: '1,2', simpleFilters: 'started=1' };
    service.getEventsByOutcomes(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/EventToOutcomeForOutcome/${params.outcomesIds}?${params.simpleFilters}`,
      jasmine.any(HttpParams)
    );
  });

  it('getEventsByOutcomes with includeDisplay true simpleFilter', () => {
    createPerformRequestSpy();

    const params = { outcomesIds: '1,2', simpleFilters: 'event.suspendAtTime:greaterThan:2023-07-25T19:57:00.000Z&includeUndisplayed=true' };
    service.getEventsByOutcomes(params);

    expect(service['performRequest']).toHaveBeenCalled();
  });

  it('getEventsByOutcomes with no outcomes', () => {
    createPerformRequestSpy();

    const params = { outcomesIds: undefined, simpleFilters: 'event.suspendAtTime:greaterThan:2023-07-25T19:57:00.000Z&includeUndisplayed=true' };
    service.getEventsByOutcomes(params);

    expect(service['performRequest']).toHaveBeenCalled();
  });

  it('getEventsByOutcomes with no outcomes', () => {
    service.isValidFzSelection = true;
    createPerformRequestSpy();
    const params = { outcomesIds: undefined, simpleFilters: 'event.suspendAtTime:greaterThan:2023-07-25T19:57:00.000Z&includeUndisplayed=true' };
    service.getEventsByOutcomes(params);
    
    expect(service['performRequest']).toHaveBeenCalled();
  });
  it('getEventsByOutcomes with no simpleFilters', () => {
    createPerformRequestSpy();

    const params = { outcomesIds: '1,2', simpleFilters: undefined };
    service.getEventsByOutcomes(params);

    expect(service['performRequest']).toHaveBeenCalled();
  });


  it('getEventsByClasses', () => {
    createPerformRequestSpy();

    const params = { classIds: '1,2', simpleFilters: 'type=HD' },
    childCount = false;

    service.getEventsByClasses(params, childCount);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/EventToOutcomeForClass/${params.classIds}?${params.simpleFilters}`,
      jasmine.any(HttpParams)
    );
  });

  it('getEventsByClasses with childCount', () => {
    createPerformRequestSpy();

    const params = { classIds: '1,2', simpleFilters: 'type=HD' },
    childCount = true,
    queryParams = new HttpParams()
      .append('prune', 'event')
      .append('prune', 'market')
      .append('childCount', 'event');

    service.getEventsByClasses(params, childCount);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/EventToOutcomeForClass/${params.classIds}?${params.simpleFilters}`, queryParams);
  });

  it('getEventsByEvents', () => {
    createPerformRequestSpy();

    const params = { eventsIds: '1,2', simpleFilters: 'type=HD' };
    service.getEventsByEvents(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/EventToOutcomeForEvent/${params.eventsIds}?${params.simpleFilters}`,
      jasmine.any(HttpParams)
    );
  });

  it('getEventsByEvents with ChildCount ', () => {
    createPerformRequestSpy();

    const params = { eventsIds: '1,2', simpleFilters: 'type=HD' };
    const childCountFlag = true;

    service.getEventsByEvents(params, childCountFlag);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/EventToOutcomeForEvent/${params.eventsIds}?${params.simpleFilters}`,
      jasmine.any(HttpParams)
    );
  });

  it('getEventsByMarkets', () => {
    createPerformRequestSpy();

    const params = { marketIds: [1, 2], simpleFilters: 'type=vip' };
    service.getEventsByMarkets(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/EventToOutcomeForMarket/${params.marketIds}?${params.simpleFilters}`
    );
  });

  it('getEventsByMarkets with marketIdArr param', () => {
    createPerformRequestSpy();

    const params = { marketIdArr: ['1', '2'], simpleFilters: 'type=vip' } as any;
    service.getEventsByMarkets(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/EventToOutcomeForMarket/${params.marketIdArr}?${params.simpleFilters}`
    );
  });

  it('getEventsByMarkets with empty params', () => {
    createPerformRequestSpy();

    const params = {} as any;
    service.getEventsByMarkets(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/EventToOutcomeForMarket/?`
    );
  });

  it('getEventsList', () => {
    createPerformRequestSpy();

    const params = { simpleFilters: 'page=1' };
    service.getEventsList(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/Event/?${params.simpleFilters}`
    );
  });

  it('getNextEventsByType', () => {
    createPerformRequestSpy();

    const params = { count: '10', typeId: '1', simpleFilters: 'enabled=1' };
    service.getNextEventsByType(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/NextNEventToOutcomeForType/${params.count}/${params.typeId}?${params.simpleFilters}`
    );
  });

  it('getNextNEventToOutcomeForClass', () => {
    createPerformRequestSpy();

    let params = { classIds: '1', simpleFilters: 'enabled=1', siteServerEventsCount: 3 };
    service.getNextNEventToOutcomeForClass(params);
    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/NextNEventToOutcomeForClass/${params.siteServerEventsCount}/${params.classIds}?${params.simpleFilters}`,
      jasmine.any(HttpParams)
    );

    params = { classIds: '1', simpleFilters: '', siteServerEventsCount: 3 };
    service.getNextNEventToOutcomeForClass(params);
    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/NextNEventToOutcomeForClass/${params.siteServerEventsCount}/${params.classIds}?`,
      jasmine.any(HttpParams)
    );
  });

  it('getRacingResultsForEvent', () => {
    createPerformRequestSpy();

    const params = { eventsIds: '1,2' };
    service.getRacingResultsForEvent(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSHistoricEndpoint']}/RacingResultsForEvent/${params.eventsIds}`
    );
  });

  it('getEventToLinkedOutcomeForEvent', () => {
    createPerformRequestSpy();

    service.getEventToLinkedOutcomeForEvent(1, 'priceHistory=true');

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/EventToLinkedOutcomeForEvent/1?priceHistory=true`
    );
  });

  it('getResultedEventByEvents', () => {
    createPerformRequestSpy();

    const params = { eventsIds: '1,2', simpleFilters: '' };
    service.getResultedEventByEvents(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSHistoricEndpoint']}/ResultedEvent/${params.eventsIds}?${params.simpleFilters}`
    );
  });

  it('getCommentsByEventsIds', () => {
    createPerformRequestSpy();

    const params = { eventsIds: '1,2' };
    service.getCommentsByEventsIds(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSCommentaryEndpoint']}/CommentaryForEvent/${params.eventsIds}`,
      jasmine.any(HttpParams)
    );
  });

  it('getCategories', () => {
    createPerformRequestSpy();

    const params = { categoriesIds: '1,2' };
    service.getCategories(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/Category/${params.categoriesIds}`
    );
  });

  it('getClasses', () => {
    createPerformRequestSpy();

    const params = { classIds: '1,2' };
    service.getClasses(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/Class/${params.classIds}`
    );
  });

  describe('getClassesByCategory', () => {
    it('shoud get data', () => {
      createPerformRequestSpy();

      const params = { categoryId: '1', siteChannels: 'N,B,A', hasOpenEvent: 'Y' };
      service.getClassesByCategory(params);

      expect(service['performRequest']).toHaveBeenCalledWith(
        `${service['SSEndpoint']}/Class`, jasmine.any(HttpParams)
      );
    });

    it('shoud get data from cache', () => {
      createPerformRequestSpy();

      const params = { categoryId: '19', siteChannels: 'N,B,A', hasOpenEvent: 'Y' };
      service.getClassesByCategory(params);

      expect(service['performRequest']).toHaveBeenCalledWith(
        `${service['SSEndpoint']}/Class`, jasmine.any(HttpParams)
      );
    });
  });

  it('getClassToSubTypeForClass', () => {
    createPerformRequestSpy();

    const params = { classIds: '1,2', simpleFilter: 'name=test' };
    service.getClassToSubTypeForClass(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/ClassToSubTypeForClass/${params.classIds}`,
      jasmine.any(HttpParams)
    );
  });

  it('getClassToSubTypeForType', () => {
    createPerformRequestSpy();

    const params = { typeIds: '1,2' };
    service.getClassToSubTypeForType(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/ClassToSubTypeForType/${params.typeIds}`
    );
  });

  it('getMarketsCountByClasses', () => {
    createPerformRequestSpy();

    const params = { classIds: '1,2', simpleFilters: 'x=1' };
    service.getMarketsCountByClasses(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/EventToMarketForClass/${params.classIds}?${params.simpleFilters}`,
      jasmine.any(HttpParams)
    );
  });

  describe('getEventToMarketForClass', () => {
    it('with filters', () => {
      createPerformRequestSpy();

      const params = {classIds: '1,2', simpleFilters: 'x=1'};
      service.getEventToMarketForClass(params);

      expect(service['performRequest']).toHaveBeenCalledWith(
        `${service['SSEndpoint']}/EventToMarketForClass/${params.classIds}?${params.simpleFilters}`
      );
    });

    it('without filters', () => {
      createPerformRequestSpy();
      const params = { classIds: '1,2' };

      service.getEventToMarketForClass(params);
      expect(service['performRequest']).toHaveBeenCalledWith(
        `${service['SSEndpoint']}/EventToMarketForClass/1,2?`
      );
    });
  });

  describe('getEventForClass', () => {
    it('it should call getEventForClass with params', () => {
      createPerformRequestSpy();

      const params = { classIds: '1,2', simpleFilters: 'x=1' };
      service.getEventForClass(params);

      expect(service['performRequest']).toHaveBeenCalledWith(
        `${service['SSEndpoint']}/EventForClass/${params.classIds}?${params.simpleFilters}`
      );
    });

    it('it should call getEventForClass without filters', () => {
      createPerformRequestSpy();

      const params = { classIds: '1,2' };
      service.getEventForClass(params);

      expect(service['performRequest']).toHaveBeenCalledWith(
        `${service['SSEndpoint']}/EventForClass/${params.classIds}?`
      );
    });
  });

  it('getMarketsCountByEventsIds', () => {
    createPerformRequestSpy();

    const params = { eventsIds: '1,2', simpleFilters: 'x=1' };
    service.getMarketsCountByEventsIds(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/EventToMarketForEvent/${params.eventsIds}?${params.simpleFilters}`,
      jasmine.any(HttpParams)
    );
  });

  it('getEventToMarketForEvent with empty simple filter', () => {
    createPerformRequestSpy();
    const params = { eventsIds: '1,2', simpleFilters: '' };
    service.getEventToMarketForEvent(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/EventToMarketForEvent/${params.eventsIds}`);    
  });

  it('getEventToMarketForEvent', ()=>{
    createPerformRequestSpy();
    const params = { eventsIds: '1,2', simpleFilters: 'scorecast:false' };
    service.getEventToMarketForEvent(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/EventToMarketForEvent/${params.eventsIds}?${params.simpleFilters}`
    );
  })

  it('getSportToCollection', () => {
    createPerformRequestSpy();

    const params = { simpleFilters: 'x=3' };
    service.getSportToCollection(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/SportToCollection?${params.simpleFilters}`
    );
  });

  it('getJackpotPools', () => {
    createPerformRequestSpy();

    service.getJackpotPools();

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/Pool`, jasmine.any(HttpParams)
    );
  });

  it('getPoolToPoolValue', () => {
    createPerformRequestSpy();

    const params = { poolsIds: '1,2', simpleFilters: 'y=2' };
    service.getPoolToPoolValue(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/PoolToPoolValue/${params.poolsIds}?${params.simpleFilters}`
    );
  });

  it('getPoolForEvent', () => {
    createPerformRequestSpy();

    const params = { eventsIds: '1,2', simpleFilters: 'z=2' };
    service.getPoolForEvent(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/PoolForEvent/${params.eventsIds}?${params.simpleFilters}`
    );
  });

  it('getPoolForClass', () => {
    createPerformRequestSpy();

    const params = { classIds: '1,2', simpleFilters: 'z=2' };
    service.getPoolForClass(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/PoolForClass/${params.classIds}?${params.simpleFilters}`
    );
  });

  it('getPool', () => {
    createPerformRequestSpy();

    const params = { poolsIds: '1,2', simpleFilters: 'z=2' };
    service.getPool(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/Pool/${params.poolsIds}?${params.simpleFilters}`
    );
  });

  it('getEventsByType', () => {
    createPerformRequestSpy();

    const params = { typeId: '1' };
    service.getEventsByType(params);

    expect(service['performRequest']).toHaveBeenCalledWith(
      `${service['SSEndpoint']}/EventForType/${params.typeId}`
    );
  });

  describe('performRequest', () => {
    it('should make successful request with params', () => {
      const url = 'https://google.com/search';
      const params = { q: 'test' };

      service['http'].get = jasmine.createSpy().and.returnValue(of({}));

      service['performRequest'](url, params);

      expect(http.get).toHaveBeenCalledWith(url, {
        observe: 'response',
        params: params,
        headers: { accept: 'application/json' }
      });
    });

    it('should re-throw Error to upper observables and/or promises', done => {
      const url = 'https://google.com/search';
      const params = { q: 'test' };

      service['http'].get = jasmine.createSpy().and.returnValue(throwError('some message'));

      service['performRequest'](url, params)
      // @ts-ignore
        .subscribe(() => {}, (err) => {
          expect(err).toEqual('some message');
          done();
        });
    });

    it('should re-throw Error to upper observables and/or promises on TimeOut', fakeAsync(() => {
      const url = 'https://google.com/search';
      const params = { q: 'test' };
      let isTimeoutError = false;

      service['http'].get = jasmine.createSpy('get').and.returnValue(new Observable());

      service['performRequest'](url, params)
        .subscribe(() => {}, (err) => {
          isTimeoutError = err.toString().includes('TimeoutError: Timeout has occurred');
        });

      tick(60000);

      expect(isTimeoutError).toBeTruthy();
    }));
  });
});
