import { StreamButtonComponent } from './stream-button.component';

import { UserService } from '@core/services/user/user.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

describe('StreamButtonComponent', () => {
  let component: StreamButtonComponent;

  let userService: UserService;
  let pubSubService: PubSubService;

  beforeEach(() => {
    userService = {
      status: true
    } as any;

    pubSubService = {
      publish: jasmine.createSpy(),
      API: {
        PUSH_TO_GTM: 'PUSH_TO_GTM'
      }
    } as any;

    component = new StreamButtonComponent(userService, pubSubService);
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  it('setActiveEvent', () => {
    component.setActiveEvent({ id: 1 } as any);
    expect(pubSubService.publish).toHaveBeenCalledWith('PUSH_TO_GTM', ['trackEvent', {
      eventCategory: 'home',
      eventAction: 'live stream',
      eventLabel: 'watch stream'
    }]);
  });

  it ('isLoggedIn', () => {
    component['userService'] = { status: true } as any;
    expect(component.isLoggedIn()).toBeTruthy();

    component['userService'] = { status: false } as any;
    expect(component.isLoggedIn()).toBeFalsy();
  });
});
