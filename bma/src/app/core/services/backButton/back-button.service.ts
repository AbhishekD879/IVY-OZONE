import { filter } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { Location } from '@angular/common';
import { NavigationEnd, Router } from '@angular/router';

import { StorageService } from '@core/services/storage/storage.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';


@Injectable()
export class BackButtonService {
  private segmentsArray: { segmentName: string; url: string; }[] = [];
  private previousPage: string;
  private hiFromBackButton: boolean;

  constructor(private storage: StorageService,
              private location: Location,
              protected window: WindowRefService,
              private router: Router,
              private routingService: RoutingState,
              private pubSubService: PubSubService) {

    this.pubSubService.subscribe('backButtonFactory', this.pubSubService.API.LAST_MADE_BET, () => {
      if (this.window.nativeWindow.sandbox === undefined) {
        this.storage.set('lastMadeBet', this.location.path());
      }
    });

    this.router.events.pipe(
        filter(event => event instanceof NavigationEnd))
        .subscribe(() => {
          // eslint-disable-next-line complexity
          if (this.hiFromBackButton) {
            this.hiFromBackButton = false;
            return;
          }
          // Clear segmentArray on home page.
          if (this.routingService.getCurrentUrl() !== this.routingService.getPreviousUrl() && this.routingService.getCurrentSegment()) {
            const cur: string = this.routingService.getCurrentSegment(),
              prev: string = this.routingService.getRouteSegment('segment', this.routingService.getPreviousRouteSnapshot());

            if (this.isRoute(cur, 'home')) {
              this.segmentsArray = [];
            }

            const isPreviousUrlMenu = this.routingService.getPreviousUrl().includes('menu');
            const isPreviousUrlMobileportal = this.routingService.getPreviousUrl().includes('mobileportal/');

            // hiFromBackButton - checking if routing with back button
            if (!(this.isRoute(cur, 'eventMain') && this.isRoute(prev, 'eventMain')) &&
              !(this.isRoute(cur, 'olympics.sport.eventMain') && this.isRoute(prev, 'olympics.sport.eventMain')) &&
              !this.isRoute(cur, '404') &&
              !(this.isRoute(cur, 'tote.event') && this.isRoute(prev, 'tote.event')) &&
              !isPreviousUrlMenu) {
              // Pushing object with route name and route params
              this.segmentsArray.push({
                segmentName: prev,
                url: this.routingService.getPreviousUrl()
              });
            }

            if ((this.isRoute(cur, 'horseracing.eventMain') || this.isRoute(cur, 'greyhound.eventMain')) &&
              (this.isRoute(prev, 'horseracing.eventMain') || this.isRoute(prev, 'greyhound.eventMain'))) {
              this.segmentsArray.push({
                segmentName: prev,
                url: this.routingService.getPreviousUrl()
              });
            }

            // Business logic for sports
            if ((this.isRoute(cur, 'sport.matches') ||
              this.isRoute(cur, 'sport.display') ||
              this.isRoute(cur, 'lotto-results.filter') ||
              this.isRoute(cur, 'olympicsSport.display.tab') ||
              this.isRoute(cur, 'olympicsSport.display')) &&
              (this.isRoute(prev, 'sport.matches') ||
                this.isRoute(prev, 'sport.display') || prev === 'sport' ||
                this.isRoute(prev, 'lotto-results') ||
                this.isRoute(prev, 'olympicsSport.display'))) {
              this.segmentsArray.pop();
            }

            // Lotto
            if (this.isRoute(cur, 'lotto') && this.isRoute(prev, 'lotto.lottery-receipt')) {
              this.segmentsArray.pop();
              this.segmentsArray.pop();
            }

            // Business logic for freebets
            if (this.isRoute(cur, 'freebets') && this.isRoute(prev, 'eventMain')) {
              this.segmentsArray.pop();
              this.segmentsArray.push({
                segmentName: prev,
                url: this.routingService.getPreviousUrl()
              });
            }

            // To avoid necessity to double click on backbutton in case of autoredirection to
            if ((this.isRoute(cur, 'horseracing.display') || this.isRoute(cur, 'greyhound.display')) &&
              (this.isRoute('horseracing', prev) || this.isRoute('greyhound', prev))) {
                const segmentsArrayLength = this.segmentsArray.length;
                if(segmentsArrayLength>=2 && this.segmentsArray[segmentsArrayLength - 1].url === this.segmentsArray[segmentsArrayLength - 2].url) {
                  this.segmentsArray.pop();
                }
            }

            // Business logic for Leagues
            if (this.isRoute(cur, 'leagues') && this.isRoute(prev, 'leagues')) {
              this.segmentsArray.pop();
            }

            // Business logic for inplay
            if (this.isRoute(prev, 'inPlay.firstSport') ||
              (this.isRoute(cur, 'tabs.cashout') && this.isRoute(prev, 'tabs.cashout')) ||
              (this.isRoute(cur, 'azSports') && this.isRoute(prev, 'azSports'))) {
              this.segmentsArray.pop();
            }

            // Business logic for Account history
            if (this.isRoute(cur, 'accountHistoryTabs') && this.isRoute(prev, 'accountHistoryTabs')) {
              this.segmentsArray.pop();
            }

            // Business logic for virtual
            if (this.isRoute(prev, 'virtual-sports.category') || this.isRoute(prev, 'virtual-sports.class') || this.isRoute(prev, 'virtual-sports.sports')) {
              this.segmentsArray.pop();
            }

            // Business logic for Big Competitions
            if ((this.isRoute(cur, 'bigCompetition.tab') && this.isRoute(prev, 'bigCompetition.tab')) ||
              this.isRoute(cur, 'bigCompetition.subtab') || this.isRoute(prev, 'bigCompetition.subtab') ||
              (this.isRoute(cur, 'bigCompetition.tab') && this.isRoute(prev, 'bigCompetition'))) {
              this.segmentsArray.pop();
            }

            // Business logic for Mobileportal
            if (isPreviousUrlMobileportal) {
              this.segmentsArray.pop();
            }

            // Business logic for deposit
            if (this.isRoute(cur, 'deposit.registered')) {
              this.segmentsArray.pop();
            }

            // Business logic for gambling controls
            if (this.isRoute(cur, 'account-closure.step-two') || this.isRoute(prev, 'account-closure.step-two')) {
              this.segmentsArray.pop();
            }

            // Business logic for account closure step two
            if (!this.isRoute(cur, 'account-closure.step-one') && this.isRoute(prev, 'account-closure.step-two')) {
              this.segmentsArray.push({
                segmentName: prev,
                url: this.routingService.getPreviousUrl()
              });
            }

            if (this.isRoute(prev, 'bigCompetition.subtab') && this.isRoute(cur, 'eventMain')) {
              this.segmentsArray.pop();
              this.segmentsArray.push({
                segmentName: prev,
                url: this.routingService.getPreviousUrl()
              });
            }

            if (this.isRoute(prev, 'addToBetSlip') && this.isRoute(cur, 'betSlipUnavailable')) {
              this.segmentsArray.pop();
            }

            // Logic for event/:id page
            if (this.isRoute(prev, 'event.eventId')) {
              this.segmentsArray.pop();
            }

            // Business logic for 1-2-free && question-engine
            if (this.isRoute(prev, '1-2-free') || this.isRoute(prev, 'question-engine')) {
              this.segmentsArray = [];
            }

            // Check if currentUrl not the same with previous Url
            if (this.segmentsArray.length &&
              this.routingService.getCurrentUrl() === this.segmentsArray[this.segmentsArray.length - 1].url ) {
              this.segmentsArray.pop();
            }
          }
    });
  }

