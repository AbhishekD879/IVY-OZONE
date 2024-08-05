import {GroupWidgetComponent} from './group-widget.component';
import { of } from 'rxjs';

describe('GroupWidgetComponent', () => {
  let component,
    bigCompetitionApiService,
    activatedRoute,
    bigCompetitionService;

  beforeEach(() => {
    bigCompetitionApiService = {
      getSingleCompetition: jasmine.createSpy('getSingleCompetition').and.returnValue(of({
        body: {
          competitionTabs: []
        }
      })),
      getCompetitionGroups: jasmine.createSpy('getCompetitionGroups').and.returnValue(of({
        body: {
          allCompetitions: []
        }
      }))
    };
    activatedRoute = {
      params: of({
        id: 'mockId'
      })
    };
    bigCompetitionService = {
      parseCompetitionGroupsData: jasmine.createSpy('parseCompetitionGroupsData').and.returnValue({
        groupsNames: ['groupsNames'],
        seasonsNames: ['seasonsNames'],
        groupsNotFound: ['groupsNotFound']
      }),
      setGroupCurrentValue: jasmine.createSpy('setGroupCurrentValue'),
      setSeasonCurrentValue: jasmine.createSpy('setSeasonCurrentValue'),
      getAllPaths: jasmine.createSpy('getAllPaths')
    };

    component = new GroupWidgetComponent(
      bigCompetitionApiService,
      activatedRoute,
      bigCompetitionService
    );

    component.module = {
      groupModuleData: {}
    };

    component.ngOnInit();
  });

  it('should create', () => {
    expect(component.statsCenterGroups).toBeDefined();
    expect(component.seasonsNames).toEqual(['seasonsNames']);
    expect(component.groupsNotFound).toEqual(['groupsNotFound']);
  });
});
