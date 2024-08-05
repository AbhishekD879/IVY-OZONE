
import { HttpErrorResponse } from "@angular/common/http";
import { FormGroup, FormControl, FormBuilder } from "@angular/forms";
import { of, throwError } from "rxjs";
import { FIRST_BET_PLACEMENT_MOCK_VALUES } from "../on-boarding-overlay.mock";
import { FirstBetOnBoardingOverlayComponent } from "./first-bet-on-boarding-overlay.component";

describe("FirstBetOnBoardingOverlayComponent", () => {
  let component: FirstBetOnBoardingOverlayComponent;
  let brandService, dialogService, apiService, cd, errorService, formBuilder, snackBar, globalLoaderService;

  beforeEach(() => {
    snackBar = {
      open: jasmine.createSpy('open')
    };
    brandService = {
      brand: "bma",
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog')
    };
    apiService = {
      firstBetPlacementService: jasmine.createSpy('firstBetPlacementService').and.returnValue({
        getDetailsByBrand: jasmine.createSpy('').and.returnValue(of({ body: {} })),
        updateFirstBet: jasmine.createSpy('updateFirstBet').and.returnValue(of({})),
        saveFirstBet: jasmine.createSpy('saveFirstBet').and.returnValue(of({})),
        postFirstBetBulbIcon: jasmine.createSpy('postFirstBetBulbIcon').and.returnValue(of({ body: {} })),
        removeFirstBetBulbIcon: jasmine.createSpy('removeFirstBetBulbIcon').and.returnValue(of({ body: {} }))
      })
    };
    cd = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    formBuilder =
      () => ({ group: object => ({}) });
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    errorService = {
      emitError: jasmine.createSpy('emitError')
    };
    component = new FirstBetOnBoardingOverlayComponent(apiService,
      dialogService, brandService, cd,
      formBuilder, snackBar, errorService, globalLoaderService);
    component.onBoardingFirstBet = FIRST_BET_PLACEMENT_MOCK_VALUES as any;
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    } as any;
    spyOn(component, 'createFormGroup');
  });

  it("should create", () => {

    expect(component).toBeTruthy();
  });

  it("ngOnInit should initialize data is empty", () => {
    apiService.firstBetPlacementService().getDetailsByBrand.and.returnValue(of({}));
    component.ngOnInit();
    expect(component.onBoardingFirstBet).toBeDefined();
  });

  it("ngOnInit should initialize data", () => {
    apiService.firstBetPlacementService().getDetailsByBrand.and.returnValue(of({ body: component.onBoardingFirstBet }))
    component.ngOnInit();
    expect(component.onBoardingFirstBet.moduleName).toEqual('test');
  });

  it("ngOnInit with service error 404", () => {
    apiService.firstBetPlacementService().getDetailsByBrand.and.returnValue(throwError({ status: 404 }))
    component.ngOnInit();
    expect(component.onBoardingFirstBet.moduleName).toEqual('');
  });

  it("ngOnInit with service error 401", () => {
    apiService.firstBetPlacementService().getDetailsByBrand.and.returnValue(throwError({ error: { message: '401' } }))
    component.ngOnInit();
    expect(component.onBoardingFirstBet.moduleName).toEqual('test');
  });

  it("verify onboarding FirstBet null", () => {
    const check = component.verifyOnboardingFirstBet(null);
    expect(check).toBe(null);
  });

  it("verify onboarding FirstBet", () => 
  {
    component.onBoardingFirstBet= FIRST_BET_PLACEMENT_MOCK_VALUES;
    component.verifyOnboardingFirstBet(FIRST_BET_PLACEMENT_MOCK_VALUES);
    expect(component.onBoardingFirstBet.displayFrom).toBeDefined();
  });

  it("save onboarding FirstBet data", () => {
    component.onBoardingFirstBet.createdAt='test';
    apiService.firstBetPlacementService().updateFirstBet.and.returnValue(of({ body: component.onBoardingFirstBet }))
    component.actionsHandler('save');
    expect(component.onBoardingFirstBet).toBeDefined();
  });



  it("revert onboarding FirstBet data", () => {
    apiService.firstBetPlacementService().saveFirstBet.and.returnValue(of(component.onBoardingFirstBet))
    component.actionsHandler('revert');
    expect(component.onBoardingFirstBet.moduleName).toEqual(undefined);
  });

  it("remove onboarding FirstBet data", () => {
    component['bannerIconUpload'] = { nativeElement: { value: '' } };
    apiService.firstBetPlacementService().removeFirstBetBulbIcon.and.returnValue(of({ body: component.onBoardingFirstBet }))
    component.removeBannerIcon();
    expect(component.onBoardingFirstBet.moduleName).toEqual('test');
  });

  it("remove onboarding FirstBet data error", () => {
    component['bannerIconUpload'] = { nativeElement: { value: '' } };
    apiService.firstBetPlacementService().removeFirstBetBulbIcon.and.returnValue(throwError({ error: { message: '' } }))
    component.removeBannerIcon();
    expect(component.onBoardingFirstBet.moduleName).toEqual('test');
  });


  it("get upload Button Name", () => {
    const data = component.getButtonName('test');
    expect(data).toEqual('Change File');
    const dataUpload = component.getButtonName('');
    expect(dataUpload).toEqual('Upload File');
  });


  it("get input", () => {
    component.inputLimit = { nativeElement: { value: '111' } };
    component.input();
    expect(component.inputLimit.nativeElement).toBeDefined();
  });

  it("get input 2 digits", () => {
    component.inputLimit = { nativeElement: { value: '11' } };
    component.input();
    expect(component.inputLimit.nativeElement).toBeDefined();
  });

  it("upload image input", () => {
    component.onBoardingFirstBet.id = ''
    const event = { target: { files: [{ type: 'image/png' }] } };
    component.prepareToUploadFile(event);

    expect(component.uploadBannerIcon).toBeDefined();

  });

  it("upload image input error postFirstBetBulbIcon", () => {
    component.onBoardingFirstBet.id = '111'
    apiService.firstBetPlacementService().postFirstBetBulbIcon.and.returnValue(throwError(new HttpErrorResponse({ error: { message: '401' } })));
    
    const event = { target: { files: [{ type: 'image/png' }] } };
    component.prepareToUploadFile(event);

    expect(component.uploadBannerIcon).toBeDefined();

  });

  it("upload image input", () => {
    component.onBoardingFirstBet.id = '111'
    const event = { target: { files: [{ type: 'image/png' }] } };
    component.prepareToUploadFile(event);

    expect(component.uploadBannerIcon).toBeDefined();

  });

  it("upload unsupported image input", () => {
    const event = { target: { files: [{ type: 'image/pn' }] } };
    component['bannerIconUpload']={nativeElement:{
      click: jasmine.createSpy('click')}
    };
    component.handleUploadImageClick();
    component.prepareToUploadFile(event);

    expect(component.uploadBannerIcon).toBeUndefined();

  });

  it("edit onboarding FirstBet data", () => {
    component.actionsHandler('edit');
    expect(component.onBoardingFirstBet.moduleName).toEqual('test');
  });

  it("handle Date Update", () => {
    component.handleDateUpdate({ startDate: '12/2/11', endDate: '3/4/11' });
    expect(component.onBoardingFirstBet.displayFrom).toEqual('2011-12-01T18:30:00.000Z');
  });

  it("update First bet Description with homepage", () => {
    component.firstBetform = new FormGroup({});
    component.firstBetform.addControl('homePageDesc', new FormControl('homePageDesc'));
    component.updateFirstbetDescription('test label', 'homePage.description', 'homePageDesc', '');
    expect(component.onBoardingFirstBet.homePage.description).toEqual('test label');
  });

  
  it("on End Date Update", () => {
    component.onEndDateUpdate('3/4/11');
    expect(component.onBoardingFirstBet.displayTo).toEqual('3/4/11');
  });

  it("update First bet Description with place your bet details", () => {
    component.firstBetform = new FormGroup({ placeYourBetFormGroup: new FormBuilder().group({ placeYourBetDefaultDesc: new FormControl('') }) });
    // component.firstBetform.addControl('placeYourBetForm',formBuilder.group(new FormControl('placeYourBetDefaultDesc')));
    component.updateFirstbetDescription('test description', 'placeYourBet.defaultContent.description', 'placeYourBetDefaultDesc', 'placeYourBetFormGroup');
    expect(component.onBoardingFirstBet.placeYourBet.defaultContent.description).toEqual('test description');
  });

  it("save onboarding FirstBet data without createdAt", () => {
    component.onBoardingFirstBet.createdAt = null;
    component.uploadBannerIcon = 'test';
    apiService.firstBetPlacementService().saveFirstBet.and.returnValue(of({ body: component.onBoardingFirstBet }))
    //spyOn(dialogService,'showNotificationDialog').and.callThrough();
    component.actionsHandler('save');
    expect(component.onBoardingFirstBet).toBeDefined();
  });

  it("save onboarding FirstBet data without createdAt error scenario", () => {
    component.onBoardingFirstBet.createdAt = null;
    apiService.firstBetPlacementService().saveFirstBet.and.returnValue(throwError(new HttpErrorResponse({ error: { message: '401' } })));
    //}))
    // spyOn(dialogService,'showNotificationDialog').and.callThrough();
    component.actionsHandler('save');
    expect(component.onBoardingFirstBet).toBeDefined();
  });
});
