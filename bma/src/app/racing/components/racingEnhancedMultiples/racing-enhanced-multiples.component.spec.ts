import { of } from 'rxjs';

import { RacingEnhancedMultiplesComponent } from './racing-enhanced-multiples.component';
import { BehaviorSubject } from 'rxjs/internal/BehaviorSubject';

describe('RacingEnhancedMultiplesComponent', () => {
  let component;
  let racingEnhancedMultiplesService;
  let gtmService;
  let carouselService;
  let vEPService;

  beforeEach(() => {
    racingEnhancedMultiplesService = {
      getEnhancedMultiplesEvents: jasmine.createSpy('getEnhancedMultiplesEvents').and.returnValue(of({})),
      sortOutcomesByDate: jasmine.createSpy('sortOutcomesByDate').and.returnValue([]),
      setEventDate: jasmine.createSpy('getOutcomesFromEvents')
    };
    gtmService = jasmine.createSpyObj('gtmService', ['push']);
    carouselService = {
      get: jasmine.createSpy('getCarousel').and.returnValue({})
    };
    vEPService = {
      bannerBeforeAccorditionHeader:  new BehaviorSubject<any>('bannerBeforeAccorditionHeader' as any),
      targetTab:  new BehaviorSubject<any>('targetTab' as any),
    };
    component = new RacingEnhancedMultiplesComponent(racingEnhancedMultiplesService, gtmService, carouselService, vEPService);
  });

  describe('@ngOnInit', () => {
    it('should store data subscription, should NOT set any outcomes and set isSingleSlide to true', () => {
      racingEnhancedMultiplesService.getEnhancedMultiplesEvents = jasmine.createSpy('getEnhancedMultiplesEvents').and.returnValue(of({
        event1: {
          id: 1
        },
        event2: {
          id: 2
        }
      }));
      racingEnhancedMultiplesService.sortOutcomesByDate = jasmine.createSpy('sortOutcomesByDate').and.returnValue(
        [{
          event1: {
            id: 1
          }
        }]);

      component.ngOnInit();

      expect(component['loadDataSubscription']).toBeDefined();
      expect(component.events).toEqual([{
        event1: {
          id: 1
        }
      }]);
      expect(component.isSingleSlide).toBe(true);
    });

    it('should store data subscription, should set outcomes and set isSingleSlide to false', () => {
      racingEnhancedMultiplesService.getEnhancedMultiplesEvents = jasmine.createSpy('getEnhancedMultiplesEvents').and.returnValue(of({
        event1: {
          id: 1
        },
        event2: {
          id: 2
        }
      }));
      racingEnhancedMultiplesService.sortOutcomesByDate = jasmine.createSpy('sortOutcomesByDate').and.returnValue([{
        event1: {
          id: 1
        },
      }, {
        event2: {
          id: 2
        }
      }]);

      component.ngOnInit();

      expect(component['loadDataSubscription']).toBeDefined();
      expect(component.events).toEqual([{
        event1: {
          id: 1
        },
      }, {
        event2: {
          id: 2
        }
      }]);
      expect(component.isSingleSlide).toBe(false);
    });
  });

  describe('@ngOnDestroy', () => {
    it('should unsubscribe from data subscription', () => {
      const loadDataSubscription = jasmine.createSpyObj('loadDataSubscription', ['unsubscribe']);

      component['loadDataSubscription'] = null;
      component.ngOnDestroy();
      component['loadDataSubscription'] = loadDataSubscription;
      component.ngOnDestroy();

      expect(loadDataSubscription.unsubscribe).toHaveBeenCalled();
    });
  });

  describe('@sendCollapseGTM', () => {
    it('should NOT do anything if isFirstTimeCollapsed is falsy', () => {
      component.isFirstTimeCollapsed = true;

      component.sendCollapseGTM();

      expect(gtmService.push).not.toHaveBeenCalled();
      expect(component.isFirstTimeCollapsed).toBe(true);
    });

    it('should push dara to gtmService and set isFirstTimeCollapsed to true', () => {
      component.isFirstTimeCollapsed = false;

      component.sendCollapseGTM();

      expect(gtmService.push).toHaveBeenCalled();
      expect(component.isFirstTimeCollapsed).toBe(true);
    });
  });

  it('@prevSlide should call get and previous method', () => {
    const carousel = {
      previous: jasmine.createSpy('previous').and.returnValue(jasmine.any(Function))
    };
    carouselService.get = jasmine.createSpy('get').and.returnValue({ previous: carousel.previous });

    component.prevSlide();

    expect(carousel.previous).toHaveBeenCalled();
    expect(carouselService.get).toHaveBeenCalled();
  });

  it('@nextSlide should call get and next method', () => {
    const carousel = {
      next: jasmine.createSpy('previous').and.returnValue(jasmine.any(Function))
    };
    carouselService.get = jasmine.createSpy('get').and.returnValue({ next: carousel.next });

    component.nextSlide();

    expect(carousel.next).toHaveBeenCalled();
    expect(carouselService.get).toHaveBeenCalled();
  });

  describe('@isLastSlide', () => {
    it('should return true', () => {
      carouselService.get = jasmine.createSpy('get').and.returnValue({
        currentSlide: 3,
        slidesCount: 4
      });

      expect(component.isLastSlide()).toBe(true);
    });

    it('should return false', () => {
      carouselService.get = jasmine.createSpy('get').and.returnValue({
        currentSlide: 2,
        slidesCount: 4
      });

      expect(component.isLastSlide()).toBe(false);
    });
  });

  describe('@isPrevActionAvailable', () => {
    it('should return true', () => {
      component.isFirstSlide = jasmine.createSpy('isFirstSlide').and.returnValue(true);

      const res = component.isPrevActionAvailable();

      expect(component.isFirstSlide).toHaveBeenCalled();
      expect(res).toBe(true);
    });

    it('should return false', () => {
      component.isFirstSlide = jasmine.createSpy('isFirstSlide').and.returnValue(false);

      const res = component.isPrevActionAvailable();

      expect(component.isFirstSlide).toHaveBeenCalled();
      expect(res).toBe(false);
    });
  });

  describe('@isNextActionAvailable', () => {
    it('should return true', () => {
      component.isLastSlide = jasmine.createSpy('isLastSlide').and.returnValue(true);

      const res = component.isNextActionAvailable();

      expect(component.isLastSlide).toHaveBeenCalled();
      expect(res).toBe(false);
    });

    it('should return true', () => {
      component.isLastSlide = jasmine.createSpy('isLastSlide').and.returnValue(false);

      const res = component.isNextActionAvailable();

      expect(component.isLastSlide).toHaveBeenCalled();
      expect(res).toBe(true);
    });
  });

  it('@trackById should return outcome.id', () => {
    const outcome = { id: 2 };
    expect(component.trackById(1, outcome)).toBe('2');
  });

  describe('isDisplayBanner', () => {
    it('isDisplayBanner', () => {
      component.bannerBeforeAccorditionHeader = 'test'
      const retVal = component.isDisplayBanner('test');
      expect(retVal).toBeTruthy();
    })

    it('isDisplayBanner name undefined', () => {
      component.bannerBeforeAccorditionHeader = null
      const retVal = component.isDisplayBanner(null);
      expect(retVal).toBeTruthy();
    })
  })
});