  /**
   * Return history of visited segments
   */
  getSegmentsArray(): { segmentName: string; url: string; }[] {
    return this.segmentsArray;
  }

  /**
   * Redirecting to previous or home page
   *
   * TODO roxanne-wallet merge conflicts resolving:
   * TODO this method&service should not include solution from vanilla! see BMA-49322
   * TODO remove this comment when resolved.
   */
  redirectToPreviousPage(): void {
    this.hiFromBackButton = true;
    this.window.nativeWindow.document.body.classList.remove('league-standings-opened');
    
    // redirect if we have gameBaseUrl or cbUrl
    if (this.storage.getCookie('gameBaseUrl')) {
      this.pubSubService.publish(this.pubSubService.API.REDIRECT);
      return;
    }

    const productRedirectUrl = this.getProductRedirectUrl();
    if (productRedirectUrl) {
      this.window.nativeWindow.location.href = productRedirectUrl;
      return;
    }

    const segmentsLength = this.segmentsArray.length;

    if (segmentsLength >= 1) {
      const lastSegment = this.segmentsArray[segmentsLength - 1],
      currentSegment = this.routingService.getCurrentSegment();
      // Get previous page
      if (this.window.nativeWindow.location.pathname.includes('/bet-filter/results')) {
        this.previousPage = '/bet-filter';
      } else {
        this.previousPage = lastSegment.url;
        this.segmentsArray.pop();
      }

      // Business logic
      if (currentSegment === 'tabs.cashout' ||
        currentSegment === 'tabs.openbets') {
        // Redirecting to page where you placed a bet
        this.router.navigateByUrl(this.storage.get('lastMadeBet') || this.previousPage);
      } else if (currentSegment === 'lobby' || currentSegment === 'contactUsConnect') {
        this.router.navigate(['/']);
      } else {
        // Redirecting to previous page
        this.router.navigateByUrl(this.previousPage);
      }
    } else {
      this.router.navigate(['/']);
    }
  }

  /**
   * Return true if loaded needed segment
   */
  private isRoute(state: string, segment: string): boolean {
    return state && state.indexOf(segment) !== -1;
  }

  private getProductRedirectUrl(): string {
    if (!this.routingService.getCurrentUrl().includes('/mobileportal')) {
      return '';
    }

    if (this.segmentsArray.some(item => item.url.includes('/mobileportal'))) {
      return '';
    }

    const product = this.storage.getCookie('lastKnownProduct');
    if (!product || !product['url']) {
      return '';
    }

    const productUrl = product['url'].toLowerCase();
    const currentUrl = this.window.nativeWindow.location.href.toLowerCase();
    return new URL(currentUrl).hostname !== new URL(productUrl).hostname ? productUrl : '';
  }
}
