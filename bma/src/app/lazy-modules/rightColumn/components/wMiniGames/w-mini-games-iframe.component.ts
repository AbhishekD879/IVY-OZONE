import { Component, OnInit, HostListener, OnDestroy } from '@angular/core';
import { CasinoGamesService } from '@vanillaInitModule/services/casinoGames/casino-games.service';
import { SafeResourceUrl, DomSanitizer } from '@angular/platform-browser';
import { MINI_GAMES_IFRAME_CONSTANTS } from './w-mini-games-event.constants';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'w-mini-games-iframe',
  styleUrls: ['./w-mini-games-iframe.component.scss'],
  templateUrl: 'w-mini-games-iframe.component.html'
})

export class WMiniGamesIframeComponent implements OnInit, OnDestroy {

  miniGamesUrl: SafeResourceUrl;
  showContent = false;
  isError = false;
  showLoadingSpinner = true;

  private readonly title = 'wMiniGamesIframeComponent';

  constructor(
    private casinoGamesService: CasinoGamesService,
    private sanitizer: DomSanitizer,
    private pubSubService: PubSubService
  ) {}

  ngOnInit(): void {
    this.setIframeUrl();
    this.pubSubService.subscribe(this.title, this.pubSubService.API.SESSION_LOGIN, () => this.setIframeUrl());
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.title);
  }

  /**
   * listener for post messages from mini games iframe
   * @param event
   */
  @HostListener('window:message', ['$event'])
  onMessage(event: MessageEvent): void {
    this.handleMessage(event);
  }

  /**
   * defines action and calls corresponding action handler
   * @param event
   */
  handleMessage(event: MessageEvent): void {
    const action = event.data.type;
    switch (action) {
      case MINI_GAMES_IFRAME_CONSTANTS.ACTIONS.LOBBY_LOADED:
        this.openIFrame();
        break;
      case MINI_GAMES_IFRAME_CONSTANTS.ACTIONS.SHOW_LOGIN:
        this.openLoginDialog();
        break;
      case MINI_GAMES_IFRAME_CONSTANTS.ACTIONS.LOBBY_FEED_ERROR:
        this.handleErrorIFrame();
        break;
      default:
        break;
    }
  }

  /**
   * If post message SHOW_LOGIN, open login popup
   */
  private openLoginDialog(): void {
    this.pubSubService.publish(this.pubSubService.API.OPEN_LOGIN_DIALOG);
  }

  /**
   * 1 case: Init iframe
   * 2 case: If user logged in, reInit iframe
   */
  private setIframeUrl(): void {
    this.showContent = false;
    this.showLoadingSpinner = true;
    this.miniGamesUrl = this.sanitizer.bypassSecurityTrustResourceUrl(this.casinoGamesService.miniGamesUrl);
  }

  /**
   * If post message LOBBY_LOADED, show IFrame content
   */
  private openIFrame(): void {
    this.showContent = true;
    this.isError = false;
    this.showLoadingSpinner = false;
  }

  /**
   * If post message LOBBY_FEED_ERROR, handle error message
   */
  private handleErrorIFrame(): void {
    this.isError = true;
    this.showContent = false;
    this.showLoadingSpinner = false;
  }

}
