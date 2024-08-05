import { Component, Input, OnDestroy, OnInit, Output, EventEmitter } from '@angular/core';
import { DeviceService } from '@app/core/services/device/device.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { RendererService } from '@app/shared/services/renderer/renderer.service';
import { PROPERTY_TYPE } from '@app/fiveASideShowDown/constants/enums';
import { PRE_DOM_ELEMENT, PRE_OVERLAY } from '@app/fiveASideShowDown/constants/fiveaside-pre-overlay.constants';
import { IWelcomeOverlay } from '@app/fiveASideShowDown/models/welcome-overlay';
import { FiveasideRulesEntryAreaService } from '@app/fiveASideShowDown/services/fiveaside-rules-entry-area.service';
import { FiveASidePreHeaderService } from '@app/fiveASideShowDown/services/fiveaside-pre-header.service';
import { GTM_EVENTS } from '@app/fiveASideShowDown/constants/constants';

@Component({
  selector: 'fiveaside-pre-event-tutorial',
  template: ``
})
export class FiveasidePreEventTutorialComponent implements OnInit, OnDestroy {

  @Input() baseClass: string;
  @Input() welcomeCard: IWelcomeOverlay;
  @Input() preEventData: IWelcomeOverlay;
  @Output() readonly clearOverlay = new EventEmitter();
  isPrizePoolTutorial: boolean = false;
  protected baseOverlayElement: HTMLElement;
  protected overlay: HTMLElement;
  protected readonly PRE_DOM = PRE_DOM_ELEMENT;

  topValue = 0;

  constructor(protected rendererService: RendererService,
    protected windowRef: WindowRefService,
    protected deviceService: DeviceService,
    protected entryService: FiveasideRulesEntryAreaService,
    protected preService: FiveASidePreHeaderService) { }

  ngOnInit(): void {
    this.setTopValue();
    this.overlay = this.windowRef.document.getElementById(this.PRE_DOM.INTRODUCTION_OVERLAY_ID);
    this.scrollTo();
    this.scrollToTop();
    this.validateBaseElement();
    this.initOverlayElements();
    this.windowRef.nativeWindow.localStorage.setItem('preEventOverlay', true);
    this.handleMultipleElements([PRE_OVERLAY.TOP_BAR], PRE_OVERLAY.SET_STYLE,
    ['0'], [PRE_OVERLAY.Z_INDEX]);
    this.enableDisableIOSBodyScroll('add');
  }

  ngOnDestroy(): void {
    this.onCloseWelcomeOverlay('unsubscribe');
    this.enableDisableIOSBodyScroll('remove');
  }

  /**
   * Scroll to top when we get scrollBar on page
   * @returns void
   */
  scrollTo(): void {
    if (!this.checkForModule()) {
      const leaderboard = this.windowRef.document.getElementsByClassName('leaderboard-container');
      leaderboard[0].scrollTo(0, 0);
    }
  }

  /**
   * Set Top Value based on screen resolution
   * @returns void
   */
   setTopValue(): void {
    if (this.windowRef.nativeWindow.innerWidth >= 1300 && this.windowRef.nativeWindow.innerWidth <= 1599) {
      this.topValue = 34;
    } else if (this.windowRef.nativeWindow.innerWidth >= 1600) {
      this.topValue = 64;
    }
  }

  /**
   * Disable background body scrolling for iOS devices when overlay is on
   * @param  {string} action
   * @returns void
   */
   enableDisableIOSBodyScroll(action: string): void {
    const preOverlay = this.windowRef.document.getElementsByClassName('pre-parent-div');
    if (this.deviceService.isIos && preOverlay) {
      this.preventScrollForTouchMove = this.preventScrollForTouchMove.bind(this);
      this.preventScrollForTouchStart = this.preventScrollForTouchStart.bind(this);
      if (action === 'add') {
        preOverlay[0].addEventListener('touchmove', this.preventScrollForTouchMove, { passive: false });
        preOverlay[0].addEventListener('touchstart', this.preventScrollForTouchStart, { passive: false });
      } else {
        preOverlay[0].removeEventListener('touchmove', this.preventScrollForTouchMove);
        preOverlay[0].removeEventListener('touchstart', this.preventScrollForTouchStart);
      }
    }
  }

  /**
   * Prevent default action for touchmove event
   * @param  {TouchEvent} event
   * @returns void
   */
   preventScrollForTouchMove(event: TouchEvent): void {
    event.preventDefault();
  }

  /**
   * Prevent default action for touchstart event
   * @param  {TouchEvent} event
   * @returns void
   */
  preventScrollForTouchStart(event: TouchEvent): void | boolean {
    const allowedIds = ['close-div', 'close-i', 'close-svg', 'getStarted',
      'go-to-rules', 'go-to-entry', 'go-to-rules-button', 'go-to-end', 'go-to-finish', 'go-to-second-half'];
    const selectedId = (event.target as HTMLInputElement).id;
    if (allowedIds.includes(selectedId)) {
      return false;
    }
    event.preventDefault();
  }

