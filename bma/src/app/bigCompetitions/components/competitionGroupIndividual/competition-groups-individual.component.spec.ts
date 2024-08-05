import {
  CompetitionGroupIndividualComponent
} from '@app/bigCompetitions/components/competitionGroupIndividual/competition-groups-individual.component';

describe('CompetitionGroupIndividualComponent', () => {

  let component: CompetitionGroupIndividualComponent;

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

    component = new CompetitionGroupIndividualComponent();
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', () => {
    component.moduleConfig = moduleConfig;
    component.ngOnInit();
    expect(component.numberQualifiers).toBe(moduleConfig.groupModuleData.numberQualifiers);
    expect(component.individualModuleData).toBe(moduleConfig.groupModuleData.data[0]);
  });

  it('#ngOnInit when groupModuleData.data is not array', () => {
    moduleConfig.groupModuleData.data = 'data';
    component.moduleConfig = moduleConfig;
    component.ngOnInit();
    expect(component.individualModuleData).toBeUndefined();
  });

  it('should return correct result', () => {
    const index = 1;
    component.numberQualifiers = 3;
    expect(component.getQualifiedClass(index)).toBe('team-qualified');
  });

  it('should return correct result', () => {
    const index = 3;
    component.numberQualifiers = 3;
    expect(component.getQualifiedClass(index)).toBe('');
  });

  it('should return correct result', () => {
    const element = {
      competitionId: 34,
      seasonId: 4553,
      tableId: 56,
      tableName: '',
      teams: [],
      ssEvents: []
    };
    const i = 5;
    expect(component.trackByTeams(i, element)).toBe('5_34');
  });
});
