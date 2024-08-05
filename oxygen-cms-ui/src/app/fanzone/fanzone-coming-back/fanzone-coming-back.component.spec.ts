import { async } from '@angular/core/testing';
import { FanzoneComingBackComponent } from './fanzone-coming-back.component';
import { of } from 'rxjs';
import { FZ_COMING_BACK_CONST } from '../constants/fanzone.constants';

describe('FanzoneComingBackComponent', () => {
  let component: FanzoneComingBackComponent;
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
      saveFanzoneComingBackData: jasmine.createSpy('saveFanzoneComingBackData').and.returnValue(of({
        body: FZ_COMING_BACK_CONST
      })),
      getFanzoneComingBackDetails: jasmine.createSpy('getFanzoneComingBackDetails').and.returnValue(of({ body: {} })),
    };
    errorService = {
      emitError: jasmine.createSpy('emitError').and.returnValue(of({}))
    };
    component = new FanzoneComingBackComponent(dialogService, brandService, fanzonesAPIService, errorService);
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    } as any;
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call ngOnInit', () => {
    spyOn(component, 'getFanzoneComingBackDetails');
    component.ngOnInit();
  });

  it('should call saveFanzoneComingBackData to save the list of fanzoneComingBack', () => {
    spyOn(component, 'getFanzoneComingBackDetails');
    component.ngOnInit();

    component.fanzoneComingBack.id = ''
    fanzonesAPIService.saveFanzoneComingBackData.subscribe = jasmine.createSpy('saveFanzoneComingBackData').and.returnValue({});
    component.saveFanzoneComingBackData();
    expect(component.fanzoneComingBack).toHaveBeenCalled;
  });

  it('should call getFanzoneComingBackDetails to get the list of fanzoneComingBack with out response', () => {
    spyOn(component, 'getFanzoneComingBackDetails');
    fanzonesAPIService.getFanzoneComingBackDetails = jasmine.createSpy('getFanzoneComingBackDetails').and.returnValue(of({}))
    spyOn(component, 'generateForm');
    component.getFanzoneComingBackDetails();
    expect(component.isReady).toBeFalse();
  });

  it('should call getFanzoneComingBackDetails to get the list of fanzoneComingBackwith empty response', () => {
    spyOn(component, 'getFanzoneComingBackDetails');
    fanzonesAPIService.getFanzoneComingBackDetails = jasmine.createSpy('getFanzoneComingBackDetails').and.returnValue(of({ body: {} }));
    spyOn(component, 'generateForm');
    component.getFanzoneComingBackDetails();
    expect(component.isReady).toBeFalsy();
  });

  it('should call getFanzoneComingBackDetails to get the list of fanzoneComingBack with response', () => {
    spyOn(component, 'getFanzoneComingBackDetails');
    fanzonesAPIService.getFanzoneComingBackDetails = jasmine.createSpy('getFanzoneComingBackDetails').and.returnValue(of({ body: { id: 1 } }));
    spyOn(component, 'generateForm');
    component.getFanzoneComingBackDetails();
    expect(component.isReady).toBeFalsy();
  });


  it('should call actionsHandler to call saveFanzoneComingBackData', () => {
    let event = 'save';
    spyOn(component, 'actionsHandler');
    component.actionsHandler(event);
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Fz FZ_COMING_BACK_CONST is Stored'
    });
  });

  it('should call actionsHandler', () => {
    let event = '';
    component.actionsHandler(event);
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Fz FZ_COMING_BACK_CONST is Stored'
    });
  });

  it('should call actionsHandler to call getFanzoneComingBackDetails', () => {
    spyOn(component, 'getFanzoneComingBackDetails');
    let event = 'revert';
    component.actionsHandler(event);
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Fz FZ_COMING_BACK_CONST is Stored'
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
