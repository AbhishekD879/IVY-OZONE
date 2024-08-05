import { Component, EventEmitter, Input, OnDestroy, OnInit, Output, ChangeDetectorRef } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { CmsService } from '@app/core/services/cms/cms.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RendererService } from '@app/shared/services/renderer/renderer.service';
import { GTM_EVENTS, LIVE_OVERLAY, LOBBY_OVERLAY } from '@app/fiveASideShowDown/constants/constants';
import { IWelcomeOverlay } from '@app/fiveASideShowDown/models/welcome-overlay';
import {
  cardPrizeInfo, entryInfoArrow, liveCardArrow, liveEntriesArrow, showdownCardArrow, teamProgressArrow,
  teamProgressDownArrow, textButtonWelcome, textContentFade, textContentNoDelay
} from '@app/fiveASideShowDown/components/fiveAsideLobbyOverlay/fiveaside-lobby-overlay.animation';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';

@Component({
  selector: 'five-a-side-live-event-overlay',
  template: ``,
  animations: [
    textContentNoDelay,
    textContentFade,
    textButtonWelcome,
    showdownCardArrow,
    entryInfoArrow,
    cardPrizeInfo,
    teamProgressArrow,
    liveCardArrow,
    teamProgressDownArrow,
    liveEntriesArrow
  ],
})
export class FiveASideLiveEventOverlayComponent implements OnInit, OnDestroy {
  @Input() baseClass: string;
  @Input() tutorialData: IWelcomeOverlay | any;
  @Output() readonly clearOverlay = new EventEmitter();
  protected timer: number;
  protected readonly WELCOME_OVERLAY_ID: string = LIVE_OVERLAY.ID;
  protected overlay: HTMLElement;
  protected baseOverlayElement: HTMLElement;
  protected readonly CONTEST_OVERLAY_CLASS_NAME: string = LIVE_OVERLAY.CLASS;
  public tutorialSteps: { [key: string]: boolean } = { step1: true, step2: false, step3: false, step4: false, step5: false };
  public isMultiEntriesPresent: boolean = false;
  public isMyEntryPresent: boolean = false;
  public componentId: string;
  public entryUpdateReceived: boolean = false;
  private activeStep: string;
  private viewReloaded: boolean = false;
  constructor(protected cmsService: CmsService,
    protected rendererService: RendererService,
    protected windowRef: WindowRefService,
    protected deviceService: DeviceService,
    protected domSanitizer: DomSanitizer,
    protected gtmService: GtmService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected pubsubService: PubSubService,
    protected coreToolsService: CoreToolsService
  ) { }

  /**
   * Init method for component
   * @returns void
   */
  ngOnInit(): void {
    this.overlay = this.windowRef.document.getElementById(this.WELCOME_OVERLAY_ID);
    this.validateOverlayBaseElement();
    this.initLiveOverlayElements();
    this.windowRef.nativeWindow.localStorage.setItem(LIVE_OVERLAY.OVERLAY, true);
    this.componentId = this.coreToolsService.uuid();
    this.initEntryExpandedListener();
    this.enableDisableIOSBodyScroll('add');
  }

  /**
   * Destroy method for component
   * @returns void
   */
  ngOnDestroy(): void {
    this.onCloseLiveOverlay();
    this.windowRef.nativeWindow.clearTimeout(this.timer);
    this.pubsubService.unsubscribe(this.componentId);
    this.enableDisableIOSBodyScroll('remove');
  }

