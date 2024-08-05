import {MatchesListComponent} from './matches-list.component';

describe('MatchListComponent', () => {
  let component,
    dialog,
    dialogService,
    bigCompetitionApiService;

  const mockEvents = [];

  beforeEach(() => {
    dialog = {};
    dialogService = {};
    bigCompetitionApiService = {};

    component = new MatchesListComponent(
      dialog,
      dialogService,
      bigCompetitionApiService
    );

    component.competitionModule = {
      knockoutModuleData: {
        events: mockEvents
      }
    };

    component.ngOnInit();
  });

  it('should create', () => {
    expect(component.matches).toEqual(mockEvents);
  });
});
