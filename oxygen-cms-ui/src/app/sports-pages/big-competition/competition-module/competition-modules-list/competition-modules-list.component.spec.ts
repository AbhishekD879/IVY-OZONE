import {CompetitionModulesListComponent} from './competition-modules-list.component';
import { of } from 'rxjs';

describe('CompetitionModulesListComponent', () => {
  let component,
    snackBar,
    dialogService,
    dialog,
    activatedRoute,
    bigCompetitionApiService;

  beforeEach(() => {
    snackBar = {};
    dialogService = {
      showNotificationDialog: jasmine.createSpy('showNotificationDialog')
    };
    dialog = {
      open: jasmine.createSpy('dialog.open').and.returnValue({
        afterClosed: jasmine.createSpy('afterClosed').and.returnValue(of({
          id: 'Module mockId',
          name: 'Module name',
        }))
      })
    };
    activatedRoute = {
      params: of({
        id: 'mock'
      })
    };
    bigCompetitionApiService = {
      createSubTabModule: jasmine.createSpy('createSubTabModule').and.returnValue(of({
        body: {}
      }))
    };

    component = new CompetitionModulesListComponent(
      snackBar,
      dialogService,
      dialog,
      activatedRoute,
      bigCompetitionApiService
    );

    component.ngOnInit();
  });

  it('should createModule', () => {
    component.createModule();

    expect(component.modulesList.length).toEqual(1);

    expect(bigCompetitionApiService.createSubTabModule).toHaveBeenCalled();
    expect(dialogService.showNotificationDialog).toHaveBeenCalled();
  });
});
