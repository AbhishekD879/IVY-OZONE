import {MatchEditComponent} from './match-edit.component';
import { of } from 'rxjs';

describe('RoundNamesEditComponent', () => {
  let component,
    bigCompetitionApiService,
    activatedRoute,
    bigCompetitionService,
    router;

  beforeEach(() => {
    bigCompetitionApiService = {
      getSingleModule: jasmine.createSpy('getSingleModule').and.returnValue(of({
        body: {
          competitionTabs: [{
            competitionSubTabs: [],
            competitionModules: [{
              knockoutModuleData: {
                rounds: [{
                  name: 'roundname'
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

    component = new MatchEditComponent(
      bigCompetitionApiService,
      activatedRoute,
      bigCompetitionService,
      router
    );

    component.dateTimeComponent = {
      setDayTime: jasmine.createSpy('setDayTime')
    };

    component.ngOnInit();
  });

  it('should create', () => {
    expect(component.form).toBeDefined();
    expect(component.module).toBeDefined();
    expect(component.match).toBeDefined();
  });
});
