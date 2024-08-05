import { UpgradeAccountService } from '@app/retail/services/upgradeAccount/upgrade-account.service';
import { fakeAsync, tick } from '@angular/core/testing';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('UpgradeAccountService', () => {
  let service: UpgradeAccountService,
    pubSubService,
    router;

  beforeEach(() => {
    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe').and.callFake((subscriberName: string, channel: any, channelFunction: Function) => {
        channelFunction(true);
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish')
    };

    router = {
      navigate: jasmine.createSpy('navigate')
    };

    service = new UpgradeAccountService(
      pubSubService,
      router
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('subscribe', () => {
    service.subscribe();

    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'upgradeFromBetslip', pubSubService.API.UPGRADE_FROM_BETSLIP, jasmine.any(Function));
  });

  describe('#afterReloginRedirection', () => {
    it('afterReloginRedirection to betslip', fakeAsync(() => {
      service['isUpgradeFromBetslip'] = true;
      service['afterReloginRedirection']();
      tick(1000);

      expect(pubSubService.publish).toHaveBeenCalledWith('show-slide-out-betslip', true);
      expect(service['isUpgradeFromBetslip']).toBeFalsy();
    }));

    it('afterReloginRedirection to deposit', () => {
      service['isUpgradeFromBetslip'] = false;

      service['afterReloginRedirection']();

      expect(router.navigate).toHaveBeenCalledWith(['/deposit', 'addcard']);
    });
  });
});
