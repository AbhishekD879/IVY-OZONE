import { DesktopRunnerSpotlightComponent } from '@ladbrokesDesktop/lazy-modules/runnerSpotlight/runner-spotlight.component';

describe('LadbrokesRunnerSpotlightComponent', () => {
  let component: DesktopRunnerSpotlightComponent;
  let locale;
  let racingPostService;

  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy()
    };
    racingPostService = {
      getLastRunText: jasmine.createSpy('getLastRunText').and.returnValue('Welcome')
    };

    component = new DesktopRunnerSpotlightComponent(locale, racingPostService);
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

});
