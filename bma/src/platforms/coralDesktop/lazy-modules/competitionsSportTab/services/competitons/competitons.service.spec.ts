import { CompetitionsService } from '@coralDesktop/lazy-modules/competitionsSportTab/services/competitons/competitons.service';
import { fakeAsync, tick } from '@angular/core/testing';

describe('Coral competitions service', () => {
  let service: CompetitionsService;
  let сurrentMatchesService;
  let gridHelperService;
  let routingHelperService;
  let routingState;
  let route;

  beforeEach(() => {
    const mockClasses = [{
      id: 1
    }, {
      id: 2
    }] as any;

    сurrentMatchesService = {
      getAllClasses: jasmine.createSpy('getAllClasses').and.returnValue(Promise.resolve(mockClasses)),
      filterInitialClasses: jasmine.createSpy('filterInitialClasses').and.returnValue(['1', '2', '3'] as any)
    };
    gridHelperService = {};
    routingHelperService = {};
    routingState = {};
    route = {};

    service = new CompetitionsService(
      сurrentMatchesService, gridHelperService, routingHelperService, routingState, route);
  });

  it('getClassesWithTypes', fakeAsync(() => {
    service.getClassesWithTypes({ popular: ['1'], all: ['1', '2'] }, '16').subscribe(data => {
      expect(data).toEqual([['1', '2', '3'], ['1', '2', '3']]);
    });
    tick();
  }));
});
