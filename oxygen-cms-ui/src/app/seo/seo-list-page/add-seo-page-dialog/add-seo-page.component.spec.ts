import { async } from '@angular/core/testing';

import {AddSeoPageComponent} from './add-seo-page.component';

describe('AddSeoPageComponent', () => {
  let component,
    dialogRef,
    brandService;

  beforeEach(async(() => {
    dialogRef = {};
    brandService = {};

    component = new AddSeoPageComponent(
      dialogRef,
      brandService
    );

    component.ngOnInit();
  }));

  it('should create', () => {
    expect(component.newSeoPage).toBeDefined();
  });
});
