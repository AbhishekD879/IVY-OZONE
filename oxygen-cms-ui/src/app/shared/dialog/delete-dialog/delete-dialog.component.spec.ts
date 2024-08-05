import { DeleteDialogComponent } from './delete-dialog.component';

describe('DeleteDialogComponent', () => {
  let component: DeleteDialogComponent;
  let dialogRef;

  beforeEach(() => {
    dialogRef = {
      close: jasmine.createSpy('close')
    };
    component = new DeleteDialogComponent(dialogRef, {});
  });

  it('onNoClick', () => {
    component.onNoClick();
    expect(dialogRef.close).toHaveBeenCalled();
  });
});
