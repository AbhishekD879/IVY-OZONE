import { Component, EventEmitter, Input, OnDestroy, OnInit, Output, ChangeDetectorRef } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { CmsService } from '@app/core/services/cms/cms.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RendererService } from '@app/shared/services/renderer/renderer.service';
import { GTM_EVENTS, LOBBY_OVERLAY } from '@app/fiveASideShowDown/constants/constants';
import {
  cardPrizeInfo, entryInfoArrow, entryInfoArrowMobile, showdownCardArrow,
  textButtonWelcome, textContentFade, textContentNoDelay
} from '@app/fiveASideShowDown/components/fiveAsideLobbyOverlay/fiveaside-lobby-overlay.animation';
import { IWelcomeOverlay } from '@app/fiveASideShowDown/models/welcome-overlay';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
import { BodyScrollLockService } from '@app/betslip/services/bodyScrollLock/betslip-body-scroll-lock.service';

@Component({
  selector: 'fiveaside-lobby-overlay',
  template: ``,
  animations: [
    textContentNoDelay,
    textContentFade,
    textButtonWelcome,
    showdownCardArrow,
    entryInfoArrow,
    entryInfoArrowMobile,
    cardPrizeInfo
  ]
})
export class FiveASideLobbyOverlayComponent implements OnInit, OnDestroy {
  @Input() baseClass: string;
  @Input() tutorialData: IWelcomeOverlay;
  @Output() readonly clearOverlay = new EventEmitter();
  protected readonly WELCOME_OVERLAY_ID: string = LOBBY_OVERLAY.ID;
  protected overlay: HTMLElement;
  protected baseOverlayElement: HTMLElement;
  protected readonly CONTEST_OVERLAY_CLASS_NAME: string = LOBBY_OVERLAY.CLASS;
  public tutorialSteps = { step1: true, step2: false, step3: false, step4: false };
  public signPostTop = '500px';
  private activeStep: string;
  private componentId: string;
  private timer: number;
  constructor(protected cmsService: CmsService,
    protected rendererService: RendererService,
    protected windowRef: WindowRefService,
    protected deviceService: DeviceService,
    protected domSanitizer: DomSanitizer,
    protected gtmService: GtmService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected pubSubService: PubSubService,
    private coreToolsService: CoreToolsService,
    protected bodyScrollLockService: BodyScrollLockService
  ) { }

  /**
   * Init method
   * @returns void
   */
  ngOnInit(): void {
    this.overlay = this.windowRef.document.getElementById(this.WELCOME_OVERLAY_ID);
    this.validateOverlayBaseElement();
    this.initLobbyOverlayElements();
    this.componentId = this.coreToolsService.uuid();
    this.windowRef.nativeWindow.localStorage.setItem('lobbyOverlay', true);
    this.lobbyDataChangeListener();
    this.enableDisableIOSBodyScroll('add');
  }