  /**
   * Triggered when overlay x svg icon is clicked
   * @returns {void}
   */
  onCloseWelcomeOverlay(action?: string): void {
    if (!action) {
      this.entryService.trackGTMEvent('5-A-Side Showdown', 'pre tutorial', 'close');
    }
    this.enableDisableIOSBodyScroll('remove');
    this.rendererService.renderer.removeClass(this.baseOverlayElement, this.PRE_DOM.CONTEST_OVERLAY_CLASS_NAME);
    this.rendererService.renderer.removeClass(this.overlay, 'active');
    this.handleMultipleElements([PRE_OVERLAY.INTRODUCTION_OVERLAY_ID, PRE_OVERLAY.PRIZEPOOL_OVERLAY_ID, PRE_OVERLAY.RULESAREA_OVERLAY_ID,
    PRE_OVERLAY.ENTRYAREA_OVERLAY_ID, PRE_OVERLAY.ANOTHERTEAM_OVERLAY_ID, PRE_OVERLAY.RULESBUTTON_OVERLAY_ID, '.pre-parent-div'],
      PRE_OVERLAY.REMOVE_CLASS, [PRE_OVERLAY.ACTIVE, PRE_OVERLAY.ACTIVE, PRE_OVERLAY.ACTIVE,
      PRE_OVERLAY.ACTIVE, PRE_OVERLAY.ACTIVE, PRE_OVERLAY.ACTIVE, PRE_OVERLAY.ACTIVE],
      [PRE_OVERLAY.CLASS, PRE_OVERLAY.CLASS, PRE_OVERLAY.CLASS, PRE_OVERLAY.CLASS, PRE_OVERLAY.CLASS, PRE_OVERLAY.CLASS,
      PRE_OVERLAY.CLASS]);
    this.clearOverlay.emit();
  }

  /**
   * goToPrizepool is used to show the Prizepool overlay
   * Providing values in element in order to achieve animation perfectly.
   * @returns {void}
   */
  goToPrizepool(): void {
    this.scrollTo();
    this.scrollToTop();
    if (this.checkForElement(['.prize-pool-header']) || this.checkForElement(['.prize-pool-record'])) {
      this.getPrizePoolInformation();
    } else {
      this.handleMultipleElements([PRE_OVERLAY.INTRODUCTION_OVERLAY_ID], PRE_OVERLAY.REMOVE_CLASS,
        [PRE_OVERLAY.ACTIVE], [PRE_OVERLAY.CLASS]);
      this.goToRulesArea();
    }
    this.entryService.trackGTMEvent('5-A-Side Showdown', 'pre tutorial', GTM_EVENTS.NEXT_STEP_1_LABEL);
  }

  /**
   * goToRulesArea is used to show the Rules Area overlay
   * @returns {void}
   */
  goToRulesArea(): void {
    if (this.checkForElement([PRE_OVERLAY.RULES_ENTRY_AREA_CLASS])) {
      this.getRulesAreaInformation();
    } else {
      this.handleMultipleElements([PRE_OVERLAY.PRIZEPOOL_OVERLAY_ID], PRE_OVERLAY.REMOVE_CLASS, [PRE_OVERLAY.ACTIVE], [PRE_OVERLAY.CLASS]);
      this.goToEntryButton();
    }
    this.entryService.trackGTMEvent('5-A-Side Showdown', 'pre tutorial', GTM_EVENTS.NEXT_STEP_2_LABEL);
  }


  /**
 * goToEntryButton is used to show the Entry Button Area overlay
 * @returns {void}
 */
  goToBuildAnotherTeamButton(): void {
    this.scrollTo();
    this.scrollToTop();
    if (this.checkForElement([PRE_OVERLAY.MY_ENTRIES_CLASS])) {
      this.initEntriesArea();
      if (this.checkForModule()) {
        const buildButton: DOMRect = this.getElementRect(PRE_OVERLAY.BUILD_BUTTON_CLASS);
        this.windowRef.nativeWindow.scrollTo(0, buildButton.top - 180);
      } else {
        const rulesDect: DOMRect = this.getElementRect(PRE_OVERLAY.RULES_BTN);
        this.windowRef.nativeWindow.scrollTo(0, rulesDect.y - 100);
      }
      const rulesArea: DOMRect = this.getElementRect(PRE_OVERLAY.RULES_ENTRY_AREA_CLASS);
      this.setAnotherBuildArea(rulesArea);
    } else {
      this.getBuildBtnInformation();
    }
    this.entryService.trackGTMEvent('5-A-Side Showdown', 'pre tutorial', GTM_EVENTS.NEXT_STEP_3_FINAL_LABEL);
  }

