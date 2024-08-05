import { PromptDialogComponent } from './prompt-dialog.component';

describe('PromptDialogComponent', () => {
  let component,
    dialogRef,
    data;

  beforeEach(() => {
    dialogRef = {
      close: jasmine.createSpy('dialogRef.close')
    };
    data = {};

    component = new PromptDialogComponent(
      dialogRef,
      data
    );
  });

  it('should close dialog', () => {
    component.onNoClick();

    expect(dialogRef.close).toHaveBeenCalled();
  });
});
