import { CompetitionSubTabsListComponent } from './competition-sub-tabs-list.component';
import { of } from "rxjs";

describe('CompetitionSubTabsListComponent', () => {
  let component: CompetitionSubTabsListComponent;
  let dialog, dialogService, snackBar, activatedRoute, bigCompetitionApiService, spaceToDashPipe;
  let tab;


  beforeEach(() => {
    dialog = {};
    dialogService = {
      showConfirmDialog: jasmine.createSpy('showConfirmDialog')
    };
    snackBar = {};
    activatedRoute = {
      params: of({
        competitionId: 1,
        tabId: 2,
        id: 3
      })
    };
    bigCompetitionApiService = {
      deleteSubTab: jasmine.createSpy('deleteSubTab').and.returnValue(of({}))
    };
    spaceToDashPipe = {};

    tab = {
      name: 'Competition',
      uri: '',
      displayOrder: 1,
      enabled: true,
      hasSubtabs: false,
      competitionSubTabs: [],
      competitionModules: []
    };

    component = new CompetitionSubTabsListComponent(dialog, dialogService, snackBar, activatedRoute, bigCompetitionApiService, spaceToDashPipe);
  });

  it('It should remove tab', () => {
    component.removeTab(tab);
    expect(dialogService.showConfirmDialog).toHaveBeenCalledWith({
      title: 'Remove Sub Tab',
      message: 'Are You Sure You Want to Remove Sub Tab?',
      yesCallback: jasmine.any(Function)
    });
  })
});
