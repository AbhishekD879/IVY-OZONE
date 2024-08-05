import { async } from '@angular/core/testing';
import { FanzoneNewSeasonComponent } from './fanzone-new-season.component';
import { of } from 'rxjs';
import { FZ_NEW_SEASON_CONST } from '../constants/fanzone.constants';

describe('FanzoneNewSeasonComponent', () => {
  let component: FanzoneNewSeasonComponent;
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
      saveFanzoneNewSeasonData: jasmine.createSpy('saveFanzoneNewSeasonData').and.returnValue(of({
        body: FZ_NEW_SEASON_CONST
      })),
      deleteFanzone: jasmine.createSpy('deleteFanzone').and.returnValue(of({})),
      getFanzoneNewSeasonDetails: jasmine.createSpy('getFanzoneNewSeasonDetails').and.returnValue(of({ body: {} })),
    };
    errorService = {
      emitError: jasmine.createSpy('emitError').and.returnValue(of({}))
    };
    component = new FanzoneNewSeasonComponent(dialogService, brandService, fanzonesAPIService, errorService);
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    } as any;
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call ngOnInit', () => {
    spyOn(component, 'getFanzoneNewSeasonDetails');
    component.ngOnInit();
  });

  it('should call saveFanzoneNewSeasonData to save the list of fanzoneNewSeason', () => {
    spyOn(component, 'getFanzoneNewSeasonDetails');
    component.ngOnInit();

    component.fanzoneNewSeason.id = ''
    fanzonesAPIService.saveFanzoneNewSeasonData.subscribe = jasmine.createSpy('saveFanzoneNewSeasonData').and.returnValue({});
    component.saveFanzoneNewSeasonData();
    expect(component.fanzoneNewSeason).toHaveBeenCalled;
  });

  it('should call getFanzoneNewSeasonDetails to get the list of fanzoneNewSeason with out response', () => {
    spyOn(component, 'getFanzoneNewSeasonDetails');
    fanzonesAPIService.getFanzoneNewSeasonDetails = jasmine.createSpy('getFanzoneNewSeasonDetails').and.returnValue(of({}))
    spyOn(component, 'generateForm');
    component.getFanzoneNewSeasonDetails();
    expect(component.isReady).toBeFalse();
  });

  it('should call getFanzoneNewSeasonDetails to get the list of fanzoneNewSeasonwith empty response', () => {
    spyOn(component, 'getFanzoneNewSeasonDetails');
    fanzonesAPIService.getFanzoneNewSeasonDetails = jasmine.createSpy('getFanzoneNewSeasonDetails').and.returnValue(of({ body: {} }));
    spyOn(component, 'generateForm');
    component.getFanzoneNewSeasonDetails();
    expect(component.isReady).toBeFalsy();
  });

  it('should call getFanzoneNewSeasonDetails to get the list of fanzoneNewSeason with response', () => {
    spyOn(component, 'getFanzoneNewSeasonDetails');
    fanzonesAPIService.getFanzoneNewSeasonDetails = jasmine.createSpy('getFanzoneNewSeasonDetails').and.returnValue(of({ body: { id: 1 } }));
    spyOn(component, 'generateForm');
    component.getFanzoneNewSeasonDetails();
    expect(component.isReady).toBeFalsy();
  });


  it('should call actionsHandler to call saveFanzoneNewSeasonData', () => {
    let event = 'save';
    spyOn(component, 'actionsHandler');
    component.actionsHandler(event);
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Fz FZ_NEW_SEASON_CONST is Stored'
    });
  });

  it('should call actionsHandler', () => {
    let event = '';
    component.actionsHandler(event);
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Fz FZ_NEW_SEASON_CONST is Stored'
    });
  });

  it('should call actionsHandler to call getFanzoneNewSeasonDetails', () => {
    spyOn(component, 'getFanzoneNewSeasonDetails');
    let event = 'revert';
    component.actionsHandler(event);
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Fz FZ_NEW_SEASON_CONST is Stored'
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
