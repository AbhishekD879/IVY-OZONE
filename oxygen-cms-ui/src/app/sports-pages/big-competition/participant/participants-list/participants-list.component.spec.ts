import { of } from 'rxjs';
import { ParticipantsListComponent } from './participants-list.component';

describe('ParticipantsListComponent', () => {
  let component: ParticipantsListComponent;
  let dialog;
  let dialogService;
  let activatedRoute;
  let bigCompetitionApiService;

  beforeEach(() => {
    dialog = {
      open: jasmine.createSpy('open').and.returnValue({
        afterClosed: jasmine.createSpy('afterClosed').and.returnValue(of(null))
      })
    };
    dialogService = {};
    activatedRoute = {};
    bigCompetitionApiService = {};

    component = new ParticipantsListComponent(
      dialog, dialogService, activatedRoute, bigCompetitionApiService
    );
  });

  it('createParticipant', () => {
    component.createParticipant();
    expect(dialog.open).toHaveBeenCalled();
  });
});
