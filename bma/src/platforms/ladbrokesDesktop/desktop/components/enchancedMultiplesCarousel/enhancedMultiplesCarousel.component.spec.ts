import { of } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { EnhancedMultiplesCarouselComponent } from './enhancedMultiplesCarousel.component';

describe('EnhancedMultiplesCarouselComponent', () => {
  let component: EnhancedMultiplesCarouselComponent;
  let carouselService;
  let enhancedMultiplesCarouselService;
  let germanSupportService;
  let pubSubService;

  beforeEach(() => {
    carouselService = {};
    enhancedMultiplesCarouselService = {
      setEventDate: jasmine.createSpy('setEventDate'),
      buildEnhancedMultiplesData: jasmine.createSpy('buildEnhancedMultiplesData').and.returnValue([{ name: 'Event' }]),
      getEnhancedMultiplesEvents: jasmine.createSpy('getEnhancedMultiplesEvents').and.returnValue(of([{ name: 'Event' }]))
    };
    germanSupportService = {
      isGermanUser: jasmine.createSpy('isGermanUser'),
      filterEnhancedOutcomes: jasmine.createSpy('filterEnhancedOutcomes')
    };
    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };

    component = new EnhancedMultiplesCarouselComponent(
      carouselService,
      enhancedMultiplesCarouselService,
      germanSupportService,
      pubSubService
    );
    component.sportName = 'football';
  });

  describe('ngOnInit', () => {
    it('should remove restricted outcomes', () => {
      component['removeRestrictedOutcomes'] = jasmine.createSpy('removeRestrictedOutcomes');
      component.ngOnInit();
      expect(component['removeRestrictedOutcomes']).toHaveBeenCalled();

      expect(enhancedMultiplesCarouselService.setEventDate).toHaveBeenCalledWith([{ name: 'Event' }]);
      expect(enhancedMultiplesCarouselService.buildEnhancedMultiplesData).toHaveBeenCalledWith([{ name: 'Event' }], 'football');
      expect(enhancedMultiplesCarouselService.getEnhancedMultiplesEvents).toHaveBeenCalledWith('football');
      expect(component.isSingleSlide).toEqual(true);
    });

    it('should remove restricted outcomes after login', () => {
      component['removeRestrictedOutcomes'] = jasmine.createSpy('removeRestrictedOutcomes');
      pubSubService.subscribe.and.callFake((p1, p2, cb) => cb());
      component.ngOnInit();
      expect(component['removeRestrictedOutcomes']).toHaveBeenCalled();

      expect(enhancedMultiplesCarouselService.setEventDate).toHaveBeenCalledWith([{ name: 'Event' }]);
      expect(enhancedMultiplesCarouselService.buildEnhancedMultiplesData).toHaveBeenCalledWith([{ name: 'Event' }], 'football');
      expect(enhancedMultiplesCarouselService.getEnhancedMultiplesEvents).toHaveBeenCalledWith('football');
      expect(component.isSingleSlide).toEqual(true);
    });
  });

  describe('#ngOnDestroy', () => {
   it('ngOnDestroy', () => {
     component.ngOnDestroy();

     expect(pubSubService.unsubscribe).toHaveBeenCalledWith(component['subscriberName']);
   });

   it('ngOnDestroy for initDataSubscription', () => {
     component.ngOnInit();
     component['initDataSubscription'].unsubscribe = jasmine.createSpy('component.initDataSubscription.unsubscribe');
     component.ngOnDestroy();

     expect(pubSubService.unsubscribe).toHaveBeenCalledWith(component['subscriberName']);
     expect(component['initDataSubscription'].unsubscribe).toHaveBeenCalled();
   });
 });

  describe('removeRestrictedOutcomes', () => {
    it('should remove restricted outcomes', () => {
      germanSupportService.isGermanUser.and.returnValue(true);
      component['removeRestrictedOutcomes']();
      expect(germanSupportService.filterEnhancedOutcomes).toHaveBeenCalled();
    });

    it('should not remove restricted outcomes', () => {
      germanSupportService.isGermanUser.and.returnValue(false);
      component['removeRestrictedOutcomes']();
      expect(germanSupportService.filterEnhancedOutcomes).not.toHaveBeenCalled();
    });
  });

  it('trackByOutcomeId', () => {
    const res = component.trackById(1, { id: '123' } as any);

    expect(res).toEqual('1123');
  });
});
