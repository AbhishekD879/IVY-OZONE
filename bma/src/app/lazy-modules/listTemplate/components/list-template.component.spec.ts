import { of } from 'rxjs';
import { ListTemplateComponent } from '@app/lazy-modules/listTemplate/components/list-template.component';

describe('ListTemplateComponent', () => {
    let component: ListTemplateComponent;

    let
        templateService, marketTypeService, timeService, locale, filtersService, coreToolsService, routingHelper,
        pubSubService, router, smartBoostsService, userService, commandService,
        windowRef, betSlipSelectionsData, priceOddsButtonService, routingState, gtmTrackingService, gtmService,
        favouritesService, sportsConfigService, scoreParserService, sportEventHelperService, seoDataService;

    let testStr, wasPriceStub, changeDetectorRef;

    const today = new Date();
    const future = new Date();
    future.setDate(future.getDate() + 1);

    function fakeCall(time) {
        const formatted = new Date(time);
        /* eslint-disable */
        return time === `${today}` ? `${formatted.getHours()}:${formatted.getMinutes()}, Today` :
            `${formatted.getHours()}:${formatted.getMinutes()} ${future.toLocaleString('en-US', { day: '2-digit' })} ${formatted.toLocaleString('en-US', { month: 'short' })}`;
        /* eslint-enable */
    }

    beforeEach(() => {

        testStr = 'TestString';
        wasPriceStub = 'TestWasPrice';

        filtersService = {
            getTeamName: (name, index) => ['teamA', 'teamB'][index],
            groupBy: jasmine.createSpy('groupBy').and.callFake(v => v)
        };

        router = {
            navigateByUrl: jasmine.createSpy('navigateByUrl')
        };

        timeService = {
            determineDay: () => 'today',
            getLocalHourMin: () => { },
            isInNext24HoursRange: () => true,
            getEventTime: jasmine.createSpy().and.callFake(fakeCall)
        };

        routingHelper = {
            formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('some url')
        };

        coreToolsService = {
            uuid: jasmine.createSpy('uuid').and.returnValue('randomId'),
            hasOwnDeepProperty: jasmine.createSpy('hasOwnDeepProperty').and.callFake((obj, path) => {
                const properties = path.split('.');
                let current = obj;
                while (typeof current === 'object' && properties.length) {
                    const property = properties.shift();
                    current = current[property];
                }
                if (!properties.length) {
                    return current !== undefined;
                }
            }),
            getOwnDeepProperty: jasmine.createSpy('getOwnDeepProperty').and.callFake((obj, path) => {
                const properties = path.split('.');
                let current = obj;
                while (typeof current === 'object' && properties.length) {
                    const property = properties.shift();
                    current = current[property];
                }
                if (!properties.length) {
                    return current;
                }
            }),
        };

        locale = {
            getString: jasmine.createSpy('getString').and.returnValue('test')
        };

        templateService = {
            getSportViewTypes: () => {
                return {};
            },
            getTemplate: () => {
                return {};
            },
            isMultiplesEvent: () => false
        };

        changeDetectorRef = {
            detectChanges: jasmine.createSpy('detectChanges'),
        };
        seoDataService = {
            eventPageSeo: jasmine.createSpy('eventPageSeo')
        };
        marketTypeService = {
            isMatchResultType: jasmine.createSpy('isMatchResultType').and.returnValue(false),
            isHeader2Columns: jasmine.createSpy('isHeader2Columns').and.returnValue(false),
            isHomeDrawAwayType: jasmine.createSpy('isHomeDrawAwayType').and.returnValue(true)
        };

        pubSubService = {
            publish: jasmine.createSpy('publish'),
            unsubscribe: jasmine.createSpy(),
            subscribe: jasmine.createSpy().and.callFake((name: string, chnl: any, func: Function) => func({ event: { id: 1 } } as any)),
            API: {
                OUTCOME_UPDATED: 'OUTCOME_UPDATED',
                DELETE_SELECTION_FROMCACHE: 'DELETE_SELECTION_FROMCACHE',
                EVENT_SCORES_UPDATE: 'EVENT_SCORES_UPDATE',
                EVENTS_CLOCK_UPDATE: 'EVENTS_CLOCK_UPDATE',
                MOVE_EVENT_TO_INPLAY: 'MOVE_EVENT_TO_INPLAY',
                ADD_TO_BETSLIP_BY_SELECTION: 'ADD_TO_BETSLIP_BY_SELECTION',
                BETSLIP_SELECTIONS_UPDATE: 'BETSLIP_SELECTIONS_UPDATE',
                ADD_TO_QUICKBET: 'ADD_TO_QUICKBET',
                REMOVE_FROM_QUICKBET: 'REMOVE_FROM_QUICKBET',
                WS_EVENT_UPDATED: 'WS_EVENT_UPDATED',
                WS_EVENT_UPDATE: 'WS_EVENT_UPDATE'
            }
        };

        smartBoostsService = {
            isSmartBoosts: jasmine.createSpy().and.returnValue(true),
            parseName: jasmine.createSpy().and.returnValue({ name: testStr, wasPrice: wasPriceStub })
        };
        sportsConfigService = {
            getSport: jasmine.createSpy('getSport').and.returnValue(of({
                sportConfig: {
                    config: {}
                }
            }))
        };

        userService = {};

        commandService = {
            executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve(false)),
            API: {
                IS_ADDTOBETSLIP_IN_PROCESS: 'IS_ADDTOBETSLIP_IN_PROCESS'
            }
        };

        windowRef = {
            nativeWindow: {}
        };

        betSlipSelectionsData = {
            getSelectionsByOutcomeId: jasmine.createSpy('getSelectionsByOutcomeId').and.returnValue([{}])
        };

        priceOddsButtonService = {
            animate: jasmine.createSpy('animate').and.returnValue(Promise.resolve(true))
        };

        routingState = {
            getCurrentSegment: jasmine.createSpy('getCurrentSegment')
        };

        gtmTrackingService = {
            detectTracking: jasmine.createSpy('detectTracking')
        };

        gtmService = {
            push: jasmine.createSpy('push')
        };

        favouritesService = {
            registerListener: () => {
                return { then: jasmine.createSpy('then') };
            },
            deRegisterListener: jasmine.createSpy('deRegisterListener'),
            add: jasmine.createSpy('add').and.returnValue({
                catch: jasmine.createSpy('catch')
            }),
            isFavourite: jasmine.createSpy().and.returnValue(Promise.resolve()),
            showFavourites: jasmine.createSpy('showFavourites').and.returnValue(of(true))
        };

        scoreParserService = {
            getScoreType: jasmine.createSpy('getScoreType'),
            parseScores: jasmine.createSpy('parseScores')
        };

        sportEventHelperService = {
            isOutrightEvent: jasmine.createSpy('isOutrightEvent'),
            isSpecialEvent: jasmine.createSpy('isSpecialEvent')
        };

        component = new ListTemplateComponent(
            templateService as any,
            marketTypeService as any,
            timeService as any,
            locale as any,
            filtersService as any,
            coreToolsService as any,
            routingHelper as any,
            pubSubService as any,
            router as any,
            smartBoostsService as any,
            userService as any,
            commandService as any,
            windowRef as any,
            betSlipSelectionsData as any,
            priceOddsButtonService as any,
            routingState as any,
            gtmTrackingService as any,
            gtmService as any,
            favouritesService as any,
            sportsConfigService as any,
            scoreParserService as any,
            sportEventHelperService,
            changeDetectorRef,
            seoDataService as any
        );

        component.event = {
            name: 'Test',
            id: 111,
            marketsCount: 3,
            markets: [{
                id: 111,
                name: 'Test',
                outcomes: [{
                    id: 111,
                    name: 'Test'
                }],
                templateMarketName:''
            }],
            categoryName: 'categoryName',
            isStarted: true,
            eventIsLive: true,
            comments: {
                teams: {
                    home: {},
                    away: {}
                }
            }
        } as any;
        component.teamRoleCodes = ['home', 'away'];
        component.selectedMarketObject = component.event.markets[0];
        component.eventStartedOrLive = true;
        spyOn(component.marketUndisplayed, 'emit');
    });

    it('should create component instance', () => {
        expect(component).toBeTruthy();
    });

   
    describe('@toggleShow', () => {
        it('should limit be undefined', () => {
            component.allShown = false;
            component.toggleShow();
            expect(component.limit).toBeUndefined();
        });

        it('should limit be selectionsLimit', () => {
            component.allShown = true;
            component.toggleShow();
            expect(component.limit).toBe(component.selectionsLimit);
        });
    });
    describe('@isShowMarketsCount', () => {
        it('should isShowMarketsCount to be true', () => {
            component.event = {
                name: 'Test',
                id: 111,
                markets: [{
                    id: 111,
                    name: 'Test',
                    outcomes: [{
                        id: 111,
                        name: 'Test'
                    }],
                    templateMarketName:''
                },
                {
                    id: 222,
                    name: 'Test',
                    outcomes: [{
                        id: 222,
                        name: 'Test'
                    }],
                    templateMarketName:''
                }],
                categoryName: 'GOLF',
                categoryCode: 'GOLF',
                isStarted: true,
                eventIsLive: true,
                comments: {
                    teams: {
                        home: {},
                        away: {}
                    }
                }
            } as any;
            component.sportsViewTypes = {
                outrights: false
            };
            component.isOddsSports = true;
            expect(component.isShowMarketsCount()).toBeTrue();
        });
    });
});
