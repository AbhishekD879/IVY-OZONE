import { MatchResultsSportTabComponent } from '@sb/components/matchResultsSportTab/match-results-sport-tab.component';
import { commandApi } from '@core/services/communication/command/command-api.constant';
import { fakeAsync, tick } from '@angular/core/testing';

describe('MatchResultsSportTabComponent', () => {
  let component: MatchResultsSportTabComponent;
  let filtersService: any;
  let commandService: any;

  beforeEach(() => {
    commandService = jasmine.createSpyObj('commandService', ['executeAsync']);
    filtersService = jasmine.createSpyObj('filtersService', ['orderBy']);

    commandService.API = commandApi;

    component = new MatchResultsSportTabComponent(commandService, filtersService);
  });

  it('ngOnInit should call showMoreDates method', () => {
    spyOn(component, 'showMoreDates');

    component.ngOnInit();

    expect(component.showMoreDates).toHaveBeenCalled();
  });

  describe('loadMatchesByDate', () => {
    let data: any;

    beforeEach(() => {
      data = {
        opened: false,
        date: 'some date',
        competitions: [
          {
            prop: 'test-prop'
          }
        ]
      };
    });

    it('should not call executeAsync method if length fo competitions is more than 0', () => {
      component.loadMatchesByDate(data);

      expect(commandService.executeAsync).not.toHaveBeenCalled();
    });

    it('should call executeAsync method if length fo competitions is 0', fakeAsync(() => {
      commandService.executeAsync.and.returnValue(Promise.resolve('data'));

      data.competitions = [];

      component.loadMatchesByDate(data);

      tick();

      expect(commandService.executeAsync).toHaveBeenCalledWith(commandApi.GET_MATCHES_BY_DATE, ['some date'], []);
    }));

    it('should return correct result if promise rejected', fakeAsync(() => {
      commandService.executeAsync.and.returnValue(Promise.reject());

      data.competitions = [];
      data.noResults = false;

      component.loadMatchesByDate(data);

      tick();

      expect(commandService.executeAsync).toHaveBeenCalled();
      expect(data.noResults).toBeTruthy();
    }));
  });

  it('showMoreDates should return correct value', fakeAsync(() => {
    commandService.executeAsync.and.returnValue(Promise.resolve([1]));
    filtersService.orderBy.and.returnValue('test');

    component['dates'] = [
      {
        competitions: [
          {
            matches: 'some text'
          }
        ]
      }
    ] as any;

    component['page'] = 1;

    component.showMoreDates();

    tick();

    expect(commandService.executeAsync).toHaveBeenCalled();
    expect(component['dates'].length).toEqual(2);
    expect(component['page']).toEqual(2);
  }));

  it('trackDatesByFn should return correct result', () => {
    expect(component.trackDatesByFn(2)).toEqual(2);
  });

  it('trackCompetitionsByFn should return correct result', () => {
    expect(component.trackCompetitionsByFn(2)).toEqual(2);
  });

  it('trackMatchesByFn should return correct result', () => {
    expect(component.trackMatchesByFn(2)).toEqual(2);
  });
});
