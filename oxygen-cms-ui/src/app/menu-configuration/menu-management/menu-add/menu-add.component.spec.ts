import { MenuAddComponent } from './menu-add.component';

describe('MenuAddComponent', () => {
  let component: MenuAddComponent;
  let dialogRef;

  beforeEach(() => {
    dialogRef = {
      close: jasmine.createSpy('close')
    };
    component = new MenuAddComponent(dialogRef);
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.menuItem).toBeDefined();
    expect(component.form).toBeDefined();
  });

  it('close', () => {
    component.closeDialog();
    expect(dialogRef.close).toHaveBeenCalled();
  });
});
