import { CorrectScoreCouponService } from '@sb/components/correctScoreCoupon/correct-score-coupon.service';

describe('CorrectScoreCouponService', () => {

  let service: CorrectScoreCouponService;

  let scoreMarketBaseService;
  let timeService;
  let storageService;

  const couponEvents = [{
    categoryId: '123124',
    typeName: 'Football Type',
    typeId: '234323',
    events: [{
      id: 8725938,
      categoryId: '16',
      categoryName: 'Football',
      eventStatusCode: 'A',
      name: 'Pontedera v Virtus Entella',
      markets: [{
        marketStatusCode: 'A',
        outcomes: [{
          id: '613115314',
          outcomeMeaningScores: '0,0,',
          outcomeStatusCode: 'A',
          name: 'Draw 0-0',
          prices: [{
            priceDen: 2,
            priceNum: 1
          }]
        }, {
          id: '613118314',
          outcomeMeaningScores: '1,0,',
          outcomeStatusCode: 'A',
          name: 'Pontedera 1-0',
          prices: [{
            priceDen: 4,
            priceNum: 1
          }]
        }, {
          id: '513118312',
          outcomeMeaningScores: '0,1,',
          outcomeStatusCode: 'A',
          name: 'Virtus Entella 1-0',
          prices: [{
            priceDen: 3,
            priceNum: 1
          }]
        }, {
          id: '613118324',
          outcomeMeaningScores: '2,0,',
          outcomeStatusCode: 'A',
          name: 'Pontedera 2-0',
          prices: [{
            priceDen: 4,
            priceNum: 2
          }]
        }, {
          id: '513118342',
          outcomeMeaningScores: '0,2,',
          outcomeStatusCode: 'A',
          name: 'Virtus Entella 2-0',
          prices: [{
            priceDen: 2,
            priceNum: 1
          }]
        }]
      }]
    }]
  }] as any;

  const teams = {
    teamA: {
      name: 'Virtus Entella',
      score: 0,
      scores: [0, 1, 2]
    },
    teamH: {
      name: 'Pontedera',
      score: 0,
      scores: [0, 1, 2]
    }
  } as any;

  const outcome = {
    id: '613115314',
    outcomeMeaningScores: '0,0,',
    outcomeStatusCode: 'A',
    name: 'Draw 0-0',
    prices: [{
      priceDen: 2,
      priceNum: 1
    }]
  } as any;

  const getObj = (obj: {}) => {
    return JSON.parse(JSON.stringify(obj));
  };

  describe('RacingSpecialsCarouselService', () => {
    beforeEach(() => {
      scoreMarketBaseService = {
        getMaxScoreValues: jasmine.createSpy().and.returnValue({
          teamA: [0, 1, 2],
          teamH: [0, 1, 2]
        })
      };
      timeService = {
        getEventTime: jasmine.createSpy().and.returnValue('23:00, 15 Nov')
      };
      storageService = {
        get: jasmine.createSpy().and.returnValue([])
      };

      service = new CorrectScoreCouponService(scoreMarketBaseService, timeService, storageService);
    });

    it('createCouponEvents - should create coupon events', () => {
      const coupons = getObj(couponEvents);
      const event = coupons[0].events[0];
      service.createCouponEvents(coupons);
      expect(event.isDelay).toBe(false);
      expect(event.isActive).toBe(false);
      expect(event.teams).toEqual(teams);
      expect(event.combinedOutcomes).toEqual(outcome);
    });

    it('createCouponEvent - should create Default coupon event', () => {
      const coupons = getObj(couponEvents);
      const event = coupons[0].events[0];
      const outcomes = event.markets[0].outcomes;
      service.createCouponEvent(event, outcomes);
      expect(event.teams).toEqual(teams);
      expect(event.combinedOutcomes).toEqual(outcome);
    });

    it('createCouponEvent - should create Active coupon event', () => {
      const coupons = getObj(couponEvents);
      const event = coupons[0].events[0];
      const outcomes = event.markets[0].outcomes;
      storageService.get = jasmine.createSpy().and.returnValue([outcome]);
      service.createCouponEvent(event, outcomes);
      expect(event.isActive).toBe(true);
      expect(event.teams).toEqual(teams);
      expect(event.combinedOutcomes).toEqual(outcome);
    });

    it('getCombinedOutcome - should get combined outcome', () => {
      const coupons = getObj(couponEvents);
      const outcomes = coupons[0].events[0].markets[0].outcomes;
      expect(service.getCombinedOutcome(teams, outcomes)).toEqual(outcome);
    });

    it('getCombinedOutcome - should get outcome with outcomeStatusCode="S"', () => {
      const outcomes = [{ outcomeMeaningScores: '4,6'}] as any;
      expect(service.getCombinedOutcome(teams, outcomes)).toEqual({outcomeStatusCode: 'S'} as any);
    });

    it('getMaxScoreValues - should get score values', () => {
      const coupons = getObj(couponEvents);
      const outcomes = coupons[0].events[0].markets[0].outcomes;
      service['getScoreValues'](outcomes);
      expect(scoreMarketBaseService.getMaxScoreValues).toHaveBeenCalledWith(outcomes);
    });

    it('getTeams - should create team object', () => {
      const coupons = getObj(couponEvents);
      const event = coupons[0].events[0];
      const outcomes = event.markets[0].outcomes;
      expect(service['getTeams']('Pontedera v Virtus Entella', outcomes)).toEqual(teams);
    });

    it('createEvent - should create Default coupon event', () => {
      const coupons = getObj(couponEvents);
      const event = coupons[0].events[0];
      const outcomes = event.markets[0].outcomes;
      service['createEvent'](event, outcomes);
      expect(event.isActive).toBe(false);
      expect(event.teams).toEqual(teams);
      expect(event.combinedOutcomes).toEqual(outcome);
    });

  });
});
