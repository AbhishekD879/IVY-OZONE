import { of } from 'rxjs';
import { ResultsModuleComponent } from './results-module.component';

describe('ResultsModuleComponent', () => {
  let component: ResultsModuleComponent;
  let bigCompetitionApiService;
  let activatedRoute;
  let bigCompetitionService;

  beforeEach(() => {
    bigCompetitionApiService = {
      getCompetitionGroups: jasmine.createSpy('getCompetitionGroups').and.returnValue(of({}))
    };
    activatedRoute = {
      params: of({})
    };
    bigCompetitionService = {
      parseCompetitionSeasonsData: jasmine.createSpy('parseCompetitionSeasonsData').and.returnValue({})
    };

    component = new ResultsModuleComponent(
      bigCompetitionApiService, activatedRoute, bigCompetitionService
    );
    component.module = {} as any;
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(bigCompetitionApiService.getCompetitionGroups).toHaveBeenCalled();
  });
});
