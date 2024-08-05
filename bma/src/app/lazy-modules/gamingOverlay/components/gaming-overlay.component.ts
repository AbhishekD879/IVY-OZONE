import { Component, OnInit, HostBinding, ChangeDetectionStrategy, OnDestroy } from '@angular/core';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { IGamingOverlayProperties } from '@app/lazy-modules/gamingOverlay/components/gaming-overlay.model';
import { GAMING_CONSTANTS } from '@lazy-modules/gamingOverlay/components/gaming-overlay.constants';

@Component({
  selector: 'gaming-overlay',
  templateUrl: './gaming-overlay.component.html',
  styleUrls: ['./gaming-overlay.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class GamingOverlayComponent implements OnInit, OnDestroy {
  @HostBinding('class.isActive') isActive: boolean = true;

  overlayProperties: IGamingOverlayProperties = {
    hideCloseButton: true
  };
  casinoOverlayElement: Element;
  splashOverlayElement: Element;
  private readonly componentName: string = 'GamingOverlay';

  constructor(
    private windowRef: WindowRefService,
    private pubSubService: PubSubService,
    private renderer: RendererService
  ) { }

  ngOnInit(): void {
    this.pubSubService.subscribe(this.componentName, this.pubSubService.API.GAMING_OVERLAY_OPEN, () => {
      this.isActive = true;
    });
    this.windowRef.document.addEventListener(GAMING_CONSTANTS.OVERLAY_LOADED_EVENT, this.onSportsOverlayLoaded);
  }

  ngOnDestroy() {
    this.pubSubService.unsubscribe(this.componentName);
  }

  /***
   * Close the overlay on the click
   */
  handleCloseClick(): void {
    setTimeout(() => {
      this.pubSubService.publish(this.pubSubService.API.GAMING_OVERLAY_CLOSE);
      this.isActive = false;
    }, GAMING_CONSTANTS.OVERLAY_CLOSING_TIMEOUT);
    this.casinoOverlayElement = this.windowRef.document.querySelector(GAMING_CONSTANTS.CASINO_OVERLAY_CLASS);
    this.splashOverlayElement = this.windowRef.document.querySelector(GAMING_CONSTANTS.SPLASH_OVERLAY_CLASS);
    this.windowRef.document.removeEventListener(GAMING_CONSTANTS.OVERLAY_LOADED_EVENT, this.onSportsOverlayLoaded);
    this.renderer.renderer.addClass(this.casinoOverlayElement, GAMING_CONSTANTS.HIDE_OVERLAY_CLASS);
    this.renderer.renderer.removeClass(this.splashOverlayElement, GAMING_CONSTANTS.HIDE_OVERLAY_CLASS);
  }

  /**
   * Function called on event listener dispatched
   */
  private onSportsOverlayLoaded(data): void {
    setTimeout(() => {
      data.target.querySelector(GAMING_CONSTANTS.SPLASH_OVERLAY_CLASS).classList.add(GAMING_CONSTANTS.HIDE_OVERLAY_CLASS);
      data.target.querySelector(GAMING_CONSTANTS.CASINO_OVERLAY_CLASS).classList.remove(GAMING_CONSTANTS.HIDE_OVERLAY_CLASS);
    }, GAMING_CONSTANTS.OVERLAY_LOADED_TIMEOUT);
  }
}
