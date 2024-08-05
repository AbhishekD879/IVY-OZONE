import { PopularbetsComponent } from './popular-bets.component';
import { HttpErrorResponse } from '@angular/common/http';
import { of, throwError } from 'rxjs';
import { POPULAR_BETS_VALUES } from './popular-bets-overlay.constants';

describe('PopularbetsComponent', () => {
  let component: PopularbetsComponent;
  let apiService, dialogService, brandService, router, globalLoaderService;

  beforeEach(() =>{
    apiService = {
      popularBetsApiService : jasmine.createSpy('popularBetsApiService').and.returnValue({
        getDetailsByBrand: jasmine.createSpy('').and.returnValue(of({ body: {} })),
        saveCMSPopularBetsData: jasmine.createSpy('').and.returnValue(of({})),
        updateCMSPopularBetsData: jasmine.createSpy('').and.returnValue(of({ }))
      })
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog')
    };
    brandService ={
      brand: "bma"
    };
    router = {
      url: 'most-popular/bet-receipt'
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader'),
    };
    component = new PopularbetsComponent(apiService, dialogService, brandService, router, globalLoaderService);
    component.popularBetsFormData = POPULAR_BETS_VALUES;
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    } as any;
    spyOn(component, 'createFormGroup');
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it("ngOnInit should initialize data is empty", () => {
    apiService.popularBetsApiService().getDetailsByBrand.and.returnValue(of({}));
    component.ngOnInit();
    expect(component.popularBetsFormData).toBeDefined();
  });

  it("ngOnInit should initialize data", () => {
    component.popularBetsFormData.displayForAllUsers = true;
    apiService.popularBetsApiService().getDetailsByBrand.and.returnValue(of({ body: component.popularBetsFormData }))
    component.ngOnInit();
    expect(component.popularBetsFormData.displayForAllUsers).toEqual(true);
  });

  it("ngOnInit with service error 404", () => {
    apiService.popularBetsApiService().getDetailsByBrand.and.returnValue(throwError({ status: 404 }))
    component.ngOnInit();
    expect(component.popularBetsFormData.brand).toEqual('bma');
  });

  it("ngOnInit with service error 401", () => {
    apiService.popularBetsApiService().getDetailsByBrand.and.returnValue(throwError({ error: { message: '401' } }))
    component.ngOnInit();
    expect(component.popularBetsFormData.displayForAllUsers).toEqual(true);
  });



  it("save popularBetsFormData", () => {
    component.popularBetsFormData.createdAt='test';
    apiService.popularBetsApiService().saveCMSPopularBetsData.and.returnValue(of({ body: component.popularBetsFormData }))
    component.actionsHandler('save');
    expect(component.popularBetsFormData).toEqual(undefined)
  });

  it("revert popularBetsFormData", () => {
    apiService.popularBetsApiService().saveCMSPopularBetsData.and.returnValue(of(component.popularBetsFormData))
    component.actionsHandler('revert');
    expect(component.popularBetsFormData).toBeDefined();
  });

  it("edit popularBetsFormData", () => {
    component.actionsHandler('edit');
    expect(component.popularBetsFormData.displayForAllUsers).toEqual(true);
  });

  it("save popularBetsFormData data without createdAt", () => {
    component.popularBetsFormData.createdAt = null;
    apiService.popularBetsApiService().saveCMSPopularBetsData.and.returnValue(of({ body: component.popularBetsFormData }))
    component.actionsHandler('save');
    expect(component.popularBetsFormData).toBeDefined();
  });

  it("save popularBetsFormData data without createdAt error scenario", () => {
    component.popularBetsFormData.createdAt = null;
    apiService.popularBetsApiService().saveCMSPopularBetsData.and.returnValue(throwError(new HttpErrorResponse({ error: { message: '401' } })));
    component.actionsHandler('save');
    expect(component.popularBetsFormData).toBeDefined();
  });


});

