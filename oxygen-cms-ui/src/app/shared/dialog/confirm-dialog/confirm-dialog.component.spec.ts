import { ConfirmDialogComponent } from './confirm-dialog.component';

describe('ConfirmDialogComponent', () => {
  let component,
    dialogRef,
    data;

  beforeEach(() => {
    dialogRef = {
      close: jasmine.createSpy('dialogRef.close')
    };
    data = {};

    component = new ConfirmDialogComponent(
      dialogRef,
      data
    );
  });

  it('should close dialog', () => {
    component.onNoClick();

    expect(dialogRef.close).toHaveBeenCalled();
  });
});
