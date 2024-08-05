import { LogoutResolver } from '@vanillaInitModule/services/logout/logout.service';

describe('VanillaLogoutResolver', () => {
  let service: LogoutResolver;
  let authService;
  beforeEach(() => {
    authService = {
      logout: jasmine.createSpy()
    };
    service = new LogoutResolver(authService);
  });

  it('resolve', () => {
    service.resolve();
    expect(authService.logout).toHaveBeenCalled();
  });
});
