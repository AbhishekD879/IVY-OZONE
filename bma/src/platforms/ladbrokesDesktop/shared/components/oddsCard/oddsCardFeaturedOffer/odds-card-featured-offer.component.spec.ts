import {
  OddsCardFeaturedOfferComponent
} from './odds-card-featured-offer.component';

describe('OddsCardFeaturedOfferComponent', () => {
  let component: OddsCardFeaturedOfferComponent;
  let sportEventHelperService;
  let routingHelperService;
  let router;
  let templateService;
  let smartBoostsService;
  let timeService;

  beforeEach(() => {
    smartBoostsService = {
      isSmartBoosts: jasmine.createSpy('isSmartBoosts'),
      parseName: jasmine.createSpy('parseName').and.returnValue({})
    };
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('/event/12345')
    };
    sportEventHelperService = jasmine.createSpyObj(['sportEventHelperService', 'isSpecialEvent', 'isFootball']);
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    templateService = jasmine.createSpyObj(['isMultiplesEvent', 'getEventCorectedDays']);
    timeService = jasmine.createSpyObj(['getEventTime']);
    component = new OddsCardFeaturedOfferComponent(
      sportEventHelperService,
      routingHelperService,
      router,
      templateService,
      smartBoostsService,
      timeService
    );
    component.featuredModule = {} as any;
    component.event = {
      name: 'test',
      markets: [{
        outcomes: [{

        }]
      }]
    } as any;
  });

  describe('ngOnInit', () => {
    it('enhanced with smart boost', () => {
      smartBoostsService.isSmartBoosts.and.returnValue(true);
      component.featuredModule.isEnhanced = true;

      component.ngOnInit();

      expect(component.typeTitle).toBe('enhanced');
      expect(component.className).toBe('enhanced-offer smart-boosts');
      expect(timeService.getEventTime).toHaveBeenCalled();
    });

    it('special with multiple event', () => {
      component.featuredModule.isEnhanced = false;
      templateService.isMultiplesEvent.and.returnValue(true);

      component.ngOnInit();

      expect(component.className).toBe('special-offer');
      expect(component.typeTitle).toBe('special');
      expect(component.multipleClassName).toBe('featured-no-pointer');
    });

    it('favorite shown', () => {
      sportEventHelperService.isFootball.and.returnValue(true);
      sportEventHelperService.isSpecialEvent.and.returnValue(false);
      component.isOutright = false;
      component['isMultipleEvent'] = false;

      component.ngOnInit();

      expect(component.isFavoriteShown).toBeTruthy();
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
