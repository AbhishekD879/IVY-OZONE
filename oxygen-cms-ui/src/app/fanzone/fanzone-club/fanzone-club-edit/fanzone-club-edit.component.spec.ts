import { async } from '@angular/core/testing';
import { ActionButtonsComponent } from '@root/app/shared/action-buttons/action-buttons.component';
import { of, throwError } from 'rxjs';
import { FANZONE_CLUB_MOCK_DATA } from '../../fanzone.mock';
import { FanzoneClubEditComponent } from './fanzone-club-edit.component';

describe('FanzoneClubEditComponent', () => {
  let component: FanzoneClubEditComponent;
  let route,
    router,
    dialogService,
    fanzonesAPIService,
    errorService;

  beforeEach(async(() => {
    route = {
      snapshot: {
        paramMap: { get: jasmine.createSpy('get').and.returnValue('22153') }
      }
    };
    router = {
      navigate: jasmine.createSpy('navigate'),
      snapshot: { paramMap: { id: '22153' } }
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
    };
    fanzonesAPIService = {
      getFanzoneClub: jasmine.createSpy('getFanzoneClub').and.returnValue(of({ body: FANZONE_CLUB_MOCK_DATA })),
      updateFanzoneClub: jasmine.createSpy('updateFanzoneClub').and.returnValue(of({ body: FANZONE_CLUB_MOCK_DATA })),
      deleteFanzoneClub: jasmine.createSpy('deleteFanzoneClub').and.returnValue(of({ body: FANZONE_CLUB_MOCK_DATA }))
    };
    errorService = {
      emitError: jasmine.createSpy('emitError')
    };
    component = new FanzoneClubEditComponent(route, router, dialogService, fanzonesAPIService, errorService);
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    } as any as ActionButtonsComponent;
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('ngOnInit', () => {
    component.getFanzoneClub = jasmine.createSpy('component.getFanzoneClub');
    component.ngOnInit();
    expect(component.id).toBe('22153');
    expect(component.getFanzoneClub).toHaveBeenCalled();
  })

  it('actionsHandler to remove fanzone', () => {
    component.deleteFanzoneClub = jasmine.createSpy('component.deleteFanzoneClub');
    component.actionsHandler('remove');
    expect(component.deleteFanzoneClub).toHaveBeenCalled();
  })

  it('updatePromotion', () => {
    component.club = { id: '1', description: 'val' } as any;
    component.updatePromotion('description');
    expect(component.club['description']).toEqual('description');
  })

  it('actionsHandler to save fanzone details', () => {
    component.updateFanzoneClub = jasmine.createSpy('component.updateFanzoneClub');
    component.actionsHandler('save');
    expect(component.updateFanzoneClub).toHaveBeenCalled();
  });


  it('actionsHandler to revert fanzone details', () => {
    component.getFanzoneClub = jasmine.createSpy('component.getFanzoneClub');
    component.actionsHandler('revert');
    expect(component.getFanzoneClub).toHaveBeenCalled();
  })

  it('actionsHandler to console fanzone details', () => {
    spyOn(console, 'error');
    component.actionsHandler('');
    expect(console.error).toHaveBeenCalled();
  })

  it('should handle if getFanzoneDetails preference API returns valid response', () => {
    fanzonesAPIService.getFanzoneClub = jasmine.createSpy('getFanzoneClub').and.returnValue(of(({ body: {} })));
    component.getFanzoneClub('');
    expect(component.club).toEqual({} as any);
    expect(component.isReady).toBeTrue();
    expect(component.breadcrumbsData).toEqual([
      { label: 'Fanzone Clubs', url: '/fanzones/club' },
      { label: undefined, url: '/fanzones/club/undefined' }
    ]);
  });

  it('should handle if getFanzoneDetails preference API returns valid response', () => {
    spyOn(console, 'error');
    fanzonesAPIService.getFanzoneClub = jasmine.createSpy('getFanzoneClub').and.returnValue(throwError({ error: '403' }));
    component.getFanzoneClub('');
    expect(console.error).toHaveBeenCalled();
  });

  it('handleDateUpdate', () => {
    component.club = FANZONE_CLUB_MOCK_DATA;
    component.handleDateUpdate({ startDate: '22-10-12', endDate: '25-10-12' });
    expect(component.club.validityPeriodStart).toBe('22-10-12');
    expect(component.club.validityPeriodEnd).toBe('25-10-12');
  });

  it('should handle if update preference API returns valid response', () => {
    component.actionButtons.extendCollection = jasmine.createSpy('component.actionButtons.extendCollection');
    fanzonesAPIService.updateFanzoneDetails = jasmine.createSpy('updateFanzoneDetails').and.returnValue(of({ body: FANZONE_CLUB_MOCK_DATA }));
    component.updateFanzoneClub();
    expect(component.club).toEqual(FANZONE_CLUB_MOCK_DATA);
    expect(component.actionButtons.extendCollection).toHaveBeenCalled();
    expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
      title: 'Club Saved'
    });
  });

  it('should handle if update preference API returns error', () => {
    fanzonesAPIService.updateFanzoneClub = jasmine.createSpy('updateFanzoneClub').and.returnValue(throwError({ error: '403' }));
    component.updateFanzoneClub();
    expect(errorService.emitError).toHaveBeenCalled();
  });

  it('should handle if delete preference API returns valid response', () => {
    fanzonesAPIService.deleteFanzoneClub = jasmine.createSpy('deleteFanzoneClub').and.returnValue(of({}));
    component.deleteFanzoneClub('');

    expect(router.navigate).toHaveBeenCalled();
  });

  it('should handle if delete preference API returns error', () => {
    spyOn(console, 'error');
    fanzonesAPIService.deleteFanzoneClub = jasmine.createSpy('deleteFanzoneClub').and.returnValue(throwError({ error: '403' }));
    component.deleteFanzoneClub('');
    expect(console.error).toHaveBeenCalled();
  });

  it('validationHandler -> should return true if form is valid', () => {
    component.club = FANZONE_CLUB_MOCK_DATA;
    const isValid = component.validationHandler();
    expect(isValid).toBe(true);
  });

});
