import { FanzoneAppOutrightsComponent } from "@app/fanzone/components/fanzoneOutrights/fanzone-outrights.component";
import { pubSubApi } from "@app/core/services/communication/pubsub/pubsub-api.constant";
import { liveChannelsEventData, EVENT_ENTITY } from '@app/fanzone/mockData/fanzone-outrights.component.mock';
import { FANZONEDETAILS } from '@app/fanzone/mockdata/fanzone-home.component.mock';
import { fanzoneSegmentMock } from "@app/fanzone/mockData/fanzone-now-next.component.mock";
import { fakeAsync, tick } from '@angular/core/testing';

describe('FanzoneAppOutrightsComponent', () => {
    const tagName = 'FanzoneAppOutrightsComponent';

    let component: FanzoneAppOutrightsComponent;

    let pubSubService;
    let changeDetectorRef;
    let channelService;
    let cacheEventsService;
    let updateEventService;
    let fanzoneModuleService;
    let fanzoneHelperService;
    let filtersService;
    let gtmService;
    let device;
    let sanitizer;
    let windowRefService;
    let domToolsService;
    let loc;

    const domElement = {
        style: {
            zIndex: '1002'
        }
    };
    const LEAGUE_BODY_CLASS = 'league-standings-opened';

    beforeEach(() => {
        pubSubService = {
            publish: jasmine.createSpy('publish'),
            subscribe: jasmine.createSpy('subscribe').and.callFake((domain, channel, fn) => fn && fn()),
            unsubscribe: jasmine.createSpy('unsubscribe'),
            API: pubSubApi
        };
        changeDetectorRef = {
            detectChanges: jasmine.createSpy('detectChanges')
        };
        channelService = {
            getLSChannelsFromArray: jasmine.createSpy('getLSChannelsFromArray').and.returnValue('1234'),
        };
        cacheEventsService = {
            store: jasmine.createSpy('getLSChannelsFromArray').and.callThrough(),
            clearByName: jasmine.createSpy('clearByName')
        };
        updateEventService = {
            init: jasmine.createSpy('init').and.callThrough()
        };
        fanzoneModuleService = {
            getFanzoneOutrights: jasmine.createSpy('getFanzoneOutrights').and.returnValue(Promise.resolve({}))
        };
        filtersService = {
            orderBy: jasmine.createSpy()
        };
        fanzoneHelperService = {
            selectedFanzone: jasmine.createSpy('selectedFanzone').and.returnValue(FANZONEDETAILS)
        };
        gtmService = { push: jasmine.createSpy('push') };
        device = { isDesktop: true };
        sanitizer = {
            bypassSecurityTrustResourceUrl: jasmine.createSpy('bypassSecurityTrustResourceUrl')
        };
        windowRefService = {
            document: {
                body: {
                    classList: {
                        add: jasmine.createSpy('add'),
                        remove: jasmine.createSpy('remove'),
                    }
                },
                querySelector: jasmine.createSpy('querySelector').and.returnValue(domElement)
            }
        };
        domToolsService = {
            addClass: jasmine.createSpy('addClass'),
            removeClass: jasmine.createSpy('removeClass'),
            css: jasmine.createSpy('css')
        };
        loc = {
            onPopState: jasmine.createSpy('onPopState')
        };

        component = new FanzoneAppOutrightsComponent(
            pubSubService,
            changeDetectorRef,
            channelService,
            cacheEventsService,
            updateEventService,
            fanzoneModuleService,
            fanzoneHelperService,
            filtersService,
            gtmService,
            device,
            sanitizer,
            windowRefService,
            domToolsService,
            loc
        );

        component.fanzoneDetails = FANZONEDETAILS;
        component.fanzoneTeam = fanzoneSegmentMock;
    });

    it('should create', () => {
        expect(loc.onPopState).toHaveBeenCalledWith(jasmine.any(Function));
        expect(component).toBeTruthy();
    });

    describe('ngOnInit', () => {
        it('should get fanzone details data ', fakeAsync(() => {
            component['loadFanzoneOutrights'] = jasmine.createSpy();
            component['pubSubService'].subscribe = jasmine.createSpy('pubSubService.subscribe')
                .and.callFake((filename: string, eventName: string, callback: Function) => {
                    if (eventName === 'FANZONE_DATA') {
                        callback(FANZONEDETAILS);

                        expect(component.fanzoneDetails).toBeDefined();

                    }
                });
            component.ngOnInit();

            tick();
            expect(component.loadFanzoneOutrights).toHaveBeenCalled();
        }));

        it(`should subscribe on OUTCOME_UPDATED`, fakeAsync(() => {
            component['loadFanzoneOutrights'] = jasmine.createSpy();
            component['filterOutcomes'] = jasmine.createSpy();
            component['pubSubService'].subscribe = jasmine.createSpy('pubSubService.subscribe')
            .and.callFake((filename: string, eventName: string, callback: Function) => {
                if (eventName === 'OUTCOME_UPDATED') {
                    callback(FANZONEDETAILS);

                }
            });
            component.ngOnInit();
            tick()
            expect(pubSubService.subscribe).toHaveBeenCalledWith(tagName, 'OUTCOME_UPDATED', jasmine.any(Function));
        
        }));

        it(`should subscribe on DELETE_EVENT_FROM_CACHE & DELETE_MARKET_FROM_CACHE`, fakeAsync(() => {
            component['loadFanzoneOutrights'] = jasmine.createSpy();
            component['filterOutcomes'] = jasmine.createSpy();
            component['pubSubService'].subscribe = jasmine.createSpy('pubSubService.subscribe')
            .and.callFake((filename: string, eventName: string[], callback: Function) => {
                callback(FANZONEDETAILS);
            });
            component.ngOnInit();

            expect(pubSubService.subscribe).toHaveBeenCalledWith(
                tagName, ['DELETE_EVENT_FROM_CACHE', 'DELETE_MARKET_FROM_CACHE'], jasmine.any(Function));
        }));

        it(`should subscribe on DELETE_SELECTION_FROMCACHE`, fakeAsync(() => {
            component['loadFanzoneOutrights'] = jasmine.createSpy();
            component['filterOutcomes'] = jasmine.createSpy();
            component['pubSubService'].subscribe = jasmine.createSpy('pubSubService.subscribe')
            .and.callFake((filename: string, eventName: string, callback: Function) => {
                if (eventName === 'DELETE_SELECTION_FROMCACHE') {
                    callback(FANZONEDETAILS);
                }
            });
            component.ngOnInit();

            expect(pubSubService.subscribe).toHaveBeenCalledWith(tagName, 'DELETE_SELECTION_FROMCACHE', jasmine.any(Function));
        }));

        it(`should subscribe on SUSPENDED_EVENT`, fakeAsync(() => {
            component['loadFanzoneOutrights'] = jasmine.createSpy();
            component['filterOutcomes'] = jasmine.createSpy();
            component['pubSubService'].subscribe = jasmine.createSpy('pubSubService.subscribe')
            .and.callFake((filename: string, eventName: string, callback: Function) => {
                if (eventName === 'SUSPENDED_EVENT') {
                    callback(FANZONEDETAILS);
                }
            });
            component.ngOnInit();

            expect(pubSubService.subscribe).toHaveBeenCalledWith(tagName, 'SUSPENDED_EVENT', jasmine.any(Function));
        }));

        it(`should subscribe on LIVE_MARKET_FOR_EDP`, fakeAsync(() => {
            component['loadFanzoneOutrights'] = jasmine.createSpy();
            component['filterOutcomes'] = jasmine.createSpy();
            component['pubSubService'].subscribe = jasmine.createSpy('pubSubService.subscribe')
            .and.callFake((filename: string, eventName: string, callback: Function) => {
                if (eventName === 'LIVE_MARKET_FOR_EDP') {
                    callback(FANZONEDETAILS);

                }
            });
            component.ngOnInit();

            expect(pubSubService.subscribe).toHaveBeenCalledWith(tagName, 'LIVE_MARKET_FOR_EDP', jasmine.any(Function));
        }));
    });

    it('ngOnDestroy', () => {
        component.isDesktop = false;
        component['setZIndex'] = jasmine.createSpy();
        component.ngOnDestroy();

        expect(component['setZIndex']).toHaveBeenCalled();
        expect(cacheEventsService.clearByName).toHaveBeenCalledWith('event');
        expect(pubSubService.publish).toHaveBeenCalledWith('UNSUBSCRIBE_LS', 'fanzone-outrights');
        expect(pubSubService.unsubscribe).toHaveBeenCalledWith(tagName);
    });

    it('loadFanzoneOutrights', fakeAsync(() => {
        const prepareCompetitionIds = spyOn<any>(component, 'prepareCompetitionIds').and.returnValue('123');
        fanzoneModuleService.getFanzoneOutrights.and.returnValue(Promise.resolve(EVENT_ENTITY));
        filtersService.orderBy.and.returnValue(EVENT_ENTITY);

        component.loadFanzoneOutrights();
        tick();
        expect(prepareCompetitionIds).toHaveBeenCalled();
        expect(filtersService.orderBy).toHaveBeenCalled();
        expect(component.eventEntity).toEqual(EVENT_ENTITY as any);
    }));

    it('loadFanzoneOutrights should throw error', fakeAsync(() => {
        spyOn<any>(component, 'prepareCompetitionIds').and.returnValue('123');
        fanzoneModuleService.getFanzoneOutrights.and.returnValue(Promise.reject({ "status": 500 }));

        component.loadFanzoneOutrights();
        tick();
        expect(component.eventEntity).toEqual([]);
    }));

    describe('#filterOutcomes', () => {
        beforeEach(() => {
            component.eventEntity = [
                {
                    id: 1992062,
                    markets: [
                        {
                            id: '42119538',
                            outcomes: [{ id: '160016381', teamExtIds: '4dsgumo7d4zupm2ugsvm4zm4d' }, { id: '160016379' }]
                        },
                        {
                            id: '42362001',
                            outcomes: [{ id: '161897575', teamExtIds: '4dsgumo7d4zupm2ugsvm4zm4d' }]
                        }
                    ]
                }
            ] as any;
        });
        it('should filter and return outcomes based on teamExtIds while getting the push updates', () => {
            const filteredEventEntity = [
                {
                    id: 1992062,
                    markets: [
                        { id: '42119538', outcomes: [{ id: '160016381', teamExtIds: '4dsgumo7d4zupm2ugsvm4zm4d' }] },
                        { id: '42362001', outcomes: [{ id: '161897575', teamExtIds: '4dsgumo7d4zupm2ugsvm4zm4d' }] }
                    ]
                }
            ] as any;

            spyOn<any>(component, 'applyFilters').and.returnValue(filteredEventEntity[0].markets[0].outcomes);

            component['filterOutcomes']({ id: '42119538' } as any);

            expect(component['applyFilters']).toHaveBeenCalledWith(component.eventEntity[0].markets[0] as any);
            expect(component.eventEntity).toEqual(filteredEventEntity);
        });

        it('should not be called applyFilters if market id is not matched in the eventEntity data', () => {
            component['applyFilters'] = jasmine.createSpy('applyFilters');

            component['filterOutcomes']({ id: '42119539' } as any);

            expect(component['applyFilters']).not.toHaveBeenCalled();
            expect(component.eventEntity).toEqual(component.eventEntity);
        });
    });

    describe('#applyFilters', () => {
        it('should filter teamExtIds outcomes of market', () => {
            const market = [{ id: '42119538', outcomes: [{ id: '160016381', teamExtIds: '123' }, { id: '160016379' }] }];

            const result = component['applyFilters'](market[0] as any);

            expect(result).toEqual([market[0].outcomes[0]] as any);
        });

        it('should return empty array', () => {
            const market = [{ id: '42119538', outcomes: [{ id: '160016381' }, { id: '160016379' }] }];

            const result = component['applyFilters'](market[0] as any);

            expect(result).toEqual([]);
        });

    });

    it('prepareCompetitionIds', () => {
        expect(component['prepareCompetitionIds']("442", " 441 , 440 ,443")).toEqual("442,441,440,443");
    });

    it('subscribe to be called', () => {
        component.eventEntity = liveChannelsEventData as any;
        component.liveConnection();

        expect(pubSubService.publish).toHaveBeenCalled();
    });

    describe('#leagueStandingsOpened', () => {
        it('should not be called setZIndex when leagueTableOpened is false & isDesktop is true', () => {
            component.leagueTableOpened = false;
            component.isDesktop = true;
            spyOn(component,'setZIndex');
            component['leagueStandingsOpened']();

            expect(domToolsService.addClass).toHaveBeenCalledWith(jasmine.anything(), LEAGUE_BODY_CLASS);
            expect(component.setZIndex).not.toHaveBeenCalled();
            expect(gtmService.push).toHaveBeenCalled();
        });

        it('should called setZIndex when leagueTableOpened is false & isDesktop is false', () => {
            component.leagueTableOpened = false;
            component.isDesktop = false;
            component['setZIndex'] = jasmine.createSpy();
            component['leagueStandingsOpened']();

            expect(domToolsService.addClass).toHaveBeenCalledWith(jasmine.anything(), LEAGUE_BODY_CLASS);
            expect(component['setZIndex']).toHaveBeenCalled();
            expect(gtmService.push).toHaveBeenCalled();
        });

        it('should not be called setZIndex when leagueTableOpened is true & isDesktop is true', () => {
            component.leagueTableOpened = true;
            component.isDesktop = true;
            component['setZIndex'] = jasmine.createSpy();
            component['leagueStandingsOpened']();

            expect(domToolsService.removeClass).toHaveBeenCalledWith(jasmine.anything(), LEAGUE_BODY_CLASS);
            expect(component['setZIndex']).not.toHaveBeenCalled();
        });

        it('should called setZIndex when leagueTableOpened is true & isDesktop is false', () => {
            component.leagueTableOpened = true;
            component.isDesktop = false;
            component['setZIndex'] = jasmine.createSpy();
            component['leagueStandingsOpened']();

            expect(domToolsService.removeClass).toHaveBeenCalledWith(jasmine.anything(), LEAGUE_BODY_CLASS);
            expect(component['setZIndex']).toHaveBeenCalled();
        });
    });

    it('#setZIndex', () => {
        component.timelineBarContainer = windowRefService.document.querySelector('.timeline-bar-container');
        component['setZIndex']('0');
        expect(domToolsService.css).toHaveBeenCalledWith(jasmine.any(Object), 'z-index', '0');
        expect(component.timelineBarContainer.style.zIndex).toEqual('0');
    });

    describe('removeStandingsClass', () => {
        it('should removeStandingsClass', () => {
            component['removeStandingsClass']();
            expect(domToolsService.removeClass).toHaveBeenCalledWith(jasmine.anything(), LEAGUE_BODY_CLASS);
        });
    });
});