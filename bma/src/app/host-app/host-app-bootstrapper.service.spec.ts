import { HostAppBootstrapper } from './host-app-bootstrapper.service';

describe('HostAppBootstrapperService', () => {
  let service: HostAppBootstrapper;

  let productActivatorService;

  beforeEach(() => {
    productActivatorService = {
      activate: jasmine.createSpy()
    };
    service = new HostAppBootstrapper(productActivatorService);
  });

  describe('onAppInit()', () => {
    it('should run bootstrappers', async () => {
      await service.onAppInit();

      expect(productActivatorService.activate).toHaveBeenCalled();
    });
  });
});
