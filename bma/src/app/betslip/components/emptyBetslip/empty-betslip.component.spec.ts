import { EmptyBetslipComponent } from './empty-betslip.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('EmptyBetslipComponent', () => {
  let router;
  let pubSubService;
  let serviceClosureService;

  let component: EmptyBetslipComponent;

  beforeEach(() => {
    router = {
      navigate: jasmine.createSpy()
    };

    pubSubService = {
      API: pubSubApi,
      publish: jasmine.createSpy('publish')
    };

    component = new EmptyBetslipComponent(router, pubSubService, serviceClosureService);
    serviceClosureService = {
      checkUserServiceClosureStatus : jasmine.createSpy('checkUserServiceClosureStatus')
    };
  });

  it('goToHomePage', () => {
    component.goToHomePage();
    expect(router.navigate).toHaveBeenCalledWith(['/']);
    expect(pubSubService.publish).toHaveBeenCalledWith('show-slide-out-betslip', false);
  });
});