  /**
   * Disable background body scrolling for iOS devices when overlay is on
   * @param  {string} action
   * @returns void
   */
  enableDisableIOSBodyScroll(action: string): void {
    const liveOverlay = this.windowRef.document.getElementById(LIVE_OVERLAY.ID);
    if (this.deviceService.isIos && liveOverlay) {
      this.preventScrollForTouchMove = this.preventScrollForTouchMove.bind(this);
      this.preventScrollForTouchStart = this.preventScrollForTouchStart.bind(this);
      if (action === 'add') {
        liveOverlay.addEventListener('touchmove', this.preventScrollForTouchMove, { passive: false });
        liveOverlay.addEventListener('touchstart', this.preventScrollForTouchStart, { passive: false });
      } else {
        liveOverlay.removeEventListener('touchmove', this.preventScrollForTouchMove);
        liveOverlay.removeEventListener('touchstart', this.preventScrollForTouchStart);
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
    const allowedIds = ['close-div', 'close-svg', 'close-qb-svg'];
    const selectedId = (event.target as HTMLInputElement).id;
    if (allowedIds.includes(selectedId) || (event.target as HTMLInputElement).localName === 'button') {
      return false;
    }
    event.preventDefault();
  }

  /**
   * Listener for Team progress update
   * @returns void
   */
  initEntryExpandedListener(): void {
    this.pubsubService.subscribe(this.componentId, LIVE_OVERLAY.ENTRY_OPENED_TUTORIAL_OVERLAY, () => {
      if (!this.entryUpdateReceived) {
        this.scrollToBannerView();
        this.entryUpdateReceived = true;
        this.entrySummaryMethod(LIVE_OVERLAY.ID_MY_ENTRY_YOUR_TEAM_EXPAND);
        return;
      }
      if (this.entryUpdateReceived && !this.viewReloaded && this.activeStep === '4') {
        this.viewReloaded = true;
        this.onClickNext(this.activeStep);
      }
    });
  }

  /**
   * Listens for leg update for defined time and skips to next step
   * @returns void
   */
  entryExpandTimeoutListener(): void {
    this.timer = this.windowRef.nativeWindow.setTimeout(() => {
      this.skipToNextEntryUpdate();
    }, LIVE_OVERLAY.TIMEOUT_DURATION);
  }

  /**
   * Skip to next step if update not received
   * @returns void
   */
  skipToNextEntryUpdate(): void {
    if (!this.entryUpdateReceived) {
      this.entryUpdateReceived = true;
      this.onClickNext('4');
    }
  }

  /**
   * Handler to close Liveoverlay
   * @param  {string='close'} action
   * @returns void
   */
  onCloseLiveOverlay(action?: string): void {
    if (action) {
      this.liveTutorialGATrack(action);
    }
    this.enableDisableIOSBodyScroll('remove');
    this.rendererService.renderer.removeClass(this.baseOverlayElement, this.CONTEST_OVERLAY_CLASS_NAME);
    this.rendererService.renderer.removeClass(this.overlay, 'active');
    this.clearOverlay.emit();
    this.pubsubService.unsubscribe(this.componentId);
    this.setElementDOMProperty(LIVE_OVERLAY.ID_SUMMARY_EXPANDED, LIVE_OVERLAY.SET_STYLE, 'display',
        `unset`);
  }

  /**
   * Live overlay tutorial steps handler
   * @param  {string} step
   * @returns void
   */
  onClickNext(step: string): void {
    this.activeStep  =step;
    switch (step) {
      case '2':
        this.updateTutorialsSteps(step);
        this.showFiveASideTeamProgress(LIVE_OVERLAY.SEL_ENTRY_SUMMARY, LIVE_OVERLAY.ID_MY_ENTRY_YOUR_TEAM);
        break;
      case '3':
        this.updateTutorialsSteps(step);
        this.showFiveASideTeamProgressExpanded();
        break;
      case '4':
        this.updateTutorialsSteps(step);
        this.showEntryProgressbarTutorial(LIVE_OVERLAY.SEL_MYENTRY_PROGRESS, LIVE_OVERLAY.ID_ENTRY_PROGRESS_INFO);
        break;
      case '5':
        this.updateTutorialsSteps(step);
        this.showLeaderboardEntriesTutorial(LIVE_OVERLAY.ID_LEADERBOARD_INFO);
        break;
      case LIVE_OVERLAY.FINISH:
        this.onCloseLiveOverlay(LIVE_OVERLAY.FINISH);
        break;
      default:
        break;
    }
  }

  /**
   * Method to show team progress screen
   * @param  {string} toBeHighlightEl
   * @param  {string} highlightHolder
   * @returns void
   */
  protected showFiveASideTeamProgress(toBeHighlightEl: string, highlightHolder: string): void {
    this.scrollToBannerView();
    this.windowRef.nativeWindow.scrollTo(0, 0);
    this.scrollToTopForDesktop();
    const myEntrySummaryEl = this.windowRef.document.querySelector(LIVE_OVERLAY.SEL_MYENTRY_WIDGET);
    const highlightEl: HTMLElement = this.windowRef.document.querySelector(highlightHolder);
    if (!myEntrySummaryEl || !highlightEl) {
      this.onClickNext('4');
      return;
    }
    const entryEl: HTMLElement = myEntrySummaryEl.querySelector(toBeHighlightEl);
    this.isMyEntryPresent = true;
    const isEntryExpanded = myEntrySummaryEl.querySelector(LIVE_OVERLAY.ID_SUMMARY_EXPANDED);
    if (isEntryExpanded) {
      this.entrySummaryMethod(LIVE_OVERLAY.ID_MY_ENTRY_YOUR_TEAM_EXPAND);
      return;
    }
    if (entryEl) {
      this.setDomPropertiesForTeamProgress(highlightHolder, entryEl);
    }
    this.liveTutorialGATrack(GTM_EVENTS.NEXT_STEP_1_LABEL);
  }

  /**
   * Set dom properties for Team progress
   * @param  {string} highlightHolder
   * @param  {HTMLElement} entryEl
   */
  protected setDomPropertiesForTeamProgress(highlightHolder: string, entryEl: HTMLElement) {
    this.windowRef.nativeWindow.scrollTo(0, entryEl.getBoundingClientRect().top - 210);
    const entry: DOMRect = entryEl.getBoundingClientRect();
    this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP, `${entry.top}px`);
    this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.LEFT,
      `${entry.left}px`);
    this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.WIDTH,
      `${entry.width}px`);
    this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.HEIGHT,
      `${entry.height}px`);
    this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.HEIGHT,
      `${entry.height}px`);
    this.setElementDOMProperty(LIVE_OVERLAY.ID_MY_ENTRY_TEAM_ARROW, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP,
      `${entry.height + 10}px`);
    this.setElementDOMProperty(LIVE_OVERLAY.ID_CARD_INFO_CONTENT, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP,
      `${entry.height * 2 - 50}px`);
    this.unsetNativeBackgroundColor();
  }

  /**
   * Set DOM properties for expanded entry
   * @param  {string} highlightHolder
   * @returns void
   */
  protected entrySummaryMethod(highlightHolder: string): void {
    const entrySummaryEl = this.windowRef.document.querySelector(LIVE_OVERLAY.SEL_MYENTRY_WIDGET);
    this.updateTutorialsSteps('3');
    this.changeDetectorRef.detectChanges();
    const legsListEl = this.windowRef.document.querySelector(LIVE_OVERLAY.ID_LEGS_LIST_DISPLAY);
    let legsChildren: Element;
    let legEl: DOMRect;
    if (entrySummaryEl && legsListEl && legsListEl.children.length) {
      legsChildren = legsListEl.children.length > 1 ? legsListEl.children[1] : legsListEl.children[0];
      legEl = legsChildren.getBoundingClientRect();
      this.windowRef.nativeWindow.scrollTo(0, legEl.top - 200);
      legEl = legsChildren.getBoundingClientRect();
      if (legEl.height === 0) {
        this.onClickNext('4');
      } else {
        this.setDomPropertiesEntryProgress(highlightHolder, legEl);
      }
    } else {
      this.onClickNext('4');
    }
    this.liveTutorialGATrack(GTM_EVENTS.NEXT_STEP_2_LABEL);
  }

  /**
   * Set DOM properties for Entry progress
   * @param  {string} highlightHolder
   * @param  {DOMRect} legEl
   */
  protected setDomPropertiesEntryProgress(highlightHolder: string, legEl: DOMRect) {
    const entryContainer = this.windowRef.document.querySelector(LIVE_OVERLAY.ID_SUMMARY_EXPANDED);
    if (entryContainer) {
      const entryContainerRect: DOMRect = entryContainer.getBoundingClientRect();
      this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP, `${legEl.top}px`);
      this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.WIDTH,
        `${entryContainerRect.width}px`);
      this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.HEIGHT,
        `${legEl.height}px`);
      this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.LEFT,
        `${entryContainerRect.left}px`);
      this.setElementDOMProperty(LIVE_OVERLAY.ID_ARROW_ENTRY_EXPAND, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP,
        `${legEl.height + 20}px`);
      this.setElementDOMProperty(LIVE_OVERLAY.ID_EXPAND_TEAM_PROGRESS, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP,
        `${legEl.height + 25}px`);
      this.unsetNativeBackgroundColor();
    }
  }

  /**
   * Show expanded team progress method
   * @returns void
   */
  protected showFiveASideTeamProgressExpanded(): void {
    this.scrollToBannerView();
    const entrySummaryEl = this.windowRef.document.querySelector(LIVE_OVERLAY.SEL_MYENTRY_WIDGET);
    if (!this.isMyEntryPresent || !entrySummaryEl) {
      this.onClickNext('4');
      return;
    }
    const entryEl: HTMLElement = entrySummaryEl.querySelector(LIVE_OVERLAY.FOCUS);
    if (entryEl) {
      // entrySummaryEl.scrollIntoView();
      entryEl.click();
      this.entryExpandTimeoutListener();
    } else {
      this.onClickNext('4');
    }
  }

  /**
   * Handler for Entry progressbar tutorial
   * @param  {string} toBeHighlightEl
   * @param  {string} highlightHolder
   * @returns void
   */
  protected showEntryProgressbarTutorial(toBeHighlightEl: string, highlightHolder: string): void {
    this.entryUpdateReceived = true;
    this.scrollToBannerView();
    this.windowRef.nativeWindow.scrollTo(0, 0);
    const entrySummaryEl = this.windowRef.document.querySelector(LIVE_OVERLAY.SEL_MYENTRY_WIDGET);
    const progressBarEl: HTMLElement = this.windowRef.document.querySelector(toBeHighlightEl);
    const highlightEl: HTMLElement = this.windowRef.document.querySelector(highlightHolder);
    const entriesProgressBar: HTMLElement = this.windowRef.document.querySelector(LIVE_OVERLAY.ID_PROGRESSBAR_OVERLAY);
    if (!entrySummaryEl || !progressBarEl || !highlightEl || !entriesProgressBar) {
      this.onClickNext('5');
      return;
    }
    const entryEl: HTMLElement = entrySummaryEl.querySelector(LIVE_OVERLAY.FOCUS);
    if (entryEl) {
      entryEl.click();
      this.setElementDOMProperty(LIVE_OVERLAY.ID_SUMMARY_EXPANDED, LIVE_OVERLAY.SET_STYLE, 'display',
        `none`);
    }
    this.isMultiEntriesPresent = entriesProgressBar.children.length > 1;
    this.setDomPropertiesEntryProgressBar(highlightHolder, progressBarEl);
    this.liveTutorialGATrack(GTM_EVENTS.NEXT_STEP_3_LABEL);
  }

  /**
   * Method to set DOM properties for Entry progress bar
   * @param  {string} highlightHolder
   * @param  {HTMLElement} progressBarEl
   */
  protected setDomPropertiesEntryProgressBar(highlightHolder: string, progressBarEl: HTMLElement) {
    let entry: DOMRect = progressBarEl.getBoundingClientRect();
    this.windowRef.nativeWindow.scrollTo(0, entry.top - 180);
    entry = progressBarEl.getBoundingClientRect();
    this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP, `${entry.top}px`);
    this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.WIDTH,
      `${entry.width}px`);
    this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.HEIGHT,
      `${entry.height}px`);
    this.setElementDOMProperty(LIVE_OVERLAY.ID_ENTRY_TOP_PROGRESS_CONTENT, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.BOTTOM,
      `${entry.height * 2}px`);
    this.setElementDOMProperty(LIVE_OVERLAY.ID_PROGRESS_ARROW, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP,
      `${entry.height}px`);
    this.setElementDOMProperty(LIVE_OVERLAY.ID_CARD_INFO_CONTENT, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP,
      `${entry.height * 1.5}px`);
    this.unsetNativeBackgroundColor();
  }

  /**
   * Method to display Leaderboard entries tutorial
   * @param  {string} highlightHolder
   * @returns void
   */
  protected showLeaderboardEntriesTutorial(highlightHolder: string): void {
    this.setElementDOMProperty(LIVE_OVERLAY.ID_SUMMARY_EXPANDED, LIVE_OVERLAY.SET_STYLE, 'display',
        `unset`);
    this.scrollToBannerView();
    const highlightEl: HTMLElement = this.windowRef.document.querySelector(highlightHolder);
    const leaderboardItemEl = this.windowRef.document.querySelector(LIVE_OVERLAY.ID_LIVE_LEADERBOARD_ITEM);
    const leaderboardTitleEl = this.windowRef.document.querySelector(LIVE_OVERLAY.CLASS_LIVE_LEADERBOARD_TITLE);
    if (!highlightEl || !leaderboardItemEl || !leaderboardTitleEl) {
      this.onClickNext('5');
      return;
    }
    const leaderboardItem = leaderboardItemEl.getBoundingClientRect();
    let leaderboardTitle = leaderboardTitleEl.getBoundingClientRect();
    this.windowRef.nativeWindow.scrollTo(0, leaderboardTitle.top * 0.8);
    leaderboardTitle = leaderboardTitleEl.getBoundingClientRect();
    const calcHeight = this.calculateLeaderboardEntriesHeight() + leaderboardTitle.height;
    // let calcHeight = calculateLeaderboardEntriesHeight();
    this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP, `${leaderboardTitle.top - 4}px`);
    this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.WIDTH,
      `${leaderboardItem.width + 4}px`);
    this.setElementDOMProperty(highlightHolder, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.HEIGHT,
      `${calcHeight + 17}px`);
    this.setElementDOMProperty(LIVE_OVERLAY.ID_CARD_INFO_CONTENT, LIVE_OVERLAY.SET_STYLE, LOBBY_OVERLAY.STYLE.TOP,
      `${calcHeight + 50}px`);
    this.unsetNativeBackgroundColor();
    this.liveTutorialGATrack(GTM_EVENTS.NEXT_STEP_4_LABEL);
  }

  /**
   * Returns the Leaderboard entries height
   * @returns number
   */
  protected calculateLeaderboardEntriesHeight(entriesIndex: number = 0): number {
    let height = 0;
    const entryItems: NodeListOf<HTMLElement> = this.windowRef.document.querySelectorAll(LIVE_OVERLAY.ID_LIVE_LEADERBOARD_ITEM);
    for (let index = 0; index < entryItems.length; index++) {
      height = height + entryItems[index].getBoundingClientRect().height;
      if (index === entriesIndex) {
        break;
      }
    }
    return height;
  }

  /**
   * Method to unset native background color
   * @returns void
   */
  protected unsetNativeBackgroundColor(): void {
    const parentEl = this.windowRef.document.querySelector(`#${LIVE_OVERLAY.ID}`);
    this.rendererService.renderer.setStyle(parentEl, LOBBY_OVERLAY.STYLE.BG_COLOR, LOBBY_OVERLAY.STYLE.UNSET);
  }

  /**
   * Initialize Overlay Elements
   * @returns {void}
   */
  protected initLiveOverlayElements(): void {
    this.rendererService.renderer.addClass(this.overlay, 'active');
    this.rendererService.renderer.addClass(this.baseOverlayElement, this.CONTEST_OVERLAY_CLASS_NAME);
  }

  /**
   * Method to set TOP, LEFT DOM properties
   * @param  {HTMLElement} element
   * @param  {number} top
   * @param  {number} left
   * @returns void
   */
  protected setTopLeftPropsToElement(element: HTMLElement, top: number, left: number): void {
    this.rendererService.renderer.setStyle(element, LOBBY_OVERLAY.STYLE.TOP, `${top}px`);
    this.rendererService.renderer.setStyle(element, LOBBY_OVERLAY.STYLE.LEFT, `${left}px`);
  }

  /**
   * To call change changeDetection
   * @returns void
   */
  protected scrollToBannerView(): void {
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Util method for setting DOM properties
   * @param  {string} selector
   * @param  {string} rendererProperty
   * @param  {string} property
   * @param  {string} value
   * @returns void
   */
  protected setElementDOMProperty(selector: string, rendererProperty: string, property: string, value: string): void {
    const htmlElement: HTMLElement = this.windowRef.document.querySelector(`${selector}`);
    if (htmlElement) {
      this.rendererService.renderer[rendererProperty](htmlElement, property, value);
    }
  }

  /**
   * Set and update tutorial steps
   * @param  {string} step
   * @returns void
   */
  protected updateTutorialsSteps(step: string): void {
    this.tutorialSteps = { step1: false, step2: false, step3: false, step4: false, step5: false };
    this.tutorialSteps[`step${step}`] = true;
  }

  /**
   * GA tracking for Live tutorial
   * @param  {string} label
   * @returns void
   */
   protected liveTutorialGATrack(label: string): void {
    const trackingObj = {
      eventCategory: '5-A-Side Showdown',
      eventAction: 'live tutorial',
      eventLabel: label
    };
    this.gtmService.push('trackEvent', trackingObj);
  }

  /**
   * To Validate base element based on input
   * @returns {void}
   */
  private validateOverlayBaseElement(): void {
    if (this.baseClass) {
      this.baseOverlayElement = this.windowRef.document.querySelector(this.baseClass);
    } else {
      this.baseOverlayElement = this.deviceService.isWrapper ?
        this.windowRef.document.querySelector('body') as HTMLElement : this.windowRef.document.querySelector('html, body');
    }
  }
  /**
   * Scrolls to Top of the container before starting the tutorial
   * @returns void
   */
  private scrollToTopForDesktop(): void {
    const containerEl = this.windowRef.document.querySelector('#custom-scroll');
    if (this.deviceService.isDesktop && containerEl) {
      containerEl.scrollTo(0,0);
    }
  }
}
