import { async } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import { CLUB, CLUB_UPDATED_DATE, CLUB_UPDATED_DESC } from '@app/fanzone/fanzone.mock';
import { FanzoneClubCreateComponent } from './fanzone-club-create.component';

describe('FanzoneClubCreateComponent', () => {
  let component: FanzoneClubCreateComponent;
  let router,
    dialogService,
    brandService,
    fanzonesAPIService,
    errorService;

  beforeEach(async(() => {
    router = {
      navigate: jasmine.createSpy('navigate'),
      url: '/test',
      snapshot: { paramMap: { id: '' } }
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog').and.callFake(({ title, message, closeCallback }) => {
        closeCallback();
      })
    };
    brandService = {
      brand: 'bma'
    };
    fanzonesAPIService = {
      saveFanzoneClub: jasmine.createSpy('saveFanzoneClub').and.returnValue(of({ body: CLUB }))
    };
    errorService = {
      emitError: jasmine.createSpy('emitError')
    };
    component = new FanzoneClubCreateComponent(router, dialogService, brandService, fanzonesAPIService, errorService);
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should assign default value to club', () => {
    component.ngOnInit();

    expect(component.club).toEqual(CLUB);
  });

  it('should update Promotion', () => {
    component.ngOnInit();
    component.updatePromotion('updated desc');

    expect(component.club).toEqual(CLUB_UPDATED_DESC);
  });

  it('should update date of club', () => {
    component.ngOnInit();
    component.handleDateUpdate({ startDate: '10-10-2020', endDate: '12-10-2020' });

    expect(component.club).toEqual(CLUB_UPDATED_DATE);
  });

  it('should save club and show confirm dialog', () => {
    component.ngOnInit();
    component.saveClub();

    expect(dialogService.showNotificationDialog).toHaveBeenCalled();
  });

  it('should handle if save club api returns error', () => {
    fanzonesAPIService.saveFanzoneClub = jasmine.createSpy('saveFanzoneClub').and.returnValue(throwError({ error: 401 }));
    component.ngOnInit();
    component.saveClub();

    expect(errorService.emitError).toHaveBeenCalled();
  });

  it('should return true if valid', () => {
    component.ngOnInit();
    component.club.title = 'test';
    component.club.bannerLink = 'test';
    component.club.description = 'test';
    const isValid = component.isValidModel();

    expect(isValid).toEqual('test');
  });

  it('should return false if invalid', () => {
    component.ngOnInit();
    const isValid = component.isValidModel();

    expect(isValid).toEqual('');
  });
});
