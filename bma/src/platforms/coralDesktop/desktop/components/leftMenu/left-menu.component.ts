import { Component, OnInit, ChangeDetectionStrategy, ChangeDetectorRef, OnDestroy } from '@angular/core';
import { map } from 'rxjs/operators';

import { ISportCategory } from '@core/services/cms/models/sport-category.model';
import { LeftMenuService } from './left-menu.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { IDesktopQuickLink, ISystemConfig } from '@core/services/cms/models';
import { UserService } from '@core/services/user/user.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';

@Component({
  selector: 'left-menu',
  templateUrl: './left-menu.component.html',
  styleUrls: ['./left-menu.component.scss'],
  providers: [
    LeftMenuService
  ],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LeftMenuComponent implements OnInit, OnDestroy {
  
  menuItems: ISportCategory[];
  quickLinks: IDesktopQuickLink[];
  quickLinkHeader: boolean;
  favouriteItems: ISportCategory[] = [];
  favouriteIds: number[] = [];
  favLimit: number;
  favourites: number[] = [];
  selectedItemIndex = null;
  showFavourites: boolean = false;
  private readonly FAVOURITES: string = 'favouriteCheckbox';
  private readonly title: string = 'LeftMenuComponent';
  enabledCategories = [];

  constructor(
    public navigationService: NavigationService,
    private leftMenuService: LeftMenuService,
    private changeDetectorRef: ChangeDetectorRef,
    private cms: CmsService,
    public userService: UserService,
    private pubSubService: PubSubService,
    private bonusSuppressionService: BonusSuppressionService
  ) { }

  ngOnInit(): void {
    this.cms.getSystemConfig().subscribe((config: ISystemConfig) => {
      if (config && config.FavouriteCount) {
        this.favLimit = config.FavouriteCount.maxFavourites;
      }
    });
    this.leftMenuService.getMenuItems().pipe(
      map((items: ISportCategory[]) => items.map(item => 
      this.setTargetUriParts(item)))
    ).subscribe((menuItems: ISportCategory[]) => {
      this.menuItems = menuItems.map(menuItem =>{ //RSS
        if(menuItem.targetUri.includes('racingsuperseries')){
        this.pubSubService.subscribe(this.title, this.pubSubService.API.USER_CLOSURE_PLAY_BREAK,(val) =>{
          this.getFavourites();
          if(val){ menuItem.targetUri = '/promotions/details/exclusion';}
        return menuItem; //RSS
      }  );
     }  return menuItem;})
      this.filterLeftMenuBasedOnRgyellow();
      this.changeDetectorRef.markForCheck();
    });
    this.cms.getDesktopQuickLinks()
      .subscribe((quickLinks: IDesktopQuickLink[]) => {
        this.quickLinks = quickLinks.filter((quickLinkItem: IDesktopQuickLink) => {
          if (quickLinkItem && quickLinkItem.isAtoZQuickLink) {
            quickLinkItem.target = `/${quickLinkItem.target.replace(/^\/+/, '')}`;
            return quickLinkItem;
          }
        });
        this.filterQuickLinksBasedOnRgyellow();
        this.quickLinkHeader = this.quickLinks.some((quickLinkItem: IDesktopQuickLink) => quickLinkItem.isAtoZQuickLink);
        this.changeDetectorRef.markForCheck();
      });
    this.pubSubService.subscribe(this.title,
      [this.pubSubService.API.SESSION_LOGIN, this.pubSubService.API.SESSION_LOGOUT], () => {
        this.cms.getCMSRGYconfigData().subscribe(() => {
          this.filterLeftMenuBasedOnRgyellow();
          this.filterQuickLinksBasedOnRgyellow();
          this.changeDetectorRef.detectChanges();
        });
    });
  }

  /**
   * Get favourites based on the favourite count
   */
  getFavourites(): void {
    if (this.favLimit > 0 && this.userService.bppToken) {
      this.leftMenuService.getFavouriteItems(this.userService.bppToken).subscribe(
        (favourites: number[]) => {
          this.favourites = favourites;
          this.favouriteIds = this.favourites.slice(0, this.favLimit);
          this.updateFavouriteItems();
        });
    }
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @param {ISportCategory} menuItem
   * @return {number}
   */
  trackById(index: number, menuItem: ISportCategory): string {
    return menuItem.id;
  }

  /**
   * extends category object with targetUriParts property
   * @param category {ISportCategory} sport category for modify
   * @return {ISportCategory} sport category with targetUriParts
   */
  private setTargetUriParts(category: ISportCategory): ISportCategory {
    return {
      ...category,
      targetUriParts: [
        '/',
        ...category.targetUri.split('/').filter(param => param)
      ]
    };
  }

  /**
   * Create and update operation on favourites
   * @param {Event} event
   * @param {ISportCategory} item
   */
  setFavourite(event: Event, item: ISportCategory): void {
    let payload = {};
    if (!((event.target as HTMLInputElement).checked) && this.favouriteItems.length > 0) {
      let favItemIndex = this.favourites.indexOf(+item.categoryId);
      this.favourites.splice(favItemIndex, 1);
      this.enabledCategories = this.menuItems.filter((menuItem: ISportCategory) => this.favourites.includes(+menuItem.categoryId));
      payload = { categories: this.enabledCategories.map((favItem: ISportCategory) => favItem.categoryId) };

      this.leftMenuService.storeFavouriteItems(this.userService.bppToken, payload).subscribe(
        (favourites: number[]) => {
          this.favourites = favourites;
          favItemIndex = this.favouriteIds.indexOf(+item.categoryId);
          this.favouriteIds.splice(favItemIndex, 1);
          this.updateFavouriteItems();
        });
    } else {
      this.enabledCategories = this.menuItems.filter((menuItem: ISportCategory) => this.favourites.includes(+menuItem.categoryId));
      payload = { categories: [...this.enabledCategories.map((favItem: ISportCategory) => favItem.categoryId), item.categoryId] };
      this.leftMenuService.storeFavouriteItems(this.userService.bppToken, payload).subscribe(
        (favourites: number[]) => {
          this.favourites = favourites;
          this.favouriteIds.push(+item.categoryId);
          this.updateFavouriteItems();
        });
    }
  }

  /**
   * display favourites based on the category ID selection
   */
  updateFavouriteItems(): void {
    this.favouriteItems = this.menuItems.filter((menuItem: ISportCategory) => this.favouriteIds.includes(+menuItem.categoryId));
    this.favouriteIds = this.favouriteItems.map((favItem: ISportCategory) => favItem.categoryId);
    this.showFavourites = this.userService.status && this.favouriteItems.length > 0;
    this.changeDetectorRef.markForCheck();
  }

  /**
   * Add/update the favourites and navigate to URL on item click
   * @param {Event} event
   * @param {ISportCategory} item
   */
  openUrl(event: Event, item: ISportCategory): void {
    if ((event.target as HTMLElement).dataset.crlat === this.FAVOURITES && this.favLimit > 0) {
      this.setFavourite(event, item);
    } else {
      this.navigationService.openUrl(item.targetUri, item.inApp);
    }
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.title);
  }

  /**
   * Filters all the menu items based on user bonus suppresion
   */
  filterLeftMenuBasedOnRgyellow(): void {
    const mItems = [...this.menuItems];
    this.menuItems = [];
    this.menuItems = mItems.filter((menuItem: ISportCategory) => {
      return this.bonusSuppressionService.checkIfYellowFlagDisabled(menuItem.imageTitle)
    });
  }

  /**
   * Filters all the Quick Link based on user bonus suppresion
   */
  filterQuickLinksBasedOnRgyellow(): void {
    const qLinks = [...this.quickLinks];
    this.quickLinks = [];
    this.quickLinks = qLinks.filter((linkItem: IDesktopQuickLink) => {
      return this.bonusSuppressionService.checkIfYellowFlagDisabled(linkItem.title)
    });
  }
}
