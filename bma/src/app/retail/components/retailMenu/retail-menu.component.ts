import { Component, Input, OnInit, OnDestroy, EventEmitter, Output } from '@angular/core';
import { IVerticalMenu } from '@core/services/cms/models';
import { GtmService } from '@core/services/gtm/gtm.service';
import { UserService } from '@core/services/user/user.service';
import { RetailMenuService } from '@retailModule/services/retailMenu/retail-menu.service';
import { Subscription } from 'rxjs';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { GRID_GA_TRACKING } from '@app/retail/constants/retail.constant';

@Component({
  selector: 'retail-menu',
  templateUrl: 'retail-menu.component.html'
})

export class RetailMenuComponent implements OnInit, OnDestroy {
  @Input() showHeader: boolean = false;
  @Input() showRetailHeader: boolean;
  @Input() showDescription: boolean = false;
  @Input() showCardNumber: boolean = false;
  @Input() trackingLocation: string;
  @Input() disableDefaultNavigation: boolean;
  @Output() readonly itemClick: EventEmitter<IVerticalMenu> = new EventEmitter<IVerticalMenu>();
  @Output() readonly showFootballBetFilterConfirmDialog: EventEmitter<boolean> = new EventEmitter();
  readonly BET_FILTER_URL: string = '/bet-filter';
  public menuItems: IVerticalMenu[] = [];
  public cardMenuItem: Partial<IVerticalMenu>;
  showTopBorder: boolean = false;
  private subscription: Subscription;

  constructor(
    private gtmService: GtmService,
    private userService: UserService,
    private retailMenuService: RetailMenuService,
    private navigationService: NavigationService,
  ) { }

  ngOnInit(): void {
    this.subscription = this.retailMenuService.retailMenuItems$.subscribe(data => {
      this.menuItems = data;
      this.showTopBorder = !this.menuItems.length;
      if (this.showCardNumber && !!this.userService.cardNumber && this.userService.isInShopUser()) {
        this.cardMenuItem = {
          title: this.userService.cardNumber,
          svgId: '#retail-card',
        };
      } else {
        this.cardMenuItem = null;
      }
    });
    GRID_GA_TRACKING.eventAction = this.trackingLocation;
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

  /** Track menu item clicks in GA.
   * @param  {IVerticalMenu} menuItem
   * @returns void
   */
  trackNavigation(menuItem: IVerticalMenu): void {
    GRID_GA_TRACKING.eventCategory = 'navigation';
    GRID_GA_TRACKING.eventLabel = menuItem.linkTitle;
    this.gtmService.push('trackEvent', GRID_GA_TRACKING);
    this.itemClick.emit(menuItem);
  }

  /** Track menu item clicks in GA.
   * @param  {IVerticalMenu} menuItem
   * @returns void
   */
  trackGridNavigation(menuItem: IVerticalMenu): void {
    GRID_GA_TRACKING.eventLabel = menuItem.linkTitle;
    GRID_GA_TRACKING.eventCategory = 'Grid';
    GRID_GA_TRACKING.eventAction = 'Menu';
    this.gtmService.push('trackEvent', GRID_GA_TRACKING);
    this.gtmService.shopLocatorTrack = true;
    if(menuItem.targetUri === this.BET_FILTER_URL) {
      this.showFootballBetFilterConfirmDialog.emit(true);
    } else {
      this.navigationService.openUrl(menuItem.targetUri, menuItem.inApp);
    }
  }
}
