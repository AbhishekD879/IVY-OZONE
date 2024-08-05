import { FilterCreateComponent } from '@app/betpack-market-place/filter/create-filter/filter-create.component';
import { EditNewFilterMock, EditNewFilterMock1, EditNewFilterMock2, NewFilterMock, NewFilterMockemp } from '@app/betpack-market-place/betpack-mock';

describe('FilterCreateComponent', () => {
  let component: FilterCreateComponent;
  let dialogRef;
  let brandService;

  beforeEach(() => {
    dialogRef = {
      close: jasmine.createSpy('close')
    };
    brandService = {};

    component = new FilterCreateComponent(dialogRef, brandService);
  });
  
  it('ngOnInit1', () => {
    component.newFilter = NewFilterMockemp;
    component.isHaveAll = false;
    component.isSpecialCar = false;
    component.ngOnInit();
    expect(component.isValid()).toBe(true);
  });

  it('closeDialog', () => {
    component.closeDialog();
    expect(dialogRef.close).toHaveBeenCalled();
  });
  it('filterCheck', () => {
    component.newFilter = NewFilterMock;
    // component.filterCheck('All');
  });
  it('filterCheck', () => {
    component.newFilter = NewFilterMock;
    // component.filterCheck('All@');
  });
  it('filterCheck', () => {
    component.newFilter = NewFilterMock;
    // component.filterCheck('Alll');
  });
  it('ngOnInit2', () => {
    component.isHaveAll = true;
    component.isSpecialCar = false;
    component.ngOnInit();
    expect(component.isValid).toBeTruthy();
  });
  it('isValid', () => {
    component.newFilter = EditNewFilterMock;
    expect(component.isValid()).toBe(true);
  });
  it('isValid1', () => {
    component.newFilter = EditNewFilterMock1;
    expect(component.isValid()).toBe(true);
  });
  it('isValid2', () => {
    component.newFilter = EditNewFilterMock2;
    expect(component.isValid()).toBe(true );
  });
});
