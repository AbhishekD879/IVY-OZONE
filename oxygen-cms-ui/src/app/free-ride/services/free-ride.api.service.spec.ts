import { FreeRideAPIService } from './free-ride.api.service';

describe('FreeRideService', () => {
  let service: FreeRideAPIService;
  let apiClientService;
  let globalLoaderService;
  beforeEach(() => {

    globalLoaderService = {
      'hideLoader': jasmine.createSpy('hideLoader'),
      'showLoader': jasmine.createSpy('showLoader')
    };
    apiClientService = {
      freeRideService: () => ({})
    };

    service = new FreeRideAPIService(
      globalLoaderService,
      apiClientService
    );

  });
  describe('FreeRideAPIService', () => {
    it('should be created', () => {
      expect(service).toBeTruthy();
    });
  });

});
