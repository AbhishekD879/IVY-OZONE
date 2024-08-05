import { NavigationPointsApiService } from './navigation-points.api.service';

describe('NavigationPointsApiService', () => {
  let service,
    globalLoaderService,
    apiClientService;

  beforeEach(() => {
    globalLoaderService = {};
    apiClientService = {
      navigationPoints: jasmine.createSpy('navigationPoints').and.returnValue({
        reorderNavigationPoints: jasmine.createSpy('reorderNavigationPoints').and.returnValue({'id':123}),
      })
    };

    service = new NavigationPointsApiService(
      globalLoaderService,
      apiClientService
    );
  });

  it('should be created', () => {
    expect(service).toBeDefined();
  });

  it('reorderNavigationPoints', () => {
    const order = { id: '1', order: ['1', '2', '3'] };
    service.reorderNavigationPoints(order);
    expect(apiClientService.navigationPoints).toHaveBeenCalled();
  });
});
