import { OutrightModuleComponent } from './market-list.component';

describe('OutrightModuleComponent', () => {
  let component: OutrightModuleComponent;
  let dialog;
  let dialogService;
  let snackBar;
  let bigCompetitionApiService;

  beforeEach(() => {
    dialog = {};
    dialogService = {};
    snackBar = {};
    bigCompetitionApiService = {};

    component = new OutrightModuleComponent(
      dialog, dialogService, snackBar, bigCompetitionApiService
    );
  });

  it('ngOnInit', () => {
    component.module = { markets: [] } as any;
    component.ngOnInit();
    expect(component.competitionMarkets).toBe(component.module.markets);
  });
});
