import { async } from '@angular/core/testing';
import { HrQuickLinksCreateComponent } from './hr-quick-links-create.component';

describe('HrQuickLinksCreateComponent', () => {
  let component, dialogRef, brandService;

  beforeEach(async(() => {
    dialogRef = {};
    brandService = {
      brand: 'coral'
    };

    component = new HrQuickLinksCreateComponent(
      dialogRef,
      brandService
    );

    component.ngOnInit();
  }));

  it('should create', () => {
    expect(component.hrQuickLink).toBeDefined();
    expect(component.form).toBeDefined();
  });
});
