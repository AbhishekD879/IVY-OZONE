import { of, throwError } from 'rxjs';
import { NetworkIndicatorComponent } from './network-indicator.component';
import { NETWORK_INDICATOR } from './network-indicator.mock';

describe('NetworkIndicatorComponent', () => {
  let component: NetworkIndicatorComponent;
  let apiService;
  let dialogService;
  let brandService;
  let networkIndicatorService;

  beforeEach(() => {
    networkIndicatorService = {
      getDetailsByBrand: jasmine.createSpy('getDetailsByBrand').and.returnValue(of({
        body: NETWORK_INDICATOR
      })),
      updateWelcomeOverlay: jasmine.createSpy('updateWelcomeOverlay').and.returnValue(of({
        body: NETWORK_INDICATOR
      })),
      saveWelcomeOverlay: jasmine.createSpy('saveWelcomeOverlay').and.returnValue(of({
        body: NETWORK_INDICATOR
      }))
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
      showCustomDialog: jasmine.createSpy('showCustomDialog').and.callFake((dialogComponent, {
        width, title, yesOption, noOption, yesCallback
      }) => {
        yesCallback(NETWORK_INDICATOR);
      }),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and
        .callFake(({ title, message, yesCallback }) => yesCallback())
    };
    apiService = {
        networkIndicatorService: () => networkIndicatorService
    };
    component = new NetworkIndicatorComponent(apiService, dialogService, brandService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should get details by brand', () => {
      component.ngOnInit();
      expect(component.networkIndicator).not.toBeNull();
    });
    it('should not get details by brand, when error throwed (404)', () => {
        networkIndicatorService.getDetailsByBrand.and.returnValue(throwError({error: {status: '404'}}));
        component.ngOnInit();
        expect(component.networkIndicator).not.toBeNull();
    });
    it('should not get details by brand, when error throwed (501)', () => {
        networkIndicatorService.getDetailsByBrand.and.returnValue(throwError({error: {status: '501'}}));
        component.ngOnInit();
        expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
            title: 'Error occurred',
            message: 'Ooops... Something went wrong, please contact support team'
        });
    });
  });

  describe('#actionsHandler', () => {
    it('should save welcome', () => {
      component.networkIndicator = {
        createdAt: ''
      } as any;
      const event = 'save';
      component.actionsHandler(event);
      expect(component.networkIndicator).not.toBeNull();
    });
    it('should edit welcome', () => {
      component.networkIndicator = {
        createdAt: '1234'
      } as any;
      const event = 'save';
      component.actionsHandler(event);
      expect(component.networkIndicator).not.toBeNull();
    });
    it('should edit welcome', () => {
      networkIndicatorService.getDetailsByBrand.and.returnValue(throwError({error: {status: '404'}}));
      component.networkIndicator = {
        createdAt: '1234'
      } as any;
      const event = 'save';
      component.actionsHandler(event);
      expect(dialogService.showNotificationDialog).toHaveBeenCalled();
    });
    it('should revert faq', () => {
      spyOn(component as any, 'loadInitialData');
      const event = 'revert';
      component.actionsHandler(event);
      expect(component['loadInitialData']).toHaveBeenCalled();
    });
    it('should set default condition', () => {
      spyOn(console, 'error');
      const event = 'racdom';
      component.actionsHandler(event);
      expect(component.networkIndicator).toBeUndefined();
    });
  });
});
