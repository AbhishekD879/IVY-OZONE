import { ParentSportsCreateComponent } from './parent-sports-create.component';

describe('ParentSportsCreateComponent', () => {
  let component: ParentSportsCreateComponent;
  let brandService;
  let dialogRef;

  beforeEach(() => {
    brandService = {};
    dialogRef = {
      close: jasmine.createSpy('close')
    };

    component = new ParentSportsCreateComponent(brandService, dialogRef);
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.newParentSport).toBeDefined();
    expect(component.form).toBeDefined();
  });

  it('closeDialog', () => {
    component.closeDialog();
    expect(dialogRef.close).toHaveBeenCalled();
  });

  it('getParentSport', () => {
    component.newParentSport = {} as any;
    component.form = {
      value: { name: 'sport' }
    } as any;
    expect(component.getParentSport()).toEqual({ title: 'sport' });
  });
});
