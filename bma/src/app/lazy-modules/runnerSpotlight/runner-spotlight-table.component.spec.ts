import { RunnerSpotlightTableComponent } from './runner-spotlight-table.component';
import { IRacingPostForm } from '@core/models/outcome.model';

describe('RunnerSpotlightTableComponent', () => {
  let component: RunnerSpotlightTableComponent;
  let outcome;
  let localeService;

  beforeEach(() => {
    localeService = {
      getString: jasmine.createSpy('getString')
    };
    outcome = {
      racingFormOutcome: {
        age: '8',
        overview: 'Took his chase record to 6-6 when winning last year\'s Ascot Chase (2m5f, soft),' +
          'looking set for further success at the ' +
          'top level; current campaign hasn\'t quite gone to plan, as he unseated mid-race in the King George (hampered by faller) then ' +
          'got trounced by Cyrname when bidding for another Ascot Chase win; however, he\'s not done with yet and is well worth another ' +
          'chance to get back in the winning groove; cheekpieces fitted.',
        weight: 'Pounds,161,'
      }
    };

    component = new RunnerSpotlightTableComponent(localeService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should handle empty racing outcome overview', () => {
    outcome.racingFormOutcome.overview = '';

    component.outcome = outcome;
    component.ngOnInit();

    expect(component.formOutcomeOverview).toEqual('');
  });

  it('trackByValue', () => {
    const data = {
      date: '2019-01-17T17:55:00'
    } as IRacingPostForm;
    const result = component.trackByValue(0, data);
    expect(result).toEqual(data.date);
  });
});
