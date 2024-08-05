import { SessionLogoutDialogComponent } from './session-logout-dialog.component';

describe('SessionLogoutDialogComponent', () => {
  let deviceService;
  let storageService;
  let localeService;
  let pubSubService;
  let windowRef;
  let component: SessionLogoutDialogComponent;

  beforeAll(() => {
    deviceService = {};
    windowRef = {
      document: {
        body: {
          classList: {
            add: jasmine.createSpy('add')
          }
        }
      }
    };
    storageService = {
      get: jasmine.createSpy('get')
    };
    localeService = {
      getString: jasmine.createSpy('getString')
    };
    pubSubService = jasmine.createSpyObj('pubSubService', ['publish', 'API']);

    component = new SessionLogoutDialogComponent(
      deviceService,
      storageService,
      localeService,
      pubSubService,
      windowRef
    );
    component.dialog = { changeDetectorRef: { detectChanges: jasmine.createSpy('detectChanges') } };
  });

  describe('open', () => {
    it('should show logged out message', () => {
      storageService.get.and.returnValue(null);
      component.open();
      expect(localeService.getString).toHaveBeenCalledWith('bma.loggedOutTittle');
    });

    it('should show logged out message with session limit', () => {
      storageService.get.and.returnValue({
        sessionLimitLogout: true, sessionLimit: 10
      });
      component.open();
      expect(localeService.getString).toHaveBeenCalledWith('bma.loggedOutTittleSessionLimit', [10]);
    });
  });

  it('openLoginDialog', () => {
    component.openLoginDialog();
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.OPEN_LOGIN_DIALOG, { placeBet: false, moduleName: 'logout' });
  });
});
