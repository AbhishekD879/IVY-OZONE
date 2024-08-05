import { CmsSimpleSelectListComponent } from './cms-simple-select-list.component';

describe('CmsSimpleAutocompleteComponent', () => {
  let component;

  beforeEach(() => {
    component = new CmsSimpleSelectListComponent();

    component.ngOnInit();
  });

  it('should Emit changes', () => {
    spyOn(component.onDataChange, 'emit');

    component.onChange();

    expect(component.onDataChange.emit).toHaveBeenCalled();
  });
});
