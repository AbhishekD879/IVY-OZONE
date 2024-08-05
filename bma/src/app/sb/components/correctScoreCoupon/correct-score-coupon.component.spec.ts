import { fakeAsync, tick } from '@angular/core/testing';
import { CorrectScoreCouponComponent } from '@sb/components/correctScoreCoupon/correct-score-coupon.component';
import { IOutcome } from '@core/models/outcome.model';

describe('CorrectScoreCouponComponent', () => {

  let component: CorrectScoreCouponComponent;

  let correctScoreCouponService;
  let pubSubService;

  let event;
  let outcome;

  beforeEach(() => {
    event = {
      id: 8725938,
      categoryId: '16',
      categoryName: 'Football',
      isActive: false,
      isDelay: false,
      eventStatusCode: 'A',
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
    outcome = {
      id: '513118312',
      outcomeMeaningScores: '0,1,',
      outcomeStatusCode: 'A',
      name: 'Virtus Entella 1-0',
      prices: [{
        priceDen: 3,
        priceNum: 1
      }]
    } as IOutcome;
    correctScoreCouponService = {
      createCouponEvents: jasmine.createSpy(),
      getCombinedOutcome: jasmine.createSpy().and.returnValue(outcome)
    };
    pubSubService = {
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      API: {
        BETSLIP_SELECTIONS_UPDATE: ''
      }
    };

    component = new CorrectScoreCouponComponent(correctScoreCouponService, pubSubService);
    component.couponEvents = [{
      categoryId: '123124',
      typeName: 'Football Type',
      typeId: '234323',
      events: []
    }] as any;
  });

  it('ngOnInit - should load coupon data', () => {
      component.ngOnInit();
      expect(correctScoreCouponService.createCouponEvents).toHaveBeenCalledWith(component.couponEvents, false);
      expect(pubSubService.subscribe).toHaveBeenCalled();
  });

  it('ngOnDestroy - should unsubscribe', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('CorrectScoreCoupon');
  });

  it('trackById - should track event by index', () => {
    expect(component.trackById(2, {} as any)).toEqual('2');
  });

  it('trackById - should track event by id', () => {
    expect(component.trackById(1, { id: 72124 } as any)).toEqual('172124');
  });

  it('priceDelay - should check if correct priceDelay', () => {
    expect(component['priceDelay']).toEqual(250);
  });

  it('onScoreChange - should change outcome on ScoreChange for Away team', fakeAsync(() => {
    component.onScoreChange(1, 'teamA', event);
    expect(event.isDelay).toEqual(true);
    tick(component['priceDelay']);
    expect(event.isDelay).toEqual(false);
    expect(event.combinedOutcomes).toEqual(outcome);
    expect(event.teams.teamA.score).toEqual(1);
  }));

  it('onScoreChange - should change outcome on ScoreChange for Home team', fakeAsync(() => {
    component.onScoreChange(2, 'teamH', event);
    expect(event.isDelay).toEqual(true);
    tick(component['priceDelay']);
    expect(event.isDelay).toEqual(false);
    expect(event.combinedOutcomes).toEqual(outcome);
    expect(event.teams.teamH.score).toEqual(2);
  }));

  it('onScoreChange - should add +1 to score on ScoreChange for Home team', fakeAsync(() => {
    event.teams.teamH.score = 3;
    component.onScoreChange(1, 'teamH', event, true);
    expect(event.isDelay).toEqual(true);
    tick(component['priceDelay']);
    expect(event.isDelay).toEqual(false);
    expect(event.combinedOutcomes).toEqual(outcome);
    expect(event.teams.teamH.score).toEqual(4); // + 1
  }));

  it('onScoreChange - should add -1 to score on ScoreChange for Away team', fakeAsync(() => {
    event.teams.teamA.score = 3;
    component.onScoreChange(-1, 'teamA', event, true);
    expect(event.isDelay).toEqual(true);
    tick(component['priceDelay']);
    expect(event.isDelay).toEqual(false);
    expect(event.combinedOutcomes).toEqual(outcome);
    expect(event.teams.teamA.score).toEqual(2); // -1
  }));

  it('isDisabled - should set true if score is max', () => {
    event.teams.teamA.score = 5;
    expect(component.isDisabled(event, 'teamA', true)).toEqual(true);
  });

  it('isDisabled - should set true if score is min', () => {
    event.teams.teamA.score = 0;
    expect(component.isDisabled(event, 'teamA', false)).toEqual(true);
  });

  it('isDisabled - should set true if event is Active', () => {
    event.isActive = true;
    expect(component.isDisabled(event, 'teamA', false)).toEqual(true);
  });

  it('isDisabled - should set false if event is not Active', () => {
    event.isActive = false;
    event.teams.teamH.score = 1;
    expect(component.isDisabled(event, 'teamH', true)).toEqual(false);
  });

  it('isDisabled - should set false if score is not min', () => {
    event.teams.teamH.score = 1;
    expect(component.isDisabled(event, 'teamH', false)).toEqual(false);
  });

  it('isDisabled - should set false if score is not max', () => {
    event.teams.teamA.score = 2;
    expect(component.isDisabled(event, 'teamA', true)).toEqual(false);
  });

  it('isHide - should set false if outcome has prices and outcomeStatusCode="A"', () => {
    expect(component.isHide(event)).toEqual(false);
  });

  it('isHide - should set true if outcome outcomeStatusCode="S"', () => {
    event.combinedOutcomes.outcomeStatusCode = 'S';
    expect(component.isHide(event)).toEqual(true);
  });

  it('isHide - should set true if outcome has price with isDisplayed=false', () => {
    event.combinedOutcomes.prices = [{ isDisplayed: false }];
    expect(component.isHide(event)).toEqual(true);
  });

  it('isHide - should set true if outcome without prices', () => {
    event.combinedOutcomes.prices = [];
    expect(component.isHide(event)).toEqual(true);
  });

  it('isSuspended - should set false if event has eventStatusCode="A" and markets has marketStatusCode="A"', () => {
    expect(component.isSuspended(event)).toEqual(false);
  });

  it('isSuspended - should set true if event has eventStatusCode="S"', () => {
    event.eventStatusCode = 'S';
    expect(component.isSuspended(event)).toEqual(true);
  });

  it('isSuspended - should set true if markets has marketStatusCode="S"', () => {
    event.eventStatusCode = 'A';
    event.markets[0].marketStatusCode = 'S';
    expect(component.isSuspended(event)).toEqual(true);
  });

  it('isArrowHide - should set true if event is Active', () => {
    event.isActive = true;
    event.eventStatusCode = 'A';
    event.markets[0].marketStatusCode = 'A';
    expect(component.isArrowHide(event)).toEqual(true);
  });

  it('isArrowHide - should set false if event is not Active', () => {
    event.isActive = false;
    event.eventStatusCode = 'A';
    event.markets[0].marketStatusCode = 'A';
    expect(component.isArrowHide(event)).toEqual(false);
  });

});
