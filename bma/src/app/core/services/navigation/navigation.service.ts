import { Injectable, NgZone } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, BehaviorSubject } from 'rxjs';
import { WindowRefService } from '@coreModule/services/windowRef/window-ref.service';
import { DeviceService } from '@coreModule/services/device/device.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { LocaleService } from '@coreModule/services/locale/locale.service';
import { UserService } from '@coreModule/services/user/user.service';
import { NativeBridgeService } from '@coreModule/services/nativeBridge/native-bridge.service';
import { GtmService } from '@coreModule/services/gtm/gtm.service';
import { CmsService } from '@coreModule/services/cms/cms.service';

import { ISystemConfig } from '@coreModule/services/cms/models';
import { NavigationUriService } from '@core/services/navigation/navigation-uri.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { ArcUserService } from '@app/lazy-modules/arcUser/service/arcUser.service';

@Injectable()
export class NavigationService {
  changeEmittedFromChild = new Observable<null>();
  emitChangeSource = new BehaviorSubject(null);
  arcAffectedUSer: boolean;

  constructor(
    private windowRefService: WindowRefService,
    private deviceService: DeviceService,
    private router: Router,
    private domToolsService: DomToolsService,
    private localeService: LocaleService,
    private userService: UserService,
    private nativeBridgeService: NativeBridgeService,
    private gtmService: GtmService,
    private ngZone: NgZone,
    private cmsService: CmsService,
    private pubSubService: PubSubService,
    private navigationUriService: NavigationUriService,
    private awsService: AWSFirehoseService,
    private routingStateService: RoutingState,
    private arcUserService: ArcUserService
  ) {
    this.changeEmittedFromChild = this.emitChangeSource.asObservable();
    this.windowRefService.nativeWindow.goToPage = (path: string) => {
      // HotFix: replace "event" in EDP URLs for racings
      path = path.replace('event/horse-racing', 'horse-racing')
        .replace('event/greyhound-racing', 'greyhound-racing');
      this.ngZone.run(() => {
        this.openUrl(path);
      });
    };
  }

