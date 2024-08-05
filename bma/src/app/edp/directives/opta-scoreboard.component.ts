import {
  Component,
  ElementRef,
  Input,
  NgZone,
  OnChanges,
  OnDestroy,
  OnInit,
  SimpleChanges,
  ViewEncapsulation,
  AfterViewInit,
  Output,
  EventEmitter
} from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { OptaScoreboardOverlayService } from '@edp/services/optaScoreboard/opta-scoreboard-overlay.service';

@Component({
  // eslint-disable-next-line
  encapsulation : ViewEncapsulation.None,
  selector: 'opta-scoreboard',
  styleUrls: ['opta-scoreboard-overlay.scss'],
  template: '<div></div>'      // TODO: move to directive after edp module migration
})
export class OptaScoreboardComponent implements OnInit, OnDestroy, OnChanges, AfterViewInit {

  @Input() event: ISportEvent;
  @Input() toggleScoreboard?: boolean;

  @Output() readonly isLoaded: EventEmitter<boolean> = new EventEmitter();

  private eventId: number = null;
  private env: string = '';
  private scoreboardContainer: HTMLElement = null;
  private scoreboardOverlay: HTMLElement  = null;
  private scoreboardOverlayWrapper: HTMLElement = null;
  private windowOrientationChangeListener: any;
  private updateCarouselTimer: number;
  private isLoadedValue: boolean;

  constructor(
    private elementRef: ElementRef,
    private gtmService: GtmService,
    private pubSubService: PubSubService,
    private ngZone: NgZone,
    private windowRefService: WindowRefService,
    private rendererService: RendererService,
    private optaScoreboardOverlayService: OptaScoreboardOverlayService
  ) {
    this.overlayHandlerFn = this.overlayHandlerFn.bind(this);
    this.gtmHandlerFn = this.gtmHandlerFn.bind(this);
    this.scoreboardHandlerFn = this.scoreboardHandlerFn.bind(this);
    this.hideOptaScoreboardHandlerFn = this.hideOptaScoreboardHandlerFn.bind(this);
    this.updateCarousel = this.updateCarousel.bind(this);
    this.env = environment.OPTA_SCOREBOARD.ENV;
  }

  /**
   * Main init function.
   * @private
   */
  ngOnInit(): void {
    this.eventId = this.event.id;

    // Execute outside of the Angular zone
    this.ngZone.runOutsideAngular(() => {
      this.initializeScoreboards();
      this.windowOrientationChangeListener = this.rendererService.renderer.listen(
        this.windowRefService.nativeWindow, 'orientationchange', this.updateCarousel);
    });
  }

  ngAfterViewInit(): void {
    this.pubSubService.publish(this.pubSubService.API.SCOREBOARD_VISUALIZATION_LOADED);
  }

  ngOnDestroy(): void {
    this.windowOrientationChangeListener && this.windowOrientationChangeListener();
    if (this.scoreboardContainer) {
      this.scoreboardContainer.remove();
    }
    this.optaScoreboardOverlayService.hideOverlay();

    if (this.scoreboardOverlayWrapper) {
      if (this.scoreboardOverlayWrapper.classList.contains('visible')) {
        this.scoreboardOverlayWrapper.classList.remove('visible');
        this.windowRefService.document.body.classList.remove('opta-scoreboard-overlay-shown');
      }
      this.scoreboardOverlay.removeEventListener('closeScoreboardOverlay', this.overlayHandlerFn);
    }

    this.clearUpdateCarouselTimer();
  }

  ngOnChanges(changes: SimpleChanges): void {
    // Update carousel component after it was toggled from hidden to visible state
    if (changes.toggleScoreboard && changes.toggleScoreboard.previousValue && !changes.toggleScoreboard.currentValue) {
      this.updateCarousel();
    }
  }

  private showScoreboardOverlayFn = (customEvent: CustomEvent): void => {
    this.setParameters(this.scoreboardOverlay, { overlayKey: customEvent.detail.scoreboardKey });
    this.optaScoreboardOverlayService.showOverlay();
  }

  private getOverlayWrapper(eventId: number, env: string): HTMLElement {
    return this.windowRefService.document.querySelector('div#opta-scoreboard-overlay-wrapper')
      || this.createOverlayWrapper(eventId, env);
  }

