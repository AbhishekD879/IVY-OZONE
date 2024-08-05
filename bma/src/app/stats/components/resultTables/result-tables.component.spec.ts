import { ResultTablesComponent } from './result-tables.component';
import { of as observableOf, throwError } from 'rxjs';
import { IStatsResults } from '../../models/results.model';

const resultsMock = [
  {
      areaId: '1',
      competitionId: '1',
      rows: [],
      seasonId: '1',
      sportId: '1',
      tableId: '1',
      tableName: 'test_table_1',
      __v: 1,
      _id: '1'
  }
];

describe('#ResultTablesComponent', () => {
  let component: ResultTablesComponent;

  let leagueService, route;

  beforeEach(() => {
    leagueService = {
      getStandings: jasmine.createSpy('leagueService.getStandings')
        .and.returnValue( observableOf([{areaId: '1'}] as IStatsResults[] ))
    } as any;
    route = {
      params: observableOf({
        competitionId: '1',
        seasonId: '1'
      })
    } as any;

    component = new ResultTablesComponent(
      leagueService,
      route
    );

    component.showSpinner = jasmine.createSpy('showSpinner');
    component.hideSpinner = jasmine.createSpy('hideSpinner');
  });

  describe('#ngOnInit', () => {
    it('Set results', () => {
      leagueService.getStandings.and.returnValue(observableOf(resultsMock));

      component.ngOnInit();

      expect(component.showSpinner).toHaveBeenCalled();
      expect(component.results).toEqual(resultsMock);
      expect(component.hideSpinner).toHaveBeenCalled();
    });

    it('Throw error', () => {
      leagueService.getStandings.and.returnValue(throwError('error'));
      component.showError = jasmine.createSpy('showError');

      component.ngOnInit();

      expect(component.showError).toHaveBeenCalled();
    });
  });

  it('#getTableValue', () => {
    const values = [
      {key: 'key_1', value: 'value_1'},
      {key: 'key_2', value: 'value_2'},
      {key: 'key_3', value: 'value_3'},
    ];

    const result = component.getTableValue(values, 'key_1');

    expect(result).toBe('value_1');
  });
});
