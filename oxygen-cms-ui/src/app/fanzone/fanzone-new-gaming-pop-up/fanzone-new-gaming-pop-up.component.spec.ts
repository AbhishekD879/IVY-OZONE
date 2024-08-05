import { async } from '@angular/core/testing';
import { FanzoneNewGamingPopUpComponent } from './fanzone-new-gaming-pop-up.component';
import { of } from 'rxjs';
import { FZ_POPUP } from '../constants/fanzone.constants';

describe('FanzoneNewGamingPopUpComponent', () => {
  let component: FanzoneNewGamingPopUpComponent;
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
      saveNewGamingPopUp: jasmine.createSpy('saveNewGamingPopUp').and.returnValue(of({
        body: FZ_POPUP
      })),
      getNewGamingPopUp: jasmine.createSpy('deleteFanzone').and.returnValue(of({})),
      deleteFanzone: jasmine.createSpy('deleteFanzone').and.returnValue(of({})),
      getfanzoneNewGamingPopUp: jasmine.createSpy('getfanzoneNewGamingPopUp').and.returnValue(of({ body: {} })),
    };
    errorService = {
      emitError: jasmine.createSpy('emitError').and.returnValue(of({}))
    };
    component = new FanzoneNewGamingPopUpComponent(dialogService, brandService, fanzonesAPIService, errorService);
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    } as any;
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call ngOnInit', () => {
    spyOn(component, 'getFzPopUp');
    component.ngOnInit();
  });

  it('should call saveFzPopUp to save the list of fanzoneNewGamingPopUp', () => {
    spyOn(component, 'saveFzPopUp');
    component.ngOnInit();

    component.fanzoneNewGamingPopUp.id = ''
    fanzonesAPIService.saveNewGamingPopUp.subscribe = jasmine.createSpy('saveNewGamingPopUp').and.returnValue({});
    component.saveFzPopUp();
    expect(component.fanzoneNewGamingPopUp).toHaveBeenCalled;
  });

  it('should call getFzPopUp to get the list of fanzoneNewGamingPopUp with out response', () => {
    spyOn(component, 'getFzPopUp');
    fanzonesAPIService.getNewSignPosting = jasmine.createSpy('getFzPopUp').and.returnValue(of({}))
    spyOn(component, 'generateForm');
    component.getFzPopUp();
    expect(component.isReady).toBeUndefined();
  });

  it('should call getFzPopUp to get the list of fanzoneNewGamingPopUpwith empty response', () => {
    spyOn(component, 'getFzPopUp');
    fanzonesAPIService.getNewSignPosting = jasmine.createSpy('getFzPopUp').and.returnValue(of({ body: {} }));
    spyOn(component, 'generateForm');
    component.getFzPopUp();
    expect(component.isReady).toBeUndefined();
  });

  it('should call getfanzoneNewGamingPopUp to get the list of fanzoneNewGamingPopUp with response', () => {
    spyOn(component, 'getFzPopUp');
    fanzonesAPIService.getfanzoneNewGamingPopUp = jasmine.createSpy('getNewSignPosting').and.returnValue(of({ body: { id: 1 } }));
    spyOn(component, 'generateForm');
    component.getFzPopUp();
    expect(component.isReady).toBeUndefined();
  });


  it('should call actionsHandler to call saveFzPopUp', () => {
    let event = 'save';
    spyOn(component, 'actionsHandler');
    component.actionsHandler(event);
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Fz NewSignPosting is Stored'
    });
  });

  it('should call actionsHandler', () => {
    let event = '';
    component.actionsHandler(event);
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Fz NewSignPosting is Stored'
    });
  });

  it('should call actionsHandler to call getfanzoneNewGamingPopUp', () => {
    let event = 'revert';
    component.actionsHandler(event);
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Fz NewSignPosting is Stored'
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