  private createOverlayWrapper(eventId: number, env: string): HTMLElement {
    const scoreboardOverlay = this.windowRefService.document.createElement('scoreboard-overlay');
    const scoreboardOverlayWrapper = this.windowRefService.document.createElement('div');

    this.setParameters(scoreboardOverlay, {matchId: eventId, env: env});
    scoreboardOverlayWrapper.setAttribute('id', 'opta-scoreboard-overlay-wrapper');
    scoreboardOverlayWrapper.appendChild(scoreboardOverlay);

    this.windowRefService.document.body.appendChild(scoreboardOverlayWrapper);

    return scoreboardOverlayWrapper;
  }

  private scoreboardHandlerFn(customEvent): void {
    this.setParameters(this.scoreboardOverlay, {overlayKey: customEvent.detail.scoreboardKey});
    this.scoreboardOverlayWrapper.classList.add('visible');
    this.windowRefService.document.body.classList.add('opta-scoreboard-overlay-shown');
    this.pubSubService.publish('NETWORK_INDICATOR_INDEX_HIDE', true);
  }

  /**
   * Should hide Opta scoreboard when receive custom event 'hideScoreboardComponent'
   */
   private hideOptaScoreboardHandlerFn = (): void => {
    this.pubSubService.publish(this.pubSubService.API.HIDE_OPTA_SCOREBOARD);
  }

  private gtmHandlerFn = (customEvent): void => {
    this.gtmService.push('trackEvent', customEvent.detail);
    if (!this.isLoadedValue) {
      this.isLoadedValue = true;
      this.isLoaded.emit(true);
    }
  }

  private overlayHandlerFn(): void {
    this.scoreboardOverlayWrapper.classList.remove('visible');
    this.windowRefService.document.body.classList.remove('opta-scoreboard-overlay-shown');
    this.pubSubService.publish('NETWORK_INDICATOR_INDEX_HIDE', false);
  }

  /**
   * Initialize scoreboard container and overlay
   */
  private initializeScoreboards(): void {
    // Initialize scoreboard Container
    this.scoreboardContainer = this.windowRefService.document.createElement('scoreboard-container');
    this.setParameters(this.scoreboardContainer);
    this.scoreboardContainer.addEventListener('showScoreboardOverlay', this.showScoreboardOverlayFn);
    this.scoreboardContainer.addEventListener('showScoreboardOverlay', this.scoreboardHandlerFn);
    this.scoreboardContainer.addEventListener('hideScoreboardComponent', this.hideOptaScoreboardHandlerFn);
    this.scoreboardContainer.addEventListener('googleAnalyticsData', this.gtmHandlerFn, true);
    this.elementRef.nativeElement.appendChild(this.scoreboardContainer);

    // Initialize scoreboard Overlay and scoreboard Overlay Wrapper
    this.scoreboardOverlayWrapper = this.getOverlayWrapper(this.eventId, this.env);
    this.scoreboardOverlay = this.scoreboardOverlayWrapper.querySelector('scoreboard-overlay');
    this.scoreboardOverlay.addEventListener('closeScoreboardOverlay', this.overlayHandlerFn);
    this.scoreboardOverlay = this.optaScoreboardOverlayService.initOverlay();

    if (this.getParameters(this.scoreboardOverlay).matchId !== this.eventId) {
      this.setParameters(this.scoreboardOverlay);
    }
  }

  private setParameters(scoreboardElement: HTMLElement, options?: Object): void {
    const sbData = {
      matchId: this.eventId,
      env: this.env,
      sport: this.event.categoryCode,
      provider: 'digital', // TODO add other data providers support
      ...options
    };
    scoreboardElement.setAttribute('sb-data', JSON.stringify(sbData));
  }

  private getParameters(scoreboardElement: HTMLElement) {
    const sbData = scoreboardElement.getAttribute('sb-data');
    if (!sbData) {
      return {};
    }
    try {
      const result = JSON.parse(sbData);
      return (typeof result === 'object') ? result : {};
    } catch (error) {
      return {};
    }
  }

  private clearUpdateCarouselTimer(): void {
    if (this.updateCarouselTimer) {
      this.windowRefService.nativeWindow.clearTimeout(this.updateCarouselTimer);
    }
  }

  private updateCarousel(): void {
    this.clearUpdateCarouselTimer();

    this.updateCarouselTimer = this.windowRefService.nativeWindow.setTimeout(() => {
      (this.scoreboardContainer as any).carousel.updateCarousel();
    }, 500);
  }
}
