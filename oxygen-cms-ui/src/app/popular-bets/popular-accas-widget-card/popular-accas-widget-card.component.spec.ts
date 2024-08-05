
import { HttpErrorResponse } from '@angular/common/http';
import { of, throwError } from 'rxjs';
import { PopularAccasWidgetCardComponent } from './popular-accas-widget-card.component';
import { popularAccasCardMock } from '../popular-accas-widget/popular-accas-widget.mock';


describe('PopularbetsComponent', () => {
  let component: PopularAccasWidgetCardComponent;
  let router,brandService,apiClientService,globalLoaderService,dialogService,activatedRoute;

  beforeEach(() =>{
    apiClientService = {
        popularAccasWidgetService : jasmine.createSpy('popularAccasWidgetService').and.returnValue({
            deletePopularAccasWidgetCardData: jasmine.createSpy('').and.returnValue(of({ })),
            getPopularAccasWidgetCardData: jasmine.createSpy('').and.returnValue(of({})),
            postpopularAccaWidgetCardsData: jasmine.createSpy('').and.returnValue(of({ })),
            putPopularAccasWidgetCardData: jasmine.createSpy('').and.returnValue(of({ }))
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
    component = new PopularAccasWidgetCardComponent(  brandService,apiClientService,globalLoaderService,dialogService,activatedRoute,router);
    component.popularAccaWidgetCardsData = popularAccasCardMock as any;
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    } as any;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it("ngOnInit should initialize data is empty", () => {
    component.ngOnInit();
    expect(component.popularAccaWidgetCardsData).toBeDefined();
  });

  it("ngOnInit should initialize data", () => {
    apiClientService.popularBetsApiService().getPopularAccasWidgetCardData.and.returnValue(of({ body: component.popularAccaWidgetCardsData }))
    component.ngOnInit();
    expect(component.popularAccaWidgetCardsData.numberOfTimeBackedThreshold).toBe(0);
  });

  it("ngOnInit with service error 404", () => {
    apiClientService.popularBetsApiService().getPopularAccasWidgetCardData.and.returnValue(throwError({ status: 404 }))
    component.ngOnInit();
    expect(dialogService.showNotificationDialog).toHaveBeenCalled();
  });

  it("ngOnInit with service error 401", () => {
    apiClientService.popularBetsApiService().getPopularAccasWidgetCardData.and.returnValue(throwError({ error: { message: '401' } }))
    component.ngOnInit();
    expect(dialogService.showNotificationDialog).toHaveBeenCalled();
  });

  it("save popularAccaWidgetCardsData", () => {
    component.popularAccaWidgetCardsData.createdAt='test';
    apiClientService.popularBetsApiService().putPopularAccasWidgetCardData.and.returnValue(of({ body: component.popularAccaWidgetCardsData }))
    component.actionsHandler('save');
    expect(component.popularAccaWidgetCardsData).toEqual(undefined)
  });

  it("revert popularAccaWidgetCardsData", () => {
    apiClientService.popularBetsApiService().getPopularAccasWidgetCardData.and.returnValue(of(component.popularAccaWidgetCardsData))
    component.actionsHandler('revert');
    expect(component.popularAccaWidgetCardsData).toBeDefined();
  });

  it("edit popularAccaWidgetCardsData", () => {
    component.actionsHandler('edit');
    expect(component.popularAccaWidgetCardsData.numberOfTimeBackedThreshold).toBe(0);
  });

  it("save popularAccaWidgetCardsData data without createdAt", () => {
    component.popularAccaWidgetCardsData.createdAt = null;
    apiClientService.popularBetsApiService().postPopularAccasWidgetCardData.and.returnValue(of({ body: component.popularAccaWidgetCardsData }))
    component.actionsHandler('save');
    expect(component.popularAccaWidgetCardsData).toBeDefined();
  });

  it("save popularAccaWidgetCardsData data without createdAt error scenario", () => {
    component.popularAccaWidgetCardsData.createdAt = null;
    apiClientService.popularBetsApiService().postPopularAccasWidgetCardData.and.returnValue(throwError(new HttpErrorResponse({ error: { message: '401' } })));
    component.actionsHandler('save');
    expect(dialogService.showNotificationDialog).toHaveBeenCalled();
  });

  it("should call validationHandler", () => {
    component.popularAccaWidgetCardsForm = { valid: true } as any;
    const isValid = component.validationHandler();
    expect(isValid).toBeDefined();
  });
  
  it("should call removeHandler", () => {
    component.actionsHandler('remove');
    expect(router.navigate).toHaveBeenCalled();
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it("should call removeHandler with error", () => {
    apiClientService.popularBetsApiService().deletePopularAccasWidgetCardData.and.returnValue(throwError(new HttpErrorResponse({ error: { message: '401' } })));
    component.actionsHandler('remove');
    expect(globalLoaderService.hideLoader).toHaveBeenCalled();
  });

  it("should call goToHomepage", () => {
    component.changeToNumber({target:{value:''}},'accaRangeMin');
    expect(component.formControls['accaRangeMin'].value).toBeDefined();
  });

  it("should call trackSportByTitle", () => {
    const data = component.trackSportByTitle({imageTitle:'test title'});
    expect(data).toBe('test title');
  });

  it("should call handleDateUpdate", () => {
    let event = {
        startDate: '21-10-2022',
        endDate: '22-10-2022',
      };
    component.handleDateUpdate(event);
    expect(component.popularAccaWidgetCardsData.displayFrom ).toBeDefined();
    expect(component.dateRangeError).toBeUndefined()
  });

  it("should call handleDateUpdate with start date less than end date", () => {
    let event = {
        startDate: '20-10-2022',
        endDate: '22-10-2022',
      };
    component.handleDateUpdate(event);
    expect(component.dateRangeError).toBe('"Display from" date should be less than display to date. Please amend your schedule.');
  });

  it("should call handleDateUpdate with start date less than todays date", () => {
    let event = {
        startDate: new Date(new Date().setDate(new Date().getDate() - 1)).toISOString(),
        endDate: '22-10-2022',
      };
    component.handleDateUpdate(event);
    expect(component.dateRangeError).toBe('"Display from" date should be today or future. Please amend your schedule.');
  });
});

