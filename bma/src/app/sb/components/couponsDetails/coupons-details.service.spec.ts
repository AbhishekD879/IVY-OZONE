import { fakeAsync } from '@angular/core/testing';
import { of } from 'rxjs';
import { CouponsDetailsService } from '@sb/components/couponsDetails/coupons-details.service';
import { FOOTBALL_COUPONS } from '@sb/components/couponsDetails/coupons-details.constant';

describe('CouponsDetailsService', () => {
  let service: CouponsDetailsService;
  let gtmService;
  let siteServerService;
  let footballService;
  let timeService;
  let betFilterParamsService;
  let cmsService;
  let cacheEventsService;
  let coupons;
  let windowRef;

  const marketOptionsMock = [
    {
    title: 'Match Result',
    templateMarketName: 'Match Betting',
    header: ['Home', 'Draw', 'Away'],
    },
    {
      title: 'Both Teams to Score',
      templateMarketName: 'Both Teams to Score',
      header: ['Yes', 'No'],
    },
    {
      title: 'Total Goals Over/Under 1.5',
      templateMarketName: 'Total Goals Over/Under 1.5',
      header: ['Over', 'Under'],
    }
  ];

  const availableMarkets = [
    'Both Teams to Score',
    'Total Goals Over/Under 1.5',
    'Total Goals Over/Under 2.5',
    'Total Goals Over/Under 3.5',
    'To Win and Both Teams to Score',
    'Draw No Bet',
    'First-Half Result',
    'To Win To Nil',
    'Score Goal in Both Halves'
  ];

  const couponEvents = [{
    typeId: 971,
    events: [{
      markets: [{
        templateMarketName: 'Match Betting'
      }]
    }, {
      markets: [{
        templateMarketName: 'Total Goals Over/Under',
        rawHandicapValue: '1.5'
      }]
    }],
    groupedByDate: [{
      events: [{
        markets: [{
          templateMarketName: 'Match Betting'
        }]
      }, {
        markets: [{
          templateMarketName: 'Total Goals Over/Under',
          rawHandicapValue: '1.5'
        }]
      }]
    }]
  }] as any;

  beforeEach(() => {
    gtmService = {
      push: jasmine.createSpy('push')
    };

    siteServerService = {
      getEventsByEventsIds: jasmine.createSpy('getEventsByEventsIds')
    };

    footballService = {
      arrangeEventsBySection: jasmine.createSpy('arrangeEventsBySection').and.returnValue(couponEvents),
      couponEventsRequestParams: jasmine.createSpy('couponEventsRequestParams').and.returnValue({categoryId : '1'}),
      couponEventsByCouponId: jasmine.createSpy('couponEventsByCouponId')
    };

    timeService = {
      getSuspendAtTime: jasmine.createSpy('getSuspendAtTime')
    };

    betFilterParamsService = {
      betFilterParams: {}
    };

    cacheEventsService = {
      store: jasmine.createSpy('store')
    };

    cmsService = {
      getToggleStatus: jasmine.createSpy('getToggleStatus').and.returnValue(of(false)),
      getSystemConfig: jasmine.createSpy('getSystemConfig'),
      getCouponMarketSelector: jasmine.createSpy('getCouponMarketSelector').and.returnValue(of(marketOptionsMock))
    };

    windowRef = {
      nativeWindow: {
        location: {
          pathname: 'testPath'
        }
      }
    } as any;

    service = new CouponsDetailsService(
      gtmService,
      siteServerService,
      timeService,
      betFilterParamsService,
      cmsService,
      cacheEventsService,
      windowRef
    );

    coupons = [
      { id : 1, markets : [ { id : 1, templateMarketName : 'Match Betting' } ] },
      { id : 2, markets : [ { id : 2, templateMarketName : 'To Win To Nil' } ] }
    ] as any;
  });

  it('constructor', () => {
    service = new CouponsDetailsService(
      gtmService,
      siteServerService,
      timeService,
      betFilterParamsService,
      cmsService,
      cacheEventsService,
      windowRef
    );

    expect(service.footballCoupons).toEqual(FOOTBALL_COUPONS);
    expect(service['defaultFootballCouponsMarkets']).toEqual(FOOTBALL_COUPONS.DEFAULT_MARKETS);
  });

  describe('@isCustomCoupon', () => {
    it('should check if coupon is custom: default = false', () => {
      expect(service.isCustomCoupon).toBe(false);
    });

    it('isCustomCoupon should check if coupon is custom: Correct Score Coupon = false', () => {
      const events = [{
        markets: {
          dispSortName: 'MR'
        }
      }] as any;
      service.isCorrectScoreCoupon = service['isCorrectScoreMarkets'](events);
      expect(service.isCustomCoupon).toBe(false);
    });

    it('should check if coupon is custom: Correct Score Coupon = false', () => {
      const events = [{
        markets: {
          dispSortName: 'MR'
        }
      }, {
        markets: {
          dispSortName: 'CS'
        }
      }] as any;
      service.isCorrectScoreCoupon = service['isCorrectScoreMarkets'](events);
      expect(service.isCustomCoupon).toBe(false);
    });

    it('should check if coupon is custom: Goalscorer Coupon = true', () => {
      service.isGoalscorerCoupon = true;
      expect(service.isCustomCoupon).toBe(true);
    });

    it('should check if coupon is custom: Correct Score Coupon = true', () => {
      const events = [{
        markets: {
          dispSortName: 'CS'
        }
      }] as any;
      service.isCorrectScoreCoupon = service['isCorrectScoreMarkets'](events);
      expect(service.isCustomCoupon).toBe(true);
    });
  });

  describe('@isQuickBetBlocked', () => {
    it('should check if isQuickBetBlocked=false', fakeAsync(() => {
      cmsService.getSystemConfig.and.returnValue(of({
        quickBet: {
          blockOnCouponDetailsPage: false
        }
      }));
      service.isQuickBetBlocked().subscribe(isQuickBetBlocked => {
        expect(isQuickBetBlocked).toEqual(false);
      });
    }));

    it('should check if isQuickBetBlocked=true', fakeAsync(() => {
      cmsService.getSystemConfig.and.returnValue(of({
        quickBet: {
          blockOnCouponDetailsPage: true
        }
      }));
      service.isQuickBetBlocked().subscribe(isQuickBetBlocked => {
        expect(isQuickBetBlocked).toEqual(true);
      });
    }));
  });

  describe('@getCouponEvents', () => {
    let nextSpy, couponEventsByCouponId, eventsByEventsIds;

    beforeEach(() => {
      nextSpy = jasmine.createSpy('nextSpy');
      spyOn(service as any, 'getCMSCouponMarketSelector').and.callThrough();
      spyOn(service as any, 'isCorrectScoreMarkets').and.callThrough();
      spyOn(service as any, 'getMarketOptions').and.callThrough();
    });

    it('should return coupons from footballService call without extra CMS requests for Correct Score coupon', () => {
      couponEventsByCouponId = [{
        typeName: 'Type 1', markets: [{ dispSortName: 'CS', templateMarketName: 'Correct Score' }]
      }];
      footballService.couponEventsByCouponId.and.returnValue(of(couponEventsByCouponId));
      service.getCouponEvents('10', 'UK Coupon', footballService).subscribe(nextSpy);
      expect((service as any).isCorrectScoreMarkets).toHaveBeenCalledWith(couponEventsByCouponId);
      expect((service as any).isCorrectScoreCoupon).toEqual(true);
      expect((service as any).getCMSCouponMarketSelector).not.toHaveBeenCalled();
      expect(cmsService.getCouponMarketSelector).not.toHaveBeenCalled();
      expect(cmsService.getToggleStatus).not.toHaveBeenCalled();
      expect(siteServerService.getEventsByEventsIds).not.toHaveBeenCalled();
      expect(nextSpy).toHaveBeenCalledWith({ coupons: couponEventsByCouponId, options: [] });
    });

    describe('should get coupon MarketSelector and FootballCoupons settings from CMS', () => {
      beforeEach(() => {
        couponEventsByCouponId = [{ id: '1', markets: [{ templateMarketName: 'Match Betting' }] }];
        footballService.couponEventsByCouponId.and.returnValue(of(couponEventsByCouponId));
      });
      it('and return coupons from preceding footballService call if FootballCoupons CMS toggle is false', () => {
        cmsService.getToggleStatus.and.returnValue(of(false));
        service.getCouponEvents('10', 'UK Coupon', footballService).subscribe(nextSpy);
        expect(nextSpy).toHaveBeenCalledWith({
          coupons: couponEventsByCouponId,
          options: [{ title: 'Match Result', templateMarketName: 'Match Betting', header: [ 'Home', 'Draw', 'Away' ] }]
        });
      });

      describe('and return coupons from preceding footballService call if FootballCoupons CMS toggle is true', () => {
        let events;

        beforeEach(() => {
          eventsByEventsIds = [{ id: '2', markets: [{ templateMarketName: 'Draw No Bet' }] }];
          cmsService.getToggleStatus.and.returnValue(of(true));
          timeService.getSuspendAtTime.and.returnValue('2020-12-31T23:59:60Z');
        });
        it('with events present in SS response', () => {
          events = eventsByEventsIds.concat(couponEventsByCouponId);
          siteServerService.getEventsByEventsIds.and.returnValue(of(eventsByEventsIds));
          service.getCouponEvents('10', 'UK Coupon', footballService).subscribe(nextSpy);
          expect(nextSpy).toHaveBeenCalledWith({
            coupons: events,
            options: [
              { title: 'Match Result', templateMarketName: 'Match Betting', header: [ 'Home', 'Draw', 'Away' ] },
              { title: 'Draw No Bet', templateMarketName: 'Draw No Bet', header: [ 'Home', 'Away' ] }
            ]
          });
        });

        it('and return coupons from preceding footballService call if FootballCoupons CMS toggle is true (no events from SS)', () => {
          events = couponEventsByCouponId;
          siteServerService.getEventsByEventsIds.and.returnValue(of(null));
          service.getCouponEvents('10', 'UK Coupon', footballService).subscribe(nextSpy);
          expect(nextSpy).toHaveBeenCalledWith({
            coupons: events,
            options: [{ title: 'Match Result', templateMarketName: 'Match Betting', header: [ 'Home', 'Draw', 'Away' ] }]
          });
        });
        afterEach(() => {
          expect((service as any).getMarketOptions).toHaveBeenCalledWith(
            [{ title: 'Match Result', templateMarketName: 'Match Betting', header: [ 'Home', 'Draw', 'Away' ] }],
            marketOptionsMock, events);
          expect(cacheEventsService.store).toHaveBeenCalledWith('coupons', '10', events);
          expect(siteServerService.getEventsByEventsIds).toHaveBeenCalledWith({
            eventsIds: ['1'],
            isStarted: false,
            marketsCount: false,
            childCount: true,
            suspendAtTime: '2020-12-31T23:59:60Z',
            templateMarketNameOnlyIntersects: true
          });
        });
      });

      afterEach(() => {
        expect((service as any).getMarketOptions).toHaveBeenCalledWith([], marketOptionsMock, couponEventsByCouponId);
        expect(cmsService.getCouponMarketSelector).toHaveBeenCalled();
        expect(cmsService.getToggleStatus).toHaveBeenCalledWith('FootballCoupons');
      });
    });

    afterEach(() => {
      expect(service.sportId).toEqual('1');
      expect(footballService.couponEventsByCouponId).toHaveBeenCalledWith({ couponId: '10', categoryId: '1' });
      expect(footballService.couponEventsRequestParams).toHaveBeenCalledWith('10');
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'Coupon Selector',
        eventAction: 'Select Coupon',
        eventLabel: 'UK Coupon'
      });
    });
  });

  describe('@isBetFilterEnable', () => {
    it('should check if bet filter is enable: couponSortCode is NOT "MR"', fakeAsync(() => {
      const coupon = {
        name: 'HH Coupon',
        couponSortCode: 'HH'
      } as any;
      service.isBetFilterEnable(coupon).subscribe((isEnable) => {
        expect(isEnable).toBe(false);
      });
    }));

    it('should check if bet filter is enable: CMS config is enable', fakeAsync(() => {
      cmsService.getSystemConfig.and.returnValue(of({
        Connect: {
          footballFilter: true
        }
      }));
      const coupon = {
        name: 'Main Coupon',
        couponSortCode: 'MR'
      } as any;
      service.isBetFilterEnable(coupon).subscribe((isEnable) => {
        expect(betFilterParamsService.betFilterParams).toEqual({
          couponName: 'Main Coupon',
          mode: 'online',
          pathname: windowRef.nativeWindow.location.pathname
        });
        expect(isEnable).toBe(true);
      });
    }));

    it('should check if bet filter is enable: CMS config is disable', fakeAsync(() => {
      cmsService.getSystemConfig.and.returnValue(of({}));
      const coupon = {
        name: 'Main Coupon',
        couponSortCode: 'MR'
      } as any;
      service.isBetFilterEnable(coupon).subscribe((isEnable) => {
        expect(betFilterParamsService.betFilterParams).toEqual({
          couponName: 'Main Coupon',
          mode: 'online',
          pathname: windowRef.nativeWindow.location.pathname
        });
        expect(isEnable).toBe(undefined);
      });
    }));
  });

  it('@pushToGTM', () => {
    service['pushToGTM']('goalscorer coupon');

    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
      eventCategory: 'Coupon Selector',
      eventAction: 'Select Coupon',
      eventLabel: 'Goalscorer Coupon'
    });
  });

  describe('@setOddsHeader', () => {
    it('should set correct odds card header', () => {
      const result = service.setOddsHeader(marketOptionsMock, 'Both teams to score');
      expect(result).toEqual(['Yes', 'No']);
    });

    it('should NOT set odds card header if it is not exist', () => {
      const result = service.setOddsHeader(marketOptionsMock, 'To Win To Nil');
      expect(result).toEqual([]);
    });

    it('should NOT set odds card header if options are not exist', () => {
      const result = service.setOddsHeader([], 'Both teams to score');
      expect(result).toEqual([]);
    });
  });

  describe('@groupCouponEvents', () => {
    it('should return grouped coupons events', () => {
      const events = [{
        typeName: 'Type 1',
        classDisplayOrder: 2,
        typeDisplayOrder: 2,
        markets: [{
          templateMarketName: 'Match Betting'
        }]
      }, {
        typeName: 'Type 2',
        classDisplayOrder: 1,
        typeDisplayOrder: 1,
        markets: [{
          templateMarketName: 'Correct Score'
        }]
      }] as any;

      const result = service.groupCouponEvents(events, footballService);
      expect(footballService.arrangeEventsBySection).toHaveBeenCalled();
      expect(result).toEqual(couponEvents);
    });
  });

  // PRIVATE METHODS

  describe('@filteredArr', () => {
    it('should filter event with same property', () => {
      const array = [{ id: '1'}, { id: '1'}, { id: '2'}, { id: '2'}, { id: '3'}] as any;
      const result = service['filteredArr'](array, 'id');

      expect(result).toEqual([{ id: '1'}, { id: '2'}, { id: '3'}] as any);
    });

    it('should filter event with same property if array is empty', () => {
      const result = service['filteredArr'](undefined, 'id');

      expect(result).toEqual([] as any);
    });

    it('should filter markets with same property', () => {
      const array = [
        { id: '1', markets: [{ id: '1'}, { id: '3'}]},
        { id: '1', markets: [{ id: '1'}, { id: '2'}]},
        { id: '2', markets: [{ id: '3'}, { id: '4'}]},
        { id: '2', markets: [{ id: '4'}, { id: '6'}]},
        { id: '3'}] as any;
      const result = service['filteredArr'](array, 'id', 'markets');

      expect(result).toEqual([
        { id: '1', markets: [{ id: '1'}, { id: '2'}, { id: '3'}]},
        { id: '2', markets: [{ id: '4'}, { id: '6'}, { id: '3'}]},
        { id: '3'}] as any);
    });

  });

  describe('@getMarketOptions', () => {
    it('should return a list of Available Markets', () => {
      const result = service['getMarketOptions']([], marketOptionsMock, coupons);

      expect(result).toEqual([{
        title: 'Match Result',
        templateMarketName: 'Match Betting',
        header: ['Home', 'Draw', 'Away'],
      }, {
        title: 'To Win To Nil',
        templateMarketName: 'To Win to Nil',
        header: [ 'Home', 'Away' ]
      }]);
    });

    it('should return a list of Available Markets if options is empty', () => {
      const result = service['getMarketOptions'](undefined, marketOptionsMock, coupons);

      expect(result).toEqual([{
        title: 'Match Result',
        templateMarketName: 'Match Betting',
        header: ['Home', 'Draw', 'Away'],
      }, {
        title: 'To Win To Nil',
        templateMarketName: 'To Win to Nil',
        header: [ 'Home', 'Away' ]
      }]);
    });

    it('should return a list of Available Markets if cmsOptions is empty', () => {
      const result = service['getMarketOptions'](marketOptionsMock, undefined, coupons);

      expect(result).toEqual([{
        title: 'Match Result',
        templateMarketName: 'Match Betting',
        header: ['Home', 'Draw', 'Away'],
      }, {
        title: 'To Win To Nil',
        templateMarketName: 'To Win to Nil',
        header: [ 'Home', 'Away' ]
      }]);
    });
  });

  describe('@modifyTemplateName', () => {
    it('should modify templateMarketName if rawHandicapValue is exist', () => {
      const couponsEvents = [{
        markets: [{
          rawHandicapValue: '1',
          templateMarketName: 'Over/Under'
        }]
      }] as any;
      service['modifyTemplateName'](couponsEvents);
      expect(couponsEvents[0].markets[0].templateMarketName).toEqual('Over/Under 1');
    });

    it('should not modify templateMarketName if rawHandicapValue is not exist', () => {
      const couponsEvents = [{
        markets: [{
          templateMarketName: 'Match Betting'
        }]
      }] as any;
      service['modifyTemplateName'](couponsEvents);
      expect(couponsEvents[0].markets[0].templateMarketName).toEqual('Match Betting');
    });

    it('should not modify templateMarketName if rawHandicapValue is exist in templateMarketName', () => {
      const couponsEvents = [{
        markets: [{
          rawHandicapValue: '1.5',
          templateMarketName: 'Over/Under 1.5'
        }]
      }] as any;
      service['modifyTemplateName'](couponsEvents);
      expect(couponsEvents[0].markets[0].templateMarketName).toEqual('Over/Under 1.5');
    });
  });

  describe('@getOpenBetMarketNames', () => {
    it('should return a list of strings', () => {
      const result = service['getOpenBetMarketNames'](coupons);

      expect(result).toEqual(['match betting', 'to win to nil']);
    });
  });

  describe('@filterDefaultOptions', () => {
    it('should return a list of market options', () => {
      const openBetMarkets = service['getOpenBetMarketNames'](coupons);
      const result = service['filterDefaultOptions'](openBetMarkets, availableMarkets);

      expect(result).toEqual([
        {
          title: 'Match Result',
          templateMarketName: 'Match Betting',
          header: ['Home', 'Draw', 'Away'],
        }
      ]);
    });
  });
});
