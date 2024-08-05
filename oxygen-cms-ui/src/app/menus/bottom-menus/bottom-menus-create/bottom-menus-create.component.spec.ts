import { BottomMenusCreateComponent } from './bottom-menus-create.component';

describe('BottomMenusCreateComponent', () => {
  let component: BottomMenusCreateComponent;
  let dialogRef;
  let brandService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {};

    component = new BottomMenusCreateComponent(dialogRef, brandService);
  });

  it('ngOnInit', () => {
    component.ngOnInit();

    expect(component.bottomMenu).toBeDefined();
    expect(component.form).toBeDefined();
  });
});
