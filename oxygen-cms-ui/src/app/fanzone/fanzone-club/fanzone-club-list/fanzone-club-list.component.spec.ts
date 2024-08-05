import { of, throwError } from 'rxjs';
import { FANZONE_CLUB_LIST_MOCK_DATA, CLUB_MOCK } from '../../fanzone.mock';
import { FanzoneClubListComponent } from './fanzone-club-list.component';

describe('FanzoneClubListComponent', () => {
  let component: FanzoneClubListComponent;
  let router,
    dialogService,
    globalLoaderService,
    fanzonesAPIService,
    errorService;
  let clubData;

  beforeEach(() => {
    clubData = FANZONE_CLUB_LIST_MOCK_DATA;
    router = {
      navigate: jasmine.createSpy('navigate')
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and
        .callFake(({ title, message, yesCallback }) => yesCallback())
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    fanzonesAPIService = {
      getAllFanzoneClubs: jasmine.createSpy('getAllFanzoneClubs').and.returnValue(of({ body: clubData })),
      deleteFanzoneClub: jasmine.createSpy('deleteFanzoneClub').and.returnValue(of({}))
    };
    errorService = {
      emitError: jasmine.createSpy('emitError')
    };
    component = new FanzoneClubListComponent(router, dialogService, globalLoaderService, fanzonesAPIService, errorService);
    component.clubData = clubData;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should fetch all fanzones based on brand', () => {
    spyOn(component as any, 'getFanzonesClubs');
    component.ngOnInit();
    expect(component['getFanzonesClubs']).toHaveBeenCalled();
    expect(component.clubData).not.toBe(null);
  });

  it('should navigate to fanzones/club-create page', () => {
    component.createClub();
    expect(router.navigate).toHaveBeenCalledWith(['fanzones/club-create']);
  });

  it('should return the list of fanzone clubs', () => {
    component.getFanzonesClubs();
    expect(component.clubData).toEqual(FANZONE_CLUB_LIST_MOCK_DATA);
  });

  it('should handle if getFanzonesClubs API returns error', () => {
    fanzonesAPIService.getAllFanzoneClubs = jasmine.createSpy('getAllFanzoneClubs').and.returnValue(throwError({ error: '401' }))

    component.getFanzonesClubs();
    expect(errorService.emitError).toHaveBeenCalled();
  });

  it('should remove multiple fanzone clubs', () => {
    component.clubData = clubData;
    component.removeHandlerMulty(['1']);
    expect(dialogService.showConfirmDialog).toHaveBeenCalled();
  });

  it('should remove single fanzone club', () => {
    component.removeFanzoneClub(CLUB_MOCK);
    expect(fanzonesAPIService.deleteFanzoneClub).toHaveBeenCalled();
  });

  it('should handle in case observable returns error for removing single fanzone club', () => {
    fanzonesAPIService.deleteFanzoneClub = jasmine.createSpy('deleteFanzoneClub').and.returnValue((throwError({ error: '401' })));

    component.removeHandlerMulty(['']);
    expect(globalLoaderService.hideLoader).not.toHaveBeenCalled();
  });

  it('should handle in case observable returns error for removing single fanzone club', () => {
    fanzonesAPIService.deleteFanzoneClub = jasmine.createSpy('deleteFanzoneClub').and.returnValue((throwError({ error: '401' })));

    component.removeFanzoneClub(CLUB_MOCK);
    expect(dialogService.showNotificationDialog).not.toHaveBeenCalled();
  });

  it('should return active and inactive clubsAmount', () => {
    component['getFilteredClubs'] = jasmine.createSpy('getFilteredClubs');
    component.ngOnInit();
    const result = component.clubsAmount;

    expect(result).toBeDefined();
    expect(component['getFilteredClubs']).toHaveBeenCalled();
  });

  it('to filter active clubs -> getFilteredClubs', () => {
    component.clubData = FANZONE_CLUB_LIST_MOCK_DATA;
    const res = component['getFilteredClubs']();
    expect(res).toEqual([CLUB_MOCK]);
  });
});
