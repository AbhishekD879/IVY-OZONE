import { GoalscorerCouponService } from '@sb/components/goalscorerCoupon/goalscorer-coupon.service';
import { IGoalscorerCoupon } from '@core/models/goalscorer-coupon.model';

describe('GoalscorerCouponService', () => {
  let service: GoalscorerCouponService;
  let filtersService;

  const couponEvents: IGoalscorerCoupon[] = [{
    id: 123,
    events: [{
      id: 3,
      markets: [{
        templateMarketName: 'First Goalscorer',
        outcomes: [{ prices: [] }]
      }]
    }, {
      id: 5,
      markets: [{
        templateMarketName: 'Last Goalscorer',
        outcomes: [{ prices: [] }]
      }]
    }]
  }, {
    id: 4,
    events: [{
      id: 3,
      markets: [{
        templateMarketName: 'Anytime Goalscorer',
        outcomes: [{ prices: [] }]
      }]
    }]
  }] as any;

  const expectedGoalScores: IGoalscorerCoupon[] = [{
    id: 123,
    events: [{
      id: 3,
      markets: [{
        templateMarketName: 'First Goalscorer',
        outcomes: [{
          prices: [],
          correctedOutcomeMeaningMinorCode: 3,
          marketIndex: 0
        }]
      }],
      goalScorersShowAll: false,
      goalScorersToShow: 5,
      goalScorersHeader: ['1st'],
      goalScorers: undefined
    }, {
      id: 5,
      markets: [{
        templateMarketName: 'Last Goalscorer',
        outcomes: [{
          prices: [],
          correctedOutcomeMeaningMinorCode: 3,
          marketIndex: 0
        }]
      }],
      goalScorersShowAll: false,
      goalScorersToShow: 5,
      goalScorersHeader: ['Last'],
      goalScorers: undefined
    } ],
    isExpanded: true
  }, {
    id: 4,
    events: [{
      id: 3,
      markets: [{
        templateMarketName: 'Anytime Goalscorer',
        outcomes: [{
          prices: [],
          correctedOutcomeMeaningMinorCode: 3,
          marketIndex: 0
        }]
      }],
      goalScorersShowAll: false,
      goalScorersToShow: 5,
      goalScorersHeader: ['Anytime'],
      goalScorers: undefined
    }],
    isExpanded: false
  }] as any;

  beforeEach(() => {
    filtersService = {
      getTeamName: jasmine.createSpy('getTeamName'),
      orderBy: jasmine.createSpy('orderBy')
    };
    service = new GoalscorerCouponService(filtersService);
  });

  describe('formGoalScorers', () => {
    it('should form coupon with event with GoalScorers markets if event selections', () => {
      expect(service.formGoalScorers(couponEvents)).toEqual(expectedGoalScores);
    });

    it('should form coupon with event with GoalScorers markets if event has NO selections', () => {
      const coupons = [{
        id: 4,
        events: [{
          id: 3,
          markets: []
        }]
      }, {
        id: 4,
        events: [{
          id: 3,
          markets: []
        }]
      }] as any;
      expect(service.formGoalScorers(coupons)).toEqual([]);
    });
  });

  describe('goalScorers', () => {
    beforeEach(() => {
      spyOn(service, 'selectionsByName' as any).and.returnValue([]);
    });

    it('should return empty array if no markets were given', () => {
      expect(service['goalScorers']([], {}, 2)).toEqual([]);
      expect(service['selectionsByName']).not.toHaveBeenCalled();
    });

    it('should form goal scores array', () => {
      const markets = [{
        outcomes: [{
          outcomeMeaningMinorCode: 'M',
          name: 'outcome',
          prices: [{
            priceDec: 1.00
          }]
        }]
      }] as any,
      expectedResult = [{
        name: 'outcome',
        priceDec: 1.00,
        teamName: 'M',
        selections: []
      }] as any;

      expect(service['goalScorers'](markets, { M: 'M' }, 1)).toEqual(expectedResult);
      expect(service['selectionsByName']).toHaveBeenCalledWith(markets, 'outcome', 1);
    });
  });
});
