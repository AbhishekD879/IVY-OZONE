import { HttpClient } from '@angular/common/http';
import { fakeAsync, TestBed, tick } from '@angular/core/testing';
import { UserService } from '@core/services/user/user.service';
import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { IBpError, IFreeRideCampaign, IRaceEvent, IUserSelectionDetail } from '@lazy-modules/freeRide/models/free-ride';
import { FreeRideService } from '@lazy-modules/freeRide/services/freeRide.service';
import { BehaviorSubject, Observable, of, throwError } from 'rxjs';
import { GtmService } from '@core/services/gtm/gtm.service';
import { SessionStorageService } from '@core/services/storage/session-storage.service';

describe('FreeRideService', () => {
    let service: FreeRideService;
    let userService: jasmine.SpyObj<UserService>;
    let freeBetsService: jasmine.SpyObj<FreeBetsService>;
    let sessionStorage: jasmine.SpyObj<SessionStorageService>;
    let gtmService: jasmine.SpyObj<GtmService>;
    let http: jasmine.SpyObj<HttpClient>;

    const mockUserSelectedData: IUserSelectionDetail = {
        freebettoken: '232323232',
        clientUserAgent: 'S|H|W0000000',
        isAccountBet: 'Y',
        currencyRef: 'GBP',
        userDto: {
            userName: 'testUser'
        },
        ipAddress: '203.153.211.250',
        channelRef: 'I',
        campaignId: 'e000012343343',
        brand: 'ladbrokes',
        userAnswers: [
            { questionId: 101, optionId: 1 },
            { questionId: 102, optionId: 2 },
            { questionId: 103, optionId: 3 }
        ]
    };

    const mockActiveCampaignInfo: IFreeRideCampaign = {
        id: '614ac62e78dbc52724af3987',
        name: 'TEST_23',
        brand: 'ladbrokes',
        displayFrom: '2021-09-23T07:02:21.270Z',
        displayTo: '2021-09-23T07:02:21.270Z',
        isPotsCreated: true,
        questionnarie: {
            questions: [
                {
                    questionId: 1,
                    quesDescription: 'Question 1',
                    options: [
                        {
                            optionId: 1,
                            optionText: 'top player'
                        },
                        {
                            optionId: 2,
                            optionText: 'Dark player'
                        },
                        {
                            optionId: 3,
                            optionText: 'Surprise Me'
                        }
                    ],
                    chatBoxResp: 'Great choice'
                }
            ],
            summaryMsg: 'Question is saved',
            welcomeMessage: 'welcomeMessage',
            horseSelectionMsg: 'Please select right horse'
        }
    };

    const mockHorseData: IRaceEvent = {
        horseName: 'HorseNametest',
        jockeyName: 'JockeyNameXYZ',
        raceName: '(USA) Club Hipico',
        raceTime: '18:21',
        silkUrl: 'https://aggregation.prod.ladbrokes.com/silks/racingpost/204683b',
        categoryName: 'Horse Racing',
        typeName: '(USA) Club Hipico',
        name: '18:21 Club Hipico',
        className: 'Horse Racing - Live',
        eventId: '8208340'
    };


    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [
                { provide: UserService, useValue: jasmine.createSpyObj('userService', ['']) },
                { provide: FreeBetsService, useValue: jasmine.createSpyObj('freeBetsService', ['getFreeBets']) },
                { provide: SessionStorageService, useValue: jasmine.createSpyObj('sessionStorage', ['get','set','remove']) },
                { provide: HttpClient, useValue: jasmine.createSpyObj('http', ['post']) },
                { provide : GtmService, useValue: jasmine.createSpyObj('gtmService', ['push'])},
            ]
        });

        service = TestBed.inject(FreeRideService);
        userService = TestBed.inject(UserService) as jasmine.SpyObj<UserService>;
        freeBetsService = TestBed.inject(FreeBetsService) as jasmine.SpyObj<FreeBetsService>;
        sessionStorage = TestBed.inject(SessionStorageService) as jasmine.SpyObj<SessionStorageService>;
        gtmService = TestBed.inject(GtmService) as jasmine.SpyObj<GtmService>;
        http = TestBed.inject(HttpClient) as jasmine.SpyObj<HttpClient>;
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });

    describe('requestSelectedHorse', () => {
        it('should return submiitedUserAnswer ', fakeAsync(() => {
            http.post.and.returnValue(of(mockHorseData));
            service.requestSelectedHorse(mockUserSelectedData).subscribe();
            tick();
            expect(service.requestSelectedHorse(mockUserSelectedData)).toEqual(jasmine.any(Observable));
        }));
    });
    it('should call thrown error ', fakeAsync(() => {
        spyOn(console, 'warn');
        const mockErr: IBpError = {
            path: 'errorPath', errMsg: 'errMsg'
        };
        http.post.and.returnValue(throwError(mockErr));
        service.requestSelectedHorse(mockUserSelectedData).subscribe(() => { }, (error) => { });
        tick();
        expect(console.warn).toHaveBeenCalled();

    }));

    describe('getAuthenticationHeader', () => {
        it('should return token ', () => {
            service['userService'].bppToken = 'tokenExist';
            service['getAuthenticationHeader']();
            expect(service['getAuthenticationHeader']).toEqual(jasmine.any(Function));
        });
        it('should return token ', () => {
            service['userService'].bppToken = undefined;
            service['getAuthenticationHeader']();
            expect(service['getAuthenticationHeader']).toEqual(jasmine.any(Function));
        });
    });

    describe('clearFreebet', () => {
        it('should call next method of behaviour sub ', () => {
            freeBetsService['isFRFreeBets'] = new BehaviorSubject<any>(1);
            sessionStorage.get.and.returnValue(JSON.stringify(mockActiveCampaignInfo));
            service.clearFreebet();
            freeBetsService['isFRFreeBets'].next('initialDataMock');
            freeBetsService['isFRFreeBets'].subscribe((data) => {
                expect(data).toBe('initialDataMock');
            });
        });
    });

   describe('sendGTM', () => {
        it('should not append eventDetails if it is not provided', () => {
          const gtmData = {
            event: 'trackEvent',
            eventAction: 'eventAction',
            eventCategory: 'free ride',
            eventLabel: 'eventLabel',
          };
          service.sendGTM('eventAction', 'eventLabel');
          expect(gtmService.push).toHaveBeenCalledWith('trackEvent', gtmData);
        });
        it('should append eventDetails if it is provided', () => {
          const gtmData = {
            event: 'trackEvent',
            eventAction: 'eventAction',
            eventCategory: 'free ride',
            eventLabel: 'eventLabel',
            eventDetails: 'eventDetails',
          };
          service.sendGTM('eventAction', 'eventLabel', 'eventDetails');
          expect(gtmService.push).toHaveBeenCalledWith('trackEvent', gtmData);
        });
      });

});
