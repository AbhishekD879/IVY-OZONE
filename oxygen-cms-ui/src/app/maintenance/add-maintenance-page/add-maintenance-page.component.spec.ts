import { AddMaintenancePageComponent } from './add-maintenance-page.component';

describe('AddMaintenancePageComponent', () => {
  let component: AddMaintenancePageComponent;
  let dialogRef;
  let brandService;

  beforeEach(() => {
    dialogRef = {};
    brandService = {};

    component = new AddMaintenancePageComponent(
      dialogRef, brandService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.maintenancePage).toBeDefined();
    expect(component.form).toBeDefined();
  });
});
