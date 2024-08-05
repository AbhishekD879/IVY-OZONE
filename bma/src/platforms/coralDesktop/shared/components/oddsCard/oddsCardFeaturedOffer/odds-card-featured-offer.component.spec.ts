import {
  OddsCardFeaturedOfferComponent
} from '@coralDesktop/shared/components/oddsCard/oddsCardFeaturedOffer/odds-card-featured-offer.component';
import { IOutputModule } from '@featured/models/output-module.model';
import { ISportEvent } from '@core/models/sport-event.model';

describe('OddsCardFeaturedOfferComponent', () => {
  let component: OddsCardFeaturedOfferComponent;

  let sportEventHelperService, templateService, smartBoostsService, timeService, routingHelperService, router;

  let today;
  let future;
  const testStr = 'TestString';
  const wasPriceStub = 'TestWasPrice';

  function fakeCall(time) {
    const formatted = new Date(time);
    /* eslint-disable */
    return time === today ? `${formatted.getHours()}:${today.getMinutes()}, Today` :
      `${formatted.getHours()}:${formatted.getMinutes()} ${future.toLocaleString('en-US', { day: '2-digit' })} ${formatted.toLocaleString('en-US', { month: 'short' })}`;
    /* eslint-enable */
  }

  beforeEach(() => {
    today = new Date();
    future = new Date();
    future.setDate(future.getDate() + 1);
    timeService = {
      getEventTime: jasmine.createSpy().and.callFake(fakeCall)
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('/event/12345')
    };
    router = {
      navigateByUrl: jasmine.createSpy()
    };
    smartBoostsService = {
      isSmartBoosts: jasmine.createSpy().and.returnValue(true),
      parseName: jasmine.createSpy().and.returnValue({ name: testStr, wasPrice: wasPriceStub })
    };

    sportEventHelperService = jasmine.createSpyObj(['sportEventHelperService', 'isSpecialEvent', 'isFootball']);

    templateService = jasmine.createSpyObj(['isMultiplesEvent', 'getEventCorectedDays']);
    component = new OddsCardFeaturedOfferComponent(sportEventHelperService, routingHelperService, router,
      templateService, timeService, smartBoostsService);

    component.event = {
      name: 'test',
      markets: [{
        outcomes: [{

        }]
      }]
    } as any;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      component.isOutright = false;
      component.isStream = false;
      component.featuredModule = { isEnhanced: false } as IOutputModule;
      component.event = { markets: [{ outcomes: [{ name: '' }] }], name: '' } as ISportEvent;
    });

    it('should check correct today event startTime format', () => {
      component.event = {
        startTime: today,
        markets: [{
          outcomes: [{
            prices: [
              {
                priceType: 'price type',
                id: '01'
              }
            ],
            id: '1'
          }]
        }] } as any;
      const formatted = `${today.getHours()}:${today.getMinutes()}, Today`;
      component.ngOnInit();

      expect(component.eventTime).toEqual(formatted);
      expect(component.typeTitle).toEqual('special');
      expect(component.outcome).toEqual(component.event.markets[0].outcomes[0]);
      expect(component.className).toContain('special-offer');
    });

    it('should check correct future event startTime format', () => {
      /* eslint-disable */
      const formatted = `${future.getHours()}:${future.getMinutes()} ${future.toLocaleString('en-US', { day: '2-digit' })} ${future.toLocaleString('en-US', { month: 'short' })}`;
      /* eslint-enable */

      component.event = {
        startTime: future,
        markets: [{
          outcomes: [{
            prices: [
              {
                priceType: 'price type',
                id: '01'
              }
            ],
            id: '1'
          }]
        }] } as any;
      component.ngOnInit();

      expect(component.eventTime).toEqual(formatted);
      expect(component.typeTitle).toEqual('special');
      expect(component.outcome).toEqual(component.event.markets[0].outcomes[0]);
      expect(component.className).toContain('special-offer');
    });

    it(`should set 'isSmartBoosts' property`, () => {
      component.ngOnInit();

      expect(component.isSmartBoosts).toBeTruthy();
    });

    it(`should set parsed eventName if market is SmartBoosts`, () => {
      component.ngOnInit();

      expect(component.eventName).toEqual(testStr);
    });

    it(`should set 'wasPrice' if market is SmartBoosts`, () => {
      component.ngOnInit();

      expect(component.wasPrice).toEqual(wasPriceStub);
    });

    it(`should add 'smart-boosts' class to 'className' if market is SmartBoosts`, () => {
      component.ngOnInit();

      expect(component.className).toContain('smart-boosts');
    });

    it(`should set Not parsed eventName if market is Not SmartBoosts`, () => {
      component['smartBoostsService'].isSmartBoosts = jasmine.createSpy().and.returnValue(false);

      component.ngOnInit();

      expect(component.eventName).toEqual('');
    });

    it(`should Not set 'wasPrice' if market is Not SmartBoosts`, () => {
      component['smartBoostsService'].isSmartBoosts = jasmine.createSpy().and.returnValue(false);

      component.ngOnInit();

      expect(component.wasPrice).toBeUndefined();
    });

    it(`should Not add 'smart-boosts' class to 'className' if market is Not SmartBoosts`, () => {
      component['smartBoostsService'].isSmartBoosts = jasmine.createSpy().and.returnValue(false);

      component.ngOnInit();

      expect(component.className).not.toContain('smart-boosts');
    });
  });

  describe('goToEvent', () => {
    it('should not navigate to edp (multiple event)', () => {
      component['isMultipleEvent'] = true;
      component.goToEvent();
      expect(router.navigateByUrl).not.toHaveBeenCalled();
    });

    it('should not navigate to edp (event finished)', () => {
      component.event.isFinished = true;
      component.goToEvent();
      expect(router.navigateByUrl).not.toHaveBeenCalled();
    });

    it('should navigate to edp', () => {
      component.event.isFinished = false;
      component['isMultipleEvent'] = false;
      component.goToEvent();
      expect(router.navigateByUrl).toHaveBeenCalledWith('/event/12345');
    });
  });
});
