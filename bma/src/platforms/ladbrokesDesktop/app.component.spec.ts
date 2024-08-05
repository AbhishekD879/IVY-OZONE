import { RootComponent } from './app.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('AppComponent', () => {
  let component;
  let appRef;
  let ngZone;
  let pubSubService;
  let router;

  beforeEach(() => {
    router = {
      events: {
        subscribe: jasmine.createSpy('subscribe')
      }
    };

    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      API: pubSubApi
    };
    appRef = {};
    ngZone = {};

    component = new RootComponent(
      appRef,
      ngZone,
      pubSubService,
      router
    );
  });
});
