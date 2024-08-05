import {
    FiveASideLobbyOverlayComponent
} from '@app/fiveASideShowDown/components/fiveAsideLobbyOverlay/fiveaside-lobby-overlay.component';
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
        domSanitizer = {
            sanitize: jasmine.createSpy().and.returnValue('test'),
            bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml')
        };
        cmsService = {
            getWelcomeOverlay: jasmine.createSpy('getWelcomeOverlay').and.returnValue(of({})),
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
                },
                setTimeout: jasmine.createSpy('setTimeout').and.callFake((cb, delay) => {
                    windowRef.nativeWindow._setTimeoutCb = cb;
                    return windowRef.nativeWindow._setTimeoutId;
                }),
                clearTimeout: jasmine.createSpy('clearTimeout')
            }
        };
        pubSubService = {
            subscribe: jasmine.createSpy(),
            unsubscribe: jasmine.createSpy(),
            publish: jasmine.createSpy()
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
        bodyScrollLockService = {
            disableBodyScroll: jasmine.createSpy('disableBodyScroll'),
            enableBodyScroll: jasmine.createSpy('enableBodyScroll')
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

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    describe('#ngOnInit', () => {
        it('should call required methods in init', () => {
            spyOn(component as any, 'validateOverlayBaseElement');
            spyOn(component as any, 'initLobbyOverlayElements');
            spyOn(component as any, 'lobbyDataChangeListener');
            spyOn(component as any, 'enableDisableIOSBodyScroll');
            component.ngOnInit();
            expect(component['validateOverlayBaseElement']).toHaveBeenCalled();
            expect(component['initLobbyOverlayElements']).toHaveBeenCalled();
        });
    });

    describe('#ngOnDestroy', () => {
        it('should call required methods in ngOnDestroy', () => {
            spyOn(component as any, 'onCloseLobbyOverlay');
            spyOn(component as any, 'enableDisableIOSBodyScroll');
            component.ngOnDestroy();
            expect(component['onCloseLobbyOverlay']).toHaveBeenCalled();
        });
    });

    describe('#enableDisableIOSBodyScroll', () => {
        it('should call addEventListener', () => {
            spyOn(component as any, 'preventScrollForTouchMove');
            spyOn(component as any, 'preventScrollForTouchStart');
            component['deviceService'] = { isIos: true } as any;
            const element = {
                addEventListener: jasmine.createSpy(),
                removeEventListener: jasmine.createSpy()
            } as any;
            windowRef.document.getElementById.and.returnValue(element);
            component.enableDisableIOSBodyScroll('add');
            expect(element.addEventListener).toHaveBeenCalled();
        });
        it('should call removeEventListener', () => {
            spyOn(component as any, 'preventScrollForTouchMove');
            spyOn(component as any, 'preventScrollForTouchStart');
            component['deviceService'] = { isIos: true } as any;
            const element = {
                addEventListener: jasmine.createSpy(),
                removeEventListener: jasmine.createSpy()
            } as any;
            windowRef.document.getElementById.and.returnValue(element);
            component.enableDisableIOSBodyScroll('remove');
            expect(element.removeEventListener).toHaveBeenCalled();
        });
        it('should not call eventListeners', () => {
            spyOn(component as any, 'preventScrollForTouchMove');
            spyOn(component as any, 'preventScrollForTouchStart');
            component['deviceService'] = { isIos: true } as any;
            const element = {
                addEventListener: jasmine.createSpy(),
                removeEventListener: jasmine.createSpy()
            } as any;
            windowRef.document.getElementById.and.returnValue(null);
            component.enableDisableIOSBodyScroll('remove');
            expect(element.addEventListener).not.toHaveBeenCalled();
        });
        it('should not call eventListeners', () => {
            spyOn(component as any, 'preventScrollForTouchMove');
            spyOn(component as any, 'preventScrollForTouchStart');
            component['deviceService'] = { isIos: false } as any;
            const element = {
                addEventListener: jasmine.createSpy(),
                removeEventListener: jasmine.createSpy()
            } as any;
            windowRef.document.getElementById.and.returnValue(null);
            component.enableDisableIOSBodyScroll('remove');
            expect(element.addEventListener).not.toHaveBeenCalled();
        });
    });

    describe('#preventScrollForTouchMove', () => {
        it('should call preventDefault', () => {
            const event = { preventDefault: jasmine.createSpy() };
            component['preventScrollForTouchMove'](event as any);
            expect(event.preventDefault).toHaveBeenCalled();
        });
    });

    describe('#preventScrollForTouchStart', () => {
        it('should not call preventDefault', () => {
            const event = { preventDefault: jasmine.createSpy(), target : {id : 'close-div'} };
            component['preventScrollForTouchStart'](event as any);
            expect(event.preventDefault).not.toHaveBeenCalled();
        });
        it('should not call preventDefault', () => {
            const event = { preventDefault: jasmine.createSpy(), target : {id : 'new-div'} };
            component['preventScrollForTouchStart'](event as any);
            expect(event.preventDefault).toHaveBeenCalled();
        });

        it('should not call preventDefault when element is button', () => {
            const event = { preventDefault: jasmine.createSpy(), target : {localName : 'button'} };
            component['preventScrollForTouchStart'](event as any);
            expect(event.preventDefault).not.toHaveBeenCalled();
        });
    });

    describe('#lobbyDataChangeListener', () => {
        it('should call setTimeout', () => {
            spyOn(component as any, 'reInitTutorial');
            component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
                if (ch === LOBBY_OVERLAY.LOBBY_DATA_RELOADED_COMPLETED) {
                    fn();
                }
            });
            windowRef.nativeWindow.setTimeout.and.callFake(cb => cb());
            component['lobbyDataChangeListener']();
            expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 1000);
        });
    });

    describe('#reInitTutorial', () => {
        it('should call onClickNext method', () => {
            spyOn(component as any, 'onClickNext');
            component['activeStep'] = '1';
            component['reInitTutorial']();
            expect(component['onClickNext']).toHaveBeenCalled();
        });
        it('should not call onClickNext method when step is finish', () => {
            spyOn(component as any, 'onClickNext');
            component['activeStep'] = 'finish';
            component['reInitTutorial']();
            expect(component['onClickNext']).not.toHaveBeenCalled();
        });
        it('should not call onClickNext method', () => {
            spyOn(component as any, 'onClickNext');
            component['activeStep'] = null;
            component['reInitTutorial']();
            expect(component['onClickNext']).not.toHaveBeenCalled();
        });
    });

    describe('#onCloseLobbyOverlay', () => {
        it('should call required methods in ngOnDestroy', () => {
            spyOn(component as any, 'lobbyTutorialGATrack');
            spyOn(component as any, 'enableDisableIOSBodyScroll');
            component.clearOverlay.emit = jasmine.createSpy('modelChangeHandler.emit');
            component.onCloseLobbyOverlay();
            expect(component.clearOverlay.emit).toHaveBeenCalled();
        });
        it('should call required methods in close scenario', () => {
            spyOn(component as any, 'lobbyTutorialGATrack');
            spyOn(component as any, 'enableDisableIOSBodyScroll');
            component.clearOverlay.emit = jasmine.createSpy('modelChangeHandler.emit');
            component.onCloseLobbyOverlay('close');
            expect(component.clearOverlay.emit).toHaveBeenCalled();
            expect(component['lobbyTutorialGATrack']).toHaveBeenCalled();
        });
    });

    describe('#onClickNext', () => {
        beforeEach(() => {
            spyOn(component as any, 'lobbyTutorialGATrack');
            spyOn(component as any, 'updateTutorialsSteps');
        });
        it('should call required methods when step is 2', () => {
            spyOn(component as any, 'showEntryPrizesTutorial');
            component.onClickNext('2');
            expect(component['updateTutorialsSteps']).toHaveBeenCalled();
            expect(component['showEntryPrizesTutorial']).toHaveBeenCalled();
        });

        it('should call required methods when step is 3', () => {
            spyOn(component as any, 'scrollToBannerView');
            spyOn(component as any, 'showEntryInfoTutorial');
            component.onClickNext('3');
            expect(component['updateTutorialsSteps']).toHaveBeenCalled();
            expect(component['showEntryInfoTutorial']).toHaveBeenCalled();
        });

        it('should call required methods when step is 4', () => {
            spyOn(component as any, 'scrollToBannerView');
            spyOn(component as any, 'showShowdownCardTutorial');
            component.onClickNext('4');
            expect(component['updateTutorialsSteps']).toHaveBeenCalled();
            expect(component['showShowdownCardTutorial']).toHaveBeenCalled();
        });

        it('should call required methods when step is FINISH', () => {
            spyOn(component as any, 'onCloseLobbyOverlay');
            component.onClickNext(LOBBY_OVERLAY.FINISH);
            expect(component['onCloseLobbyOverlay']).toHaveBeenCalled();
        });

        it('should not any methods when it is default case', () => {
            component.onClickNext('abc');
            expect(component['updateTutorialsSteps']).not.toHaveBeenCalled();
        });
    });

    describe('#initLobbyOverlayElements', () => {
        it('should init rules lobby overlay', () => {
            spyOn(component as any, 'lobbyTutorialGATrack');
            component['initLobbyOverlayElements']();
            expect(rendererService.renderer.addClass).toHaveBeenCalledWith(undefined, 'active');
        });
    });

    describe('#showEntryPrizesTutorial', () => {
        beforeEach(() => {
            const element = {
                addEventListener: jasmine.createSpy(),
                removeEventListener: jasmine.createSpy()
            } as any;
            windowRef.document.getElementById.and.returnValue(element);
        });
        it('should return to next tutorial if current highlighting element is null', () => {
            spyOn(component as any, 'scrollToBannerView');
            spyOn(component as any, 'onClickNext');
            spyOn(component as any, 'lobbyTutorialGATrack');
            windowRef.document.querySelector = jasmine.createSpy().and.returnValue(null);
            component['showEntryPrizesTutorial'](LOBBY_OVERLAY.ID_CARD_TOTAL_PRIZES, LOBBY_OVERLAY.ID_ENTRY_PRIZES);
            expect(component['scrollToBannerView']).toHaveBeenCalled();
            expect(component['onClickNext']).toHaveBeenCalled();
        });

        it('should return to next tutorial if current highlighting and holder element is present', () => {
            spyOn(component as any, 'scrollToBannerView');
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
            expect(component['scrollToBannerView']).toHaveBeenCalled();
            expect(component['setTopLeftPropsToElement']).toHaveBeenCalled();
        });

        it('should return to next tutorial when entry is null', () => {
            spyOn(component as any, 'scrollToBannerView');
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
            expect(component['scrollToBannerView']).toHaveBeenCalled();
            expect(component['setTopLeftPropsToElement']).not.toHaveBeenCalled();
        });

        it('should return to next tutorial when element is null', () => {
            spyOn(component as any, 'scrollToBannerView');
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
            expect(component['scrollToBannerView']).toHaveBeenCalled();
            expect(component['setTopLeftPropsToElement']).not.toHaveBeenCalled();
        });
    });

    describe('#setElementDOMProperty', () => {
        it('should set dom property for HTML element', () => {
            windowRef.document.querySelector = jasmine.createSpy()
                .and.returnValue({});
            component['setElementDOMProperty'](LOBBY_OVERLAY.ID_SIGN_POST, 'setStyle', LOBBY_OVERLAY.STYLE.TOP, '2px');
            expect(rendererService.renderer.setStyle).toHaveBeenCalled();
        });
        it('should not set dom property when element is null', () => {
            windowRef.document.querySelector = jasmine.createSpy()
                .and.returnValue(null);
            component['setElementDOMProperty'](LOBBY_OVERLAY.ID_SIGN_POST, 'setStyle', LOBBY_OVERLAY.STYLE.TOP, '2px');
            expect(rendererService.renderer.setStyle).not.toHaveBeenCalled();
        });
    });

    describe('#showLobbySignPostingTutorial', () => {
        beforeEach(() => {
            const element = {
                addEventListener: jasmine.createSpy(),
                removeEventListener: jasmine.createSpy()
            } as any;
            windowRef.document.getElementById.and.returnValue(element);
        });
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
        it('should set dom property for HTML element', () => {
            spyOn(component as any, 'setElementDOMProperty');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            spyOn(component as any, 'lobbyTutorialGATrack');
            component['showLobbySignPostingTutorial'](el as any);
            expect(component['setElementDOMProperty']).toHaveBeenCalled();
        });

        it('should not set dom property for HTML element when no parentElement found inside', () => {
            spyOn(component as any, 'setElementDOMProperty');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            spyOn(component as any, 'lobbyTutorialGATrack');
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

    describe('#showEntryInfoTutorial', () => {
        beforeEach(() => {
            const element = {
                addEventListener: jasmine.createSpy(),
                removeEventListener: jasmine.createSpy()
            } as any;
            windowRef.document.getElementById.and.returnValue(element);
        });
        it('should return to next tutorial when entry is null', () => {
            spyOn(component as any, 'scrollToBannerView');
            spyOn(component as any, 'onClickNext');
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                if (args === LOBBY_OVERLAY.ID_CARD_ENTRY_INFO) {
                    return null;
                }
            });
            component['showEntryInfoTutorial'](LOBBY_OVERLAY.ID_CARD_ENTRY_INFO, LOBBY_OVERLAY.ID_ENTRY_INFO);
            expect(component['scrollToBannerView']).toHaveBeenCalled();
            expect(component['onClickNext']).toHaveBeenCalled();
        });

        it('should return to next tutorial when entry holder is null', () => {
            spyOn(component as any, 'scrollToBannerView');
            spyOn(component as any, 'onClickNext');
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                if (args === LOBBY_OVERLAY.ID_ENTRY_INFO) {
                    return null;
                }
            });
            component['showEntryInfoTutorial'](LOBBY_OVERLAY.ID_CARD_ENTRY_INFO, LOBBY_OVERLAY.ID_ENTRY_INFO);
            expect(component['scrollToBannerView']).toHaveBeenCalled();
            expect(component['onClickNext']).toHaveBeenCalled();
        });

        it('should return to next tutorial when entry element and entry holder is not null', () => {
            spyOn(component as any, 'scrollToBannerView');
            spyOn(component as any, 'setTopLeftPropsToElement');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            spyOn(component as any, 'lobbyTutorialGATrack');
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                if (args === LOBBY_OVERLAY.ID_CARD_ENTRY_INFO) {
                    return { getBoundingClientRect: boundFunc, parentElement: {}, scrollIntoView: () => { } };
                } else if (args === LOBBY_OVERLAY.ID_ENTRY_INFO) {
                    return {};
                }
            });
            component['showEntryInfoTutorial'](LOBBY_OVERLAY.ID_CARD_ENTRY_INFO, LOBBY_OVERLAY.ID_ENTRY_INFO);
            expect(component['scrollToBannerView']).toHaveBeenCalled();
            expect(component['setTopLeftPropsToElement']).toHaveBeenCalled();
        });

        it('should return to next tutorial when entry element and entry holder is not null, parent is null', () => {
            spyOn(component as any, 'scrollToBannerView');
            spyOn(component as any, 'setTopLeftPropsToElement');
            spyOn(component as any, 'unsetNativeBackgroundColor');
            spyOn(component as any, 'lobbyTutorialGATrack');
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                if (args === LOBBY_OVERLAY.ID_CARD_ENTRY_INFO) {
                    return { getBoundingClientRect: boundFunc, parentElement: null, scrollIntoView: () => { } };
                } else if (args === LOBBY_OVERLAY.ID_ENTRY_INFO) {
                    return {};
                }
            });
            component['showEntryInfoTutorial'](LOBBY_OVERLAY.ID_CARD_ENTRY_INFO, LOBBY_OVERLAY.ID_ENTRY_INFO);
            expect(component['scrollToBannerView']).toHaveBeenCalled();
            expect(component['setTopLeftPropsToElement']).toHaveBeenCalled();
        });
    });

    describe('#showShowdownCardTutorial', () => {
        beforeEach(() => {
            const element = {
                addEventListener: jasmine.createSpy(),
                removeEventListener: jasmine.createSpy()
            } as any;
            windowRef.document.getElementById.and.returnValue(element);
        });
        it('should return to next tutorial when entry is null', () => {
            spyOn(component as any, 'scrollToBannerView');
            spyOn(component as any, 'onClickNext');
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
            windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
                if (args === LOBBY_OVERLAY.ID_CARD_MAIN) {
                    return { getBoundingClientRect: boundFunc, scrollIntoView: () => { } };
                } else if (args === LOBBY_OVERLAY.ID_CARD_INFO) {
                    return {};
                }
            });
            component['showShowdownCardTutorial'](LOBBY_OVERLAY.ID_CARD_MAIN, LOBBY_OVERLAY.ID_CARD_INFO);
            expect(component['setTopLeftPropsToElement']).toHaveBeenCalled();
        });
    });
    describe('#unsetNativeBackgroundColor', () => {
        it('should call renderer service setStyle', () => {
            windowRef.document.querySelector = jasmine.createSpy().and.returnValue({});
            component['unsetNativeBackgroundColor']();
            expect(rendererService.renderer.setStyle).toHaveBeenCalled();
        });
    });

    describe('#setTopLeftPropsToElement', () => {
        it('should call renderer service setStyle', () => {
            component['setTopLeftPropsToElement']({} as any, 10, 50);
            expect(rendererService.renderer.setStyle).toHaveBeenCalled();
        });
    });

    describe('#scrollToBannerView', () => {
        it('should call changeDetectorRef and scrollIntoView', () => {
            windowRef.document.querySelector = jasmine.createSpy().and.returnValue({ scrollIntoView: () => { } });
            component['scrollToBannerView']();
            expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
        });

        it('should not call scrollIntoView when el is null', () => {
            windowRef.document.querySelector = jasmine.createSpy().and.returnValue(null);
            component['scrollToBannerView']();
            expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
        });
    });

    describe('#updateTutorialsSteps', () => {
        it('should update corresponding step', () => {
            component.tutorialSteps = { step1: false, step2: false, step3: false, step4: false };
            component['updateTutorialsSteps']('2');
            expect(component.tutorialSteps.step2).toBeTruthy();
        });
    });

    describe('#validateOverlayBaseElement', () => {
        beforeEach(() => {
            windowRef.document.querySelector = jasmine.createSpy();
        });
        it('should handle when base class is available', () => {
            component.baseClass = 'lobby';
            component['validateOverlayBaseElement']();
            expect(windowRef.document.querySelector).toHaveBeenCalledWith('lobby');
        });
        it('should handle when base class is not available, and is wrapper', () => {
            component['validateOverlayBaseElement']();
            expect(windowRef.document.querySelector).toHaveBeenCalledWith('body');
        });
        it('should handle when base class is not available, and is wrapper false', () => {
            deviceService.isWrapper = false;
            component['validateOverlayBaseElement']();
            expect(windowRef.document.querySelector).toHaveBeenCalledWith('html, body');
        });
    });

    describe('#lobbyTutorialGATrack', () => {
        it('should call gtmService.push', () => {
            component['lobbyTutorialGATrack']('ShowdownCard');
            expect(gtmService.push).toHaveBeenCalled();
        });
    });
});
