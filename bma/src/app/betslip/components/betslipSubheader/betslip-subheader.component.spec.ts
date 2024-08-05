import { BetslipSubheaderComponent } from './betslip-subheader.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('BetslipSubheaderComponent', () => {
  let component: BetslipSubheaderComponent;
  let infoDialogService;
  let localeService;
  let pubSubService;
  let betslipService;
  let gtmService;
  let serviceClosureService;
  let changeDetection;
  beforeEach(() => {
    infoDialogService = {
      openInfoDialog: jasmine.createSpy('openInfoDialog'),
      closePopUp: jasmine.createSpy('closePopUp')
    };
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('')
    };
    pubSubService = {
      API: pubSubApi,
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    betslipService = {
      count: jasmine.createSpy('count'),
      closeNativeBetslipAndWaitAnimation: jasmine.createSpy('closeNativeBetslipAndWaitAnimation').and.callFake(cb => cb())
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    serviceClosureService = {
      updateClosureFlag : jasmine.createSpy('updateClosureFlag')
    };
    changeDetection = {
      detectChanges: jasmine.createSpy('detectChanges')
    };
    component = new BetslipSubheaderComponent(
      infoDialogService,
      localeService,
      pubSubService,
      betslipService,
      gtmService,
      serviceClosureService,
      changeDetection);
  });

  it('ngOnInit', () => {
    pubSubService.subscribe.and.callFake((p1, p2, cb) => cb());
    component.ngOnInit();
    expect(betslipService.count).toHaveBeenCalledTimes(1);
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'BetslipSubheaderComponent', 'BETSLIP_COUNTER_UPDATE', jasmine.any(Function)
    );
  });

  it('ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('BetslipSubheaderComponent');
  });

  describe('showConfirm', () => {
    it('should show dialog', () => {
      component.showConfirm();

      expect(infoDialogService.openInfoDialog).toHaveBeenCalledWith(
        jasmine.any(String),
        jasmine.any(String),
        'bs-clear-dialog', undefined, undefined,
        jasmine.any(Array)
      );
      expect(localeService.getString).toHaveBeenCalledWith('bs.clearBetslipTitle');
      expect(localeService.getString).toHaveBeenCalledWith('bs.confirmClearOfBetSlip');
      expect(localeService.getString).toHaveBeenCalledWith('bs.clearBetslipCancel');
      expect(localeService.getString).toHaveBeenCalledWith('bs.clearBetslipContinue');
    });

    it('should close dialog', () => {
      infoDialogService.openInfoDialog.and.callFake((...params) => {
        params[5][1].handler();
      });
      component.showConfirm();
      expect(betslipService.closeNativeBetslipAndWaitAnimation).toHaveBeenCalledTimes(1);
      expect(infoDialogService.closePopUp).toHaveBeenCalledTimes(1);
      expect(component['gtmService'].push).toHaveBeenCalledWith('trackEvent', {
        eventAction: 'trackEvent',
        eventCategory: 'betslip',
        eventLabel: 'clear betslip click'
      });
    });
    it('should clear suspended', () => {
      spyOn(component.remove, 'emit').and.callThrough();
      component.removeSuspended();
      expect(component.remove.emit).toHaveBeenCalled();

    });
  });
});
