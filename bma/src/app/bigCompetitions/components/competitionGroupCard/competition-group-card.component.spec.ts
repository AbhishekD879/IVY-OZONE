import {
  CompetitionGroupCardComponent
} from '@app/bigCompetitions/components/competitionGroupCard/competition-group-card.component';

describe('CompetitionGroupCardComponent', () => {
  let component: CompetitionGroupCardComponent;

  beforeEach(() => {
    component = new CompetitionGroupCardComponent();
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', () => {
    component.redirectLink = '/redirectLink';
    component.groupData = {
      competitionId: 32,
      seasonId: 34898,
      tableId: 1,
      tableName: 'name',
      teams: [],
      ssEvents: []
    };
    component.ngOnInit();
    expect(component.redirectLink).toBe('/big-competition/redirectLink');
    expect(component.groupData.tableName).toBe('e');
  });

  it('#ngOnInit when redirectLink is empty', () => {
    component.redirectLink = '';
    component.groupData = {
      competitionId: 32,
      seasonId: 34898,
      tableId: 1,
      tableName: 'name',
      teams: [],
      ssEvents: []
    };
    component.ngOnInit();
    expect(component.redirectLink).toBeFalsy();
    expect(component.groupData.tableName).toBe('e');
  });

  it('should return correct class name', () => {
    component.numberQualifiers = 3;
    const className = component.getQualifiedClass(1);
    expect(className).toBe('team-qualified');
  });

  it('should return correct class name', () => {
    component.numberQualifiers = 3;
    const className = component.getQualifiedClass(3);
    expect(className).toBe('');
  });

  it('should return correct result', () => {
    const element = {
      name: 'name',
      obName: 'obName'
    };
    expect(component.trackByTeam(2, element)).toBe('2_name');
  });
});
