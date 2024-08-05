import { FanzonesComponent } from './fanzones.component';
import { FANZONE_MOCK_DATA, FZ } from '@app/fanzone/fanzone.mock';
import { of, throwError } from 'rxjs';

describe('FanzonesComponent', () => {
  let component: FanzonesComponent;
  let router;
  let dialogService;
  let globalLoaderService;
  let fanzonesAPIService;
  let fanzoneData;

  beforeEach(() => {
    fanzoneData = FANZONE_MOCK_DATA;
    router = {
      navigate: jasmine.createSpy('navigate'),
      url: '/racing-edp-markets/1'
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
      getAllFanzones: jasmine.createSpy('getAllFanzones').and.returnValue(of({
        body: fanzoneData
      })),
      deleteFanzone: jasmine.createSpy('deleteFanzone').and.returnValue(of({}))
    };
    component = new FanzonesComponent(router, dialogService, globalLoaderService, fanzonesAPIService);

  });

  describe('fanzone list', () => {
    it('should create', () => {
      expect(component).toBeTruthy();
    });

    it('should fetch all fanzones based on brand', () => {
      spyOn(component as any, 'getFanzonesList');
      component.ngOnInit();
      expect(component['getFanzonesList']).toHaveBeenCalled();
      expect(component.fanzoneData).not.toBe(null);
    });

    it('should navigate to fanzone/create page', () => {
      component.createFanzone();
      expect(router.navigate).toHaveBeenCalledWith(['fanzones/create']);
    });

    it('should  return the list of fanzones', () => {
      component.getFanzonesList();
      expect(component.fanzoneData).toEqual(fanzoneData);
    });

    it('should  handle if getFanzonesList API returns error', () => {
      fanzonesAPIService.getAllFanzones = jasmine.createSpy('getAllFanzones').and.returnValue(throwError({ error: '401' }));

      component.getFanzonesList();
      expect(component.fanzoneData).not.toEqual(fanzoneData);
    });

    it('should remove multiple fanzones', () => {
      component.fanzoneData = fanzoneData;
      component.removeHandlerMulty(['1']);
      expect(dialogService.showConfirmDialog).toHaveBeenCalled();
    });

    it('should remove single fanzone', () => {
      component.removeFanzone(FZ);
      expect(fanzonesAPIService.deleteFanzone).toHaveBeenCalled();
    });

    it('should handle in case observable returns error for removing single fanzone', () => {
      fanzonesAPIService.deleteFanzone = jasmine.createSpy('deleteFanzone').and.returnValue((throwError({ error: '401' })));

      component.removeHandlerMulty(['']);
      expect(globalLoaderService.hideLoader).not.toHaveBeenCalled();
    });

    it('should handle in case observable returns error for removing single fanzone', () => {
      fanzonesAPIService.deleteFanzone = jasmine.createSpy('deleteFanzone').and.returnValue((throwError({ error: '401' })));

      component.removeFanzone(FZ);
      expect(dialogService.showNotificationDialog).not.toHaveBeenCalled();
    });
  });
});
