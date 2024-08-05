import { of } from 'rxjs';
import { CompetitionEditComponent } from './competition-edit.component';

describe('CompetitionEditComponent', () => {
  let component: CompetitionEditComponent;
  let spaceToDashPipe;
  let dialogService;
  let activatedRoute;
  let router;
  let bigCompetitionApiService;
  let bigCompetitionService;
  let brandService;

  beforeEach(() => {
    spaceToDashPipe = {};
    dialogService = {};
    activatedRoute = {
      params: of({})
    };
    router = {};
    bigCompetitionApiService = {
      getSingleCompetition: jasmine.createSpy('getSingleCompetition').and.returnValue(of({}))
    };
    bigCompetitionService = {};
    brandService = {};

    component = new CompetitionEditComponent(
      spaceToDashPipe, dialogService, activatedRoute, router,
      bigCompetitionApiService, bigCompetitionService, brandService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(bigCompetitionApiService.getSingleCompetition).toHaveBeenCalled();
  });
});
