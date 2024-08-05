import {CompetitionSubTabEditComponent} from './competition-sub-tab-edit.component';
import { of } from "rxjs";

describe('CompetitionSubTabEditComponent', () => {
  let component: CompetitionSubTabEditComponent;
  let spaceToDashPipe, dialogService, router, activatedRoute, bigCompetitionApiService, bigCompetitionService;

  beforeEach(() => {
    spaceToDashPipe = {};
    dialogService = {};
    router = {};
    activatedRoute = {
      params: of({
        competitionId: 1,
        tabId: 2,
        subTabId: 3
      })
    };
    bigCompetitionApiService = {
      getSingleSubTab: jasmine.createSpy('getSingleSubTab').and.returnValue(of({body: {}}))
    };
    bigCompetitionService = {};

    component = new CompetitionSubTabEditComponent(spaceToDashPipe, dialogService, router, activatedRoute, bigCompetitionApiService, bigCompetitionService);
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(bigCompetitionApiService.getSingleSubTab).toHaveBeenCalledWith(1, 2, 3);
  });
});
