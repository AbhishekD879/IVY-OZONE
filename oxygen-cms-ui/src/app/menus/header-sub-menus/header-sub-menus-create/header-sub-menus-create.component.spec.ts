import { HeaderSubMenusCreateComponent } from './header-sub-menus-create.component';

describe('HeaderSubMenusCreateComponent', () => {
  let component: HeaderSubMenusCreateComponent;
  let dialogRef, brandService

  beforeEach(() => {
    dialogRef = {};
    brandService = {
      brand: 'CORAL'
    };

    component = new HeaderSubMenusCreateComponent(dialogRef, brandService);
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.headerSubMenu).toBeTruthy();
    expect(component.form).toBeTruthy();
  });
});
