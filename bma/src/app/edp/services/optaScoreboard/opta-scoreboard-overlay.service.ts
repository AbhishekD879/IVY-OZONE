import { Injectable } from '@angular/core';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import environment from '@environment/oxygenEnvConfig';

@Injectable({
  providedIn: 'root'
})
export class OptaScoreboardOverlayService {
  overlayElement: HTMLElement = null;
  wrapperElement: HTMLElement = null;

  private optaEnv: string = '';
  private readonly wrapperId: string = 'opta-scoreboard-overlay-wrapper';
  private readonly overlayTagName: string = 'scoreboard-overlay';
  private readonly overlayShownBodyClass: string = 'opta-scoreboard-overlay-shown';
  private readonly closeOverlayEventName: string = 'closeScoreboardOverlay';

  constructor(
    private windowRefService: WindowRefService,
    private pubSubService: PubSubService
  ) {
    this.optaEnv = environment.OPTA_SCOREBOARD.ENV;
  }

  /**
   * initialise the overlay
   * @returns {HTMLElement}
   */
  initOverlay(): HTMLElement {
    if(this.overlayElement) {
      this.overlayElement.removeEventListener(this.closeOverlayEventName, this.hideOverlay);
    }
    this.wrapperElement = this.windowRefService.document.getElementById(this.wrapperId);
    this.overlayElement = this.wrapperElement ? this.wrapperElement.querySelector(this.overlayTagName) : null;
    if(this.overlayElement) {
      this.overlayElement.addEventListener(this.closeOverlayEventName, this.hideOverlay);
    }
    return this.overlayElement || this.createOverlay();
  }

  /**
   * destruct the overlay
   * @returns {void}
   */
  destroyOverlay(): void {
    if (this.overlayElement) {
      this.overlayElement.removeEventListener(this.closeOverlayEventName, this.hideOverlay);
      this.overlayElement.remove();
    }

    if (this.wrapperElement) {
      this.hideOverlay();
      this.wrapperElement.remove();
    }
    this.overlayElement = null;
    this.wrapperElement = null;
  }

  /**
   * show the overlay
   * @returns {void}
   */
  showOverlay = (): void => {
    if (this.wrapperElement) {
      this.wrapperElement.classList.add('visible');
      this.windowRefService.document.body.classList.add(this.overlayShownBodyClass);
    }
  }

  /**
   * hide the overlay
   * @returns {void}
   */
  hideOverlay = (): void => {
    this.pubSubService.publish('NETWORK_INDICATOR_INDEX_HIDE', false);
    if (this.wrapperElement) {
      this.wrapperElement.classList.remove('visible');
    }
    this.windowRefService.document.body.classList.remove(this.overlayShownBodyClass);
  }

  /**
   * set the overlaydata
   * @param { Object } data
   * @returns {void}
   */
  setOverlayData(data: Object = {}): void {
    if (this.overlayElement) {
      const sbData = Object.assign({
        env: this.optaEnv,
        sport: 'FOOTBALL',
        provider: 'digital'
      }, data);
      this.overlayElement.setAttribute('sb-data', JSON.stringify(sbData));
    }
  }

  /**
   * create the overlay
   * @returns {HTMLElement}
   */
  private createOverlay(): HTMLElement {
    this.destroyOverlay(); // clean-up any left-overs
    this.wrapperElement = this.windowRefService.document.createElement('div');
    this.overlayElement = this.windowRefService.document.createElement(this.overlayTagName);
    this.overlayElement.addEventListener(this.closeOverlayEventName, this.hideOverlay);
    this.wrapperElement.setAttribute('id', this.wrapperId);
    this.wrapperElement.appendChild(this.overlayElement);
    this.windowRefService.document.body.appendChild(this.wrapperElement);
    return this.overlayElement;
  }
}
