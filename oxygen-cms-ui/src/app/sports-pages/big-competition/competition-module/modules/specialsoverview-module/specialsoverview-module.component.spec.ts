import { SpecialsoverviewModuleComponent } from './specialsoverview-module.component';

describe('SpecialsoverviewModuleComponent', () => {
  let component: SpecialsoverviewModuleComponent;
  let snackBar;
  let globalLoaderService;
  let bigCompetitionAPIService;

  beforeEach(() => {
    snackBar = {};
    globalLoaderService = {};
    bigCompetitionAPIService = {};

    component = new SpecialsoverviewModuleComponent(
      snackBar, globalLoaderService, bigCompetitionAPIService
    );
    component.module = {
      specialModuleData: { typeIds: [], eventIds: [] }
    } as any;
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.loadedTypeIds).toBe(component.module.specialModuleData.typeIds);
    expect(component.loadedEventIds).toBe(component.module.specialModuleData.eventIds);
  });
});
