import { pairwise, filter } from 'rxjs/operators';
import { Component, ElementRef, OnInit, OnDestroy, Input, HostListener } from '@angular/core';
import { Router, Event, NavigationEnd, ActivatedRoute } from '@angular/router';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { Subscription } from 'rxjs';
import { Location } from '@angular/common';
import * as _ from 'underscore';

import { CmsService } from '@coreModule/services/cms/cms.service';
import { DeviceService } from '@core/services/device/device.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { UserService } from '@core/services/user/user.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';

@Component({
  selector: 'sidebar',
  templateUrl: 'sidebar.component.html'
})
export class SidebarComponent implements OnInit, OnDestroy {
  @Input() sideClass: string;
  @Input() sideHideClose?: string;
  @Input() sidePosition?: string;
  @Input() sideId?: string;
  @Input() sideWidth?: number;

  classList: string;
  sidebarShown: boolean;
  private element: HTMLElement;
  private resizeListerner: Function;
  private orientationChangeListerner: Function;
  private windowScrollY: number;
  private document: HTMLDocument;
  private routeChangeListener: Subscription;
  private tagName: string = 'sidebar';

  private static getEdpUrl(url: string): string {
    return url.split('/').splice(0, 6).join('/');
  }

  constructor(
    private device: DeviceService,
    private cms: CmsService,
    private nativeBridgeService: NativeBridgeService,
    private windowRef: WindowRefService,
    private rendererService: RendererService,
    private domTools: DomToolsService,
    private elementRef: ElementRef,
    private user: UserService,
    private location: Location,
    private router: Router,
    private pubSubService: PubSubService,
    private route: ActivatedRoute,
    private routingState: RoutingState,
    private sessionStorage: SessionStorageService
  ) {
    this.element = this.elementRef.nativeElement;
    this.document = this.windowRef.nativeWindow.document;

    this.showSidebar = this.showSidebar.bind(this);
    this.resizeSidebar = this.resizeSidebar.bind(this);
  }

  ngOnInit(): void {
    this.tagName = this.sideClass ? `sidebar-${this.sideClass}` : this.tagName;
    this.resizeListerner = this.rendererService.renderer.listen(this.windowRef.nativeWindow,
      'resize', this.resizeSidebar);

    this.orientationChangeListerner = this.rendererService.renderer.listen(this.windowRef.nativeWindow,
      'orientationchange', this.resizeSidebar);

    this.pubSubService.subscribe(this.tagName, `show-${this.sideClass}`,
      data => {
        this.showSidebar(!!data);
      });
    this.classList = this.formClassList();
    this.routeChangeListener = this.router.events.pipe(
      filter((event: Event) => event instanceof NavigationEnd),
      pairwise()) // TODO Remove pairwise() function after remove "onSameUrlNavigation: 'reload'" from app-routing.module
      .subscribe((navigationEvents: Event[]) => {
        const prevPage = <NavigationEnd>navigationEvents[0];
        const currentPage = <NavigationEnd>navigationEvents[1];
        const market = this.routingState.getRouteParam('market', this.route.snapshot);
        const marketType = this.routingState.getRouteParam('marketType', this.route.snapshot);
        const currentPageUrl = this.getCurrentPage(currentPage.urlAfterRedirects);

        if (prevPage.urlAfterRedirects === currentPageUrl ||
            `${prevPage.urlAfterRedirects}/${market}` === currentPageUrl ||
            `${prevPage.urlAfterRedirects}/${market}/${marketType}` === currentPageUrl ||
            this.isSameRacingUrl(prevPage.urlAfterRedirects, currentPageUrl)) {
          return;
        }

        // TODO Remove navigationEvents after remove "onSameUrlNavigation: 'reload'" from app-routing.module
        this.handleRouteChange(prevPage);
      });
  }

  ngOnDestroy(): void {
    if (this.routeChangeListener) {
      this.routeChangeListener.unsubscribe();
    }

    if (this.resizeListerner) {
      this.resizeListerner();
    }

    if (this.orientationChangeListerner) {
      this.orientationChangeListerner();
    }

    this.showSidebar(false, false);
    this.pubSubService.unsubscribe(this.tagName);
  }

  @HostListener('document:keyup', ['$event.keyCode'])
  onKeyDown(keyCode: number): void {
    if (keyCode === 27) {
      this.hideSidebar();
    }
  }

  /**
   * Close sidebar by clicking on CloseButton or Overlay
   * @param {MouseEvent} event
   */
  handleOuterClick(event: MouseEvent): void {
    const target: HTMLElement = event.target as HTMLElement;
    if (target.classList.contains("sidebar-close") && this.sessionStorage.get('betPlaced')) {
      const currentType = this.sessionStorage.get('cashOutAvail') ? 'cashOut' : 'defaultContent';
      this.pubSubService.publish(this.pubSubService.API.FIRST_BET_PLACEMENT_TUTORIAL,
        { step: 'betDetails', tutorialEnabled: true, type: currentType });
    }
    if (target.classList.contains('sidebar') || target.classList.contains('sidebar-close')) {
      this.showSidebar(false);
    }
  }

  /**
   * To fetch current page details
   * @param {string} urlAfterRedirects
   * @returns {string}
   */
  private getCurrentPage(urlAfterRedirects: string): string {
    const currentUrlData = urlAfterRedirects.split('?');
    return currentUrlData[0];
  }

