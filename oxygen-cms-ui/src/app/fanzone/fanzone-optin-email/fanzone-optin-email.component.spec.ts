import { async } from '@angular/core/testing';
import { FanzoneOptinEmailComponent } from './fanzone-optin-email.component';
import { of } from 'rxjs';
import { FANZONE_OPTIN_EMAIL } from '../constants/fanzone.constants';

describe('FanzoneOptinEmailComponent', () => {
  let component: FanzoneOptinEmailComponent;
  let dialogService;
  let brandService;
  let fanzonesAPIService;
  let errorService;

  beforeEach(async(() => {
    brandService = {
      brand: ''
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and
        .callFake(({ yesCallback }) => yesCallback())
    };
    fanzonesAPIService = {
      saveOptinEmail: jasmine.createSpy('saveOptinEmail').and.returnValue(of({
        body: FANZONE_OPTIN_EMAIL
      })),
      deleteFanzone: jasmine.createSpy('deleteFanzone').and.returnValue(of({})),
      getOptinEmail: jasmine.createSpy('getOptinEmail').and.returnValue(of({ body: {} })),
    };
    errorService = {
      emitError: jasmine.createSpy('emitError').and.returnValue(of({}))
    };
    component = new FanzoneOptinEmailComponent( brandService, fanzonesAPIService, dialogService, errorService);
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    } as any;
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call ngOnInit', () => {
    spyOn(component, 'getOptinEmail');
    component.ngOnInit();
  });

  it('should call saveOptinEmail to save the list of fanzoneOptinEmail', () => {
    spyOn(component, 'getOptinEmail');
    component.ngOnInit();

    component.fanzoneOptinEmail.id = ''
    fanzonesAPIService.saveOptinEmail.subscribe = jasmine.createSpy('saveOptinEmail').and.returnValue({});
    component.saveOptinEmail();
    expect(component.fanzoneOptinEmail).toHaveBeenCalled;
  });

  it('should call getOptinEmail to get the list of fanzoneOptinEmail with out response', () => {
    spyOn(component, 'getOptinEmail');
    fanzonesAPIService.getOptinEmail = jasmine.createSpy('getOptinEmail').and.returnValue(of({}))
    spyOn(component, 'generateForm');
    component.getOptinEmail();
    expect(component.isReady).toBeUndefined();
  });

  it('should call getOptinEmail to get the list of fanzoneOptinEmailwith empty response', () => {
    spyOn(component, 'getOptinEmail');
    fanzonesAPIService.getOptinEmail = jasmine.createSpy('getOptinEmail').and.returnValue(of({ body: {} }));
    spyOn(component, 'generateForm');
    component.getOptinEmail();
    expect(component.isReady).toBeUndefined();
  });

  it('should call getOptinEmail to get the list of fanzoneOptinEmail with response', () => {
    spyOn(component, 'getOptinEmail');
    fanzonesAPIService.getOptinEmail = jasmine.createSpy('getOptinEmail').and.returnValue(of({ body: { id: 1 } }));
    spyOn(component, 'generateForm');
    component.getOptinEmail();
    expect(component.isReady).toBeUndefined();
  });


  it('should call actionsHandler to call saveOptinEmail', () => {
    let event = 'save';
    spyOn(component, 'actionsHandler');
    component.actionsHandler(event);
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Fz FANZONE_OPTIN_EMAIL is Stored'
    });
  });

  it('should call actionsHandler', () => {
    let event = '';
    component.actionsHandler(event);
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Fz FANZONE_OPTIN_EMAIL is Stored'
    });
  });

  it('should call actionsHandler to call getOptinEmail', () => {
    spyOn(component, 'getOptinEmail');
    let event = 'revert';
    component.actionsHandler(event);
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Fz FANZONE_OPTIN_EMAIL is Stored'
    });
  });

  it('validationHandler -> should return true if form is valid', () => {
    component.form = { valid: true } as any;
    const isValid = component.validationHandler();
    expect(isValid).toBe(true);
  });

  it('validationHandler -> should return false if form is invalid', () => {
    component.form = { valid: false } as any;
    const isInValid = component.validationHandler();
    expect(isInValid).toBe(false);
  });
});
