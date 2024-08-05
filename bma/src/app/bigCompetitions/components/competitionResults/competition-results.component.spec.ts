import {
  CompetitionResultsComponent
} from '@app/bigCompetitions/components/competitionResults/competition-results.component';
import { ISportEvent } from '@core/models/sport-event.model';

describe('CompetitionResultsComponent', () => {

  let component: CompetitionResultsComponent;

  let moduleConfig;

  beforeEach(() => {
    moduleConfig = {
      id: 'id',
      type: 'type',
      name: 'name',
      maxDisplay: 10,
      viewType: 'card',
      markets: [],
      results: [
        {
          limit: 2,
          matches: [
            {
              teamA: {
                goalScorers: '',
                name: 'C',
                score: ''
              },
              teamB: {
                goalScorers: '',
                name: 'A',
                score: ''
              },
              index: 3
            },
            {
              teamA: {
                goalScorers: '',
                name: 'A',
                score: ''
              },
              teamB: {
                goalScorers: '',
                name: 'B',
                score: ''
              },
              index: 1
            }
          ],
          date: ''
        }
      ]
    };

    component = new CompetitionResultsComponent();
    component.moduleConfig = moduleConfig;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', () => {
    component.matchesAmount = 5;
    component.showMore = jasmine.createSpy();
    component.ngOnInit();
    expect(component.moduleConfig.results[0].limit).toBe(5);
    expect(component.moduleConfig.results[0].matches[0].index).toBe(7);
    expect(component.moduleConfig.results[0].matches[1].index).toBe(6);
    expect(component.moduleConfig.results[0].matches[0].teamA.name).toBe('A');
    expect(component.moduleConfig.results[0].matches[1].teamA.name).toBe('C');
    expect(component.showMore).toHaveBeenCalled();
  });

  it('should return correct result', () => {
    const event = { id: 5 } as ISportEvent;
    const index = 7;
    expect(component.trackByEvent(index, event)).toBe('75');
  });

  it('should return correct result', () => {
    const group = {
      limit: 5,
      matches: [],
      date: 'date'
    };
    const index = 3;
    expect(component.trackByGroup(index, group)).toBe('3date');
  });

  it('should set correct property values', () => {
    component.showMore();
    expect(component.limit).toBe(10);
    expect(component.showMoreAvailable).toBeFalsy();
  });

  it('should return correct result', () => {
    const group = {
      limit: 3,
      matches: [],
      date: ''
    };
    component.limit = 5;
    expect(component.isGroupVisible(group)).toBeTruthy();
  });

  it('should return correct result', () => {
    const event = { index: 4 } as ISportEvent;
    component.limit = 5;
    expect(component.isEventVisible(event)).toBeTruthy();
  });
});
