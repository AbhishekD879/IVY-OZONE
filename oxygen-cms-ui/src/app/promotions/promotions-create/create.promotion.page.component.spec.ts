import { fakeAsync, tick } from '@angular/core/testing';
import { FormControl } from '@angular/forms';
import { Competition, Promotion, SportCategory } from '@root/app/client/private/models';
import { of } from 'rxjs';
import { COMPETITIONS_MOCK, CREATE_PROMOTION_REQ_MOCK, SPORT_CATEGORY_MOCK } from './constants/betpack.config';
import { CreatePromotionComponent } from './create.promotion.page.component';

describe('CreatePromotionComponent', () => {
  let component: CreatePromotionComponent;
  let errorService;
  let dialogService;
  let route;
  let router;
  let promotionsAPIService;
  let brandService, betpackService;
  let promotionsNavigationsService, apiClientService, freeRideValidationServiceService;
  let promotion: Promotion, sportCategory: SportCategory[], competitionsData: Competition[];

  beforeEach(() => {
    promotion = CREATE_PROMOTION_REQ_MOCK;
    sportCategory = SPORT_CATEGORY_MOCK;
    competitionsData = COMPETITIONS_MOCK;
    errorService = {};
    dialogService = { showNotificationDialog: jasmine.createSpy('showNotificationDialog') };
    route = {
      snapshot: {
        paramMap: { get: () => 'id' }
      }
    };
    router = {};
    promotionsAPIService = {
      getSportCategories: jasmine.createSpy('getSportCategories').and.returnValue(of({ body: sportCategory })),
      getCompetitions: jasmine.createSpy('getCompetitions').and.returnValue(of({ body: competitionsData })),
      postNewPromotion: jasmine.createSpy('postNewPromotion').and.returnValue(of({ body: promotion })),
      postNewPromotionImage: jasmine.createSpy('postNewPromotionImage').and.returnValue(of({ promotion }))
    };
    brandService = {};
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

    }

    component = new CreatePromotionComponent(
      errorService, dialogService, route, router, promotionsAPIService, brandService, betpackService, freeRideValidationServiceService, apiClientService
    );
  });

  it('constructor', () => {
    expect(component).toBeDefined();
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.id).toEqual('id');
    expect(promotionsAPIService.getSportCategories).toHaveBeenCalled();
    expect(promotionsAPIService.getCompetitions).toHaveBeenCalled();
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
               url: 'testUrl', 
               navigationGroupId: '62c806e8262e87300effd7b0',
               id: '62c806e8262e87300effd7b0',
               brand: 'ladbrokes',
               createdBy: 'testUser',
               createdAt: 'testUser',
               updatedBy: 'testUser',
               updatedAt: 'testUser',
               updatedByUserName: 'testUser;',
               createdByUserName: 'testUser',
               navType:"url"
              }]
            }
          ];
      promotionsAPIService.getCompetitions.and.returnValue(of({ body: competitionsData }));
      promotionsNavigationsService.findAllByBrand.and.returnValue(of({ body: mockNavigationData }));
      
      component.loadInitialData();

      tick();
      tick();
      expect(promotionsNavigationsService.findAllByBrand).toHaveBeenCalled();
      expect(component.promotionNavigation).toEqual(mockNavigationData);
    }));
  });

  describe('updatePromotion', () => {
    it(' update property, called by child component eventEmitter', () => {
      component.updatePromotion('data', 'description');
      expect(component.promotion.description).toEqual('data');

    });
  });

  describe('prepareToUploadFile', () => {
    it('should upload file on calling prepareToUploadFile', () => {
      const event = {
        'target': {
          'files': [{
            'name': 'sample.png',
            'size': 38656,
            'type': 'image/png'
          }]
        }
      } as any;
      component.prepareToUploadFile(event);
      expect(component.uploadImageName).toBe('sample.png');
      expect(component.imageToUpload).toBe(event.target.files[0]);
    });

    it('should open error dialog', () => {
      const event = {
        'target': {
          'files': [{
            'name': 'sample.jpg',
            'size': 38656,
            'type': 'image/jpg'
          }]
        }
      } as any;
      component.prepareToUploadFile(event);
      expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
        title: `Error. Unsupported file type.`,
        message: 'Supported \"jpeg\" and \"png\".'
      });
    });
  });

  describe('uploadFile', () => {
    it('Upload file on input change event.', () => {
      const file = {
        'name': 'sample.jpg',
        'size': 38656,
        'type': 'image/jpg'
      };
      component.uploadFile(file);
      expect(promotionsAPIService.postNewPromotionImage).toHaveBeenCalled();
    });
  });

  describe('finishPromotionCreation', () => {
    it('finishPromotionCreation Confirmation pop up', () => {
      component.finishPromotionCreation();
      expect(dialogService.showNotificationDialog).toHaveBeenCalled();
    });
  });

  describe('removeMainImage', () => {
    it('removeMainImage: UploadImagename & imageToUpload', () => {
      component.removeMainImage();
      expect(component.uploadImageName).toBeUndefined();
      expect(component.imageToUpload).toBeUndefined();
    });
  });

  describe('isValidModel', () => {
    it('check Validity of the Model', () => {
      component.title = new FormControl('title');
      component.promoKey = new FormControl('1233');
      component.isValidModel();
      expect(component.isVipLevelValid()).toBeTruthy();
    });
  });

  describe('onShowToCustomerChange', () => {
    it('check onShowToCustomerChange', () => {
      component.onShowToCustomerChange('test');
      expect(component.promotion.showToCustomer).toEqual('test');
    });
  });
});
