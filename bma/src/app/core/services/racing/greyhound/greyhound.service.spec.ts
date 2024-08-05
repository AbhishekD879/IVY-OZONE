import { GreyhoundService } from '@core/services/racing/greyhound/greyhound.service';

describe('GreyhoundService', () => {
  let service: GreyhoundService;

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
  let cmsService;
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
    cmsService = {};
    racingPostService = {};
    routingHelperservice = {
      encodeUrlPart: jasmine.createSpy('encodeUrlPart')
    };

    service = new GreyhoundService(
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
      cmsService,
      routingHelperservice,
      racingPostService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });
});
