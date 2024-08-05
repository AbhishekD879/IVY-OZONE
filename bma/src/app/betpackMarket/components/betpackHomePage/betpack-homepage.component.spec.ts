import { BetpackHomepageComponent } from '@app/betpackMarket/components/betpackHomePage/betpack-homepage.component';
import { of } from 'rxjs/internal/observable/of';
import { fakeAsync, flush, tick } from '@angular/core/testing';
import {ACCOUNT_FREE_BETS} from '@app/betpackReview/components/betpackReviewHomePage/mockData/betpack-review-homepage.mock';
import { ACCOUNT_LIMIT, BETPACKOFFER } from '@app/betpackMarket//constants/betpack.constants';

describe('BetpackHomepageComponent', () => {
    let component,
        pubSubService,
        userService,
        currencyPipe,
        serviceClosureService,
        betpackCmsService,
        changeDetectorRef,
        freeBetsService,
        storage,
        device,
        bonusSuppression,
        bppProviderService,
        timeService,
        sessionStorage,
        componentFactoryResolver,
        dialogService,
        liveServConnectionService: any,
        gtmService;

    let fakeConnection;
    beforeEach(() => {
        pubSubService = {
            subscribe: jasmine.createSpy('subscribe'),
            publish: jasmine.createSpy('publish'),
            unsubscribe: jasmine.createSpy('unsubscribe'),
            API: {
                SESSION_LOGIN: 'SESSION_LOGIN',
                USER_CLOSURE_PLAY_BREAK: 'USER_CLOSURE_PLAY_BREAK'
            }
        };
        changeDetectorRef = {
            detectChanges: jasmine.createSpy('detectChanges'),
        };
        serviceClosureService = {
            userServiceClosureOrPlayBreakCheck: jasmine.createSpy('userServiceClosureOrPlayBreakCheck').and.returnValue(true),
            userServiceClosureOrPlayBreak: true
        };
        betpackCmsService = {
            betpackLabels: {
                betPackMarketplacePageTitle: 'BET BUNDLES',
                maxBetPackPerDayBannerLabel: 'only 1 bet pack per day',
                betPackAlreadyPurchasedPerDayBannerLabel: 'daily limit exceeded',
                isDailyLimitBannerEnabled: true,
            },
            getFreeBets: {},
            getBetPackDetails: jasmine.createSpy('getBetPackDetails').and.returnValue(of([{ betPackActive: true, sortOrder: -60 }, { betPackActive: false, sortOrder: -40 }, { betPackActive: true, sortOrder: -20 }])),
            getAccountLevelLimits: jasmine.createSpy('getAccountLevelLimits').and.returnValue(of({ response: { model: { activeLimits: { limitEntry: { limitRemaining: 1, limitDefinition: { limitComponent: { limitParam: [{ name: "current", value: 0 }, { name: "threshold", value: 1 }] } } } } } } })),
            getBetPackLabels: jasmine.createSpy('getBetPackLabels').and.returnValue({ subscribe: jasmine.createSpy('subscribe') }),
            getBetPackBanners: jasmine.createSpy('getBetPackBanners').and.returnValue(of({ bannerTextDescInMarketPlacePage: 'test' }))
        };
        freeBetsService = {
            getFreeBets: jasmine.createSpy('getFreeBets').and.returnValue(of([{}])),
            getAccLimitFreeBetReq: jasmine.createSpy('getAccLimitFreeBetReq').and.returnValue(of(BETPACKOFFER))
        };
        currencyPipe = {
            transform: jasmine.createSpy('transform')
        };
        userService = {
            status: true, maxStakeScale: '0.2', bppToken: true,
            isInShopUser: jasmine.createSpy('isInShopUser').and.returnValue(true),
            username: 'testUser',
        } as any;
        storage = {
            set: jasmine.createSpy('set'),
            get: jasmine.createSpy('get').and.returnValue({ onBoardingTutorial: { 'betPack-testUser': true } })
        };
        device = {
            isMobile: jasmine.createSpy('isMobile').and.returnValue(true),
            isDesktop: jasmine.createSpy('isDesktop').and.returnValue(true),
        };
        bppProviderService = {
            initialWSGetLimits: jasmine.createSpy('initialWSGetLimits').and.returnValue(of({ response: { respFreebetGetOffers: { freebetOffer: [{ freebetOfferId: '37505', freebetOfferLimits: { limitEntry: [{ limitId: 37441, limitRemaining: 90, limitDefinition: { limitComponent: { limitParam: [{ name: 'current', value: 10 }, { name: 'threshold', value: 100 }] } } }] } }] } } })),
        };
        bonusSuppression = {
            navigateAwayForRGYellowCustomer: jasmine.createSpy('navigateAwayForRGYellowCustomer'),
            checkIfYellowFlagDisabled: jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(true)
        };
        liveServConnectionService = {
            connect: jasmine.createSpy('connect').and.returnValue(of(fakeConnection)),
            unsubscribeBP: jasmine.createSpy('unsubscribeBP').and.returnValue(of({})),
            subscribeBP: jasmine.createSpy('subscribe').and.returnValue(of({})),
        };
        gtmService = {
            push: jasmine.createSpy('push')
        };
        timeService = {
            parseDateTime: (parseDate) => {
                return new Date(parseDate);
            },
            compareDate:jasmine.createSpy('compareDate').and.returnValue(1)
        };
        sessionStorage = {
            get: jasmine.createSpy('get'),
            set: jasmine.createSpy('set'),
            remove: jasmine.createSpy('remove')
        };
        componentFactoryResolver = {
            resolveComponentFactory: jasmine.createSpy('resolveComponentFactory')
        };
        dialogService = jasmine.createSpyObj('dialogService', ['openDialog', 'closeDialog']);
        component = new BetpackHomepageComponent(pubSubService,
            userService,
            currencyPipe,
            serviceClosureService,
            betpackCmsService,
            changeDetectorRef,
            freeBetsService,
            storage,
            device,
            bonusSuppression,
            bppProviderService,
            liveServConnectionService,
            timeService,
            sessionStorage,
            dialogService,
            componentFactoryResolver,
            gtmService
        );
        component.betpackLabels = {
            betPackMarketplacePageTitle: 'BET BUNDLES',
            maxBetPackPerDayBannerLabel: 'only 1 bet pack per day',
            betPackAlreadyPurchasedPerDayBannerLabel: 'daily limit exceeded',
            isDailyLimitBannerEnabled: true
        };
    });

    describe('constructor', () => {
        it('bet pack data should be disabled', fakeAsync(() => {
            userService = { status: true, maxStakeScale: '0.2' } as any;
            pubSubService['subscribe'] = jasmine.createSpy().and.callFake((fileName, method, callback) => {
                if (method === 'STORE_STAKE_FACTOR') {
                    callback('');
                }
            });

            component = new BetpackHomepageComponent(pubSubService,
                userService,
                currencyPipe,
                serviceClosureService,
                betpackCmsService,
                changeDetectorRef,
                freeBetsService,
                storage,
                device,
                bonusSuppression,
                bppProviderService,
                liveServConnectionService,
                timeService,
                sessionStorage,
                dialogService,
                componentFactoryResolver,
                gtmService
            );
            expect(component.disableBetPack).toEqual(true);

        }));

        it('bet pack data should be enabled when user is not logged in ', fakeAsync(() => {
            userService = { status: false } as any;
            pubSubService['subscribe'] = jasmine.createSpy().and.callFake((fileName, method, callback) => {
                if (method === 'STORE_STAKE_FACTOR') {
                    callback('');
                }
            });

            component = new BetpackHomepageComponent(pubSubService,
                userService,
                currencyPipe,
                serviceClosureService,
                betpackCmsService,
                changeDetectorRef,
                freeBetsService,
                storage,
                device,
                bonusSuppression,
                bppProviderService,
                liveServConnectionService,
                timeService,
                sessionStorage,
                dialogService,
                componentFactoryResolver,
                gtmService
            );
            expect(component.disableBetPack).toEqual(false);
        }));

        it('bet pack data should be enabled when stake factor is not present', fakeAsync(() => {
            userService = { status: true } as any;
            pubSubService['subscribe'] = jasmine.createSpy().and.callFake((fileName, method, callback) => {
                if (method === 'STORE_STAKE_FACTOR') {
                    callback('');
                }
            });

            component = new BetpackHomepageComponent(pubSubService,
                userService,
                currencyPipe,
                serviceClosureService,
                betpackCmsService,
                changeDetectorRef,
                freeBetsService,
                storage,
                device,
                bonusSuppression,
                bppProviderService,
                liveServConnectionService,
                timeService,
                sessionStorage,
                dialogService,
                componentFactoryResolver,
                gtmService
            );
            expect(component.disableBetPack).toEqual(false);
        }));

        it('bet pack data should be enabled when stake factor is more', fakeAsync(() => {
            userService = { status: true, maxStakeScale: '75.2' } as any;
            pubSubService['subscribe'] = jasmine.createSpy().and.callFake((fileName, method, callback) => {
                if (method === 'STORE_STAKE_FACTOR') {
                    callback('');
                }
            });
            component = new BetpackHomepageComponent(pubSubService,
                userService,
                currencyPipe,
                serviceClosureService,
                betpackCmsService,
                changeDetectorRef,
                freeBetsService,
                storage,
                device,
                bonusSuppression,
                bppProviderService,
                liveServConnectionService,
                timeService,
                sessionStorage,
                dialogService,
                componentFactoryResolver,
                gtmService
            );
            expect(component.disableBetPack).toEqual(false);
        }));

        it('bet pack data should be enabled user logged out', fakeAsync(() => {
            userService = { status: false } as any;
            pubSubService['subscribe'] = jasmine.createSpy().and.callFake((fileName, method, callback) => {
                if (method === 'SESSION_LOGOUT') {
                    callback('');
                }
            });
            component = new BetpackHomepageComponent(pubSubService,
                userService,
                currencyPipe,
                serviceClosureService,
                betpackCmsService,
                changeDetectorRef,
                freeBetsService,
                storage,
                device,
                bonusSuppression,
                bppProviderService,
                liveServConnectionService,
                timeService,
                sessionStorage,
                dialogService,
                componentFactoryResolver,
                gtmService
            );
            expect(component.disableBetPack).toEqual(false);
        }));

        it('should navigate to homepage in case of rgy user', fakeAsync(() => {
            userService.status = true;
            bonusSuppression.checkIfYellowFlagDisabled = jasmine.createSpy('checkIfYellowFlagDisabled').and.returnValue(false);
            pubSubService = {
                subscribe: jasmine.createSpy().and.callFake((fileName, method, callback) => {
                    if (method !== 'RELOAD_COMPONENTS') {
                        callback();
                    }
                }),
                API: {
                    SESSION_LOGIN: 'SESSION_LOGIN',
                    RELOAD_COMPONENTS: 'RELOAD_COMPONENTS'
                }
            };
            betpackCmsService = {
                getAccountLevelLimits: jasmine.createSpy('getAccountLevelLimits').and.returnValue(of(ACCOUNT_LIMIT)),
                betpackLabels: { isDailyLimitBannerEnabled: false },
                getBetPackBanners: jasmine.createSpy('getBetPackBanners').and.returnValue(of({ bannerTextDescInMarketPlacePage: 'test' }))
            };
            freeBetsService = {
                getFreeBets: jasmine.createSpy('getFreeBets').and.returnValue(of([{}])),
                getAccLimitFreeBetReq: jasmine.createSpy('getAccLimitFreeBetReq').and.returnValue(of(BETPACKOFFER))
            };
            component.bannerData = {
                bannerTextDescInMarketPlacePage: 'test'
            }
            component = new BetpackHomepageComponent(pubSubService,
                userService,
                currencyPipe,
                serviceClosureService,
                betpackCmsService,
                changeDetectorRef,
                freeBetsService,
                storage,
                device,
                bonusSuppression,
                bppProviderService,
                liveServConnectionService,
                timeService,
                sessionStorage,
                dialogService,
                componentFactoryResolver,
                gtmService
            );

            spyOn(component, 'init');
            expect(bonusSuppression.navigateAwayForRGYellowCustomer).toHaveBeenCalled();
            flush();
        }));
    });

    describe('init', () => {
        it('getAccountLevelLimits should be called in case of data not in storage', () => {
            component = new BetpackHomepageComponent(pubSubService,
                userService,
                currencyPipe,
                serviceClosureService,
                betpackCmsService,
                changeDetectorRef,
                freeBetsService,
                storage,
                device,
                bonusSuppression,
                bppProviderService,
                liveServConnectionService,
                timeService,
                sessionStorage,
                dialogService,
                componentFactoryResolver,
                gtmService
            );
            spyOn(component, 'getLimitsCheck');
            spyOn(component, 'getPrompt');
            spyOn(component, 'expiringTokenCount');
            betpackCmsService.getAccountLevelLimits = jasmine.createSpy('getAccountLevelLimits').and.returnValue(of(ACCOUNT_LIMIT)),
                component.init();
            expect(betpackCmsService.getAccountLevelLimits).toHaveBeenCalled();
            expect(component.getLimitsCheck).toHaveBeenCalled();
        });

        it('getAccountLevelLimits should not be called', () => {
            userService.status = false;
            spyOn(component, 'betpackDetailsFormat');
            spyOn(component, 'expiringTokenCount')
            component.init();
            expect(betpackCmsService.getAccountLevelLimits).not.toHaveBeenCalled();
        });

        it('getAccountLevelLimits when user limits are unlimited', () => {
            userService.status = true;
            betpackCmsService.getAccountLevelLimits = jasmine.createSpy('getAccountLevelLimits').and.returnValue(of({ response: { model: { activeLimits: { limitEntry: { limitRemaining: 1, limitDefinition: { limitComponent: { limitParam: [{ name: "current", value: 0 }, { name: "threshold", value: 1 }] } } } } } } })),
                spyOn(component, 'checkLimitAvailable').and.returnValue(false);
            spyOn(component, 'expiringTokenCount')
            component.init();
            expect(component.getLimitsData).toBe('unlimited');
        });

        it('getAccountLevelLimits userLimitsCheck should be called', () => {
            userService.status = true;
            betpackCmsService.getAccountLevelLimits = jasmine.createSpy('getAccountLevelLimits').and.returnValue(of({ response: { model: { activeLimits: { limitEntry: { limitRemaining: 1, limitDefinition: { limitComponent: { limitParam: [{ name: "current", value: 0 }, { name: "threshold", value: 1 }] } } } } } } })),
                spyOn(component, 'checkLimitAvailable').and.returnValue(true);
            spyOn(component, 'userLimitsCheck')
            spyOn(component, 'expiringTokenCount')
            component.init();
            expect(component.userLimitsCheck).toHaveBeenCalled();
        });
        it('accLimitFreeBets userLimitsCheck should be called1', () => {
            userService.status = true;      
            betpackCmsService.getAccountLevelLimits = jasmine.createSpy('getAccountLevelLimits').and.returnValue(of({ response: { model: { activeLimits: { limitEntry: { limitRemaining: 1, limitDefinition: { limitComponent: { limitParam: [{ name: "current", value: 0 }, { name: "threshold", value: 1 }] } } } } } } })),      
            freeBetsService.getAccLimitFreeBetReq = jasmine.createSpy('getAccLimitFreeBetReq').and.returnValue(of(null)),      
            spyOn(component, 'checkLimitAvailable').and.returnValue(true);      
            spyOn(component, 'userLimitsCheck');      
            spyOn(component, 'expiringTokenCount');      
            component.init();      
            expect(component.userLimitsCheck).toHaveBeenCalled();      
          });
    });

    describe('ngOnInit', () => {
        it('ngOnInit should be called', fakeAsync(() => {
            component.betpackDetailsMaster = {
                betPackActive: true,
                betPackEndDate: "2022-08-31T06:05:36Z",
                betPackFreeBetsAmount: "£1"
            };
            spyOn(component, 'reloadComponent');
            pubSubService.subscribe = jasmine.createSpy().and.callFake((fileName, method, callback) => {
                if (method == pubSubService.API.USER_CLOSURE_PLAY_BREAK) {
                    callback(true);
                }
                else {
                    callback();
                }
            });
            spyOn(component, 'getCmsBetpackDetails')
            spyOn(component, 'init')
            spyOn(component, 'betpackDetailsFormat')
            spyOn(component, 'getPrompt');
            spyOn(component, 'getBannerData');
            component.ngOnInit();
            expect(component.topBarInnerContent).toBeTruthy();
            expect(pubSubService.subscribe).toHaveBeenCalled();
            expect(dialogService.closeDialog).toHaveBeenCalled();
        }));

        it('ngOnInit should be called in case of different betpack labels', fakeAsync(() => {
            component.betpackDetailsMaster = {
                betPackActive: true,
                betPackEndDate: "2022-08-31T06:05:36Z",
                betPackFreeBetsAmount: "£1"
            };
            pubSubService.subscribe = jasmine.createSpy().and.callFake((fileName, method, callback) => {
                callback();
            });
            spyOn(component, 'reloadComponent');
            spyOn(component, 'getCmsBetpackDetails')
            spyOn(component, 'init')
            spyOn(component, 'betpackDetailsFormat')
            spyOn(component, 'getPrompt');
            spyOn(component, 'getBannerData');
            betpackCmsService.betpackLabels.betPackMarketplacePageTitle = 'BET PACK';
            component.ngOnInit();
            expect(component.topBarInnerContent).toBeFalsy();
        }));

        it('ngOnInit should be called in case of no betpack labels', fakeAsync(() => {
            component.betpackDetailsMaster = {
                betPackActive: true,
                betPackEndDate: "2022-08-31T06:05:36Z",
                betPackFreeBetsAmount: "£1"
            }
            spyOn(component, 'getCmsBetpackDetails')
            spyOn(component, 'init')
            spyOn(component, 'betpackDetailsFormat')
            spyOn(component, 'getPrompt');
            spyOn(component, 'getBannerData');
            betpackCmsService.betpackLabels = null;
            component.ngOnInit();
            expect(component.topBarInnerContent).toBeFalsy();
        }));
    });

    describe('reloadComponent', () => {
        it('should reload', () => {
            spyOn(component, 'ngOnDestroy');
            spyOn(component, 'initialCall');
            spyOn(component, 'ngOnInit');
            component.reloadComponent();
            expect(component.ngOnDestroy).toHaveBeenCalled();
        });
    });

    describe('getPrompt', () => {
        it('getPrompt when limit greaterthan 0', () => {
            component.betpackLabels.isDailyLimitBannerEnabled = true;
            component.filteredBetPacksList = [{}];
            component.filteredBetPack = [{}];
            component.userLimits = 5;
            component.getPrompt();
            expect(component.message).toEqual(component.betpackLabels.maxBetPackPerDayBannerLabel);
            expect(component.isPromptDisplay).toBeTruthy();
        });

        it('getPrompt when limit equal to 0', () => {
            component.betpackLabels.isDailyLimitBannerEnabled = true;
            component.filteredBetPacksList = [{}];
            component.filteredBetPack = [{}];
            component.userLimits = 0;
            component.thresholdLimit = 2;
            component.getPrompt();
            expect(component.message).toEqual(component.betpackLabels.betPackAlreadyPurchasedPerDayBannerLabel);
            expect(component.isPromptDisplay).toBeTruthy();
        });

        it('getPrompt when no betpacks existing scenario-1', () => {
            component.filteredBetPacksList = [];
            component.filteredBetPack = [];
            component.getPrompt();
            expect(component.message).toBeUndefined();
            expect(component.isPromptDisplay).not.toBeTruthy();
        });

        it('getPrompt when no betpacks existing scenario-2', () => {
            component.filteredBetPacksList = null;
            component.filteredBetPack = null;
            component.getPrompt();
            expect(component.message).toBeUndefined();
            expect(component.isPromptDisplay).not.toBeTruthy();
        });
    });

    describe('get closeNotification', () => {
        it('closeNotification return false', () => {
            component.closeNotification();
            expect(component.isPromptDisplay).toBeFalsy()
        });
    });

    describe('get isValidOBBetpack', () => {
        it('isValidOBBetpack return true', () => {
            const startDate = new Date(new Date().setDate(new Date().getDate() - 1)).toISOString();
            const endDate = new Date(new Date().setDate(new Date().getDate() + 1)).toISOString();
            const retVal = component.isValidOBBetpack({ betPackStartDate: startDate, betPackEndDate: endDate });
            expect(retVal).toBeTruthy();
        });

        it('isValidOBBetpack return false', () => {
            const startDate = new Date(new Date().setDate(new Date().getDate() + 1)).toISOString();
            const endDate = new Date(new Date().setDate(new Date().getDate() - 1)).toISOString();
            const retVal = component.isValidOBBetpack({ betPackStartDate: startDate, betPackEndDate: endDate });
            expect(retVal).toBeFalsy();
        });
    });

    describe('get filteredBetPacks', () => {
        it('filteredBetPacks return true', () => {
            component.filteredBetPackEnable = new Map();
            const betpackDetails = [{ filterList: [{ val: 1 }] }, { filterList: [{ val: 2 }] }];
            component.betpackDetails = [{ betPackId: 1, filterList: ['All', 'Some'] }];
            component.filteredBetPacks(betpackDetails);
            expect(component.filteredBetPack).toBe(betpackDetails);
        });

        it('filteredBetPacks return false', () => {
            const betpackDetails = [];
            component.betpackDetails = [{ betPackId: 1, filterList: ['All', 'Some'] }];
            component.filteredBetPacks(betpackDetails);
            expect(component.filteredBetPack).toBe(betpackDetails);
        });
    });

    describe('get getLimitsCheck', () => {
        it('getLimitsCheck should be equal', () => {
            const getlimits = 0;
            component.getLimitsCheck(getlimits);
            expect(component.isMaxPurchaseLimitOver).toBeTruthy();
        });
        it('getLimitsCheck should be not equal', () => {
            const getlimits = { limitParam: [{ value: 0 }, { value: 1 }] };
            component.getLimitsCheck(getlimits);
            expect(component.isMaxPurchaseLimitOver).toBeFalsy();

            userService.status = false;
            component = new BetpackHomepageComponent(pubSubService, userService, currencyPipe, serviceClosureService, betpackCmsService, changeDetectorRef, freeBetsService, storage, device, bonusSuppression, bppProviderService, liveServConnectionService, timeService, sessionStorage, dialogService, componentFactoryResolver, gtmService);
            const getlimits1 = { limitParam: [{ value: 0 }, { value: 1 }] };
            component.getLimitsCheck(getlimits1);
            expect(component.isMaxPurchaseLimitOver).toBeFalsy();
        });
    });

    describe('get onFilterTabChange', () => {
        it('should invoke if clicked on this differeent filter other than ALL', () => {
            const filter = { filterName: 'Some' };
            component.betpackDetails = [{ betPackId: 1, filterList: ['All', 'Some'] }, { betPackId: 2, filterList: ['All'] }];
            component.onFilterTabChange(filter);
            expect(component.filteredBetPackEnable.size).toBe(2);
        });

        it('should invoke if clicked on ALL filter', () => {
            component.filteredBetPackEnable = new Map();
            const filter = { filterName: 'All' };
            component.betpackDetails = [{ betPackId: 1, filterList: ['All', 'Some'] }]
            component.onFilterTabChange(filter);
            expect(component.filteredBetPackEnable.size).toBe(1);
        });

        it('should invoke if clicked on ALL filter when filteredBetPackEnable is not defined', () => {
            const filter = { filterName: 'All' };
            component.betpackDetails = [{ betPackId: 1, filterList: ['All', 'Some'] }]
            component.onFilterTabChange(filter);
            expect(component.filteredBetPackEnable).toBeUndefined();
        });
    });

    describe('getCmsBetpackDetails', () => {
        it('should be called', fakeAsync(() => {
            spyOn(component, 'betpackDetailsFormat');
            spyOn(component, 'isValidOBBetpack').and.returnValue(true);
            spyOn(component, 'init')
            component.getCmsBetpackDetails();
            tick(1000);
            expect(component.betpackDetailsMaster.length).toBe(2);
        }));

        it('should be called with different sort order', fakeAsync(() => {
            spyOn(component, 'betpackDetailsFormat');
            spyOn(component, 'init')
            spyOn(component, 'isValidOBBetpack').and.returnValue(true);
            betpackCmsService.getBetPackDetails = jasmine.createSpy('getBetPackDetails').and.returnValue(of([{ betPackActive: true, sortOrder: 60 }, { betPackActive: false, sortOrder: 40 }, { betPackActive: true, sortOrder: 20 }])),
                component.getCmsBetpackDetails();
            tick(1000);
            expect(component.betpackDetailsMaster.length).toBe(2);
        }));

        it('should be called with equal sort order', fakeAsync(() => {
            spyOn(component, 'betpackDetailsFormat');
            spyOn(component, 'init')
            spyOn(component, 'isValidOBBetpack').and.returnValue(true);
            betpackCmsService.getBetPackDetails = jasmine.createSpy('getBetPackDetails').and.returnValue(of([{ betPackActive: true, sortOrder: 60 }, { betPackActive: false, sortOrder: 40 }, { betPackActive: true, sortOrder: 60 }])),
                component.getCmsBetpackDetails();
            tick(1000);
            expect(component.betpackDetailsMaster.length).toBe(2);
        }));

        it('should be called in case of no betpacks', fakeAsync(() => {
            spyOn(component, 'isValidOBBetpack').and.returnValue(true);
            betpackCmsService.getBetPackDetails = jasmine.createSpy('getBetPackDetails').and.returnValue(of([])),
                component.getCmsBetpackDetails();
            tick(1000);
            expect(component.betpackDetailsMaster.length).toBe(0);
            expect(component.betpackCmsService.userloginLoaded).toBeFalsy();
        }));
    });

    describe('betpackDetailsFormat', () => {
        it('should be called', () => {
            spyOn(component, 'filteredBetPacks');
            device.isMobile = true;
            component.betpackDetailsFromBuyNowClicked = { bp: { betPackId: 1 } };
            component.betpackDetailsMaster = [{
                betPackId: 1,
                betPackPurchaseAmount: '2', betPackFreeBetsAmount: '2',
                betPackMoreInfoText: 'text',
                betPackTokenList: [{ tokenTitle: "4 accumulator" }]
            }];
            component.betpackDetailsFormat();
            expect(component.betpackDetails.length).toBe(1);
            expect(pubSubService.publish).toHaveBeenCalled();
            expect(pubSubService.publish.calls.argsFor(0)[0]).toBe('BETPACK_POPUP_UPDATE');
        });

        it('should be called when tokens have no currency', () => {
            spyOn(component, 'filteredBetPacks');
            component.betpackDetailsMaster = [{
                betPackId: 2,
                betPackPurchaseAmount: '2', betPackFreeBetsAmount: '2',
                betPackMoreInfoText: 'text',
                betPackTokenList: [{ tokenTitle: "accumulator" }],
                expiresIntimer: 1000
            }];
            component.betpackLabels = { expiresInLabel: 'Expires' };
            component.betpackDetailsFromBuyNowClicked = { bp: { betPackId: 2 } };
            component.betpackDetailsFormat();
            expect(component.betpackDetailsFromBuyNowClicked.signPostingMsg).toBe(component.betpackLabels.expiresInLabel);
            expect(component.betpackDetails.length).toBe(1);
            expect(pubSubService.publish.calls.argsFor(0)[0]).toBe('BETPACK_POPUP_UPDATE');
        });

        it('should not set current & threshold in case of invalid response from initialWSGetLimits (no respFreebetGetOffers)', () => {
            spyOn(component, 'filteredBetPacks');
            component.betpackDetailsMaster = [{
                betPackPurchaseAmount: '2', betPackFreeBetsAmount: '2',
                betPackMoreInfoText: 'text',
                betPackTokenList: [{ tokenTitle: "accumulator" }]
            }];
            bppProviderService.initialWSGetLimits = jasmine.createSpy('initialWSGetLimits').and.returnValue(of({ response: {} }));
            component.betpackDetailsFormat();
            expect(component.current).toBeUndefined();
            expect(component.threshold).toBeUndefined();
        });

        it('should not set current & threshold in case of invalid response from initialWSGetLimits (no response)', () => {
            spyOn(component, 'filteredBetPacks');
            component.betpackDetailsMaster = [{
                betPackPurchaseAmount: '2', betPackFreeBetsAmount: '2',
                betPackMoreInfoText: 'text',
                betPackTokenList: [{ tokenTitle: "accumulator" }]
            }];
            bppProviderService.initialWSGetLimits = jasmine.createSpy('initialWSGetLimits').and.returnValue(of({}));
            component.betpackDetailsFormat();
            expect(component.current).toBeUndefined();
            expect(component.threshold).toBeUndefined();
        });

        it('should not set current & threshold in case of null response from initialWSGetLimits', () => {
            spyOn(component, 'filteredBetPacks');
            component.betpackDetailsMaster = [{
                betPackPurchaseAmount: '2', betPackFreeBetsAmount: '2',
                betPackMoreInfoText: 'text',
                betPackTokenList: [{ tokenTitle: "accumulator" }]
            }];
            bppProviderService.initialWSGetLimits = jasmine.createSpy('initialWSGetLimits').and.returnValue(of(null));
            component.betpackDetailsFormat();
            expect(component.current).toBeUndefined();
            expect(component.threshold).toBeUndefined();
        });
    });

    describe('betpack Onboarding', () => {
        it('Should call loadBetPackInfo on load when local storage has onBoardtutorial', () => {
            userService.username = 'testUser';
            device = { isMobile: true } as any;
            storage = {
                get: jasmine.createSpy('get').and.returnValue({ onBoardingTutorial: { 'betPack-testUser': true } })
            };
            component = new BetpackHomepageComponent(pubSubService, userService, currencyPipe, serviceClosureService, betpackCmsService, changeDetectorRef, freeBetsService, storage, device, bonusSuppression, bppProviderService, liveServConnectionService, timeService, sessionStorage, dialogService, componentFactoryResolver, gtmService);
            spyOn(component, 'getBannerData');
            component.ngOnInit();

            expect(component.isUserLoggedIn).toEqual(true);
            expect(component.isMobile).toEqual(true);
        });
        -
            it('Should call loadBetPackInfo on load when local storage doesnt have onBoardtutorial', () => {
                spyOn(component, 'getBannerData');
                userService.username = 'testUser';
                device = { isMobile: true } as any;
                storage = {
                    get: jasmine.createSpy('get').and.returnValue(false)
                };
                component = new BetpackHomepageComponent(pubSubService, userService, currencyPipe, serviceClosureService, betpackCmsService, changeDetectorRef, freeBetsService, storage, device, bonusSuppression, bppProviderService, liveServConnectionService, timeService, sessionStorage, dialogService, componentFactoryResolver, gtmService);
                spyOn(component, 'getBannerData');
                component.ngOnInit();

                expect(component.isUserLoggedIn).toEqual(true);
                expect(component.isMobile).toEqual(true);
            });

        it('isKYCVerified should be false when KYC is not verified', () => {
            userService = {
                isInShopUser: jasmine.createSpy('isInShopUser').and.returnValue(true),
                username: 'testUser',
            } as any;
            betpackCmsService.kycVerified = false;
            betpackCmsService.verificationStatus = 'Pending';
            device = { isMobile: true } as any;
            storage = {
                get: jasmine.createSpy('get').and.returnValue(false)
            };
            component = new BetpackHomepageComponent(pubSubService, userService, currencyPipe, serviceClosureService, betpackCmsService, changeDetectorRef, freeBetsService, storage, device, bonusSuppression, bppProviderService, liveServConnectionService, timeService, sessionStorage, dialogService, componentFactoryResolver, gtmService);
            spyOn(component, 'getBannerData');

            component.ngOnInit();

            expect(component.isKYCVerified).toEqual(false);
        });

        it('isKYCVerified should be true when KYC is verified', () => {
            betpackCmsService.getBetPackBanners = jasmine.createSpy('getBetPackBanners').and.returnValue({ bannerTextDescInMarketPlacePage: 'test' })
            userService = {
                isInShopUser: jasmine.createSpy('isInShopUser').and.returnValue(false),
                username: 'testUser',
            } as any;
            betpackCmsService.kycVerified = true;
            betpackCmsService.verificationStatus = 'Verified';
            device = { isMobile: true } as any;
            storage = {
                get: jasmine.createSpy('get').and.returnValue(false)
            };
            component = new BetpackHomepageComponent(pubSubService, userService, currencyPipe, serviceClosureService, betpackCmsService, changeDetectorRef, freeBetsService, storage, device, bonusSuppression, bppProviderService, liveServConnectionService, timeService, sessionStorage, dialogService, componentFactoryResolver, gtmService);
            spyOn(component, 'getBannerData');
            component.ngOnInit();

            expect(component.isKYCVerified).toEqual(true);
        });

        it('should close the onboarding screen on close emitter', () => {
            const event: any = { output: 'closeOnboardingEmitter', value: '' }
            component.handleOnBoardingEvents(event);
            expect(component.onBoardingOverlaySeen).toEqual(true);
        });
    });

    describe('signPostings', () => {
        it('should not be called when no betpack labels', () => {
            const bpData = {
                id: '2', threshold: 100, current: 20, betpackEndDate: new Date(new Date().setDate(new Date().getDate() + 1)).toISOString(),
                expiryData: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString()
            };
            const betPack = { betpackEndDate: new Date(new Date().setDate(new Date().getDate() + 1)).toISOString() };
            component.betpackLabels = undefined;
            component.signPostings(bpData, betPack);
            expect(betPack['signPostingMsg']).toBe(undefined);
        });

        it('should be called when endingSoonLabel', () => {
            const bpData = {
                id: '2', threshold: 100, current: 20, betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 10700000)).toISOString(),
                expiryData: new Date(new Date().setTime(new Date().getTime() + 20800000)).toISOString()
            };
            const betPack = { betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 10700000)).toISOString() };
            component.betpackLabels = { endingSoonLabel: 'ENDING SOON' };
            component.signPostings(bpData, betPack);
            expect(betPack['signPostingMsg']).toEqual(component.betpackLabels.endingSoonLabel);
        });

        it('should be called when expiry', () => {
            const bpData = {
                id: '2', threshold: 100, current: 20, betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 3500000)).toISOString(),
                expiryData: new Date(new Date().setTime(new Date().getTime() + 3500000)).toISOString()
            };
            const betPack = { betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30700000)).toISOString() };
            component.betpackLabels = { maxOnePurchasedLabel: 'MAX 1' };
            component.signPostings(bpData, betPack);
            expect(betPack['expiresIntimer']).toBeDefined();
        });

        it('should be called when maxOnePurchasedLabel', () => {
            component.userService.username = 'abc';
            const bpData = {
                id: '2', threshold: 100, current: 20, betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30700000)).toISOString(),
                expiryData: new Date(new Date().setTime(new Date().getTime() + 10800000)).toISOString(), maxClaimLimitRemaining: 2
            };
            const betPack = { betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30700000)).toISOString() };
            component.betpackLabels = { maxOnePurchasedLabel: 'MAX <max-claims>', maxOnePurchasedTooltip: 'MAX <max-claims>' };
            component.signPostings(bpData, betPack);
            expect(betPack['signPostingMsg']).toEqual('MAX 2');
        });
        it('should  set signposting as cms max claim value when unlimited flag for betpack is not check', () => {
            component.userService.username = 'abc';
            const bpData = {
                id: '2', threshold: 100, current: 20, betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30700000)).toISOString(),
                expiryData: new Date(new Date().setTime(new Date().getTime() + 10800000)).toISOString(), maxClaimLimitRemaining: undefined
            };
            const betPack = { betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30700000)).toISOString(), unlimitedCheck: false, maxClaims: '2' };
            component.betpackLabels = { maxOnePurchasedLabel: 'MAX <max-claims>', maxOnePurchasedTooltip: 'MAX <max-claims>' };
            component.signPostings(bpData, betPack);
            expect(betPack['signPostingMsg']).toEqual('MAX 2');
        });

        it('should  set signposting as cms LIMITED AVAILABILITY in logged out state if total max claim is not unlimited', () => {
            component.userService.username = null;
            const bpData = {
                id: '2', threshold: 100, current: 20, betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30700000)).toISOString(),
                expiryData: new Date(new Date().setTime(new Date().getTime() + 10800000)).toISOString(), maxClaimLimitRemaining: undefined
            };
            const betPack = { betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30700000)).toISOString(), unlimitedCheck: false, maxClaims: '2' };
            component.betpackLabels = { maxOnePurchasedLabel: 'MAX 2', limitedLabel: 'LIMITED AVAILABILITY' };
            component.signPostings(bpData, betPack);
            expect(betPack['signPostingMsg']).toEqual('LIMITED AVAILABILITY');
        });

        it('should  set signposting as blank(No signposting) in logged out state if total max claim current is 0', () => {
            component.userService.username = null;
            const bpData = {
                id: '2', threshold: 100, current: 0, betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30700000)).toISOString(),
                expiryData: new Date(new Date().setTime(new Date().getTime() + 10800000)).toISOString(), maxClaimLimitRemaining: undefined
            };
            const betPack = { betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30700000)).toISOString(), unlimitedCheck: false, maxClaims: '2' };
            component.betpackLabels = { maxOnePurchasedLabel: 'MAX 2', limitedLabel: 'LIMITED AVAILABILITY' };
            component.signPostings(bpData, betPack);
            expect(betPack['signPostingMsg']).toEqual(' ');
        });

        it('should be called when ENDED', () => {
            const bpData = {
                id: '2', threshold: 100, current: 20, betpackEndDate: new Date(new Date().setTime(new Date().getTime() - 30000)).toISOString(),
                expiryData: new Date(new Date().setTime(new Date().getTime() + 20800000)).toISOString()
            };
            const betPack = { betpackEndDate: new Date(new Date().setTime(new Date().getTime() - 30000)).toISOString() };
            component.betpackLabels = { endedLabel: 'ENDED' };
            component.signPostings(bpData, betPack);
            expect(betPack['signPostingMsg']).toEqual(component.betpackLabels.endedLabel);
        });

        it('should be called when soldOutLabel ', () => {
            const bpData = {
                id: '2', betPackId: 'test', threshold: 100, current: 100, betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30000)).toISOString(),
                expiryData: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString()
            };
            const betPack = { betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30000)).toISOString() };
            component.betpackLabels = { soldOutLabel: 'Sold out', soldOutTooltip: 'Sold out tooltip' };
            component.signPostings(bpData, betPack);
            expect(betPack['signPostingMsg']).toBe('Sold out');
        });

        it('should be called when endedLabel ', () => {
            const bpData = {
                id: '2', betPackId: 'test', threshold: 100, current: 100, betpackEndDate: new Date(new Date().setTime(new Date().getTime() - 30000)).toISOString(),
                expiryData: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString()
            };
            const betPack = { betpackEndDate: new Date(new Date().setTime(new Date().getTime() - 30000)).toISOString() };
            component.betpackLabels = { endedLabel: 'Ended', endedTooltip: 'Ended tooltip' };
            component.signPostings(bpData, betPack);
            expect(betPack['signPostingMsg']).toBe('Ended');
        });

        it('should not be called when  no betpack', () => {
            component.expireIn = true;
            component.betpackLabels = { endedLabel: 'Ended' };
            const betPack = { betpackEndDate: new Date(new Date().setTime(new Date().getTime() - 30000)).toISOString() };
            component.signPostings(null, betPack);
            expect(betPack['disableBuyBtn']).toBe(true);
        });

        it('signPostings when threshold is unlimited', () => {
            const bpData = {
                id: '2', betPackId: 'test', threshold: 'unlimited', current: 100,
                expiryData: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString()
            };
            const betPack = { betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30000)).toISOString() };
            component.betpackLabels = { soldOutLabel: 'Sold out', soldOutTooltip: 'Sold out tooltip' };
            component.checkThresholdValue = jasmine.createSpy('checkThresholdValue').and.returnValue(true);
            component.signPostings(bpData, betPack);
            expect(betPack['disableBuyBtn']).toBe(false);
        });

        it('signPostings when threshold is unlimited', () => {
            const bpData = {
                id: '2',
                betPackId: 'test',
                threshold: 'unlimited',
                current: 100,
                expiryData: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString()
            };

            const betPack = {
                betpackEndDate: new Date(new Date().setTime(new Date().getTime() + 30000)).toISOString()
            };

            let time = 1111111111111111;
            spyOn(timeService, 'parseDateTime').and.returnValue({
                getTime: function (a) {
                    time--;
                    return time;
                }
            })

            component.betpackLabels = { soldOutLabel: 'Sold out', soldOutTooltip: 'Sold out tooltip' };
            component.checkThresholdValue = jasmine.createSpy('checkThresholdValue').and.returnValue(true);
            component.signPostings(bpData, betPack);
            expect(betPack['disableBuyBtn']).toBe(false);
        });
    });

    describe('UserLevelvalidation', () => {
        it('isMaxPurchaseLimitOver is true', () => {
            const betPacks = [{
                betPackId: '123',
                betPackStartDate: new Date(new Date().setDate(new Date().getDate() - 3)).toISOString(),
                signPostingMsg: '',
                signPostingToolTip: '',
                disableBuyBtn: ''
            }]
            spyOn(component, 'updateComingSoonSignPost');
            component.isMaxPurchaseLimitOver = true;
            component.UserLevelvalidation(betPacks);
            expect(component.updateComingSoonSignPost).toHaveBeenCalled();
        });
        it('isMaxPurchaseLimitOver is false', () => {
            spyOn(component, 'userLevelPurchase');
            const betPacks = [{
                betPackId: '123',
                betPackStartDate: new Date(new Date().setDate(new Date().getDate() - 3)).toISOString(),
                signPostingMsg: '',
                signPostingToolTip: '',
                disableBuyBtn: ''
            }]
            component.getLimitsData = 1;
            component.isMaxPurchaseLimitOver = false;
            component.UserLevelvalidation(betPacks);
            expect(component.userLevelPurchase).toHaveBeenCalled();
        });
    });

    describe('userLevelPurchase', () => {
        it('should show isMaxPurchaseLimitOver for betpacks which are purchased and when limits are remaining when getfreebets1', () => {
            const betPacks = [{
                betPackId: '37505'
            }, {
                betPackId: '3'
            }];
            component.accLimitFreeBets = [{
                freebetOfferId: '37505'
            }];
            component.betpackLabels = {
                maxPurchasedLabel: 'max purchased'
            };
            spyOn(component, 'checkForMaxLimits').and.returnValue(true);
            component.init();
            component.userLevelPurchase(betPacks);
            expect(betPacks[1]['disableBuyBtn']).toBeFalsy();
        });
        it('should show isMaxPurchaseLimitOver for betpacks which are purchased and when limits are remaining when no getfreebets', () => {
            betpackCmsService.getFreeBets = null;
            const betPacks = [{
                betPackId: '37505'
            }, {
                betPackId: '3'
            }];
            component.accLimitFreeBets = [{
                freebetOfferId: '37505'
            }];
            component.betpackLabels = {
                maxPurchasedLabel: 'max purchased'
            };
            spyOn(component, 'checkForMaxLimits').and.returnValue(true);
            component.userLevelPurchase(betPacks);
            expect(betPacks[0]['disableBuyBtn']).toBeTruthy();
        });
        it('should show isMaxPurchaseLimitOver for betpacks which are purchased and when limits are remaining when no getfreebets', () => {
            betpackCmsService.getFreeBets = null;
            const betPacks = [{
                betPackId: '37505'
            }, {
                betPackId: '3'
            }];
            component.betpackLabels = {
                maxPurchasedLabel: 'max purchased'
            };
            spyOn(component, 'checkForMaxLimits').and.returnValue(true);
            component.userLevelPurchase(betPacks);
        });
    });
      

    describe('computeInitialNonLoggedInSignPostings', () => {
        it('should not call signPostings in case of invalid response from initialWSGetLimits', () => {
            spyOn(component, 'signPostings');
            component.betpackDetails = [{
                betPackPurchaseAmount: '2', betPackFreeBetsAmount: '2',
                betPackMoreInfoText: 'text',
                betPackTokenList: [{ tokenTitle: "accumulator" }]
            }];
            component.computeInitialNonLoggedInSignPostings([null]);
            expect(component.signPostings).not.toHaveBeenCalled();
        });

        it('should not call signPostings in case of response from initialWSGetLimits does not have freebetOfferLimits', () => {
            component.init();
            spyOn(component, 'signPostings');
            component.betpackDetails = [{
                betPackPurchaseAmount: '2', betPackFreeBetsAmount: '2',
                betPackMoreInfoText: 'text',
                betPackId: '37505',
                betPackTokenList: [{ tokenTitle: "accumulator" }]
            }];
            component.computeInitialNonLoggedInSignPostings([{ freebetOfferId: '37505' }]);
            expect(component.signPostings).not.toHaveBeenCalled();
        });

        it('should not call signPostings in case of betPackId is not matching with freebetOfferId', () => {
            component.init();
            spyOn(component, 'signPostings');
            spyOn(component, 'getMaxClaimData');
            component.betpackDetails = [{
                betPackPurchaseAmount: '2', betPackFreeBetsAmount: '2',
                betPackMoreInfoText: 'text',
                betPackId: '37506',
                betPackTokenList: [{ tokenTitle: "accumulator" }]
            }];
            component.computeInitialNonLoggedInSignPostings([{ freebetOfferId: '37505' }]);
            expect(component.signPostings).not.toHaveBeenCalled();
        });

        it('should not call signPostings in case of betPackId is not matching with freebetOfferId', () => {
            spyOn(component, 'signPostings');
            spyOn(component, 'getMaxClaimData');
            component.betpackDetails = [{
                betPackPurchaseAmount: '2', betPackFreeBetsAmount: '2',
                betPackMoreInfoText: 'text',
                betPackId: '37505',
                betPackTokenList: [{ tokenTitle: "accumulator" }]
            }];
            component.getMaxClaimData(null);
            expect(component.signPostings).not.toHaveBeenCalled();
        });

        it('should not call signPostings in case of response from initialWSGetLimits does not have limitEntry', () => {
            spyOn(component, 'signPostings');
            component.betpackDetails = [{
                betPackPurchaseAmount: '2', betPackFreeBetsAmount: '2',
                betPackMoreInfoText: 'text',
                betPackId: '37505',
                betPackTokenList: [{ tokenTitle: "accumulator" }]
            }];
            component.computeInitialNonLoggedInSignPostings([{ freebetOfferId: '37505', freebetOfferLimits: null }, { freebetOfferId: '37506', freebetOfferLimits: null }]);
            expect(component.signPostings).not.toHaveBeenCalled();
        });

        it('should call signPostings in case of valid response from initialWSGetLimits', () => {
            spyOn(component, 'signPostings');
            component.betpackDetails = [{
                betPackPurchaseAmount: '2', betPackFreeBetsAmount: '2',
                betPackMoreInfoText: 'text',
                betPackId: '37505',
                betPackTokenList: [{ tokenTitle: "accumulator" }]
            }];
            component.betpackLabels = { maxPurchasedLabel: 'max purchased' };
            component.computeInitialNonLoggedInSignPostings([{
                freebetOfferId: '37505', freebetOfferLimits: {
                    limitEntry: [{ limitId: 37441, limitRemaining: 90, limitDefinition: { limitComponent: { limitParam: [{ name: 'current', value: 10 }, { name: 'threshold', value: 100 }] } } }]
                }
            }]);
            expect(component.signPostings).toHaveBeenCalled();
            expect(component.current).toBe(10);
            expect(component.threshold).toBe(100);
        });

        it('should not call signPostings in case of valid response from initialWSGetLimits and betpack is purchased', () => {
            spyOn(component, 'signPostings');
            component.betpackLabels = { maxPurchasedLabel: 'max purchased' };
            component.betpackDetails = [{
                betPackPurchaseAmount: '2', betPackFreeBetsAmount: '2',
                betPackMoreInfoText: 'text',
                betPackId: '37505',
                betPackTokenList: [{ tokenTitle: "accumulator" }],
                signPostingMsg: component.betpackLabels.maxPurchasedLabel
            }];
            component.computeInitialNonLoggedInSignPostings([{ freebetOfferId: '37505', freebetOfferLimits: { limitEntry: [{ limitId: 37441, limitRemaining: 90, limitDefinition: { limitComponent: { limitParam: [{ name: 'current', value: 10 }, { name: 'threshold', value: 100 }] } } }] } }]);
            expect(component.signPostings).not.toHaveBeenCalled();
        });

        it('should call signPostings when accLimitFrrebets ', () => {
            spyOn(component, 'signPostings');
            spyOn(component, 'getMaxClaimData');
            component.accLimitFreeBets = [{
                freebetOfferId: '37505'
            }]
            component.userService = {
                status: true,
            }
            component.betpackLabels = { maxPurchasedLabel: 'max purchased' };
            component.betpackDetails = [{
                betPackPurchaseAmount: '2', betPackFreeBetsAmount: '2',
                betPackMoreInfoText: 'text',
                betPackId: '37505',
                betPackTokenList: [{ tokenTitle: "accumulator" }],
                signPostingMsg: component.betpackLabels.maxPurchasedLabel
            }];
            component.computeInitialNonLoggedInSignPostings([{ freebetOfferId: '37505', freebetOfferLimits: { limitEntry: [{ limitId: 37441, limitRemaining: 90, limitDefinition: { limitComponent: { limitParam: [{ name: 'current', value: 10 }, { name: 'threshold', value: 100 }] } } }] } }]);
            expect(component.signPostings).not.toHaveBeenCalled();
        });
        it('should call signPostings no acclimits free bets', () => {
            spyOn(component, 'signPostings');
            spyOn(component, 'getMaxClaimData');
            component.accLimitFreeBets = [{
                freebetOfferId: '3750'
            }]
            component.userService = {
                status: true,
            }
            component.betpackLabels = { maxPurchasedLabel: 'max purchased' };
            component.betpackDetails = [{
                betPackPurchaseAmount: '2', betPackFreeBetsAmount: '2',
                betPackMoreInfoText: 'text',
                betPackId: '37505',
                betPackTokenList: [{ tokenTitle: "accumulator" }],
                signPostingMsg: component.betpackLabels.maxPurchasedLabel,
                offerGroupId: '123',
                showSignPost: true,
            }];
            const signPostingData = [{
                freebetOfferId : 37505
            }]
            component.computeInitialNonLoggedInSignPostings([{ freebetOfferId: '37505', freebetOfferLimits: { limitEntry: [{ limitId: 37441, limitRemaining: 90, limitDefinition: { limitComponent: { limitParam: [{ name: 'current', value: 10 }, { name: 'threshold', value: 100 }] } } }] } }]);
            expect(component.signPostings).not.toHaveBeenCalled();
        });
    });

    describe('subscribeForBetpacks', () => {
        it('should subscribe for updates and store new connection', () => {
            const channels = ['SUBSCRIBE_BPMP'];
            const updateHandler = jasmine.createSpy('updateHandler');
            component.subscribeForBetpacks(channels, updateHandler);
            expect(liveServConnectionService.connect).toHaveBeenCalled();
            expect(liveServConnectionService.subscribeBP).toHaveBeenCalledWith(channels, jasmine.any(Function));
        });

        it('should call updateHandler on connection subscribe', () => {
            const channels = ['SUBSCRIBE_BPMP'];
            const updateHandler = jasmine.createSpy('updateHandler');
            let storedHandler = (args) => { };
            liveServConnectionService.subscribeBP.and.callFake((channel, handlerFn) => {
                storedHandler = handlerFn;
            });
            component.subscribeForBetpacks(channels, updateHandler);

            storedHandler({ type: 'UPDATE' });
            expect(updateHandler).toHaveBeenCalledWith({ type: 'UPDATE' });

            const updateMessage = { type: 'MESSAGE' };
            storedHandler(updateMessage);
            expect(updateHandler).toHaveBeenCalledWith(updateMessage);
        });
    });

    describe('ngOnDestroy', () => {
        it('should unsubscribe connections', () => {
            component.betpackDetailsMaster = [{ betPackId: 1 }, { betPackId: 2 }];
            component.ngOnDestroy();
            expect(liveServConnectionService.unsubscribeBP).toHaveBeenCalled();
        });
    });

    describe('updateHandler', () => {
        it('updateHandler', () => {
            component.betpackDetailsMaster = [{ betPackId: 1 }, { betPackId: 2 }];
            component.updateHandler();
            expect(pubSubService.publish).toHaveBeenCalled();
        });
    });

    describe('openPopup', () => {
        beforeEach(() => {
            component.disableBetPack = false;
            serviceClosureService.userServiceClosureOrPlayBreakCheck = jasmine.createSpy('userServiceClosureOrPlayBreakCheck').and.returnValue(false);
            serviceClosureService.userServiceClosureOrPlayBreak = false;
            component.gamblingControlsCheck = false;
        });

        it('should open popup in case of data available in session storage', () => {
            sessionStorage.get = jasmine.createSpy('get').and.returnValue({ bp: {} });
            component.openPopup();
            expect(dialogService.openDialog).toHaveBeenCalled();
        });

        it('should not open popup in case of data not available in session storage', () => {
            sessionStorage.get = jasmine.createSpy('get').and.returnValue(undefined);
            component.openPopup();
            expect(dialogService.openDialog).not.toHaveBeenCalled();
        });

        it('should open popup in desktop after login from betpack buy button', () => {
            sessionStorage.get = jasmine.createSpy('get').and.returnValue({ bp: { betPackId: 1 }, signPostingMsg: 'max 1', signPostingToolTip: 'max 1 tooltip' });
            component.openPopup(true);
            expect(dialogService.openDialog).toHaveBeenCalled();
            const args = dialogService.openDialog.calls.argsFor(0);
            expect(args[3]['data']).toBe(null);
        });

        it('should not open popup in case of play break', () => {
            serviceClosureService.userServiceClosureOrPlayBreakCheck = jasmine.createSpy('userServiceClosureOrPlayBreakCheck').and.returnValue(true);
            serviceClosureService.userServiceClosureOrPlayBreak = true;
            component.gamblingControlsCheck = true;
            component.openPopup();
            expect(dialogService.openDialog).not.toHaveBeenCalled();
        });

        it('should not open popup in case of stake factor less than 0.25', () => {
            component.disableBetPack = true;
            component.openPopup();
            expect(dialogService.openDialog).not.toHaveBeenCalled();
        });
    });
    describe('gmtService', () => {
        it('gmtService', () => {
            component.sendGtmData('test');
            expect(gtmService.push).toHaveBeenCalled();
        });
    });

    describe('getBannerData', () => {
        it('getBannerData', () => {
            betpackCmsService.getBetPackBanners = jasmine.createSpy('getBetPackBanners').and.returnValue(of({ bannerTextDescInMarketPlacePage: 'test' }))
            component.getBannerData();
            expect(component.bannerData).toEqual({ bannerTextDescInMarketPlacePage: 'test' })
        });
        it('getBannerData', () => {
            betpackCmsService.getBetPackBanners = jasmine.createSpy('getBetPackBanners').and.returnValue(of({}))
            component.getBannerData();
            expect(component.bannerData).toEqual({});
        });
    });

    describe('expiringTokenCount', () => {
        it('expiringTokenCount', () => {
            spyOn(component, 'calculateExpirinTokens');
            component.bannerData = {
                bannerTextDescInMarketPlacePage: 'test'
            }
            component.expiringTokenCount();
            expect(component.calculateExpirinTokens).toHaveBeenCalled();
        });
    });
    describe('groupLevelCheck', () => {
        it('groupLevelCheck when group limit is 0', () => {
            spyOn(component, 'updateGroupedBps');
            const freeBetOffer = {
                freebetOfferLimits: {
                    limitEntry: [{
                        limitSort: 'OFFER_GROUP_MAX_CLAIMS_LIMIT',
                        limitRemaining: 0
                    }]
                }
            } as any;
            const bp = 'test';
            component.groupLevelCheck(freeBetOffer, bp);
            expect(component.updateGroupedBps).toHaveBeenCalled();
        });
        it('groupLevelCheck when group limit is greater than 0', () => {
            spyOn(component, 'updateGroupedBps');
            const freeBetOffer = {
                freebetOfferLimits: {
                    limitEntry: [{
                        limitSort: 'OFFER_GROUP_MAX_CLAIMS_LIMIT',
                        limitRemaining: 2
                    }]
                }
            } as any;
            const bp = 'test';
            component.groupLevelCheck(freeBetOffer, bp);
            expect(component.updateGroupedBps).toHaveBeenCalled();
        });
        it('groupLevelCheck when group limit is greater than 0', () => {
            spyOn(component, 'updateGroupedBps').and.returnValue(true);
            const freeBetOffer = {
                freebetOfferLimits: {
                    limitEntry: [{
                        limitSort: 'OFFER_GROUP_MAX_CLAIMS_LIMIT',
                        limitRemaining: 2
                    }]
                }
            } as any;
            const bp = 'test';
            component.groupLevelCheck(freeBetOffer, bp);
            expect(component.updateGroupedBps).toHaveBeenCalled();
        });
        it('groupLevelCheck when freebetofferlimits are not available', () => {
            spyOn(component, 'updateGroupedBps');
            const freeBetOffer = {} as any;
            const bp = 'test';
            component.groupLevelCheck(freeBetOffer, bp);
            expect(component.updateGroupedBps).toHaveBeenCalled();
          });
    });

    describe('checkForMaxLimits', () => {
        it('checkForMaxLimits when group limit is 0', () => {
            spyOn(component, 'groupLevelCheck');
            const freeBetOffer = {
                offerGroup: {
                    offerGroupId: '1234'
                },
                freebetOfferLimits: {
                    limitEntry: [{
                        limitSort: 'OFFER_MAX_CLAIMS_LIMIT',
                        limitRemaining: 0
                    }]
                }
            } as any;
            const bp = 'test';
            component.checkForMaxLimits(freeBetOffer, bp);
            expect(component.groupLevelCheck).toHaveBeenCalled();
        });
        it('checkForMaxLimits when group limit is 0 without limits', () => {
            spyOn(component, 'groupLevelCheck');
            const freeBetOffer = {
                offerGroup: {
                    offerGroupId: '1234'
                }
            } as any;
            const bp = 'test';
            component.checkForMaxLimits(freeBetOffer, bp);
            expect(component.groupLevelCheck).toHaveBeenCalled();
        });
        it('checkForMaxLimits when group limit is  without group and limits', () => {
            spyOn(component, 'groupLevelCheck');
            const freeBetOffer = {} as any;
            const bp = 'test';
            component.checkForMaxLimits(freeBetOffer, bp);
            expect(component.groupLevelCheck).not.toHaveBeenCalled();
        });
        it('checkForMaxLimits when group limit is greater than 0', () => {
            spyOn(component, 'updateGroupedBps');
            const freeBetOffer = {
                freebetOfferLimits: {
                    limitEntry: [{
                        limitSort: 'OFFER_MAX_CLAIMS_LIMIT',
                        limitRemaining: 2
                    }]
                }
            } as any;
            const bp = 'test';
            component.checkForMaxLimits(freeBetOffer, bp);
            expect(component.updateGroupedBps).not.toHaveBeenCalled();
        });
    });

    describe('updateGroupedBps', () => {
        it('updateGroupedBps limit true when id match with non - maxpurchase', () => {
            spyOn(component, 'updateComingSoonSignPost');
            spyOn(component, 'OfferLimitUpdate');
            const limit = true;
            const freeBetOffer = {
                offerGroup: {
                    offerGroupId: '1234'
                },
                freebetOfferLimits: {
                    limitEntry: [{
                        limitSort: 'OFFER_MAX_CLAIMS_LIMIT',
                        limitRemaining: 0
                    }]
                }
            } as any;
            const bp = {
                offerGroupId: '123'
            }
            component.betpackLabels = {
                maxPurchasedLabel: 'test'
            }
            component.betpackDetails = [{
                offerGroupId: '123',
                signPostingMsg: 'test1'
            }]
            component.updateGroupedBps(freeBetOffer, bp, limit);
            expect(component.updateComingSoonSignPost).toHaveBeenCalled();
        });
        it('updateGroupedBps limit true when  id match with  maxpurchase', () => {
            spyOn(component, 'updateComingSoonSignPost');
            spyOn(component, 'OfferLimitUpdate');
            const limit = true;
            const freeBetOffer = {
                offerGroup: {
                    offerGroupId: '123'
                },
                freebetOfferLimits: {
                    limitEntry: [{
                        limitSort: 'OFFER_MAX_CLAIMS_LIMIT',
                        limitRemaining: 0
                    }]
                }
            } as any;
            const bp = {
                offerGroupId: '123'
            }
            component.betpackLabels = {
                maxPurchasedLabel: 'test'
            }
            component.betpackDetails = [{
                offerGroupId: '123',
                signPostingMsg: 'test'
            }]
            component.updateGroupedBps(freeBetOffer, bp, limit);
            expect(component.updateComingSoonSignPost).not.toHaveBeenCalled();
        });
        it('updateGroupedBps limit true when id match with non - maxpurchase', () => {
            spyOn(component, 'updateComingSoonSignPost');
            spyOn(component, 'OfferLimitUpdate');
            const limit = true;
            const freeBetOffer = {
                offerGroup: {
                    offerGroupId: '1234'
                },
                freebetOfferLimits: {
                    limitEntry: [{
                        limitSort: 'OFFER_MAX_CLAIMS_LIMIT',
                        limitRemaining: 0
                    }]
                }
            } as any;
            const bp = {
                offerGroupId: '123'
            }
            component.betpackLabels = {
                maxPurchasedLabel: 'test'
            }
            component.checkForMaxLimits(freeBetOffer, bp, limit);
            expect(component.updateComingSoonSignPost).not.toHaveBeenCalled();
        });
        it('updateGroupedBps limit true with no offergroup ID', () => {
            spyOn(component, 'updateComingSoonSignPost');
            spyOn(component, 'OfferLimitUpdate');
            const limit = true;
            const freeBetOffer = {
                offerGroup: {
                    offerGroupId: '1234'
                },
                freebetOfferLimits: {
                    limitEntry: [{
                        limitSort: 'OFFER_MAX_CLAIMS_LIMIT',
                        limitRemaining: 0
                    }]
                }
            } as any;
            const bp = {
                offerGroupId: ''
            }
            component.betpackLabels = {
                maxPurchasedLabel: 'test'
            }
            component.checkForMaxLimits(freeBetOffer, bp, limit);
            expect(component.updateComingSoonSignPost).not.toHaveBeenCalled();
        });
        it('updateGroupedBps limit false', () => {
            spyOn(component, 'updateComingSoonSignPost');
            spyOn(component, 'OfferLimitUpdate');
            const limit = true;
            const freeBetOffer = {
                offerGroup: {
                    offerGroupId: '1234'
                },
                freebetOfferLimits: {
                    limitEntry: [{
                        limitSort: 'OFFER_MAX_CLAIMS_LIMIT',
                        limitRemaining: 0
                    }]
                }
            } as any;
            const bp = {
                offerGroupId: '123'
            }
            component.betpackLabels = {
                maxPurchasedLabel: 'test'
            }
            component.checkForMaxLimits(freeBetOffer, bp, limit);
            expect(component.OfferLimitUpdate).toHaveBeenCalled();
        });
    });
    describe('updateComingSoonSignPost', () => {
        it('updateComingSoonSignPost dates match', () => {
            component.initialSignPostData = [{
                freebetOfferId: '123',
                startTime: new Date(new Date().setDate(new Date().getDate() - 2)).toISOString()
            }]
            const betpack = {
                betPackId: '123',
                betPackStartDate: new Date(new Date().setDate(new Date().getDate() - 1)).toISOString(),
                signPostingMsg: '',
                signPostingToolTip: '',
                disableBuyBtn: ''
            }
            component.betpackLabels = {
                comingSoon: 'comingSoon',
                maxPurchasedLabel: 'maxPurchasedLabel'
            }
            component.updateComingSoonSignPost(betpack);
            expect(betpack.disableBuyBtn).toBeTruthy()
        });
        it('updateComingSoonSignPost today date > than bpp start date', () => {
            component.initialSignPostData = [{
                freebetOfferId: '123',
                startTime: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString()
            }]
            const betpack = {
                betPackId: '123',
                betPackStartDate: new Date(new Date().setDate(new Date().getDate() - 1)).toISOString(),
                signPostingMsg: '',
                signPostingToolTip: '',
                disableBuyBtn: ''
            }
            component.betpackLabels = {
                comingSoon: 'comingSoon',
                maxPurchasedLabel: 'maxPurchasedLabel'
            }
            component.updateComingSoonSignPost(betpack);
            expect(betpack.disableBuyBtn).toBeFalsy()
        });
        it('updateComingSoonSignPost cmsDate date < than bpp start date', () => {
            component.initialSignPostData = [{
                freebetOfferId: '123',
                startTime: new Date(new Date().setDate(new Date().getDate() - 2)).toISOString()
            }]
            const betpack = {
                betPackId: '123',
                betPackStartDate: new Date(new Date().setDate(new Date().getDate() - 3)).toISOString(),
                signPostingMsg: '',
                signPostingToolTip: '',
                disableBuyBtn: ''
            }
            component.betpackLabels = {
                comingSoon: 'comingSoon',
                maxPurchasedLabel: 'maxPurchasedLabel'
            }
            component.updateComingSoonSignPost(betpack);
            expect(betpack.disableBuyBtn).toBeTruthy()
        });
        it('updateComingSoonSignPost when no id match', () => {
            component.initialSignPostData = [{
                freebetOfferId: '12',
                startTime: new Date(new Date().setDate(new Date().getDate() - 2)).toISOString()
            }]
            const betpack = {
                betPackId: '123',
                betPackStartDate: new Date(new Date().setDate(new Date().getDate() - 3)).toISOString(),
                signPostingMsg: '',
                signPostingToolTip: '',
            } as any;
            component.betpackLabels = {
                comingSoon: 'comingSoon',
                maxPurchasedLabel: 'maxPurchasedLabel'
            }
            component.updateComingSoonSignPost(betpack);
            expect(betpack.disableBuyBtn).toBeUndefined()
        });
    });

    describe('OfferLimitUpdate', () => {
        it('OfferLimitUpdate with limitUpdate', () => {
            spyOn(component, 'limitEntryUpdatewithlimits');
            spyOn(component, 'checkMaxPurchase');
            spyOn(component, 'updateAllGroupedBPswithLimits');
            const freeBetOffer = {
                freebetOfferId: '123',
                offerGroup: {
                    offerGroupId: '12'
                },
                freebetOfferLimits: {
                    limitEntry: [{}]
                }
            }
            const betpack = {
                betPackId: '123',
                betPackStartDate: new Date(new Date().setDate(new Date().getDate() - 1)).toISOString(),
                signPostingMsg: '',
                signPostingToolTip: '',
                disableBuyBtn: ''
            }
            component.initialSignPostData = [{
                freebetOfferId: '123',
                startTime: new Date(new Date().setDate(new Date().getDate() - 2)).toISOString()
            }]
            component.betpackDetails = [{
                offerGroupId: '123',
                signPostingMsg: 'test'
            }]
            component.betpackLabels = {
                comingSoon: 'comingSoon',
                maxPurchasedLabel: 'maxPurchasedLabel'
            }
            component.OfferLimitUpdate(freeBetOffer, betpack);
            expect(component.updateAllGroupedBPswithLimits).toHaveBeenCalled();
        });
        it('OfferLimitUpdate when no limits', () => {
            spyOn(component, 'limitEntryUpdatewithlimits');
            spyOn(component, 'checkMaxPurchase');
            spyOn(component, 'updateAllGroupedBPswithLimits');
            const freeBetOffer = {
                freebetOfferId: '123',
                offerGroup: {
                    offerGroupId: '12'
                }
            }
            const betpack = {
                betPackId: '123',
                betPackStartDate: new Date(new Date().setDate(new Date().getDate() - 1)).toISOString(),
                signPostingMsg: '',
                signPostingToolTip: '',
                disableBuyBtn: ''
            }
            component.initialSignPostData = [{
                freebetOfferId: '123',
                startTime: new Date(new Date().setDate(new Date().getDate() - 2)).toISOString()
            }]
            component.betpackDetails = [{
                offerGroupId: '123',
                signPostingMsg: 'test'
            }]
            component.betpackLabels = {
                comingSoon: 'comingSoon',
                maxPurchasedLabel: 'maxPurchasedLabel'
            }
            component.OfferLimitUpdate(freeBetOffer, betpack);
            expect(component.updateAllGroupedBPswithLimits).toHaveBeenCalled();
        });
        it('OfferLimitUpdate when freeberOffers', () => {
            spyOn(component, 'limitEntryUpdatewithlimits');
            spyOn(component, 'checkMaxPurchase');
            spyOn(component, 'updateAllGroupedBPswithLimits');
            const betpack = {
                betPackId: '123',
                betPackStartDate: new Date(new Date().setDate(new Date().getDate() - 1)).toISOString(),
                signPostingMsg: '',
                signPostingToolTip: '',
                disableBuyBtn: ''
            }
            component.initialSignPostData = [{
                freebetOfferId: '123',
                startTime: new Date(new Date().setDate(new Date().getDate() - 2)).toISOString()
            }]
            component.betpackDetails = [{
                offerGroupId: '123',
                signPostingMsg: 'test'
            }]
            component.betpackLabels = {
                comingSoon: 'comingSoon',
                maxPurchasedLabel: 'maxPurchasedLabel'
            }
            component.OfferLimitUpdate(undefined, betpack);
            expect(component.updateAllGroupedBPswithLimits).toHaveBeenCalled();
        });
        it('OfferLimitUpdate when freeberOffers', () => {
            spyOn(component, 'limitEntryUpdatewithlimits');
            spyOn(component, 'checkMaxPurchase');
            spyOn(component, 'updateAllGroupedBPswithLimits');
            const freeBetOffer = {
                freebetOfferId: '123',
                freebetOfferLimits: {
                    limitEntry: [{}]
                }
            }
            const betpack = {
                betPackId: '123',
                betPackStartDate: new Date(new Date().setDate(new Date().getDate() - 1)).toISOString(),
                signPostingMsg: '',
                signPostingToolTip: '',
                disableBuyBtn: ''
            }
            component.initialSignPostData = [{
                freebetOfferId: '123',
                startTime: new Date(new Date().setDate(new Date().getDate() - 2)).toISOString()
            }]
            component.betpackDetails = [{
                offerGroupId: '123',
                signPostingMsg: 'test'
            }]
            component.betpackLabels = {
                comingSoon: 'comingSoon',
                maxPurchasedLabel: 'maxPurchasedLabel'
            }
            component.OfferLimitUpdate(freeBetOffer, betpack);
            expect(component.updateAllGroupedBPswithLimits).toHaveBeenCalled();
        });
    });
    describe('limitEntryUpdatewithlimits', () => {
        it('limitEntryUpdatewithlimits index ', () => {
            spyOn(component, 'CheckGropuLimitAndUpdateEventService').and.returnValue({
                limitSort: '1'
            });
            component.limitEntryUpdatewithlimits({}, {
                freebetOfferLimits: {
                    limitEntry: [{
                        limitSort: '1',
                        limitRemaining: 1
                    }, {
                        limitSort: '2',
                        limitRemaining: 2
                    }]
                }
            }, {});
            expect(component.disableBuyBtn).toBeFalsy();
        });
          
          
        it('limitEntryUpdatewithlimits', () => {
            spyOn(component, 'CheckGropuLimitAndUpdateEventService').and.returnValue({ limitSort: '2' });
            component.limitEntryUpdatewithlimits({}, { freebetOfferLimits: { limitEntry: [{ limitSort: '1' }] } }, {});
            expect(component.disableBuyBtn).toBeFalsy();
        });
        it('limitEntryUpdatewithlimits without limit sort ', () => {
            spyOn(component, 'CheckGropuLimitAndUpdateEventService').and.returnValue(null);
            component.limitEntryUpdatewithlimits({}, {
              freebetOfferLimits: {
                limitEntry: [{
                  limitSort: '1',
                  limitRemaining: 1
                }, {
                  limitSort: '2',
                  limitRemaining: 2
                }]
              }
            }, {});
            expect(component.disableBuyBtn).toBeFalsy();
          });
          
    })
    describe('cmsBetpackWithGroupIds', () => {
        it('cmsBetpackWithGroupIds', () => {
            component.initialSignPostData = [{
                freebetOfferId: '123',
                offerGroup: {
                    offerGroupId: '12'
                },
                startTime: new Date(new Date().setDate(new Date().getDate() - 2)).toISOString()
            }]
            component.betpackDetails = [{
                betPackId : '123',
                offerGroupId: '12',
                signPostingMsg: 'test'
            }]
            component.betpackLabels = {
                comingSoon: 'comingSoon',
                maxPurchasedLabel: 'maxPurchasedLabel'
            }
            component.cmsBetpackWithGroupIds();
        });
        it('cmsBetpackWithGroupIds', () => {
            component.initialSignPostData = [{
                freebetOfferId: '123',
                startTime: new Date(new Date().setDate(new Date().getDate() - 2)).toISOString()
            }]
            component.betpackDetails = [{
                betPackId: '123',
                offerGroupId: '12',
                signPostingMsg: 'test'
            }]
            component.betpackLabels = {
                comingSoon: 'comingSoon',
                maxPurchasedLabel: 'maxPurchasedLabel'
            }
            component.cmsBetpackWithGroupIds();
        });
        it('cmsBetpackWithGroupIds', () => {
            component.initialSignPostData = [{
                freebetOfferId: '123',
                startTime: new Date(new Date().setDate(new Date().getDate() - 2)).toISOString()
            }]
            component.betpackDetails = [{
                offerGroupId: '123',
                signPostingMsg: 'test'
            }]
            component.betpackLabels = {
                comingSoon: 'comingSoon',
                maxPurchasedLabel: 'maxPurchasedLabel'
            }
            component.cmsBetpackWithGroupIds();
        });
    });
    describe('checkMaxPurchase', () => {
        it('checkMaxPurchase', () => {
            const index = 0
            const accLimitFreeBet = {
                freebetOfferLimits: {
                    limitEntry: [
                        { limitRemaining: 0 }
                    ]
                }
            }
            const betpack = {
                betPackId: '123',
                betPackStartDate: new Date(new Date().setDate(new Date().getDate() - 1)).toISOString(),
                signPostingMsg: '',
                signPostingToolTip: '',
                disableBuyBtn: ''
            }
            component.betpackDetails = [{
                offerGroupId: '123',
                signPostingMsg: 'test'
            }]
            component.betpackLabels = {
                comingSoon: 'comingSoon',
                maxPurchasedLabel: 'maxPurchasedLabel'
            }
            component.checkMaxPurchase(accLimitFreeBet, index, betpack);
            expect(betpack.disableBuyBtn).toBeTruthy();
        });
    });
    describe('CheckGropuLimitAndUpdateEventService', () => {
        it('freebetOfferId and offerid are equal', () => {
            spyOn(component, 'updateLimitDataWithCmsMaxClaims');
            const retVal = component.CheckGropuLimitAndUpdateEventService({
                OfferId: '8', limitDetails: [{ limitSort: 'OFFER_GROUP_MAX_CLAIMS_LIMIT', limitRemaining: '1' },
                { limitSort: 'OFFER_MAX_CLAIMS_LIMIT', limitRemaining: '1' }]
            },
                { freebetOfferLimits: { limitEntry: [{ limitSort: '1' }] }, freebetOfferId: '8' },
                { maxClaims: '1' });
            expect(retVal.limitSort).toBe('OFFER_GROUP_MAX_CLAIMS_LIMIT')
        });
        it('freebetOfferId and offerid are not equal', () => {
            spyOn(component, 'updateLimitDataWithCmsMaxClaims');
            const retVal = component.CheckGropuLimitAndUpdateEventService({ OfferId: '8', limitDetails: [{ limitSort: 'OFFER_GROUP_MAX_CLAIMS_LIMIT', limitRemaining: '1' }, { limitSort: 'OFFER_MAX_CLAIMS_LIMIT', limitRemaining: '1' }] }, {
                freebetOfferLimits:
                    { limitEntry: [{ limitSort: '1' }] }, freebetOfferId: '18'
            },
                { maxClaims: '1' });
            expect(retVal.limitSort).toBe('OFFER_GROUP_MAX_CLAIMS_LIMIT')
        });
        it('bplimit > group limit', () => {
            spyOn(component, 'updateLimitDataWithCmsMaxClaims').and.returnValue('10'); const retVal = component.CheckGropuLimitAndUpdateEventService({
                OfferId: '8', limitDetails: [{ limitSort: 'OFFER_GROUP_MAX_CLAIMS_LIMIT', limitRemaining: '2' },
                { limitSort: 'OFFER_MAX_CLAIMS_LIMIT', limitRemaining: '1' }]
            },
                { freebetOfferLimits: { limitEntry: [{ limitSort: '1' }] }, freebetOfferId: '18' },
                { maxClaims: '1' });
            expect(retVal).toBe('10')
        });
        it('bplimit < group limit', () => {
            spyOn(component, 'updateLimitDataWithCmsMaxClaims').and.returnValue('10');
            const retVal = component.CheckGropuLimitAndUpdateEventService({
                OfferId: '8', limitDetails:
                    [{ limitSort: 'OFFER_GROUP_MAX_CLAIMS_LIMIT', limitRemaining: '2' },
                    { limitSort: 'OFFER_MAX_CLAIMS_LIMIT', limitRemaining: '1' }]
            },
                { freebetOfferLimits: { limitEntry: [{ limitSort: '1' }] }, freebetOfferId: '8' },
                { maxClaims: '1' });
            expect(retVal.limitSort).toBe('OFFER_MAX_CLAIMS_LIMIT')
        });
        it('bplimit undefined', () => {
            spyOn(component, 'updateLimitDataWithCmsMaxClaims').and.returnValue('10');
            const retVal = component.CheckGropuLimitAndUpdateEventService({
                OfferId: '8', limitDetails: [{ limitSort: 'OFFER_GROUP_MAX_CLAIMS_LIMIT', limitRemaining: '2' },
                { limitSort: 'OFFER_MAX_CLAIMS_LIMIT', limitRemaining: '1' }]
            },
                { freebetOfferLimits: { limitEntry: [{ limitSort: '1' }] }, freebetOfferId: '8' },
                undefined);
            expect(retVal).toBeUndefined();
        });
        it('limit update undefined', () => {
            spyOn(component, 'updateLimitDataWithCmsMaxClaims').and.returnValue('10');
            const retVal = component.CheckGropuLimitAndUpdateEventService({},
                { freebetOfferLimits: { limitEntry: [{ limitSort: '1' }] }, freebetOfferId: '8' }, { maxClaims: '1' });
            expect(retVal).toBe('10');
        });
        it('limit update undefined', () => {
            spyOn(component, 'updateLimitDataWithCmsMaxClaims').and.returnValue('10');
            const retVal = component.CheckGropuLimitAndUpdateEventService({
              OfferId: '8',
              limitDetails: [{
                limitSort: 'OFFER_GROUP_MAX_CLAIMS_LIMIT1',
                limitRemaining: '1'
              }, {
                limitSort: 'OFFER_MAX_CLAIMS_LIMIT1',
                limitRemaining: '1'
              }]
            }, {
              freebetOfferLimits: {
                limitEntry: [{
                  limitSort: '1'
                }]
              },
              freebetOfferId: '8'
            }, {
              maxClaims: '1'
            });
            expect(retVal).toBeUndefined();
          });
          
    })
    describe('closeBaner', () => {
        it('closeBaner', () => {
            const container = {
                remove: jasmine.createSpy('remove')
            }
            component.closeBaner(container);
            expect(storage.set).toHaveBeenCalledWith('betPackMarketBanner', false);
        });
    });
    describe('getheightFromChild', () => {
        it('getheightFromChild', () => {
            const element = {
                offsetHeight: 4
            }
            const retVal = component.getheightFromChild(element,0);
            expect(retVal).toEqual(element.offsetHeight + 'px');
        });
    });

    describe('getSvgWidth', () => {
        it('getSvgWidth', () => {
            const element = {
                offsetWidth: 4
            }
            const retVal = component.getSvgWidth(element);
            expect(retVal).toEqual(element.offsetWidth + 'px');
        });
    });

    describe('calculateExpirinTokens ', () => {
        it('calculateExpirinTokens with tokens', () => {
            component.freeBetToken = ACCOUNT_FREE_BETS.response.model.freebetToken;
            expect(component.calculateExpirinTokens()).toBeDefined();
        });

        it('calculateExpirinTokens with tokens without freebets', () => {
            const date = new Date();
            date.setHours(date.getHours() + 4);
            component.freeBetToken = [{
                freebetTokenExpiryDate: date,
                freebetOfferCategories: {
                    freebetOfferCategory: 'Bet Pack'
                }
            }];
            expect(component.calculateExpirinTokens()).toEqual('1');
        });
        it('calculateExpirinTokens with tokens without freebets1', () => {
            const date = new Date();
            date.setHours(date.getHours() + 4);
            component.freeBetToken = [{
                freebetTokenExpiryDate: date,
            }];
            expect(component.calculateExpirinTokens()).toEqual('0');
        });
        it('calculateExpirinTokens with tokens', () => {
            component.freeBetToken = null;
            expect(component.calculateExpirinTokens()).toBeUndefined();
        });
        it('calculateExpirinTokens with tokens without freebets1', () => {
            const date = new Date();      
            date.setHours(date.getHours() + 4);      
            component.freeBetToken = [{      
              freebetTokenExpiryDate: date,      
            }];      
            expect(component.calculateExpirinTokens()).toEqual('0');      
          });

    });
    describe('updateAllGroupedBPswithLimits', () => {
        it('', () => {
            component.initialSignPostData = [{
                offerGroup: {
                    offerGroupId: '1'
                },
                freebetOfferId: '1',
                freebetOfferLimits: {
                    limitEntry: [{
                        limitRemaining: 3
                    }]
                }
            }];
            component.betpackDetails = [{
                betPackId: '1',
                showSignPost: 'true'
            }];
            spyOn(component, 'limitEntryUpdatewithlimits');
            spyOn(component, 'checkMaxPurchase');
            const retVal = component.updateAllGroupedBPswithLimits({
                offerGroup: {
                    offerGroupId: '1'
                }
            }, {});
            expect(retVal).toBeUndefined();
        });
        it('', () => {
            component.initialSignPostData = [{
                offerGroup: {
                    offerGroupId: '1'
                },
                freebetOfferId: '1',
                freebetOfferLimits: {
                    limitEntry: [{
                        limitRemaining: 3
                    }]
                }
            }];
            component.betpackDetails = [{
                betPackId: '1'
            }];
            spyOn(component, 'limitEntryUpdatewithlimits');
            spyOn(component, 'checkMaxPurchase');
            component.updateAllGroupedBPswithLimits({
                offerGroup: {
                    offerGroupId: '1'
                }
            }, {});
            expect(component.checkMaxPurchase).toHaveBeenCalled();
        });
        it('', () => {
            component.initialSignPostData = [{ offerGroup: { offerGroupId: '1' }, freebetOfferId: '1' }];
            component.betpackDetails = [{ betPackId: '1' }];
            spyOn(component, 'limitEntryUpdatewithlimits');
            spyOn(component, 'checkMaxPurchase');
            component.updateAllGroupedBPswithLimits({
                offerGroup: {
                    offerGroupId: '1'
                }
            }, {});
            expect(component.checkMaxPurchase).toHaveBeenCalled();
        });
        it('inside timeservice case', () => {
            component.initialSignPostData = [{
                startTime: '1', offerGroup: { offerGroupId: '1' },
                freebetOfferId: '1',
                freebetOfferLimits: { limitEntry: [{ limitRemaining: 3 }] }
            }];
            component.betpackDetails = [{ betPackId: '1', betPackStartDate: '2' }];
            let time = 11111111111111;
            spyOn(timeService, 'parseDateTime').and.returnValue({
                getTime: function (a) {
                    time--;
                    return time;
                }
            });
            spyOn(component, 'limitEntryUpdatewithlimits');
            spyOn(component, 'checkMaxPurchase');
            component.updateAllGroupedBPswithLimits({
                offerGroup: {
                    offerGroupId: '1'
                }
            }, {});
            expect(component.checkMaxPurchase).toHaveBeenCalled();
        });
        it('no freebetOfferLimits', () => {
            component.initialSignPostData = [{ startTime: '1', offerGroup: { offerGroupId: '1' }, freebetOfferId: '1' }];
            component.betpackDetails = [{ betPackId: '1', betPackStartDate: '2' }];
            let time = 11111111111111;
            spyOn(timeService, 'parseDateTime').and.returnValue({
                getTime: function (a) {
                    time--;
                    return time;
                }
            });
            spyOn(component, 'limitEntryUpdatewithlimits')
            spyOn(component, 'checkMaxPurchase');
            component.updateAllGroupedBPswithLimits({
                offerGroup: {
                    offerGroupId: '1'
                }
            }, {});
            expect(component.checkMaxPurchase).toHaveBeenCalled();
        });
    })
    describe('updateLimitDataWithCmsMaxClaims', () => {
        it('updateLimitDataWithCmsMaxClaims if case', () => {
            const retVal = component.updateLimitDataWithCmsMaxClaims({
                freebetOfferLimits: {
                    limitEntry: [{
                        limitRemaining: '1'
                    }]
                }
            }, {
                maxClaims: '1'
            });
            expect(retVal.limitRemaining).toBe('1')
        });
        it('updateLimitDataWithCmsMaxClaims else case', () => {
            const retVal = component.updateLimitDataWithCmsMaxClaims({
                freebetOfferLimits: {
                    limitEntry: [{
                        test: '1'
                    }]
                }
            }, {
                maxClaims: '1'
            });
            expect(retVal.limitRemaining).toBe('1')
        });
    })
    describe('getMaxClaimData', () => {
        it('getMaxClaimData', () => {
            const bpMaxClaimData = {
                freebetOfferLimits: {
                    limitEntry: [{
                        limitRemaining: 2
                    }]
                }
            }
            const retVal = component.getMaxClaimData(bpMaxClaimData);
            expect(retVal).toEqual(2)
        });
    })
    it('getMaxClaimData', () => {
        const retVal = component.getMaxClaimData(undefined);
        expect(retVal).toBeUndefined()
    });
    it('getMaxClaimData', () => {
        const bpMaxClaimData = {
            freebetOfferId: '123',
            freebetOfferLimits: null
        }
        const retVal = component.getMaxClaimData(bpMaxClaimData);
        expect(retVal).toBeUndefined()
    });
});
