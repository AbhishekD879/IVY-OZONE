import { SbQuickbetComponent } from '@app/quickbet-stream-bet/components/quickbet/sb-quickbet.component';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { QuickbetComponent } from '@app/quickbet/components/quickbet/quickbet.component';
import { Subject } from 'rxjs';

describe('SbQuickbetComponent', () => {
  let component: SbQuickbetComponent;
  let locale;
  let pubsub;
  let gtm;
  let quickbetService;
  let remoteBsService;
  let quickbetOverAskService;
  let command;
  let dialogService;
  let infoDialogService;
  let device;
  let nativeBridgeService;
  let location;
  let quickbetDataProviderService;
  let rendererService;
  let windowRef;
  let gtmTrackingService;
  let quickbetDepositService;
  let quickbetNotificationService;
  let awsService;
  let changeDetectorRef;
  let userService;
  let sessionStorage;
  let racingPostTipService;
  let arcUserService;
  let storageService;
  let betslipService;
  let betReciptService;

  beforeEach(() => {
    locale = {
        getString: jasmine.createSpy().and.returnValue(''),
      };

    device = {
      isOnline: jasmine.createSpy('isOnline')
    };

    quickbetService = {
      quickBetOnOverlayCloseSubj: new Subject<string>
    };

    infoDialogService = {
      openConnectionLostPopup: jasmine.createSpy('openConnectionLostPopup')
    };

    betslipService={
      betKeyboardData:''
    };

    betReciptService = {

    }

    pubsub = {
      API: pubSubApi,
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy().and.callFake((file, method, callback) => {
          if (method === 'REMOVE_FROM_SB_QUICKBET') {
            callback('frac');
          } else {
            callback();
          }
      }),
      unsubscribe: jasmine.createSpy()
    };
    component = new SbQuickbetComponent(
        locale,
        pubsub,
        gtm,
        quickbetService,
        remoteBsService,
        quickbetOverAskService,
        command,
        dialogService,
        infoDialogService,
        device,
        nativeBridgeService,
        location,
        quickbetDataProviderService,
        rendererService,
        windowRef,
        gtmTrackingService,
        quickbetDepositService,
        quickbetNotificationService,
        awsService,
        changeDetectorRef,
        userService,
        sessionStorage,
        racingPostTipService,
        arcUserService,
        storageService,
        betslipService,
        betReciptService
    );
  });

  describe('#SbQuickbetComponent', () => {

    it('ngOnInit is called', () => {
      spyOn(QuickbetComponent.prototype, 'ngOnInit');
      spyOn(component, 'addSelectionHandler');
      component.selection = {stake: '1.23'} as any;
      spyOn(component, 'placeBetListener');
      const closePanelSpy = spyOn(component, 'closePanel');
      component.ngOnInit();
      component.quickbetService.quickBetOnOverlayCloseSubj.next('fullscreen exit');
      expect(closePanelSpy).toHaveBeenCalled();
    });

    it('closePanel is called and device isOnline is true', () => {
      spyOn(QuickbetComponent.prototype, 'closePanel');
      device.isOnline.and.returnValue(true);
      component.closePanel();
      expect(QuickbetComponent.prototype.closePanel).toHaveBeenCalled();
    });

    it('closePanel is called and device isOnline is false', () => {
      device.isOnline.and.returnValue(false);
      component.closePanel();
      expect(infoDialogService.openConnectionLostPopup).toHaveBeenCalled();
    });

    it('ngOnDestroy', () => {
      const pubsubSpy = pubsub.unsubscribe;
      component.ngOnDestroy();
      expect(pubsubSpy).toHaveBeenCalled();
    })
  });
});
