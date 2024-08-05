import { async } from '@angular/core/testing';
import { FanzoneCreateComponent } from './fanzone-create.component';
import { FANZONE } from '@app/fanzone/constants/fanzone.constants';
import { of, throwError } from 'rxjs';

describe('FanzoneCreateComponent', () => {
  let component: FanzoneCreateComponent;
  let router;
  let dialogService;
  let brandService;
  let fanzonesAPIService;
  let errorService;

  beforeEach(async(() => {
    router = {
      navigate: jasmine.createSpy('navigate'),
      url: '/racing-edp-markets/1'
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog').and.callFake(({ title, message, closeCallback }) => {
        closeCallback();
      })
    };
    brandService = {
      brand: jasmine.createSpy('brand').and.returnValue('bma')
    };
    fanzonesAPIService = {
      createFanzone: jasmine.createSpy('createFanzone').and.returnValue(of({
        body: FANZONE
      }))
    };
    errorService = {
      emitError: jasmine.createSpy('emitError')
    };
    component = new FanzoneCreateComponent(router, dialogService, brandService, fanzonesAPIService, errorService);

  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit form', () => {
    component.ngOnInit();
    expect(component.form).toBeDefined();
  });

  it('should handle if save preference API returns error', () => {
    fanzonesAPIService.createFanzone = jasmine.createSpy('createFanzone').and.returnValue(throwError({ error: '403' }));
    component.createFanzone();
    expect(errorService.emitError).toHaveBeenCalled();
  });

  it('should create finishCampaignCreation based on brand', () => {
    spyOn(component as any, 'finishCampaignCreation');
    component.createFanzone();
    expect(fanzonesAPIService.createFanzone).toHaveBeenCalled();
    expect(component['finishCampaignCreation']).toHaveBeenCalled();
  });

  it('should create fanzones based on brand', () => {
    brandService.brand = 'bma';
    const fz = {
      ...FANZONE,
      brand: 'bma'
    };
    component.generateForm = jasmine.createSpy('generateForm');
    component.ngOnInit();
    expect(component.fanzone).toEqual(fz);
    expect(component.generateForm).toHaveBeenCalled();
  });

  it('show dialog when fanzone campaign creation is done', () => {
    component.finishCampaignCreation('1');
    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Fanzone is Created and Stored. Continue to Configure',
      closeCallback: jasmine.any(Function)
    });
  });

  it('isValidModel -> should return true if form is valid', () => {
    component.form = { valid: true } as any;
    const isValid = component.isValidModel();
    expect(isValid).toBe(false);
  });

  it('isInValidModel -> should return false if form is invalid', () => {
    component.form = { valid: false } as any;
    const isInValid = component.isValidModel();
    expect(isInValid).toBe(false);
  });
});
