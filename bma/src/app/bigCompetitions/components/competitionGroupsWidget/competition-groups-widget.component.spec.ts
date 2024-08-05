import {
  CompetitionGroupsWidgetComponent
} from '@app/bigCompetitions/components/competitionGroupsWidget/competition-groups-widget.component';

describe('CompetitionGroupsWidgetComponent', () => {

  let component: CompetitionGroupsWidgetComponent;

  let moduleConfig;

  beforeEach(() => {
    moduleConfig = {
      id: 'id',
      name: 'name',
      type: '',
      maxDisplay: 10,
      viewType: 'inplay',
      aemPageName: '',
      isExpanded: false,
      markets: [],
      specialModuleData: {
        typeIds: [],
        eventIds: [],
        linkUrl: ''
      },
      groupModuleData: {
        sportId: 12,
        areaId: 32,
        competitionId: 34,
        seasonId: 43,
        numberQualifiers: 11,
        details: null,
        data: [
          {
            competitionId: 32,
            seasonId: 32443,
            tableId: 43,
            tableName: '',
            teams: [],
            ssEvents: []
          }
        ]
      },
      events: [],
      errors: [],
      results: []
    };

    component = new CompetitionGroupsWidgetComponent();
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', () => {
    component.moduleConfig = moduleConfig;
    component.ngOnInit();
    expect(component.groupsData).toBe(moduleConfig.groupModuleData);
  });

  it('should return correct result', () => {
    const element = {
      competitionId: 57,
      seasonId: 3425,
      tableId: 98,
      tableName: '',
      teams: [],
      ssEvents: []
    };
    const i = 7;
    expect(component.trackByTeams(i, element)).toBe('7_57');
  });
});
