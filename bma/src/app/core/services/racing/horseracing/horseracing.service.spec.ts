import { HorseracingService } from '@core/services/racing/horseracing/horseracing.service';

describe('HorseracingService', () => {
  let service: HorseracingService;

  let timeformService;
  let ukToteService;
  let dailyRacingService;
  let eventFactory;
  let templateService;
  let timeService;
  let filtersService;
  let liveUpdatesWSService;
  let channelService;
  let lpAvailabilityService;
  let commandService;
  let localeService;
  let racingYourcallService;
  let pubSubService;
  let cmsCervice;
  let racingPostService;
  let routingHelperservice;

  beforeEach(() => {
    timeformService = {};
    ukToteService = {};
    dailyRacingService = {};
    eventFactory = {};
    templateService = {};
    timeService = {};
    filtersService = {};
    liveUpdatesWSService = {};
    channelService = {};
    lpAvailabilityService = {};
    commandService = {};
    localeService = {};
    racingYourcallService = {};
    pubSubService = {};
    cmsCervice = {};
    racingPostService = {};
    routingHelperservice = {
      encodeUrlPart: jasmine.createSpy('encodeUrlPart')
    };

    service = new HorseracingService(
      timeformService,
      ukToteService,
      dailyRacingService,
      eventFactory,
      templateService,
      timeService,
      filtersService,
      liveUpdatesWSService,
      channelService,
      lpAvailabilityService,
      commandService,
      localeService,
      racingYourcallService,
      pubSubService,
      cmsCervice,
      racingPostService,
      routingHelperservice
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });
});
