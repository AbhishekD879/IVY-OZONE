import { fakeAsync, tick } from '@angular/core/testing';
import { of, Subject } from 'rxjs';
import { FreeRideHelperService } from '@lazy-modules/freeRideHelper/freeRideHelper.service';
import { IFreebetToken } from '@bpp/services/bppProviders/bpp-providers.model';
import { IFreeRideCampaign } from '@lazy-modules/freeRide/models/free-ride';

describe('@FreeRideRideService', () => {

    let service: FreeRideHelperService,
        freeBetsService, sessionStorage, cmsService,pubSubService, http;

    const freeBetsRes: IFreebetToken = {
        tokenId: '2200000778',
        freebetTokenId: '2200000778',
        freebetOfferId: '28985',
        freebetOfferName: 'CRM-Offer-1',
        freebetOfferDesc: 'LASPRETLASPONONFRBNN',
        freebetTokenDisplayText: '',
        freebetTokenValue: '5.00',
        freebetAmountRedeemed: '0.00',
        freebetTokenRedemptionDate: '2022-03-29 06:47:43',
        freebetRedeemedAgainst: '2022-03-29 06:47:43',
        freebetTokenExpiryDate: '2022-03-29 06:47:43',
        freebetMinPriceNum: '',
        freebetMinPriceDen: '',
        freebetTokenAwardedDate: '2022-03-29 06:47:43',
        freebetTokenStartDate: '2022-03-29 06:47:43',
        freebetTokenType: 'BETBOOST',
        freebetTokenRestrictedSet: {
            level: '',
            id: ''
        },
        freebetGameName: '',
        freebetTokenStatus: '',
        currency: '',
        tokenPossibleBet: {
            name: '',
            betLevel: '',
            betType: '',
            betId: '',
            channels: ''
        },
        tokenPossibleBets: [{
            name: '',
            betLevel: '',
            betType: '',
            betId: '',
            channels: ''
        }],
        freebetOfferType: '',
        tokenPossibleBetTags: {
            'tagName': 'FRRIDE'
        }
    };

    const activeCampaignDetail: IFreeRideCampaign = {
        id: '61711866f5c4a05b22fd8a0b',
        name: 'Campaign_01_dev',
        brand: 'ladbrokes',
        displayFrom: '2021-11-01T02:51:50Z',
        displayTo: '2021-11-01T17:51:50Z',
        isPotsCreated: false,
        questionnarie: {
            questions: [
                {
                    questionId: 1,
                    quesDescription: 'q1',
                    options: [
                        {
                            optionId: 1,
                            optionText: 'o1'
                        },
                        {
                            optionId: 2,
                            optionText: 'o2'
                        },
                        {
                            optionId: 3,
                            optionText: 'o2'
                        }
                    ],
                    chatBoxResp: 'cbr'
                },
                {
                    questionId: 2,
                    quesDescription: 'q2',
                    options: [
                        {
                            optionId: 4,
                            optionText: 'o1'
                        },
                        {
                            optionId: 5,
                            optionText: 'o2'
                        },
                        {
                            optionId: 6,
                            optionText: 'o3'
                        }
                    ],
                    chatBoxResp: 'cbr2'
                },
                {
                    questionId: 3,
                    quesDescription: 'q3',
                    options: [
                        {
                            optionId: 7,
                            optionText: 'o1'
                        },
                        {
                            optionId: 8,
                            optionText: 'o2'
                        },
                        {
                            optionId: 9,
                            optionText: 'o3'
                        }
                    ],
                    chatBoxResp: 'cbr3'
                }
            ],
            summaryMsg: 'Summary',
            welcomeMessage: 'Welcome',
            horseSelectionMsg: 'Horse select'
        }
    };

    const initialDataMock = {
        systemConfiguration: { systemConfiguration: {} },
        modularContent: { modularContent: {} },
        navigationPoints: [{ a: 1, b: 2 }],
        sportCategories: [{ categoryId: 1, sportName: 'category1', showFreeRideBanner: true },
        { categoryId: 2, sportName: 'category2', showFreeRideBanner: false },
        { categoryId: 3, sportName: 'greyhoundracing', showFreeRideBanner: false },
        { categoryId: 4, imageTitle: 'football', svgId: '#1', showFreeRideBanner: false }],
        svgSpriteContent: '<svg>',
        seoPages: { '1': { title: 'bet on sports', description: 'betting on sports' } },
        seoAutoPages: { '/event': { title: 'bet on event', description: 'betting on event' } }
    } as any;

    beforeEach(() => {

        freeBetsService = {
            isFRFreeBets: {
                subscribe: jasmine.createSpy('subscribe').and.returnValue(of(freeBetsRes)),
                next: jasmine.createSpy('next').and.returnValue(of(freeBetsRes))
            }
        };

        freeBetsService = {
            isFRFreeBets: {
                subscribe: jasmine.createSpy('subscribe').and.returnValue(of(freeBetsRes)),
                next: jasmine.createSpy('next').and.returnValue(of(freeBetsRes))
            }
        };

        http = {
            get: jasmine.createSpy('get').and.returnValue(of(
                {
                    body: []
                }))
        };

        sessionStorage = {
            set: jasmine.createSpy('set'),
            get: jasmine.createSpy('get'),
            remove: jasmine.createSpy('remove')
        };

        cmsService = {
            getCmsInitData: jasmine.createSpy('getCmsInitData').and.returnValue(of(initialDataMock)),

        };
        
        pubSubService = {
            subscribe: jasmine.createSpy('subscribe').and.callFake((arg1, arg2, callback) => {
                sessionStorage.get.and.returnValue(JSON.stringify(activeCampaignDetail));
                callback();
            }),
            API: {
                SESSION_LOGOUT: 'SESSION_LOGOUT',
                SESSION_LOGIN: 'SESSION_LOGIN'
            },
            publish: jasmine.createSpy('publish')
          } as any;

        service = new FreeRideHelperService(
            freeBetsService,
            sessionStorage,
            cmsService,
            pubSubService,
            http,
        );
        jasmine.clock().install();
    });

    afterEach(() => {
        jasmine.clock().uninstall();
      });

    it('#constructor', () => {
        expect(sessionStorage.get.and.returnValue(JSON.stringify(activeCampaignDetail)).and.returnValue(true)).toBeTruthy();
        expect(sessionStorage.get.and.returnValue(JSON.stringify(freeBetsRes)).and.returnValue(true)).toBeTruthy();
    });

    it('#constructor', () => {
        expect(sessionStorage.get.and.returnValue(null).and.returnValue(false)).toBeTruthy();
        expect(sessionStorage.get.and.returnValue(null).and.returnValue(false)).toBeTruthy();
    });

    it('should be created', () => {
        sessionStorage.get.and.returnValue(JSON.stringify(activeCampaignDetail));
        spyOn(service, 'getFreeRide').and.returnValue(of(activeCampaignDetail));
        expect(service).toBeTruthy();
    });

    it('should be created', fakeAsync(() => {
        sessionStorage.get.and.returnValue(JSON.stringify(activeCampaignDetail));
        spyOn(service, 'getFreeRide').and.returnValue(of(activeCampaignDetail));
        tick();
        expect(service).toBeTruthy();
    }));

    it('should be created', fakeAsync(() => {
        freeBetsService.isFRFreeBets = new Subject<any>();

        service = new FreeRideHelperService(
            freeBetsService,
            sessionStorage,
            cmsService,
            pubSubService,
            http,
        );
        sessionStorage.get.and.returnValue(null);
        spyOn(service, 'getFreeRide').and.returnValue(of(activeCampaignDetail));
        freeBetsService.isFRFreeBets.next(freeBetsRes);
        tick();
        tick();
        expect(service).toBeTruthy();

    }));

    describe('campaignExist', () => {
        it('should return true if campaign is active ', () => {

            const date = new Date(Date.now());
            date.setHours(date.getHours() - 5);
            const startTime = date.toISOString();
            date.setHours(date.getHours() + 10);
            const endDate = date.toISOString();
            activeCampaignDetail.displayFrom = startTime;
            activeCampaignDetail.displayTo = endDate;

            sessionStorage.get.and.returnValue(JSON.stringify(activeCampaignDetail));

            service.campaignExist();

            expect(service.campaignExist).toBeTruthy();
        });
        it('should return false if campaign is false ', () => {

            sessionStorage.get.and.returnValue(null);

            const capaginExistFn = service.campaignExist();

            expect(capaginExistFn).toBeFalse();
        });
    });

    describe('showFreeRideOnSportPage', () => {
        it('should return true if campaign is active ', () => {

            service.showFRBannerOnSportsPages = ['test1', 'test2']

            service.showFreeRideOnSportPage('test1');

            expect(service.showFreeRideOnSportPage).toBeTruthy();
        });
    });

    describe('@getData()', () => {
        it('should call getData() with params', () => {
            const url = 'test-link',
                options = { option: 'option' };

            service.CMS_ENDPOINT = 'testCMS.com';
            service.brand = 'ladbrokes';
            service['getData'](url, options);


            expect(http.get).toHaveBeenCalledWith(
                `${service.CMS_ENDPOINT}/${service.brand}/${url}`,
                { observe: 'response', params: options }
            );
        });

        it('should call getData() with defalut params', () => {
            const url = 'test-link';

            service.CMS_ENDPOINT = 'testCMS.com';
            service.brand = 'ladbrokes';
            service['getData'](url);


            expect(http.get).toHaveBeenCalledWith(
                `${service.CMS_ENDPOINT}/${service.brand}/${url}`,
                { observe: 'response', params: {} }
            );
        });
    });

    describe('getFreeRideCampaign', () => {
        it('should return true if campaign is active ', fakeAsync(() => {
            service['getData'] = jasmine.createSpy('getData').and.returnValue(of({ body: activeCampaignDetail }));

            service.getFreeRideCampaign().subscribe();
            tick();

            expect(service.getFreeRideCampaign).toBeTruthy();
        }));
    });

    describe('activFreeRideCampaign', () => {
        it('should return activFreeRideCampaign if Date is in active range', () => {
            const baseDate = new Date(); 
            baseDate.setHours(16);
            jasmine.clock().mockDate(baseDate);

            const startTime = new Date();
            startTime.setHours(15);

            const endDate = new Date();
            endDate.setHours(17);
            activeCampaignDetail.displayFrom = startTime.toISOString();
            activeCampaignDetail.displayTo = endDate.toISOString();
            activeCampaignDetail.isPotsCreated = true;

            service.getFreeRideActiveCampaign([activeCampaignDetail]);

            expect(service.getFreeRideActiveCampaign([activeCampaignDetail])).toEqual(activeCampaignDetail);
        });

        it('should return activFreeRideCampaign if Date is not in active range', () => {
            const baseDate = new Date('2022-02-05T08:49:37.177Z');
            jasmine.clock().mockDate(baseDate);

            baseDate.setHours(13, 0);

            const startTime = baseDate.toISOString();
            baseDate.setHours(15, 0);

            const endDate = baseDate.toISOString();

            const campaignDetail = [
                {
                    'displayFrom': startTime,
                    'displayTo': endDate,
                    'isPotsCreated': false
                }
            ];
            service.getFreeRideActiveCampaign(campaignDetail);

            expect(service.getFreeRideActiveCampaign(campaignDetail)).toBeUndefined();
        });
    });

    describe('getFreeRide', () => {
        it('should return true if campaign is active ', fakeAsync(() => {
            service['getData'] = jasmine.createSpy('getData').and.returnValue(of({ body: activeCampaignDetail }));

            spyOn(service, 'getFreeRideCampaign').and.returnValue(of([activeCampaignDetail]));
            spyOn(service, 'getFreeRideActiveCampaign').and.returnValue(activeCampaignDetail);

            service.getFreeRide().subscribe();
            tick();

            expect(service.getFreeRideCampaign).toBeTruthy();
        }));
    });

    describe('showFreeRide', () => {
        it('should return true if campaign exists', () => {

            spyOn(service, 'campaignExist').and.returnValue(true);
            spyOn(service, 'freeBetExist').and.returnValue(true);
            service.showFreeRide();

            expect(service.showFreeRide).toBeTruthy();
        });

        it('should return true if campaign exists', () => {
            spyOn(service, 'campaignExist').and.returnValue(false);
            spyOn(service, 'freeBetExist').and.returnValue(false);

            service.showFreeRide();

            expect(service.showFreeRide).toBeTruthy();
        });
    });

    describe('freeBetExist', () => {
        it('should return true if freeBetExpiryDate is in active range ', () => {
            const baseDate = new Date('2022-02-05T08:49:37.177Z');
            jasmine.clock().mockDate(baseDate);

            baseDate.setHours(15, 0);

            const endDate = baseDate.toISOString();

            const freeBetRespJson = {
                freeBetExpiryDate: endDate,
                freeBetTokenId: '2200000778'
            };
            sessionStorage.get.and.returnValue(JSON.stringify(freeBetRespJson));

            service.freeBetExist();

            expect(service.freeBetExist).toBeTruthy();
        });

        it('should return true if freeBetExpiryDate is not in active range ', () => {
            const date = new Date();
            date.setHours(22);
            const endDate = date.toISOString();


            const freeBetRespJson = {
                freeBetTokenId: '2200000778'
            };
            sessionStorage.get.and.returnValue(JSON.stringify(freeBetRespJson));

            const freeBetExistFn = service.freeBetExist();

            expect(freeBetExistFn).toBeFalse();
        });
    });

    describe('freeRideOnSportsPages', () => {
        it('should return true if campaign is active ', () => {

            service.showFRBannerOnSportsPages = ['test1', 'test2'];

            const freeRideOnSportsPagesFn = service.freeRideOnSportsPages();

            expect(freeRideOnSportsPagesFn).toEqual();
        });
    });
});