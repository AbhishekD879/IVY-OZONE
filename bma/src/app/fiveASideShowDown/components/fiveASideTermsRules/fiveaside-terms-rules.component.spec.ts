import { of, throwError } from 'rxjs';
import { USER_SHOWDOWN_DATA, USER_SHOWDOWN_DATA_NO_DISPLAY } from '@app/fiveASideShowDown/components/fiveASideRulesEntryArea/fiveaside-rules-entry-area.mock';
import { FiveasideTermsRulesComponent } from '@app/fiveASideShowDown/components/fiveASideTermsRules/fiveaside-terms-rules.component';
import { FAQS_MOCK, T_AND_C } from '@app/fiveASideShowDown/components/fiveASideTermsRules/fiveaside-terms-rules.mock';

describe('FiveasideTermsRulesComponent', () => {
  let component: FiveasideTermsRulesComponent;
  let rendererService,
  domSanitizer,
  cmsService,
  windowRefService,
  gtmservice,
  deviceService,
  rulesEntryService;

  beforeEach(() => {
    rendererService = {
      renderer: {
        addClass: jasmine.createSpy('addClass'),
        removeClass: jasmine.createSpy('removeClass')
      }
    };
    rulesEntryService = {
      formFlagName: jasmine.createSpy('formFlagName').and.returnValue('#flag_round_england')
    };
    domSanitizer = {
      sanitize: jasmine.createSpy().and.returnValue('test'),
      bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml')
    };
    cmsService = {
      getFAQs: jasmine.createSpy('getFAQs').and.returnValue(of(FAQS_MOCK)),
      getTermsAndConditions: jasmine.createSpy('getTermsAndConditions').and.returnValue(of([T_AND_C]))
    };
    windowRefService = {
      document: {
        querySelector: jasmine.createSpy('querySelector').and.returnValue({
          parentNode: {}
        } as any),
        getElementById: jasmine.createSpy('querySelector').and.returnValue({
          parentNode: {}
        } as any)
      }
    };
    gtmservice = {
      push: jasmine.createSpy('push')
    };
    deviceService = {
      isWrapper: true
    } as any;
    component = new FiveasideTermsRulesComponent(cmsService, rendererService, windowRefService,
      deviceService, domSanitizer, gtmservice, rulesEntryService);
    component.clearOverlay.emit = jasmine.createSpy('modelChangeHandler.emit');
    component.showDown = USER_SHOWDOWN_DATA;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should fetch cms data in ngOnInit', () => {
    spyOn(component as any, 'getCMSData');
    spyOn(component as any, 'initOverlayElements');
    spyOn(component as any, 'validateBaseElement');
    component.leaderboardData = USER_SHOWDOWN_DATA_NO_DISPLAY;
    component.prizePoolData = USER_SHOWDOWN_DATA_NO_DISPLAY.prizeMap;
    component.ngOnInit();
    expect(component.homeTeam).toEqual('England');
  });

  it('should switch active tab based on input', () => {
    component.faqs = [{isExpanded: false, question: 'question'}] as any;
    const event = {
      id: 'prizes',
      tab: {
        id: 'prizes',
        label: 'PRIZES',
        title: 'PRIZES',
        isFiveASideNewIconAvailable: false,
        url: ''
      }
    };
    component.switchTab(event);
    expect(component.activeTab).toEqual({
      id: 'prizes',
      label: 'PRIZES',
      title: 'PRIZES',
      isFiveASideNewIconAvailable: false,
      url: ''
    });
  });

  it('should track faq question on open', () => {
    component.faqs = [{isExpanded: false, question: 'question'}] as any;
    component.faqHandler(0);
    expect(gtmservice.push).toHaveBeenCalled();
  });
  it('should not track faq question on close', () => {
    component.faqs = [{isExpanded: true, question: 'question'}] as any;
    component.faqHandler(0);
    expect(gtmservice.push).not.toHaveBeenCalled();
  });

  describe('#onCloseRulesOverlay', () => {
    it('should close rules overlay', () => {
      component.onCloseRulesOverlay();
      expect(rendererService.renderer.removeClass).toHaveBeenCalledWith(undefined, 'active');
    });
  });

  describe('#getCMSData', () => {
    it('should map cms data, if you get response', () => {
      component['getCMSData']();
      expect(component.faqs).not.toBeNull();
    });
    it('should not map cms data, if you get no response', () => {
      cmsService.getFAQs.and.returnValue(throwError({error: '401'}));
      cmsService.getTermsAndConditions.and.returnValue(of(null));
      component['getCMSData']();
      expect(component.faqs).toEqual([]);
    });
  });

  describe('#initOverlayElements', () => {
    it('should init rules overlay', () => {
      component['initOverlayElements']();
      expect(rendererService.renderer.addClass).toHaveBeenCalledWith(undefined, 'active');
    });
  });

  describe('#setTermsConditions', () => {
    it('should not set staticblock, if all conditions fail', () => {
      component.termsConditions = null;
      component['setTermsConditions']();
      expect(component.staticBlockTerms).toBeUndefined();
    });
    it('should not set staticblock, if only one condition pass', () => {
      component.termsConditions = {} as any;
      component['setTermsConditions']();
      expect(component.staticBlockTerms).toBeUndefined();
    });
    it('should set staticblock, if two conditions pass', () => {
      component.termsConditions = { text: 'welcome'} as any;
      component['setTermsConditions']();
      expect(component.staticBlockTerms).not.toBeUndefined();
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
});
