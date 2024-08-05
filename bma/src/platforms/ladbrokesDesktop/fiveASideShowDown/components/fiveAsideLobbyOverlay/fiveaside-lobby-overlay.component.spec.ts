import {
    FiveASideLobbyOverlayComponent
} from '@ladbrokesDesktop/fiveASideShowDown/components/fiveAsideLobbyOverlay/fiveaside-lobby-overlay.component';
import { of } from 'rxjs';
import { LOBBY_OVERLAY } from '@app/fiveASideShowDown/constants/constants';

describe('FiveASideLobbyOverlayComponent', () => {
    let component: FiveASideLobbyOverlayComponent;
    let rendererService,
        domSanitizer,
        cmsService,
        windowRef,
        deviceService,
        gtmService,
        changeDetectorRef,
        pubSubService,
        coreToolsService,
        bodyScrollLockService;
    const boundFunc = () => ({ 'top': 50, 'left': 50 });

    beforeEach(() => {
        rendererService = {
            renderer: {
                addClass: jasmine.createSpy('addClass'),
                removeClass: jasmine.createSpy('removeClass'),
                setStyle: jasmine.createSpy('setStyle')
            }
        };
        coreToolsService = {
            uuid: jasmine.createSpy()
        };
        pubSubService = {
            subscribe: jasmine.createSpy(),
            unsubscribe: jasmine.createSpy(),
            publish: jasmine.createSpy()
        };
        domSanitizer = {
            sanitize: jasmine.createSpy().and.returnValue('test'),
            bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml')
        };
        cmsService = {
            getWelcomeOverlay: jasmine.createSpy('getWelcomeOverlay').and.returnValue(of({})),
        };
        bodyScrollLockService = {
            disableBodyScroll: jasmine.createSpy('disableBodyScroll'),
            enableBodyScroll: jasmine.createSpy('enableBodyScroll')
          };
        windowRef = {
            document: {
                querySelector: { get: jasmine.createSpy() },
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
        component = new FiveASideLobbyOverlayComponent(cmsService,
            rendererService,
            windowRef,
            deviceService,
            domSanitizer,
            gtmService,
            changeDetectorRef,
            pubSubService,
            coreToolsService,
            bodyScrollLockService);
        component.clearOverlay.emit = jasmine.createSpy('modelChangeHandler.emit');
    });

    it('should create #FiveASideLobbyOverlayComponent Desktop', () => {
        expect(component).toBeTruthy();
    });

    describe('#getContainerRect Desktop', () => {
        it('should return rect coordinates object', () => {
            windowRef.document.querySelector = jasmine.createSpy().and.returnValue({ getBoundingClientRect: boundFunc });
            expect(component['getContainerRect']()).not.toBeNull();
        });
        it('should return null coordinates object', () => {
            windowRef.document.querySelector = jasmine.createSpy().and.returnValue(null);
            expect(component['getContainerRect']()).toBeNull();
        });
    });
    describe('#showEntryPrizesTutorial Desktop', () => {
        it('should return to next tutorial if current highlighting element is null', () => {
            spyOn(component as any, 'scrollToBannerView');
            spyOn(component as any, 'onClickNext');
            spyOn(component as any, 'lobbyTutorialGATrack');
            windowRef.document.querySelector = jasmine.createSpy().and.returnValue(null);
            component['showEntryPrizesTutorial'](LOBBY_OVERLAY.ID_CARD_TOTAL_PRIZES, LOBBY_OVERLAY.ID_ENTRY_PRIZES);
            expect(component['onClickNext']).toHaveBeenCalled();
        });

        it('should return to next tutorial if current highlighting and holder element is present', () => {
            spyOn(component as any, 'setElementDOMProperty');
            spyOn(component as any, 'setTopLeftPropsToElement');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            spyOn(component as any, 'lobbyTutorialGATrack');
            const parentEl = {
                querySelector: jasmine.createSpy().and.
                    returnValue({
                        scrollIntoView: jasmine.createSpy(),
                        getBoundingClientRect: boundFunc,
                        parentElement: { getBoundingClientRect: boundFunc }
                    })
            };
            const el = {
                parentElement: {
                    parentElement: {
                        parentElement: parentEl
                    }
                }
            };
            windowRef.document.querySelector = jasmine.createSpy()
                .and.returnValue({
                    scrollIntoView: jasmine.createSpy(),
                    parentElement: el,
                    getBoundingClientRect: boundFunc
                });
            component['showEntryPrizesTutorial'](LOBBY_OVERLAY.ID_CARD_TOTAL_PRIZES, LOBBY_OVERLAY.ID_ENTRY_PRIZES);
            expect(component['setElementDOMProperty']).toHaveBeenCalled();
        });

        it('should return to next tutorial when entry is null', () => {
            spyOn(component as any, 'setElementDOMProperty');
            spyOn(component as any, 'setTopLeftPropsToElement');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            spyOn(component as any, 'lobbyTutorialGATrack');
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                if (args === LOBBY_OVERLAY.ID_CARD_TOTAL_PRIZES) {
                    return {};
                } else if (args === LOBBY_OVERLAY.ID_ENTRY_PRIZES) {
                    return null;
                }
            });
            component['showEntryPrizesTutorial'](LOBBY_OVERLAY.ID_CARD_TOTAL_PRIZES, LOBBY_OVERLAY.ID_ENTRY_PRIZES);
            expect(component['setTopLeftPropsToElement']).not.toHaveBeenCalled();
        });

        it('should return to next tutorial when element is null', () => {
            spyOn(component as any, 'setElementDOMProperty');
            spyOn(component as any, 'setTopLeftPropsToElement');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            spyOn(component as any, 'lobbyTutorialGATrack');
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                if (args === LOBBY_OVERLAY.ID_CARD_TOTAL_PRIZES) {
                    return null;
                } else if (args === LOBBY_OVERLAY.ID_ENTRY_PRIZES) {
                    return {};
                }
            });
            component['showEntryPrizesTutorial'](LOBBY_OVERLAY.ID_CARD_TOTAL_PRIZES, LOBBY_OVERLAY.ID_ENTRY_PRIZES);
            expect(component['setElementDOMProperty']).not.toHaveBeenCalled();
            expect(component['setTopLeftPropsToElement']).not.toHaveBeenCalled();
        });

        it('should return to next tutorial when element is null', () => {
            spyOn(component as any, 'setElementDOMProperty');
            spyOn(component as any, 'setTopLeftPropsToElement');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            spyOn(component as any, 'lobbyTutorialGATrack');
            spyOn(component as any, 'getContainerRect').and.returnValue({});
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                return null;
            });
            component['showEntryPrizesTutorial'](LOBBY_OVERLAY.ID_CARD_TOTAL_PRIZES, LOBBY_OVERLAY.ID_ENTRY_PRIZES);
            expect(component['setElementDOMProperty']).not.toHaveBeenCalled();
            expect(component['setTopLeftPropsToElement']).not.toHaveBeenCalled();
        });

        it('should return to next tutorial when getContainerRect is null', () => {
            spyOn(component as any, 'setElementDOMProperty');
            spyOn(component as any, 'setTopLeftPropsToElement');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            spyOn(component as any, 'lobbyTutorialGATrack');
            spyOn(component as any, 'getContainerRect').and.returnValue(null);
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                return null;
            });
            component['showEntryPrizesTutorial'](LOBBY_OVERLAY.ID_CARD_TOTAL_PRIZES, LOBBY_OVERLAY.ID_ENTRY_PRIZES);
            expect(component['setElementDOMProperty']).not.toHaveBeenCalled();
            expect(component['setTopLeftPropsToElement']).not.toHaveBeenCalled();
        });
    });

    describe('#showLobbySignPostingTutorial Desktop', () => {
        const el = {
            parentElement: {
                parentElement: {
                    parentElement:
                    {
                        parentElement: {
                            querySelector: jasmine.createSpy().and.returnValue(
                                {
                                    getBoundingClientRect: boundFunc,
                                    parentElement: { getBoundingClientRect: boundFunc }
                                })
                        }
                    }
                }
            }
        };

        it('should set dom property for HTML element and getContainerRect is null', () => {
            spyOn(component as any, 'setElementDOMProperty');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            spyOn(component as any, 'lobbyTutorialGATrack');
            spyOn(component as any, 'getContainerRect').and.returnValue(null);
            component['showLobbySignPostingTutorial'](el as any);
            expect(component['setElementDOMProperty']).not.toHaveBeenCalled();
        });

        it('should set dom property for HTML element', () => {
            spyOn(component as any, 'setElementDOMProperty');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            spyOn(component as any, 'lobbyTutorialGATrack');
            spyOn(component as any, 'getContainerRect').and.returnValue({ left: 50 });
            component['showLobbySignPostingTutorial'](el as any);
            expect(component['setElementDOMProperty']).toHaveBeenCalled();
        });

        it('should not set dom property for HTML element when no parentElement found inside', () => {
            spyOn(component as any, 'setElementDOMProperty');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            spyOn(component as any, 'lobbyTutorialGATrack');
            spyOn(component as any, 'getContainerRect');
            const element = {
                parentElement: {
                    parentElement: {
                        parentElement:
                        {
                            parentElement: {
                                querySelector: jasmine.createSpy().and.returnValue(
                                    {
                                        getBoundingClientRect: boundFunc
                                    })
                            }
                        }
                    }
                }
            };
            component['showLobbySignPostingTutorial'](element as any);
            expect(component['setElementDOMProperty']).not.toHaveBeenCalled();
        });

        it('should not set dom property for HTML element when parentElement querySelector returns null', () => {
            spyOn(component as any, 'setElementDOMProperty');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            spyOn(component as any, 'lobbyTutorialGATrack');
            spyOn(component as any, 'getContainerRect');
            const element = {
                parentElement: {
                    parentElement: {
                        parentElement:
                        {
                            parentElement: {
                                querySelector: jasmine.createSpy().and.returnValue(null)
                            }
                        }
                    }
                }
            };
            component['showLobbySignPostingTutorial'](element as any);
            expect(component['setElementDOMProperty']).not.toHaveBeenCalled();
        });
        it('should not set dom property for HTML element when parentElement is null', () => {
            spyOn(component as any, 'setElementDOMProperty');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            spyOn(component as any, 'lobbyTutorialGATrack');
            spyOn(component as any, 'getContainerRect');
            const element = {
                parentElement: {
                    parentElement: {
                        parentElement:
                        {
                            parentElement: null
                        }
                    }
                }
            };
            component['showLobbySignPostingTutorial'](element as any);
            expect(component['setElementDOMProperty']).not.toHaveBeenCalled();
        });
    });

    describe('#showEntryInfoTutorial Desktop', () => {
        it('should return to next tutorial when entry is null', () => {
            spyOn(component as any, 'onClickNext');
            spyOn(component as any, 'getContainerRect');
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                if (args === LOBBY_OVERLAY.ID_CARD_ENTRY_INFO) {
                    return null;
                }
            });
            component['showEntryInfoTutorial'](LOBBY_OVERLAY.ID_CARD_ENTRY_INFO, LOBBY_OVERLAY.ID_ENTRY_INFO);
            expect(component['onClickNext']).toHaveBeenCalled();
        });

        it('should return to next tutorial when entry holder is null', () => {
            spyOn(component as any, 'onClickNext');
            spyOn(component as any, 'getContainerRect');
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                if (args === LOBBY_OVERLAY.ID_ENTRY_INFO) {
                    return null;
                }
            });
            component['showEntryInfoTutorial'](LOBBY_OVERLAY.ID_CARD_ENTRY_INFO, LOBBY_OVERLAY.ID_ENTRY_INFO);
            expect(component['onClickNext']).toHaveBeenCalled();
        });

        it('should return to next tutorial when entry element and entry holder is not null', () => {
            spyOn(component as any, 'setTopLeftPropsToElement');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            spyOn(component as any, 'lobbyTutorialGATrack');
            spyOn(component as any, 'getContainerRect');
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                if (args === LOBBY_OVERLAY.ID_CARD_ENTRY_INFO) {
                    return { getBoundingClientRect: boundFunc, parentElement: {} };
                } else if (args === LOBBY_OVERLAY.ID_ENTRY_INFO) {
                    return {};
                }
            });
            component['showEntryInfoTutorial'](LOBBY_OVERLAY.ID_CARD_ENTRY_INFO, LOBBY_OVERLAY.ID_ENTRY_INFO);
            expect(component['setTopLeftPropsToElement']).not.toHaveBeenCalled();
        });

        it('should return to next tutorial when entry element and entry holder is not null, parent is null', () => {
            spyOn(component as any, 'scrollToBannerView');
            spyOn(component as any, 'setTopLeftPropsToElement');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            spyOn(component as any, 'lobbyTutorialGATrack');
            spyOn(component as any, 'getContainerRect');
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                if (args === LOBBY_OVERLAY.ID_CARD_ENTRY_INFO) {
                    return { getBoundingClientRect: boundFunc, parentElement: null };
                } else if (args === LOBBY_OVERLAY.ID_ENTRY_INFO) {
                    return {};
                }
            });
            component['showEntryInfoTutorial'](LOBBY_OVERLAY.ID_CARD_ENTRY_INFO, LOBBY_OVERLAY.ID_ENTRY_INFO);
            expect(component['scrollToBannerView']).not.toHaveBeenCalled();
        });

        it('should return to next tutorial when entry el and entry holder is not nullparent is null and getContainerRect is null', () => {
            spyOn(component as any, 'scrollToBannerView');
            spyOn(component as any, 'setTopLeftPropsToElement');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            spyOn(component as any, 'lobbyTutorialGATrack');
            spyOn(component as any, 'getContainerRect').and.returnValue(null);
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                if (args === LOBBY_OVERLAY.ID_CARD_ENTRY_INFO) {
                    return { getBoundingClientRect: boundFunc, parentElement: null };
                } else if (args === LOBBY_OVERLAY.ID_ENTRY_INFO) {
                    return {};
                }
            });
            component['showEntryInfoTutorial'](LOBBY_OVERLAY.ID_CARD_ENTRY_INFO, LOBBY_OVERLAY.ID_ENTRY_INFO);
            expect(component['scrollToBannerView']).not.toHaveBeenCalled();
        });
    });

    describe('#showShowdownCardTutorial Desktop', () => {
        it('should return to next tutorial when entry is null', () => {
            spyOn(component as any, 'scrollToBannerView');
            spyOn(component as any, 'onClickNext');
            spyOn(component as any, 'getContainerRect');
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                if (args === LOBBY_OVERLAY.ID_CARD_MAIN) {
                    return null;
                }
            });
            component['showShowdownCardTutorial'](LOBBY_OVERLAY.ID_CARD_MAIN, LOBBY_OVERLAY.ID_CARD_INFO);
            expect(component['onClickNext']).toHaveBeenCalled();
        });

        it('should return to next tutorial when entry holder is null', () => {
            spyOn(component as any, 'scrollToBannerView');
            spyOn(component as any, 'onClickNext');
            spyOn(component as any, 'getContainerRect');
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                if (args === LOBBY_OVERLAY.ID_CARD_INFO) {
                    return null;
                }
            });
            component['showShowdownCardTutorial'](LOBBY_OVERLAY.ID_CARD_MAIN, LOBBY_OVERLAY.ID_CARD_INFO);
            expect(component['onClickNext']).toHaveBeenCalled();
        });

        it('should return to next tutorial when entry element and entry holder is not null', () => {
            spyOn(component as any, 'scrollToBannerView');
            spyOn(component as any, 'setTopLeftPropsToElement');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            spyOn(component as any, 'lobbyTutorialGATrack');
            spyOn(component as any, 'getContainerRect');
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                if (args === LOBBY_OVERLAY.ID_CARD_MAIN) {
                    return { getBoundingClientRect: boundFunc };
                } else if (args === LOBBY_OVERLAY.ID_CARD_INFO) {
                    return {};
                }
            });
            component['showShowdownCardTutorial'](LOBBY_OVERLAY.ID_CARD_MAIN, LOBBY_OVERLAY.ID_CARD_INFO);
            expect(component['scrollToBannerView']).not.toHaveBeenCalled();
        });

        it('should return to next tutorial when entry element and entry holder is null, getContainerRect is not null', () => {
            spyOn(component as any, 'scrollToBannerView');
            spyOn(component as any, 'setTopLeftPropsToElement');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            spyOn(component as any, 'lobbyTutorialGATrack');
            spyOn(component as any, 'getContainerRect').and.returnValue({ left: 50 });
            spyOn(component as any, 'onClickNext');
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                return null;
            });
            component['showShowdownCardTutorial'](LOBBY_OVERLAY.ID_CARD_MAIN, LOBBY_OVERLAY.ID_CARD_INFO);
            expect(component['onClickNext']).toHaveBeenCalled();
        });
    });
});
