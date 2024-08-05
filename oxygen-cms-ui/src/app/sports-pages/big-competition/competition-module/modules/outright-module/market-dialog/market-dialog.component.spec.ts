import { MarketDialogComponent } from './market-dialog.component';

describe('MarketDialogComponent', () => {
  let component: MarketDialogComponent;
  let dialogRef;
  let bigCompetitionApiService;

  beforeEach(() => {
    dialogRef = {};
    bigCompetitionApiService = {};

    component = new MarketDialogComponent(
      dialogRef, bigCompetitionApiService, {}
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(component.marketIsValid).toBeFalsy();
  });
});
