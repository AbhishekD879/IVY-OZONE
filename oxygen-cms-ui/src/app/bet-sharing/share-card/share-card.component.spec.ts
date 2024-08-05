import { ShareCardComponent } from './share-card.component';
import { of, throwError } from 'rxjs';
import { BET_SHARE_MOCK_VALUES } from './share-card.mock';
import { HttpErrorResponse } from '@angular/common/http';
import { FormControl, FormGroup } from '@angular/forms';

describe('ShareCardComponent', () => {
  let component: ShareCardComponent;
  let apiService, dialogService, brandService;

  beforeEach(() =>{
    apiService = {
      betSharingApiService : jasmine.createSpy('betSharingApiService').and.returnValue({
        getDetailsByBrand: jasmine.createSpy('').and.returnValue(of({ body: {} })),
        saveCMSBetShareData: jasmine.createSpy('').and.returnValue(of({})),
        updateCMSBetShareData: jasmine.createSpy('').and.returnValue(of({ }))
      })
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog')
    };
    brandService ={
      brand: "bma"
    };
    component = new ShareCardComponent(apiService, dialogService, brandService);
    component.shareCardFormData = BET_SHARE_MOCK_VALUES;
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    } as any;
    spyOn(component, 'createFormGroup');
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it("ngOnInit should initialize data is empty", () => {
    apiService.betSharingApiService().getDetailsByBrand.and.returnValue(of({}));
    component.ngOnInit();
    expect(component.shareCardFormData).toBeDefined();
  });

  it("ngOnInit should initialize data", () => {
    apiService.betSharingApiService().getDetailsByBrand.and.returnValue(of({ body: component.shareCardFormData }))
    component.ngOnInit();
    expect(component.shareCardFormData.shareCardImageFileName).toEqual('test');
  });

  it("ngOnInit with service error 404", () => {
    apiService.betSharingApiService().getDetailsByBrand.and.returnValue(throwError({ status: 404 }))
    component.ngOnInit();
    expect(component.shareCardFormData.shareCardImageFileName).toEqual('');
  });

  it("ngOnInit with service error 401", () => {
    apiService.betSharingApiService().getDetailsByBrand.and.returnValue(throwError({ error: { message: '401' } }))
    component.ngOnInit();
    expect(component.shareCardFormData.shareCardImageFileName).toEqual('test');
  });

  it("verify shareCardFormData null", () => {
    const check = component.verifyBetSharingData(null);
    expect(check).toBe(false);
  });

  it("verify shareCardFormData", () => 
  {
    component.shareCardFormData= BET_SHARE_MOCK_VALUES;
    component.verifyBetSharingData(BET_SHARE_MOCK_VALUES);
    expect(component.shareCardFormData.shareCardImageFileName).toBeDefined();
  });

  it("save shareCardFormData", () => {
    component.shareCardFormData.createdAt='test';
    apiService.betSharingApiService().updateCMSBetShareData.and.returnValue(of({ body: component.shareCardFormData }))
    component.actionsHandler('save');
    expect(component.shareCardFormData).toBeDefined();
  });

  it("revert shareCardFormData", () => {
    apiService.betSharingApiService().saveCMSBetShareData.and.returnValue(of(component.shareCardFormData))
    component.actionsHandler('revert');
    expect(component.shareCardFormData.shareCardImageFileName).toEqual(undefined);
  });

  it("edit shareCardFormData", () => {
    component.actionsHandler('edit');
    expect(component.shareCardFormData.shareCardImageFileName).toEqual('test');
  });

  it("save shareCardFormData data without createdAt", () => {
    component.shareCardFormData.createdAt = null;
    apiService.betSharingApiService().saveCMSBetShareData.and.returnValue(of({ body: component.shareCardFormData }))
    //spyOn(dialogService,'showNotificationDialog').and.callThrough();
    component.actionsHandler('save');
    expect(component.shareCardFormData).toBeDefined();
  });

  it("save shareCardFormData data without createdAt error scenario", () => {
    component.shareCardFormData.createdAt = null;
    apiService.betSharingApiService().saveCMSBetShareData.and.returnValue(throwError(new HttpErrorResponse({ error: { message: '401' } })));
    //}))
    // spyOn(dialogService,'showNotificationDialog').and.callThrough();
    component.actionsHandler('save');
    expect(component.shareCardFormData).toBeDefined();
  });

    it("userPerferncesChange openBetControl", () => 
  {
    component.shareCardFormData.openBetControl = BET_SHARE_MOCK_VALUES.openBetControl;
    console.log('BET_SHARE_MOCK_VALUES',BET_SHARE_MOCK_VALUES['openBetControl']);
    component.shareCardFormGroup = new FormGroup({});
    component.shareCardFormGroup.addControl('openBetControl', new FormControl());
    component.userPerferncesChange('openBetControl');
    expect(component.openBetChecked).toBeDefined();
  });

  it("userPerferncesChange wonBetControl", () => 
  {
    component.shareCardFormData.wonBetControl = BET_SHARE_MOCK_VALUES['wonBetControl'];
    component.shareCardFormGroup = new FormGroup({});
    component.shareCardFormGroup.addControl('wonBetControl', new FormControl(BET_SHARE_MOCK_VALUES['wonBetControl']));
    component.userPerferncesChange('wonBetControl');
    expect(component.wonBetChecked).toBeDefined();
  });

  it("userPerferncesChange lostBetControl", () => 
  {
    component.shareCardFormData.lostBetControl = BET_SHARE_MOCK_VALUES['lostBetControl'];
    component.shareCardFormGroup = new FormGroup({});
    //component.shareCardFormGroup.setValue({...BET_SHARE_MOCK_VALUES});
    component.shareCardFormGroup.addControl('lostBetControl', new FormControl(BET_SHARE_MOCK_VALUES['lostBetControl']));
    component.userPerferncesChange('lostBetControl');
    expect(component.lostBetChecked).toBeDefined();
  });

  it("userPerferncesChange cashedOutBetControl", () => 
  {
    component.shareCardFormData.cashedOutBetControl = BET_SHARE_MOCK_VALUES['cashedOutBetControl'];
    component.shareCardFormGroup = new FormGroup({});
    component.shareCardFormGroup.addControl('cashedOutBetControl', new FormControl(BET_SHARE_MOCK_VALUES['cashedOutBetControl']));  
    component.userPerferncesChange('cashedOutBetControl');
    expect(component.cashedOutBetChecked).toBeDefined();
  });


});
