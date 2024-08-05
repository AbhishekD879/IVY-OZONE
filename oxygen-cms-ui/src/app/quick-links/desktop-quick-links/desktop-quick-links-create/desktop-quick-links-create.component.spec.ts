import { async } from '@angular/core/testing';

import {DesktopQuickLinksCreateComponent} from './desktop-quick-links-create.component';

describe('DesktopQuickLinksCreateComponent', () => {
  let component,
    dialogRef,
    brandService;

  beforeEach(async(() => {
    dialogRef = {};
    brandService = {
      brand: 'coral'
    };

    component = new DesktopQuickLinksCreateComponent(
      dialogRef,
      brandService
    );
    component.ngOnInit();
  }));

  it('should create', () => {
    expect(component.desktopQuickLink).toBeDefined();
    expect(component.form).toBeDefined();
  });
});
