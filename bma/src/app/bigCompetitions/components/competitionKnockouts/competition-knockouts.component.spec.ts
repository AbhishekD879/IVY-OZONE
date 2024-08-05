import { fakeAsync, tick } from '@angular/core/testing';
import {
  CompetitionKnockoutsComponent
} from '@app/bigCompetitions/components/competitionKnockouts/competition-knockouts.component';
import { IBCModule } from '@app/bigCompetitions/services/bigCompetitions/big-competitions.model';
import { IEventsByRoundMap } from '@app/bigCompetitions/services/competitionKnockouts/competition-knockouts.model';

describe('CompetitionKnockoutsComponent', () => {

  let component: CompetitionKnockoutsComponent;

  let competitionKnockoutsService;
  let windowRef;

  const eventsByRound = {} as IEventsByRoundMap;
  const element = document.createElement('div');

  beforeEach(() => {
    competitionKnockoutsService = {
      parseData: jasmine.createSpy().and.returnValue(eventsByRound)
    };
    windowRef = {
      document: {
        querySelector: jasmine.createSpy().and.returnValue(element)
      }
    };

    window.scrollTo = jasmine.createSpy();

    component = new CompetitionKnockoutsComponent(competitionKnockoutsService, windowRef);
    component.moduleConfig = {} as IBCModule;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', () => {
    component.scrollToActiveRound = jasmine.createSpy();
    component.ngOnInit();
    expect(component.eventsByRound).toBe(eventsByRound);
    expect(competitionKnockoutsService.parseData).toHaveBeenCalledWith(component.moduleConfig);
    expect(component.scrollToActiveRound).toHaveBeenCalled();
  });

  it('should return correct result', () => {
    const round = {
      name: 'name',
      active: true,
      abbreviation: '',
      number: 2
    };
    const index = 5;
    expect(component.trackByStatus(index, round)).toBe('5true');
  });

  it('should call correct methods', fakeAsync(() => {
    component.scrollToActiveRound();

    tick(100);

    expect(windowRef.document.querySelector).toHaveBeenCalledWith('.active-round');
    expect(window.scrollTo).toHaveBeenCalledWith(0, 0);
  }));

  it('should call methods when element is undefined', fakeAsync(() => {
    windowRef.document.querySelector = jasmine.createSpy().and.returnValue(undefined);

    component.scrollToActiveRound();

    tick(100);

    expect(windowRef.document.querySelector).toHaveBeenCalledWith('.active-round');
    expect(window.scrollTo).not.toHaveBeenCalledWith(0, 40);
  }));
});
