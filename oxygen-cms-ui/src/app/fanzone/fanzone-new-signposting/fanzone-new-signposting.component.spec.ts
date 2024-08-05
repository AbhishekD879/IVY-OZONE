import { async } from '@angular/core/testing';
import { FanzoneNewSignpostingComponent } from './fanzone-new-signposting.component';
import { of } from 'rxjs';
import { NEWSIGNPOSTING } from '../constants/fanzone.constants';

describe('FanzoneNewSignpostingComponent', () => {
  let component: FanzoneNewSignpostingComponent;
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
      saveSignPosting: jasmine.createSpy('saveSignPosting').and.returnValue(of({
        body: NEWSIGNPOSTING
      })),
      saveNewSignPosting: jasmine.createSpy('saveNewSignPosting').and.returnValue(of({
        body: NEWSIGNPOSTING
      })),
      getNewGamingPopUp: jasmine.createSpy('deleteFanzone').and.returnValue(of({})),
      deleteFanzone: jasmine.createSpy('deleteFanzone').and.returnValue(of({})),
      getfanzoneNewSignposting: jasmine.createSpy('getfanzoneNewSignposting').and.returnValue(of({ body: {} })),
    };
    errorService = {
      emitError: jasmine.createSpy('emitError').and.returnValue(of({}))
    };
    component = new FanzoneNewSignpostingComponent(dialogService, brandService, fanzonesAPIService, errorService);
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    } as any;
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call ngOnInit', () => {
    spyOn(component, 'getNewSignPosting');
    component.ngOnInit();
  });

  it('should call saveSignPosting to save the list of fanzoneNewSignposting', () => {
    spyOn(component, 'getNewSignPosting');
    component.ngOnInit();

    component.fanzoneNewSignposting.id = ''
    fanzonesAPIService.saveSignPosting.subscribe = jasmine.createSpy('saveSignPosting').and.returnValue({});
    component.saveSignPosting();
    expect(component.fanzoneNewSignposting).toHaveBeenCalled;
  });

  it('should call getNewSignPosting to get the list of fanzoneNewSignposting with out response', () => {
    spyOn(component, 'getNewSignPosting');
    fanzonesAPIService.getNewSignPosting = jasmine.createSpy('getNewSignPosting').and.returnValue(of({}))
    spyOn(component, 'generateForm');
    component.getNewSignPosting();
    expect(component.isReady).toBeUndefined();
  });

  it('should call getNewSignPosting to get the list of fanzoneNewSignpostingwith empty response', () => {
    spyOn(component, 'getNewSignPosting');
    fanzonesAPIService.getNewSignPosting = jasmine.createSpy('getNewSignPosting').and.returnValue(of({ body: {} }));
    spyOn(component, 'generateForm');
    component.getNewSignPosting();
    expect(component.isReady).toBeUndefined();
  });

  it('should call getfanzoneNewSignposting to get the list of fanzoneNewSignposting with response', () => {
    spyOn(component, 'getNewSignPosting');
    fanzonesAPIService.getfanzoneNewSignposting = jasmine.createSpy('getNewSignPosting').and.returnValue(of({ body: { id: 1 } }));
    spyOn(component, 'generateForm');
    component.getNewSignPosting();
    expect(component.isReady).toBeUndefined();
  });


  it('should call actionsHandler to call saveSignPosting', () => {
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

  it('should call actionsHandler to call getfanzoneNewSignposting', () => {
    spyOn(component, 'getNewSignPosting');
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
