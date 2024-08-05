import { of } from 'rxjs';
import { ParticipantEditComponent } from './participant-edit.component';

describe('ParticipantEditComponent', () => {
  let component: ParticipantEditComponent;
  let dialogService;
  let router;
  let activatedRoute;
  let bigCompetitionApiService;
  let snackBar;

  beforeEach(() => {
    dialogService = {};
    router = {};
    activatedRoute = {
      params: of({})
    };
    bigCompetitionApiService = {
      getSingleParticipant: jasmine.createSpy('getSingleParticipant').and.returnValue(of({}))
    };
    snackBar = {};

    component = new ParticipantEditComponent(
      dialogService, router, activatedRoute, bigCompetitionApiService, snackBar
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(bigCompetitionApiService.getSingleParticipant).toHaveBeenCalled();
  });
});