  /**
   * goToEntryButton is used to show the Entry Button Area overlay
   * @returns {void}
   */
  goToEntryButton(): void {
    this.scrollTo();
    this.scrollToTop();
    if (this.checkForElement([PRE_OVERLAY.MY_ENTRIES_CLASS])) {
      this.initSeparateEntriesArea();
      if (this.checkForModule()) {
        const buildButton: DOMRect = this.getElementRect(PRE_OVERLAY.BUILD_BUTTON_CLASS);
        this.windowRef.nativeWindow.scrollTo(0, buildButton.top - 180);
      } else {
        const rulesDect: DOMRect = this.getElementRect(PRE_OVERLAY.RULES_BTN);
        this.windowRef.nativeWindow.scrollTo(0, rulesDect.y - 100);
      }
      this.setAnotherBuildAreaForEntries();
    } else {
      this.getBuildBtnInformation();
    }
    this.entryService.trackGTMEvent('5-A-Side Showdown', 'pre tutorial', GTM_EVENTS.NEXT_STEP_3_LABEL);
  }

  /**
   * getRulesButton is used to show the Rules Button Area overlay
   * @returns {void}
   */
  getRulesButton(): void {
    if (this.checkForElement([PRE_OVERLAY.RULES_BTN])) {
      this.scrollTo();
      this.scrollToTop();
      this.initRulesButton();
      const rulesRect: DOMRect = this.getElementRect(PRE_OVERLAY.RULES_BTN);
      this.setRulesButtonArea(rulesRect);
      this.entryService.trackGTMEvent('5-A-Side Showdown', 'pre tutorial', GTM_EVENTS.NEXT_STEP_4_LABEL);
    } else {
      this.onCloseWelcomeOverlay();
    }
  }

  /**
   * getEnded is used to complete the overlay flow for pre event.
   * @returns {void}
   */
  getEnded(): void {
    this.rendererService.renderer.removeClass(this.baseOverlayElement, this.PRE_DOM.CONTEST_OVERLAY_CLASS_NAME);
    this.rendererService.renderer.removeClass(this.overlay, 'active');
    this.handleMultipleElements([PRE_OVERLAY.ENTRYAREA_OVERLAY_ID, PRE_OVERLAY.ANOTHERTEAM_OVERLAY_ID, PRE_OVERLAY.RULESBUTTON_OVERLAY_ID],
      PRE_OVERLAY.REMOVE_CLASS, [PRE_OVERLAY.ACTIVE, PRE_OVERLAY.ACTIVE, PRE_OVERLAY.ACTIVE],
      [PRE_OVERLAY.CLASS, PRE_OVERLAY.CLASS, PRE_OVERLAY.CLASS]);
    this.scrollTo();
    this.scrollToTop();
    this.entryService.trackGTMEvent('5-A-Side Showdown', 'pre tutorial', 'finish');
    this.clearOverlay.emit();
    this.enableDisableIOSBodyScroll('remove');
  }

  /**
   * scrollToTop is used to scroll to the top of page.
   * @returns {void}
   */
  private scrollToTop(): void {
    this.windowRef.nativeWindow.scrollTo(0, 0);
  }

  /**
   * To Validate base element based on input
   * @returns {void}
   */
  private validateBaseElement(): void {
    if (this.baseClass) {
      this.baseOverlayElement = this.windowRef.document.querySelector(this.baseClass);
    } else {
      this.baseOverlayElement = this.deviceService.isWrapper ?
        this.windowRef.document.querySelector('body') : this.windowRef.document.querySelector('html, body');
    }
  }

  /**
   * initOverlayElements to load the initial overlay
   * @returns {void}
   */
  private initOverlayElements(): void {
    this.rendererService.renderer.addClass(this.overlay, 'active');
    this.rendererService.renderer.addClass(this.baseOverlayElement, this.PRE_DOM.CONTEST_OVERLAY_CLASS_NAME);
  }

  /**
   * handleMultipleElements is used handle multiple HTML element.
   * @param {string[]}
   * @param {string}
   * @param {string[]}
   * @param {string[]}
   * @returns {void}
   */
  private handleMultipleElements(elements: string[], rendererProperty: string, values: string[], property: string[]): void {
    elements.forEach((element, index) => this.setDOMProperty(element, rendererProperty, property[index], values[index]));
  }

  /**
   * setDOMProperty is used render HTML element.
   * @param {string}
   * @param {string}
   * @param {string}
   * @returns {void}
   */
  private setDOMProperty(selector: string, rendererProperty: string, property: string, value: string): void {
    const htmlElement: HTMLElement = this.windowRef.document.querySelector(`${selector}`);
    if (htmlElement) {
      if (property === PROPERTY_TYPE.CLASS) {
        this.rendererService.renderer[rendererProperty](htmlElement, value);
      } else {
        this.rendererService.renderer[rendererProperty](htmlElement, property, value);
      }
    }
  }

