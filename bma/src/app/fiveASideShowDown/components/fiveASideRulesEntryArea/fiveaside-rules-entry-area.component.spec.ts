import { of } from 'rxjs';
import { FiveASideRulesEntryAreaComponent
} from '@app/fiveASideShowDown/components/fiveASideRulesEntryArea/fiveaside-rules-entry-area.component';
import { RULES_MOCK, USER_SHOWDOWN_DATA
} from '@app/fiveASideShowDown/components/fiveASideRulesEntryArea/fiveaside-rules-entry-area.mock';
import { CONTEST_STATUSES } from '@app/fiveASideShowDown/components/fiveASideRulesEntryArea/fiveaside-rules-entry-area.constant';
import { BUTTON_TYPE } from '@app/fiveASideShowDown/constants/enums';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
describe('FiveASideRulesEntryAreaComponent', () => {
  let component: FiveASideRulesEntryAreaComponent;
  let localeService,
  rendererService,
  domSanitizer,
  cmsService,
  windowRefService,
  rulesEntryService,
  decimalPipe,
  router,
  fiveASideContestSelectionService,
  pubSubService,
  userService,
  leaderBoardService;
  beforeEach(() => {
    localeService = {
      applySubstitutions: jasmine.createSpy('applySubstitutions').and.returnValue('welcome')
    };
    rendererService = {
      renderer: {
        removeAttribute: jasmine.createSpy('removeAttribute'),
        setStyle: jasmine.createSpy('setStyle'),
        setProperty: jasmine.createSpy('setProperty'),
        addClass: jasmine.createSpy('addClass'),
        insertBefore: jasmine.createSpy('insertBefore'),
        createElement: jasmine.createSpy('createElement')
      }
    };
    domSanitizer = {
      sanitize: jasmine.createSpy().and.returnValue('test'),
      bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml')
    };
    cmsService = {
      getStaticBlock: jasmine.createSpy('getStaticBlock').and.returnValue(of(RULES_MOCK))
    };
    windowRefService = {
      nativeWindow: {
        setTimeout: jasmine.createSpy().and.callFake((callback: Function) => {
          callback();
        })
      },
      document: {
        querySelector: jasmine.createSpy('querySelector').and.returnValue({
          parentNode: {}
        } as any),
      }
    };
    fiveASideContestSelectionService = {
      defaultSelection: jasmine.createSpy('defaultSelection')
    };
    router = {
      navigate: jasmine.createSpy('navigate')
    } as any;
    rulesEntryService = {
      formFiveASideUrl: jasmine.createSpy('formFiveASideUrl').and.returnValue('url'),
      trackGTMEvent: jasmine.createSpy('trackGTMEvent'),
      getButtonStatus: jasmine.createSpy('getButtonStatus').and.returnValue({buttonType: 'BUILD TEAM',
      isBuildBetEnabled: true})
    };
    decimalPipe = {
      transform: jasmine.createSpy('transform').and.callFake((value) => {
        if (value === 1000) { return '1,000';} else { return value; }
      })
    };
    pubSubService = {
      publish: jasmine.createSpy(),
      subscribe: jasmine.createSpy(),
      API: pubSubApi
    } as any;
    userService = {
      status: true
    } as any;
    leaderBoardService = { optInUserIntoTheContest: jasmine.createSpy() } as any;
    component = new FiveASideRulesEntryAreaComponent(localeService, rendererService, domSanitizer,
      cmsService, windowRefService, router, rulesEntryService, decimalPipe, fiveASideContestSelectionService, pubSubService, userService, leaderBoardService);
    component.showRulesOverlay.emit = jasmine.createSpy('modelChangeHandler.emit');
    component.contest = USER_SHOWDOWN_DATA as any;
    component.contestSize = USER_SHOWDOWN_DATA.currentContestEntries;
    component.userContestSize = USER_SHOWDOWN_DATA.betsPlaced;
    component.eventEntity = USER_SHOWDOWN_DATA.eventDetails;
    component.contestStatus = CONTEST_STATUSES.pre;
  });
  it('should create', () => {
    expect(component).toBeTruthy();
  });
  it('should fetch initial data in ngOnInit', () => {
    spyOn(component as any, 'fetchInitialData');
    component.ngOnInit();
    expect(component['fetchInitialData']).toHaveBeenCalled();
  });
  describe('#ngAfterViewInit', () => {
    beforeEach(() => {
      spyOn(component as any, 'setRulesInformation');
      component.rulesArea = {
        changes: {
         subscribe: jasmine.createSpy('subscribe').and.callFake((next) => {
           next({id: 1} as any);
         })
        }
      } as any;
    });
    it('should set rules information, if change exists', () => {
      component.ngAfterViewInit();
      expect(component['setRulesInformation']).toHaveBeenCalled();
    });
    it('should not set rules information, if change does not exists', () => {
      component.rulesArea = {
        changes: {
          subscribe: jasmine.createSpy('subscribe').and.callFake((next) => {
            next(null);
          })
         }
      } as any;
      component.ngAfterViewInit();
      expect(component['setRulesInformation']).not.toHaveBeenCalled();
    });
  });
  describe('#handleActionClick', () => {
    const event = {
      preventDefault: jasmine.createSpy('preventDefault'),
      target: {
        className: 'build-btn'
      }
    } as any;
    it('should not handle, if target is not available', () => {
      const eventMock = {preventDefault: jasmine.createSpy('preventDefault')} as any;
      component.handleActionClick(eventMock);
      expect(router.navigate).not.toHaveBeenCalledWith([`/url/5-a-side/pitch`]);
    });
    it('should not handle, if className is not available', () => {
      const eventMock = { preventDefault: jasmine.createSpy('preventDefault'),target: {}} as any;
      component.handleActionClick(eventMock);
      expect(router.navigate).not.toHaveBeenCalledWith([`/url/5-a-side/pitch`]);
    });
    it('should handle build btn scenario. Case: Enabled', () => {
      component['isBuildBetEnabled'] = true;
      userService.username = 'Nick';
      component.handleActionClick(event);
      expect(router.navigate).toHaveBeenCalledWith([`/url/5-a-side/pitch`]);
    });
    it('should handle build btn scenario. Case: Disabled', () => {
      component.handleActionClick(event);
      expect(router.navigate).not.toHaveBeenCalledWith([`/url/5-a-side/pitch`]);
    });
    it('should handle rules-btn scenario', () => {
      event.target.className = BUTTON_TYPE.RULES;
      component.handleActionClick(event);
      expect(component.showRulesOverlay.emit).toHaveBeenCalled();
    });
    it('should handle back-btn scenario', () => {
      event.target.className = BUTTON_TYPE.BACK;
      component.handleActionClick(event);
      expect(router.navigate).toHaveBeenCalledWith([`/5-a-side/lobby`]);
    });
    it('should handle return-to-lobby scenario', () => {
      event.target.className = BUTTON_TYPE.RETURN_TO_LOBBY;
      component.handleActionClick(event);
      expect(router.navigate).toHaveBeenCalledWith([`/5-a-side/lobby`]);
    });
    it('should handle unknow class scenario', () => {
      event.target.className = BUTTON_TYPE.UNKNOWN;
      component.handleActionClick(event);
      expect(router.navigate).not.toHaveBeenCalledWith([`/5-a-side/lobby`]);
    });
    it('should handle build btn scenario. Logout scenario', () => {
      event.target.className = BUTTON_TYPE.BUILD;
      component['isBuildBetEnabled'] = true;
      userService = null;
      component.handleActionClick(event);
      expect(router.navigate).not.toHaveBeenCalledWith([`/url/5-a-side/pitch`]);
    });
    it('should handle build btn scenario. to Open Login popup', () => {
      component['isBuildBetEnabled'] = true;
      userService = null;
      component.handleActionClick(event);
      expect(pubSubService.publish).toHaveBeenCalled();
    });
    it('should handle build btn scenario. when username is null', () => {
      component['isBuildBetEnabled'] = true;
      userService = { username: null };
      component.handleActionClick(event);
      expect(pubSubService.publish).toHaveBeenCalled();
    });
  });
  describe('#fetchInitialData', () => {
    it('should fetch static block content', () => {
      component['fetchInitialData']();
      expect(component.staticBlockContent).not.toBeNull();
    });
  });
  describe('#setRulesInformation', () => {
    beforeEach(() => {
      spyOn(component as any, 'appendBlurbInformation');
      spyOn(component as any, 'validateBuildButton');
      spyOn(component as any, 'removeElementsBasedOnContestStatus');
      spyOn(component as any, 'setDOMProperty');
      spyOn(component as any, 'validateContestProperties');
      spyOn(component as any, 'addRulesStyles');
    });
    it('should not display third rule element, if size and teams is not available', () => {
      component.hasMaxWidth = true;
      component.contest = {} as any;
      component['setRulesInformation']();
      expect(component['setDOMProperty']).toHaveBeenCalled();
    });
    it('should validateContestProperties, if teams is available', () => {
      component.contest = { maxEntriesPerUser: 2} as any;
      component['setRulesInformation']();
      expect(component['validateContestProperties']).toHaveBeenCalled();
    });
    it('should validateContestProperties, if size is available', () => {
      component.contest = { maxEntries: 2} as any;
      component['setRulesInformation']();
      expect(component['validateContestProperties']).toHaveBeenCalled();
    });
  });
  it('should remove DOM elements', () => {
    component.removeElements = ['.rules-btn'];
    component.contestStatus = CONTEST_STATUSES.post;
    component['removeElementsBasedOnContestStatus']();
    expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({
      parentNode: {}
    }, 'display', 'none');
  });
  it('should remove DOM elements with status as pre', () => {
    component.removeElements = ['.rules-btn'];
    component.contestStatus = CONTEST_STATUSES.pre;
    component['removeElementsBasedOnContestStatus']();
    expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({
      parentNode: {}
    }, 'display', 'none');
  });
  describe('#appendBlurbInformation', () => {
    it('should not append blurb, if contest has no blurb', () => {
      windowRefService.document.querySelector.and.returnValue(null);
      component.contest = {} as any;
      component['appendBlurbInformation']();
      expect(rendererService.renderer.createElement).not.toHaveBeenCalled();
    });
    it('should not append blurb, if only contest has blurb', () => {
      windowRefService.document.querySelector.and.returnValue(null);
      component.contest = { blurb: '<p>welcome</p>'} as any;
      component['appendBlurbInformation']();
      expect(rendererService.renderer.createElement).not.toHaveBeenCalled();
    });
    it('should not append blurb, if has change is true', () => {
      component.contest = { blurb: '<p>welcome</p>'} as any;
      component['appendBlurbInformation'](true);
      expect(rendererService.renderer.createElement).not.toHaveBeenCalled();
    });
    it('should append blurb, if both contest has blurb and element is available', () => {
      component.contest = { blurb: '<p>welcome</p>'} as any;
      component['appendBlurbInformation']();
      expect(rendererService.renderer.createElement).toHaveBeenCalledWith('div');
    });
  });
  describe('#validateBuildButton', () => {
    it('should validate button based on buttonstatus(enabled)', () => {
      windowRefService.document.querySelector.and.returnValue(null);
      component['validateBuildButton']();
      expect(component['isBuildBetEnabled']).toBe(true);
    });
    it('should validate button based on buttonstatus(disabled)', () => {
      rulesEntryService.getButtonStatus.and.returnValue({buttonType: 'CONTEST FULL',
      isBuildBetEnabled: false});
      component['validateBuildButton']();
      expect(component['isBuildBetEnabled']).toBe(false);
    });
  });
  describe('#validateContestProperties', () => {
    it('should not set DOM property, if contest does not has size or teams property', () => {
      component.contest = {} as any;
      component['validateContestProperties']('maxEntriesPerUser', '.user-entries-normal', '.user-entries-bold',
      '.entries-per-user', { maxUserEntries: 5, betsPlaced: 2 });
      expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({
        parentNode: {}
      }, 'display', 'none');
    });
    it('should set DOM property, if contest has size or teams property', () => {
      spyOn(component as any, 'setDOMProperty');
      component.contest = { maxEntriesPerUser: 5 } as any;
      component['validateContestProperties']('maxEntriesPerUser', '.user-entries-normal', '.user-entries-bold',
      '.entries-per-user', { maxUserEntries: 5, betsPlaced: 2 });
      expect(component['setDOMProperty']).toHaveBeenCalled();
    });
  });
  describe('#setDOMProperty', () => {
    it('should set dom property if element exists (case: textContent)', () => {
      spyOn(component as any, 'transformToDecimal').and.returnValue({ maxUserEntries: 5, betsPlaced: 2 });
      component['setDOMProperty']('.user-entries-normal', 'setProperty', { maxUserEntries: 5, betsPlaced: 2 },
      'textContent', 'welcome');
      expect(rendererService.renderer.setProperty).toHaveBeenCalledWith({
        parentNode: {}
      }, 'textContent', 'welcome');
    });
    it('should set dom property if element exists (case: textContent)', () => {
      spyOn(component as any, 'transformToDecimal').and.returnValue({ maxUserEntries: 5, betsPlaced: 2 });
      component['setDOMProperty']('.user-entries-normal', 'setProperty', { maxUserEntries: 5, betsPlaced: 2 },
      'textContent', 'welcome', '{betsPlaced}/{maxUserEntries}');
      expect(rendererService.renderer.setProperty).toHaveBeenCalledWith({
        parentNode: {}
      }, 'textContent', 'welcome');
    });
    it('should set dom property if element exists (case: class)', () => {
      spyOn(component as any, 'transformToDecimal').and.returnValue({ maxUserEntries: 5, betsPlaced: 2 });
      component['setDOMProperty']('.user-entries-normal', 'addClass', { maxUserEntries: 5, betsPlaced: 2 },
      'class', 'welcome');
      expect(rendererService.renderer.addClass).toHaveBeenCalledWith({
        parentNode: {}
      }, 'welcome');
    });
    it('should set dom property if element exists (case: style)', () => {
      spyOn(component as any, 'transformToDecimal').and.returnValue({ maxUserEntries: 5, betsPlaced: 2 });
      component['setDOMProperty']('.user-entries-normal', 'setStyle', { maxUserEntries: 5, betsPlaced: 2 },
      'display', 'none');
      expect(rendererService.renderer.setStyle).toHaveBeenCalledWith({
        parentNode: {}
      }, 'display', 'none');
    });
    it('should not set dom property if element does not exists', () => {
      spyOn(component as any, 'transformToDecimal').and.returnValue({ maxUserEntries: 5, betsPlaced: 2 });
      windowRefService.document.querySelector.and.returnValue(null);
      component['setDOMProperty']('.user-entries-normal','setProperty', { maxUserEntries: 5, betsPlaced: 2 },
      'textContent', 'welcome');
      expect(rendererService.renderer.setProperty).not.toHaveBeenCalledWith({
        parentNode: {}
      }, 'textContent', 'welcome');
    });
  });

  describe('#transformToDecimal', () => {
    it('should transform when input given', () => {
      const response = component['transformToDecimal']({ maxUserEntries: 1000, betsPlaced: 2 });
      expect(response).toEqual({ maxUserEntries: '1,000', betsPlaced: 2 });
    });
    it('should transform when input given(case entry stake)', () => {
      const response = component['transformToDecimal']({ minAmount: 0.10 });
      expect(response).toEqual({ minAmount: 0.10 });
    });
  });

  describe('#addRulesStyles', () => {
    it('should add styles if rulesdiv exists', () => {
      spyOn(component as any, 'setDOMProperty');
      component['addRulesStyles']();
      expect(component['setDOMProperty']).toHaveBeenCalled();
    });
    it('should not add styles if rulesdiv exists', () => {
      windowRefService.document.querySelector.and.returnValue(null);
      spyOn(component as any, 'setDOMProperty');
      component['addRulesStyles']();
      expect(component['setDOMProperty']).toHaveBeenCalled();
    });
  });
  describe('#ngOnChanges', () => {
    it('should set rules information, if both conditions satsfies', () => {
      spyOn(component as any, 'setRulesInformation');
      const changes = {
        userContestSize: {
          isFirstChange: () => false
        }
      } as any;
      component.ngOnChanges(changes);
      expect(component['setRulesInformation']).toHaveBeenCalled();
    });
    it('should not set rules information, if 1st condition does not satisfy', () => {
      spyOn(component as any, 'setRulesInformation');
      const changes = {} as any;
      component.ngOnChanges(changes);
      expect(component['setRulesInformation']).not.toHaveBeenCalled();
    });
    it('should not set rules information, if 2nd condition does not satsfy', () => {
      spyOn(component as any, 'setRulesInformation');
      const changes = {
        userContestSize: {
          isFirstChange: () => true
        }
      } as any;
      component.ngOnChanges(changes);
      expect(component['setRulesInformation']).not.toHaveBeenCalled();
    });
  });

  describe('#validateButtonOnLogin', () => {
    it('should call validateBuildButton and optInUserIntoTheContest on login success callback', () => {
      spyOn(component as any, 'validateBuildButton');
      component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === pubSubService.API.SUCCESSFUL_LOGIN) {
          fn();
        }
      });
      component.contest = { id: '1' } as any;
      component['validateButtonOnLogin']();
      expect(leaderBoardService.optInUserIntoTheContest).toHaveBeenCalled();
    });
    it('should call validateBuildButton and not optInUserIntoTheContest on login success callback', () => {
      spyOn(component as any, 'validateBuildButton');
      component['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
        if (ch === pubSubService.API.SUCCESSFUL_LOGIN) {
          fn();
        }
      });
      component.contest = null;
      component['validateButtonOnLogin']();
      expect(component['validateBuildButton']).toHaveBeenCalled();
      expect(leaderBoardService.optInUserIntoTheContest).not.toHaveBeenCalled();
    });
  });
});
