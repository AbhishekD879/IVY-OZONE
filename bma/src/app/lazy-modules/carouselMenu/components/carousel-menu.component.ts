import {
  AfterViewInit,
  Component,
  ElementRef,
  Input,
  NgZone,
  OnDestroy,
  OnInit,
  HostBinding,
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  SimpleChanges,
  ViewEncapsulation
} from '@angular/core';
import { Subscription } from 'rxjs';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { ISportCategory } from '@core/services/cms/models/sport-category.model';
import { ServingService } from '@core/services/serving/serving.service';
import { CasinoLinkService } from '@core/services/casinoLink/casino-link.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { EVENT_NAME, MENU_ICONS_STATE } from './carousel-menu.constant';
import { GtmService } from '@core/services/gtm/gtm.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { CarouselMenuStateService } from '@app/core/services/carouselMenuState/carousel-menu-state.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { IGATrackingModel } from '@app/core/models/gtm.event.model';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';

@Component({
  selector: 'carousel-menu',
  styleUrls: ['./carousel-menu.component.scss'],
  templateUrl: 'carousel-menu.component.html',
  encapsulation: ViewEncapsulation.None,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CarouselMenuComponent implements OnInit, OnDestroy, AfterViewInit {
  @Input() menuItems: ISportCategory[];
  @Input() activeMenuItem: string;
  @Input() isSticky: boolean;
  @Input() isLiveCounter: boolean;
  @Input() isTopScroll: boolean = false;
  @Input() GATrackingModule?: string;
  @Input() GTMTrackingObj?: IGATrackingModel;
  @Input() carouselClass?: string;
  @Input() carouselId? : string;
  @HostBinding('class.menu-hide') isHidden: boolean = false;

  isAvailable: boolean;

  public document: HTMLDocument;
  private lastScrollPosition: number = 0;
  private eventName: string;
  private eventNameConst: { live: string, upcoming: string } = EVENT_NAME;
  private scrollListener: Function;
  private forceVisibility: boolean;
  private carouselStickSubscription: Subscription;
  private title: string = 'casousel-menu';
  private isScrollEnabled: boolean = false;

  constructor(
    public windowRef: WindowRefService,
    private rendererService: RendererService,
    private serving: ServingService,
    private casinoLink: CasinoLinkService,
    private pubsub: PubSubService,
    private gtm: GtmService,
    private navigationService: NavigationService,
    private carouselMenuStateService: CarouselMenuStateService,
    private zone: NgZone,
    private elementRef: ElementRef,
    private changeDetectorRef: ChangeDetectorRef,
    public domTools: DomToolsService,
    private bonusSuppressionService: BonusSuppressionService
  ) {
    this.document = this.windowRef.document;
  }

  ngAfterViewInit(): void {
    // Set Sticky Menu on Scroll
    if (this.isSticky) {
      this.lastScrollPosition = 0;
      this.scrollListener = this.rendererService.renderer.listen(this.document, 'scroll', () => {
        if (this.elementRef && !this.forceVisibility) {
          this.setSticky();
        }
      });
    }
  }

  ngOnInit(): void {
    // Menu Items
    this.menuItems = (this.casinoLink.decorateCasinoLink(this.menuItems)).filter((item) => {
      item.targetUri = item.targetUri && (item.targetUri.startsWith('/') || this.navigationService.isAbsoluteUri(item.targetUri))
        ? item.targetUri : `/${item.targetUri}`;

      return !item.disabled && !item.hidden && this.bonusSuppressionService.checkIfYellowFlagDisabled(item.imageTitle);
    });
    this.isAvailable = !!(this.menuItems && this.menuItems.length);

    // InPlay Live Events Counter
    if (this.isLiveCounter) {
      this.pubsub.subscribe('CarouselMenu', this.pubsub.API.EVENT_COUNT, eventName => {
        this.eventName = eventName;
        this.changeDetectorRef.markForCheck();
      });
    }
    this.zone.runOutsideAngular(() => {
      this.carouselStickSubscription = this.carouselMenuStateService.carouselStick$
        .subscribe((data: { stick: boolean, forceVisibility: boolean }) => {
          this.isHidden = data.stick;
          this.forceVisibility = data.forceVisibility;
        });
    });
    this.pubsub.subscribe('CarouselMenu',
      [this.pubsub.API.SESSION_LOGIN, this.pubsub.API.SESSION_LOGOUT], () => {
          this.filterCarouselBasedOnRgyellow();
          this.changeDetectorRef.detectChanges();
      });
  }

   ngOnChanges(changes: SimpleChanges) {
      if(changes.menuItems) {
        this.menuItems = this.menuItems.filter(item => {
          return this.bonusSuppressionService.checkIfYellowFlagDisabled(item.imageTitle);
        })
      }
      if(changes.activeMenuItem){
        this.changeDetectorRef.markForCheck();  
        }
      this.isAvailable = !!(this.menuItems && this.menuItems.length);
      this.changeDetectorRef.detectChanges();
     }

  ngOnDestroy(): void {
    if (this.scrollListener) {
      this.scrollListener();
    }
    this.pubsub.unsubscribe('CarouselMenu');
    this.forceVisibility = false;
    this.carouselStickSubscription.unsubscribe();
  }

  /**
   * to add class for icon at pressed state
   * @param item 
   */
  iconPressedState(item){
    this.isScrollEnabled = false;
    this.addClass(item.targetUri, MENU_ICONS_STATE.ICON_PRESSED_STATE);
    this.addClass(item.imageTitle, MENU_ICONS_STATE.ICON_PRESSED);
    this.removeClass(item.imageTitle, MENU_ICONS_STATE.ICON_DEFAULT);
  }

   /**
   * triggers on menu items scroll
   * @private 
   */
  menuScrolled() {
    this.isScrollEnabled = true;
  }

  /**
   * to add class for icon at default state
   * @param item 
   */
  iconDefaultState($event, item, itemIndex) {
    this.addClass(item.targetUri, MENU_ICONS_STATE.ICON_DEFAULT_STATE);
    this.addClass(item.imageTitle, MENU_ICONS_STATE.ICON_DEFAULT);
    this.removeClass(item.imageTitle, MENU_ICONS_STATE.ICON_PRESSED);
    if(!this.isScrollEnabled) {
      this.buttonAction($event, item, itemIndex + 1);
    }
  }
/**
 * add class by id for svg icon at pressed state
 * @param item 
 * @param event 
 */
  addClass(item: string, event: string) {
    this.windowRef.document.getElementById(item).classList.add(event);
  }

  /**
   * remove class by id for svg icon at default state
   * @param item 
   * @param event 
   */
  removeClass(item: string, event: string) {
    this.windowRef.document.getElementById(item).classList.remove(event);
  }
  
  /**
   * Show Event Counter
   * @param event
   * @returns {*}
   */
  eventCount(event: { liveEventCount: number; upcomingEventCount: number }): number {
    // using default name if event 'EVENT_COUNT' is triggered before subscription
    const eventName: string = this.eventName || this.eventNameConst.live;
    const isLive: number = eventName.includes(this.eventNameConst.live) && event.liveEventCount;
    const isUpcoming: number = eventName.includes(this.eventNameConst.upcoming) && event.upcomingEventCount;
    if (isLive) {
      return event.liveEventCount;
    } else if (isUpcoming) {
      return event.upcomingEventCount;
    }
    return 0;
  }

  /**
   * Send cookies if link is external
   * @param {MouseEvent} $event
   * @param {ISportCategory} item
   */
  buttonAction($event: MouseEvent, item: ISportCategory, itemIndex:number): void {
    $event && $event.preventDefault();

    this.navigationService.openUrl(item.targetUri, item.inApp, this.isTopScroll);

    this.navigationTracking(item.imageTitle, itemIndex);
    this.serving.sendExternalCookies(item.relUri);
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @return {number}
   */
  trackByFn(index: number): number {
    return index;
  }

  /**
   * Vanilla Mobile Carousel menu must have 'position: relative' initially. When Smart-Banner is shown,
   * the sticky Vanilla Header can be scrolled up, so the menu should follow it, until reaches the top.
   * This will toggle the 'position: fixed' with strictly defined alignment, so menu stays fixed to header.
   * If smart banner is closed, relatively positioned menu without top property will keep proper place.
   */
  protected setSticky(): void {
    const element = this.elementRef.nativeElement,
      height: number = element.offsetHeight,
      offsetTop: number = element.offsetTop,
      scrollPosition: number = this.windowRef.nativeWindow.pageYOffset ||
        this.windowRef.document.documentElement.scrollTop ||
        this.windowRef.document.body.scrollTop || 0;

    this.isHidden = scrollPosition > this.lastScrollPosition && (this.isHidden ? offsetTop > 0 : offsetTop > height);
    this.lastScrollPosition = scrollPosition;
  }

  /**
   * Tracking - Navigation of sports carousel
   * @param {string} menuItem (Example - Horse Racing)
   */
  private navigationTracking(menuItem: string, position:number): void {
    this.gtm.push('trackEvent', {
      eventCategory: 'navigation',
      eventAction: 'main',
      eventLabel: menuItem,
      position: position
    });
  }

  /**
   * Filter set correct links
   * @private
   */
  filterCarouselBasedOnRgyellow(): void {
    this.menuItems = this.menuItems.filter((link: ISportCategory) => {
      return this.bonusSuppressionService.checkIfYellowFlagDisabled(link.imageTitle);
    })
  }
}
