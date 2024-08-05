import { async } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import { FZPreferences, FZPreferencesWithData, FZPreferencesWithInvalidData } from '@app/fanzone/fanzone.mock';
import { FanzonePreferenceCentreComponent } from './fanzone-preference-centre.component';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';


describe('FanzonePreferenceCentreComponent', () => {
  let component: FanzonePreferenceCentreComponent;
  let dialogService;
  let brandService;
  let fanzonesAPIService;
  let errorService;
  let actionButtons: ActionButtonsComponent;

  beforeEach(async(() => {
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
    };
    brandService = {
      brand: 'bma'
    };
    fanzonesAPIService = {
      getFanzonePreferences: jasmine.createSpy('getFanzonePreferences').and.returnValue(of({})),
      saveFanzonePreferences: jasmine.createSpy('saveFanzonePreferences').and.returnValue(of({}))
    };
    errorService = {
      emitError: jasmine.createSpy('emitError')
    };
    component = new FanzonePreferenceCentreComponent(dialogService, brandService, fanzonesAPIService, errorService);
    actionButtons = jasmine.createSpyObj(ActionButtonsComponent, ['extendCollection']);
    component.actionButtons = actionButtons;
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should assign default value to fanzonePreferences', () => {
    component.ngOnInit();

    expect(component.fanzonePreferences).toEqual(FZPreferences);
  });

  it('should assign fanzonePreferences as null if api returns null', () => {
    fanzonesAPIService.getFanzonePreferences = jasmine.createSpy('getFanzonePreferences').and.returnValue(of({ body: FZPreferencesWithData }));
    component.ngOnInit();

    expect(component.fanzonePreferences).toEqual(FZPreferencesWithData);
  });

  it('should return preference centre keys', () => {
    component.ngOnInit();
    const result = component.pcKeys;

    expect(result).toBeDefined();
  });

  it('should add preferences', () => {
    component.ngOnInit();
    component.addPreference({ name: 'test', key: '123' });

    expect(component.fanzonePreferences.pcKeys).toEqual([{ name: '', key: '' }, { name: '', key: '' }]);
  });

  it('should delete preferences if pc keys are more then 1', () => {
    component.ngOnInit();
    component.addPreference({ name: 'test', key: '123' });
    component.addPreference({ name: 'test2', key: '1234' });
    component.deletePreference(1);

    expect(component.fanzonePreferences.pcKeys.length).toEqual(2);
  });

  it('should not delete preferences if pc keys is 1', () => {
    component.ngOnInit();
    component.deletePreference(1);

    expect(component.fanzonePreferences.pcKeys.length).toEqual(1);
  });

  it('should save fanzone preferences', () => {
    fanzonesAPIService.getFanzonePreferences = jasmine.createSpy('getFanzonePreferences').and.returnValue(of({ body: FZPreferencesWithData }));
    component.ngOnInit();
    component.actionsHandler('save');

    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Fanzone SYC is Stored'
    });
  });

  it('should handle if save preference API returns error', () => {
    fanzonesAPIService.saveFanzonePreferences = jasmine.createSpy('saveFanzonePreferences').and.returnValue(throwError({ error: '403' }));
    component.ngOnInit();
    component.actionsHandler('save');

    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Fanzone SYC is Stored'
    });
    expect(errorService.emitError).toHaveBeenCalled();
  });

  it('should revert fanzone preferences', () => {
    component.ngOnInit();
    component.actionsHandler('revert');

    expect(component.isReady).toBeTrue();
  });

  it('should handle wrong action i.e other then save and revert', () => {
    component.ngOnInit();
    component.actionsHandler('revert2');

    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Fanzone SYC is Stored'
    });
  });

  it('should return true if form is valid', () => {
    fanzonesAPIService.getFanzonePreferences = jasmine.createSpy('getFanzonePreferences').and.returnValue(of({ body: FZPreferencesWithData }));
    component.ngOnInit();
    const isValid = component.validationHandler();

    expect(isValid).toBeTrue();
  })

  it('should return false if form is invalid', () => {
    fanzonesAPIService.getFanzonePreferences = jasmine.createSpy('getFanzonePreferences').and.returnValue(of({ body: FZPreferencesWithInvalidData }));
    component.ngOnInit();
    const isValid = component.validationHandler();

    expect(isValid).toBeFalse();
  })

});
