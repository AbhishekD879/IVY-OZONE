import {
    FiveasideWelcomeOverlayComponent
} from '@app/fiveASideShowDown/components/fiveASideWelcomeOverlay/fiveaside-welcome-overlay.component';
import { welcome_mock } from '@app/fiveASideShowDown/components/fiveASideWelcomeOverlay/fiveaside-welcome-overlay.mock';
import { of, throwError } from 'rxjs';
import { welcome_GA_Tag } from '@app/fiveASideShowDown/constants/constants';

describe('FiveasideWelcomeOverlayComponent', () => {
    let component: FiveasideWelcomeOverlayComponent;
    let rendererService,
        domSanitizer,
        cmsService,
        windowRefService,
        deviceService, gtmService, changeDetectorRef;
    beforeEach(() => {
        rendererService = {
            renderer: {
                addClass: jasmine.createSpy('addClass'),
                removeClass: jasmine.createSpy('removeClass')
            }
        };
        domSanitizer = {
            sanitize: jasmine.createSpy().and.returnValue('test'),
            bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml'),
            bypassSecurityTrustResourceUrl: jasmine.createSpy().and.returnValue('testUrl')
        };
        gtmService = {
            push: jasmine.createSpy('push')
        };
        cmsService = {
            getWelcomeOverlay: jasmine.createSpy('getWelcomeOverlay').and.returnValue(of(welcome_mock)),
        };
        windowRefService = {
            document: {
                querySelector: jasmine.createSpy('querySelector'),
                getElementById: jasmine.createSpy('getElementById'),
                getElementsByTagName: jasmine.createSpy('getElementsByTagName'),
            },
            nativeWindow: {
                localStorage: {
                    clear: jasmine.createSpy('clear'),
                    setItem: jasmine.createSpy('setItem'),
                    getItem: jasmine.createSpy('getItem').and.returnValue(true)
                },
            }
        };
        deviceService = {
            isWrapper: true
        } as any;
        changeDetectorRef = {
            detectChanges: jasmine.createSpy('detectChanges')
        };
        component = new FiveasideWelcomeOverlayComponent(
            cmsService,
            rendererService,
            windowRefService,
            deviceService,
            domSanitizer,
            gtmService,
            changeDetectorRef
        );
        component.clearOverlay.emit = jasmine.createSpy('modelChangeHandler.emit');
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should fetch cms data in ngOnInit', () => {
        spyOn(component as any, 'checkOverlayDisplayed');
        component.ngOnInit();
        expect(component['showdownOverlay']).toBe(true);
    });

    it('should check for overlay is seen', () => {
        spyOn(component as any, 'checkOverlayDisplayed');
        windowRefService.nativeWindow.localStorage.getItem = jasmine.createSpy('showdownOverlay').and.returnValue(true);
        component.ngOnInit();
        expect(component['showdownOverlay']).toBe(true);
    });
    it('should check for overlay is not seen', () => {
        spyOn(component as any, 'checkOverlayDisplayed');
        windowRefService.nativeWindow.localStorage.getItem = jasmine.createSpy('showdownOverlay').and.returnValue(false);
        component.ngOnInit();
    });

    it('should call get started ga tag', () => {
        component.getStartedClick();
        expect(gtmService.push).toHaveBeenCalledWith('trackEvent', welcome_GA_Tag.getStartedGa);
    });

    describe('checkOverlayDisplayed', () => {
        it('when showdownOverlay is true', () => {
            component['showdownOverlay'] = true;
            component['checkOverlayDisplayed']();
        });
        it('when showdownOverlay is false', () => {
            spyOn(component as any, 'getWelcomeOverlayCMS');
            spyOn(component as any, 'initOverlayElements');
            spyOn(component as any, 'validateBaseElement');
            component['showdownOverlay'] = false;
            component['checkOverlayDisplayed']();
        });
    });

    describe('#onCloseRulesOverlay', () => {
        it('should close rules overlay', () => {
            component.onCloseWelcomeOverlay();
            expect(rendererService.renderer.removeClass).toHaveBeenCalledWith(undefined, 'active');
        });
    });

    describe('#getWelcomeOverlayCMS', () => {
        it('should map cms data, if you get response', () => {
            component['getWelcomeOverlayCMS']();
            expect(component.welcomeCard).not.toBeNull();
        });
        it('should not map cms data, if you get no response', () => {
            cmsService.getWelcomeOverlay.and.returnValue(of(null));
            component['getWelcomeOverlayCMS']();
            expect(component.welcomeCard).toEqual(null);
        });
        it('should not map cms data, if you get error response', () => {
            cmsService.getWelcomeOverlay.and.returnValue(throwError({ status: 404 }));
            component['getWelcomeOverlayCMS']();
            expect(component.welcomeCard).toBeUndefined();
        });
    });

    describe('#getPreEvent', () => {
        it('should check for pre event', () => {
            component['getPreEvent']();
            expect(rendererService.renderer.removeClass).toHaveBeenCalledWith(undefined, 'active');
        });
    });

    describe('#initOverlayElements', () => {
        it('should init rules overlay', () => {
            component['initOverlayElements']();
            expect(rendererService.renderer.addClass).toHaveBeenCalledWith(undefined, 'active');
        });
    });

    describe('#validateBaseElement', () => {
        it('should handle when base class is available', () => {
            component.baseClass = 'welcome';
            component['validateBaseElement']();
            expect(windowRefService.document.querySelector).toHaveBeenCalledWith('welcome');
        });
        it('should handle when base class is not available, and is wrapper', () => {
            component['validateBaseElement']();
            expect(windowRefService.document.querySelector).toHaveBeenCalledWith('body');
        });
        it('should handle when base class is not available, and is wrapper false', () => {
            deviceService.isWrapper = false;
            component['validateBaseElement']();
            expect(windowRefService.document.querySelector).toHaveBeenCalledWith('html, body');
        });
    });


    describe('#lobbyTutorialTrigger', () => {
        it('should call startLobbyOverlay method', () => {
            spyOn(component as any, 'checkOverlayDisplayed');
            component.lobbyTutorial = true;
            component['lobbyTutorialTrigger']();
            expect(component['checkOverlayDisplayed']).toHaveBeenCalled();
        });

        it('should not call startLobbyOverlay method', () => {
            spyOn(component as any, 'checkOverlayDisplayed');
            component.lobbyTutorial = false;
            component['lobbyTutorialTrigger']();
            expect(component['checkOverlayDisplayed']).not.toHaveBeenCalled();
        });

        it('should call startLobbyOverlay method', () => {
            spyOn(component as any, 'startLobbyOverlay');
            component.lobbyTutorial = false;
            component['welcomeOverlaySeen'] = true;
            component.currentOverlay = 'LOBBY';
            component['lobbyTutorialTrigger']();
            expect(component['startLobbyOverlay']).toHaveBeenCalled();
        });

        it('should not call startLobbyOverlay method', () => {
            spyOn(component as any, 'startLobbyOverlay');
            component.lobbyTutorial = false;
            component['welcomeOverlaySeen'] = true;
            component.currentOverlay = 'PRE-EVENT';
            component['lobbyTutorialTrigger']();
            expect(component['startLobbyOverlay']).not.toHaveBeenCalled();
        });

        it('should not call startLobbyOverlay method', () => {
            spyOn(component as any, 'startLobbyOverlay');
            component.lobbyTutorial = false;
            component['welcomeOverlaySeen'] = false;
            component.currentOverlay = 'LOBBY';
            component['lobbyTutorialTrigger']();
            expect(component['startLobbyOverlay']).not.toHaveBeenCalled();
        });
    });

    describe('#liveTutorialTrigger', () => {
        it('should call liveTutorialTrigger method', () => {
            spyOn(component as any, 'checkOverlayDisplayed');
            component.liveTutorial = true;
            component['liveTutorialTrigger']();
            expect(component['checkOverlayDisplayed']).toHaveBeenCalled();
        });

        it('should not call liveTutorialTrigger method', () => {
            spyOn(component as any, 'checkOverlayDisplayed');
            component.liveTutorial = false;
            component['liveTutorialTrigger']();
            expect(component['checkOverlayDisplayed']).not.toHaveBeenCalled();
        });

        it('should not call startLiveEventOverlay method', () => {
            spyOn(component as any, 'startLiveEventOverlay');
            component.lobbyTutorial = false;
            component['welcomeOverlaySeen'] = true;
            component.currentOverlay = 'LOBBY';
            component['liveTutorialTrigger']();
            expect(component['startLiveEventOverlay']).not.toHaveBeenCalled();
        });

        it('should call startLiveEventOverlay method', () => {
            spyOn(component as any, 'startLiveEventOverlay');
            component.lobbyTutorial = false;
            component['welcomeOverlaySeen'] = true;
            component.currentOverlay = 'LIVE-EVENT';
            component['liveTutorialTrigger']();
            expect(component['startLiveEventOverlay']).toHaveBeenCalled();
        });

        it('should not call startLiveEventOverlay method', () => {
            spyOn(component as any, 'startLiveEventOverlay');
            component.lobbyTutorial = false;
            component['welcomeOverlaySeen'] = false;
            component.currentOverlay = 'LOBBY';
            component['liveTutorialTrigger']();
            expect(component['startLiveEventOverlay']).not.toHaveBeenCalled();
        });
    });

    describe('#startLobbyOverlay', () => {
        it('should close rules overlay and open lobby overlay', () => {
            component.startLobbyOverlay();
            expect(rendererService.renderer.removeClass).toHaveBeenCalled();
        });
    });

    describe('#startLiveEventOverlay', () => {
        it('should close rules overlay and open lobby overlay', () => {
            component.startLiveEventOverlay();
            expect(rendererService.renderer.removeClass).toHaveBeenCalled();
        });
    });
    it('#iframeLoaded check for iframe loaded', () => {
        component.iframeLoaded();
        expect(component.showImage).toBe(true);
    });

    describe('#getStartedClick', () => {
        it('should call startLobbyOverlay', () => {
            component.currentOverlay = 'LOBBY';
            spyOn(component, 'startLobbyOverlay');
            component.getStartedClick();
            expect(component.startLobbyOverlay).toHaveBeenCalled();
            expect(component.videoPlayer).toBe(false);
        });

        it('should call getPreEvent', () => {
            component.currentOverlay = 'PREEVENT';
            spyOn(component, 'getPreEvent');
            component.getStartedClick();
            expect(component.getPreEvent).toHaveBeenCalled();
            expect(component.videoPlayer).toBe(false);
        });

        it('should call startLiveEventOverlay', () => {
            component.currentOverlay = 'LIVE-EVENT';
            spyOn(component, 'startLiveEventOverlay');
            component.getStartedClick();
            expect(component.startLiveEventOverlay).toHaveBeenCalled();
            expect(component.videoPlayer).toBe(false);
        });

        it('should call not startLobbyOverlay', () => {
            component.currentOverlay = 'ABC';
            spyOn(component, 'startLobbyOverlay');
            component.getStartedClick();
            expect(component.startLobbyOverlay).not.toHaveBeenCalled();
            expect(component.videoPlayer).toBe(true);
        });
    });
});
