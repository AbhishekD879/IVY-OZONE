import { SsoCreateComponent } from './sso.create.component';
import {MAT_DIALOG_DATA as data} from '@angular/material/dialog';

describe('SsoCreateComponent', () => {
  let component: SsoCreateComponent;
  let dialogRef, brandService;

  beforeEach(() => {
    dialogRef = {
      close: jasmine.createSpy('close')
    },
    brandService = {};
    component = new SsoCreateComponent(
      data, dialogRef, brandService
    );

    component.ngOnInit();
  });

  it('should close dialog', () => {
    component.closeDialog();
    expect(dialogRef.close).toHaveBeenCalled();
  });
});