  /**
   * Component destroy method
   * @returns void
   */
  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.componentId);
    this.windowRef.nativeWindow.clearTimeout(this.timer);
    this.onCloseLobbyOverlay();
    this.enableDisableIOSBodyScroll('remove');
  }

  /**
   * Disable background body scrolling for iOS devices when overlay is on
   * @param  {string} action
   * @returns void
   */
  enableDisableIOSBodyScroll(action: string): void {
    const lobbyOverlay = this.windowRef.document.getElementById(LOBBY_OVERLAY.ID);
    if (this.deviceService.isIos && lobbyOverlay) {
      this.preventScrollForTouchMove = this.preventScrollForTouchMove.bind(this);
      this.preventScrollForTouchStart = this.preventScrollForTouchStart.bind(this);
      if (action === 'add') {
        lobbyOverlay.addEventListener('touchmove', this.preventScrollForTouchMove, { passive: false });
        lobbyOverlay.addEventListener('touchstart', this.preventScrollForTouchStart, { passive: false });
      } else {
        lobbyOverlay.removeEventListener('touchmove', this.preventScrollForTouchMove);
        lobbyOverlay.removeEventListener('touchstart', this.preventScrollForTouchStart);
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
   * Handler to close LobbyOverlay
   * @param  {string='close'} action
   * @returns void
   */
  onCloseLobbyOverlay(action?: string): void {
    if (action) {
      this.lobbyTutorialGATrack(action);
    }
    this.enableDisableIOSBodyScroll('remove');
    this.rendererService.renderer.removeClass(this.baseOverlayElement, this.CONTEST_OVERLAY_CLASS_NAME);
    this.rendererService.renderer.removeClass(this.overlay, 'active');
    this.clearOverlay.emit();
  }

  /**
   * Lobby overlay tutorial steps handler
   * @param  {string} step
   * @returns void
   */
  onClickNext(step: string): void {
    this.activeStep = step;
    switch (step) {
      case '2':
        this.updateTutorialsSteps(step);
        this.showEntryPrizesTutorial(LOBBY_OVERLAY.ID_CARD_TOTAL_PRIZES, LOBBY_OVERLAY.ID_ENTRY_PRIZES);
        break;
      case '3':
        this.updateTutorialsSteps(step);
        this.showEntryInfoTutorial(LOBBY_OVERLAY.ID_CARD_ENTRY_INFO, LOBBY_OVERLAY.ID_ENTRY_INFO);
        break;
      case '4':
        this.updateTutorialsSteps(step);
        this.showShowdownCardTutorial(LOBBY_OVERLAY.ID_CARD_MAIN, LOBBY_OVERLAY.ID_CARD_INFO);
        break;
      case LOBBY_OVERLAY.FINISH:
        this.onCloseLobbyOverlay('finish');
        break;
      default:
        break;
    }
  }

  /**
   * Lobby data change listener
   * @returns void
   */
  protected lobbyDataChangeListener(): void {
    this.pubSubService.subscribe(this.componentId, LOBBY_OVERLAY.LOBBY_DATA_RELOADED_COMPLETED, () => {
      this.timer = this.windowRef.nativeWindow.setTimeout(() => {
        this.reInitTutorial();
      }, 1000);
    });
  }

  /**
   * Resume tutorial from current step
   * @returns void
   */
  protected reInitTutorial(): void {
    if (this.activeStep && this.activeStep !== LOBBY_OVERLAY.FINISH) {
      this.onClickNext(this.activeStep);
    }
  }

  /**
   * GA tracking for Lobby tutorial
   * @param  {string} label
   * @returns void
   */
  protected lobbyTutorialGATrack(label: string): void {
    const trackingObj = {
      eventCategory: '5-A-Side Showdown',
      eventAction: 'lobby tutorial',
      eventLabel: label
    };
    this.gtmService.push('trackEvent', trackingObj);
  }

  /**
   * To call scroll method and change changeDetection
   * @returns void
   */
  protected scrollToBannerView(): void {
    this.changeDetectorRef.detectChanges();
    const bannerEl = this.windowRef.document.querySelector(LOBBY_OVERLAY.BANNER_ID);
    if (bannerEl) {
      bannerEl.scrollIntoView();
    }
  }

  /**
   * Initialize Overlay Elements
   * @returns {void}
   */
  protected initLobbyOverlayElements(): void {
    this.rendererService.renderer.addClass(this.overlay, 'active');
    this.rendererService.renderer.addClass(this.baseOverlayElement, this.CONTEST_OVERLAY_CLASS_NAME);
  }

  /**
   * Method to show entry prizes tutorial
   * @param  {string} toBeHighlightEl
   * @param  {string} highlightHolder
   * @returns void
   */
  protected showEntryPrizesTutorial(toBeHighlightEl: string, highlightHolder: string): void {
    this.scrollToBannerView();
    this.windowRef.nativeWindow.scrollTo(0, 0);
    const entryEl: HTMLElement = this.windowRef.document.querySelector(toBeHighlightEl);
    const highlightEl: HTMLElement = this.windowRef.document.querySelector(highlightHolder);
    if (!entryEl || !highlightEl) {
      this.onClickNext('3');
      return;
    }
    let entry: DOMRect = entryEl.getBoundingClientRect();
    this.windowRef.nativeWindow.scrollTo(0, entry.top - 110);
    entry = entryEl.getBoundingClientRect();
    const topPixels = entry.top - 17;
    const leftPixels = entry.left - 6;
    this.setTopLeftPropsToElement(highlightEl, topPixels, leftPixels);
    this.showLobbySignPostingTutorial(entryEl);
  }

  /**
   * Method to set DOM properties
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
   * Method to display sign posting tutorial
   * @param  {HTMLElement} entryEl
   * @returns void
   */
  protected showLobbySignPostingTutorial(entryEl: HTMLElement): void {
    const signPosting: HTMLElement = entryEl.parentElement.parentElement.parentElement.parentElement;
    if (signPosting) {
      const rectEl: HTMLElement = signPosting.querySelector(LOBBY_OVERLAY.SIGN_POST);
      if (rectEl && rectEl.parentElement) {
        const rect: DOMRect = rectEl.getBoundingClientRect();
        const rectElParentLeft = rectEl.parentElement.getBoundingClientRect().left;
        const rectElParentWidth = rectEl.parentElement.offsetWidth;
        this.setElementDOMProperty(LOBBY_OVERLAY.ID_SIGN_POST, 'setStyle', LOBBY_OVERLAY.STYLE.TOP, `${rect.top - 12}px`);
        this.setElementDOMProperty(LOBBY_OVERLAY.ID_SIGN_POST, 'setStyle', LOBBY_OVERLAY.STYLE.LEFT,
          `${rectElParentLeft}px`);
        this.setElementDOMProperty(LOBBY_OVERLAY.ID_SIGN_POST, 'setStyle', LOBBY_OVERLAY.STYLE.WIDTH,
          `${rectElParentWidth}px`);
        this.unsetNativeBackgroundColor();
        this.lobbyTutorialGATrack(GTM_EVENTS.NEXT_STEP_1_LABEL);
      }
    }
  }

  /**
   * Method to display show entry info tutorial
   * @param  {string} toBeHighlightEl
   * @param  {string} highlightHolder
   * @returns void
   */
  protected showEntryInfoTutorial(toBeHighlightEl: string, highlightHolder: string): void {
    this.scrollToBannerView();
    this.windowRef.nativeWindow.scrollTo(0, 0);
    const entryEl = this.windowRef.document.querySelector(toBeHighlightEl);
    const el1: HTMLElement = this.windowRef.document.querySelector(highlightHolder);
    if (!entryEl || !el1) {
      this.onClickNext('4');
      return;
    }
    let entry = entryEl.getBoundingClientRect();
    this.windowRef.nativeWindow.scrollTo(0, entry.top - 105);
    entry = entryEl.getBoundingClientRect();
    const topPixels = entry.top - 16;
    const leftPixels = entry.left - 11;
    const cardParentEl = entryEl.parentElement;
    if (cardParentEl) {
      this.rendererService.renderer.setStyle(el1, LOBBY_OVERLAY.STYLE.WIDTH, `${entry.width + 19}px`);
      this.setElementDOMProperty('#entry-info-text', 'setStyle', LOBBY_OVERLAY.STYLE.TOP,
        `${topPixels + 200}px`);
    }
    this.setTopLeftPropsToElement(el1, topPixels, leftPixels);
    this.unsetNativeBackgroundColor();
    this.lobbyTutorialGATrack(GTM_EVENTS.NEXT_STEP_2_LABEL);
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
   * Method to display showdown card tutorial
   * @param  {string} toBeHighlightEl
   * @param  {string} highlightHolder
   * @returns void
   */
  protected showShowdownCardTutorial(toBeHighlightEl: string, highlightHolder: string): void {
    this.changeDetectorRef.detectChanges();
    this.windowRef.nativeWindow.scrollTo(0, 0);
    const entryEl: HTMLElement = this.windowRef.document.querySelector(toBeHighlightEl);
    const el1: HTMLElement = this.windowRef.document.querySelector(highlightHolder);
    if (!entryEl || !el1) {
      this.onClickNext(LOBBY_OVERLAY.FINISH);
      return;
    }
    let entry: DOMRect = entryEl.getBoundingClientRect();
    this.windowRef.nativeWindow.scrollTo(0, entry.top - 85);
    entry = entryEl.getBoundingClientRect();
    const topPixels = entry.top + 5;
    const leftPixels = entry.left + 2;
    this.setTopLeftPropsToElement(el1, topPixels, leftPixels);
    this.rendererService.renderer.setStyle(el1, LOBBY_OVERLAY.STYLE.HEIGHT, `${entry.height}px`);
    this.rendererService.renderer.setStyle(el1, LOBBY_OVERLAY.STYLE.WIDTH, `${entryEl.offsetWidth - 8}px`);
    this.unsetNativeBackgroundColor();
    this.lobbyTutorialGATrack(GTM_EVENTS.NEXT_STEP_3_LABEL);
  }

  /**
   * Method to unset native background color
   * @returns void
   */
  protected unsetNativeBackgroundColor(): void {
    const parentEl = this.windowRef.document.querySelector(`#${LOBBY_OVERLAY.ID}`);
    this.rendererService.renderer.setStyle(parentEl, LOBBY_OVERLAY.STYLE.BG_COLOR, LOBBY_OVERLAY.STYLE.UNSET);
  }

  /**
   * Set and update tutorial steps
   * @param  {string} step
   * @returns void
   */
  protected updateTutorialsSteps(step: string): void {
    this.tutorialSteps = { step1: false, step2: false, step3: false, step4: false };
    this.tutorialSteps[`step${step}`] = true;
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
        this.windowRef.document.querySelector('body') : this.windowRef.document.querySelector('html, body');
    }
  }
}
