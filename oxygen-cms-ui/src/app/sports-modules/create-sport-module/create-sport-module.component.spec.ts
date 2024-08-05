import { CreateSportModuleComponent } from './create-sport-module.component';

describe('CreateSportModuleComponent', () => {
  let component,
    data,
    dialogRef;

  beforeEach(() => {
    data = {
      data: {
        sportModules: []
      }
    };
    dialogRef = {};

    component = new CreateSportModuleComponent(
      data,
      dialogRef
    );

    component.ngOnInit();
  });

  it('should Init', () => {
    expect(component.createdSportModules).toBeDefined();
    expect(component.moduleName).toEqual('Quick Links Module');
    expect(component.moduleType).toEqual('QUICK_LINK');
  });
});
