import { DesktopHorseRaceGridComponent } from './horse-race-grid.component';

describe('DesktopHorseRaceGridComponent', () => {
  let component: DesktopHorseRaceGridComponent;
  let routingHelperService, locale, lpAvailabilityService, racingGaService,
    racingService, racingGaServicePublic: any,
    pubsub, gtmService, deviceService;

  beforeEach(() => {
    routingHelperService = {
      formEdpUrl: jasmine.createSpy()
    };
    racingService = {
      getFirstActiveEventFromGroup: jasmine.createSpy().and.returnValue({ id: 2 })
    };
    deviceService = {
      isMobile: true,
      isDesktop: false
    }

    locale = lpAvailabilityService = racingGaService = racingGaServicePublic = {};
    pubsub = {};
    gtmService = {};
    component = new DesktopHorseRaceGridComponent(
      locale,
      locale,
      lpAvailabilityService,
      racingGaService,
      routingHelperService,
      racingGaServicePublic,
      racingService,
      pubsub,
      gtmService,
      deviceService
    );
    component.switchers = [{} as any];
    component.filter = 'some';
  });

  describe('isRaceOffOrResulted', () => {
    it('should return true if race started', () => {
      expect(component.isRaceOffOrResulted({
        isStarted: true,
        isLiveNowEvent: false,
        isResulted: false
      } as any)).toEqual(true);
    });
    it('should return true if race is live', () => {
      expect(component.isRaceOffOrResulted({
        isStarted: false,
        isLiveNowEvent: true,
        isResulted: false
      } as any)).toEqual(true);
    });
    it('should return true if race is resulted', () => {
      expect(component.isRaceOffOrResulted({
        isStarted: false,
        isLiveNowEvent: false,
        isResulted: true
      } as any)).toEqual(true);
    });
    it('should return false if race is not off', () => {
      expect(component.isRaceOffOrResulted({
        isStarted: false,
        isLiveNowEvent: false,
        isResulted: false
      } as any)).toEqual(false);
    });
  });
});
