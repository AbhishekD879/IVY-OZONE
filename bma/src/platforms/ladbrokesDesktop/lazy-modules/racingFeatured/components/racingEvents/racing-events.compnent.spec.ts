import { RacingEventsComponent } from './racing-events.component';

describe('RacingEventsComponent', () => {
  let component;
  let locale;
  let storage;
  let racingService, windowRef, gtm, deviceService, vEPService;

  beforeEach(() => {
    locale = {};
    storage = {};
    racingService = {
      filterRacingGroup: jasmine.createSpy('filterRacingGroup')
    };
    windowRef = {
      nativeWindow: {
        scrollTo: jasmine.createSpy('scrollTo')      
      }
    };
    gtm = {
      push: jasmine.createSpy('push')
    };
    deviceService = { isDesktop: true };
    vEPService = {}
    component = new RacingEventsComponent(locale, storage, racingService, windowRef, gtm, deviceService, vEPService);
  });

  it('emitFetchCardId', () => {
    component.fetchCardId.emit = jasmine.createSpy('emitFetchCardId.emit');
    component.emitFetchCardId({id: '1'});
    expect(component.fetchCardId.emit).toHaveBeenCalledWith({id: '1'});
  });
});
