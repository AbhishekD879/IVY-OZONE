import { HeaderMenusCreateComponent } from './header-menus-create.component';
import { of } from "rxjs";

describe('HeaderMenusCreateComponent', () => {
  let component: HeaderMenusCreateComponent, dialogRef: any, brandService, apiClientService;

  beforeEach(() => {
    brandService = {
      brand: 'CORAL'
    };

    apiClientService = {
      headerMenu: jasmine.createSpy('headerMenu').and.returnValue(
        { findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of([])) }
      )
    };
    component = new HeaderMenusCreateComponent(dialogRef, brandService, apiClientService);
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.headerMenu).toBeTruthy();
    expect(component.form).toBeTruthy();
    expect(apiClientService.headerMenu().findAllByBrand).toHaveBeenCalled();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
