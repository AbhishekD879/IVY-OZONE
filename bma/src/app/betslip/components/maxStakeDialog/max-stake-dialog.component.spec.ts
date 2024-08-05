import { MaxStakeDialogComponent } from './max-stake-dialog.component';

describe('MaxStakeDialogComponent', () => {
  let component, device, windowRef;

  beforeEach(() => {
    device = {};
    windowRef = {};
    component = new MaxStakeDialogComponent(device, windowRef);
  });

  it('ngOnInit should call super.ngOnInit and set text value', () => {
    const mockText = 123;
    const parentNgOnInit = spyOn(MaxStakeDialogComponent.prototype['__proto__'], 'ngOnInit');
    component.params = { text: mockText };
    component.ngOnInit();

    expect(parentNgOnInit).toHaveBeenCalled();
    expect(component.text).toEqual(mockText);
  });
});
