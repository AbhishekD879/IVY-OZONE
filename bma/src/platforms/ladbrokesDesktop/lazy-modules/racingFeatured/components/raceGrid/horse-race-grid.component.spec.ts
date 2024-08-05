import { DesktopHorseRaceGridComponent } from './horse-race-grid.component';

describe('LadbrokesDesktopHorseRaceGridComponent', () => {
  let component: DesktopHorseRaceGridComponent;
  let routingHelperService, locale, lpAvailabilityService, racingGaService,
    racingService, racingGaServicePublic: any,
    pubsub,
    gtmService,
    deviceService;

  beforeEach(() => {
    routingHelperService = {
      formEdpUrl: jasmine.createSpy()
    };

    racingService = {
      getFirstActiveEventFromGroup: jasmine.createSpy().and.returnValue({ id: 2 })
    };
    locale = lpAvailabilityService = racingGaService = racingGaServicePublic = {};
    pubsub = {};
    gtmService = {};
    deviceService = {
      isMobile: true,
      isDesktop: false
    }
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

  it('should split meeteing name and sub region in groupedRaces', () => {
    component.groupedRaces = [{
      groupName: 'Worcester (USA)',
      cashoutAvailable: false,
      liveStreamAvailable: true,
      events: []
    }, {
      groupName: 'Busan',
      cashoutAvailable: false,
      liveStreamAvailable: true,
      events: []
    }, {
      groupName: 'Belmont Park (FR)(UA)',
      cashoutAvailable: false,
      liveStreamAvailable: true,
      events: []
    }] as any;

    const resultMock = [{
      groupName: 'Worcester',
      subRegion: '(USA)',
      cashoutAvailable: false,
      liveStreamAvailable: true,
      events: []
    }, {
      groupName: 'Busan',
      cashoutAvailable: false,
      liveStreamAvailable: true,
      events: []
    }, {
      groupName: 'Belmont Park',
      subRegion: '(FR)(UA)',
      cashoutAvailable: false,
      liveStreamAvailable: true,
      events: []
    }] as any;

    component.generateEventList();
    expect(component.groupedRaces).toEqual(resultMock);
  });
});
