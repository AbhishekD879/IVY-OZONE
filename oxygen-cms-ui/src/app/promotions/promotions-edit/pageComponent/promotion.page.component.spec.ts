import { fakeAsync, TestBed, tick } from '@angular/core/testing';

import { PromotionPageComponent } from './promotion.page.component';
import { of, throwError } from 'rxjs';
import { Competition, Promotion, SportCategory } from '@root/app/client/private/models';
import { COMPETITIONS_MOCK, CREATE_PROMOTION_REQ_MOCK, SPORT_CATEGORY_MOCK } from '../../promotions-create/constants/betpack.config';
import { Router } from '@angular/router';

describe('PromotionsPageComponent', () => {
  let component: PromotionPageComponent,
    dialogService,
    route,
    router,
    promotionsAPIService, betpackService;
  let promotionsNavigationsService,apiClientService;
  let promotion: Promotion, sportCategory: SportCategory[], competitionsData: Competition[];
  let freeRideValidationServiceService;

  beforeEach(() => {
    promotion = CREATE_PROMOTION_REQ_MOCK;
    sportCategory = SPORT_CATEGORY_MOCK;
    competitionsData = COMPETITIONS_MOCK;
    dialogService = { showNotificationDialog: jasmine.createSpy('showNotificationDialog') };
    route = {
      snapshot: {
        paramMap: {
          get: jasmine.createSpy('get').and.returnValue('idMock')
        }
      }
    };

    TestBed.configureTestingModule({
      providers: [
        { provide: Router, useValue: router }
      ]
    });

    router = { navigate: jasmine.createSpy('navigate') };
    promotionsAPIService = {
      getSportCategories: jasmine.createSpy('getSportCategories').and.returnValue(of({
        body: { sportCategory }
      })),
      getCompetitions: jasmine.createSpy('getCompetitions').and.returnValue(of({
        body: { competitionsData }
      })),
      getSinglePromotionData: jasmine.createSpy('getSinglePromotionData').and.returnValue(of({
        body: { promotion }
      })),
      removePromotionImage: jasmine.createSpy('removePromotionImage').and.returnValue(of({})),
      postNewPromotionImage: jasmine.createSpy('postNewPromotionImage').and.returnValue(of({ body: promotion })),
      deletePromotion: jasmine.createSpy('deletePromotion').and.returnValue(of({})),
      postNewPromotion: jasmine.createSpy('postNewPromotion').and.returnValue(of({})),
      putPromotionChanges: jasmine.createSpy('putPromotionChanges').and.returnValue(of({}))
    };
    betpackService = {
      isBetPackDetailsValid: jasmine.createSpy('isBetPackDetailsValid').and.returnValue(true)
    };

    promotionsNavigationsService = {
      findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({ body: [] }))
    };
    apiClientService = {
      promotionsNavigationsService: () => promotionsNavigationsService
    };
    freeRideValidationServiceService = {

    };

    component = new PromotionPageComponent(dialogService, route, router, promotionsAPIService, betpackService,
      freeRideValidationServiceService, apiClientService
    );
  });

  it('constructor', () => {
    expect(component).toBeDefined();
  });

  it('should Init', () => {
    component.ngOnInit();
    expect(component.id).toEqual('idMock');
    expect(promotionsAPIService.getSportCategories).toHaveBeenCalled();
    expect(promotionsAPIService.getCompetitions).toHaveBeenCalled();
    expect(promotionsAPIService.getSinglePromotionData).toHaveBeenCalled();
  });


  describe('loadInitialData', () => {
    it('Load sport categories to map promotion', fakeAsync(() => {
      promotionsAPIService.getSportCategories.and.returnValue(of({ body: sportCategory }));
      component.loadInitialData();
      tick();
      tick();
      expect(promotionsAPIService.getSportCategories).toHaveBeenCalled();
      expect(component.sportCategories).toBeDefined();
    }));

    it('Load competitions to map promotion', fakeAsync(() => {
      promotionsAPIService.getCompetitions.and.returnValue(of({ body: competitionsData }));
      component.loadInitialData();
      tick();
      tick();
      expect(promotionsAPIService.getCompetitions).toHaveBeenCalled();
      expect(component.competitions).toEqual(competitionsData);
    }));

    it('Load navigations to map navigation', fakeAsync(() => {
      let mockNavigationData =  [
        {
            id: "62c6b78cc1bbb96a5e621894",
            brand: 'testUser',
            title: "Tenis",
            status: true,
            updatedAt: "2022-07-07T10:38:04.814Z",
            promotionIds: [
                "62c806e8262e87300effd7b0",
                "62c806fc262e87300effd7b1"
            ],   
            navItems : [{
              name: 'test',
               navType : 'url',
               navigationGroupId: '62c806e8262e87300effd7b0',
               id: '62c806e8262e87300effd7b0',
               brand: 'ladbrokes',
               createdBy: 'testUser',
               createdAt: 'testUser',
               updatedBy: 'testUser',
               updatedAt: 'testUser',
               updatedByUserName: 'testUser;',
               createdByUserName: 'testUser',
              }]
            }
          ];

      spyOn(component,'loadPromotion');
      promotionsAPIService.getCompetitions.and.returnValue(of({ body: competitionsData }));
      promotionsNavigationsService.findAllByBrand.and.returnValue(of({ body: mockNavigationData }));

      component.loadInitialData();
      tick();
      tick();
      expect(promotionsNavigationsService.findAllByBrand).toHaveBeenCalled();
      expect(component.promotionNavigation).toEqual(mockNavigationData);
    }));
  });


  describe('loadPromotion', () => {
    it('Load current promotion data', fakeAsync(() => {
      promotionsAPIService.getSinglePromotionData.and.returnValue(of({ body: promotion }));
      component.loadPromotion();
      tick();
      tick();
      expect(promotionsAPIService.getSinglePromotionData).toHaveBeenCalled();
      expect(component.promotion).toBeDefined();
    }));

    it('Load current promotion data Error scenario', fakeAsync(() => {
      promotionsAPIService.getSinglePromotionData.and.returnValue(throwError(new Error('message')));
      component.loadPromotion();
      tick();
      tick();
      expect(promotionsAPIService.getSinglePromotionData).toHaveBeenCalled();
      expect(router.navigate).toHaveBeenCalledWith(['/promotions']);
    }));
  });

  describe('updatePromotion', () => {
    it(' update property, called by child component eventEmitter', () => {
      component.loadPromotion();
      component.updatePromotion('data', 'description');
      expect(component.promotion.description).toEqual('data');
    });
  });


  describe('uploadFile', () => {
    it('Upload file on input change event.', () => {
      const file = new FormData();
      component.loadPromotion();
      component.promotion.id = promotion.id;
      component.uploadFile(file);
      expect(promotionsAPIService.postNewPromotionImage).toHaveBeenCalled();
    });
  });

  describe('removeFile', () => {
    it('remove file on input change event.', () => {
      component.loadPromotion();
      component.promotion.id = promotion.id;
      component.removeFile();
      expect(promotionsAPIService.removePromotionImage).toHaveBeenCalled();
      expect(dialogService.showNotificationDialog).toHaveBeenCalled();
    });
  });

  describe('removePromotion', () => {
    it('Send DELETE API request', () => {
      component.loadPromotion();
      component.promotion.id = promotion.id;
      component.removePromotion();
      expect(promotionsAPIService.deletePromotion).toHaveBeenCalled();
      expect(dialogService.showNotificationDialog).toHaveBeenCalled();
      expect(router.navigate).toHaveBeenCalledWith(['/promotions']);
    });
  });

  describe('actionsHandler', () => {
    it('check actions Handler for save', () => {
      component.loadPromotion();
      component.promotion = promotion;
      component.actionsHandler('save');
      expect(betpackService.isBetPackDetailsValid).toHaveBeenCalled();
      expect(promotionsAPIService.putPromotionChanges).toHaveBeenCalled();
    });
  });

  describe('isVipLevelValid', () => {
    it('check Validity of the isVipLevel', () => {
      component.loadPromotion();
      component.promotion.vipLevelsInput = '123';
      component.isVipLevelValid();
      expect(component.isVipLevelValid()).toBeTruthy();
    });
  });
});
