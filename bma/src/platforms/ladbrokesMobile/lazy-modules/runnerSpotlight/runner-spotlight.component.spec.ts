import { LadbrokesRunnerSpotlightComponent } from '@ladbrokesMobile/lazy-modules/runnerSpotlight/runner-spotlight.component';

describe('LadbrokesRunnerSpotlightComponent', () => {
  let component: LadbrokesRunnerSpotlightComponent;
  let locale;
  let racingPostService;

  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy()
    };
    racingPostService = {
      getLastRunText: jasmine.createSpy('getLastRunText').and.returnValue('Welcome')
    };
    component = new LadbrokesRunnerSpotlightComponent(locale, racingPostService);
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });
});
