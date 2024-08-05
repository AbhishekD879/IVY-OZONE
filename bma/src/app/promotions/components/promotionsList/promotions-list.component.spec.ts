import { fakeAsync, tick } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import * as _ from 'underscore';

import { PromotionsListComponent } from './promotions-list.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('PromotionsListComponent', () => {
  let promotionsService;
  let pubSubService, user;
  let component: PromotionsListComponent;
  let bonusSuppressionService;

  beforeEach(() => {
    promotionsService = {
      isUserLoggedIn: jasmine.createSpy('isUserLoggedIn'),
      preparePromotions: jasmine.createSpy('preparePromotions').and.returnValue(of(null)),
      promotionsRetailData: jasmine.createSpy('promotionsRetailData').and.returnValue(of(null)),
      promotionsGroupedData: jasmine.createSpy('promotionsGroupedData').and.returnValue(of(null)),
      promotionsDigitalData: jasmine.createSpy('promotionsDigitalData').and.returnValue(of(null)),
      isGroupBySectionsEnabled: jasmine.createSpy('isGroupBySectionsEnabled'),
      filterByOfferId: jasmine.createSpy('filterByOfferId'),
      getPromotionsFromSiteCore: jasmine.createSpy('getPromotionsFromSiteCore').and.returnValue(of({}))
    } as any;
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    user = {
      bppToken: 'abc123',
      status: true
    };
    bonusSuppressionService = {
      navigateAwayForRGYellowCustomer: jasmine.createSpy('navigateAwayForRGYellowCustomer'),
      checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(true)
    };

    component = new PromotionsListComponent(
      promotionsService,
      pubSubService,
      user,
      bonusSuppressionService
    );
  });

  it('constructor', () => {
    expect(promotionsService.isUserLoggedIn).toHaveBeenCalledTimes(1);
  });

  describe('ngOnInit', () => {
    beforeEach(() => {
      component.showSpinner = jasmine.createSpy('showSpinner');
      component.hideSpinner = jasmine.createSpy('hideSpinner');
      component.showError = jasmine.createSpy('showError');
      component['init'] = jasmine.createSpy('init');
      component['getPromotionsRequest'] = jasmine.createSpy('getPromotionsRequest').and.returnValue(of({}));
    });

    it('should not load data', () => {
      component.promotions = [];

      component.ngOnInit();

      expect(component.showSpinner).toHaveBeenCalledTimes(1);
      expect(component['init']).toHaveBeenCalledTimes(1);
    });

    it('should load data', fakeAsync(() => {
      component.promotions = undefined;
      const response = [{
        teasers : []
      }];

      component.isRetail = true;
      component.ngOnInit();
      tick();

      (component['getPromotionsRequest'] as any).and.returnValue(of({ promotionsBySection: [] }));
      (promotionsService['getPromotionsFromSiteCore']as any).and.returnValue(of(response));
      component.ngOnInit();
      tick();

      expect(component.showSpinner).toHaveBeenCalledTimes(2);
      expect(component['getPromotionsRequest']).toHaveBeenCalledTimes(2);
      expect(component['init']).toHaveBeenCalledTimes(2);
    }));

    it('should show error', fakeAsync(() => {
      component.promotions = undefined;
      (component['getPromotionsRequest'] as any).and.returnValue(throwError(null));

      component.ngOnInit();
      tick();

      expect(component['init']).not.toHaveBeenCalledTimes(1);
      expect(component.showError).toHaveBeenCalledTimes(1);
    }));
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledTimes(1);
  });

  it('trackPromotionBy', () => {
    expect(component.trackPromotionBy(0, { id: '1' } as any)).toBe('1');
  });

  it('trackGroupBy', () => {
    expect(component.trackGroupBy(0, { name: 'group1' } as any)).toBe('group1_0');
  });

  describe('init', () => {
    beforeEach(() => {
      component['initPromotionsList'] = jasmine.createSpy('initPromotionsList');
    });

    it('init promotions list (not loggedIn)', () => {
      component['init']();
      expect(component['initPromotionsList']).toHaveBeenCalledTimes(1);
      expect(pubSubService.subscribe).toHaveBeenCalledTimes(2);
    });

    it('session login & vip status changed', fakeAsync(() => {
      component['getPromotionsRequest'] = jasmine.createSpy('getPromotionsRequest').and.returnValue(of({}));
      bonusSuppressionService.checkIfYellowFlagDisabled = jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(false);
      pubSubService.subscribe.and.callFake((p1, p2, cb) => {
        if (p2 === 'SESSION_LOGIN') {
          cb();
        }
      });
      component['init']();
      tick();
      expect(component['initPromotionsList']).toHaveBeenCalledTimes(2);
    }));

    it('logout', fakeAsync(() => {
      pubSubService.subscribe.and.callFake((p1, p2, cb) => {
        _.contains(p2, pubSubService.API.SESSION_LOGOUT) && cb();
      });
      promotionsService.isUserLoggedIn.and.returnValue(true);

      component.lastLoginStatus = false;
      component['init']();
      tick();

      component.lastLoginStatus = true;
      component['init']();
      tick();

      expect(component['initPromotionsList']).toHaveBeenCalledTimes(4);
    }));
  });

  it('initPromotionsList', () => {
    expect(component.state.loading).toEqual(true);
    component.promotions = [];
    component.groupedPromotions = undefined;
    component['initPromotionsList']();

    component.promotions = undefined;
    component.groupedPromotions = {
      promotionsBySection: [
        { promotions: [] }, { promotions: [] }
      ]
    } as any;
    component['initPromotionsList']();

    expect(promotionsService.preparePromotions).toHaveBeenCalledTimes(3);
    expect(promotionsService.filterByOfferId).toHaveBeenCalled();
    expect(component.state.loading).toEqual(false);
  });

  describe('availableGroupedPromotions', () => {
    it('should check if availableGroupedPromotions (empty promotionsBySection)', () => {
      component.groupedPromotions = <any>{
        promotionsBySection: []
      };
      component['initPromotionsList']();
      expect(component.availableGroupedPromotions).toEqual(false);
    });

    it('should check if availableGroupedPromotions (promotions)', () => {
      component.groupedPromotions = <any>{
        promotionsBySection: [{}]
      };
      promotionsService.preparePromotions.and.returnValue([]);
      component['initPromotionsList']();
      expect(component.availableGroupedPromotions).toEqual(false);
    });

    it('should check if availableGroupedPromotions (promotions)', () => {
      component.groupedPromotions = <any>{
        promotionsBySection: [{}]
      };
      promotionsService.preparePromotions.and.returnValue([{}]);
      component['initPromotionsList']();
      expect(component.availableGroupedPromotions).toEqual(true);
    });
  });

  describe('getPromotionsRequest', () => {
    it('retail promotions', () => {
      component.isRetail = true;
      component['getPromotionsRequest']();
      expect(promotionsService.promotionsRetailData).toHaveBeenCalledTimes(1);
    });

    it('digital or grouped data', fakeAsync(() => {
      promotionsService.isGroupBySectionsEnabled.and.returnValue(of(true));
      component['getPromotionsRequest']().subscribe();
      tick();

      promotionsService.isGroupBySectionsEnabled.and.returnValue(of(false));
      component['getPromotionsRequest']().subscribe();
      tick();

      expect(promotionsService.isGroupBySectionsEnabled).toHaveBeenCalledTimes(2);
      expect(promotionsService.promotionsGroupedData).toHaveBeenCalledTimes(1);
      expect(promotionsService.promotionsDigitalData).toHaveBeenCalledTimes(1);
    }));
  });

  describe('setPromotions', () => {
    it('should set grouped promotions if skipGrouped is as default false', () => {
      const data = {
        promotionsBySection: [{ name: 'test', promotions:[{title:'promotions'}] }],
        promotions: [{ name: 'test2' }]
      } as any;

      component['setPromotions'](data);

      expect(component.groupedPromotions).toEqual(data);
      expect(component.promotions).toBeFalsy();
    });

    it('should set grouped promotions if skipGrouped is as default false', () => {
      const data = {
        promotionsBySection: null,
        promotions: [{ name: 'test2' }]
      } as any;

      component['setPromotions'](data);

      expect(component.groupedPromotions).toBeFalsy();
      expect(component.promotions).toEqual(data.promotions);
    });

    it('should not set grouped promotions if skipGrouped is true', () => {
      const data = {
        promotionsBySection: [{ name: 'test' }],
        promotions: [{ name: 'test2' }]
      } as any;
      const storedPromotions = [{ name: 'test3' }] as any;

      component.groupedPromotions = storedPromotions;
      component.skipGrouped = true;
      component['setPromotions'](data);

      expect(component.groupedPromotions).toEqual(storedPromotions);
      expect(component.promotions).toBeFalsy();
    });

    it('should not set grouped promotions if skipGrouped is true', () => {
      const data = {
        promotionsBySection: null,
        promotions: [{ name: 'test2' }]
      } as any;
      const storedPromotions = [{ name: 'test3' }] as any;

      component.promotions = storedPromotions;
      component.skipGrouped = true;
      component['setPromotions'](data);

      expect(component.groupedPromotions).toBeFalsy();
      expect(component.promotions).toEqual(storedPromotions);
    });
  });
});