  /**
   * Add Class to Sidebar
   * @returns {{is-visible: (boolean|*), sidebar-android: *}}
   */
  private formClassList(): string {
    // Left or Right Sidebar Class
    const position = this.sidePosition ? `${this.sidePosition}-side` : 'right-side';

    return `${this.device.isNativeAndroid ? 'sidebar-android' : ''} ${position} ${this.sideClass}`;
  }

  /**
   * Hide Sidebar
   * @param {boolean} hasRouteChanged
   */
  private hideSidebar(hasRouteChanged: boolean = false): void {
    if (this.sidebarShown) {
      this.showSidebar(false, hasRouteChanged);
    }
  }

  /**
   * Show/Close Sidebar
   * @param {boolean} showSide (true/false)
   * @param {boolean|undefined} hasRouteChanged
   */
  private showSidebar(showSide: boolean, hasRouteChanged: boolean = false): void {
    const isWrapper = this.device.isWrapper,
      isBetSlip = this.sideClass === 'slide-out-betslip';

    // required for native wrapper in cases when we close sidebar
    // and should open native homepage
    if (isBetSlip && !showSide && isWrapper) {
      // trigger on close Slide Out BetSlip
      this.nativeBridgeService.onCloseBetSlip();

      this.updateSidebarState(showSide, true, isBetSlip, hasRouteChanged);
    } else {
      // make additional request just when opening betslip
      if (showSide && isBetSlip) {
        // trigger on open Slide Out BetSlip for nativeApp
        if (isWrapper) {
          this.nativeBridgeService.onOpenBetSlip();
        }
        this.cms.triggerSystemConfigUpdate();
        this.windowScrollY = this.windowRef.nativeWindow.pageYOffset;
      }

      this.updateSidebarState(showSide, false, isBetSlip, hasRouteChanged);
    }
  }

  /**
   * Update Sidebar Width on Resize
   */
  private resizeSidebar(): void {
    if (this.sidebarShown && !this.sideWidth) {
      this.updateSidebarWidth();
    }
  }

  /**
   * Updates state of the sidebar
   * @param showSide {boolean}
   * @param shouldPreventMethodCall {boolean|undefined}
   * @param isBetSlip {boolean}
   * @param {boolean|undefined} hasRouteChanged
   */
  private updateSidebarState(showSide: boolean, shouldPreventMethodCall: boolean, isBetSlip: boolean, hasRouteChanged: boolean): void {
    // Animation time the same as $animation-time in sidebar.scss
    const animationTime = 220;

    this.sidebarShown = showSide;
    this.domTools.toggleClass(this.element.children[0], 'is-visible', showSide);
    this.domTools.toggleClass(this.document.body, `${this.sideClass}-open`, showSide);
    this.domTools.toggleClass(this.document.documentElement, `${this.sideClass}-open`, showSide);
    this.updateSidebarWidth();

    // trigger on right menu click on wrappers
    if (showSide) {
      this.nativeBridgeService.onRightMenuClick();
    } else if (this.device.isMobile) {
      // return back to default betslip mode when close side bar
      this.pubSubService.publish(this.pubSubService.API.HOME_BETSLIP);
    }

    this.windowRef.nativeWindow.setTimeout(() => {
      // Callback Close/Open
      // Remove focus from from active element to fix bug
      // when focus remains on stakeBox and browser back button was pressed
      if (!showSide) {
        const activeElement = this.document.activeElement as HTMLElement;

        if (activeElement) {
          activeElement.blur();
        }
      }
      this.pubSubService.publish(`show-${this.sideClass}-${showSide}`, shouldPreventMethodCall ? 'prevent' : '');
    }, animationTime, false);

    if (!showSide && isBetSlip && !hasRouteChanged) {
      this.document.documentElement.scrollTop = this.windowScrollY; // For Chrome, Firefox, IE and Opera
      this.document.body.scrollTop = this.windowScrollY; // For Safari
    }
  }

  /**
   * Update Sidebar Width
   */
  private updateSidebarWidth(): void {
    const fixedFooter: NodeList = this.element.querySelectorAll('.bs-footer-anchoring');
    const elmSideContent: Element = this.element.querySelector('aside').children[0];
    const closeWidth: number = this.sideHideClose ? 0 : 50;
    const elmWidth: number = this.sideWidth || (this.windowRef.nativeWindow.innerWidth - closeWidth);

    this.domTools.css(elmSideContent, { width: elmWidth });
    _.each(fixedFooter, (element: Element) => {
      this.domTools.css(element, { width: elmWidth });
    });
  }

  private handleRouteChange(prevPage: NavigationEnd): void {
    // Fix of https://jira.egalacoral.com/browse/BMA-53111
    const isPrivateMarketsTab = prevPage.url === '/home/private-markets';
    // Fix of https://jira.egalacoral.com/browse/BMA-47390
    const isBetFilter = this.location.path().includes('/bet-filter/results/');

    if (this.sidebarShown && !this.user.loginPending && !isPrivateMarketsTab && !isBetFilter) {
      this.hideSidebar(true);
    }
  }

  private isSameRacingUrl(previousUrl: string, currentUrl: string): boolean {
    return SidebarComponent.getEdpUrl(previousUrl) === SidebarComponent.getEdpUrl(currentUrl);
  }
}
