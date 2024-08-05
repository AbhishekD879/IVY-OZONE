import { of } from 'rxjs';

import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { EnhancedMultiplesTabComponent } from './enhanced-multiples-tab.component';

describe('EnhancedMultiplesTabComponent', () => {
  let component: EnhancedMultiplesTabComponent;
  let enhancedMultiplesService;
  let filterSerice;
  let germanSupportService;
  let pubSubService;

  beforeEach(() => {
    enhancedMultiplesService = {
      getAllEnhancedMultiplesEvents: jasmine.createSpy('getAllEnhancedMultiplesEvents').and.returnValue(of([]))
    };
    filterSerice = {};
    germanSupportService = {
      isGermanUser: jasmine.createSpy('isGermanUser'),
      filterEnhancedCategories: jasmine.createSpy('filterEnhancedCategories')
    };
    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };

    component = new EnhancedMultiplesTabComponent(
      enhancedMultiplesService,
      filterSerice,
      germanSupportService,
      pubSubService
    );
  });

  it('should subscribe to session login', () => {
    component.ngOnInit();
    expect(pubSubService.subscribe).toHaveBeenCalledWith(component['subscriberName'], 'SESSION_LOGIN', jasmine.any(Function));
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith(component['subscriberName']);
  });

  it('eventsLoaded', () => {
    component['removeRestrictedCategories'] = jasmine.createSpy('removeRestrictedCategories');
    component['eventsLoaded']([]);
    expect(component['removeRestrictedCategories']).toHaveBeenCalled();
  });

  describe('removeRestrictedCategories', () => {
    it('should remove restricted categories', () => {
      germanSupportService.isGermanUser.and.returnValue(true);
      component['removeRestrictedCategories']();
      expect(germanSupportService.filterEnhancedCategories).toHaveBeenCalled();
    });

    it('should not remove restricted categories', () => {
      germanSupportService.isGermanUser.and.returnValue(false);
      component['removeRestrictedCategories']();
      expect(germanSupportService.filterEnhancedCategories).not.toHaveBeenCalled();
    });
  });
});
