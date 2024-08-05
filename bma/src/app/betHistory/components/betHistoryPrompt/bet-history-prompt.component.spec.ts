import { BetHistoryPromptComponent } from './bet-history-prompt.component';

describe('#BetHistoryPromptComponent', () => {
  let component: BetHistoryPromptComponent,
  emaService,
  locale;

  beforeEach(() => {
    emaService = {
      emaConfig: {
        genericErrorText: 'Error'
      },
      savedAccas: {}
    };

    locale = {
      getString: jasmine.createSpy('locale.getString').and.returnValue('Success')
    };

    component = new BetHistoryPromptComponent(emaService, locale);
  });

  describe('#ngOninit', () => {
    it('Success prompt', () => {
      component.prompt = 'success';
      component.mode = 'ema';
      component.promptText = 'sometext';
      component.ngOnInit();

      expect(locale.getString).toHaveBeenCalled();
      expect(component.promptText).toBe('Success');
    });

    it('Error prompt', () => {
      component.prompt = 'error';
      component.mode = 'ema';
      component.promptText = 'sometext';
      component.ngOnInit();

      expect(component.promptText).toBe('Error');
    });
    it('Cashout mode case', () => {
      component.prompt = 'error';
      component.mode = 'cashout';
      component.promptText = 'sometext';
      component.ngOnInit();

      expect(component.promptText).toBe('sometext');
    });
  });
});

