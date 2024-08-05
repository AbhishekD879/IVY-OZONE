import { BmaRunService } from './bma-run.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('BmaRunService', () => {
  let service: BmaRunService;
  let pubsub;
  let liveServIframeService;
  let apiLoadCallback;

  beforeEach(() => {
    pubsub = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((file, method, callback) => {
        apiLoadCallback = callback;
      }),
      API: pubSubApi
    };
    liveServIframeService = {
      initIframe: jasmine.createSpy('initIframe'),
    };

    service = new BmaRunService(
      pubsub,
      liveServIframeService
    );
  });

  it('constructor', () => {
    expect(service).toBeDefined();
  });

  it('should init', () => {
    service.init();
    expect(pubsub.subscribe).toHaveBeenCalledWith('bma', pubSubApi.APP_IS_LOADED, jasmine.any(Function));
  });

  it('should init iframe', () => {
    service.init();
    apiLoadCallback();
    expect(liveServIframeService.initIframe).toHaveBeenCalled();
  });
});
