import { fakeAsync, TestBed, tick } from '@angular/core/testing';
import { Router } from '@angular/router';
import { of, throwError } from 'rxjs';
import { PlatformLocation } from '@angular/common';
import { ClientUserAgentService } from '@core/services/clientUserAgent/client-user-agent.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DeviceService } from '@core/services/device/device.service';
import { IRoutingHelperEvent } from '@core/services/routingHelper/routing-helper.model';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { TimeSyncService } from '@core/services/timeSync/time-sync.service';
import { UserService } from '@core/services/user/user.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { FreeRideService } from '@lazy-modules/freeRide/services/freeRide.service';
import { FreeRideDomService } from '@lazy-modules/freeRide/services/freeRideDom.service';
import { FreeRideOverlayComponent } from '@lazy-modules/freeRide/components/free-ride-overlay/free-ride-overlay.component';
import { FreeRideHelperService } from '@lazy-modules/freeRideHelper/freeRideHelper.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IFreeRideCampaign, IQuestionnarie, IRaceEvent, IUserSelectionDetail } from '@lazy-modules/freeRide/models/free-ride';

describe('FreeRideOverlayComponent', () => {
    let component;
    let loc, deviceService,
        router, windowRef,
        rendererService, userService, freeRideService, routingHelperService,
        clientUserAgentService, timeSyncService, pubsubService, freeRideDomService, freeRideHelperService;
    const mockHorseSel = {
        horseName: 'ABC',
        jockeyName: 'XYZ',
        raceName: 'Cheltenham',
        raceTime: 'xx:xx',
        silkUrl: 'string',
        categoryName: 'string',
        typeName: '((USA) Club Hipico)',
        name: '(18:21 Club Hipico)',
        className: '(Horse Racing - Live)',
        eventId: '(8208340)',
        betError: []
    };
    const mockOptions = [{
        'optionId': 1,
        'optionText': 'top player'
    },
    {
        'optionId': 2,
        'optionText': 'Dark player'
    }];
    const mockQuestions: IQuestionnarie = {
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
            },
            {
                questionId: 2,
                quesDescription: 'Question 2',
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
            },
            {
                questionId: 2,
                quesDescription: 'Question 2',
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
        summaryMsg: 'Summary msg',
        welcomeMessage: 'welcome',
        horseSelectionMsg: 'horse selected'
    };
    const mockSplashInfo = {
        bannerImageUrl: '/images/uploads/freeRideSplashPage',
        buttonText: 'btn',
        brand: 'bma',
        freeRideLogoUrl: null,
        id: '611b88622418810936bdefc8',
        splashImageUrl: '/images/uploads/freeRideSplashPage',
        termsAndCondition: 'T&C',
        welcomeMsg: 'welcome'
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
    const mockSelectionRequestData: IUserSelectionDetail = {
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

    const mockCampaign : IFreeRideCampaign ={
        id: 'abc',
        name:  'test',
        brand: 'ladbrokes',
        displayFrom: '',
        displayTo: '',
        isPotsCreated: false,
        questionnarie: mockQuestions
    };

    beforeEach(async () => {
        TestBed.configureTestingModule({
            providers: [
                { provide: UserService, useValue: jasmine.createSpyObj('userService', ['']) },
                { provide: WindowRefService, useValue: windowRef },
                { provide: RendererService, useValue: rendererService },
                { provide: FreeRideService, useClass: FreeRideService },
                { provide: RoutingHelperService, useValue: routingHelperService },
                { provide: PlatformLocation, useValue: loc },
                { provide: Router, useValue: router },
                { provide: ClientUserAgentService, useValue: clientUserAgentService },
                { provide: TimeSyncService, useValue: timeSyncService },
                { provide: DeviceService, useValue: deviceService },
                { provide: PubSubService, useValue: pubsubService },
                { provide: FreeRideDomService, useValue: freeRideDomService },
                { provide: FreeRideHelperService, useValue: freeRideHelperService}
            ]
        });

        rendererService = {
            renderer: {
                appendChild: jasmine.createSpy(),
                addClass: jasmine.createSpy(),
                removeClass: jasmine.createSpy(),
                setAttribute: jasmine.createSpy(),
                createElement: jasmine.createSpy(),
                setProperty: jasmine.createSpy(),
                removeChild: jasmine.createSpy(),
                listen: jasmine.createSpy().and.callFake((a, b, event) => {
                    event({ stopPropagation: jasmine.createSpy() });
                }),
                setStyle: jasmine.createSpy(),
                removeStyle: jasmine.createSpy()
            }
        };

        clientUserAgentService = {
            getId: jasmine.createSpy('getId').and.returnValue(of('ssgqgsd'))
        };

        routingHelperService = {
            formEdpUrl: jasmine.createSpy('formEdpUrl')
        };

        loc = {
            onPopState: jasmine.createSpy('onPopState')
        };

        router = {
            navigateByUrl: jasmine.createSpy('navigateByUrl')
        };

        pubsubService = {
            API: { FREE_RIDE_BET: 'FREE_RIDE_BET' },
            publish: jasmine.createSpy('publish')
        };

        freeRideDomService = {
            createDOMElements: jasmine.createSpy().and.returnValue(
                {
                    get: jasmine.createSpy().and.returnValue({ scrollIntoView: () => { } }),
                    scrollIntoView: () => { }
                }),
            appendDomElems: jasmine.createSpy(),
            removeElem: jasmine.createSpy()
        };

        windowRef = {
            document: {
                querySelector: jasmine.createSpy(),
                querySelectorAll: jasmine.createSpy().and.returnValue([
                    { className: 'answer-option', remove: jasmine.createSpy() },
                    { className: 'answer-option', remove: jasmine.createSpy() }
                ])
            },
            nativeWindow: {
                setTimeout: jasmine.createSpy('setTimeout').and.callFake(fn => fn()),
                clearTimeout: jasmine.createSpy('clearTimeout')
            }
        };

        component = new FreeRideOverlayComponent(
            loc,
            router,
            windowRef,
            rendererService,
            freeRideService,
            routingHelperService,
            clientUserAgentService,
            userService,
            timeSyncService,
            deviceService,
            pubsubService,
            freeRideDomService,
            freeRideHelperService
        );

        component.audioPlayerRef = jasmine.createSpyObj('audioPlayerRef', ['nativeElement']);

        component.audioPlayerRef = {
            nativeElement: {
                load: jasmine.any(Function),
                play: jasmine.any(Function),
                pause: jasmine.any(Function),
            }
        };
        component.currentAudio = {
            nativeElement: {
                load: jasmine.any(Function),
                play: jasmine.any(Function),
                pause: jasmine.createSpy('pause'),
            }
        };
        component.ansAudioPlayerRef = {
             nativeElement: {
                   play:jasmine.createSpy('play').and.returnValue({catch : jasmine.createSpy('catch')})
            }
        };

        component.quesAudioPlayerRef = {
            nativeElement: {
                   play:jasmine.createSpy('play').and.returnValue({catch : jasmine.createSpy('catch')})
            }
        };

        component.resultAudioPlayerRef = {
            nativeElement: {
                   play:jasmine.createSpy('play').and.returnValue({catch : jasmine.createSpy('catch')})
            }
        };

        component['userService'] = jasmine.createSpyObj('userService', ['currency']);
        component['timeSyncService'] = jasmine.createSpyObj('timeSyncService', ['ip']);
        component['deviceService'] = jasmine.createSpyObj('deviceService', ['channel']);
        component['freeRideService'] = jasmine.createSpyObj('freeRideService', ['requestSelectedHorse','sendGTM']);
        component['freeRideHelperService'] = jasmine.createSpyObj('freeRideHelperService', ['getFreeRideActiveCampaign']);
        component.questions = {
            questions: [],
            summaryMsg: 'string',
            welcomeMessage: 'string',
            horseSelectionMsg: 'string',
        };
        component['deviceService'].channel = {
            channelRef: {
                id: 'I'
            }
        };
    });

    it('should create', () => {
        expect(loc.onPopState).toHaveBeenCalledWith(jasmine.any(Function));
        expect(component).toBeTruthy();
    });

    describe('ngOnInit', () => {
        it('should call initOverlay', () => {
            spyOn(component, 'initOverlay');

            component.ngOnInit();
    
            expect(component.initOverlay).toHaveBeenCalled();
        });
    });

    describe('initOverlay', () => {
        it('should initOverlay', () => {
            spyOn(component, 'getDomAccessors');
            spyOn(component, 'displayQuestionNumber');

            const campaignData = {
                isSoundChecked: true,
                campaignInfo: mockCampaign,
                splashInfo: mockSplashInfo,
                freeBetToken: '123456789'
            };
            component.initOverlay(campaignData);
            expect(component.soundSelected).toBeTruthy();
            expect(component.getDomAccessors).toHaveBeenCalled();
            expect(component['rendererService'].renderer.setStyle).toHaveBeenCalled();
            expect(freeRideDomService.appendDomElems).toHaveBeenCalled();
            expect(freeRideDomService.createDOMElements).toHaveBeenCalled();
            expect(component.displayQuestionNumber).toHaveBeenCalledWith(1);

        });
    });

    describe('getDomAccessors', () => {
        it('should get Dom Accessors', () => {
            component.getDomAccessors();
            expect(windowRef.document.querySelector).toHaveBeenCalledWith('html');
            expect(windowRef.document.querySelector).toHaveBeenCalledWith('#freeRideOverlay');
            expect(windowRef.document.querySelector).toHaveBeenCalledWith('.content-area');
            expect(windowRef.document.querySelector).toHaveBeenCalledWith('.loadingChat');
            expect(windowRef.document.querySelector).toHaveBeenCalledWith('.mainImage');
            expect(windowRef.document.querySelector).toHaveBeenCalledWith('.headingImage');
            expect(windowRef.document.querySelector).toHaveBeenCalledWith('.bannerContainer');
            expect(windowRef.document.querySelector).toHaveBeenCalledWith('source');

        });
    });

    describe('displayOptionsList', () => {
        it('should display displayOptionsList', fakeAsync(() => {
             component.overlayContentArea = {
                scrollIntoView: () => { }
            };
            component.questions = mockQuestions;
            component.soundSelected = true;
            spyOn(component, 'bindEvent');
            component.displayOptionsList(1);
            expect(freeRideDomService.appendDomElems).toHaveBeenCalledTimes(4);
            expect(freeRideDomService.createDOMElements).toHaveBeenCalled();
            //expect(el).toHaveBeenCalledWith(component.overlayContentArea);
        }));

        it('should not call appendDomElems if stepNum is not provided', fakeAsync(() => {
            component.questions = mockQuestions;
            component.soundSelected = true;
            spyOn(component, 'bindEvent');
            component.displayOptionsList();
            expect(freeRideDomService.appendDomElems).not.toHaveBeenCalledTimes(4);
            expect(freeRideDomService.createDOMElements).not.toHaveBeenCalled();
        }));
    });

    describe('display Additional Msg', () => {
        it('should display AdditionalMsg', fakeAsync(() => {
            spyOn(component, 'executeCallback');
            component.soundSelected = true;
            component.displayAdditionalMsg('Mock msg');
            expect(freeRideDomService.createDOMElements).toHaveBeenCalled();
            tick(1000);
            expect(component.executeCallback).toHaveBeenCalled();
        }));
    });

    describe('displaySavedDetailsMsg', () => {
        it('should call playSound if soundSelected true', () => {
            spyOn(component, 'executeCallback');
            component.displaySavedDetailsMsg();
            expect(component.executeCallback).toHaveBeenCalled();
        });
    });

    describe('displayResultMsg', () => {
        it('should display Result Msg', fakeAsync(() => {
            spyOn(component, 'executeCallback');
            component.displayResultMsg(mockHorseData);
            tick(2000);
            expect(component['rendererService'].renderer.setStyle).toHaveBeenCalled();
            expect(component.executeCallback).toHaveBeenCalled();
        }));
        it('should call renderer.setStyle', fakeAsync(() => {
            const mockHorseDetails = {
                horseName: 'HorseNametest',
                jockeyName: 'JockeyNameXYZ',
                raceName: '(USA) Club Hipico',
                raceTime: '18:21',
                categoryName: 'Horse Racing',
                typeName: '(USA) Club Hipico',
                name: '18:21 Club Hipico',
                className: 'Horse Racing - Live',
                eventId: '8208340'
            };
            spyOn(component, 'executeCallback');
            component.displayResultMsg(mockHorseDetails);
            tick(2000);
            expect(component['rendererService'].renderer.setStyle).toHaveBeenCalled();
            expect(component.executeCallback).toHaveBeenCalled();
        }));
    });

    describe('storeSelectedData', () => {
        it('should call storeSelectedData "Surprise Me" ', () => {
            spyOn(component, 'optionSelected');
            component.userAnswers = [];
            component.userAnswers.length = 0;
            component['optionsList'] = jasmine.createSpy();

            const evt = {
                'currentTarget': {
                    'innerText': 'Surprise Me'
                }
            };
            const elem = {
                id: '1'
            };
            const questionsData = {
                options: { optionId: 1 },
                questionId: 1
            };
            component.storeSelectedData(evt, elem, questionsData);
            expect(component.optionSelected).toHaveBeenCalled();
            expect(component['optionsList']).toHaveBeenCalled();
        });
        it('should call storeSelectedData "Surprise Me" & optionSet 1 and set the userAnswers', () => {
            spyOn(component, 'optionSelected');
            component['optionsList'] = jasmine.createSpy();
            component.userAnswers =[
                { questionId: 1, optionId: 1 },
                { questionId: 102, optionId: 2 },
                { questionId: 103, optionId: 3 }
            ];
            const evt = {
                'currentTarget': {
                    'innerText': 'Surprise Me'
                }
            };
            const elem = {
                id: '1'
            };
            const questionsData = {
                options: { optionId: 1 },
                questionId: 1
            };
            component.storeSelectedData(evt, elem, questionsData);
            expect(component.optionSelected).toHaveBeenCalled();
            expect(component['optionsList']).toHaveBeenCalled();
        });
    });

    describe('updateOverlayDisplay', () => {
        it('should update Overlay Display False', () => {
            component.updateOverlayDisplay(false);
            expect(component['rendererService'].renderer.removeClass).toHaveBeenCalledTimes(2);
        });
        it('should update Overlay Display', () => {
            component.updateOverlayDisplay(true);
            expect(component['rendererService'].renderer.addClass).toHaveBeenCalled();
        });
    });

    describe('showLoading', () => {
        it('should not showLoading', () => {
            component.showLoading(false);
            expect(component['rendererService'].renderer.addClass).toHaveBeenCalled();
        });
        it('should showLoading ', () => {
            component.showLoading(true);
            expect(component['rendererService'].renderer.removeClass).toHaveBeenCalled();
        });
    });

    describe('optionSelected', () => {
        it('should return optionSelected ', () => {
            spyOn(component['audioPlayerRef'].nativeElement, 'load');
            spyOn(component['audioPlayerRef'].nativeElement, 'play').and.returnValue({ catch: jasmine.createSpy() });
            spyOn(component, 'showLoading');
            spyOn(component, 'displayQuestionNumber');
            component.soundSelected = true;
            component.optionSelected('Mock Msh', 1);
            expect(windowRef.document.querySelector).toHaveBeenCalledWith('.optionContainer');
            expect(component.showLoading).toHaveBeenCalled();
            expect(component.displayQuestionNumber).toHaveBeenCalled();
        });
        it('should not call playSound if soundSeleted is false ', () => {
            spyOn(component['audioPlayerRef'].nativeElement, 'load');
            spyOn(component['audioPlayerRef'].nativeElement, 'play').and.returnValue({ catch: jasmine.createSpy() });
            spyOn(component, 'showLoading');
            spyOn(component, 'displayQuestionNumber');
            spyOn(component, 'playSound');
            component.soundSelected = false;
            component.optionSelected('Mock Msh', 1);
            expect(windowRef.document.querySelector).toHaveBeenCalledWith('.optionContainer');
            expect(component.showLoading).toHaveBeenCalled();
            expect(component.playSound).not.toHaveBeenCalled();
            expect(component.displayQuestionNumber).toHaveBeenCalled();

        });
        it('should not call displayQuestionNumber if quesSetNum is greator than 5', () => {
           // spyOn(component['audioPlayerRef'].nativeElement, 'load');
          //  spyOn(component['audioPlayerRef'].nativeElement, 'play').and.returnValue({ catch: jasmine.createSpy() });
            spyOn(component, 'showLoading');
            spyOn(component, 'displayQuestionNumber');
            component.soundSelected = true;
            component.optionSelected('Mock Msh', 6, 1);
            expect(windowRef.document.querySelector).toHaveBeenCalledWith('.optionContainer');
            expect(component.showLoading).toHaveBeenCalled();
        });
    });

    describe('destroyOverlay', () => {
        it('should destroyOverlay', fakeAsync(() => {
           const callbackHandler = jasmine.createSpy('callbackHandler');

           component.freeRideClose.subscribe(callbackHandler);
            
            component.destroyOverlay();
            tick();
            
            expect(callbackHandler).toHaveBeenCalled();
        }));
    });

    describe('sendUserSelectedAnswers', () => {
        it('should check if campaign is active', fakeAsync(() => {
            component['freeRideHelperService'].getFreeRideActiveCampaign = jasmine.createSpy().and.returnValue(of(mockCampaign));
            component['freeRideService'].requestSelectedHorse = jasmine.createSpy().and.returnValue(of(mockHorseData));
            component['freeRideService'].clearFreebet = jasmine.createSpy();
            spyOn(component, 'displayResultMsg');
            component.sendUserSelectedAnswers(mockSelectionRequestData);
            tick();
            expect(component['freeRideHelperService'].getFreeRideActiveCampaign).toHaveBeenCalled();
            expect(component['freeRideService'].requestSelectedHorse).toHaveBeenCalled();
        }));
        it('show error message if campaign is inactive', fakeAsync(() => {
            component['freeRideHelperService'].getFreeRideActiveCampaign = jasmine.createSpy().and.returnValue(undefined);
            spyOn(component, 'showResultantEventError');

            component.sendUserSelectedAnswers(mockSelectionRequestData);
            tick();
            expect(component['freeRideHelperService'].getFreeRideActiveCampaign).toHaveBeenCalled();
            expect(component['freeRideService'].requestSelectedHorse).not.toHaveBeenCalled();
        }));
        it('should sendUserSelectedAnswers', fakeAsync(() => {
            component['freeRideHelperService'].getFreeRideActiveCampaign = jasmine.createSpy().and.returnValue(of(mockCampaign));
            component['freeRideService'].requestSelectedHorse = jasmine.createSpy().and.returnValue(of(mockHorseSel));
            component['freeRideService'].clearFreebet = jasmine.createSpy();
            spyOn(component, 'displayResultMsg');
            spyOn(component, 'showResultantEventError');
            component.sendUserSelectedAnswers(mockSelectionRequestData);
            tick();
            expect(component['freeRideService'].requestSelectedHorse).toHaveBeenCalled();
            expect(component.displayResultMsg).toHaveBeenCalled();
            expect(pubsubService.publish).toHaveBeenCalled();
            expect(component.selectedHorseDetails).toEqual(mockHorseSel);
        }));
        it('should showResultantEventError if berError exist in response', fakeAsync(() => {
            const mockHorseSelErr = {
                horseName: 'ABC',
                jockeyName: 'XYZ',
                raceName: 'Cheltenham',
                raceTime: 'xx:xx',
                silkUrl: 'string',
                categoryName: 'string',
                typeName: '((USA) Club Hipico)',
                name: '(18:21 Club Hipico)',
                className: '(Horse Racing - Live)',
                eventId: '(8208340)',
                errMsg: 'errMsg',
                betError: [{ msg: ' msg' }]
            };
            component['freeRideHelperService'].getFreeRideActiveCampaign = jasmine.createSpy().and.returnValue(of(mockCampaign));
            component['freeRideService'].requestSelectedHorse = jasmine.createSpy().and.returnValue(of(mockHorseSelErr));
            spyOn(component, 'showResultantEventError');
            component.sendUserSelectedAnswers(mockSelectionRequestData);
            tick();
            expect(component['freeRideService'].requestSelectedHorse).toHaveBeenCalled();
            expect(component.showResultantEventError).toHaveBeenCalled();
        }));
        it('should showResultantEventError if get error from freeRideService', fakeAsync(() => {
            component['freeRideService'].requestSelectedHorse = jasmine.createSpy().and.returnValue(throwError('error'));
            spyOn(component, 'showResultantEventError');
            component.sendUserSelectedAnswers(mockSelectionRequestData);
            tick();
            expect(component.showResultantEventError).toHaveBeenCalled();
        }));
        it('should showResultantEventError if get error from freeRideService', fakeAsync(() => {
            component['freeRideHelperService'].getFreeRideActiveCampaign = jasmine.createSpy().and.returnValue(of(mockCampaign));
            component['freeRideService'].requestSelectedHorse = jasmine.createSpy().and.returnValue(throwError('error'));
            spyOn(component, 'showResultantEventError');
            component.sendUserSelectedAnswers(mockSelectionRequestData);
            tick();
            expect(component.showResultantEventError).toHaveBeenCalled();
        }));
    });

    describe('bindEvent', () => {
        it('should call goToEdpPage', () => {
            spyOn(component, 'storeSelectedData');
            spyOn(component, 'goToEdpPage');
            const elem = { className: 'ctaBtn' };
            component.bindEvent('click', elem, mockOptions);
            expect(component['rendererService'].renderer.listen).toHaveBeenCalled();
            expect(component.goToEdpPage).toHaveBeenCalled();
        });
        it('should call storeSelectedData', () => {
            spyOn(component, 'storeSelectedData');
            spyOn(component, 'goToEdpPage');
            const elem = { className: 'abc' };
            component.bindEvent('click', elem, mockOptions);
            expect(component['rendererService'].renderer.listen).toHaveBeenCalled();
            expect(component.storeSelectedData).toHaveBeenCalled();
        });
    });

    describe('displayQuestionNumber', () => {
        it('should display Question Number 1', () => {
            component.questions = mockQuestions;
            spyOn(component, 'displayAdditionalMsg');
            spyOn(component, 'executeCallback');
            component.displayQuestionNumber(1);
            expect(component.executeCallback).toHaveBeenCalledWith(3600, jasmine.any(Function), 'Question 1', 1);
            expect(component.displayAdditionalMsg).toHaveBeenCalled();
        });
        it('should display Question Number 2', () => {
            component.questions = mockQuestions;
            spyOn(component, 'displayAdditionalMsg');
            spyOn(component, 'executeCallback');
            spyOn(component, 'updateOverlayDisplay');
            component.displayQuestionNumber(2);
            expect(component.displayAdditionalMsg).toHaveBeenCalled();
            expect(component.updateOverlayDisplay).toHaveBeenCalledWith(true);
            expect(component.executeCallback).toHaveBeenCalledWith(3600, jasmine.any(Function), 'Question 2', 2);
        });
        it('should display Question Number 3', () => {
            component.questions = mockQuestions;
            spyOn(component, 'displayAdditionalMsg');
            spyOn(component, 'executeCallback');
            component.displayQuestionNumber(3);

            expect(component.displayAdditionalMsg).toHaveBeenCalled();
            expect(component.executeCallback).toHaveBeenCalledWith(3600, jasmine.any(Function), 'Question 2', 3);
        });
        it('should display Question Number 4', () => {
            component.questions = mockQuestions;
            spyOn(component, 'displaySavedDetailsMsg');
            spyOn(component, 'sendUserSelectedAnswers');
            spyOn(component, 'displayAdditionalMsg');
            spyOn(component, 'executeCallback');
            component.displayQuestionNumber(4);
            component.userAnswers = [];
            expect(component.displayAdditionalMsg).toHaveBeenCalledWith('Great choice');
            expect(component.displaySavedDetailsMsg).toHaveBeenCalled();
            expect(component.sendUserSelectedAnswers).toHaveBeenCalledWith(component.buildResponse());
        });
        it('should not call any method by default', () => {
            component.questions = mockQuestions;
            spyOn(component, 'displayAdditionalMsg');
            spyOn(component, 'displaySavedDetailsMsg');
            spyOn(component, 'sendUserSelectedAnswers');
            component.displayQuestionNumber(0);
            component.userAnswers = [];
            expect(component.displayAdditionalMsg).not.toHaveBeenCalled();
            expect(component.displaySavedDetailsMsg).not.toHaveBeenCalled();
            expect(component.sendUserSelectedAnswers).not.toHaveBeenCalled();
        });
    });

    describe('displayQuestion', () => {
        it('should display Question', () => {
            spyOn(component, 'showLoading');
            spyOn(component, 'playSound');
            spyOn(component, 'executeCallback');
            component.soundSelected = true;
            component.questions = mockQuestions;
            component.displayQuestion('Mock msg', 1);
            expect(component.showLoading).toHaveBeenCalled();
            expect(component.playSound).toHaveBeenCalled();
        });
        it('should not play Soud if soundSelected is false', () => {
            spyOn(component, 'showLoading');
            spyOn(component, 'playSound');
            spyOn(component, 'executeCallback');
            component.soundSelected = false;
            component.questions = mockQuestions;
            component.displayQuestion('Mock msg', 1);
            expect(component.showLoading).toHaveBeenCalled();
            expect(component.playSound).not.toHaveBeenCalled();
        });
    });

    describe('buildEdpUrl', () => {
        it('should call routingHelperService.formEdpUrl', () => {
            component.selectedHorseDetails = mockHorseData;
            const eventEntity: IRoutingHelperEvent | ISportEvent = {
                categoryId: '21',
                categoryName: 'Horse Racing',
                typeName: component.selectedHorseDetails.name.substring(6),
                name: component.selectedHorseDetails.name,
                className: component.selectedHorseDetails.className,
                id: component.selectedHorseDetails.eventId
            };
            component.buildEdpUrl();
            expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith(eventEntity);
        });
    });

    describe('goToEdpPage', () => {
        it('should call router.navigateByUrl', () => {
            const spyBuildEdpUrl = spyOn(component, 'buildEdpUrl');
            component['ctaEvent'] = jasmine.createSpy();
            component.goToEdpPage();
            expect(router.navigateByUrl).toHaveBeenCalledWith(spyBuildEdpUrl());
        });
    });

    describe('executeCallback', () => {
        it('should call indowRef.nativeWindow.setTimeout', () => {
            component.executeCallback(0, () => { }, []);
            expect(windowRef['nativeWindow'].setTimeout).toHaveBeenCalled();
        });
        it('should call indowRef.nativeWindow.setTimeout with value other than 0', () => {
            component.executeCallback(1, () => { }, []);
            expect(windowRef['nativeWindow'].setTimeout).toHaveBeenCalled();
        });
    });

    describe('showResultantEventError', () => {
        it('should call showLoading', () => {
            spyOn(component, 'showLoading');
            component.showResultantEventError();
            expect(component.freeRideError).toBeTruthy();
            expect(component.showLoading).toHaveBeenCalled();
        });
    });

    describe('closeErrorMessage', () => {
        it('should set freeRideError falsy', () => {
            spyOn(component, 'showLoading');
            const mouseEvent: any = {
                preventDefault: jasmine.createSpy()
            };
            component.closeErrorMessage(mouseEvent);
            expect(component.freeRideError).toBeFalsy();
        });
    });

    describe('displayCTAButton', () => {
        it('should call playSound method', () => {
            const el = {
                scrollIntoView: () => { }
            };
            spyOn(component, 'showLoading');
            component.soundSelected = true;
            spyOn(component, 'playSound');
            spyOn(component, 'bindEvent');
            component.displayCTAButton(el);
            expect(freeRideDomService.createDOMElements).toHaveBeenCalled();
            expect(component.showLoading).toHaveBeenCalled();
            expect(freeRideDomService.appendDomElems).toHaveBeenCalled();
            expect(component.playSound).toHaveBeenCalled();
        });
        it('should not call playSound method', () => {
            const el = {
                scrollIntoView: () => { }
            };
            spyOn(component, 'showLoading');
            component.soundSelected = false;
            spyOn(component, 'playSound');
            spyOn(component, 'bindEvent');
            component.displayCTAButton(el);
            expect(freeRideDomService.createDOMElements).toHaveBeenCalled();
            expect(component.showLoading).toHaveBeenCalled();
            expect(freeRideDomService.appendDomElems).toHaveBeenCalled();
            expect(component.playSound).not.toHaveBeenCalled();
        });
    });

    describe('showDetails', () => {
        it('should call playSound if soundSelected is true', () => {
            const el = {
                scrollIntoView: () => { }
            };
            component.overlayContentArea = {
                scrollIntoView: () => { }
            };
            spyOn(component, 'playSound');
            component.soundSelected = true;
            component.showDetails(el);
            expect(freeRideDomService.appendDomElems).toHaveBeenCalled();
            expect(component.playSound).toHaveBeenCalled();
        });
        it('should not call playSound if soundSelected is false', () => {
            const el = {
                scrollIntoView: () => { }
            };
            component.overlayContentArea = {
                scrollIntoView: () => { }
            };

            spyOn(component, 'playSound');
            component.soundSelected = false;
            component.showDetails(el);
            expect(freeRideDomService.appendDomElems).toHaveBeenCalled();
            expect(component.playSound).not.toHaveBeenCalled();
        });
        it('should not call playSound if soundSelected is false', () => {
            const el = {
                scrollIntoView: () => { }
            };
            component.overlayContentArea = {
                scrollIntoView: () => { }
            };

            spyOn(component, 'playSound');
            spyOn(component, 'showLoading');
            component.soundSelected = false;
            component.showDetails(el, true);
            expect(freeRideDomService.appendDomElems).toHaveBeenCalled();
            expect(component.playSound).not.toHaveBeenCalled();
            expect(component.showLoading).toHaveBeenCalledWith(true);
        });
        it('should not call playSound if soundSelected is false', () => {
            const el = {
                scrollIntoView: () => { }
            };
            component.overlayContentArea = {
                scrollIntoView: () => { }
            };

            spyOn(component, 'playSound');
            spyOn(component, 'showLoading');
            component.soundSelected = false;
            component.showDetails(el, false);
            expect(freeRideDomService.appendDomElems).toHaveBeenCalled();
            expect(component.playSound).not.toHaveBeenCalled();
            expect(component.showLoading).toHaveBeenCalledWith(false);
        });
    });

    describe('playSound', () => {
        it('should  call  nativeElement.load and nativeElement.play ', () => {
            spyOn(component['audioPlayerRef'].nativeElement, 'load');
            spyOn(component['audioPlayerRef'].nativeElement, 'play').and.returnValue({ catch: () => { throwError('error'); } });
            component.playSound('audioSource');
        });
        it('should  test quesAudioPlayerRef case ', () => {
            spyOn(component['audioPlayerRef'].nativeElement, 'load');
            spyOn(component['audioPlayerRef'].nativeElement, 'play').and.returnValue({ catch: () => { throwError('error'); } });
            const audioSource = component.quesAudioPlayerRef;
            component.playSound(audioSource);
            expect(component.quesAudioPlayerRef.nativeElement.play).toHaveBeenCalled();
        });
        it('should  test resultAudioPlayerRef case ', () => {
            spyOn(component['audioPlayerRef'].nativeElement, 'load');
            spyOn(component['audioPlayerRef'].nativeElement, 'play').and.returnValue({ catch: () => { throwError('error'); } });
            const audioSource = component.resultAudioPlayerRef;
            component.playSound(audioSource);
            expect(component.resultAudioPlayerRef.nativeElement.play).toHaveBeenCalled();
        });
    });
});