import { of } from 'rxjs';
import { FiveASideLiveEventOverlayComponent } from './five-a-side-live-event-overlay.component';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { LIVE_OVERLAY, LOBBY_OVERLAY } from '../../constants/constants';

describe('FiveASideLiveEventOverlayComponent', () => {
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
  const boundFunc = () => ({ 'top': 50, 'left': 50, 'right': 50, 'bottom': '50', 'height': 50 });

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
        },
        setTimeout: jasmine.createSpy('setTimeout').and.callFake(fn => fn()),
        clearTimeout: jasmine.createSpy('clearTimeout')
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
  describe('#ngOnInit', () => {
    it('should call required methods in init', () => {
      spyOn(component as any, 'validateOverlayBaseElement');
      spyOn(component as any, 'initLiveOverlayElements');
      spyOn(component as any, 'enableDisableIOSBodyScroll');
      component.ngOnInit();
      expect(component['validateOverlayBaseElement']).toHaveBeenCalled();
      expect(component['initLiveOverlayElements']).toHaveBeenCalled();
    });
  });

  describe('#ngOnDestroy', () => {
    it('should call required methods in ngOnDestroy', () => {
      spyOn(component as any, 'onCloseLiveOverlay');
      spyOn(component as any, 'enableDisableIOSBodyScroll');
      component.ngOnDestroy();
      expect(component['onCloseLiveOverlay']).toHaveBeenCalled();
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
      const event = { preventDefault: jasmine.createSpy(), target: { id: 'close-div' } };
      component['preventScrollForTouchStart'](event as any);
      expect(event.preventDefault).not.toHaveBeenCalled();
    });
    it('should not call preventDefault', () => {
      const event = { preventDefault: jasmine.createSpy(), target: { id: 'new-div' } };
      component['preventScrollForTouchStart'](event as any);
      expect(event.preventDefault).toHaveBeenCalled();
    });

    it('should not call preventDefault when element is button', () => {
      const event = { preventDefault: jasmine.createSpy(), target: { localName: 'button' } };
      component['preventScrollForTouchStart'](event as any);
      expect(event.preventDefault).not.toHaveBeenCalled();
    });
  });

  describe('#initEntryExpandedListener', () => {
    beforeEach(() => {
      component['pubsubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === LIVE_OVERLAY.ENTRY_OPENED_TUTORIAL_OVERLAY) {
          fn();
        }
      });
    });
    it('should call required methods in initEntryExpandedListener', () => {
      spyOn(component as any, 'entrySummaryMethod');
      component.entryUpdateReceived = false;
      component.initEntryExpandedListener();
      expect(component['entrySummaryMethod']).toHaveBeenCalled();
    });
    it('should not call required methods in initEntryExpandedListener', () => {
      spyOn(component as any, 'entrySummaryMethod');
      component.entryUpdateReceived = true;
      component.initEntryExpandedListener();
      expect(component['entrySummaryMethod']).not.toHaveBeenCalled();
    });
    it('should call onClickNext when all conditions are met', () => {
      spyOn(component as any, 'entrySummaryMethod');
      spyOn(component as any, 'onClickNext');
      component.entryUpdateReceived = true;
      component['viewReloaded'] = false;
      component['activeStep'] = '4';
      component.initEntryExpandedListener();
      expect(component['onClickNext']).toHaveBeenCalled();
    });

    it('should not call onClickNext when activeStep is not 4', () => {
      spyOn(component as any, 'entrySummaryMethod');
      spyOn(component as any, 'onClickNext');
      component.entryUpdateReceived = true;
      component['viewReloaded'] = false;
      component['activeStep'] = '3';
      component.initEntryExpandedListener();
      expect(component['onClickNext']).not.toHaveBeenCalled();
    });

    it('should not call onClickNext when viewReloaded is true', () => {
      spyOn(component as any, 'entrySummaryMethod');
      spyOn(component as any, 'onClickNext');
      component.entryUpdateReceived = true;
      component['viewReloaded'] = true;
      component['activeStep'] = '4';
      component.initEntryExpandedListener();
      expect(component['onClickNext']).not.toHaveBeenCalled();
    });

    it('should not call onClickNext when viewReloaded is true', () => {
      spyOn(component as any, 'entrySummaryMethod');
      spyOn(component as any, 'onClickNext');
      component.entryUpdateReceived = false;
      component['viewReloaded'] = false;
      component['activeStep'] = '4';
      component.initEntryExpandedListener();
      expect(component['onClickNext']).not.toHaveBeenCalled();
    });
  });

  describe('#entryExpandTimeoutListener', () => {
    it('should call setTimeout', () => {
      spyOn(component as any, 'skipToNextEntryUpdate');
      component.entryExpandTimeoutListener();
      expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), LIVE_OVERLAY.TIMEOUT_DURATION);
    });
  });

  describe('#skipToNextEntryUpdate', () => {
    it('should call onClickNext when entry update not received', () => {
      spyOn(component as any, 'onClickNext');
      component.entryUpdateReceived = false;
      component.skipToNextEntryUpdate();
      expect(component['onClickNext']).toHaveBeenCalled();
    });
    it('should not call onClickNext when entry update not received', () => {
      spyOn(component as any, 'onClickNext');
      component.entryUpdateReceived = true;
      component.skipToNextEntryUpdate();
      expect(component['onClickNext']).not.toHaveBeenCalled();
    });
  });

  describe('#onCloseLiveOverlay', () => {
    it('should call required methods in onCloseLiveOverlay', () => {
      spyOn(component as any, 'liveTutorialGATrack');
      spyOn(component as any, 'setElementDOMProperty');
      spyOn(component as any, 'enableDisableIOSBodyScroll');
      component.clearOverlay.emit = jasmine.createSpy('modelChangeHandler.emit');
      component.onCloseLiveOverlay('close');
      expect(component.clearOverlay.emit).toHaveBeenCalled();
      expect(component['liveTutorialGATrack']).toHaveBeenCalled();
    });
    it('should call required methods in onCloseLiveOverlay(without param)', () => {
      spyOn(component as any, 'liveTutorialGATrack');
      spyOn(component as any, 'setElementDOMProperty');
      spyOn(component as any, 'enableDisableIOSBodyScroll');
      component.clearOverlay.emit = jasmine.createSpy('modelChangeHandler.emit');
      component.onCloseLiveOverlay();
      expect(component.clearOverlay.emit).toHaveBeenCalled();
    });
  });

  describe('#onClickNext', () => {
    beforeEach(() => {
      spyOn(component as any, 'liveTutorialGATrack');
      spyOn(component as any, 'updateTutorialsSteps');
    });
    it('should call required methods when step is 2', () => {
      spyOn(component as any, 'showFiveASideTeamProgress');
      component.onClickNext('2');
      expect(component['updateTutorialsSteps']).toHaveBeenCalled();
      expect(component['showFiveASideTeamProgress']).toHaveBeenCalled();
    });

    it('should call required methods when step is 3', () => {
      spyOn(component as any, 'scrollToBannerView');
      spyOn(component as any, 'showFiveASideTeamProgressExpanded');
      component.onClickNext('3');
      expect(component['updateTutorialsSteps']).toHaveBeenCalled();
      expect(component['showFiveASideTeamProgressExpanded']).toHaveBeenCalled();
    });

    it('should call required methods when step is 4', () => {
      spyOn(component as any, 'scrollToBannerView');
      spyOn(component as any, 'showEntryProgressbarTutorial');
      component.onClickNext('4');
      expect(component['updateTutorialsSteps']).toHaveBeenCalled();
      expect(component['showEntryProgressbarTutorial']).toHaveBeenCalled();
    });

    it('should call required methods when step is 5', () => {
      spyOn(component as any, 'scrollToBannerView');
      spyOn(component as any, 'showLeaderboardEntriesTutorial');
      component.onClickNext('5');
      expect(component['updateTutorialsSteps']).toHaveBeenCalled();
      expect(component['showLeaderboardEntriesTutorial']).toHaveBeenCalled();
    });

    it('should call required methods when step is FINISH', () => {
      spyOn(component as any, 'onCloseLiveOverlay');
      component.onClickNext(LOBBY_OVERLAY.FINISH);
      expect(component['onCloseLiveOverlay']).toHaveBeenCalled();
    });

    it('should not any methods when it is default case', () => {
      component.onClickNext('abc');
      expect(component['updateTutorialsSteps']).not.toHaveBeenCalled();
    });
  });

  describe('#showFiveASideTeamProgress', () => {
    beforeEach(() => {
      spyOn(component as any, 'scrollToBannerView');
      spyOn(component as any, 'entrySummaryMethod');
      spyOn(component as any, 'setDomPropertiesForTeamProgress');
      spyOn(component as any, 'liveTutorialGATrack');
      spyOn(component as any, 'onClickNext');
      spyOn(component as any, 'scrollToTopForDesktop');
    });

    it('should call methods when all conditions are met', () => {
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return {
            querySelector: jasmine.createSpy().and.returnValue(() => { })
          };
        } else if (args === LIVE_OVERLAY.ID_MY_ENTRY_YOUR_TEAM) {
          return {
            querySelector: jasmine.createSpy().and.returnValue(() => { })
          };
        }
      });
      component['showFiveASideTeamProgress'](LIVE_OVERLAY.SEL_ENTRY_SUMMARY, LIVE_OVERLAY.ID_MY_ENTRY_YOUR_TEAM);
      expect(component['setDomPropertiesForTeamProgress']).not.toHaveBeenCalled();
    });

    it('should call methods when entryEl is null', () => {
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return null;
        } else if (args === LIVE_OVERLAY.ID_MY_ENTRY_YOUR_TEAM) {
          return {
            querySelector: jasmine.createSpy().and.returnValue(() => { })
          };
        }
      });
      component['showFiveASideTeamProgress'](LIVE_OVERLAY.SEL_ENTRY_SUMMARY, LIVE_OVERLAY.ID_MY_ENTRY_YOUR_TEAM);
      expect(component['setDomPropertiesForTeamProgress']).not.toHaveBeenCalled();
    });

    it('should call methods when isEntryExpanded is null', () => {
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return {
            querySelector: jasmine.createSpy().and.returnValue({})
          };
        } else if (args === LIVE_OVERLAY.ID_MY_ENTRY_YOUR_TEAM) {
          return {
            querySelector: jasmine.createSpy().and.returnValue(() => { })
          };
        } else if (args === LIVE_OVERLAY.ID_SUMMARY_EXPANDED) {
          return {
            querySelector: jasmine.createSpy().and.returnValue(null)
          };
        }
      });
      component['showFiveASideTeamProgress'](LIVE_OVERLAY.SEL_ENTRY_SUMMARY, LIVE_OVERLAY.ID_MY_ENTRY_YOUR_TEAM);
      expect(component['entrySummaryMethod']).toHaveBeenCalled();
    });

    it('should call methods when highlightEl is null', () => {
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return {
            querySelector: jasmine.createSpy().and.returnValue({})
          };
        } else if (args === LIVE_OVERLAY.ID_MY_ENTRY_YOUR_TEAM) {
          return null;
        } else if (args === LIVE_OVERLAY.ID_SUMMARY_EXPANDED) {
          return {
            querySelector: jasmine.createSpy().and.returnValue(null)
          };
        }
      });
      component['showFiveASideTeamProgress'](LIVE_OVERLAY.SEL_ENTRY_SUMMARY, LIVE_OVERLAY.ID_MY_ENTRY_YOUR_TEAM);
      expect(component['setDomPropertiesForTeamProgress']).not.toHaveBeenCalled();
    });

    it('should call methods when all conditions are met with SEL_MYENTRY_WIDGET query selectors', () => {
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return {
            querySelector: jasmine.createSpy().and.callFake((arg) => {
              if (arg === LIVE_OVERLAY.ID_SUMMARY_EXPANDED) {
                return {};
              } else if (arg === LIVE_OVERLAY.SEL_ENTRY_SUMMARY) {
                return {};
              }
            })
          };
        } else if (args === LIVE_OVERLAY.ID_MY_ENTRY_YOUR_TEAM) {
          return {
            querySelector: jasmine.createSpy().and.returnValue(() => { })
          };
        }
      });
      component['showFiveASideTeamProgress'](LIVE_OVERLAY.SEL_ENTRY_SUMMARY, LIVE_OVERLAY.ID_MY_ENTRY_YOUR_TEAM);
      expect(component['setDomPropertiesForTeamProgress']).not.toHaveBeenCalled();
    });

    it('should call methods when all conditions are met with SEL_MYENTRY_WIDGET query selectors are null', () => {
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return {
            querySelector: jasmine.createSpy().and.callFake((arg) => {
              if (arg === LIVE_OVERLAY.ID_SUMMARY_EXPANDED) {
                return null;
              } else if (arg === LIVE_OVERLAY.SEL_ENTRY_SUMMARY) {
                return null;
              }
            })
          };
        } else if (args === LIVE_OVERLAY.ID_MY_ENTRY_YOUR_TEAM) {
          return {
            querySelector: jasmine.createSpy().and.returnValue(() => { })
          };
        }
      });
      component['showFiveASideTeamProgress'](LIVE_OVERLAY.SEL_ENTRY_SUMMARY, LIVE_OVERLAY.ID_MY_ENTRY_YOUR_TEAM);
      expect(component['setDomPropertiesForTeamProgress']).not.toHaveBeenCalled();
    });
    it('should call setDomPropertiesForTeamProgress', () => {
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return {
            querySelector: jasmine.createSpy().and.returnValue({}).
              and.callFake((arg) => {
                if (arg === LIVE_OVERLAY.ID_SUMMARY_EXPANDED) {
                  return null;
                } else if (arg === LIVE_OVERLAY.SEL_ENTRY_SUMMARY) {
                  return {
                    querySelector: jasmine.createSpy().and.returnValue({})
                  };
                }
              })
          };
        } else if (args === LIVE_OVERLAY.ID_MY_ENTRY_YOUR_TEAM) {
          return {
            querySelector: jasmine.createSpy().and.returnValue(null)
          };
        } else if (args === LIVE_OVERLAY.ID_SUMMARY_EXPANDED) {
          return {
            querySelector: jasmine.createSpy().and.returnValue(null)
          };
        }
      });
      component['showFiveASideTeamProgress'](LIVE_OVERLAY.SEL_ENTRY_SUMMARY, LIVE_OVERLAY.ID_MY_ENTRY_YOUR_TEAM);
      expect(component['setDomPropertiesForTeamProgress']).toHaveBeenCalled();
    });
  });

  describe('#setDomPropertiesForTeamProgress', () => {
    it('should call required methods', () => {
      spyOn(component as any, 'setElementDOMProperty');
      spyOn(component as any, 'unsetNativeBackgroundColor');
      component['setDomPropertiesForTeamProgress']('', { getBoundingClientRect: boundFunc } as any);
      expect(component['unsetNativeBackgroundColor']).toHaveBeenCalled();
    });
  });

  describe('#entrySummaryMethod', () => {
    it('should call required methods', () => {
      spyOn(component as any, 'updateTutorialsSteps');
      spyOn(component as any, 'setDomPropertiesEntryProgress');
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return {
            querySelector: jasmine.createSpy().and.returnValue({
              querySelector: boundFunc
            }),
            scrollIntoView: () => { }
          };
        } else if (args === LIVE_OVERLAY.ID_LEGS_LIST_DISPLAY) {
          return {
            children: [{}, { getBoundingClientRect: boundFunc }, {}]
          };
        } else if (args === LIVE_OVERLAY.ID_SUMMARY_EXPANDED) {
          return {
            querySelector: jasmine.createSpy().and.returnValue(null)
          };
        }
      });
      component['entrySummaryMethod']('');
      expect(component['setDomPropertiesEntryProgress']).toHaveBeenCalled();
    });

    it('should call onClickNext when height is zero', () => {
      spyOn(component as any, 'updateTutorialsSteps');
      spyOn(component as any, 'setDomPropertiesEntryProgress');
      spyOn(component as any, 'onClickNext');
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return {
            querySelector: jasmine.createSpy().and.returnValue({
              querySelector: boundFunc
            }),
            scrollIntoView: () => { }
          };
        } else if (args === LIVE_OVERLAY.ID_LEGS_LIST_DISPLAY) {
          return {
            children: [{}, {
              getBoundingClientRect:
                () => ({ 'top': 50, 'left': 50, 'right': 50, 'bottom': '50', 'height': 0 })
            }, {}]
          };
        } else if (args === LIVE_OVERLAY.ID_SUMMARY_EXPANDED) {
          return {
            querySelector: jasmine.createSpy().and.returnValue(null)
          };
        }
      });
      component['entrySummaryMethod']('');
      expect(component['onClickNext']).toHaveBeenCalled();
    });

    it('should call required methods when children length is 1', () => {
      spyOn(component as any, 'updateTutorialsSteps');
      spyOn(component as any, 'setDomPropertiesEntryProgress');
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return {
            querySelector: jasmine.createSpy().and.returnValue({
              querySelector: boundFunc
            }),
            scrollIntoView: () => { }
          };
        } else if (args === LIVE_OVERLAY.ID_LEGS_LIST_DISPLAY) {
          return {
            children: [{ getBoundingClientRect: () => boundFunc }]
          };
        } else if (args === LIVE_OVERLAY.ID_SUMMARY_EXPANDED) {
          return {
            querySelector: jasmine.createSpy().and.returnValue(null)
          };
        }
      });
      component['entrySummaryMethod']('');
      expect(component['setDomPropertiesEntryProgress']).toHaveBeenCalled();
    });

    it('should call required methods when children length is 0', () => {
      spyOn(component as any, 'updateTutorialsSteps');
      spyOn(component as any, 'setDomPropertiesEntryProgress');
      spyOn(component as any, 'onClickNext');
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return {
            querySelector: jasmine.createSpy().and.returnValue({
              querySelector: boundFunc
            }),
            scrollIntoView: () => { }
          };
        } else if (args === LIVE_OVERLAY.ID_LEGS_LIST_DISPLAY) {
          return {
            children: []
          };
        } else if (args === LIVE_OVERLAY.ID_SUMMARY_EXPANDED) {
          return {
            querySelector: jasmine.createSpy().and.returnValue(null)
          };
        }
      });
      component['entrySummaryMethod']('');
      expect(component['onClickNext']).toHaveBeenCalled();
    });
  });

  it('should call required methods when children length is 0', () => {
    spyOn(component as any, 'updateTutorialsSteps');
    spyOn(component as any, 'setDomPropertiesEntryProgress');
    spyOn(component as any, 'onClickNext');
    windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
      if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
        return null;
      } else if (args === LIVE_OVERLAY.ID_LEGS_LIST_DISPLAY) {
        return null;
      } else if (args === LIVE_OVERLAY.ID_SUMMARY_EXPANDED) {
        return {
          querySelector: jasmine.createSpy().and.returnValue(null)
        };
      }
    });
    component['entrySummaryMethod']('');
    expect(component['onClickNext']).toHaveBeenCalled();
  });

  it('should call required methods when entrySummaryEl is null', () => {
    spyOn(component as any, 'updateTutorialsSteps');
    spyOn(component as any, 'setDomPropertiesEntryProgress');
    spyOn(component as any, 'onClickNext');
    windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
      if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
        return null;
      } else if (args === LIVE_OVERLAY.ID_LEGS_LIST_DISPLAY) {
        return null;
      } else if (args === LIVE_OVERLAY.ID_SUMMARY_EXPANDED) {
        return {
          querySelector: jasmine.createSpy().and.returnValue(null)
        };
      }
    });
    component['entrySummaryMethod']('');
    expect(component['onClickNext']).toHaveBeenCalled();
  });

  describe('#setDomPropertiesEntryProgress', () => {
    it('should call setElementDOMProperty method with properties', () => {
      spyOn(component as any, 'setElementDOMProperty');
      windowRef.document.querySelector = jasmine.createSpy().and.returnValue({ getBoundingClientRect: boundFunc });
      component['setDomPropertiesEntryProgress']('#id', boundFunc() as any);
      expect(component['setElementDOMProperty']).toHaveBeenCalled();
    });
    it('should not call setElementDOMProperty method with properties', () => {
      spyOn(component as any, 'setElementDOMProperty');
      windowRef.document.querySelector = jasmine.createSpy().and.returnValue(null);
      component['setDomPropertiesEntryProgress']('#id', boundFunc() as any);
      expect(component['setElementDOMProperty']).not.toHaveBeenCalled();
    });
  });

  describe('#showFiveASideTeamProgressExpanded', () => {
    beforeEach(() => {
      spyOn(component as any, 'scrollToBannerView');
      spyOn(component as any, 'onClickNext');
      spyOn(component as any, 'liveTutorialGATrack');
      spyOn(component as any, 'entryExpandTimeoutListener');
    });
    it('should call required methods in showFiveASideTeamProgressExpanded', () => {
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return {
            querySelector: jasmine.createSpy().and.returnValue({
              querySelector: boundFunc,
              click: () => { }
            }),
            scrollIntoView: () => { }
          };
        }
      });
      component.isMyEntryPresent = true;
      component['showFiveASideTeamProgressExpanded']();
      expect(component['onClickNext']).not.toHaveBeenCalled();
    });

    it('should skip to next screen when entryEl is null', () => {
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return {
            querySelector: jasmine.createSpy().and.returnValue(null),
            scrollIntoView: () => { }
          };
        }
      });
      component.isMyEntryPresent = true;
      component['showFiveASideTeamProgressExpanded']();
      expect(component['onClickNext']).toHaveBeenCalled();
    });
    it('should skip to next screen when entrySummaryEl is null', () => {
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return null;
        }
      });
      component.isMyEntryPresent = true;
      component['showFiveASideTeamProgressExpanded']();
      expect(component['onClickNext']).toHaveBeenCalled();
    });

    it('should skip to next screen when isMyEntryPresent is false', () => {
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return null;
        }
      });
      component.isMyEntryPresent = false;
      component['showFiveASideTeamProgressExpanded']();
      expect(component['onClickNext']).toHaveBeenCalled();
    });
  });

  describe('#showEntryProgressbarTutorial', () => {
    beforeEach(() => {
      spyOn(component as any, 'scrollToBannerView');
      spyOn(component as any, 'onClickNext');
      spyOn(component as any, 'setElementDOMProperty');
      spyOn(component as any, 'setDomPropertiesEntryProgressBar');
      spyOn(component as any, 'liveTutorialGATrack');
    });
    it('should call required methods in showFiveASideTeamProgressExpanded', () => {
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return {
            querySelector: jasmine.createSpy().and.returnValue(
              { click: () => { } }
            ),
            scrollIntoView: () => { }
          };
        } else if (args === LIVE_OVERLAY.ID_PROGRESSBAR_OVERLAY) {
          return { children: [1, 2, 3] };
        } else if (args === LIVE_OVERLAY.SEL_MYENTRY_PROGRESS) {
          return {};
        } else if (args === LIVE_OVERLAY.ID_ENTRY_PROGRESS_INFO) {
          return {};
        }
      });
      component.isMyEntryPresent = true;
      component['showEntryProgressbarTutorial'](LIVE_OVERLAY.SEL_MYENTRY_PROGRESS, LIVE_OVERLAY.ID_ENTRY_PROGRESS_INFO);
      expect(component['onClickNext']).not.toHaveBeenCalled();
    });

    it('should call required methods when entryEl is null', () => {
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return {
            querySelector: jasmine.createSpy().and.returnValue(null)
          };
        } else if (args === LIVE_OVERLAY.ID_PROGRESSBAR_OVERLAY) {
          return { children: [1, 2, 3] };
        } else if (args === LIVE_OVERLAY.SEL_MYENTRY_PROGRESS) {
          return {};
        } else if (args === LIVE_OVERLAY.ID_ENTRY_PROGRESS_INFO) {
          return {};
        }
      });
      component.isMyEntryPresent = true;
      component['showEntryProgressbarTutorial'](LIVE_OVERLAY.SEL_MYENTRY_PROGRESS, LIVE_OVERLAY.ID_ENTRY_PROGRESS_INFO);
      expect(component['onClickNext']).not.toHaveBeenCalled();
    });

    it('should call required methods when entriesProgressBar is null', () => {
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return {
            querySelector: jasmine.createSpy().and.returnValue(null)
          };
        } else if (args === LIVE_OVERLAY.ID_PROGRESSBAR_OVERLAY) {
          return null;
        } else if (args === LIVE_OVERLAY.SEL_MYENTRY_PROGRESS) {
          return {};
        } else if (args === LIVE_OVERLAY.ID_ENTRY_PROGRESS_INFO) {
          return {};
        }
      });
      component.isMyEntryPresent = true;
      component['showEntryProgressbarTutorial'](LIVE_OVERLAY.SEL_MYENTRY_PROGRESS, LIVE_OVERLAY.ID_ENTRY_PROGRESS_INFO);
      expect(component['onClickNext']).toHaveBeenCalled();
    });


    it('should call required methods when highlightEl is null', () => {
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return {
            querySelector: jasmine.createSpy().and.returnValue(null)
          };
        } else if (args === LIVE_OVERLAY.ID_PROGRESSBAR_OVERLAY) {
          return {};
        } else if (args === LIVE_OVERLAY.SEL_MYENTRY_PROGRESS) {
          return {};
        } else if (args === LIVE_OVERLAY.ID_ENTRY_PROGRESS_INFO) {
          return null;
        }
      });
      component.isMyEntryPresent = true;
      component['showEntryProgressbarTutorial'](LIVE_OVERLAY.SEL_MYENTRY_PROGRESS, LIVE_OVERLAY.ID_ENTRY_PROGRESS_INFO);
      expect(component['onClickNext']).toHaveBeenCalled();
    });

    it('should call required methods when toBeHighlightEl is null', () => {
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return {
            querySelector: jasmine.createSpy().and.returnValue(null)
          };
        } else if (args === LIVE_OVERLAY.ID_PROGRESSBAR_OVERLAY) {
          return {};
        } else if (args === LIVE_OVERLAY.SEL_MYENTRY_PROGRESS) {
          return null;
        } else if (args === LIVE_OVERLAY.ID_ENTRY_PROGRESS_INFO) {
          return {};
        }
      });
      component.isMyEntryPresent = true;
      component['showEntryProgressbarTutorial'](LIVE_OVERLAY.SEL_MYENTRY_PROGRESS, LIVE_OVERLAY.ID_ENTRY_PROGRESS_INFO);
      expect(component['onClickNext']).toHaveBeenCalled();
    });


    it('should call required methods when entrySummaryEl is null', () => {
      windowRef.document.querySelector = jasmine.createSpy().and.callFake((args) => {
        if (args === LIVE_OVERLAY.SEL_MYENTRY_WIDGET) {
          return null;
        } else if (args === LIVE_OVERLAY.ID_PROGRESSBAR_OVERLAY) {
          return {};
        } else if (args === LIVE_OVERLAY.SEL_MYENTRY_PROGRESS) {
          return null;
        } else if (args === LIVE_OVERLAY.ID_ENTRY_PROGRESS_INFO) {
          return {};
        }
      });
      component.isMyEntryPresent = true;
      component['showEntryProgressbarTutorial'](LIVE_OVERLAY.SEL_MYENTRY_PROGRESS, LIVE_OVERLAY.ID_ENTRY_PROGRESS_INFO);
      expect(component['onClickNext']).toHaveBeenCalled();
    });

  });

  describe('#setDomPropertiesEntryProgressBar', () => {
    it('should call required methods in setDomPropertiesEntryProgressBar', () => {
      spyOn(component as any, 'setElementDOMProperty');
      spyOn(component as any, 'unsetNativeBackgroundColor');
      component['setDomPropertiesEntryProgressBar']('#id', { scrollIntoView: () => { }, getBoundingClientRect: boundFunc } as any);
      expect(component['setElementDOMProperty']).toHaveBeenCalled();
    });
  });

  describe('#showLeaderboardEntriesTutorial', () => {
    beforeEach(() => {
      spyOn(component as any, 'scrollToBannerView');
      spyOn(component as any, 'onClickNext');
      spyOn(component as any, 'setElementDOMProperty');
      spyOn(component as any, 'unsetNativeBackgroundColor');
      spyOn(component as any, 'liveTutorialGATrack');
      spyOn(component as any, 'calculateLeaderboardEntriesHeight');
    });
    it('should call required methods in showLeaderboardEntriesTutorial', () => {
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

  describe('#initLiveOverlayElements', () => {
    it('should init rules live leaderboard overlay', () => {
      spyOn(component as any, 'liveTutorialGATrack');
      component['initLiveOverlayElements']();
      expect(rendererService.renderer.addClass).toHaveBeenCalledWith(undefined, 'active');
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
    it('should call changeDetectorRef', () => {
      component['scrollToBannerView']();
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  describe('#updateTutorialsSteps', () => {
    it('should update corresponding step', () => {
      component.tutorialSteps = { step1: false, step2: false, step3: false, step4: false, step5: false };
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

  describe('#liveTutorialGATrack', () => {
    it('should call gtmService.push', () => {
      component['liveTutorialGATrack']('live-leaderboard');
      expect(gtmService.push).toHaveBeenCalled();
    });
  });

  describe('#calculateLeaderboardEntriesHeight', () => {
    it('should return height of elements when 3 elements are passed', () => {
      const returnData =
        [{ getBoundingClientRect: boundFunc }, { getBoundingClientRect: boundFunc }, { getBoundingClientRect: boundFunc }];
      windowRef.document.querySelectorAll = jasmine.createSpy().and.returnValue(returnData);
      component['calculateLeaderboardEntriesHeight']();
      expect(component['calculateLeaderboardEntriesHeight']()).not.toEqual(0);
    });
    it('should return height of elements when 1 element is passed', () => {
      const returnData = [{ getBoundingClientRect: boundFunc }];
      windowRef.document.querySelectorAll = jasmine.createSpy().and.returnValue(returnData);
      component['calculateLeaderboardEntriesHeight']();
      expect(component['calculateLeaderboardEntriesHeight']()).not.toEqual(0);
    });
    it('should return height of elements when 4 elements are passed', () => {
      const returnData =
        [{ getBoundingClientRect: boundFunc }, { getBoundingClientRect: boundFunc }, { getBoundingClientRect: boundFunc }];
      windowRef.document.querySelectorAll = jasmine.createSpy().and.returnValue(returnData);
      component['calculateLeaderboardEntriesHeight']();
      expect(component['calculateLeaderboardEntriesHeight']()).not.toEqual(0);
    });
    it('should take parameter value if not passed', () => {
      const returnData =
        [{ getBoundingClientRect: boundFunc }, { getBoundingClientRect: boundFunc }, { getBoundingClientRect: boundFunc }];
      windowRef.document.querySelectorAll = jasmine.createSpy().and.returnValue(returnData);
      component['calculateLeaderboardEntriesHeight'](2);
      expect(component['calculateLeaderboardEntriesHeight']()).not.toEqual(0);
    });
    it('should return height of elements when no elemnts passed', () => {
      windowRef.document.querySelectorAll = jasmine.createSpy().and.returnValue([]);
      component['calculateLeaderboardEntriesHeight']();
      expect(component['calculateLeaderboardEntriesHeight']()).toEqual(0);
    });
  });

  describe('#scrollToTopForDesktop', () => {
    it('should call element scrollTo', () => {
      const element = { scrollTo: jasmine.createSpy('scrollTo') };
      windowRef.document.querySelector = jasmine.createSpy().and.returnValue(element);
      component['deviceService'].isDesktop = true;
      component['scrollToTopForDesktop']();
      expect(element.scrollTo).toHaveBeenCalled();
    });
    it('should not call element scrollTo when element is null', () => {
      const element = null;
      windowRef.document.querySelector = jasmine.createSpy().and.returnValue(element);
      component['deviceService'].isDesktop = true;
      component['scrollToTopForDesktop']();
      expect(element).toBeNull();
    });
    it('should not call element scrollTo when device is not desktop', () => {
      const element = { scrollTo: jasmine.createSpy('scrollTo') };
      windowRef.document.querySelector = jasmine.createSpy().and.returnValue(element);
      component['deviceService'].isDesktop = false;
      component['scrollToTopForDesktop']();
      expect(element.scrollTo).not.toHaveBeenCalled();
    });
  });
});
