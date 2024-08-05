import { BYBSwitchersCreateComponent } from './byb-switchers-create.component';

describe('BYBSwitchersCreateComponent', () => {
  let component: BYBSwitchersCreateComponent;
  let dialogRef;
  let brandService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {};

    component = new BYBSwitchersCreateComponent(dialogRef, brandService);
  });

  it('ngOnInit', () => {
    component.ngOnInit();

    expect(component.form).toBeDefined();
  });
});
