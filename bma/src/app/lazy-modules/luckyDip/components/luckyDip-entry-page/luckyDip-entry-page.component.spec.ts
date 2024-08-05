import { fakeAsync, tick } from "@angular/core/testing";
import { LuckyDipEntryPageComponent } from "@lazy-modules/luckyDip/components/luckyDip-entry-page/luckyDip-entry-page.component";
import { of } from "rxjs";

describe('LuckyDipEntryPageComponent', () => {
    let component: LuckyDipEntryPageComponent,
        luckyDipCMSService,
        componentFactoryResolver,
        dialogService,
        vanillaApiService,
        changeDetectorRef,
        storage;

    let mockLuckyDipCMSData;
    let mockEvent;
    let mockOutcome;
    let mockMarket;


    beforeEach(() => {
        mockLuckyDipCMSData = {
            id: ' 63ecd2a079768e6cf926a83b',
            luckyDipBannerConfig: {
                animationImgPath: '{4690D591-2C33-47BD-85E2-F7382C8F74AC}',
                bannerImgPath: "{8C4DE9BA-3F8C-49D9-949E-A2FA9BA9232E}",
                overlayBannerImgPath: '{8C4DE9BA-3F8C-49D9-949E-A2FA9BA9232D}'
            },
            luckyDipFieldsConfig: {
                title: 'Lucky DIp test 1',
                desc: 'Here u can play',
                welcomeMessage: ' Welcome to COntest',
                betPlacementTitle: 'First title',
                betPlacementStep1: 'Step 1',
                betPlacementStep2: 'Step 2',
                betPlacementStep3: 'Step 3',
                termsAndConditionsURL: 'http:/url.com',
                playerCardDesc: 'Player 1',
                potentialReturnsDesc: 'Win Money'
            },
            playerPageBoxImgPath: '{4690D591-2C33-47BD-85E2-F7382C8F74AT}'
        };
        mockEvent = {
            "id": "3331136",
            "name": "TEST",
            "eventStatusCode": "A",
            "isActive": "true",
            "isDisplayed": "true",
            "displayOrder": "0",
            "siteChannels": "P,Q,C,I,M,",
            "eventSortCode": "MTCH",
            "startTime": "2023-02-28T18:43:00Z",
            "rawIsOffCode": "-",
            "classId": "195",
            "typeId": "3545",
            "sportId": "18",
            "liveServChannels": "sEVENT0003331136,",
            "liveServChildrenChannels": "SEVENT0003331136,",
            "categoryId": "18",
            "categoryCode": "GOLF",
            "categoryName": "Golf",
            "categoryDisplayOrder": "-377",
            "className": "Golf All Golf",
            "classDisplayOrder": "0",
            "classSortCode": "ST",
            "classFlagCodes": "SP,",
            "typeName": "Golf Day test",
            "typeDisplayOrder": "-100",
            "isOpenEvent": "true",
            "isNext2DayEvent": "true",
            "isNext1WeekEvent": "true",
            "isAvailable": "true",
            "cashoutAvail": "N",
            "children": [
                {
                    "market": {
                        "id": "48980432",
                        "eventId": "3331136",
                        "templateMarketId": "1597587",
                        "templateMarketName": "Lucky Dip",
                        "marketMeaningMajorCode": "N",
                        "marketMeaningMinorCode": "CW",
                        "name": "Lucky Dip",
                        "isLpAvailable": "true",
                        "betInRunIndex": "1",
                        "displayOrder": "0",
                        "marketStatusCode": "A",
                        "isActive": "true",
                        "isDisplayed": "true",
                        "siteChannels": "P,Q,C,I,M,",
                        "liveServChannels": "sEVMKT0048980432,",
                        "liveServChildrenChannels": "SEVMKT0048980432,",
                        "priceTypeCodes": "LP,",
                        "drilldownTagNames": "MKTFLAG_LD,",
                        "isAvailable": "true",
                        "maxAccumulators": "25",
                        "minAccumulators": "1",
                        "cashoutAvail": "N",
                        "termsWithBet": "N",
                        "children": [
                            {
                                "outcome": {
                                    "id": "213900109",
                                    "marketId": "48980432",
                                    "name": "Player A",
                                    "outcomeMeaningMajorCode": "CW",
                                    "displayOrder": "0",
                                    "outcomeStatusCode": "A",
                                    "isActive": "true",
                                    "isDisplayed": "true",
                                    "siteChannels": "P,Q,C,I,M,",
                                    "liveServChannels": "sSELCN0213900109,",
                                    "liveServChildrenChannels": "SSELCN0213900109,",
                                    "isAvailable": "true",
                                    "cashoutAvail": "N",
                                    "children": [
                                        {
                                            "price": {
                                                "id": "1",
                                                "priceType": "LP",
                                                "priceNum": "125",
                                                "priceDen": "1",
                                                "priceDec": "126.00",
                                                "isActive": "true",
                                                "displayOrder": "1"
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            ]
        };
        mockOutcome = {
            "id": "213900109",
            "marketId": "48980432",
            "name": "Player A",
            "outcomeMeaningMajorCode": "CW",
            "displayOrder": 0,
            "outcomeStatusCode": "A",
            "isActive": "true",
            "isDisplayed": "true",
            "siteChannels": "P,Q,C,I,M,",
            "liveServChannels": "sSELCN0213900109,",
            "liveServChildrenChannels": "SSELCN0213900109,",
            "isAvailable": "true",
            "cashoutAvail": "N",
            "prices": [
                {
                    "id": "1",
                    "priceType": "LP",
                    "priceNum": 125,
                    "priceDen": 1,
                    "priceDec": 126,
                    "isActive": "true",
                    "displayOrder": "1"
                }
            ]
        };

        mockMarket = {
            "id": "48980432",
            "eventId": "3331136",
            "templateMarketId": "1597587",
            "templateMarketName": "Lucky Dip",
            "marketMeaningMajorCode": "N",
            "marketMeaningMinorCode": "CW",
            "name": "random,random golfer,125,1",
            "isLpAvailable": "true",
            "betInRunIndex": "1",
            "displayOrder": 0,
            "marketStatusCode": "A",
            "isActive": "true",
            "isDisplayed": "true",
            "siteChannels": "P,Q,C,I,M,",
            "liveServChannels": "sEVMKT0048980432,",
            "liveServChildrenChannels": "SEVMKT0048980432,",
            "priceTypeCodes": "LP,",
            "drilldownTagNames": "MKTFLAG_LD,",
            "isAvailable": "true",
            "maxAccumulators": "25",
            "minAccumulators": "1",
            "cashoutAvail": "N",
            "termsWithBet": "N",
            "outcomes": [
                {
                    "id": "213900109",
                    "marketId": "48980432",
                    "name": "Player A",
                    "outcomeMeaningMajorCode": "CW",
                    "displayOrder": 0,
                    "outcomeStatusCode": "A",
                    "isActive": "true",
                    "isDisplayed": "true",
                    "siteChannels": "P,Q,C,I,M,",
                    "liveServChannels": "sSELCN0213900109,",
                    "liveServChildrenChannels": "SSELCN0213900109,",
                    "isAvailable": "true",
                    "cashoutAvail": "N",
                    "prices": [
                        {
                            "id": "1",
                            "priceType": "LP",
                            "priceNum": 125,
                            "priceDen": 1,
                            "priceDec": 126,
                            "isActive": "true",
                            "displayOrder": "1"
                        }
                    ]
                }
            ],
            "viewType": "List",
            "terms": "Each Way: undefined/undefined odds - places "
        };

        luckyDipCMSService = {
            getLuckyDipCMSData: jasmine.createSpy('luckyDipCMSService.getLuckyDipCMSData').and.returnValue(of(mockLuckyDipCMSData)),
        } as any;

        componentFactoryResolver = {
            resolveComponentFactory: jasmine.createSpy('componentFactoryResolver.resolveComponentFactory')
        } as any;
        dialogService = {
            openDialog: jasmine.createSpy('openDialog')
        };

        vanillaApiService = {
            get: jasmine.createSpy('get')
        }
        changeDetectorRef = {
            detectChanges: jasmine.createSpy('detectChanges')
        }
        storage = {
            setCookie: jasmine.createSpy(),
            get: jasmine.createSpy(),
            set: jasmine.createSpy(),
            remove: jasmine.createSpy(),
            removeCookie: jasmine.createSpy(),
            getCookie: jasmine.createSpy()
          };

        component = new LuckyDipEntryPageComponent(
            luckyDipCMSService, componentFactoryResolver, dialogService, storage,vanillaApiService,
            changeDetectorRef
        );
    });

    describe('ngOnInit', () => {
        it('ngOnInit', () => {

            const spySetMarketDetails = spyOn(component, 'setMarketDetails');
            component.ngOnInit();

            expect(spySetMarketDetails).toHaveBeenCalled();

        });
    });
    
    describe('ngOnDestroy', () => {
        it('ngOnDestroy', () => {
            component.ngOnDestroy();

            expect(storage.remove).toHaveBeenCalled();
        });
    });


    describe('ngAfterViewInit', () => {

        it('should set cmsData if get response from getLuckyDipCMSData', fakeAsync(() => {
            mockLuckyDipCMSData
            component.event = mockEvent;
            const mockTeaser = [
                {
                    "type": "segmentDefault",
                    "teasers": [
                        {
                            "backgroundImage": {
                                "src": "https://scmedia.cms.test.env.works/$-$/020f4a8f6dae46edb62f029a570bbc12.svg",
                                "alt": "ldBgbanner (1)"
                            },
                            "bannerLink": {
                                "url": "https://scmedia.cms.test.env.works/$-$/00372699c2dd4583a76c430e53916ada.svg",
                                "attributes": {
                                    "target": "_blank"
                                }
                            },
                            "itemId": "{4690D591-2C33-47BD-85E2-F7382C8F74AC}",
                            "itemName": "luckydip%20banner"
                        },
                        {
                            "backgroundImage": {
                                "src": "https://scmedia.cms.test.env.works/$-$/00372699c2dd4583a76c430e53916ada.svg",
                                "alt": "Luckydip Logo"
                            },
                            "bannerLink": {
                                "url": "https://google.com",
                                "attributes": {

                                }
                            },
                            "itemId": "{8C4DE9BA-3F8C-49D9-949E-A2FA9BA9232E}",
                            "itemName": "luckydip%20overlay%20banner"
                        },
                        {
                            "backgroundImage": {
                                "src": "https://scmedia.cms.test.env.works/$-$/00372699c2dd4583a76c430e53916ada.svg",
                                "alt": "Luckydip Logo"
                            },
                            "bannerLink": {
                                "url": "https://google.com",
                                "attributes": {

                                }
                            },
                            "itemId": "{E45E91B6-245E-4B39-91B4-CBDA9624E214}",
                            "itemName": "testmar20"
                        },
                        {
                            "backgroundImage": {
                                "src": "https://scmedia.cms.test.env.works/$-$/00372699c2dd4583a76c430e53916ada.svg",
                                "alt": "Luckydip Logo"
                            },
                            "bannerLink": {
                                "url": "https://google.com",
                                "attributes": {

                                }
                            },
                            "itemId": "{8C4DE9BA-3F8C-49D9-949E-A2FA9BA9232D}",
                            "itemName": "testmar20"
                        },
                        {
                            "backgroundImage": {
                                "src": "https://scmedia.cms.test.env.works/$-$/00372699c2dd4583a76c430e53916ada.svg",
                                "alt": "Luckydip Logo"
                            },
                            "bannerLink": {
                                "url": "https://google.com",
                                "attributes": {

                                }
                            },
                            "itemId": "{4690D591-2C33-47BD-85E2-F7382C8F74AT}",
                            "itemName": "testmar20"
                        }

                    ]
                }
            ]
            component.getOverlayBannerFromSiteCore = jasmine.createSpy('getOverlayBannerFromSiteCore').and.returnValue(of(mockTeaser))
            component.market = mockMarket;
            component.outcome = mockOutcome;

            component.ngAfterViewInit();
            tick();
            expect(component.cmsData).toEqual(mockLuckyDipCMSData);
        }));

        it('If empty response get from getBannerFromSitecore ', fakeAsync(() => {


            const mockTeaser = [
                {
                    "type": "segmentDefault",
                }
            ]
            component.getOverlayBannerFromSiteCore = jasmine.createSpy('getOverlayBannerFromSiteCore').and.returnValue(of(mockTeaser))
            component.ngAfterViewInit();
            tick();
            expect(component.animationImg).toBeUndefined();
            expect(component.bannerImage).toBeUndefined();
            expect(component.overlayBannerImage).toBeUndefined();
        }));

    });

    describe('onInfoIconClick', () => {

        it('should open popup', () => {
            const event = {
                stopPropagation: jasmine.createSpy('stopPropagation')
            };

            const spyOpenPopUp = spyOn(component, 'openPopUp');
            component.onInfoIconClick(event as any);

            expect(spyOpenPopUp).toHaveBeenCalled();
        });
    });

    describe('openPopUp', () => {
        it('open dialog', () => {
            component.cmsData = mockLuckyDipCMSData
            const data = {
                data: {
                    marketTitle: 'Lucky DIp test 1',
                    marketDescripton: 'Here u can play',
                    overlayBannerImgPath: undefined
                },

            };
            component.openPopUp();

            expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
            expect(dialogService.openDialog).toHaveBeenCalledWith('marketDescription', undefined, true, data);
        });
    });

    describe('getOverlayBannerFromSiteCore', () => {
        it('getOverlayBannerFromSiteCore', () => {

            component.getOverlayBannerFromSiteCore();

            expect(vanillaApiService.get).toHaveBeenCalled();
        });
    });

    describe('setMarketDetails', () => {
        it('setMarketDetails', () => {

            component.market = mockMarket;

            component.setMarketDetails();

            expect(component.marketName).toEqual('random');
            expect(component.luckyDipDesc).toEqual('random golfer');
            expect(component.odds).toEqual('125');

        });
    });

});
