import { of } from 'rxjs';
import { CompetitionsListComponent } from './competitions-list.component';

describe('CompetitionsListComponent', () => {
  let component: CompetitionsListComponent;
  let dialogService;
  let dialog;
  let bigCompetitionApiService;

  beforeEach(() => {
    dialogService = {};
    dialog = {};
    bigCompetitionApiService = {
      getCompetitionsList: jasmine.createSpy('getCompetitionsList').and.returnValue(of({}))
    };

    component = new CompetitionsListComponent(
      dialogService, dialog, bigCompetitionApiService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(bigCompetitionApiService.getCompetitionsList).toHaveBeenCalled();
  });
});
