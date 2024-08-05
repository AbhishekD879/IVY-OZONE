import { AfterViewInit, Component, Input, OnChanges, OnDestroy, OnInit } from '@angular/core';
import { Event, NavigationEnd, Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { Location } from '@angular/common';
import * as _ from 'underscore';

import { UserService } from '@core/services/user/user.service';
import { ModuleRibbonService } from '@core/services/moduleRibbon/module-ribbon.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

import { IModuleRibbonTab, INavigationPoint } from '@core/services/cms/models';
import { IConstant } from '@core/services/models/constant.model';
import { SessionService } from '@authModule/services/session/session.service';
import { CmsService } from '@core/services/cms/cms.service';
import { GA_TRACKING } from '../../constants/channel.constant';
import { IGATrackingModel } from '@app/core/models/gtm.event.model';
import { SessionStorageService } from '@app/core/services/storage/session-storage.service';
import { DeviceService } from '@app/core/services/device/device.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';

@Component({
  selector: 'module-ribbon',
  templateUrl: 'module-ribbon.component.html'
})
export class ModuleRibbonComponent implements OnInit, OnChanges, OnDestroy, AfterViewInit {

  @Input() ribbon: IModuleRibbonTab[];

  homeTabUrl: string;
  activeTab: IConstant;
  moduleList: Partial<IModuleRibbonTab>[];
  superButtonAvailable: boolean = false;
  sbAlignment = '';
  GTMTrackingObj: IGATrackingModel;
  initialTabLoaded: string;
  isFirstBetAvailable: boolean = true;
  protected privateMarketTabCreated: boolean;

  private routeListener: Subscription;
  private hasNavPointForHome: any;
  private readonly title = 'ModuleRibbonComponent';
  constructor(
    protected location: Location,
    protected ribbonService: ModuleRibbonService,
    protected user: UserService,
    protected pubSubService: PubSubService,
    protected router: Router,
    protected sessionService: SessionService,
    protected cmsService: CmsService,
    private device: DeviceService,
    protected sessionStorageService: SessionStorageService,
    private bonusSuppressionService: BonusSuppressionService
  ) {
  }

  ngOnChanges(): void {
    this.moduleList = this.ribbonService.filterTabs(this.ribbon);
    this.filterModulesBasedOnRgyellow();
    const url = this.location.path();
    const [baseURL] = url.split('?');
    const isTabAvailable = this.moduleList.find(module => module.url === baseURL);
    if (!isTabAvailable) {
      this.router.navigate(['/']);
    }
  }
  /**
   * Initialization function
   */
  ngOnInit(): void {
    this.moduleList = this.ribbonService.moduleList.length
      ? this.ribbonService.moduleList : this.ribbonService.filterTabs(this.ribbon);
    this.filterModulesBasedOnRgyellow();
    this.getHomeTabNavigationPoints();
    this.setActiveTab();
    this.setGATrackingData();
    this.sessionService.whenUserSession()
      .subscribe(() => this.addPrivateMarketTab(), err => console.error(err));

    this.pubSubService.subscribe(this.title, [this.pubSubService.API.SESSION_LOGIN], () => {
        this.filterModulesBasedOnRgyellow();
    });

    this.pubSubService.subscribe(this.title, [this.pubSubService.API.SUCCESSFUL_LOGIN], () => {
      this.addPrivateMarketTab();
    });

    this.pubSubService.subscribe(this.title, [this.pubSubService.API.SEGMENTED_INIT_FE_REFRESH], () => {
      if (!this.superButtonAvailable) {
        this.setActiveTab();
      }
    });

    this.routeListener = this.router.events.subscribe((event: Event) => {
      if (event instanceof NavigationEnd) {
        this.setActiveTab();
      }
    });

    this.isFirstBetAvailable = !this.sessionStorageService.get('firstBetTutorial')?.firstBetAvailable;
  }

  /**
   *  checks if the main page is home page
  */
  private checkIfHomeUrl(): boolean {
    const currentPath: string = this.location.path();
    return currentPath === '' || currentPath.indexOf('/home/') > -1 || currentPath.indexOf('utm_source=PWA') > -1 ||
      currentPath.startsWith('?');
  }

  setGATrackingData() {
    this.GTMTrackingObj = {
      isHomePage: this.checkIfHomeUrl(),
      event: GA_TRACKING.event,
      GATracking: {
        eventAction: GA_TRACKING.eventAction,
        eventCategory: GA_TRACKING.moduleRibbon.eventCategory,
        eventLabel: "",
      }
    };
  }

  ngAfterViewInit() {
    if (performance.mark) { performance.mark('BMA:FMP'); }
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.title);
    this.routeListener.unsubscribe();
  }

  protected addPrivateMarketTab(): void {
    if (this.user && this.user.status && !this.isOnPrivateMarketTab() && !this.privateMarketTabCreated) {
      this.privateMarketTabCreated = true;
      this.ribbonService.getPrivateMarketTab(_.clone(this.ribbon)).subscribe(result => {
        this.moduleList = [...result];
        this.filterModulesBasedOnRgyellow();
        this.setLocation();
      }, () => this.privateMarketTabCreated = false);
    }
  }

  /**
   * Set Location
   * @private
   */
  protected setLocation(): void {
    if (this.canRedirectToHomePage()) {
      this.router.navigate(['/']);
    } else if (this.canRedirectToPrivateMarketsTab()) {
      this.router.navigate(['home', 'private-markets']);
    }
  }

  protected isOnPrivateMarketTab(): boolean {
    return this.location.isCurrentPathEqualTo('/home/private-markets');
  }

  protected canRedirectToHomePage() {
    return !this.ribbonService.isPrivateMarketsTab() && this.isOnPrivateMarketTab();
  }

  protected isCurrentPathEmpty(): boolean {
    return this.router.url.split(/[?#]/)[0] === '/';
  }

  protected canRedirectToPrivateMarketsTab() {
    return this.isCurrentPathEmpty() && this.ribbonService.isPrivateMarketsTab();
  }

  private isActiveTabHome(): boolean {
    return this.activeTab.url === '/home/featured' || this.activeTab.url === '';
  }

  /**
   * Set Active Tab
   * @param {string} currentUrl
   */
  private setActiveTab(currentUrl?: string): void {
    this.sbAlignment = '';
    const url = currentUrl || this.location.path();
    const [baseURL] = url.split('?');
    if (baseURL === '/' || baseURL === '/home/featured' || baseURL === '') {
      this.getHomeTabNavigationPoints();
    }
    const activeTab = _.find(this.moduleList, m => m.url === url.split('?')[0]);
    const currentId = activeTab ? activeTab.id : 'tab-featured';

    this.homeTabUrl = `${this.isCurrentPathEmpty() ? '/home/featured' : this.location.path()}`;
    [this.homeTabUrl] = this.homeTabUrl.split('?');
    this.activeTab = {
      id: currentId,
      url: activeTab ? activeTab.url : ''
    };
    this.superButtonAvailable = !this.isActiveTabHome() ||!_.isEmpty(this.hasNavPointForHome) || this.cmsService.hasExtraNavPoints;
    if(this.device.requestPlatform === 'mobile' && !this.sessionStorageService.get('initialTabLoaded')) {
      this.sessionStorageService.set('initialTabLoaded', {id: this.activeTab.id, url: this.homeTabUrl});
    } else {
      this.initialTabLoaded = this.sessionStorageService.get('initialTabLoaded').id;
    }
  }

  private getHomeTabNavigationPoints() {
    this.cmsService.getNavigationPoints(['/home/featured'],'homeTabs').subscribe((data: INavigationPoint[]) => {
      this.hasNavPointForHome = data.filter((item: INavigationPoint) => {
        return item.homeTabs.some((tab: string) => tab === '/home/featured');
      });
      this.sbAlignment = this.hasNavPointForHome && this.hasNavPointForHome.length && this.hasNavPointForHome[0]['ctaAlignment'];
    });
  }
  getPlaceholderCls() {
    const alignmentClasses = {
      right: 'cta-right',
      center: 'cta-center',
    };
    if(this.sbAlignment) {
      return alignmentClasses[this.sbAlignment];
    } else if(this.superButtonAvailable && this.isActiveTabHome()) {
      return 'no-cta'
    }
  }

  /**
   * Filter set correct links
   * @private
   */
   filterModulesBasedOnRgyellow(): void {
    const moduleList = [...this.moduleList];
    this.moduleList = [];
    this.moduleList = moduleList.filter((link: IModuleRibbonTab) => {
      return this.bonusSuppressionService.checkIfYellowFlagDisabled(link.title);
    })
  }

  onStartTutorialClick(): void {
    this.isFirstBetAvailable = false;
  }
}