  /**
   * initRulesButton to load the Rules button area
   * @returns {void}
   */
  private initRulesButton(): void {
    this.handleMultipleElements([PRE_OVERLAY.ENTRYAREA_OVERLAY_ID], PRE_OVERLAY.REMOVE_CLASS, [PRE_OVERLAY.ACTIVE], [PRE_OVERLAY.CLASS]);
    this.validateBaseElement();
    this.handleMultipleElements([PRE_OVERLAY.RULESBUTTON_OVERLAY_ID], PRE_OVERLAY.ADD_CLASS, [PRE_OVERLAY.ACTIVE], [PRE_OVERLAY.CLASS]);
    this.handleMultipleElements([PRE_OVERLAY.BUILD_BUTTON_CLASS], 'removeStyle', [PRE_OVERLAY.BORDER], [PRE_OVERLAY.BORDER]);
  }

  /**
   * getElementRect used to get the rect of dom element
   * @param {string}
   * @returns {DOMRect}
   */
  private getElementRect(elementName: string): DOMRect {
    return this.windowRef.document.querySelector(elementName).getBoundingClientRect();
  }

  /**
   * checkForModule used to check for the module view
   * @returns {boolean}
   */
  private checkForModule(): boolean {
    return this.windowRef.document.documentElement.className.includes(PRE_OVERLAY.MOBILE_VIEW);
  }

  /**
   * initPrizePool used to load the prize pool area
   * @returns {void}
   */
  private initPrizePool(): void {
    this.handleMultipleElements([PRE_OVERLAY.INTRODUCTION_OVERLAY_ID], PRE_OVERLAY.REMOVE_CLASS, [PRE_OVERLAY.ACTIVE], [PRE_OVERLAY.CLASS]);
    this.validateBaseElement();
    this.handleMultipleElements([PRE_OVERLAY.PRIZEPOOL_OVERLAY_ID], PRE_OVERLAY.ADD_CLASS, [PRE_OVERLAY.ACTIVE], [PRE_OVERLAY.CLASS]);
  }

  /**
   * initRulesArea used to load rules area
   * @returns {void}
   */
  private initRulesArea(): void {
    this.scrollTo();
    this.scrollToTop();
    this.handleMultipleElements([PRE_OVERLAY.PRIZEPOOL_OVERLAY_ID], PRE_OVERLAY.REMOVE_CLASS, [PRE_OVERLAY.ACTIVE], [PRE_OVERLAY.CLASS]);
    this.validateBaseElement();
    this.handleMultipleElements([PRE_OVERLAY.RULESAREA_OVERLAY_ID], PRE_OVERLAY.ADD_CLASS, [PRE_OVERLAY.ACTIVE], [PRE_OVERLAY.CLASS]);
  }

  /**
   * initEntriesArea used to load Entries area
   * @returns {void}
   */
  private initEntriesArea(): void {
    this.handleMultipleElements([PRE_OVERLAY.ANOTHERTEAM_ENTRIES_OVERLAY_ID], PRE_OVERLAY.REMOVE_CLASS, [PRE_OVERLAY.ACTIVE], [PRE_OVERLAY.CLASS]);
    this.validateBaseElement();
    this.handleMultipleElements([PRE_OVERLAY.ANOTHERTEAM_OVERLAY_ID], PRE_OVERLAY.ADD_CLASS, [PRE_OVERLAY.ACTIVE], [PRE_OVERLAY.CLASS]);
  }

  /**
   * initEntriesArea used to load Entries area
   * @returns {void}
   */
   private initSeparateEntriesArea(): void {
    this.handleMultipleElements([PRE_OVERLAY.RULESAREA_OVERLAY_ID], PRE_OVERLAY.REMOVE_CLASS, [PRE_OVERLAY.ACTIVE], [PRE_OVERLAY.CLASS]);
    this.validateBaseElement();
    this.handleMultipleElements([PRE_OVERLAY.ANOTHERTEAM_ENTRIES_OVERLAY_ID], PRE_OVERLAY.ADD_CLASS, [PRE_OVERLAY.ACTIVE], [PRE_OVERLAY.CLASS]);
  }

  /**
   * initEntryButton used to load entry button area
   * @returns {void}
   */
  private initEntryButton(): void {
    this.handleMultipleElements([PRE_OVERLAY.RULESAREA_OVERLAY_ID], PRE_OVERLAY.REMOVE_CLASS, [PRE_OVERLAY.ACTIVE], [PRE_OVERLAY.CLASS]);
    this.validateBaseElement();
    this.handleMultipleElements([PRE_OVERLAY.ENTRYAREA_OVERLAY_ID], PRE_OVERLAY.ADD_CLASS, [PRE_OVERLAY.ACTIVE], [PRE_OVERLAY.CLASS]);
  }

  /**
   * scrollWithElement used to scroll to particular position with element name
   * @param {string}
   * @returns {void}
   */
  private scrollWithElement(elementName: string): void {
    const elementRect: DOMRect = this.getElementRect(elementName);
    this.scrollSmooth(elementRect.y);
  }

