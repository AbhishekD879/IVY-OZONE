import { RacingAntepostContentComponent } from "./racing-antepost-content.component";

describe('RacingAntepostContentComponent', () => {
  let component;
  let locale;
  let deviceService;

  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy('locale.getString').and.returnValue('France translated')
    };
    deviceService = {
        isDesktop: true
    }
    component = new RacingAntepostContentComponent(deviceService, locale);
    component.environment = {brand: 'ladbrokes'};
  });

  it('should create a comonent', () => {
    expect(component).toBeTruthy();
  });
});