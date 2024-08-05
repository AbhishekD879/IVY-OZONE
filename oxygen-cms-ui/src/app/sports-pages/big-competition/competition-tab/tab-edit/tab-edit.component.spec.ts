import { TabEditComponent } from './tab-edit.component';
import { of } from "rxjs";

describe('TabEditComponent', () => {
  let component: TabEditComponent;
  let spaceToDashPipe, dialogService, router, activatedRoute, bigCompetitionApiService, bigCompetitionService;


  beforeEach(() => {
    spaceToDashPipe = {};
    dialogService = {};
    router = {};
    activatedRoute = {
      params: of({
        competitionId: 1,
        tabId: 2
      })
    };
    bigCompetitionApiService = {
      getSingleCompetitionTab: jasmine.createSpy('getSingleCompetitionTab').and.returnValue(of({}))
    };
    bigCompetitionService = {};

    component = new TabEditComponent(spaceToDashPipe, dialogService, router, activatedRoute, bigCompetitionApiService, bigCompetitionService);
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(bigCompetitionApiService.getSingleCompetitionTab).toHaveBeenCalledWith(1, 2);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
