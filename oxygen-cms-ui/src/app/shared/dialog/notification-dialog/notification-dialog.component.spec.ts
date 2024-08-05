import {NotificationDialogComponent} from './notification-dialog.component';

describe('NotificationDialogComponent', () => {
  let component,
    dialogRef,
    data;

  beforeEach(() => {
    dialogRef = {
      close: jasmine.createSpy('dialogRef.close')
    };
    data = {};

    component = new NotificationDialogComponent(
      dialogRef,
      data
    );
  });

  it('should close dialog', () => {
    component.onNoClick();

    expect(dialogRef.close).toHaveBeenCalled();
  });
});