  /**
   * scrollElement is used to scroll to particular div with HTMLElement.
   * @param { string }
   * @returns {void}
   */
  private scrollElement(element: string): void {
    const scrollView = this.getElementRect(element);
    this.windowRef.nativeWindow.scrollTo(scrollView.x, scrollView.y);
  }

  /**
   * scrollSmooth is used to scroll to particular div with HTMLElement.
   * @param { number }
   * @returns {void}
   */
  private scrollSmooth(topValue: number): void {
    this.windowRef.nativeWindow.scrollTo({ top: topValue, left: 0, behavior: 'smooth' });
  }

  /**
   * checkForElement is used check whether expected element is present in DOM.
   * @param { string[] }
   * @returns {boolean}
   */
  private checkForElement(elements: string[]): boolean {
    let elementCheck: boolean = true;
    elements.forEach((element) => {
      if (this.windowRef.document.querySelector(element) === null) {
        elementCheck = false;
      }
    });
    return elementCheck;
  }

  /**
   * getPrizePoolInformation is used get and show the prize pool information.
   * @returns {void}
   */
  private getPrizePoolInformation(): void {
    this.initPrizePool();
    const prizePoolRect: DOMRect = this.getElementRect(PRE_OVERLAY.PRIZE_POOL_CONTAINER);
    if (this.checkForElement([PRE_OVERLAY.MY_ENTRIES_CLASS])) {
      const myEntriesRect: DOMRect = this.getElementRect('fiveaside-entry-list');
      this.windowRef.nativeWindow.scrollTo(0, myEntriesRect.top + myEntriesRect.height - 100);
    } else {
      const buildBtnRect: DOMRect = this.getElementRect(PRE_OVERLAY.BUILD_BUTTON_CLASS);
      this.windowRef.nativeWindow.scrollTo(0, buildBtnRect.y - 6);
    }
    const updatedEl: DOMRect = this.getElementRect(PRE_OVERLAY.PRIZE_POOL_CONTAINER);
    this.setPrizePoolArea(prizePoolRect, updatedEl);
  }

  /**
   * getRulesAreaInformation is used get and show the Rules Area information.
   * @returns {void}
   */
  private getRulesAreaInformation(): void {
    this.initRulesArea();
    const rulesEntryAreaRect: DOMRect = this.getElementRect(PRE_OVERLAY.RULES_CONTAINER);
    const scrollArea: DOMRect = this.getElementRect(PRE_OVERLAY.RULES_BTN);
    this.windowRef.nativeWindow.scrollTo({ top: scrollArea.y - 60, left: 0});
    const rulesArea: DOMRect = this.getElementRect(PRE_OVERLAY.RULES_CONTAINER);
    this.setRulesArea(rulesArea, rulesEntryAreaRect);
  }

  /**
   * getBuildBtnInformation is used get and show the Build Button information.
   * @returns {void}
   */
  private getBuildBtnInformation(): void {
    if (this.checkForElement([PRE_OVERLAY.BUILD_BUTTON_CLASS, PRE_OVERLAY.RULES_ENTRY_AREA_CLASS])) {
      this.initEntryButton();
      const scrollArea: DOMRect = this.getElementRect(PRE_OVERLAY.RULES_BTN);
      if (this.checkForModule()) {
        this.windowRef.nativeWindow.scrollTo(0, scrollArea.y + 80);
      } else {
        this.windowRef.nativeWindow.scrollTo(0, scrollArea.y - 120);
      }
      const buildButton: DOMRect = this.getElementRect(PRE_OVERLAY.BUILD_BUTTON_CLASS);
      const rulesArea: DOMRect = this.getElementRect(PRE_OVERLAY.RULES_ENTRY_AREA_CLASS);
      this.setBuildArea(buildButton, rulesArea);
    } else {
      this.handleMultipleElements([PRE_OVERLAY.RULESAREA_OVERLAY_ID],
        PRE_OVERLAY.REMOVE_CLASS, [PRE_OVERLAY.ACTIVE], [PRE_OVERLAY.CLASS]);
      this.getRulesButton();
    }
  }

  /**
   * setPrizePoolArea is used set the values to achieve animations
   * Providing values in element in order to achieve animation perfectly.
   * @param { DOMRect }
   * @param { DOMRect }
   * @returns {void}
   */
  private setPrizePoolArea(prizePoolRect: DOMRect, updatedEl: DOMRect): void {
    if (this.checkForModule()) {
      this.setPrizeInformationModule(updatedEl);
    } else {
      this.setPrizeInformationData(prizePoolRect, updatedEl);
    }
  }

