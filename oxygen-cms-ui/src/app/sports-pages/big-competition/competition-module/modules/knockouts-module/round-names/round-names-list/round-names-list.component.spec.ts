import {RoundNamesListComponent} from './round-names-list.component';

describe('RoundNamesListComponent', () => {
  let component,
    dialogService,
    dialog,
    bigCompetitionApiService,
    snackBar;

  const mockRounds = [];

  beforeEach(() => {
    dialogService = {};
    dialog = {};
    bigCompetitionApiService = {};
    snackBar = {};

    component = new RoundNamesListComponent(
      dialogService,
      dialog,
      bigCompetitionApiService,
      snackBar
    );

    component.competitionModule = {
      knockoutModuleData: {
        rounds: mockRounds
      }
    };

    component.ngOnInit();

  });

  it('should create', () => {
    expect(component.roundNames).toEqual(mockRounds);
  });
});
