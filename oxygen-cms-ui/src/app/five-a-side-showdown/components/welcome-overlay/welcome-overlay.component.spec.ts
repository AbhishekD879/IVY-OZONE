import { of, throwError } from 'rxjs';

import { WELCOME_OVERLAY } from '@app/five-a-side-showdown/components/welcome-overlay/welcome-overlay.mock';
import { WelcomeOverlayComponent } from '@app/five-a-side-showdown/components/welcome-overlay/welcome-overlay.component';

describe('WelcomeOverlayComponent', () => {
  let component: WelcomeOverlayComponent;
  let apiService;
  let dialogService;
  let brandService;
  let welcomeOverlayService;

  beforeEach(() => {
    welcomeOverlayService = {
      getDetailsByBrand: jasmine.createSpy('getDetailsByBrand').and.returnValue(of({
        body: WELCOME_OVERLAY
      })),
      updateWelcomeOverlay: jasmine.createSpy('updateWelcomeOverlay').and.returnValue(of({
        body: WELCOME_OVERLAY
      })),
      saveWelcomeOverlay: jasmine.createSpy('saveWelcomeOverlay').and.returnValue(of({
        body: WELCOME_OVERLAY
      }))
    };
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog'),
      showCustomDialog: jasmine.createSpy('showCustomDialog').and.callFake((dialogComponent, {
        width, title, yesOption, noOption, yesCallback
      }) => {
        yesCallback(WELCOME_OVERLAY);
      }),
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and
        .callFake(({ title, message, yesCallback }) => yesCallback())
    };
    apiService = {
      welcomeOverlayService: () => welcomeOverlayService
    };
    component = new WelcomeOverlayComponent(apiService, dialogService, brandService);
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    } as any;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should get details by brand', () => {
      component.ngOnInit();
      expect(component.welcomeOverlay).not.toBeNull();
    });
    it('should not get details by brand, when error throwed (404)', () => {
      welcomeOverlayService.getDetailsByBrand.and.returnValue(throwError({error: {status: '404'}}));
      component.ngOnInit();
      expect(component.welcomeOverlay).not.toBeNull();
    });
    it('should not get details by brand, when error throwed (501)', () => {
      welcomeOverlayService.getDetailsByBrand.and.returnValue(throwError({error: {status: '501'}}));
      component.ngOnInit();
      expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
        title: 'Error occurred',
        message: 'Ooops... Something went wrong, please contact support team'
      });
    });
  });

  describe('#actionsHandler', () => {
    it('should save welcome', () => {
      component.welcomeOverlay = {
        createdAt: ''
      } as any;
      const event = 'save';
      component.actionsHandler(event);
      expect(component.welcomeOverlay).not.toBeNull();
    });
    it('should edit welcome', () => {
      component.welcomeOverlay = {
        createdAt: '1234'
      } as any;
      const event = 'save';
      component.actionsHandler(event);
      expect(component.welcomeOverlay).not.toBeNull();
    });
    it('should edit welcome', () => {
      welcomeOverlayService.updateWelcomeOverlay.and.returnValue(throwError({error: '404'}))
      component.welcomeOverlay = {
        createdAt: '1234'
      } as any;
      const event = 'save';
      component.actionsHandler(event);
      expect(dialogService.showNotificationDialog).toHaveBeenCalledWith({
        title: 'Error on saving',
        message: 'Ooops... Something went wrong, please contact support team'
      });
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
      expect(component.welcomeOverlay).toBeUndefined();
    });
  });

  describe('#verifywelcomeOverlay', () => {
    it('should return true', () => {
      const response = component.verifywelcomeOverlay({ id: 1} as any);
      expect(response).toBe(true);
    });
    it('should return false', () => {
      const response = component.verifywelcomeOverlay(null);
      expect(response).toBe(false);
    });
  });
});
