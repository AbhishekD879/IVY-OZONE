import { RightMenusCreateComponent } from './right-menus-create.component';

describe('RightMenusCreateComponent', () => {
  let component: RightMenusCreateComponent;
  let dialogRef;
  let brandService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {};

    component = new RightMenusCreateComponent(
      dialogRef, brandService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.rightMenu).toBeDefined();
    expect(component.form).toBeDefined();
  });
});
