import { TabsListComponent } from './tabs-list.component';

describe('TabsListComponent', () => {
  let component: TabsListComponent;
  let dialog, snackBar, dialogService, activatedRoute, bigCompetitionApiService, spaceToDashPipe;

  beforeEach(() => {
    dialog = {};
    snackBar = {};
    dialogService = {};
    activatedRoute = {};
    bigCompetitionApiService = {};
    spaceToDashPipe = {};

    component = new TabsListComponent(dialog, snackBar, dialogService, activatedRoute, bigCompetitionApiService, spaceToDashPipe);
    component.ngOnInit();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
