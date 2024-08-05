import { RunnerSpotlightComponent } from '@lazy-modules/runnerSpotlight/runner-spotlight.component';

describe('RunnerSpotlightComponent', () => {
  let component;
  let localeService;
  let outcome;
  let racingPostService;

  beforeEach(() => {
    localeService = {
      getString: jasmine.createSpy('getString').and.returnValue('January')
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
    racingPostService = {
      getLastRunText: jasmine.createSpy('getLastRunText').and.returnValue('Welcome')
    };

    component = new RunnerSpotlightComponent(localeService, racingPostService);
  });

  describe('ngOnInit', () => {
    it('should handle empty racing outcome overview', () => {
      outcome.racingFormOutcome.overview = '';

      component.outcome = outcome;
      component.ngOnInit();

      expect(component.spotlightOverview).toEqual('');
    });

    it('should set full spotlight overview if device is desktop', () => {

      component.outcome = outcome;
      component.ngOnInit();

      expect(component.noDetails).toBeFalsy();
      expect(component.spotlightOverview).toEqual(outcome.racingFormOutcome.overview);
    });

    it('should set property as no details', () => {
      outcome.racingFormOutcome.age = null;
      outcome.racingFormOutcome.weight = null;

      component.outcome = outcome;
      component.ngOnInit();

      expect(component.noDetails).toBeTruthy();
    });

  });

  describe('#isOverview', () => {
    it('Should return true if spotlightOverview exists', () => {
      component.spotlightOverview = {
      } as any;
      const reponse = component.isOverview();
      expect(reponse).toBe(true);
    });
    it('Should return false if spotlightOverview does not exists', () => {
      component.spotlightOverview = undefined;
      const reponse = component.isOverview();
      expect(reponse).toBe(false);
    });
  });

  describe('#getCorrectWeight', () => {
    it('Should return 0st if spotlightOverview weight does not exist', () => {
      component.outcome = {
        racingFormOutcome: {
          weight: 'Pounds,0,'
        }
      } as any;
      const response = component['getCorrectWeight']();
      expect(response).toBe('0st');
    });
    it('Should return value if spotlightOverview weight  exist', () => {
      component.outcome = {
        racingFormOutcome: {
          weight: 'Pounds,161,'
        }
      } as any;
      const response = component['getCorrectWeight']();
      expect(response).toBe('11st-7lb');
    });
  });
});
