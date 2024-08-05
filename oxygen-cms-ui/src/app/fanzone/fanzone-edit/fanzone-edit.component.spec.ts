import { async } from '@angular/core/testing';
import { FANZONE_MOCK_DATA } from '../fanzone.mock';
import { of, throwError } from 'rxjs';

import { FanzoneEditComponent } from './fanzone-edit.component';
import { FANZONE } from '../constants/fanzone.constants';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';

describe('FanzoneEditComponent', () => {
  let component: FanzoneEditComponent;
  let route;
  let router;
  let dialogService;
  let fanzonesAPIService;
  let errorService;

  beforeEach(async(() => {
    route = {
      snapshot: {
        paramMap: { get: jasmine.createSpy('get').and.returnValue('12345') }
      }
    };
    router = {
      navigate: jasmine.createSpy('navigate'),
      url: '/racing-edp-markets/1',
      snapshot: { paramMap: { id: '' } }
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog')
    }
    fanzonesAPIService = {
      getFanzoneDetails: jasmine.createSpy('getFanzoneDetails').and.returnValue(of({
        body: FANZONE_MOCK_DATA
      })),
      updateFanzoneDetails: jasmine.createSpy('updateFanzoneDetails').and.returnValue(of({
        body: FANZONE_MOCK_DATA
      })),
      deleteFanzone: jasmine.createSpy('deleteFanzone').and.returnValue(of({
        body: FANZONE_MOCK_DATA
      }))
    };
    errorService = {
      emitError: jasmine.createSpy('emitError')
    };
    component = new FanzoneEditComponent(route, router, dialogService, fanzonesAPIService, errorService);

    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    } as any as ActionButtonsComponent;
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit', () => {
    component.form = {} as any;
    component.getFanzoneDetails = jasmine.createSpy('component.getFanzoneDetails');
    component.ngOnInit();
    expect(component.id).toBeDefined();
    expect(component.getFanzoneDetails).toHaveBeenCalled();
  });

  it('actionsHandler to remove fanzone', () => {
    component.deleteFanzone = jasmine.createSpy('component.deleteFanzone');
    component.actionsHandler('remove');
    expect(component.deleteFanzone).toHaveBeenCalled();
  });

  it('actionsHandler to save fanzone details', () => {
    component.updateFanzoneDetails = jasmine.createSpy('component.updateFanzoneDetails');
    component.actionsHandler('save');
    expect(component.updateFanzoneDetails).toHaveBeenCalled();
  });

  it('actionsHandler to revert fanzone details', () => {
    component.getFanzoneDetails = jasmine.createSpy('component.getFanzoneDetails');
    component.actionsHandler('revert');
    expect(component.getFanzoneDetails).toHaveBeenCalled();
  });

  it('actionsHandler to console fanzone details', () => {
    spyOn(console, 'error');
    component.actionsHandler('');
    expect(console.error).toHaveBeenCalled();
  });

  it('should handle if getFanzoneDetails preference API returns valid response', () => {
    component.generateForm = jasmine.createSpy('component.generateForm');
    fanzonesAPIService.getFanzoneDetails = jasmine.createSpy('getFanzoneDetails').and.returnValue(of({ body: FANZONE }));
    component.getFanzoneDetails('');
    expect(component.fanzone).toEqual(FANZONE);
    expect(component.isReady).toBeTrue();
    expect(component.generateForm).toHaveBeenCalled();
  });

  it('should handle if getFanzoneDetails preference API returns valid response', () => {
    spyOn(console, 'error');
    fanzonesAPIService.getFanzoneDetails = jasmine.createSpy('getFanzoneDetails').and.returnValue(throwError({ error: '403' }));
    component.getFanzoneDetails('');
    expect(console.error).toHaveBeenCalled();
  });

  it('should handle if update preference API returns valid response', () => {
    component.actionButtons.extendCollection = jasmine.createSpy('component.actionButtons.extendCollection');
    fanzonesAPIService.updateFanzoneDetails = jasmine.createSpy('updateFanzoneDetails').and.returnValue(of({ body: FANZONE }));
    component.updateFanzoneDetails('', FANZONE as any);
    expect(component.fanzone).toEqual(FANZONE);
    expect(component.actionButtons.extendCollection).toHaveBeenCalled();
    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
      title: 'Fanzone Saved'
    });
  });

  it('should handle if update preference API returns error', () => {
    fanzonesAPIService.updateFanzoneDetails = jasmine.createSpy('updateFanzoneDetails').and.returnValue(throwError({ error: '403' }));
    component.updateFanzoneDetails('', FANZONE_MOCK_DATA as any);
    expect(errorService.emitError).toHaveBeenCalled();
  });

  it('should handle if delete preference API returns valid response', () => {
    fanzonesAPIService.deleteFanzone = jasmine.createSpy('deleteFanzone').and.returnValue(of({}));
    component.deleteFanzone('');

    expect(router.navigate).toHaveBeenCalled();
  });

  it('should handle if delete preference API returns error', () => {
    spyOn(console, 'error');
    fanzonesAPIService.deleteFanzone = jasmine.createSpy('deleteFanzone').and.returnValue(throwError({ error: '403' }));
    component.deleteFanzone('');
    expect(console.error).toHaveBeenCalled();
  });

  it('should fetch fanzone details based on id', () => {
    spyOn(component as any, 'getFanzoneDetails');
    component.ngOnInit();
    expect(component.id).toBeDefined();
    expect(component['getFanzoneDetails']).toHaveBeenCalled();
  });

  it('generateForm', () => {
    component.fanzone = FANZONE;
    component.form = {} as any;
    component.generateForm();
    expect(component.form).toBeDefined();
  });

  it('validationHandler -> should return true if form is valid', () => {
    component.form = { valid: true } as any;
    const isValid = component.validationHandler();
    expect(isValid).toBe(false);
  });

  it('validationHandler -> should return false if form is invalid', () => {
    component.form = { valid: false } as any;
    const isInValid = component.validationHandler();
    expect(isInValid).toBe(false);
  });
});
