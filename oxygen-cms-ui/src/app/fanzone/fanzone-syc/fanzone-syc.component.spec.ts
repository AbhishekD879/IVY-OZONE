import { async } from '@angular/core/testing';
import { FanzoneSycComponent } from './fanzone-syc.component';
import { of, throwError } from 'rxjs';
import { SYC } from '../constants/fanzone.constants';
import { FZPreferencesWithData, FZPreferencesWithInvalidData } from '@app/fanzone/fanzone.mock';

describe('FanzoneSycComponent', () => {
  let component: FanzoneSycComponent;
  let brandService;
  let dialogService;
  let fanzonesAPIService;
  let errorService;

  beforeEach(async(() => {
    brandService = {
      brand: 'bma'
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and
        .callFake(({ title, message, yesCallback }) => yesCallback())
    };
    fanzonesAPIService = {
      getFanzonePreferences: jasmine.createSpy('getFanzonePreferences').and.returnValue(of({})),
      saveFanzoneSyc: jasmine.createSpy('saveFanzoneSyc').and.returnValue(of({
        body: SYC
      })),
      deleteFanzone: jasmine.createSpy('deleteFanzone').and.returnValue(of({})),
      getFanzoneSyc: jasmine.createSpy('getFanzoneSyc').and.returnValue(of({ body: {} }))
    };
    errorService = {
      emitError: jasmine.createSpy('emitError')
    };
    component = new FanzoneSycComponent(dialogService, brandService, fanzonesAPIService, errorService);
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    } as any;
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call ngOnInit', () => {
    spyOn(component, 'getFanzoneSyc');
    component.ngOnInit();
  });

  it('should call saveSYC to save the list of fanzoneSyc', () => {
    spyOn(component, 'getFanzoneSyc');
    component.ngOnInit();

    component.fanzoneSyc.id = '1'
    fanzonesAPIService.saveFanzoneSyc.subscribe = jasmine.createSpy('saveFanzoneSyc').and.returnValue({});
    component.saveSYC();
    expect(component.fanzoneSyc).toEqual(SYC);
  });

  it('should  handle if saveSYC API returns error', () => {
    spyOn(component, 'getFanzoneSyc');
    component.ngOnInit();
    component.fanzoneSyc.id = null;
    fanzonesAPIService.saveFanzoneSyc = jasmine.createSpy('saveFanzoneSyc').and.returnValue(throwError({ error: '401' }));
    component.saveSYC();
    expect(errorService.emitError).toHaveBeenCalled();
  });

  it('should call getFanzoneSyc to get the list of fanzoneSyc with out response', () => {
    fanzonesAPIService.getFanzoneSyc = jasmine.createSpy('getFanzoneSyc').and.returnValue(of({}))
    spyOn(component, 'generateForm');
    component.getFanzoneSyc();
    expect(component.isReady).toEqual(true);
  });

  it('should call getFanzoneSyc to get the list of fanzoneSycwith empty response', () => {
    fanzonesAPIService.getFanzoneSyc = jasmine.createSpy('getFanzoneSyc').and.returnValue(of({ body: {} }));
    spyOn(component, 'generateForm');
    component.getFanzoneSyc();
    expect(component.isReady).toEqual(true);
  });

  it('should call getFanzoneSyc to get the list of fanzoneSyc with response', () => {
    fanzonesAPIService.getFanzoneSyc = jasmine.createSpy('getFanzoneSyc').and.returnValue(of({ body: { id: 1 } }));
    spyOn(component, 'generateForm');
    component.getFanzoneSyc();
    expect(component.isReady).toEqual(true);
  });

  it('should handleDateUpdate', () => {
    spyOn(component, 'getFanzoneSyc');
    component.ngOnInit();
    let event = {
      startDate: '21-10-2022',
      endDate: '22-10-2022',
    };
    component.fanzoneSyc.seasonStartDate = '21-10-2022';
    component.fanzoneSyc.seasonEndDate = '22-10-2022';
    component.handleDateUpdate(event);
    expect(component.fanzoneSyc.seasonStartDate).toEqual('21-10-2022');
    expect(component.fanzoneSyc.seasonEndDate).toEqual('22-10-2022');
  });

  it('should call actionsHandler to call savesyc', () => {
    let event = 'save';
    spyOn(component, 'saveSYC');
    component.actionsHandler(event);
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Fanzone SYC is Stored'
    });
  });

  it('should call actionsHandler', () => {
    let event = '';
    component.actionsHandler(event);
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Fanzone SYC is Stored'
    });
  });

  it('should call actionsHandler to call getFanzoneSyc', () => {
    let event = 'revert';
    spyOn(component, 'getFanzoneSyc');
    component.actionsHandler(event);
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalledWith({
      title: 'Save Completed',
      message: 'Fanzone SYC is Stored'
    });
  });

  it('initialize the form', () => {
    spyOn(component, 'getFanzoneSyc');
    component.ngOnInit();
    component.generateForm();
    expect(component.form.get(component.fanzoneSyc.sycPopUpTitle)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.sycPopUpDescription)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.sycImage)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.okCTA)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.dontShowAgain)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.remindLater)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.remindLaterHideDays)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.sycTitle)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.sycDescription)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.sycLoginCTA)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.sycConfirmCTA)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.sycExitCTA)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.sycCancelCTA)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.sycThankYouTitle)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.sycConfirmTitle)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.sycNoTeamSelectionTitle)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.customTeamNameText)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.customTeamNameDescription)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.thankYouMsg)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.sycConfirmMsgMobile)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.sycConfirmMsgDesktop)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.sycPreLoginTeamSelectionMsg)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.sycPreLoginNoTeamSelectionMsg)).toEqual(null);
    expect(component.form.get(component.fanzoneSyc.changeTeamTimePeriodMsg)).toEqual(null);
  });

  it('should return true if form is valid', () => {
    fanzonesAPIService.getFanzonePreferences = jasmine.createSpy('getFanzonePreferences').and.returnValue(of({ body: FZPreferencesWithData }));
    component.ngOnInit();
    const isValid = component.validationHandler();

    expect(isValid).toBeFalse();
  });

  it('should return false if form is invalid', () => {
    fanzonesAPIService.getFanzonePreferences = jasmine.createSpy('getFanzonePreferences').and.returnValue(of({ body: FZPreferencesWithInvalidData }));
    component.ngOnInit();
    const isValid = component.validationHandler();

    expect(isValid).toBeFalse();
  });
});
