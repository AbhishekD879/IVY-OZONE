import { UserMenusCreateComponent } from './user-menus-create.component';

describe('UserMenusCreateComponent', () => {
  let component: UserMenusCreateComponent;
  let dialogRef;
  let brandService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {};

    component = new UserMenusCreateComponent(dialogRef, brandService);
  });

  it('ngOnInit', () => {
    component.ngOnInit();

    expect(component.userMenu).toBeDefined();
    expect(component.form).toBeDefined();
  });
});
