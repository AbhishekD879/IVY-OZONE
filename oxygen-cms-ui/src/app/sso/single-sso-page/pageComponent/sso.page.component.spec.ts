import {SsoPageComponent} from './sso.page.component';
import { of } from 'rxjs';

describe('SsoPageComponent', () => {
  let component: SsoPageComponent;
  let snackBar, dialogService, route, router, ssoApiService;

  beforeEach(() => {
      snackBar = {},
      dialogService = {},
      route = {
        snapshot: {
          paramMap: { get: jasmine.createSpy('get') }
        }
      },
      ssoApiService = {
        getSingleSsoPageData: jasmine.createSpy('getSingleSsoPageData').and.returnValue(of({body: {test: ''}}))
      },
      router = {};
    component = new SsoPageComponent(
      snackBar, dialogService, route, router, ssoApiService
    );

    component.ngOnInit();
  });

  it('should load init data', () => {
    expect(ssoApiService.getSingleSsoPageData).toHaveBeenCalled();
  });
});
