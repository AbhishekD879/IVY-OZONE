import { forkJoin as observableForkJoin, Observable, BehaviorSubject, of } from 'rxjs';
import { Injectable } from '@angular/core';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { UserService } from '@core/services/user/user.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IRetailMenu, IVerticalMenu, IMenuActionResult } from '@core/services/cms/models';
import { BetFilterParamsService } from '../betFilterParams/bet-filter-params.service';
import { IRetailConfig } from '@core/services/cms/models/system-config';
import { Router, Routes, Route } from '@angular/router';

@Injectable()
export class RetailMenuService {
  public retailMenuItems: BehaviorSubject<IVerticalMenu[]> = new BehaviorSubject<IVerticalMenu[]>([]);
  public retailMenuItems$: Observable<IVerticalMenu[]> = this.retailMenuItems.asObservable();

  constructor(
    private cmsService: CmsService,
    private userService: UserService,
    private pubSubService: PubSubService,
    private betFilterParamsService: BetFilterParamsService,
    protected router: Router
  ) {
    this.createRetailMenuItems();
  }

  subscribe(): void {
    this.pubSubService.subscribe('userLoginOnConnectMenu',
      [this.pubSubService.API.SUCCESSFUL_LOGIN, this.pubSubService.API.SESSION_LOGOUT], () => {
        this.updateRetailMenuItems();
      });
  }

  getRouterConfig(): Routes {
    return this.router.config.find((routeConfig: Route) => routeConfig.path === '').children;
  }

  private createRetailMenuItems() {
    observableForkJoin([
      this.cmsService.getSystemConfig(),
      this.cmsService.getRetailMenu()
    ]).subscribe(([systemConfig, connectItems]) => {
      if (systemConfig.Connect && systemConfig.Connect.menu) {
        const newConnectItems = connectItems.map((item: IRetailMenu) => {
          const menuItem: Partial<IRetailMenu & IVerticalMenu> = item;
          menuItem.title = menuItem.linkTitle;
          menuItem.subtitle = menuItem.linkSubtitle;
          menuItem.hidden = !this.isMenuItemAvailable(menuItem.targetUri, systemConfig.Connect);
          menuItem.targetUri = this.redirectInShopUser(menuItem.targetUri);

          // TODO Remove when new router is implemented.
          this.assignMenuAction(menuItem);

          return menuItem as IVerticalMenu;
        });
        this.retailMenuItems.next(newConnectItems);
      }
    });
  }

  private updateRetailMenuItems() {
    this.cmsService.getSystemConfig().subscribe(systemConfig => {
      const currentMenuItems = this.retailMenuItems.value;
      this.retailMenuItems.next(currentMenuItems.map(item => ({
        ...item,
        hidden: !this.isMenuItemAvailable(item.targetUri, systemConfig.Connect),
        targetUri: this.redirectInShopUser(item.targetUri)
      })));
    });
  }

  private redirectInShopUser(targetUri: string): string {
    return !!this.userService.getRetailCard() && targetUri.includes('upgrade') ? '/retail-registration' : targetUri;
  }

  private isMenuItemAvailable(uri: string, config: IRetailConfig): boolean {
    const sanitizedUrl = uri.replace(/^\/+/g, '').replace(/\/+$/, '');
    if (uri.includes('upgrade') || uri.includes('registration')) {
      return this.userService.isInShopUser() && config.upgrade;
    } else {
      const uriRoute = this.getRouterConfig().find(routeConfig => {
        if (routeConfig.data && routeConfig.data.path) {
          return sanitizedUrl === routeConfig.data.path;
        } else if (routeConfig.path) {
          return sanitizedUrl === routeConfig.path;
        } else {
          return false;
        }
      });
      return uriRoute && uriRoute.data && uriRoute.data.feature ? config[uriRoute.data.feature] : false;
    }
  }

  private assignMenuAction(menuItem: Partial<IRetailMenu & IVerticalMenu>): Partial<IRetailMenu & IVerticalMenu> {
    if (menuItem.targetUri.includes('bet-filter')) {
      menuItem.action = this.betFilterMenuItemAction.bind(this);
    } else if (menuItem.upgradePopup) {
      menuItem.action = this.commonMenuItemAction.bind(this);
    }

    return menuItem;
  }

  private betFilterMenuItemAction(): Observable<IMenuActionResult> {
    return this.betFilterParamsService.chooseMode();
  }

  private commonMenuItemAction(): Observable<IMenuActionResult> {
    return of({ cancelled: false });
  }
}
