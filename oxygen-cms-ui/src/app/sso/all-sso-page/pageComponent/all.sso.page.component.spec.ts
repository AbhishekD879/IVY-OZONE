import { AllSsoPageComponent } from './all.sso.page.component';
import { of } from 'rxjs';

describe('AllSsoPageComponent', () => {
  let component: AllSsoPageComponent;
  let snackBar, dialogService, dialog, ssoApiService, router;

  beforeEach(() => {
      snackBar = {},
      dialogService = {},
      dialog = {},
      ssoApiService = {
        getSsoPagesData: jasmine.createSpy('getConfigurationData').and.returnValue(of({body: {test: ''}}))
      },
      router = {};
    component = new AllSsoPageComponent(
      snackBar, dialogService, dialog, ssoApiService, router
    );

    component.ngOnInit();
  });

  it('should load init data', () => {
    const res = {test: ''} as any;
    expect(ssoApiService.getSsoPagesData).toHaveBeenCalled();
    expect(component.ssoPagesData).toEqual(res);
  });
});
