import { ChildSportsCreateComponent } from './child-sports-create.component';

describe('ChildSportsCreateComponent', () => {
  let component: ChildSportsCreateComponent;
  let brandService;
  let dialogRef;

  beforeEach(() => {
    brandService = {};
    dialogRef = {};
    component = new ChildSportsCreateComponent(brandService, dialogRef, {});
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.newChildSport).toBeDefined();
    expect(component.form).toBeDefined();
  });
});
