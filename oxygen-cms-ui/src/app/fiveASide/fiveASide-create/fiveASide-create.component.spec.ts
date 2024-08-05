import {FiveASideCreateComponent} from './fiveASide-create.component';

describe('MarketSelectorCreateComponent', () => {
  let component: FiveASideCreateComponent;
  let dialogRef;
  let brandService;

  beforeEach(() => {
    dialogRef = {
      close: jasmine.createSpy('close')
    };
    brandService = {
      brand: 'Test Brand'
    };

    component = new FiveASideCreateComponent(
      dialogRef,
      brandService
    );
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit should create formation object', () => {
    component.ngOnInit();
    const expectResult = {
      id: null,
      createdAt: null,
      createdBy: null,
      updatedByUserName: null,
      createdByUserName: null,
      updatedAt: null,
      updatedBy: null,
      brand: brandService.brand,

      title: '',
      actualFormation: '',
      position1: '',
      stat1: null,
      position2: '',
      stat2: null,
      position3: '',
      stat3: null,
      position4: '',
      stat4: null,
      position5: '',
      stat5: null,
      sortOrder: 0
    };
    expect(component.fiveASideFormation).toEqual(expectResult);
    expect(component.form).toBeTruthy();
  });

  it('#closeDialog should call dialogRef.close', () => {
    component.closeDialog();
    expect(dialogRef.close).toHaveBeenCalled();
  });

});
