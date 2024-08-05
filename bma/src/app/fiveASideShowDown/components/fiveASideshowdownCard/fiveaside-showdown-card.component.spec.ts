import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { eventDetails, EVENTS_DETAILS_COMMENTS, sCLOCKUpdate, sEVENTupdate } from '@app/fiveASideShowDown/services/show-down-cards.mock';
import {
    FiveASideShowdownCardComponent
} from '@app/fiveASideShowDown/components/fiveASideshowdownCard/fiveaside-showdown-card.component';
import { of } from 'rxjs';
import { fakeAsync } from '@angular/core/testing';
import { SHOWDOWN_CARDS, PUBSUB_API } from '@app/fiveASideShowDown/constants/constants';
import { LocaleService } from '@app/core/services/locale/locale.service';
import * as fs from '@app/lazy-modules/locale/translations/en-US/fiveaside.lang';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';

describe('FiveASideShowdownCardComponent', () => {
    let component: FiveASideShowdownCardComponent;
    let pubSubService, fiveASideShowDownLobbyService, fiveAsideLiveServeUpdatesService, coreToolsService,
        localeService, domToolsService, showDownService = null;
    let router = null;
    let gtmService = null, windowRef = null, liveEventClockProviderService, timeSyncService, changeDetectorRef;
    beforeEach(() => {
        coreToolsService = new CoreToolsService();
        localeService = new LocaleService(coreToolsService);
        localeService.setLangData(fs);
        fiveASideShowDownLobbyService = {
            setEventStateByStartDate: jasmine.createSpy(),
            isValidValue: jasmine.createSpy(),
            signPostingsPriority: jasmine.createSpy().and.returnValue({ size: true }),
            setContestSignPosting: jasmine.createSpy().and.returnValue({ totalPrizes: '1 Total Prizes' }),
            getTeamNameFromEventComments: jasmine.createSpy().and.returnValue({ homeTeam: 'India', awayTeam: 'England' }),
            addScoresAndClock: jasmine.createSpy().and.returnValue(of(
                EVENTS_DETAILS_COMMENTS
            )),
        };
        showDownService = {
            hasImageForHomeAway: jasmine.createSpy().and.returnValue(false),
            setDefaultTeamColors: jasmine.createSpy().and.returnValue([{ primaryColour: '#23423' }, { primaryColour: '#23424' }])
        };
        router = {
            navigate: jasmine.createSpy()
        };
        gtmService = {
            push: jasmine.createSpy('push')
        };
        pubSubService = {
            subscribe: jasmine.createSpy(),
            unsubscribe: jasmine.createSpy(),
            publish: jasmine.createSpy(),
            API: pubSubApi
        };
        fiveAsideLiveServeUpdatesService = {
            updateEventComments: jasmine.createSpy(),
            eventClockUpdate: jasmine.createSpy(),
            updateEventLiveData: jasmine.createSpy(),
            createEventScoreComments: jasmine.createSpy()
        };
        windowRef = {
            nativeWindow: {
                setTimeout: jasmine.createSpy().and.callFake(cb => cb()),
                clearTimeout: jasmine.createSpy('clearTimeout')
            }
        };
        domToolsService = {
            scrollPageTop: jasmine.createSpy('scrollPageTop')
        };
        changeDetectorRef = {
            detectChanges: jasmine.createSpy(),
            detach: jasmine.createSpy()
        };
        liveEventClockProviderService = {
            create: jasmine.createSpy().and.returnValue({})
        };
        timeSyncService = {
            getTimeDelta: jasmine.createSpy()
        };
        component = new FiveASideShowdownCardComponent(pubSubService,
            fiveASideShowDownLobbyService,
            fiveAsideLiveServeUpdatesService,
            coreToolsService, router, gtmService, windowRef, domToolsService, showDownService,
            timeSyncService, liveEventClockProviderService, changeDetectorRef);
    });

    it('should create component', () => {
        expect(component).toBeTruthy();
    });

    it('#ngOnInit should call methods during ngOnInit', () => {
        component['initShowdownCardDetails'] = jasmine.createSpy('initShowdownCardDetails');
        component['registerLiveServeUpdateSubscriptions'] = jasmine.createSpy('registerLiveServeUpdateSubscriptions');
        component.event = {} as any;
        component.contestData = {} as any;
        component.event.clockData = {} as any;
        component.ngOnInit();
        expect(component['initShowdownCardDetails']).toHaveBeenCalled();
        expect(component['registerLiveServeUpdateSubscriptions']).toHaveBeenCalled();
        expect(domToolsService.scrollPageTop).toHaveBeenCalled();
    });

    it('#ngOnInit should not call initShowdownCardDetails when event and contestData is null', () => {
        component['initShowdownCardDetails'] = jasmine.createSpy('initShowdownCardDetails');
        component['registerLiveServeUpdateSubscriptions'] = jasmine.createSpy('registerLiveServeUpdateSubscriptions');
        component.event = null;
        component.contestData = null;
        component.ngOnInit();
        expect(component['initShowdownCardDetails']).not.toHaveBeenCalled();
        expect(component['registerLiveServeUpdateSubscriptions']).not.toHaveBeenCalled();
        expect(domToolsService.scrollPageTop).toHaveBeenCalled();
    });

    it('#ngOnInit should call methods during ngOnInit when clock data null', () => {
        component['initShowdownCardDetails'] = jasmine.createSpy('initShowdownCardDetails');
        component['registerLiveServeUpdateSubscriptions'] = jasmine.createSpy('registerLiveServeUpdateSubscriptions');
        component.event = {} as any;
        component.contestData = {} as any;
        component.event.clockData = null as any;
        component.ngOnInit();
        expect(component['initShowdownCardDetails']).toHaveBeenCalled();
        expect(component['registerLiveServeUpdateSubscriptions']).toHaveBeenCalled();
        expect(domToolsService.scrollPageTop).toHaveBeenCalled();
    });

    it('#ngOnDestroy unsubscribes the required subsciptions', () => {
        component['componentId'] = '1';
        component.ngOnDestroy();
        expect(pubSubService.unsubscribe).toHaveBeenCalledWith(component['componentId']);
    });

    describe('#initAssetManagementFlags', () => {
        it('#should call required services', () => {
            component.teamColors = [];
            component['contestData'] = { assets: [{ primaryColour: '#23423' }, { secondaryColor: '#23423' }],assetManagement: [{ primaryColour: '#23423' }] } as any;
            component['initAssetManagementFlags']();
            expect(component.teamColors.length).toEqual(2);
        });

        it('#should not call required services', () => {
            component.teamColors = [];
            component['contestData'] = {} as any;
            component['initAssetManagementFlags']();
            expect(component.teamColors.length).toEqual(0);
        });
    });

    it('#initShowdownCardDetails should call all required methods', () => {
        component['contestData'] = { id: '1' } as any;
        component['setEventLiveStatus'] = jasmine.createSpy('setEventLiveStatus');
        spyOn(component, 'initScoresFromEventComments');
        spyOn(component as any, 'initAssetManagementFlags');
        spyOn(component as any, 'handleETClockUpdate');
        spyOn(coreToolsService, 'uuid').and.returnValue('550e8400');
        component['initShowdownCardDetails']();
        expect(component['setEventLiveStatus']).toHaveBeenCalled();
        expect(fiveASideShowDownLobbyService.setEventStateByStartDate).toHaveBeenCalled();
        expect(coreToolsService.uuid).toHaveBeenCalled();
        expect(component['componentId']).toEqual('550e8400');
        expect(component['initScoresFromEventComments']).toHaveBeenCalled();
        expect(component['initAssetManagementFlags']).toHaveBeenCalled();
        expect(component['signPostingsInfo'] as any).toEqual({ size: true });
        expect(component['contestDetails'] as any).toEqual({ totalPrizes: '1 Total Prizes' });
    });

    describe('#initScoresFromEventComments', () => {
        it('should call all required methods', () => {
            component.event = { ...eventDetails} as any;
            component.event['isResulted'] = true;
            component.event.scores = { 
                    home: { score: '1' }, away: { score: '2' }
            } as any;
            component['isMatchCompletedAndResulted'] = jasmine.createSpy().and.returnValue(true);
            component['isTeamScoresAvailable'] = jasmine.createSpy().and.returnValue(true);
            component['initScoresFromEventComments']();
            expect(fiveASideShowDownLobbyService.getTeamNameFromEventComments).toHaveBeenCalledWith(component['event']);
            expect(component.homeTeam).toEqual('India');
            expect(component.awayTeam).toEqual('England');
            expect(component['isMatchCompletedAndResulted']).toHaveBeenCalled();
            expect(component.isMatchCompleted).toBeTruthy();
            expect(component['isTeamScoresAvailable']).toHaveBeenCalled();
            expect(component.isScoresAvailable).toBeTruthy();
        });

        it('should call all required methods when event is empty', () => {
            component.event = undefined;
            component['isMatchCompletedAndResulted'] = jasmine.createSpy().and.returnValue(true);
            component['isTeamScoresAvailable'] = jasmine.createSpy().and.returnValue(true);
            component['initScoresFromEventComments']();
            expect(fiveASideShowDownLobbyService.getTeamNameFromEventComments).toHaveBeenCalledWith(component['event']);
            expect(component.homeTeam).toEqual('India');
            expect(component.awayTeam).toEqual('England');
            expect(component['isMatchCompletedAndResulted']).toHaveBeenCalled();
            expect(component.isMatchCompleted).toBeTruthy();
            expect(component['isTeamScoresAvailable']).toHaveBeenCalled();
            expect(component.isScoresAvailable).toBeTruthy();
        });

        it('should call all required methods when comments are empty', () => {
            component.event = { ...eventDetails } as any;
            component.event['isResulted'] = true;
            component.event['comments'] = {
                teams: {}
            } as any;
            component['isMatchCompletedAndResulted'] = jasmine.createSpy().and.returnValue(true);
            component['isTeamScoresAvailable'] = jasmine.createSpy().and.returnValue(true);
            component['initScoresFromEventComments']();
            expect(fiveASideShowDownLobbyService.getTeamNameFromEventComments).toHaveBeenCalledWith(component['event']);
            expect(component.homeTeam).toEqual('India');
            expect(component.awayTeam).toEqual('England');
            expect(component['isMatchCompletedAndResulted']).toHaveBeenCalled();
            expect(component.isMatchCompleted).toBeTruthy();
            expect(component['isTeamScoresAvailable']).toHaveBeenCalled();
            expect(component.isScoresAvailable).toBeTruthy();
        });
        it('should call all required methods when home and away are empty', () => {
            component.event = { ...eventDetails } as any;
            component.event['isResulted'] = true;
            component.event['comments'] = {
                home: {}, away: {}
            } as any;
            component['isMatchCompletedAndResulted'] = jasmine.createSpy().and.returnValue(true);
            component['isTeamScoresAvailable'] = jasmine.createSpy().and.returnValue(true);
            component['initScoresFromEventComments']();
            expect(fiveASideShowDownLobbyService.getTeamNameFromEventComments).toHaveBeenCalledWith(component['event']);
            expect(component.homeTeam).toEqual('India');
            expect(component.awayTeam).toEqual('England');
            expect(component['isMatchCompletedAndResulted']).toHaveBeenCalled();
            expect(component.isMatchCompleted).toBeTruthy();
            expect(component['isTeamScoresAvailable']).toHaveBeenCalled();
            expect(component.isScoresAvailable).toBeTruthy();
        });
    });

    describe('#registerLiveServeUpdateSubscriptions SHOWDOWN_LIVE_SCORE_UPDATE subscription', () => {
        let update;
        beforeEach(() => {
            update = {
                id: 232341790,
                payload: {
                    scores: {}
                }
            } as any;
            component.event = { ...eventDetails } as any;
            component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
                if (ch === PUBSUB_API.SHOWDOWN_LIVE_SCORE_UPDATE) {
                    fn(update);
                }
            });
        });

        it('should update scores when all conditions are met', () => {
            update = {
                id: 232341790,
                payload: {
                  scores: { home: { score: 1 }, away: { score: 2 } }
                }
              } as any;
              spyOn(component as any, 'initScoresFromEventComments');
              component['registerLiveServeUpdateSubscriptions']();
              expect(component.initScoresFromEventComments).not.toHaveBeenCalled();
        });

        it('should not update scores if not the same event', () => {
            spyOn(component, 'initScoresFromEventComments');
            update.id = 1000;
            component['registerLiveServeUpdateSubscriptions']();
            expect(fiveAsideLiveServeUpdatesService.updateEventComments).not.toHaveBeenCalled();
            expect(component['initScoresFromEventComments']).not.toHaveBeenCalled();
        });

        it('should not update scores if payload is null', () => {
            update.payload = null;
            component['registerLiveServeUpdateSubscriptions']();
            expect(fiveAsideLiveServeUpdatesService.updateEventComments).not.toHaveBeenCalled();
        });

        it('should not update scores if update is null', () => {
            update = null;
            component['registerLiveServeUpdateSubscriptions']();
            expect(fiveAsideLiveServeUpdatesService.updateEventComments).not.toHaveBeenCalled();
        });

        it('should not update scores if event id is null', () => {
            component.event.id = null;
            component['registerLiveServeUpdateSubscriptions']();
            expect(fiveAsideLiveServeUpdatesService.updateEventComments).not.toHaveBeenCalled();
        });
    });

    describe('#gotoLeaderboard', () => {
        it('#gotoLeaderboard should call pre leaderboard', () => {
            component['event'] = { started: false } as any;
            spyOn(component as any, 'showdownCardGATrack');
            component['gotoLeaderboard' as any]('123');
            expect(component['showdownCardGATrack']).toHaveBeenCalled();
            expect(router.navigate).toHaveBeenCalledWith([SHOWDOWN_CARDS.LEADERBOARD_BASE_URL, '123']);
        });
    });

    it('#showdownCardGATrack should call gtm service', () => {
        component.contestData = { name: 'xan' } as any;
        component.event = { id: 123 } as any;
        component['showdownCardGATrack' as any]();
        expect(gtmService.push).toHaveBeenCalled();
    });

    describe('#registerLiveServeUpdateSubscriptions SHOWDOWN_LIVE_CLOCK_UPDATE subscription', () => {
        let update;
        beforeEach(() => {
            spyOn(component as any, 'createClockForEvent');
            spyOn(component as any, 'handleETClockUpdate');
            update = { ...sCLOCKUpdate } as any;
            component.event = { ...eventDetails } as any;
            component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
                if (ch === PUBSUB_API.SHOWDOWN_LIVE_CLOCK_UPDATE) {
                    fn(update);
                }
            });
        });

        it('should update clock when all conditions are met', () => {
            component['registerLiveServeUpdateSubscriptions']();
            expect(fiveAsideLiveServeUpdatesService.eventClockUpdate).toHaveBeenCalledWith(update.payload, component.event);
        });

        it('should not update clock if not the same event', () => {
            update.id = 1000;
            component['registerLiveServeUpdateSubscriptions']();
            expect(fiveAsideLiveServeUpdatesService.eventClockUpdate).not.toHaveBeenCalled();
        });

        it('should not update clock if payload is null', () => {
            update.payload = null;
            component['registerLiveServeUpdateSubscriptions']();
            expect(fiveAsideLiveServeUpdatesService.eventClockUpdate).not.toHaveBeenCalled();
        });

        it('should not update clock if update is null', () => {
            update = null;
            component['registerLiveServeUpdateSubscriptions']();
            expect(fiveAsideLiveServeUpdatesService.eventClockUpdate).not.toHaveBeenCalled();
        });

        it('should not update clock if event id is null', () => {
            component.event.id = null;
            component['registerLiveServeUpdateSubscriptions']();
            expect(fiveAsideLiveServeUpdatesService.eventClockUpdate).not.toHaveBeenCalled();
        });
    });

    describe('#registerLiveServeUpdateSubscriptions SHOWDOWN_LIVE_EVENT_UPDATE subscription', () => {
        let update;
        beforeEach(() => {
            spyOn(component as any, 'setEventLiveStatusFromUpdate');
            update = { ...sEVENTupdate };
            component.event = { ...eventDetails } as any;
            component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
                if (ch === PUBSUB_API.SHOWDOWN_LIVE_EVENT_UPDATE) {
                    fn(update);
                }
            });
        });

        it('should update event when all conditions are met', () => {
            component['registerLiveServeUpdateSubscriptions']();
            expect(fiveAsideLiveServeUpdatesService.updateEventLiveData).toHaveBeenCalledWith(component.event, update);
        });

        it('should not update event if not the same event', () => {
            update.id = 1000;
            component['registerLiveServeUpdateSubscriptions']();
            expect(fiveAsideLiveServeUpdatesService.updateEventLiveData).not.toHaveBeenCalled();
        });

        it('should not update event if payload is null', () => {
            update.payload = null;
            component['registerLiveServeUpdateSubscriptions']();
            expect(fiveAsideLiveServeUpdatesService.updateEventLiveData).not.toHaveBeenCalled();
        });

        it('should not update event if update is null', () => {
            update = null;
            component['registerLiveServeUpdateSubscriptions']();
            expect(fiveAsideLiveServeUpdatesService.updateEventLiveData).not.toHaveBeenCalled();
        });

        it('should not update event if event id is null', () => {
            component.event.id = null;
            component['registerLiveServeUpdateSubscriptions']();
            expect(fiveAsideLiveServeUpdatesService.updateEventLiveData).not.toHaveBeenCalled();
        });
    });

    describe('#registerLiveServeUpdateSubscriptions SHOWDOWN_EVENT_STARTED subscription', () => {
        let eventId;
        beforeEach(() => {
            eventId = 232341790;
            component.event = { ...eventDetails } as any;
            component['initEventStarted'] = jasmine.createSpy();
            component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
                if (ch === 'SHOWDOWN_EVENT_STARTED') {
                    fn(eventId);
                }
            });
        });

        it('should update event when all conditions are met', () => {
            component['registerLiveServeUpdateSubscriptions']();
            expect(component['initEventStarted']).toHaveBeenCalledWith(component.event as any, eventId);
        });

        it('should update event when all conditions are met and check default scores', () => {
            component.homeScore = undefined; component.awayScore = undefined;
            component['registerLiveServeUpdateSubscriptions']();
            expect(component['initEventStarted']).toHaveBeenCalledWith(component.event as any, eventId);
            expect(component.homeScore).toEqual('0');
            expect(component.awayScore).toEqual('0');
        });

        it('should update event when all conditions are met and check default scores initialized', () => {
            component.homeScore = '3'; component.awayScore = '3';
            component['isTeamScoresAvailable'] = jasmine.createSpy().and.returnValue(true);
            component['registerLiveServeUpdateSubscriptions']();
            expect(component['initEventStarted']).toHaveBeenCalledWith(component.event as any, eventId);
            expect(component.homeScore).toEqual('3');
            expect(component.awayScore).toEqual('3');
        });

        it('should not update event if not the same event', () => {
            eventId = 1000;
            component['registerLiveServeUpdateSubscriptions']();
            expect(component['initEventStarted']).not.toHaveBeenCalled();
        });

        it('should not update event if eventId is null', () => {
            eventId = null;
            component['registerLiveServeUpdateSubscriptions']();
            expect(component['initEventStarted']).not.toHaveBeenCalled();
        });

        it('should not update event if event id is null', () => {
            component.event.id = null;
            component['registerLiveServeUpdateSubscriptions']();
            expect(component['initEventStarted']).not.toHaveBeenCalled();
        });

        it('should not update event if update event id and event id null', () => {
            eventId = null;
            component.event.id = null;
            component['registerLiveServeUpdateSubscriptions']();
            expect(component['initEventStarted']).not.toHaveBeenCalled();
        });

        it('should not update event if update event id is null and event id is present', () => {
            eventId = null;
            component.event.id = 232341790;
            component['registerLiveServeUpdateSubscriptions']();
            expect(component['initEventStarted']).not.toHaveBeenCalled();
        });

        it('should not update event if update event id is present and event id is null', () => {
            eventId = 232341790;
            component.event.id = null;
            component['registerLiveServeUpdateSubscriptions']();
            expect(component['initEventStarted']).not.toHaveBeenCalled();
        });
    });

    describe('#createClockForEvent', () => {
        it('should add the clock to event', () => {
            component.event = { clock: undefined, started: true } as any;
            const update = { id: 123, seconds: '1' } as any;
            component['createClockForEvent'](update);
            expect(component.event.clock).not.toBeUndefined();
        });
        it('should not add the clock to the event', () => {
            component.event = { clock: undefined, started: false } as any;
            const update = { id: 123, seconds: '1' } as any;
            component['createClockForEvent'](update);
            expect(component.event.clock).toBeUndefined();
        });
        it('should not call liveEventClockProviderService', () => {
            component.event = { clock: {}, started: true } as any;
            const update = { id: 123, seconds: '1' } as any;
            component['createClockForEvent'](update);
            expect(liveEventClockProviderService.create).not.toHaveBeenCalled();
        });
    });

    describe('#initEventStarted', () => {
        let event;
        let updateEventId;
        beforeEach(() => {
            event = { ...eventDetails } as any;
            updateEventId = 232341790;
            component['updateEventCommentaryAvailability'] = jasmine.createSpy();
            component['setEventLiveStatus'] = jasmine.createSpy('setEventLiveStatus');
            spyOn(component, 'initScoresFromEventComments');
        });
        it('#initEventStarted should add the clock and score to the event', fakeAsync(() => {
            event.started = false;
            component['initEventStarted'](event, updateEventId);
            expect(event.started).toEqual(true);
        }));

        it('#initEventStarted should not call / add the clock and score to the event', () => {
            event.started = false;
            component['initEventStarted'](event, updateEventId);
            expect(fiveASideShowDownLobbyService['addScoresAndClock']).not.toHaveBeenCalled();
        });

        it('#initEventStarted should exit out of function if started is true', () => {
            event.started = true;
            component['initEventStarted'](event, updateEventId);
            expect(event.started).toEqual(true);
        });

        it('#initEventStarted should not call / add the clock and score to the event when updateEvent not found', () => {
            event.started = false;
            component['initEventStarted'](event, 123);
            expect(component['updateEventCommentaryAvailability']).not.toHaveBeenCalled();
            expect(fiveASideShowDownLobbyService['setEventStateByStartDate']).not.toHaveBeenCalled();
            expect(component['initScoresFromEventComments']).not.toHaveBeenCalled();
            // expect(component['setEventLiveStatus']).not.toHaveBeenCalled();
        });
    });

    describe('#updateEventCommentaryAvailability', () => {
        it('should update isNoCommentaryAvailable as true', () => {
            component.isNoCommentaryAvailable = false;
            const event = { started: true, clock: null, comments: null } as any;
            component['updateEventCommentaryAvailability'](event);
            expect(component.isNoCommentaryAvailable).toBeTruthy();
        });

        it('should update isNoCommentaryAvailable as false', () => {
            component.isNoCommentaryAvailable = false;
            const event = null;
            component['updateEventCommentaryAvailability'](event);
            expect(component.isNoCommentaryAvailable).toBeFalsy();
        });

        it('should update isNoCommentaryAvailable as false', () => {
            component.isNoCommentaryAvailable = false;
            const event = { started: false, clock: null, comments: null } as any;
            component['updateEventCommentaryAvailability'](event);
            expect(component.isNoCommentaryAvailable).toBeFalsy();
        });
        it('should update isNoCommentaryAvailable as false', () => {
            component.isNoCommentaryAvailable = false;
            const event = { started: true, clock: {}, comments: null } as any;
            component['updateEventCommentaryAvailability'](event);
            expect(component.isNoCommentaryAvailable).toBeFalsy();
        });
        it('should update isNoCommentaryAvailable as false', () => {
            component.isNoCommentaryAvailable = false;
            const event = { started: true, clock: {}, comments: {} } as any;
            component['updateEventCommentaryAvailability'](event);
            expect(component.isNoCommentaryAvailable).toBeFalsy();
        });
    });

    it('#isMatchPeriodStatus should return true', () => {
        component.event = { clock: { matchTime: 'HT' } } as any;
        component.event.clock = { matchTime: 'HT' };
        expect(component.isMatchPeriodStatus).toEqual(true);
    });

    it('#isMatchPeriodStatus should return false', () => {
        component.event = { clock: { matchTime: '07:00' } } as any;
        expect(component.isMatchPeriodStatus).toEqual(false);
    });

    it('#isMatchPeriodStatus should return undefined when event is null', () => {
        component.event = null as any;
        expect(component.isMatchPeriodStatus).toEqual(undefined);
    });

    it('#isMatchPeriodStatus should return undefined when event clock is null', () => {
        component.event = { clock: null } as any;
        expect(component.isMatchPeriodStatus).toEqual(null);
    });

    it('#isMatchFullTime should return true', () => {
        component.event = { isResulted: false, clock: { matchTime: 'FT' } } as any;
        expect(component.isMatchFullTime).toEqual(true);
    });

    it('#isMatchFullTime should return false when isResulted is false', () => {
        component.event = { isResulted: false, clock: { matchTime: 'PENS' } } as any;
        expect(component.isMatchFullTime).toEqual(false);
    });

    it('#isMatchFullTime should return false', () => {
        component.event = null;
        expect(component.isMatchFullTime).toEqual(undefined);
    });

    it('#isMatchFullTime should return false when clock is null', () => {
        component.event = { clock: null } as any;
        expect(component.isMatchFullTime).toEqual(undefined);
    });

    it('#isMatchFullTime when regularTimeFinished is true', () => {
        component.event = { clock: null, regularTimeFinished: true } as any;
        expect(component.isMatchFullTime).toEqual(true);
    });

    it('#isMatchFullTime when regularTimeFinished is missing', () => {
        component.event = { clock: null } as any;
        expect(component.isMatchFullTime).toBeUndefined();
    });

    describe('#isMatchCompletedAndResulted', () => {
        it('#isMatchCompletedAndResulted should return true', () => {
            component.event = { regularTimeFinished: true } as any;
            expect(component['isMatchCompletedAndResulted']()).toBeTruthy();
        });

        it('#isMatchCompletedAndResulted should return false', () => {
            component.event = { regularTimeFinished: false } as any;
            expect(component['isMatchCompletedAndResulted']()).toBeFalsy();
        });

        it('#isMatchCompletedAndResulted should return null', () => {
            component.event = null;
            expect(component['isMatchCompletedAndResulted']()).toBeNull();
        });

        it('#isMatchCompletedAndResulted should return undefined', () => {
            component.event = {} as any;
            expect(component['isMatchCompletedAndResulted']()).toBeUndefined();
        });
    });

    describe('#setEventLiveStatus', () => {
        it('set eventIsLive false when started is true and isResulted is true', () => {
            component.event = { started: true, regularTimeFinished: true } as any;
            component['setEventLiveStatus']();
            expect(component['eventIsLive']).toBeFalsy();
        });

        it('set eventIsLive false when started is false and isResulted is true', () => {
            component.event = { started: false, regularTimeFinished: true } as any;
            component['setEventLiveStatus']();
            expect(component['eventIsLive']).toBeFalsy();
        });

        it('set eventIsLive false when started is true and isResulted is false', () => {
            component.event = { started: true, regularTimeFinished: false } as any;
            component['setEventLiveStatus']();
            expect(component['eventIsLive']).toBeTruthy();
        });

        it('set eventIsLive false when started is false and isResulted is false', () => {
            component.event = { started: false, regularTimeFinished: false } as any;
            component['setEventLiveStatus']();
            expect(component['eventIsLive']).toBeFalsy();
        });

        it('set eventIsLive false when event is null', () => {
            component.event = null as any;
            component['setEventLiveStatus']();
            expect(component['eventIsLive']).toBeFalsy();
        });

        it('set eventIsLive false when event is not null and started is present', () => {
            component.event = { started: true } as any;
            component['setEventLiveStatus']();
            expect(component['eventIsLive']).toBeTruthy();
        });

        it('set eventIsLive false when event is not null and started is present', () => {
            component.event = { started: false } as any;
            component['setEventLiveStatus']();
            expect(component['eventIsLive']).toBeFalsy();
        });

        it('set eventIsLive false when event is not null and isResulted is present', () => {
            component.event = { regularTimeFinished: false } as any;
            component['setEventLiveStatus']();
            expect(component['eventIsLive']).toBeUndefined();
        });

        it('set eventIsLive false when event is not null and isResulted is present', () => {
            component.event = { regularTimeFinished: true } as any;
            component['setEventLiveStatus']();
            expect(component['eventIsLive']).toBeUndefined();
        });

        it('set eventIsLive false when event is not null and the values are not present', () => {
            component.event = {} as any;
            component['setEventLiveStatus']();
            expect(component['eventIsLive']).toBeUndefined();
        });

        it('set eventIsLive false when event isResulted is true and publish SHOWDOWN_LIVE_EVENT_RESULTED', () => {
            component.event = { id: 1, regularTimeFinished: true } as any;
            component['setEventLiveStatus']();
            expect(component['eventIsLive']).toBeUndefined();
            expect(pubSubService.publish).toHaveBeenCalledWith(PUBSUB_API.SHOWDOWN_LIVE_EVENT_RESULTED, component.event.id);
        });

        it('set eventIsLive false when event isResulted is false and not publish SHOWDOWN_LIVE_EVENT_RESULTED', () => {
            component.event = { id: 1, regularTimeFinished: false } as any;
            component['setEventLiveStatus']();
            expect(component['eventIsLive']).toBeUndefined();
            expect(pubSubService.publish).not.toHaveBeenCalledWith(PUBSUB_API.SHOWDOWN_LIVE_EVENT_RESULTED, component.event.eventId);
        });

        it('set eventIsLive false when event is null and not publish SHOWDOWN_LIVE_EVENT_RESULTED', () => {
            component.event = null;
            component['setEventLiveStatus']();
            expect(pubSubService.publish).not.toHaveBeenCalledWith(PUBSUB_API.SHOWDOWN_LIVE_EVENT_RESULTED, '');
        });
    });

    describe('#setEventLiveStatusFromUpdate', () => {
        it('set eventIsLive as true and when conditions are met', () => {
            const update = { payload: { started: true, regular_time_finished: false } };
            component['setEventLiveStatusFromUpdate'](update as any);
            expect(component['eventIsLive']).toBeTruthy();
        });
        it('set eventIsLive as false and when result_conf is Y', () => {
            const update = { payload: { started: true, regular_time_finished: true} };
            component['setEventLiveStatusFromUpdate'](update as any);
            expect(component['eventIsLive']).toBeFalsy();
        });
        it('set eventIsLive as false and when started is N', () => {
            const update = { payload: { started: false, regular_time_finished: false } };
            component['setEventLiveStatusFromUpdate'](update as any);
            expect(component['eventIsLive']).toBeFalsy();
        });
    });

    describe('#isTeamScoresAvailable', () => {
        beforeEach(() => {
            fiveASideShowDownLobbyService.isValidValue.and.callFake((value) => {
                if (value === '0') {
                    return true;
                } else if (value === 0) {
                    return true;
                } else if (value === 1) {
                    return true;
                } else if (value === null) {
                    return false;
                }
            });
        });

        it('set isTeamScoresAvailable true when scores available', () => {
            component.homeScore = 0 as any;
            component.awayScore = 1 as any;
            expect(component['isTeamScoresAvailable']()).toBeTruthy();
        });

        it('set isTeamScoresAvailable true when scores available', () => {
            component.homeScore = '0';
            component.awayScore = '0';
            expect(component['isTeamScoresAvailable']()).toBeTruthy();
        });

        it('set isTeamScoresAvailable false when homeScore not available', () => {
            component.homeScore = null;
            component.awayScore = '0';
            expect(component['isTeamScoresAvailable']()).toBeFalsy();
        });

        it('set isTeamScoresAvailable false when awayScore not available', () => {
            component.homeScore = '0';
            component.awayScore = null;
            expect(component['isTeamScoresAvailable']()).toBeFalsy();
        });

        it('set isTeamScoresAvailable false when both scores are not available', () => {
            component.homeScore = null;
            component.awayScore = null;
            expect(component['isTeamScoresAvailable']()).toBeFalsy();
        });
    });

    describe('#handleETClockUpdate', () => {
        it('should return isExtraTimePeriod as true when period_code matches in array', () => {
            component.event = { clock: { period_code: 'EXTRA_TIME_FIRST_HALF' } } as any;
            component['handleETClockUpdate']();
            expect(component.isExtraTimePeriod).toBeTruthy();
        });
        it('should return isExtraTimePeriod as false when period_code not matches in array', () => {
            component.event = { clock: { period_code: 'FIRST_HALF' } } as any;
            component['handleETClockUpdate']();
            expect(component.isExtraTimePeriod).toBeFalsy();
        });
        it('should return isExtraTimePeriod as false when period_code not matches in array', () => {
            component.event = { clock: null } as any;
            component.isExtraTimePeriod = false;
            component['handleETClockUpdate']();
            expect(component.isExtraTimePeriod).toBeFalsy();
        });
    });

    describe('#isMatchFTorResulted', () => {
        it('should return true if match is either FT or resulted', () => {
            component.isMatchFT = true as any;
            expect(component.isMatchFTorResulted).toBeTruthy();
        });
        it('should return true if match is either FT or resulted', () => {
            component.isMatchFT = false as any;
            component.isEventResulted = true as any;
            expect(component.isMatchFTorResulted).toBeTruthy();
        });
        it('should return false if match is neither FT nor resulted', () => {
            component.isMatchFT = false as any;
            component.isEventResulted = false as any;
            expect(component.isMatchFTorResulted).toBeFalsy();
        });
    });

    describe('#createClockForEventForInit', () => {
        it('should add the clock to event', () => {
            component.event = { clock: undefined, started: true } as any;
            const update = { id: 123, seconds: '1' } as any;
            component['createClockForEventForInit']();
            expect(component.event.clock).not.toBeUndefined();
        });
        it('should not add the clock to the event', () => {
            component.event = { clock: undefined, started: false } as any;
            const update = { id: 123, seconds: '1' } as any;
            component['createClockForEventForInit']();
            expect(component.event.clock).toBeUndefined();
        });
        it('should not call liveEventClockProviderService', () => {
            component.event = { clock: {}, started: true } as any;
            const update = { id: 123, seconds: '1' } as any;
            component['createClockForEventForInit']();
            expect(liveEventClockProviderService.create).not.toHaveBeenCalled();
        });
    });
});
