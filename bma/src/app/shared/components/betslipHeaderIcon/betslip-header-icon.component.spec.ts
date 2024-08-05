import { BetslipHeaderIconComponent } from '@shared/components/betslipHeaderIcon/betslip-header-icon.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('BetslipHeaderIconComponent', () => {
  let component: BetslipHeaderIconComponent;

  let betslipTabsService;
  let pubSubService;
  let GTM;

  beforeEach(() => {
    betslipTabsService = {
      redirectToBetSlipTab: jasmine.createSpy()
    };
    pubSubService = {
      API: pubSubApi,
      publish: jasmine.createSpy('publish')
    };
    GTM = {
      push: jasmine.createSpy()
    };
    component = new BetslipHeaderIconComponent(betslipTabsService, pubSubService, GTM);
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('should call correct methods', () => {
    component.openBetslip();
    expect(GTM.push)
      .toHaveBeenCalledWith('trackPageview', jasmine.objectContaining({ virtualUrl: '/betslip-receipt' }));
    expect(betslipTabsService.redirectToBetSlipTab).toHaveBeenCalledWith('Bet Slip', true);
    expect(pubSubService.publish).toHaveBeenCalledWith('show-slide-out-betslip', true);
  });
});
