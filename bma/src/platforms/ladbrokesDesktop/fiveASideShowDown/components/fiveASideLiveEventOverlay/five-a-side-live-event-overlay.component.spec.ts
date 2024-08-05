import { FiveASideLiveEventOverlayComponent } from './five-a-side-live-event-overlay.component';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { of } from 'rxjs';
import { LIVE_OVERLAY } from '@app/fiveASideShowDown/constants/constants';

describe('FiveASideLiveEventOverlayComponent Desktop', () => {
    let component: FiveASideLiveEventOverlayComponent;
    let rendererService,
        domSanitizer,
        cmsService,
        windowRef,
        deviceService,
        gtmService,
        changeDetectorRef,
        pubsubService,
        coreToolsService;
    const boundFunc = () => ({ 'top': 50, 'left': 50, 'right': 50, 'bottom': '50' });

    beforeEach(() => {
        rendererService = {
            renderer: {
                addClass: jasmine.createSpy('addClass'),
                removeClass: jasmine.createSpy('removeClass'),
                setStyle: jasmine.createSpy('setStyle')
            }
        };
        domSanitizer = {
            sanitize: jasmine.createSpy().and.returnValue('test'),
            bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml')
        };
        coreToolsService = {
            uuid: jasmine.createSpy('uuid').and.returnValue('123abc')
        };
        cmsService = {
            getWelcomeOverlay: jasmine.createSpy('getWelcomeOverlay').and.returnValue(of({})),
        };
        pubsubService = {
            subscribe: jasmine.createSpy('subscribe'),
            unsubscribe: jasmine.createSpy('unsubscribe'),
            API: pubSubApi

        };
        windowRef = {
            document: {
                querySelector: { get: jasmine.createSpy() },
                querySelectorAll: { get: jasmine.createSpy() },
                getElementById: jasmine.createSpy('querySelector').and.returnValue({
                    parentNode: {}
                } as any)
            },
            nativeWindow: {
                scrollTo: jasmine.createSpy(),
                localStorage: {
                    clear: jasmine.createSpy('clear'),
                    setItem: jasmine.createSpy('setItem'),
                    getItem: jasmine.createSpy('getItem').and.returnValue(true)
                }
            }
        };
        deviceService = {
            isWrapper: true
        } as any;
        changeDetectorRef = {
            detectChanges: jasmine.createSpy('detectChanges'),
            detach: jasmine.createSpy('detach'),
        };
        gtmService = {
            push: jasmine.createSpy()
        };
        component = new FiveASideLiveEventOverlayComponent(cmsService,
            rendererService,
            windowRef,
            deviceService,
            domSanitizer,
            gtmService,
            changeDetectorRef,
            pubsubService,
            coreToolsService);
        component.clearOverlay.emit = jasmine.createSpy('modelChangeHandler.emit');
    });
    it('should create', () => {
        expect(component).toBeTruthy();
    });

    describe('#setDomPropertiesForTeamProgress Desktop', () => {
        it('should call required methods when getParentContainerRect is not null', () => {
            spyOn(component as any, 'getParentContainerRect').and.returnValue(boundFunc());
            spyOn(component as any, 'setElementDOMProperty');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            component['setDomPropertiesForTeamProgress']('', { getBoundingClientRect: () => boundFunc } as any);
            expect(component['unsetNativeBackgroundColor']).toHaveBeenCalled();
        });
        it('should call required methods when getParentContainerRect is null', () => {
            spyOn(component as any, 'getParentContainerRect').and.returnValue(null);
            spyOn(component as any, 'setElementDOMProperty');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            component['setDomPropertiesForTeamProgress']('', { getBoundingClientRect: () => boundFunc } as any);
            expect(component['unsetNativeBackgroundColor']).not.toHaveBeenCalled();
        });
    });

    describe('#setDomPropertiesEntryProgress Desktop', () => {
        it('should call setElementDOMProperty method with properties and when getParentContainerRect is not null', () => {
            spyOn(component as any, 'getParentContainerRect').and.returnValue(boundFunc());
            windowRef.document.querySelector = jasmine.createSpy().and.returnValue({ getBoundingClientRect: boundFunc });
            spyOn(component as any, 'setElementDOMProperty');
            component['setDomPropertiesEntryProgress']('#id', boundFunc() as any);
            expect(component['setElementDOMProperty']).toHaveBeenCalled();
        });
        it('should call setElementDOMProperty method with properties and when getParentContainerRect is null', () => {
            spyOn(component as any, 'getParentContainerRect').and.returnValue(null);
            windowRef.document.querySelector = jasmine.createSpy().and.returnValue(null);
            spyOn(component as any, 'setElementDOMProperty');
            component['setDomPropertiesEntryProgress']('#id', boundFunc() as any);
            expect(component['setElementDOMProperty']).not.toHaveBeenCalled();
        });
        it('should call setElementDOMProperty method with properties and when entryContainer is null', () => {
            spyOn(component as any, 'getParentContainerRect').and.returnValue(boundFunc());
            windowRef.document.querySelector = jasmine.createSpy().and.returnValue(null);
            spyOn(component as any, 'setElementDOMProperty');
            component['setDomPropertiesEntryProgress']('#id', boundFunc() as any);
            expect(component['setElementDOMProperty']).not.toHaveBeenCalled();
        });
        it('should call setElementDOMProperty method with properties and when getParentContainerRect is null not entryContainer', () => {
            spyOn(component as any, 'getParentContainerRect').and.returnValue(null);
            windowRef.document.querySelector = jasmine.createSpy().and.returnValue({ getBoundingClientRect: boundFunc });
            spyOn(component as any, 'setElementDOMProperty');
            component['setDomPropertiesEntryProgress']('#id', boundFunc() as any);
            expect(component['setElementDOMProperty']).not.toHaveBeenCalled();
        });
    });

    describe('#setDomPropertiesEntryProgressBar Desktop', () => {
        it('should call required methods in setDomPropertiesEntryProgressBar and when getParentContainerRect is not null', () => {
            spyOn(component as any, 'getParentContainerRect').and.returnValue(boundFunc());
            spyOn(component as any, 'setElementDOMProperty');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            component['setDomPropertiesEntryProgressBar']('#id', { scrollIntoView: () => { }, getBoundingClientRect: boundFunc } as any);
            expect(component['setElementDOMProperty']).toHaveBeenCalled();
        });
        it('should call required methods in setDomPropertiesEntryProgressBar and when getParentContainerRect is null', () => {
            spyOn(component as any, 'getParentContainerRect').and.returnValue(null);
            spyOn(component as any, 'setElementDOMProperty');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            component['setDomPropertiesEntryProgressBar']('#id', { scrollIntoView: () => { }, getBoundingClientRect: boundFunc } as any);
            expect(component['setElementDOMProperty']).not.toHaveBeenCalled();
        });
    });

    describe('#showLeaderboardEntriesTutorial Desktop', () => {
        beforeEach(() => {
            spyOn(component as any, 'scrollToBannerView');
            spyOn(component as any, 'onClickNext');
            spyOn(component as any, 'setElementDOMProperty');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            spyOn(component as any, 'liveTutorialGATrack');
            spyOn(component as any, 'calculateLeaderboardEntriesHeight');
        });
        it('should call required methods in showLeaderboardEntriesTutorial', () => {
            spyOn(component as any, 'getParentContainerRect').and.returnValue(boundFunc());
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                if (args === LIVE_OVERLAY.ID_LEADERBOARD_INFO) {
                    return {};
                } else if (args === LIVE_OVERLAY.ID_LIVE_LEADERBOARD_ITEM) {
                    return { getBoundingClientRect: boundFunc };
                } else if (args === LIVE_OVERLAY.CLASS_LIVE_LEADERBOARD_TITLE) {
                    return { getBoundingClientRect: boundFunc };
                }
            });
            component['showLeaderboardEntriesTutorial'](LIVE_OVERLAY.ID_LEADERBOARD_INFO);
            expect(component['onClickNext']).not.toHaveBeenCalled();
        });
        it('should call required methods in showLeaderboardEntriesTutorial when getParentContainerRect is null', () => {
            spyOn(component as any, 'getParentContainerRect').and.returnValue(null);
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                if (args === LIVE_OVERLAY.ID_LEADERBOARD_INFO) {
                    return {};
                } else if (args === LIVE_OVERLAY.ID_LIVE_LEADERBOARD_ITEM) {
                    return { getBoundingClientRect: boundFunc };
                } else if (args === LIVE_OVERLAY.CLASS_LIVE_LEADERBOARD_TITLE) {
                    return { getBoundingClientRect: boundFunc };
                }
            });
            component['showLeaderboardEntriesTutorial'](LIVE_OVERLAY.ID_LEADERBOARD_INFO);
            expect(component['onClickNext']).not.toHaveBeenCalled();
        });
        it('should call required methods in leaderboardTitleEl is null', () => {
            spyOn(component as any, 'getParentContainerRect').and.returnValue(boundFunc());
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                if (args === LIVE_OVERLAY.ID_LEADERBOARD_INFO) {
                    return {};
                } else if (args === LIVE_OVERLAY.ID_LIVE_LEADERBOARD_ITEM) {
                    return { getBoundingClientRect: boundFunc };
                } else if (args === LIVE_OVERLAY.CLASS_LIVE_LEADERBOARD_TITLE) {
                    return null;
                }
            });
            component['showLeaderboardEntriesTutorial'](LIVE_OVERLAY.ID_LEADERBOARD_INFO);
            expect(component['onClickNext']).toHaveBeenCalled();
        });

        it('should call required methods in leaderboardItemEl is null', () => {
            spyOn(component as any, 'getParentContainerRect').and.returnValue(boundFunc());
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                if (args === LIVE_OVERLAY.ID_LEADERBOARD_INFO) {
                    return {};
                } else if (args === LIVE_OVERLAY.ID_LIVE_LEADERBOARD_ITEM) {
                    return null;
                } else if (args === LIVE_OVERLAY.CLASS_LIVE_LEADERBOARD_TITLE) {
                    return {};
                }
            });
            component['showLeaderboardEntriesTutorial'](LIVE_OVERLAY.ID_LEADERBOARD_INFO);
            expect(component['onClickNext']).toHaveBeenCalled();
        });

        it('should call required methods in highlightEl is null', () => {
            spyOn(component as any, 'getParentContainerRect').and.returnValue(boundFunc());
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                if (args === LIVE_OVERLAY.ID_LEADERBOARD_INFO) {
                    return null;
                } else if (args === LIVE_OVERLAY.ID_LIVE_LEADERBOARD_ITEM) {
                    return {};
                } else if (args === LIVE_OVERLAY.CLASS_LIVE_LEADERBOARD_TITLE) {
                    return {};
                }
            });
            component['showLeaderboardEntriesTutorial'](LIVE_OVERLAY.ID_LEADERBOARD_INFO);
            expect(component['onClickNext']).toHaveBeenCalled();
        });
    });

    describe('#getParentContainerRect Desktop', () => {
        it('should return rect coordinates object', () => {
            windowRef.document.querySelector = jasmine.createSpy().and.returnValue({ getBoundingClientRect: boundFunc });
            expect(component['getParentContainerRect']()).not.toBeNull();
        });
        it('should return null coordinates object', () => {
            windowRef.document.querySelector = jasmine.createSpy().and.returnValue(null);
            expect(component['getParentContainerRect']()).toBeNull();
        });
    });
});
