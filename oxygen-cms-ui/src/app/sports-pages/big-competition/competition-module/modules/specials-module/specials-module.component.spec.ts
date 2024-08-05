import { SpecialsModuleComponent } from './specials-module.component';

describe('SpecialsModuleComponent', () => {
  let component: SpecialsModuleComponent;
  let snackBar;
  let globalLoaderService;
  let bigCompetitionAPIService;

  beforeEach(() => {
    snackBar = {};
    globalLoaderService = {};
    bigCompetitionAPIService = {};

    component = new SpecialsModuleComponent(
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
