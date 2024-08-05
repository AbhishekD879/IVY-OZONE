import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { Router, Event, NavigationEnd, ActivatedRoute, Params } from '@angular/router';
import { Subscription } from 'rxjs';
import { FiltersService } from '@core/services/filters/filters.service';
import { LocalStorageMapperService } from '@app/vsbr/services/local-storage-mapper.service';
import { VirtualSportsService } from '@app/vsbr/services/virtual-sports.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { VIRTUAL_ROUTE_NAME, SPORTS_ROUTE_NAME } from '@app/vsbr/constants/virtual-sports.constant';
import { IVirtualSportsEventsData } from '../../models/virtuals-ss-respose.model';
import { IVirtualSportsMenuItem, IVirtualSportsMenuItemLabel } from './../../models/menu-item.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { VirtualMenuDataService } from '@app/vsbr/services/virtual-menu-data.service';
import { IVirtualCategoryStructure, IVirtualChildCategory } from '@app/vsbr/models/virtual-sports-structure.model';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { SPRITE_PATH } from '@bma/constants/image-manager.constant';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { ISystemConfig } from '@app/core/services/cms/models';
import { VirtualHubService } from "@app/vsbr/services/virtual-hub.service";

@Component({
  selector: 'virtual-sports-page',
  templateUrl: './virtual-sports-page.component.html'
})
export class VirtualSportsPageComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  eventsData: IVirtualSportsEventsData;
  categories: IVirtualCategoryStructure[];
  titleTranslation: string = 'vsbr.virtualSports';
  parentMenuItems: IVirtualSportsMenuItem[];
  activeParent: number;
  activeChild: number;
  currentTime: number;
  virtualIcons: string;
  isVirtualHomeDisabled: boolean = false;

  private MENU_TIMER_CLASS_NAME: string = 'vc-timer';
  private MENU_LIVE_CLASS_NAME: string = 'vс-live';

  private routeChangeSuccessHandler: Subscription;
  private virtualSportsEventsSubscription: Subscription;
  private timerSubscription: Subscription;
  private eventsDataSub: Subscription;

  constructor(
    private pubsub: PubSubService,
    private filterService: FiltersService,
    private localStorageMapperService: LocalStorageMapperService,
    private virtualSportsService: VirtualSportsService,
    private router: Router,
    private route: ActivatedRoute,
    private virtualMenuDataService: VirtualMenuDataService,
    private navigationService: NavigationService,
    private asyncScriptLoaderService: AsyncScriptLoaderService,
    private cmsService: CmsService,
    private changeDetectorRef: ChangeDetectorRef,
    private virtualHubService: VirtualHubService
  ) {
    super()/* istanbul ignore next */;
    this.loadVirtualIcons();
  }

  ngOnInit(): void {
    this.showSpinner();

    this.eventsDataSub = this.virtualSportsService.eventsData().subscribe((categories: IVirtualCategoryStructure[]): void => {
      if (!categories || !categories.length) {
        this.showError();
        return;
      }

      categories.forEach((parentCategory: IVirtualCategoryStructure) => {
        if (!parentCategory.childs || !parentCategory.childs.size) {
          return;
        }

        parentCategory.childs.forEach((child: IVirtualChildCategory) => {
          if (!child.timeLeft) {
            parentCategory.childs.delete(child.classId);
          }
        });
      });

      this.categories = categories.filter((category: IVirtualCategoryStructure) => {
        return  category.childs && category.childs.size;
      });

      this.createTopSportMenu(this.categories);
      this.virtualHomepageCheck();
      this.addListeners();
      this.updateActiveTab();
      this.localStorageMapperService.init();
      this.virtualSportsService.subscribeForUpdates();

      this.pubsub.subscribe('virtualSport', 'INSOMNIA', data => {
        if (data.actionType === 'category-update') {
          const classId = data.classId && data.classId.toString();
          const parentCategory: IVirtualCategoryStructure = this.categories.find((category: IVirtualCategoryStructure) => {
            return category.childs && category.childs.get(classId) !== undefined;
          });

          const childCategory: IVirtualChildCategory = parentCategory && parentCategory.childs.get(classId);

          if (childCategory && childCategory.events) {
            this.virtualSportsService.updateCategoryClasses(
              childCategory.events, childCategory
            );
          }
        }
      });
      this.hideSpinner();
    }, (error) => {
      if (error === 'noCategories') {
        this.virtualMenuDataService && this.virtualMenuDataService.destroy();
        this.parentMenuItems = [];
        this.hideSpinner();
      } else {
        this.showError();
      }
    });
  }

  ngOnDestroy(): void {
    this.timerSubscription && this.timerSubscription.unsubscribe();
    this.pubsub.unsubscribe('VirtualSportsCtrl');
    this.pubsub.unsubscribe('virtualSport');
    this.virtualSportsService.unsubscribeFromUpdates();
    this.virtualSportsEventsSubscription && this.virtualSportsEventsSubscription.unsubscribe();
    this.routeChangeSuccessHandler && this.routeChangeSuccessHandler.unsubscribe();
    this.eventsDataSub && this.eventsDataSub.unsubscribe();
    this.virtualMenuDataService && this.virtualMenuDataService.destroy();
    this.parentMenuItems = [];
    this.categories = [];
    this.virtualSportsService.removeLiveServeUpdateEventListener();
  }

  /**
   * Assign listeners - interval for event start timers, location change
   */
  private addListeners(): void {
    this.timerSubscription = this.virtualSportsService.time.subscribe(now => {
      this.currentTime = now;
      this.timerHandler();
    });

    this.routeChangeSuccessHandler = this.router.events.subscribe((event: Event) => {
      if (event instanceof NavigationEnd) {
        this.updateActiveTab();
      }
    });

    // reload main virtual sports segment after lost of internet connection or sleep mode
    this.pubsub.subscribe('VirtualSportsCtrl', this.pubsub.API.RELOAD_COMPONENTS, () => {
      this.virtualSportsService.setIsReloaded(true);
      this.reload();
    });

    this.virtualSportsService.addLiveServeUpdateEventListener();
  }

  /**
   * Recalculate timeLeft value for vs sport events
   */
  private timerHandler(): void {
    this.categories.forEach((parentCategory: IVirtualCategoryStructure) => {
      if (!parentCategory.childs) {
        return;
      }

      parentCategory.childs.forEach((childCategory) => {
        if (childCategory.timeLeft !== undefined) {
          childCategory.timeLeft = childCategory.startTimeUnix - this.currentTime;

          const parentItem: IVirtualSportsMenuItem = this.parentMenuItems.find(
            (parent: IVirtualSportsMenuItem) => parent.alias === parentCategory.alias);
          const childItem: IVirtualSportsMenuItem = parentItem.childMenuItems.find(
            (child: IVirtualSportsMenuItem) => child.alias === childCategory.alias);

          childItem.label = this.getLabel(childCategory.timeLeft);
        }
      });
    });
  }

  /**
   * Create vs parent and child carousel menu
   */
  private createTopSportMenu(categories: IVirtualCategoryStructure[]): void {
    this.parentMenuItems = categories.map((parentCategory: IVirtualCategoryStructure, parentIndex: number) => {
      if (!parentCategory.childs || !parentCategory.childs.size) {
        return;
      }

      let index: number = 0;
      const childMenuItems: IVirtualSportsMenuItem[] = [];

      parentCategory.childs.forEach((childCategory: IVirtualChildCategory) => {
        const childMenuItem: IVirtualSportsMenuItem = {
          name: childCategory.title,
          inApp: true,
          svgId: '',
          targetUri: `/${VIRTUAL_ROUTE_NAME}/${SPORTS_ROUTE_NAME}/${parentCategory.alias}/${childCategory.alias}`,
          targetUriSegment: `${childCategory.alias}`,
          priority: index++,
          numberOfEvents: childCategory.numberOfEvents,
          showRunnerNumber: childCategory.showRunnerNumber,
          showRunnerImages: childCategory.showRunnerImages,
          displayOrder: index++,
          alias: childCategory.alias,
          streamUrl: childCategory.streamUrl
        };
        childMenuItem.label = this.getLabel(childCategory.timeLeft);
        childMenuItems.push(childMenuItem);
      });

      const sportMenuItem: IVirtualSportsMenuItem = {
        name: parentCategory.title,
        inApp: true,
        svgId: parentCategory.svgId,
        svg: parentCategory.svg,
        targetUri: `/${VIRTUAL_ROUTE_NAME}/${SPORTS_ROUTE_NAME}/${parentCategory.alias}`,
        targetUriSegment: `${parentCategory.alias}`,
        priority: parentIndex,
        displayOrder: parentIndex,
        childMenuItems: childMenuItems,
        alias: parentCategory.alias
      };
      return sportMenuItem;
    });

    this.virtualMenuDataService.menu = this.parentMenuItems;
  }

  /**
   * Get label object for carousel menu item (seconds, live or nothing)
   * @param {(Number|undefined)} timeLeft - milliseconds to start
   * @returns {Object} - className and text of label
   */
  private getLabel(timeLeft: number): IVirtualSportsMenuItemLabel {
    if (timeLeft >= 0) {
      return {
        className: this.MENU_TIMER_CLASS_NAME,
        text: this.filterService.date(timeLeft.toString(), 'mm:ss')
      };
    }
    return { className: this.MENU_LIVE_CLASS_NAME, text: 'Live' };
  }

  /**
   * Update active tab on route change and check if need to redirect
   */
  private updateActiveTab(): void {
    const params = this.route.children && this.route.children[0] && this.route.children[0].snapshot.params || ([] as Params);

    // some error with menu
    if (!this.virtualMenuDataService.hasParentAndChild()) {
      return;
    }

    this.activeParent = this.virtualMenuDataService.getParentIndex(params.category);
    this.activeChild = this.virtualMenuDataService.getChildIndex(params.category, params.alias);

    let parentOrChildHasChanged: boolean = false;
    if (this.activeParent < 0) {
      parentOrChildHasChanged = !!params?.category; // check that parent was present before
      this.activeParent = 0;
    }
    if (this.activeChild === undefined || this.activeChild < 0) {
      parentOrChildHasChanged = parentOrChildHasChanged? parentOrChildHasChanged : !!params.alias;
      this.activeChild = 0;
    }

    this.virtualMenuDataService.activeParentIndex = this.activeParent;
    this.virtualMenuDataService.activeChildIndex = this.activeChild;

    this.setActiveMenuElement(this.activeParent, this.activeChild);
    
    if (!params.eventId) {
      this.checkAndRedirect(parentOrChildHasChanged);
    }

    this.changeDetectorRef.detectChanges();
  }

  /**
   * Check if main virtual sport route and redirect to first tab by default
   */
  private checkAndRedirect(redirectToParent: boolean): void {
    const path = this.router.url;
    const menuItem = this.parentMenuItems[this.activeParent];
    const innApp = menuItem && menuItem.inApp || false;
    const parentSegment = menuItem && menuItem.alias;
    const childSegment = menuItem && menuItem.childMenuItems && menuItem.childMenuItems[this.activeChild]
      && menuItem.childMenuItems[this.activeChild].alias;

    if (redirectToParent) {
      if (!this.isVirtualHomeDisabled) {
        this.navigationService.openUrl(`/${VIRTUAL_ROUTE_NAME}/${SPORTS_ROUTE_NAME}/${parentSegment}/${childSegment}`, innApp, true);
      } else {
        this.navigationService.openUrl(`/${VIRTUAL_ROUTE_NAME}/${SPORTS_ROUTE_NAME}/${parentSegment}`, innApp, true);
      }
    } else if (path && (!path.includes(VIRTUAL_ROUTE_NAME) || !path.includes(parentSegment) || !path.includes(childSegment) || (parentSegment == childSegment))) {
      if(!this.isTwice(path, parentSegment)) 
        this.navigationService.openUrl(`/${VIRTUAL_ROUTE_NAME}/${SPORTS_ROUTE_NAME}/${parentSegment}/${childSegment}`, innApp, true);
    }

    if (!this.isVirtualHomeDisabled) {
      const gtmUrl: string = `/${VIRTUAL_ROUTE_NAME}/${SPORTS_ROUTE_NAME}/${parentSegment}/${childSegment}`;
      this.virtualHubService.triggerGTATracking(gtmUrl);
    }
  }

  private isTwice(path, parentSegment): boolean {
    let count = 0
    path.split('/').forEach(pathName => {
      if(pathName.includes(parentSegment)) {
        count++;
      }
    })
    return count > 1;
  }

  private setActiveMenuElement(activeParent: number, activeChild: number): void {
    activeParent = activeParent >= 0 ? activeParent : 0;
    activeChild = activeChild >= 0 ? activeChild : 0;

    const parentMenu: IVirtualSportsMenuItem[] = this.virtualMenuDataService.menu;
    if (parentMenu.length) {
      parentMenu.forEach((parent:IVirtualSportsMenuItem, index) => parent.isActive = index === activeParent);

      const activeParentItem: IVirtualSportsMenuItem = parentMenu[activeParent];

      if (activeParentItem.childMenuItems && activeParentItem.childMenuItems.length) {
        activeParentItem.childMenuItems.forEach((child: IVirtualSportsMenuItem, index) => child.isActive = index === activeChild);
      }
    }
  }

  /**
   * Additional check if reloaded after lost of internet connection or sleep mode,
   * because location is same, in such case - reload component
   */
  private reload(): void {
    if (this.virtualSportsService.isReloaded()) {
      this.virtualSportsService.setIsReloaded(false);
      this.reloadComponent();
    }
  }

  private loadVirtualIcons(): void {
    this.asyncScriptLoaderService.getSvgSprite(SPRITE_PATH.virtual).subscribe((icons: string) => this.virtualIcons = icons);
  }

  private virtualHomepageCheck(): void {
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      if ((config && !config.VirtualHubHomePage)
        || (config && config.VirtualHubHomePage && !config.VirtualHubHomePage.enabled)
        || (!config.VirtualHubHomePage.topSports && !config.VirtualHubHomePage.otherSports
          && !config.VirtualHubHomePage.nextEvents && !config.VirtualHubHomePage.featureZone
          && !config.VirtualHubHomePage.headerBanner)) {
        this.isVirtualHomeDisabled = true;
      }

    });

  }
}
