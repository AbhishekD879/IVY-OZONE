import { PRE_OVERLAY } from '@app/fiveASideShowDown/constants/fiveaside-pre-overlay.constants';
import { FiveasidePreEventTutorialComponent
} from '@app/fiveASideShowDown/components/fiveasidePreEventTutorial/fiveaside-pre-event-tutorial.component';

describe('FiveasidePreEventTutorialComponent', () => {
    let component: FiveasidePreEventTutorialComponent;
    let rendererService,
        windowRef,
        deviceService, rectResponse, entryService, preService;
    beforeEach(() => {
        entryService = {
            trackGTMEvent: jasmine.createSpy('trackGTMEvent')
          };
          preService = {
            formParamArray: jasmine.createSpy('formParamArray')
          };
        rendererService = {
            renderer: {
                addClass: jasmine.createSpy('addClass'),
                removeClass: jasmine.createSpy('removeClass')
            }
        };
        rectResponse = {
            'x': 0,
            'y': 554.5108032226562,
            'width': 360.1190490722656,
            'height': 0,
            'top': 554.5108032226562,
            'right': 360.1190490722656,
            'bottom': 554.5108032226562,
            'left': 0
        };
        windowRef = {
            document: {
                querySelector: jasmine.createSpy('querySelector').and.returnValue({
                    parentNode: {}
                } as any),
                getElementById: jasmine.createSpy('querySelector').and.returnValue({
                    parentNode: {}
                } as any),
                getElementsByClassName: jasmine.createSpy('querySelector').and.returnValue({
                    parentNode: {}
                } as any)
            },
            nativeWindow: {
                scrollTo: jasmine.createSpy(),
                localStorage: {
                    setItem: jasmine.createSpy('setItem'),
                },
                innerWidth: '1800'
            }
        };
        deviceService = {
            isWrapper: true
        } as any;
        component = new FiveasidePreEventTutorialComponent(
            rendererService,
            windowRef,
            deviceService, entryService, preService);
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    describe('ngOnInit', () => {
        it('should load ngOnInit', () => {
            spyOn(component as any, 'scrollTo');
            spyOn(component as any, 'scrollToTop');
            spyOn(component as any, 'validateBaseElement');
            spyOn(component as any, 'initOverlayElements');
            spyOn(component as any, 'handleMultipleElements');
            spyOn(component as any, 'enableDisableIOSBodyScroll');
            component.ngOnInit();
            expect(component['handleMultipleElements']).toHaveBeenCalled();
            expect(windowRef.nativeWindow.localStorage.setItem).toHaveBeenCalled();
        });
    });

    describe('setTopValue for medium screens', () => {
        it('should set Top values for medium desktops', () => {
            windowRef.nativeWindow.innerWidth = '1536';
            component.setTopValue();
            expect(component.topValue).toEqual(34);
        });
    });

    describe('setTopValue for large screens', () => {
        it('should set Top values for large desktops', () => {
            windowRef.nativeWindow.innerWidth = '1800';
            component.setTopValue();
            expect(component.topValue).toEqual(64);
        });
    });

    describe('ngOnDestroy', () => {
        it('should load ngOnDestroy', () => {
            spyOn(component as any, 'onCloseWelcomeOverlay');
            spyOn(component as any, 'enableDisableIOSBodyScroll');
            component.ngOnDestroy();
            expect(component['onCloseWelcomeOverlay']).toHaveBeenCalled();
        });
    });

    describe('#scrollTo', () => {
        it('should call for scrollTo positive', () => {
            spyOn(component as any, 'checkForModule').and.returnValue(false);
            const element = [{
                scrollTo: jasmine.createSpy()
            }] as any;
            windowRef.document.getElementsByClassName.and.returnValue(element);
            component.scrollTo();
            expect(component['checkForModule']).toHaveBeenCalled();
            expect(element[0].scrollTo).toHaveBeenCalled();
        });
        it('should call for scrollTo Negative', () => {
            spyOn(component as any, 'checkForModule').and.returnValue(true);
            component.scrollTo();
            expect(component['checkForModule']).toHaveBeenCalled();
        });
    });

    describe('#enableDisableIOSBodyScroll', () => {
        it('should call addEventListener', () => {
            spyOn(component as any, 'preventScrollForTouchMove');
            spyOn(component as any, 'preventScrollForTouchStart');
            component['deviceService'] = { isIos: true } as any;
            const element = [{
                addEventListener: jasmine.createSpy(),
                removeEventListener: jasmine.createSpy()
            }] as any;
            windowRef.document.getElementsByClassName.and.returnValue(element);
            component.enableDisableIOSBodyScroll('add');
            expect(element[0].addEventListener).toHaveBeenCalled();
        });
        it('should call removeEventListener', () => {
            spyOn(component as any, 'preventScrollForTouchMove');
            spyOn(component as any, 'preventScrollForTouchStart');
            component['deviceService'] = { isIos: true } as any;
            const element = [{
                addEventListener: jasmine.createSpy(),
                removeEventListener: jasmine.createSpy()
            }] as any;
            windowRef.document.getElementsByClassName.and.returnValue(element);
            component.enableDisableIOSBodyScroll('remove');
            expect(element[0].removeEventListener).toHaveBeenCalled();
        });
        it('should not call eventListeners', () => {
            spyOn(component as any, 'preventScrollForTouchMove');
            spyOn(component as any, 'preventScrollForTouchStart');
            component['deviceService'] = { isIos: true } as any;
            const element = {
                addEventListener: jasmine.createSpy(),
                removeEventListener: jasmine.createSpy()
            } as any;
            windowRef.document.getElementsByClassName.and.returnValue(null);
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
            windowRef.document.getElementsByClassName.and.returnValue(null);
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
    });

    describe('onCloseWelcomeOverlay', () => {
        beforeEach(() => {
            spyOn(component as any, 'setDOMProperty');
        });
        it('should close the overlay', () => {
            component.clearOverlay.emit = jasmine.createSpy('modelChangeHandler.emit');
            spyOn(component as any, 'enableDisableIOSBodyScroll');
            component.onCloseWelcomeOverlay();
            expect(component.clearOverlay.emit).toHaveBeenCalled();
            expect(component['setDOMProperty']).toHaveBeenCalled();
        });
        it('should close the overlay (ngonDestroy)', () => {
            component.clearOverlay.emit = jasmine.createSpy('modelChangeHandler.emit');
            spyOn(component as any, 'enableDisableIOSBodyScroll');
            component.onCloseWelcomeOverlay('unsubscribe');
            expect(component.clearOverlay.emit).toHaveBeenCalled();
            expect(component['setDOMProperty']).toHaveBeenCalled();
        });
    });

    describe('goToPrizepool', () => {
        beforeEach(() => {
            spyOn(component as any, 'scrollTo');
            spyOn(component as any, 'initPrizePool');
            spyOn(component as any, 'getElementRect').and.returnValue(rectResponse);
            spyOn(component as any, 'handleMultipleElements');
            spyOn(component as any, 'setPrizePoolArea');
        });
        it('should check for module positive scenario for pool info', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(true);
            spyOn(component as any, 'scrollToTop');
            component.goToPrizepool();
            expect(component['scrollToTop']).toHaveBeenCalled();
            expect(component['checkForElement']).toHaveBeenCalled();
            expect(component['initPrizePool']).toHaveBeenCalled();
            expect(component['getElementRect']).toHaveBeenCalled();
            expect(component['setPrizePoolArea']).toHaveBeenCalled();
        });
        it('should check for module negative scenario', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(false);
            spyOn(component as any, 'goToRulesArea');
            spyOn(component as any, 'scrollToTop');
            component.goToPrizepool();
            expect(component['scrollToTop']).toHaveBeenCalled();
            expect(component['checkForElement']).toHaveBeenCalled();
            expect(component['handleMultipleElements']).toHaveBeenCalled();
            expect(component['goToRulesArea']).toHaveBeenCalled();
        });
    });

    describe('getPrizePoolInformation', () => {
        beforeEach(() => {
            spyOn(component as any, 'initPrizePool');
            spyOn(component as any, 'getElementRect').and.returnValue(rectResponse);
            spyOn(component as any, 'setPrizePoolArea');
        });
        it('should check for module positive scenario for pool info', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(true);
            component['getPrizePoolInformation']();
            expect(component['checkForElement']).toHaveBeenCalled();
            expect(component['initPrizePool']).toHaveBeenCalled();
            expect(component['getElementRect']).toHaveBeenCalled();
            expect(component['setPrizePoolArea']).toHaveBeenCalled();
        });
        it('should check for module negative scenario', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(false);
            component['getPrizePoolInformation']();
            expect(component['checkForElement']).toHaveBeenCalled();
            expect(component['initPrizePool']).toHaveBeenCalled();
            expect(component['getElementRect']).toHaveBeenCalled();
            expect(component['setPrizePoolArea']).toHaveBeenCalled();
        });
    });

    describe('goToRulesArea', () => {
        beforeEach(() => {
            spyOn(component as any, 'initRulesArea');
            spyOn(component as any, 'getElementRect').and.returnValue(rectResponse);
            spyOn(component as any, 'scrollWithElement');
            spyOn(component as any, 'setRulesArea');
        });
        it('should be called for rules area positive scenario', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(true);
            component.goToRulesArea();
            expect(component['checkForElement']).toHaveBeenCalled();
            expect(component['initRulesArea']).toHaveBeenCalled();
            expect(component['getElementRect']).toHaveBeenCalled();
            expect(component['setRulesArea']).toHaveBeenCalled();
        });
        it('should be called for rules area negative scenario', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(false);
            spyOn(component as any, 'handleMultipleElements');
            spyOn(component as any, 'goToEntryButton');
            component.goToRulesArea();
            expect(component['handleMultipleElements']).toHaveBeenCalled();
            expect(component['goToEntryButton']).toHaveBeenCalled();
        });
    });

    describe('goToEntryButton Build Another Button Scenario', () => {
        beforeEach(() => {
            spyOn(component as any, 'scrollTo');
            spyOn(component as any, 'initSeparateEntriesArea');
            spyOn(component as any, 'scrollElement');
            spyOn(component as any, 'setAnotherBuildAreaForEntries');
        });
        it('should check for module positive scenario for mobile', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(true);
            spyOn(component as any, 'checkForModule').and.returnValue(true);
            spyOn(component as any, 'getElementRect').and.returnValue(rectResponse);
            component.goToEntryButton();
            expect(component['checkForElement']).toHaveBeenCalled();
            expect(component['checkForModule']).toHaveBeenCalled();
            expect(component['initSeparateEntriesArea']).toHaveBeenCalled();
            expect(component['getElementRect']).toHaveBeenCalled();
            expect(component['setAnotherBuildAreaForEntries']).toHaveBeenCalled();
        });
        it('should check for module positive scenario not mobile', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(true);
            spyOn(component as any, 'checkForModule').and.returnValue(false);
            spyOn(component as any, 'getElementRect').and.returnValue(rectResponse);
            component.goToEntryButton();
            expect(component['checkForElement']).toHaveBeenCalled();
            expect(component['checkForModule']).toHaveBeenCalled();
            expect(component['initSeparateEntriesArea']).toHaveBeenCalled();
            expect(component['getElementRect']).toHaveBeenCalled();
            expect(component['setAnotherBuildAreaForEntries']).toHaveBeenCalled();
        });
        it('should check for module negative scenario', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(false);
            spyOn(component as any, 'getBuildBtnInformation');
            component.goToEntryButton();
            expect(component['checkForElement']).toHaveBeenCalled();
            expect(component['getBuildBtnInformation']).toHaveBeenCalled();
        });
    });

    describe('goToBuildAnotherTeamButton Build Another Button Scenario', () => {
        beforeEach(() => {
            spyOn(component as any, 'scrollTo');
            spyOn(component as any, 'scrollToTop');
            spyOn(component as any, 'initEntriesArea');
            spyOn(component as any, 'scrollElement');
            spyOn(component as any, 'setAnotherBuildArea');
        });
        it('should check for module positive scenario for mobile', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(true);
            spyOn(component as any, 'checkForModule').and.returnValue(true);
            spyOn(component as any, 'getElementRect').and.returnValue(rectResponse);
            component.goToBuildAnotherTeamButton();
            expect(component['checkForElement']).toHaveBeenCalled();
            expect(component['checkForModule']).toHaveBeenCalled();
            expect(component['initEntriesArea']).toHaveBeenCalled();
            expect(component['getElementRect']).toHaveBeenCalled();
            expect(component['setAnotherBuildArea']).toHaveBeenCalled();
        });
        it('should check for module positive scenario not mobile', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(true);
            spyOn(component as any, 'checkForModule').and.returnValue(false);
            spyOn(component as any, 'getElementRect').and.returnValue(rectResponse);
            component.goToBuildAnotherTeamButton();
            expect(component['checkForElement']).toHaveBeenCalled();
            expect(component['checkForModule']).toHaveBeenCalled();
            expect(component['initEntriesArea']).toHaveBeenCalled();
            expect(component['getElementRect']).toHaveBeenCalled();
            expect(component['setAnotherBuildArea']).toHaveBeenCalled();
        });
        it('should check for module negative scenario', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(false);
            spyOn(component as any, 'getBuildBtnInformation');
            component.goToBuildAnotherTeamButton();
            expect(component['checkForElement']).toHaveBeenCalled();
            expect(component['getBuildBtnInformation']).toHaveBeenCalled();
        });
    });

    describe('getBuildBtnInformation Build Button Scenario', () => {
        beforeEach(() => {
            windowRef = {
                document: {
                    querySelector: jasmine.createSpy('querySelector').and.returnValue(null)
                },
                nativeWindow: {
                    scrollTo: jasmine.createSpy()
                }
            };
            component = new FiveasidePreEventTutorialComponent(
                rendererService,
                windowRef,
                deviceService, entryService, preService);
            spyOn(component as any, 'initEntryButton');
            spyOn(component as any, 'scrollElement');
            spyOn(component as any, 'getElementRect').and.returnValue(rectResponse);
            spyOn(component as any, 'setBuildArea');
        });
        it('should check for module for positive scneario', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(true);
            spyOn(component as any, 'checkForModule').and.returnValue(true);
            component['getBuildBtnInformation']();
            expect(component['checkForElement']).toHaveBeenCalled();
            expect(component['checkForModule']).toHaveBeenCalled();
            expect(component['initEntryButton']).toHaveBeenCalled();
            expect(component['getElementRect']).toHaveBeenCalled();
            expect(component['setBuildArea']).toHaveBeenCalled();
        });
        it('should check for Deck positive scenario', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(true);
            spyOn(component as any, 'checkForModule').and.returnValue(false);
            component['getBuildBtnInformation']();
            expect(component['checkForElement']).toHaveBeenCalled();
            expect(component['checkForModule']).toHaveBeenCalled();
            expect(component['initEntryButton']).toHaveBeenCalled();
            expect(component['getElementRect']).toHaveBeenCalled();
            expect(component['setBuildArea']).toHaveBeenCalled();
        });
        it('should check for negative scenario', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(false);
            spyOn(component as any, 'handleMultipleElements');
            spyOn(component as any, 'getRulesButton');
            component['getBuildBtnInformation']();
            expect(component['checkForElement']).toHaveBeenCalled();
            expect(component['handleMultipleElements']).toHaveBeenCalled();
            expect(component['getRulesButton']).toHaveBeenCalled();
        });
    });

    describe('getRulesButton', () => {
        beforeEach(() => {
            windowRef = {
                document: {
                    querySelector: jasmine.createSpy('querySelector').and.returnValue({
                        parentNode: {}
                    } as any),
                    getElementById: jasmine.createSpy('querySelector').and.returnValue({
                        parentNode: {}
                    } as any)
                },
                nativeWindow: {
                    scrollTo: jasmine.createSpy()
                }
            };
            deviceService = {
                isWrapper: true
            } as any;
            component = new FiveasidePreEventTutorialComponent(
                rendererService,
                windowRef,
                deviceService, entryService, preService);
            spyOn(component as any, 'scrollTo');
            spyOn(component as any, 'initRulesButton');
            spyOn(component as any, 'getElementRect').and.returnValue(rectResponse);
            spyOn(component as any, 'setRulesButtonArea');
        });
        it('should be called for rules area', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(true);
            component.getRulesButton();
            expect(component['checkForElement']).toHaveBeenCalled();
            expect(component['initRulesButton']).toHaveBeenCalled();
            expect(component['getElementRect']).toHaveBeenCalled();
            expect(component['setRulesButtonArea']).toHaveBeenCalled();
        });
        it('should be called for rules area', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(false);
            spyOn(component as any, 'onCloseWelcomeOverlay');
            component.getRulesButton();
            expect(component['checkForElement']).toHaveBeenCalled();
            expect(component['onCloseWelcomeOverlay']).toHaveBeenCalled();
        });
    });

    describe('getEnded', () => {
        beforeEach(() => {
            spyOn(component as any, 'handleMultipleElements');
            spyOn(component as any, 'scrollTo');
        });
        it('should be called to complete tutorial', () => {
            component.clearOverlay.emit = jasmine.createSpy('modelChangeHandler.emit');
            spyOn(component as any, 'enableDisableIOSBodyScroll');
            component.getEnded();
            expect(component.clearOverlay.emit).toHaveBeenCalled();
            expect(component['handleMultipleElements']).toHaveBeenCalled();
        });
    });

    describe('scrollToTop', () => {
        it('should be called to scroll to top of page', () => {
            component['scrollToTop']();
        });
    });

    describe('validateBaseElement', () => {
        it('should handle when base class is available', () => {
            component.baseClass = 'welcome';
            component['validateBaseElement']();
            expect(windowRef.document.querySelector).toHaveBeenCalledWith('welcome');
        });
        it('should handle when base class is not available, and is wrapper', () => {
            component['validateBaseElement']();
            expect(windowRef.document.querySelector).toHaveBeenCalledWith('body');
        });
        it('should handle when base class is not available, and is wrapper false', () => {
            deviceService.isWrapper = false;
            component['validateBaseElement']();
            expect(windowRef.document.querySelector).toHaveBeenCalledWith('html, body');
        });
    });

    describe('initOverlayElements', () => {
        beforeEach(() => {
            rendererService = {
                renderer: {
                    addClass: jasmine.createSpy('addClass'),
                }
            };
            component = new FiveasidePreEventTutorialComponent(
                rendererService,
                windowRef,
                deviceService, entryService, preService);
        });
        it('should init rules overlay', () => {
            component['initOverlayElements']();
            expect(rendererService.renderer.addClass).toHaveBeenCalledWith(undefined, 'active');
        });
    });

    describe('handleMultipleElements', () => {
        it('should be used to handle multiple elements', () => {
            component['handleMultipleElements']([PRE_OVERLAY.INTRODUCTION_OVERLAY_ID],
                PRE_OVERLAY.ADD_CLASS, [PRE_OVERLAY.ACTIVE], [PRE_OVERLAY.CLASS]);
        });
    });

    describe('setDOMProperty', () => {
        it('should be used set the property for class', () => {
            component['setDOMProperty'](PRE_OVERLAY.INTRODUCTION_OVERLAY_ID,
                PRE_OVERLAY.ADD_CLASS, PRE_OVERLAY.ACTIVE, PRE_OVERLAY.CLASS);
        });
        it('should be used set the property for other then class', () => {
            component['setDOMProperty'](PRE_OVERLAY.INTRODUCTION_OVERLAY_ID,
                PRE_OVERLAY.ADD_CLASS, PRE_OVERLAY.ACTIVE, PRE_OVERLAY.CLASS);
        });
        it('should be used set the property for class', () => {
            component['setDOMProperty'](PRE_OVERLAY.INTRODUCTION_OVERLAY_ID,
                PRE_OVERLAY.ADD_CLASS, 'class', PRE_OVERLAY.CLASS);
        });
    });

    describe('setDOMProperty negative scenario', () => {
        beforeEach(() => {
            windowRef = {
                document: {
                    querySelector: jasmine.createSpy('querySelector').and.returnValue(null)
                }
            };
            component = new FiveasidePreEventTutorialComponent(
                rendererService,
                windowRef,
                deviceService, entryService, preService);
        });
        it('should be used set the null html', () => {
            component['setDOMProperty'](PRE_OVERLAY.INTRODUCTION_OVERLAY_ID,
                PRE_OVERLAY.ADD_CLASS, PRE_OVERLAY.ACTIVE, PRE_OVERLAY.CLASS);
        });
    });

    describe('checkForElement positive scenario', () => {
        it('should be used to check if we have element', () => {
            component['checkForElement'](['element']);
        });
    });

    describe('checkForElement negative scenario', () => {
        it('should be used to check if we have element', () => {
            component['checkForElement']([null]);
        });
    });

    describe('checkForElement negative scenario', () => {
        beforeEach(() => {
            windowRef = {
                document: {
                    querySelector: jasmine.createSpy('querySelector').and.returnValue(null)
                },
            };
            component = new FiveasidePreEventTutorialComponent(
                rendererService,
                windowRef,
                deviceService, entryService, preService);
        });
        it('should be used to check if we have element', () => {
            component['checkForElement'](['element']);
        });
    });

    describe('getElementRect', () => {
        beforeEach(() => {
            windowRef = {
                document: {
                    querySelector: jasmine.createSpy('querySelector').and.returnValue({
                        getBoundingClientRect: jasmine.createSpy('getBoundingClientRect').and.returnValue({
                            rectResponse
                        })
                    } as any)
                }
            };
            deviceService = {
                isWrapper: true
            } as any;
            component = new FiveasidePreEventTutorialComponent(
                rendererService,
                windowRef,
                deviceService, entryService, preService);
        });
        it('should be used to get element', () => {
            component['getElementRect']('element');
        });
    });

    describe('checkForModule return true', () => {
        beforeEach(() => {
            windowRef = {
                document: {
                    documentElement: {
                        className: {
                            includes: jasmine.createSpy().and.returnValue(true)
                        }
                    }
                }
            };
            deviceService = {
                isWrapper: true
            } as any;
            component = new FiveasidePreEventTutorialComponent(
                rendererService,
                windowRef,
                deviceService, entryService, preService);
        });
        it('should be used to check for module', () => {
            component['checkForModule']();
        });
    });

    describe('checkForModule return false', () => {
        beforeEach(() => {
            windowRef = {
                document: {
                    documentElement: {
                        className: {
                            includes: jasmine.createSpy().and.returnValue(false)
                        }
                    }
                }
            };
            deviceService = {
                isWrapper: true
            } as any;
            component = new FiveasidePreEventTutorialComponent(
                rendererService,
                windowRef,
                deviceService, entryService, preService);
        });
        it('should be used to check for module', () => {
            component['checkForModule']();
        });
    });

    describe('initPrizePool', () => {
        beforeEach(() => {
            spyOn(component as any, 'handleMultipleElements');
            spyOn(component as any, 'validateBaseElement');
        });
        it('should be used initialize the prize pool', () => {
            component['initPrizePool']();
            expect(component['handleMultipleElements']).toHaveBeenCalled();
            expect(component['validateBaseElement']).toHaveBeenCalled();
        });
    });

    describe('initRulesButton', () => {
        beforeEach(() => {
            spyOn(component as any, 'handleMultipleElements');
            spyOn(component as any, 'validateBaseElement');
        });
        it('should be used initialize the Rules Button', () => {
            component['initRulesButton']();
            expect(component['handleMultipleElements']).toHaveBeenCalled();
            expect(component['validateBaseElement']).toHaveBeenCalled();
        });
    });

    describe('initRulesArea', () => {
        beforeEach(() => {
            spyOn(component as any, 'scrollTo');
            spyOn(component as any, 'handleMultipleElements');
            spyOn(component as any, 'validateBaseElement');
        });
        it('should be used initialize the Rules Area', () => {
            component['initRulesArea']();
            expect(component['handleMultipleElements']).toHaveBeenCalled();
            expect(component['validateBaseElement']).toHaveBeenCalled();
        });
    });

    describe('initEntriesArea', () => {
        beforeEach(() => {
            spyOn(component as any, 'handleMultipleElements');
            spyOn(component as any, 'validateBaseElement');
        });
        it('should be used initialize the Entries Area', () => {
            component['initEntriesArea']();
            expect(component['handleMultipleElements']).toHaveBeenCalled();
            expect(component['validateBaseElement']).toHaveBeenCalled();
        });
    });

    describe('#initSeparateEntriesArea', () => {
        beforeEach(() => {
            spyOn(component as any, 'handleMultipleElements');
            spyOn(component as any, 'validateBaseElement');
        });
        it('should be used initialize the Entries Area', () => {
            component['initSeparateEntriesArea']();
            expect(component['handleMultipleElements']).toHaveBeenCalled();
            expect(component['validateBaseElement']).toHaveBeenCalled();
        });
    });

    describe('initEntryButton', () => {
        beforeEach(() => {
            spyOn(component as any, 'handleMultipleElements');
            spyOn(component as any, 'validateBaseElement');
        });
        it('should be used initialize the Entry Area', () => {
            component['initEntryButton']();
            expect(component['handleMultipleElements']).toHaveBeenCalled();
            expect(component['validateBaseElement']).toHaveBeenCalled();
        });
    });

    describe('scrollWithElement', () => {
        beforeEach(() => {
            spyOn(component as any, 'getElementRect').and.returnValue(rectResponse);
            spyOn(component as any, 'scrollSmooth');
        });
        it('should be used scroll with element', () => {
            component['scrollWithElement']('element');
            expect(component['getElementRect']).toHaveBeenCalled();
            expect(component['scrollSmooth']).toHaveBeenCalledWith(554.5108032226562);
        });
    });

    describe('scrollElement', () => {
        beforeEach(() => {
            spyOn(component as any, 'getElementRect').and.returnValue(rectResponse);
        });
        it('should be used scroll with element', () => {
            component['scrollElement']('element');
            expect(component['getElementRect']).toHaveBeenCalled();
            expect(windowRef.nativeWindow.scrollTo).toHaveBeenCalledWith(0, 554.5108032226562);
        });
    });

    describe('scrollSmooth', () => {
        it('should be used scroll with element', () => {
            component['scrollSmooth'](0);
            expect(windowRef.nativeWindow.scrollTo).toHaveBeenCalledWith({ top: 0, left: 0, behavior: 'smooth' });
        });
    });

    describe('setPrizePoolArea', () => {
        it('should be used to set prize pool area for module', () => {
            spyOn(component as any, 'checkForModule').and.returnValue(true);
            spyOn(component as any, 'setPrizeInformationModule');
            component['setPrizePoolArea'](rectResponse, rectResponse);
            expect(component['checkForModule']).toHaveBeenCalled();
            expect(component['setPrizeInformationModule']).toHaveBeenCalled();
        });
        it('should be used to set prize pool area for Dect', () => {
            spyOn(component as any, 'checkForModule').and.returnValue(false);
            spyOn(component as any, 'setPrizeInformationData');
            component['setPrizePoolArea'](rectResponse, rectResponse);
            expect(component['checkForModule']).toHaveBeenCalled();
            expect(component['setPrizeInformationData']).toHaveBeenCalled();
        });
    });

    describe('setPrizeInformationModule', () => {
        it('should be used to set prize pool area for module', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(true);
            spyOn(component as any, 'getElementRect').and.returnValue(rectResponse);
            spyOn(component as any, 'handleMultipleElements');
            component['setPrizeInformationModule'](rectResponse);
            expect(component['checkForElement']).toHaveBeenCalled();
            expect(component['handleMultipleElements']).toHaveBeenCalledTimes(2);
        });
        it('should be used to set prize pool area for Dect', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(false);
            spyOn(component as any, 'getElementRect').and.returnValue(rectResponse);
            spyOn(component as any, 'handleMultipleElements');
            component['setPrizeInformationModule'](rectResponse);
            expect(component['checkForElement']).toHaveBeenCalled();
            expect(component['handleMultipleElements']).toHaveBeenCalledTimes(2);
        });
    });

    describe('setPrizeInformationData', () => {
        it('should be used to set prize pool area for module', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(true);
            spyOn(component as any, 'handleMultipleElements');
            component['setPrizeInformationData'](rectResponse, rectResponse);
            expect(component['checkForElement']).toHaveBeenCalled();
            expect(component['handleMultipleElements']).toHaveBeenCalledTimes(2);
        });
        it('should be used to set prize pool area for Dect', () => {
            spyOn(component as any, 'checkForElement').and.returnValue(false);
            spyOn(component as any, 'handleMultipleElements');
            component['setPrizeInformationData'](rectResponse, rectResponse);
            expect(component['checkForElement']).toHaveBeenCalled();
            expect(component['handleMultipleElements']).toHaveBeenCalledTimes(2);
        });
    });

    describe('setRulesArea', () => {
        it('should be used to set rules area for module', () => {
            spyOn(component as any, 'checkForModule').and.returnValue(true);
            spyOn(component as any, 'handleMultipleElements');
            component['setRulesArea'](rectResponse, rectResponse);
            expect(component['checkForModule']).toHaveBeenCalled();
            expect(component['handleMultipleElements']).toHaveBeenCalledTimes(2);
        });
        it('should be used to set rules area for Dect', () => {
            spyOn(component as any, 'checkForModule').and.returnValue(false);
            spyOn(component as any, 'handleMultipleElements');
            component['setRulesArea'](rectResponse, rectResponse);
            expect(component['checkForModule']).toHaveBeenCalled();
            expect(component['handleMultipleElements']).toHaveBeenCalledTimes(2);
        });
    });

    describe('setAnotherBuildArea', () => {
        it('should be used to set Another build area for module', () => {
            spyOn(component as any, 'getElementRect').and.returnValue(rectResponse);
            spyOn(component as any, 'handleMultipleElements');
            spyOn(component as any, 'checkForModule').and.returnValue(true);
            component['setAnotherBuildArea'](rectResponse);
            expect(component['checkForModule']).toHaveBeenCalled();
            expect(component['handleMultipleElements']).toHaveBeenCalledTimes(5);
        });
        it('should be used to set Another build area for dect', () => {
            spyOn(component as any, 'getElementRect').and.returnValue(rectResponse);
            spyOn(component as any, 'handleMultipleElements');
            spyOn(component as any, 'checkForModule').and.returnValue(false);
            component['setAnotherBuildArea'](rectResponse);
            expect(component['checkForModule']).toHaveBeenCalled();
            expect(component['handleMultipleElements']).toHaveBeenCalledTimes(7);
        });
    });

    describe('setAnotherBuildAreaForEntries', () => {
        it('should be used to set Another build area for module', () => {
            spyOn(component as any, 'getElementRect').and.returnValue(rectResponse);
            spyOn(component as any, 'handleMultipleElements');
            spyOn(component as any, 'checkForModule').and.returnValue(true);
            component['setAnotherBuildAreaForEntries']();
            expect(component['checkForModule']).toHaveBeenCalled();
            expect(component['handleMultipleElements']).toHaveBeenCalledTimes(2);
        });
        it('should be used to set Another build area for dect', () => {
            spyOn(component as any, 'getElementRect').and.returnValue(rectResponse);
            spyOn(component as any, 'handleMultipleElements');
            spyOn(component as any, 'checkForModule').and.returnValue(false);
            component['setAnotherBuildAreaForEntries']();
            expect(component['checkForModule']).toHaveBeenCalled();
            expect(component['handleMultipleElements']).toHaveBeenCalledTimes(4);
        });
    });

    describe('setBuildArea', () => {
        it('should be used to set build area for module', () => {
            spyOn(component as any, 'handleMultipleElements');
            spyOn(component as any, 'checkForModule').and.returnValue(true);
            component['setBuildArea'](rectResponse, rectResponse);
            expect(component['checkForModule']).toHaveBeenCalled();
            expect(component['handleMultipleElements']).toHaveBeenCalledTimes(4);
        });
        it('should be used to set build area for dect', () => {
            spyOn(component as any, 'handleMultipleElements');
            spyOn(component as any, 'checkForModule').and.returnValue(false);
            component['setBuildArea'](rectResponse, rectResponse);
            expect(component['checkForModule']).toHaveBeenCalled();
            expect(component['handleMultipleElements']).toHaveBeenCalledTimes(6);
        });
    });

    describe('setRulesButtonArea', () => {
        it('should be used to set build area for module', () => {
            spyOn(component as any, 'handleMultipleElements');
            spyOn(component as any, 'checkForModule').and.returnValue(true);
            component['setRulesButtonArea'](rectResponse);
            expect(component['checkForModule']).toHaveBeenCalled();
            expect(component['handleMultipleElements']).toHaveBeenCalledTimes(2);
        });
        it('should be used to set build area for dect', () => {
            spyOn(component as any, 'handleMultipleElements');
            spyOn(component as any, 'getElementRect').and.returnValue(rectResponse);
            spyOn(component as any, 'checkForModule').and.returnValue(false);
            component['setRulesButtonArea'](rectResponse);
            expect(component['checkForModule']).toHaveBeenCalled();
            expect(component['handleMultipleElements']).toHaveBeenCalledTimes(2);
        });
    });
});