  /**
   * Open given URL in router / current tab / new window
   *
   * The <undefined> value of inApp parameter behaves like <auto> :
   *  internal links open page without page reload
   *  external links open new page
   *
   * @param url
   * @param inApp {boolean | undefined}
   * @param restoreScroll - restore scroll position of previous route (bma-main and vanilla-core scrolls to top on nave end)
   */
  openUrl(url: string, inApp?: boolean, restoreScroll = false, menuItem?:any,header?: string): void {
    this.arcAffectedUSer = this.arcUserService.crossSellRemoval;
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      const gamingEnabled = config.GamingEnabled || {};
      const { enabledGamingOverlay, gamingUrl } = gamingEnabled;
      if (enabledGamingOverlay && url === gamingUrl) {
        if (this.deviceService.isWrapper) {
          this.nativeBridgeService.onGaming();
        } else if (this.userService.status && !this.arcAffectedUSer) {
          if (this.deviceService.isAndroid || (this.deviceService.isIos && this.deviceService.osVersion >= '13.0.0')) {
            this.pubSubService.publish(this.pubSubService.API.GAMING_OVERLAY_OPEN);
            if (this.router.url.includes('virtual-sports')) {
              this.router.navigate(['/']);
            }
            return;
          }
        }
      }
      if (this.isInternalUri(url)) {
        if (inApp || inApp === undefined) {
          const {offsetTop, fixedUrl} = this.getOffsetAndUrl(url);

          this.router.navigateByUrl(fixedUrl).then(() => {
            if (restoreScroll) {
              this.domToolsService.scrollPageTop(offsetTop);
            }
          });
        } else {
          // God knows why we need this, but legacy says that
          // navigating by "internal" non-inApp link should reload the app TODO check this!
          this.redirectCurrPage(url);
        }
      } else {
        if (inApp) {
          this.redirectCurrPage(url);
        } else {
          this.openNewPage(url);
        }
      }
    });
    if (menuItem && Object.keys(menuItem).length) { this.trackGTMEvent('a-z sports', menuItem.imageTitle, 'navigation', header === 'sb.azSports'? 'a-z betting' : 'featured'); }
  }

  /**
   * Open given Url in router
   * @param {string} url
   * @param {boolean} scroll
   * @returns {void}
   */
  openRouterUrl(url: string, scroll: boolean): void {
    const {offsetTop, fixedUrl} = this.getOffsetAndUrl(url);
    const navigation: Promise<boolean> = this.navigateByUrl(fixedUrl);
    this.postNavigation(navigation, offsetTop, scroll);
  }

  /**
   * Redirects current page with specified URL
   *
   * Old Android browsers correctly support only changing document.location directly (without href property),
   *  for the rest there is $window.location.href
   *
   * @param path
   * @param customWindow - window reference you want to change location (omit to use current)
   */
  redirectCurrPage(path: string, customWindow?: Window): void {
    const nativeWindow = customWindow || this.windowRefService.nativeWindow;

    if (this.deviceService.isAndroid) {
      nativeWindow.document.location = path;
    } else {
      nativeWindow.location.href = path;
    }
  }

  /**
   * Open new page/tab with given url
   *
   * @param url
   */
  openNewPage(url: string = ''): Window | null {
    const newWinRef = this.windowRefService.nativeWindow.open(url, '_blank');

    if (newWinRef && url) {
      newWinRef.focus();
    }

    return newWinRef;
  }

  /**
   * Asynchronous opening (workaround for browsers that block "popups"):
   *  open new page/tab with "loading" message,
   *  when (after async operation) url is created - load given url
   *
   * Call returned function with required url to load it in prepared window.
   */
  openNewPageAsync(): Function {
    const newWinRef = this.openNewPage();

    if (!newWinRef) {
      throw new Error(`Error opening new window for async navigation!`);
    }

    newWinRef.document.body.innerText = this.localeService.getString('bma.asyncOpeningMessage');

    return (href: string): void => {
      this.redirectCurrPage(href, newWinRef);
      newWinRef.focus();
    };
  }

  trackGTMEvent(eventAction: string, eventLabel: string, eventCategory: string = 'navigation', eventDetails: string ='a-z betting'): void {
    this.gtmService.push('trackEvent', { eventCategory, eventAction, eventLabel, eventDetails });
  }

  /**
   * Checks if given URI is internal (could be given to angular router)
   *
   * @param uri
   */
  isInternalUri(uri: string = ''): boolean {
    return this.navigationUriService.isInternalUri(uri);
  }

  /**
   * Checks if given URI is absolute (starts with http or https)
   *
   * @param uri
   */
  isAbsoluteUri(uri: string = ''): boolean {
    return this.navigationUriService.isAbsoluteUri(uri);
  }

  /**
   * Checks if given URI has same origin as current page
   *
   * @param uri
   */
  isSameOriginUri(uri: string = ''): boolean {
    return this.navigationUriService.isSameOriginUri(uri);
  }

  /**
   * Removes origin part of given URI if matches to current
   *
   * @param uri
   */
  removeCurrOrigin(uri: string = ''): string {
    return uri.replace(this.navigationUriService.origin, '');
  }

  /**
   * Tracks current not found page params and redirect to home page.
   * @param {string} location
   * @param {string} activeUrl
   */
  handleHomeRedirect(location: string = 'general', activeUrl?: string): void {
    const trackingData = {
      location,
      activeUrl: activeUrl ? activeUrl : this.router.url,
      previousUrl: this.routingStateService.getPreviousUrl()
    };

    this.gtmService.push('not-found-page', trackingData);
    this.awsService.addAction(this.awsService.API.NOT_FOUND_PAGE_HIT, trackingData);
    this.router.navigate(['/']);
  }

  /**
   * To get offset value, and fixedUrl
   * @param {string} url
   * @returns {offsetTop: number, fixedUrl: string}
   */
  private getOffsetAndUrl(url: string): {offsetTop: number, fixedUrl: string} {
    const offsetTop = this.domToolsService.getPageScrollTop();
    const fixedUrl = this.removeCurrOrigin(url);
    return {offsetTop, fixedUrl};
  }

  /**
   * Uses Router to navigate
   * @param {string} url
   * @returns {Promise<boolean>}
   */
  private navigateByUrl(url: string): Promise<boolean> {
    return this.router.navigateByUrl(url);
  }

  /**
   * steps to do on post navigation
   * @param {Promise<boolean>} navigation
   * @param {number} offsetTop
   * @param {boolean} hasScroll
   * @returns {void}
   */
  private postNavigation(navigation: Promise<boolean>, offsetTop: number, hasScroll: boolean): void {
    navigation.then(() => {
      if (hasScroll) {
        this.domToolsService.scrollPageTop(offsetTop);
      }
    });
  }
}
