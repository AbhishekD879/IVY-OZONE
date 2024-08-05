import {CompetitionModuleEditComponent} from './competition-module-edit.component';
import { of } from 'rxjs';

describe('CompetitionModuleEditComponent', () => {
  let component,
    componentFactoryResolver,
    bigCompetitionApiService,
    activatedRoute,
    bigCompetitionService,
    dialogService,
    router,
    apiClientService,
    brandService,
    globalLoaderService;

  beforeEach(() => {
    componentFactoryResolver = {};
    bigCompetitionApiService = {
      getSingleModule: jasmine.createSpy('bigCompetitionService.getSingleModule').and.returnValue(of({
        body: {}
      }))
    };
    activatedRoute = {
      params: of({
        id: 'mockId'
      })
    };
    bigCompetitionService = {

    };
    dialogService = {};
    router = {};

    component = new CompetitionModuleEditComponent(
      componentFactoryResolver,
      bigCompetitionApiService,
      activatedRoute,
      bigCompetitionService,
      dialogService,
      router,
      apiClientService,
      brandService,
      globalLoaderService
    );

    component.ngOnInit();
  });

  it('should create', () => {
    expect(component.routeState).toBeDefined();
    expect(component.competition).toBeDefined();
  });
});
