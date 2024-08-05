import {RoundNamesEditComponent} from './round-names-edit.component';
import { of } from 'rxjs';

describe('RoundNamesEditComponent', () => {
  let component,
    bigCompetitionApiService,
    activatedRoute,
    bigCompetitionService,
    router,
    snackBar;

  beforeEach(() => {
    bigCompetitionApiService = {
      getSingleModule: jasmine.createSpy('getSingleModule').and.returnValue(of({
        body: {
          competitionTabs: [{
            competitionSubTabs: [],
            competitionModules: [{
              knockoutModuleData: {
                rounds: [{
                  name: 'roundname',
                  abbreviation: 'mockAbbreviation'
                }],
                events: [{
                  round: 'roundname',
                  abbreviation: 'mockAbbreviation'
                }]
              }
            }]
          }],
        }
      }))
    };
    activatedRoute = {
      params: of({
        abbreviation: 'mockAbbreviation',
        id: 'mockId'
      })
    };
    bigCompetitionService = {
      breadcrumbParser: jasmine.createSpy('breadcrumbParser').and.returnValue([])
    };
    router = {};
    snackBar = {};

    component = new RoundNamesEditComponent(
      bigCompetitionApiService,
      activatedRoute,
      bigCompetitionService,
      router,
      snackBar
    );
    component.ngOnInit();
  });

  it('should initialise', () => {
    expect(component.module).toBeDefined();
    expect(component.breadcrumbsData).toBeDefined();
    expect(component.form).toBeDefined();
  });
});