  /**
   * setPrizeInformationData is used set the values to achieve animations
   * Providing values in element in order to achieve animation perfectly.
   * @param { DOMRect }
   * @param { DOMRect }
   * @returns {void}
   */
  private setPrizeInformationData(prizePoolRect: DOMRect, updatedEl: DOMRect):void {
    if (this.checkForElement(['.prize-pool-header'])) {
      this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.RECTANGLE_ID, 4),
        PRE_OVERLAY.SET_STYLE, [`${prizePoolRect.top - 145}px`,
        `${updatedEl.width - 13}px`, '200px', 'absolute'], this.PRE_DOM.TOP_WIDTH_HEIGHT_POSITION);
      this.handleMultipleElements(this.PRE_DOM.PRIZE_DOM, PRE_OVERLAY.SET_STYLE,
        ['65px', `-${prizePoolRect.top + 40}px`,
        `-${prizePoolRect.top + 40}px`, `-${prizePoolRect.top + 50}px`],
        this.PRE_DOM.PRIZE_DOM_RECT);
    } else {
      this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.RECTANGLE_ID, 4),
        PRE_OVERLAY.SET_STYLE, [`${prizePoolRect.top - 145}px`,
        `${updatedEl.width - 13}px`, '150px', 'absolute'], this.PRE_DOM.TOP_WIDTH_HEIGHT_POSITION);
      this.handleMultipleElements(this.PRE_DOM.PRIZE_DOM, PRE_OVERLAY.SET_STYLE,
        ['65px', `-${prizePoolRect.top - 10}px`,
          `-${prizePoolRect.top - 10}px`, `-${prizePoolRect.top + 60}px`],
        this.PRE_DOM.PRIZE_DOM_RECT);
    }
  }

  /**
   * setPrizeInformationModule is used set the values to achieve animations
   * Providing values in element in order to achieve animation perfectly.
   * @param { DOMRect }
   * @returns {void}
   */
  private setPrizeInformationModule(updatedEl: DOMRect):void {
    const recordRect: DOMRect = this.getElementRect('.prize-pool-record');
    if (this.checkForElement(['.prize-pool-header'])) {
      this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.RECTANGLE_ID, 3),
      PRE_OVERLAY.SET_STYLE, ['116px', `${recordRect.right - 8}px`, '200px'], this.PRE_DOM.TOP_WIDTH_HEIGHT);
      this.handleMultipleElements(this.PRE_DOM.PRIZE_MODULE, PRE_OVERLAY.SET_STYLE,
        ['-284px', '-282px', '-290px'],
        this.preService.formParamArray(PRE_OVERLAY.BOTTOM, 3));
    } else {
      this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.RECTANGLE_ID, 3),
      PRE_OVERLAY.SET_STYLE, [`${recordRect.top}px`, `${recordRect.right - 8}px`, '150px'], this.PRE_DOM.TOP_WIDTH_HEIGHT);
      this.handleMultipleElements(this.PRE_DOM.PRIZE_MODULE, PRE_OVERLAY.SET_STYLE,
        ['-244px', '-262px', '-290px'],
        this.preService.formParamArray(PRE_OVERLAY.BOTTOM, 3));
    }
  }

  /**
   * setRulesArea is used set the values to achieve animations
   * Providing values in element in order to achieve animation perfectly.
   * @param { DOMRect }
   * @param { DOMRect }
   * @returns {void}
   */
  private setRulesArea(rulesArea: DOMRect, rulesEntryAreaRect: DOMRect): void {
    if (this.checkForModule()) {
      this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.RULES_AREA_ID, 4),
      PRE_OVERLAY.SET_STYLE, [`${rulesArea.top}px`, `${rulesArea.width}px`, `${rulesArea.height}px`, `${rulesArea.left}px`],
        this.PRE_DOM.TOP_WIDTH_HEIGHT_LEFT);
      this.handleMultipleElements(this.PRE_DOM.RULES_MODULE, PRE_OVERLAY.SET_STYLE,
        [`-${rulesArea.height + 50}px`, `-${rulesArea.height + 50}px`, `-${rulesArea.height + 50}px`],
        this.preService.formParamArray(PRE_OVERLAY.BOTTOM, 3));
    } else {
      this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.RULES_AREA_ID, 4), PRE_OVERLAY.SET_STYLE,
      [`${260 + this.topValue}px`, `${rulesArea.height}px`, '82px', `${rulesArea.width}px`],
        this.PRE_DOM.TOP_HEIGHT_LEFT_WIDTH);
      this.handleMultipleElements(this.PRE_DOM.RULES_RECT, PRE_OVERLAY.SET_STYLE,
        [`-${rulesEntryAreaRect.bottom - 200}px`, `${rulesEntryAreaRect.bottom - 180}px`, `${rulesEntryAreaRect.bottom - 170}px`],
        this.PRE_DOM.BOTTOM_TOP_TOP);
    }
  }

  /**
   * setAnotherBuildArea is used set the values to achieve animations
   * Providing values in element in order to achieve animation perfectly.
   * @returns {void}
   */
  private setAnotherBuildArea(rulesArea: DOMRect): void {
    const buildButton: DOMRect = this.getElementRect(PRE_OVERLAY.BUILD_BUTTON_CLASS);
    const myentriesCord: DOMRect = this.getElementRect(PRE_OVERLAY.FOCUS_CLASS);
    this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.ENTRY_AREA_NEW_ANOTHER_ID, 4), PRE_OVERLAY.SET_STYLE,
      [`${buildButton.top + 2}px`, `${buildButton.height - 2}px`, `${buildButton.left + 1}px`, `${buildButton.width - 2}px`],
      this.PRE_DOM.TOP_HEIGHT_LEFT_WIDTH);
    this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.ENTRY_AREA_BOX, 4), PRE_OVERLAY.SET_STYLE,
      [`${buildButton.top - 1}px`, `${50}px`, `${rulesArea.left}px`, `${rulesArea.width}px`],
      this.PRE_DOM.TOP_HEIGHT_LEFT_WIDTH);
    this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.USER_ENTRY_ID, 4), PRE_OVERLAY.SET_STYLE,
      [`${myentriesCord.top - 30}px`, `${myentriesCord.height + 25}px`, `${myentriesCord.left + 3}px`, `${myentriesCord.width - 6}px`],
      this.PRE_DOM.TOP_HEIGHT_LEFT_WIDTH);
    if (this.checkForModule()) {
      this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.ENTRY_AREA_NEW_ANOTHER_ID, 1), PRE_OVERLAY.SET_STYLE,
        ['0px 0px 4px 3px #007aff'], [PRE_OVERLAY.BOX_SHADOW]);
      this.handleMultipleElements(PRE_DOM_ELEMENT.BUILD_AREA_RECT,
        PRE_OVERLAY.SET_STYLE, [`-180.6px`, `-${buildButton.top + 10}px`, `-${buildButton.top + 20}px`],
        this.preService.formParamArray(PRE_OVERLAY.BOTTOM, 3));
    } else {
      const buildButtonD: DOMRect = this.getElementRect(PRE_OVERLAY.BUILD_BUTTON_CLASS);
      const myentriesCordD: DOMRect = this.getElementRect(PRE_OVERLAY.FOCUS_CLASS);
      this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.ENTRY_AREA_NEW_ANOTHER_ID, 1), PRE_OVERLAY.SET_STYLE,
    ['0px 0px 4px 3px #007aff,0 -315px 0 580px rgb(0 0 0 / 80%)'], [PRE_OVERLAY.BOX_SHADOW]);
      this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.ENTRY_AREA_NEW_ANOTHER_ID, 4), PRE_OVERLAY.SET_STYLE,
        [`${buildButtonD.top + 131 + this.topValue}px`, `${buildButtonD.height - 1}px`, '179px', `${buildButtonD.width - 6}px`],
        this.PRE_DOM.TOP_HEIGHT_LEFT_WIDTH);
      this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.USER_ENTRY_ID, 4), PRE_OVERLAY.SET_STYLE,
        [`${myentriesCordD.top + 100 + this.topValue}px`, `${myentriesCordD.height + 22}px`, '72px',
        `${myentriesCordD.width - 6}px`],
        this.PRE_DOM.TOP_HEIGHT_LEFT_WIDTH);
      this.handleMultipleElements([PRE_OVERLAY.ANOTHER_BUTTON_ARROW_ID], PRE_OVERLAY.SET_STYLE,
        [`${250 + this.topValue}px`], [PRE_OVERLAY.TOP]);
    }
  }

  /**
   * setAnotherBuildAreaForEntries is used set the values for entries area to achieve animations
   * Providing values in element in order to achieve animation perfectly.
   * @returns {void}
   */
  private setAnotherBuildAreaForEntries(): void {
    const myentriesCord: DOMRect = this.getElementRect(PRE_OVERLAY.FOCUS_CLASS);
    this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.USER_ENTRY_ID, 4), PRE_OVERLAY.SET_STYLE,
      [`${myentriesCord.top - 30}px`, `${myentriesCord.height + 25}px`, `${myentriesCord.left + 3}px`, `${myentriesCord.width - 6}px`],
      this.PRE_DOM.TOP_HEIGHT_LEFT_WIDTH);
    if (this.checkForModule()) {
      this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.ENTRY_AREA_ANOTHER_ID, 1), PRE_OVERLAY.SET_STYLE,
      ['0px 0px 4px 3px #007aff'], [PRE_OVERLAY.BOX_SHADOW]);
    } else {
      const myentriesCordD: DOMRect = this.getElementRect(PRE_OVERLAY.FOCUS_CLASS);
      this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.USER_ENTRY_ID, 4), PRE_OVERLAY.SET_STYLE,
        [`${myentriesCordD.top + 100 + this.topValue}px`, `${myentriesCordD.height + 22}px`, '72px',
        `${myentriesCordD.width - 6}px`],
        this.PRE_DOM.TOP_HEIGHT_LEFT_WIDTH);
      this.handleMultipleElements([PRE_OVERLAY.GO_TO_SECOND_HALF], PRE_OVERLAY.SET_STYLE,
        [`${myentriesCordD.top + 20 + this.topValue}px`], [PRE_OVERLAY.TOP]);
      this.handleMultipleElements([PRE_OVERLAY.ANOTHER_FOOTER_ID], PRE_OVERLAY.SET_STYLE,
        [`${myentriesCordD.top - 200 + this.topValue}px`], [PRE_OVERLAY.TOP]);
    }
  }

  /**
   * setBuildArea is used set the values to achieve animations
   * Providing values in element in order to achieve animation perfectly.
   * @param { DOMRect }
   * @param { DOMRect }
   * @returns {void}
   */
  private setBuildArea(buildButton: DOMRect, rulesArea: DOMRect): void {
    this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.ENTRY_AREA_BTN_ID, 4),
      PRE_OVERLAY.SET_STYLE,
      [`${buildButton.top}px`, `${buildButton.width - 1}px`, `${buildButton.height}px`, `${buildButton.left}px`],
      this.PRE_DOM.TOP_WIDTH_HEIGHT_LEFT);
    this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.ENTRY_AREA_ID, 4), PRE_OVERLAY.SET_STYLE,
      [`${buildButton.top - 1}px`, `${50}px`, `${rulesArea.left}px`, `${rulesArea.width}px`],
      this.PRE_DOM.TOP_HEIGHT_LEFT_WIDTH);
    this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.ENTRY_AREA_BTN_ID, 1), PRE_OVERLAY.SET_STYLE,
      ['0px 0px 4px 3px #007aff'], [PRE_OVERLAY.BOX_SHADOW]);
    if (this.checkForModule()) {
      this.handleMultipleElements(this.PRE_DOM.BUILD_BTN_MODULE, PRE_OVERLAY.SET_STYLE,
        [`-${rulesArea.height - 120}px`, `-${rulesArea.height - 110}px`, `-${rulesArea.height - 100}px`],
        this.preService.formParamArray(PRE_OVERLAY.BOTTOM, 3));
    } else {
      this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.ENTRY_AREA_BTN_ID, 4),
        PRE_OVERLAY.SET_STYLE,
        [`${buildButton.top + 111 + this.topValue}px`, `${buildButton.width}px`, `${buildButton.height - 1}px`, `${buildButton.left - 170}px`],
        this.PRE_DOM.TOP_WIDTH_HEIGHT_LEFT);
      this.handleMultipleElements(this.preService.formParamArray(PRE_OVERLAY.ENTRY_AREA_ID, 4), PRE_OVERLAY.SET_STYLE,
        [`${212 + this.topValue}px`, `${rulesArea.height}px`, '65px', `${rulesArea.width}px`], this.PRE_DOM.TOP_HEIGHT_LEFT_WIDTH);
      this.handleMultipleElements(this.PRE_DOM.BUILD_BTN_RECT, PRE_OVERLAY.SET_STYLE,
        [`-${rulesArea.bottom + rulesArea.top - 20}px`, `-${rulesArea.bottom + rulesArea.top - 15}px`, `-${rulesArea.bottom + rulesArea.top - 10}px`],
        this.preService.formParamArray(PRE_OVERLAY.BOTTOM, 3));
    }
  }

  /**
   * setRulesButtonArea is used set the values to achieve animations
   * Providing values in element in order to achieve animation perfectly.
   * @param { DOMRect }
   * @returns {void}
   */
  private setRulesButtonArea(rulesRect: DOMRect): void {
    if (this.checkForModule()) {
      this.handleMultipleElements([PRE_OVERLAY.RULES_BTN_AREA_ID],
        PRE_OVERLAY.SET_STYLE, ['0 0 4px 3px #007aff, 0 0 0 775px rgb(0 0 0 / 88%)'], [PRE_OVERLAY.BOX_SHADOW]);
      this.handleMultipleElements([PRE_OVERLAY.RULES_BTN_AREA_ID, PRE_OVERLAY.RULES_BTN_AREA_ID],
        PRE_OVERLAY.SET_STYLE, [`${rulesRect.left - 9}px`, `${rulesRect.top - 17}px`],
        [PRE_OVERLAY.LEFT, PRE_OVERLAY.TOP]);
    } else {
      this.handleMultipleElements([PRE_OVERLAY.RULES_BTN_AREA_ID],
        PRE_OVERLAY.SET_STYLE, ['25px'], ['border-radius']);
      const rulesArea: DOMRect = this.getElementRect('.rules-btn');
      this.handleMultipleElements(['#rules-button-area','#rules-button-area' ],
        PRE_OVERLAY.SET_STYLE, [`${rulesArea.left - 178}px`, `${215 + this.topValue}px`], [PRE_OVERLAY.LEFT, PRE_OVERLAY.TOP]);
    }
  }
}
