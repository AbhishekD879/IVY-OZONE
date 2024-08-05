import {
  BuildYourRaceCardPageService
} from '@ladbrokesDesktop/racing/components/buildYourRaceCardPage/build-your-race-card-page.service';
import { of, throwError } from 'rxjs';

describe('BuildYourRaceCardPageService', () => {
  let service: BuildYourRaceCardPageService;
  let cacheEventsService;
  let siteServerService;
  let channelService;
  let pubSubService;
  let cmsService;
  let racingPostService;
  let eventService;

  const racingPostResponce = {
    document: [
      {
        1: { horses: { trainer: 'who1_RDH', saddle: 1 } },
        2: { horses: { trainer: 'who2_RDH', saddle: 1 } }
      }
    ]
  };
  const eventsOB = [
    {
      id: 1,
      name: '1',
      startTime: 1,
      markets: [ { outcomes: [ { runnerNumber: 1, racingFormOutcome: { trainer: 'who1_OB' } } ] } ],
      isUKorIRE: true
    },
    {
      id: 2,
      name: '2',
      startTime: 2,
      markets: [ { outcomes: [ { runnerNumber: 1, racingFormOutcome: { trainer: 'who2_OB' } } ] } ],
      isUKorIRE: true
    }
  ] as any;
  const eventsWithRDH = [
    {
      id: 1,
      name: '1',
      startTime: 1,
      markets: [ { outcomes: [ { runnerNumber: 1, racingFormOutcome: { trainer: 'who1_RDH' } } ] } ],
      isUKorIRE: true
    },
    {
      id: 2,
      name: '2',
      startTime: 2,
      markets: [ { outcomes: [ { runnerNumber: 1, racingFormOutcome: { trainer: 'who2_RDH' } } ] } ],
      isUKorIRE: true
    }
  ];

  beforeEach(() => {
    cacheEventsService = {
      store: jasmine.createSpy().and.callFake((cacheName, moduleName, events) => events)
    };
    siteServerService = {
      getEvent: jasmine.createSpy().and.returnValue(Promise.resolve(eventsOB))
    };
    channelService = {
      getLSChannelsFromArray: jasmine.createSpy()
    };
    pubSubService = {
      publish: jasmine.createSpy()
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(of({ RacingDataHub: { isEnabledForHorseRacing: true } }))
    };
    racingPostService = {
      getHorseRacingPostById: jasmine.createSpy().and.returnValue(of(racingPostResponce)),
      mergeHorseRaceData: jasmine.createSpy().and.returnValue(eventsWithRDH)
    };
    eventService = {
      isUKorIRE: jasmine.createSpy('isUKorIRE').and.returnValue(true)
    };
  });

  beforeEach(() => {
    service = new BuildYourRaceCardPageService(
       cacheEventsService,
       siteServerService,
       channelService,
       pubSubService,
       cmsService,
       racingPostService,
       eventService
    );
  });

  it('should create service instance', () => {
    expect(service).toBeTruthy();
    expect(service['moduleName']).toEqual('buildYouRaceCard');
    expect(service['requestParams']).toEqual({ priceHistory: true, externalKeysEvent: true });
  });

  describe('#getEvents', () => {
    it('should return events with data from Racing Data Hub when RDH is enabled in the CSM', done => {
      service.getEvents('1,2')
        .then(events => {
          // @ts-ignore
          expect(events).toEqual(eventsWithRDH);

          expect(service['siteServerService'].getEvent)
            .toHaveBeenCalledWith('1,2', {
              priceHistory: true,
              externalKeysEvent: true
            }, false); // racingFormOutcome: true, racingFormEvent: true

          expect(service['racingPostService'].mergeHorseRaceData).toHaveBeenCalledWith(eventsOB, racingPostResponce as any);

          expect(service['cacheEventsService'].store).toHaveBeenCalledWith('events', 'buildYouRaceCard', eventsWithRDH);
          done();
        });
    });

    it('should return events with data from OB only when RDH is NOT enabled in the CSM', done => {
      cmsService.getSystemConfig.and.returnValue(of({ RacingDataHub: { isEnabledForHorseRacing: false } }));
      racingPostService.mergeHorseRaceData.and.returnValue(eventsOB);

      service.getEvents('1,2')
        .then(events => {
          // @ts-ignore
          expect(events).toEqual(eventsOB);

          expect(service['siteServerService'].getEvent)
            .toHaveBeenCalledWith('1,2', {
              priceHistory: true,
              externalKeysEvent: true,
              racingFormOutcome: true,
              racingFormEvent: true
            }, false);

          expect(service['racingPostService'].mergeHorseRaceData).toHaveBeenCalledWith(eventsOB, undefined);

          expect(service['cacheEventsService'].store).toHaveBeenCalledWith('events', 'buildYouRaceCard', eventsOB);
          done();
        });
    });

    describe('#getEvents Errors catching - ', () => {

      it('should fail on error from CMS', done => {
        cmsService.getSystemConfig.and.returnValue(throwError('error from CMS'));

        service.getEvents('1,2')
          .catch(err => {
            expect(err).toEqual('error from CMS');
            done();
          });
      });

      it('should fail on error from OB', done => {
        siteServerService.getEvent.and.returnValue(Promise.reject('error from OB'));

        service.getEvents('1,2')
          .catch(err => {
            expect(err).toEqual('error from OB');
            done();
          });
      });

      it('should fail on error from RDH', done => {
        racingPostService.getHorseRacingPostById.and.returnValue(throwError('error from RDH'));

        service.getEvents('1,2')
          .catch(err => {
            expect(err).toEqual('error from RDH');
            done();
          });
      });
    });
  });

  describe('subscribeForUpdates', () => {
    it(`should subscribe on subscribeForUpdates`, () => {
      const channel = ['sEVENT1'];
      channelService.getLSChannelsFromArray.and.returnValue(channel);
      service.subscribeForUpdates(eventsOB);

      expect(channelService.getLSChannelsFromArray).toHaveBeenCalledWith(eventsOB);
      expect(pubSubService.publish).toHaveBeenCalledWith('SUBSCRIBE_LS', {
        channel,
        module: 'build-your-race-card'
      });
    });
  });
});
