import { ImgScoreboardProviderComponent } from '@edp/components/imgArenaScoreboard/components/img-scoreboard-provider.component';
import { of } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';
import * as md5 from 'blueimp-md5';

describe('ImgScoreboardProviderComponent', () => {
    let component: ImgScoreboardProviderComponent;
    let ngZone, asyncScriptLoaderFactory, windowRef, activatedRoute, timeSyncService, imgEventCenter, userService, cmsService, deviceService;
    beforeEach(() => {
        ngZone = {
            runOutsideAngular: jasmine.createSpy('runOutsideAngular'),
        };
        windowRef = {
            nativeWindow: {
                frontRowSeat: {
                    eventCentreUtils: jasmine.createSpy('frontRowSeat.eventCentreUtils'),
                    eventCentre: jasmine.createSpy().and.returnValue({
                        on: jasmine.createSpy(),
                        emit: jasmine.createSpy()
                    })
                }
            }
        };
        asyncScriptLoaderFactory = {
            loadJsFile: jasmine.createSpy().and.returnValue(of(null))
        };
        activatedRoute = {
            snapshot: {
                paramMap: {
                    get: jasmine.createSpy('paramMap.get').and.returnValue('golf')
                }
            },
            params: of({
                sport: 'golf',
                id: '18'
            })
        };
        timeSyncService = {
            getUserSessionTime: jasmine.createSpy().and.returnValue(of({
                'timestamp': 1642393233124,
                'x-forward-for': '103.115.128.202'
            }))
        };
        deviceService = {
            requestPlatform: 'desktop'
        }
        cmsService = {
            getSystemConfig: jasmine.createSpy().and.returnValue(of({
                IMGScoreboardHoleStreaming: {
                    'desktop': true,
                    'mobile': true,
                    'tablet': false
                }
            }
            ))
        };
        userService = {
            status: false
        };
        windowRef.nativeWindow.frontRowSeat.eventCentreUtils = {
            "MessageTopics": {
                "VIDEO_PLAYBACK_AUTH_REQUEST": "video-playback-auth-request",
                "VIDEO_PLAYBACK_AUTH_RESPONSE": "video-playback-auth-response"
            }
        };
        imgEventCenter = {
            sport: 'golf',
            targetModule: "full",
            version: "5.x",
            language: "en",
            targetElementSelector: "#img-arena-event-centre",
            operator: environment.DOMAIN.includes('coral') ? 'coral' : 'ladbrokes',
            eventId: '123',
            options: {
                videoPlaybackEnabled: false
            },
            initialContext: {
                view: "GroupDetail",
                roundNo: '9',
                groupNo: '8',
                holeNo: '7'
            }
        };
        component = new ImgScoreboardProviderComponent(
            ngZone,
            windowRef,
            asyncScriptLoaderFactory,
            timeSyncService,
            activatedRoute,
            userService,
            cmsService,
            deviceService
        );
    });

    it('constructor', () => {
        expect(component).toBeTruthy();
    });

    describe('initImgScoreBoardLoader', () => {
        beforeEach(() => {
            spyOn<any>(component, 'addImgScoreBoard');
            component['IMG_ARENA_SCOREBOARD'] = 'https://unpkg.com/@img-arena/front-row-seat';
        });
        it('should call addImgScoreBoard if img front row arena unpkg is called', () => {
            component['initImgScoreBoardLoader']();
            expect(asyncScriptLoaderFactory.loadJsFile).toHaveBeenCalledWith(component['IMG_ARENA_SCOREBOARD']);
            expect(component['addImgScoreBoard']).toHaveBeenCalled();
        });
    });

    describe('Operator Check if Coral', () => {
        beforeEach(() => {
            environment.DOMAIN = 'coral.co.uk';
        });
        it('IMG Opertaor is coral', () => {
            component['imgEventDetails'] = '123:9:8:7';
            component['addImgScoreBoard']();
            expect(component['imgEventCenter']['operator']).toEqual('coral');
            expect(component['imgEventCenter']['operator']).not.toEqual('ladbrokes');
        });
    });

    describe('Operator Check if ladbrokes', () => {
        beforeEach(() => {
            environment.DOMAIN = 'ladbrokes.com';
        });
        it('IMG Opertaor is ladbrokes', () => {
            component['imgEventDetails'] = '123:9:8:7';
            component['addImgScoreBoard']();
            expect(component['imgEventCenter']['operator']).toEqual('ladbrokes');
            expect(component['imgEventCenter']['operator']).not.toEqual('coral');
        });
    });

    describe('add IMG Arena Scoreboard frontRowSeat defined', () => {
        it('IMG Arena Isomorphic Rendering frontRowSeat object defined', () => {
            spyOn<any>(component, 'addImgScoreBoard');
            component['loadImgScoreBoard']();
            expect(component.showImgScoreboardLoader).toEqual(true);
            expect(component['addImgScoreBoard']).toHaveBeenCalled();
        });
        it('If Sport is GOLF then Event Center Object matches and user is not logged in', () => {
            component['imgEventDetails'] = '123:9:8:7';
            component['addImgScoreBoard']();
            expect(component.showImgScoreboardLoader).toEqual(false);
            expect(component.showImgScoreboard).toEqual(true);
            expect(component.sportName).toEqual('golf');
            expect(component['imgEventCenter']).toEqual(imgEventCenter);
            expect(component['imgEventCenter']['options']['videoPlaybackEnabled']).toEqual(false);
            expect(component.isLoggedIn).toEqual(false);
        });
    });

    describe('If User is logged in ', () => {
        beforeEach(() => {
            userService = {
                status: true
            };
            component = new ImgScoreboardProviderComponent(
                ngZone,
                windowRef,
                asyncScriptLoaderFactory,
                timeSyncService,
                activatedRoute,
                userService,
                cmsService,
                deviceService
            );
            component['imgEventDetails'] = '123:9:8:7';
            component['addImgScoreBoard']();
        });
        it('Video Play back would be enabled', () => {
            expect(component['imgEventCenter']['options']['videoPlaybackEnabled']).toEqual(true);
            expect(component.isLoggedIn).toEqual(true);
        });
        it('User clicked on play button', () => {
            let requestlistener, responsereceiver;

            const eventCentreInstanceMock = {
                on: jasmine.createSpy('on'),
                emit: jasmine.createSpy('emit')
            };
            windowRef.nativeWindow.frontRowSeat.eventCentre.and.returnValue(eventCentreInstanceMock);

            eventCentreInstanceMock.on.and.callFake((action, handler) => {
                if (action === 'video-playback-auth-request') {
                    requestlistener = handler;
                }
            });

            eventCentreInstanceMock.emit.and.callFake((action, handler) => {
                if (action === 'video-playback-auth-response') {
                    responsereceiver = handler;
                }
            });
            component['addImgScoreBoard']();
            requestlistener();
            expect(eventCentreInstanceMock.on).toHaveBeenCalledTimes(1);
            expect(responsereceiver.operatorId).toBe(environment.IMG_ARENA_OPERATOR_ID);
            expect(responsereceiver.timestamp).toBe(1642393233124);
            const auth = md5(`${environment.IMG_ARENA_OPERATOR_SECRET_KEY}:103.115.128.202:1642393233124`, environment.IMG_ARENA_OPERATOR_SECRET_KEY);
            expect(responsereceiver.auth).toBe(auth);
        });
    });

    describe('Sport is not Golf', () => {
        beforeEach(() => {
            activatedRoute = {
                snapshot: {
                    paramMap: {
                        get: jasmine.createSpy('paramMap.get').and.returnValue('notGolf')
                    }
                },
                params: of({
                    sport: 'notGolf',
                    id: '99'
                })
            };
            component = new ImgScoreboardProviderComponent(
                ngZone,
                windowRef,
                asyncScriptLoaderFactory,
                timeSyncService,
                activatedRoute,
                userService,
                cmsService,
                deviceService
            );
        });
        it('If Sport is not GOLF then Event Center Object should be {}', () => {
            component['addImgScoreBoard']();
            expect(component.sportName).toEqual('notGolf');
            expect(component.showImgScoreboardLoader).toEqual(false);
            expect(component.showImgScoreboard).toEqual(false);
            expect(Object.keys(component['imgEventCenter']).length).toBe(1);
            expect(component['imgEventCenter']['options']).toBeUndefined();
        });
    });

    describe('loadImgScoreBoard for available frontRowSeat', () => {
        it('IMG Arena Isomorphic Rendering frontRowSeat object defined', () => {
            spyOn<any>(component, 'addImgScoreBoard');
            component['loadImgScoreBoard']();
            expect(windowRef.nativeWindow.frontRowSeat).toBeDefined();
            expect(component.showImgScoreboardLoader).toEqual(true);
            expect(component['addImgScoreBoard']).toHaveBeenCalled();
        });
    });

    describe('ngAfterViewInit', () => {
        it('ngAfterViewInit call for ngZone', () => {
            ngZone.runOutsideAngular.and.callFake(cb => cb());
            spyOn(component as any, 'loadImgScoreBoard').and.callFake(() => jasmine.createSpy());
            component.ngAfterViewInit();
            expect(component['loadImgScoreBoard']).toHaveBeenCalledTimes(1);
        });
    });

    describe('loadImgScoreBoard for initialising frontRowSeat', () => {
        beforeEach(() => {
            windowRef = {
                nativeWindow: {
                    frontRowSeat: undefined
                }
            };
            ngZone = {
                runOutsideAngular: jasmine.createSpy('runOutsideAngular'),
            };
            asyncScriptLoaderFactory = {
                loadJsFile: jasmine.createSpy().and.returnValue(of(null))
            };
            component = new ImgScoreboardProviderComponent(
                ngZone,
                windowRef,
                asyncScriptLoaderFactory,
                timeSyncService,
                activatedRoute,
                userService,
                cmsService,
                deviceService
            );
        });
        it('IMG Arena Isomorphic Rendering frontRowSeat object undefined before initialisation', () => {
            spyOn<any>(component, 'initImgScoreBoardLoader');
            component['loadImgScoreBoard']();
            expect(component.showImgScoreboardLoader).toEqual(true);
            expect(component['initImgScoreBoardLoader']).toHaveBeenCalled();
        });

        it('IMG Arena Isomorphic Rendering frontRowSeat object undefined', () => {
            component['addImgScoreBoard']();
            expect(windowRef.nativeWindow.frontRowSeat).toBeUndefined();
            expect(component.showImgScoreboardLoader).toEqual(false);
        });
    });

    describe('ngOnDestroy', () => {
        it('ngOnDestroy asyncLoaderSub', () => {
            component['asyncLoaderSub'] = <any>{
                unsubscribe: jasmine.createSpy('unsubscribe')
            };
            component.ngOnDestroy();
            expect(component['asyncLoaderSub'].unsubscribe).toHaveBeenCalled();
        });
    });
});