
import { HttpErrorResponse } from '@angular/common/http';
import { of, throwError } from 'rxjs';
import { PopularAccasWidgetComponent } from './popular-accas-widget.component';
import { popularAccasMock } from './popular-accas-widget.mock';


describe('PopularbetsComponent', () => {
  let component: PopularAccasWidgetComponent;
  let router,brandService,apiClientService,globalLoaderService,snackBar,dialogService,errorService;

  beforeEach(() =>{
    apiClientService = {
        popularAccasWidgetService : jasmine.createSpy('popularAccasWidgetService').and.returnValue({
            getPopularAccasWidgetData: jasmine.createSpy('').and.returnValue(of({ body: {} })),
            putPopularAccasWidgetData: jasmine.createSpy('').and.returnValue(of({})),
            postPopularAccasWidgetData: jasmine.createSpy('').and.returnValue(of({ })),
            getsegmentdata: jasmine.createSpy('').and.returnValue(of({ })),
            reorderPopularAccasWidgetcardData: jasmine.createSpy('').and.returnValue(of({ })),
            deletePopularAccasWidgetCardData: jasmine.createSpy('').and.returnValue(of({ }))
      })
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog')
    };
    brandService ={
      brand: "bma"
    };
    router = {
        navigate: jasmine.createSpy('navigate')
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader'),
    };
    snackBar = {
      open: jasmine.createSpy('open'),
    }
    errorService = {
      emitError: jasmine.createSpy('emitError')
    };
    component = new PopularAccasWidgetComponent(  router,brandService,apiClientService,globalLoaderService,snackBar,dialogService,errorService);
    component.popularAccasWidgetData = popularAccasMock as any;
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    } as any;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it("ngOnInit should initialize data is empty", () => {
    component.ngOnInit();
    expect(component.popularAccasWidgetData).toBeDefined();
  });

  it("ngOnInit should initialize data", () => {
    apiClientService.popularBetsApiService().getDetailsByBrand.and.returnValue(of({ body: component.popularAccasWidgetData }))
    apiClientService.popularBetsApiService().getsegmentdata.and.returnValue(of({ body: component.popularAccasWidgetData }))
    component.ngOnInit();
    expect(component.popularAccasWidgetData.displayOn).toBeDefined();
  });

  it("ngOnInit with service error 404", () => {
    apiClientService.popularBetsApiService().getDetailsByBrand.and.returnValue(throwError({ status: 404 }))
    apiClientService.popularBetsApiService().getsegmentdata.and.returnValue(throwError({ status: 404 }))
    component.ngOnInit();
    expect(errorService.emitError).toHaveBeenCalled();
  });

  it("ngOnInit with service error 401", () => {
    apiClientService.popularBetsApiService().getDetailsByBrand.and.returnValue(throwError({ error: { message: '401' } }))
    apiClientService.popularBetsApiService().getsegmentdata.and.returnValue(throwError({ error: { message: '401' } }))
    component.ngOnInit();
    expect(errorService.emitError).toHaveBeenCalled();
  });



  it("save popularAccasWidgetData", () => {
    component.popularAccasWidgetData.createdAt='test';
    apiClientService.popularBetsApiService().postPopularAccasWidgetCardData.and.returnValue(of({ body: component.popularAccasWidgetData }))
    component.actionsHandler('save');
    expect(component.popularAccasWidgetData).toEqual(undefined)
  });

  it("revert popularAccasWidgetData", () => {
    apiClientService.popularBetsApiService().getPopularAccasWidgetData.and.returnValue(of(component.popularAccasWidgetData))
    component.actionsHandler('revert');
    expect(component.popularAccasWidgetData).toBeDefined();
  });

  it("edit popularAccasWidgetData", () => {
    component.actionsHandler('edit');
    expect(component.popularAccasWidgetData.displayOn).toBeDefined();
  });

  it("save popularAccasWidgetData data without createdAt", () => {
    component.popularAccasWidgetData.createdAt = null;
    apiClientService.popularBetsApiService().postPopularAccasWidgetData.and.returnValue(of({ body: component.popularAccasWidgetData }))
    component.actionsHandler('save');
    expect(component.popularAccasWidgetData).toBeDefined();
  });

  it("save popularAccasWidgetData data without createdAt error scenario", () => {
    component.popularAccasWidgetData.createdAt = null;
    apiClientService.popularBetsApiService().postPopularAccasWidgetData.and.returnValue(throwError(new HttpErrorResponse({ error: { message: '401' } })));
    component.actionsHandler('save');
    expect(errorService.emitError).toHaveBeenCalled();
  });

  it("should call validationHandler", () => {
    component.popularAccasWidgetForm = { valid: true } as any;
    const isValid = component.validationHandler();
    expect(isValid).toBeDefined();
  });
  
  it("should call removeHandler", () => {
    component.removeHandler({is:'12323'} as any);
    expect(snackBar.open).toHaveBeenCalled();
  });

  it("should call removeHandler with error", () => {
    apiClientService.popularBetsApiService().deletePopularAccasWidgetCardData.and.returnValue(throwError(new HttpErrorResponse({ error: { message: '401' } })));
    component.removeHandler({is:'12323'} as any);
    expect(errorService.emitError).toHaveBeenCalled();
  });

  it("should call reorderHandler", () => {
    component.reorderHandler({});
    expect(snackBar.open).toHaveBeenCalled();
  });

  it("should call reorderHandler with error", () => {
    apiClientService.popularBetsApiService().reorderPopularAccasWidgetcardData.and.returnValue(throwError(new HttpErrorResponse({ error: { message: '401' } })));
    component.reorderHandler({});
    expect(errorService.emitError).toHaveBeenCalled();
  });

  it("should call goToHomepage", () => {
    component.goToHomepage('');
    expect(router.navigate).toHaveBeenCalled();
  });
});

