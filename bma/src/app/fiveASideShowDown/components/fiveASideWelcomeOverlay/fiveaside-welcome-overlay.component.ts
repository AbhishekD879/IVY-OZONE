import {
  ChangeDetectorRef,
  Component,
  EventEmitter,
  Input,
  OnInit,
  Output
} from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DeviceService } from '@core/services/device/device.service';
import { IWelcomeOverlay } from '@app/fiveASideShowDown/models/welcome-overlay';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { LIVE_OVERLAY, welcome_GA_Tag } from '@app/fiveASideShowDown/constants/constants';
import { FiveASideCmsService } from '@app/fiveASideShowDown/services/fiveaside-cms.service';
@Component({
  selector: 'fiveaside-welcome-overlay',
  template: ``
})
export class FiveasideWelcomeOverlayComponent implements OnInit {
  @Input() baseClass: string;
  @Input() currentOverlay: string;
  @Input() lobbyTutorial: boolean;
  @Input() preEventData: string;
  @Input() tutorialData: IWelcomeOverlay;
  @Input() liveTutorial: boolean;
  @Output() readonly clearOverlay = new EventEmitter();
  isPreEvent: boolean = false;
  public isLobbyOverlay: boolean = false;
  public isLiveOverlay: boolean = false;
  public welcomeCard: IWelcomeOverlay;
  public welcomeUrl: SafeResourceUrl | any;
  public videoPlayer: boolean = true;
  public showImage: boolean = false;
  protected readonly WELCOME_OVERLAY_ID: string = 'fiveaside-welcome-overlay';
  protected overlay: HTMLElement;
  protected baseOverlayElement: HTMLElement;
  protected readonly CONTEST_OVERLAY_CLASS_NAME: string = 'fiveaside-cards-overlay';
  private showdownOverlay: boolean = false;
  private welcomeOverlaySeen: boolean = false;

  constructor(protected cmsService: FiveASideCmsService,
    protected rendererService: RendererService,
    protected windowRef: WindowRefService,
    protected deviceService: DeviceService,
    protected domSanitizer: DomSanitizer,
    protected gtmService: GtmService,
    protected changeDetectorRef: ChangeDetectorRef) { }

  /**
   * Init method
   * @returns void
   */
  ngOnInit(): void {
    this.overlay = this.windowRef.document.getElementById(this.WELCOME_OVERLAY_ID);
    this.welcomeOverlaySeen = this.windowRef.nativeWindow.localStorage.getItem('showdownOverlay');
    if (this.windowRef.nativeWindow.localStorage.getItem('showdownOverlay')) {
      this.showdownOverlay = true;
    }
    this.checkOverlayDisplayed();
    this.validateBaseElement();
    this.getWelcomeOverlayCMS();
    this.initOverlayElements();
    this.lobbyTutorialTrigger();
    this.liveTutorialTrigger();
  }

  /**
   * Method to open lobby overlay
   * @returns void
   */
  lobbyTutorialTrigger(): void {
    if (this.lobbyTutorial) {
      this.showdownOverlay = false;
      this.checkOverlayDisplayed();
    } else if (this.welcomeOverlaySeen && this.currentOverlay === 'LOBBY') {
      this.startLobbyOverlay();
    }
  }

  /**
   * Remove existing welcome overlay and start lobby overlay
   * @returns void
   */
  startLobbyOverlay(): void {
    this.rendererService.renderer.removeClass(this.baseOverlayElement, this.CONTEST_OVERLAY_CLASS_NAME);
    this.rendererService.renderer.removeClass(this.overlay, 'active');
    this.isLobbyOverlay = true;
  }

  /**
   * Triggered when overlay x svg icon is clicked
   * @returns {void}
   */
  onCloseWelcomeOverlay(): void {
    this.rendererService.renderer.removeClass(this.baseOverlayElement, this.CONTEST_OVERLAY_CLASS_NAME);
    this.rendererService.renderer.removeClass(this.overlay, 'active');
    this.clearOverlay.emit();
  }

  /**
   * Method to open live overlay
   * @returns void
   */
  liveTutorialTrigger(): void {
    if (this.liveTutorial) {
      this.showdownOverlay = false;
      this.checkOverlayDisplayed();
    } else if (this.welcomeOverlaySeen && this.currentOverlay === 'LIVE-EVENT') {
      this.startLiveEventOverlay();
    }
  }

  /**
   * getStartedClick is used to check for event specific.
   * @returns {void}
   */
  getStartedClick(): void {
    switch (this.currentOverlay) {
      case 'LOBBY':
        this.startLobbyOverlay();
        this.videoPlayer = false;
        break;
      case 'PREEVENT':
        this.getPreEvent();
        this.videoPlayer = false;
        break;
      case 'LIVE-EVENT':
        this.startLiveEventOverlay();
        this.videoPlayer = false;
        break;
      default:
        break;
    }
    this.gtmService.push('trackEvent', welcome_GA_Tag.getStartedGa);
  }

  /**
   * getPreEvent is used to check is pre event
   * @returns {void}
   */
  getPreEvent() {
    this.rendererService.renderer.removeClass(this.baseOverlayElement, this.CONTEST_OVERLAY_CLASS_NAME);
    this.rendererService.renderer.removeClass(this.overlay, 'active');
    this.isPreEvent = true;
  }

  /**
   * Remove existing welcome overlay and start live overlay
   */
  startLiveEventOverlay() {
    this.rendererService.renderer.removeClass(this.baseOverlayElement, this.CONTEST_OVERLAY_CLASS_NAME);
    this.rendererService.renderer.removeClass(this.overlay, 'active');
    this.isLiveOverlay = true;
  }

  /**
   * check iframe loaded or not
   */
  iframeLoaded(): void {
    this.showImage = true;
  }

  /**
   * Initialize Overlay Elements
   * @returns {void}
   */
  protected initOverlayElements(): void {
    this.rendererService.renderer.addClass(this.overlay, 'active');
    this.rendererService.renderer.addClass(this.baseOverlayElement, this.CONTEST_OVERLAY_CLASS_NAME);
  }

  private checkOverlayDisplayed(): void {
    if (!this.showdownOverlay) {
      this.validateBaseElement();
      this.getWelcomeOverlayCMS();
      this.initOverlayElements();
    }
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
   * To fetch welcome overlay from CMS
   * @returns {void}
   */
  private getWelcomeOverlayCMS(): void {
    this.cmsService.getWelcomeOverlay().subscribe((response: IWelcomeOverlay) => {
      if (response) {
        this.windowRef.nativeWindow.localStorage.setItem('showdownOverlay', true);
        const url = `${LIVE_OVERLAY.YOUTUBE}${response.videoURL}`;
        this.welcomeUrl = url;
      }
      this.welcomeCard = response;
    }, (error) => {
      console.warn(error);
    });
  }
}
