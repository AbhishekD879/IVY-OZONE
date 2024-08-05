import { GoalscorerCouponComponent } from '@sb/components/goalscorerCoupon/goalscorer-coupon.component';
import { ISportEvent } from '@core/models/sport-event.model';

describe('GoalscorerCouponComponent', () => {

  let component: GoalscorerCouponComponent;

  let goalscorerCouponService;
  let timeService;
  let routingHelperService;
  let gtmService;
  let datePipe;
  let router;

  const event = {
    id: 8725938,
    categoryId: '16',
    categoryName: 'Football',
    isActive: false,
    isDelay: false,
    eventStatusCode: 'A',
    startTime: '1552059210588',
    combinedOutcomes: {
      id: '513118312',
      outcomeMeaningScores: '0,1,',
      outcomeStatusCode: 'A',
      name: 'Virtus Entella 1-0',
      prices: [{
        priceDen: 3,
        priceNum: 1
      }]
    },
    name: 'Pontedera v Virtus Entella',
    teams: {
      teamA: {
        name: 'Virtus Entella',
        score: 0,
        scores: [0, 1, 2, 3, 4, 5]
      },
      teamH: {
        name: 'Pontedera',
        score: 0,
        scores: [0, 1, 2, 3, 4]
      }
    },
    markets: [{
      marketStatusCode: 'A',
      outcomes: [{
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
      }]
    }]
  } as any;

  const sportEvent: ISportEvent = {
    id: 1,
    name: 'Sport event',
    goalScorersShowAll: false,
    goalScorersToShow: 5,
    goalScorers: []
  } as any;

  const formDate = (timestamp: number) => {
    const date = new Date(timestamp * 1000),
      hours = date.getHours(),
      minutes = date.getMinutes();

    return `${ hours }:${ minutes < 10 ? '0' : '' }${ minutes }`;
  };

  beforeEach(() => {
    goalscorerCouponService = {
      goalScorersLimit: 5,
      goalScorersToShow: 5,
      formGoalScorers: jasmine.createSpy()
    };

    routingHelperService = {
      formEdpUrl: jasmine.createSpy(),
      formResultedEdpUrl: jasmine.createSpy('formResultedEdpUrl')
    };

    timeService = {
      getLocalHourMinInMilitary: jasmine.createSpy('getLocalHourMinInMilitary').and.callFake((timestamp: number) => {
        return formDate(timestamp);
      })
    };

    gtmService = {
      push: jasmine.createSpy()
    };

    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };

    datePipe = {
      transform: jasmine.createSpy()
    };

    component = new GoalscorerCouponComponent(
      goalscorerCouponService,
      routingHelperService,
      timeService,
      gtmService,
      datePipe,
      router
    );

  });

  describe('@ngOnInit', () => {
    it('should set goalScorersLimit', () => {
      component.ngOnInit();
      expect(component.goalScorersLimit).toEqual(5);
    });
  });

  it('@getStartTime should return start time in HH:mm', () => {
    const startTime = Math.round(new Date().getTime() / 1000);

    expect(component.getStartTime(startTime)).toEqual(formDate(startTime));
  });

  it('@goToEvent should form url from event and navigate to it', () => {
    routingHelperService.formResultedEdpUrl.and.returnValue('edp/url/event');
    component.trackGoToEDP = jasmine.createSpy('trackGoToEDP');

    component.goToEvent({ name: 'event' } as any);
    expect(router.navigateByUrl).toHaveBeenCalledWith('edp/url/event');
    expect(component.trackGoToEDP).toHaveBeenCalledWith('event');
  });

  describe('getEventUrl', () => {
    it('should call formEdpUrl', () => {
      component.getEventUrl(event);
      expect(routingHelperService.formEdpUrl).toHaveBeenCalled();
    });
  });

  it('@trackGoToEDP ', () => {
    component.trackGoToEDP('eventName');

    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
      eventCategory: 'goalscorer coupon',
      eventAction: 'go to event',
      eventLabel: 'eventName'
    });
  });

  describe('getHeaderTime', () => {
    it('should call formEdpUrl', () => {
      component.getHeaderTime(event);
      expect(datePipe.transform).toHaveBeenCalled();
    });
  });

  describe('@isExpandedEvent', () => {
    it('should return true if both goalScorerEventsIndex and couponEventsIndex are 0', () => {
      expect(component.isExpandedEvent(0, 0, 159)).toBeTruthy();
    });

    it('should return false if at least one of goalScorerEventsIndex and couponEventsIndex is greater than 0', () => {
      expect(component.isExpandedEvent(1, 0, 159)).toBeFalsy();
      expect(component.isExpandedEvent(0, 1, 159)).toBeFalsy();
    });

    it('should return true if eventID is same that event id from EDP', () => {
      component.eventIdFromEDP = 159;
      expect(component.isExpandedEvent(0, 1, 159)).toBeTruthy();
    });
  });

  describe('showMoreClick toggle', () => {
    it('should change "goalScorersShowAll" to be true', () => {
      sportEvent.goalScorersShowAll = false;
      component.showMoreClick(sportEvent);

      expect(sportEvent.goalScorersShowAll).toBeTruthy();
    });

    it('should change "goalScorersShowAll" to be false', () => {
      sportEvent.goalScorersShowAll = true;
      component.showMoreClick(sportEvent);

      expect(sportEvent.goalScorersShowAll).toBeFalsy();
    });

    it('should call trackShowAll', () => {
      component.trackShowAll = jasmine.createSpy('trackShowAll');
      component.showMoreClick(sportEvent);

      expect(component.trackShowAll).toHaveBeenCalled();
    });
  });

});
