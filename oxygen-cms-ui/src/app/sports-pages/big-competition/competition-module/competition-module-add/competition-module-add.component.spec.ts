import {CompetitionModuleAddComponent} from './competition-module-add.component';

describe('CompetitionModuleAddComponent', () => {
  let component,
    dialogRef,
    brandService,
    bigCompetitionService;

  beforeEach(() => {
    brandService = {
      brand: 'coral'
    };
    dialogRef = {
      close: jasmine.createSpy('dialogRef.close')
    };
    bigCompetitionService = {};

    component = new CompetitionModuleAddComponent(
      dialogRef,
      brandService,
      bigCompetitionService
    );

    component.ngOnInit();
  });

  it('should init', () => {
    expect(component.moduleTypes).toBeDefined();
    expect(component.newModule).toBeDefined();
    expect(component.form).toBeDefined();
  });

  it('should close dialog', () => {
    component.closeDialog();
    expect(dialogRef.close).toHaveBeenCalled();
  });
});
