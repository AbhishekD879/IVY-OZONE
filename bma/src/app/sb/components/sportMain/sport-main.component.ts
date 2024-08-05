import { Component, OnInit, Input, OnDestroy } from '@angular/core';
import { Router, Event, NavigationEnd, ActivatedRoute } from '@angular/router';

import { Subscription, Observable } from 'rxjs';
import { map, concatMap } from 'rxjs/operators';

import * as _ from 'underscore';

import { CmsService } from '@core/services/cms/cms.service';
import { ISportConfigTab, ISportConfig, ISportTabs } from '@core/services/cms/models';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { GamingService } from '@core/services/sport/gaming.service';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { Location } from '@angular/common';
import { StorageService } from '@core/services/storage/storage.service';
import { UserService } from '@core/services/user/user.service';
import { TimeService } from '@core/services/time/time.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { DeviceService } from '@core/services/device/device.service';
import { SportTabsService } from '@sb/services/sportTabs/sport-tabs.service';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
import { SlpSpinnerStateService } from '@core/services/slpSpinnerState/slpSpinnerState.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DialogService } from '@app/core/services/dialogService/dialog.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { ILazyComponentOutput } from '@app/shared/components/lazy-component/lazy-component.model';

@Component({
  selector: 'sport-main-component',
  templateUrl: './sport-main.component.html'
})
export class SportMainComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  @Input() sportBanner?: string;

  sport: GamingService;
  sportName: string;
  sportTitle: string;
  sportIconId: string;
  sportIconSvg: string;
  sportId: string;
  sportTabs: ISportConfigTab[];
  sportActiveTab: { [id: string]: string };
  topBarInnerContent: boolean;
  displayCBLink: boolean;
  categoryId: string;
  favourites: any;
  isSportDetailPage: boolean;
  goToDefaultPage: Function;
  isLazyComponentLoaded: boolean;
  isChildComponentLoaded: boolean = false;
  configuredTabs:ISportConfigTab[];

  initialStorageTab: string;
  protected defaultTab: string = 'matches';
  protected config: any; // todo: get integface after GameService PR merge !
  protected privateSportName: string;
  protected shouldSaveTab: boolean;
  protected extension: string;
  protected url: string;
  protected sportPath: string;
  protected baseUrl: string;
  protected routeChangeListener: Subscription;
  protected routeParamsListener: Subscription;
  protected loadTimeout: any; // Timer
  protected param: string = '';
  channelName: string = 'sportMain';
  competitions: string = 'competitions';
  public isEnhancedMultiplesEnabled: boolean = false;
  private eventId: string;
  private editMyAccaUnsavedOnEdp: boolean;
  private sportsConfigSubscription: Subscription;
  private navigationServiceSubscription: Subscription;
  changeMatch: boolean = false;
  isQuickSwitchEnabled: boolean = false;
  typeId: string;

  constructor(
    protected cmsService: CmsService,
    protected timeService: TimeService,
    protected sportsConfigService: SportsConfigService,
    protected routingState: RoutingState,
    protected pubSubService: PubSubService,
    protected location: Location,
    protected Storage: StorageService,
    protected User: UserService,
    protected router: Router,
    protected route: ActivatedRoute,
    protected device: DeviceService,
    protected sportTabsService: SportTabsService,
    protected coreToolsService: CoreToolsService,
    protected slpSpinnerStateService: SlpSpinnerStateService,
    protected navigationService: NavigationService,
    protected windowRefService: WindowRefService,
    protected dialogService: DialogService,
    protected gtmService: GtmService) {
    super();
  }

  ngOnInit(): void {
    this.isChildComponentLoaded = false;
    this.param = this.routingState.getRouteParam('sport', this.route.snapshot);
    this.eventId = this.routingState.getRouteParam('id', this.route.snapshot);
    this.loadSportData();

    this.routeParamsListener = this.route.params.subscribe((params: { sport: string, id: string}) => {
      if (params.id && Number(params.id).toString() !== params.id) {
        this.navigationService.handleHomeRedirect('slp');
      }

      // After change of sport name in url OR event ID component should be reloaded
      if (this.param !== params['sport'] || (this.eventId && this.eventId !== params['id'])) {
        this.param = params['sport'];
        this.eventId = params['id'];
        this.loadComponent();
      }
    });

    this.routeChangeListener = this.router.events.subscribe((event: Event) => {
      if (event instanceof NavigationEnd) {
        if (this.routingState.getRouteParam('display', this.route.snapshot) === null) {
          this.filterTabs(this.sportTabs);
        }
        const display = this.routingState.getRouteParam('display', this.route.snapshot) || this.defaultTab,
          sportPath = this.routingState.getRouteParam('sport', this.route.snapshot);
        if (display && display !== this.defaultTab && display !== this.competitions) { this.isChildComponentLoaded = true; }
        if (sportPath === this.sportPath) {
          this.processUrl(display, event);
        }
      }
    });

    this.getIsEnhancedMultiplesEnabled().subscribe((isEnhancedMultiplesEnabled: boolean) => {
      this.isEnhancedMultiplesEnabled = isEnhancedMultiplesEnabled;
    });

    this.pubSubService.subscribe(this.channelName, this.pubSubService.API.EMA_UNSAVED_ON_EDP, (unsaved: boolean) => {
      this.editMyAccaUnsavedOnEdp = unsaved;
    });
    this.navigationServiceSubscription = this.navigationService.changeEmittedFromChild.subscribe(loaded => {
      this.isChildComponentLoaded = loaded;
    });
  }

  ngOnDestroy(): void {
    this.routeParamsListener && this.routeParamsListener.unsubscribe();
    this.routeChangeListener && this.routeChangeListener.unsubscribe();
    this.destroySportData();
    this.slpSpinnerStateService.clearSpinnerState();
    this.pubSubService.unsubscribe(this.channelName);
    this.sportsConfigSubscription && this.sportsConfigSubscription.unsubscribe();
    this.navigationServiceSubscription && this.navigationServiceSubscription.unsubscribe();
    this.navigationService.emitChangeSource.next(null);
  }

  canChangeRoute(): boolean {
    return !this.editMyAccaUnsavedOnEdp;
  }

  onChangeRoute(): void {
    this.pubSubService.publish(this.pubSubService.API.EMA_OPEN_CANCEL_DIALOG);
  }

  /**
   * Check if it's sport home url
   */
  isHomeUrl(): boolean {
    const routeSegment = this.routingState.getRouteSegment('segment', this.route.snapshot);
    return _.contains(['sport', 'olympicsSport'], routeSegment);
  }

  initLazyHandler(): void {
    this.isLazyComponentLoaded = true;
    this.isChildComponentLoaded = true;
  }

  /**
   * Set sport configuration to model from sport config constant, for example: 'FOOTBALL_CONFIG'
   * @param sportInstance
   */
  protected applySportConfiguration(sportInstance: any): void {
    const sportConfiguration: ISportConfig = sportInstance.sportConfig;
    const sportURL: string = this.route.snapshot.url[0].path === 'olympics' ? `olympics/` : 'sport/';
    const sportDefaultPage: string = sportConfiguration.config.defaultTab
      || this.getSportUri(sportURL);

    this.sportName = sportConfiguration.config.name;
    this.sportTitle = sportConfiguration.config.title;
    this.sportBanner = this.sportName || this.sportBanner;

    this.sportId = sportConfiguration.config.request.categoryId;

    this.goToDefaultPage = () => {
      this.pubSubService.publish(this.pubSubService.API.SPORT_DEFAULT_PAGE);

      if (sportDefaultPage) {
        this.router.navigateByUrl(sportDefaultPage);
      }
    };
  }

  protected filterTabs(sportTabs: ISportConfigTab[]): ISportConfigTab[] {
    this.configuredTabs = sportTabs;
    this.checkTabs(sportTabs);

    const matchesTab: ISportConfigTab = sportTabs.find((tab: ISportConfigTab) => tab.name === 'matches' && !tab.hidden);
    if (matchesTab) {
      this.defaultTab = matchesTab.name;
    } else {
      const firstTab = sportTabs.find((tab: ISportConfigTab) => !tab.hidden);
      this.defaultTab = firstTab && firstTab.name;
    }

    return sportTabs;
  }

  /**
   * Get tab and start to track route change and login event for sport
   */
  protected selectTabSport(): void {
    const display: string = this.routingState.getRouteParam('display', this.route.snapshot);
    if (display && _.findWhere(this.sportTabs, { name: display }) && !_.findWhere(this.sportTabs, { name: display }).hidden) {
      this.processUrl(display);
    } else if (!display) {
      this.processUrl(display);
    } else {
      this.windowRefService.nativeWindow.setTimeout(() => this.router.navigate([this.defaultTab], { relativeTo: this.route }));
    }
    this.pubSubService.subscribe(this.channelName, this.pubSubService.API.SESSION_LOGIN, () => {
      if (this.isDefaultUrl() || display) {
        this.setSportTab(display || this.defaultTab);
      }
    });
  }

  favIconDown() {
    this.windowRefService.document.getElementById('fav-icon').classList.add('fav-icon-active');
  }

  favIconUp() {
    this.windowRefService.document.getElementById('fav-icon').classList.add('fav-icon-inactive');
  }

  protected shouldNavigatedToTab() {
    return this.isHomeUrl();
  }

  protected checkTabs(sportTabs: ISportConfigTab[]): void {
    if (!sportTabs.length || sportTabs.every(el => el.hidden)) {
      this.navigationService.handleHomeRedirect('slp');
    }
  }

  /**
   * Form sport uri for:
   * mobile - sport/{sportName}
   * desktop - sport/{sportName}/matches/today
   * @param sportURL
   */
  private getSportUri(sportURL: string): string {
    return this.device.isDesktop ? `${sportURL}${this.route.snapshot.params.sport}/matches/today` :
      `${sportURL}${this.route.snapshot.params.sport}`;
  }

  private loadSportData(): void {
    this.isSportDetailPage = this.route.snapshot.data['segment'] === 'eventMain';

    this.sportsConfigSubscription = this.sportsConfigService.getSport(this.route.snapshot.paramMap.get('sport'), this.isSportDetailPage)
    .pipe(
      concatMap((sport: GamingService) => {
        this.sport = sport;
        this.initModel();
        this.applySportConfiguration(sport);
        return this.cmsService.getSportTabs(this.sportId);
      }),
      map((sportTabs: ISportTabs) => this.filterTabs(sportTabs.tabs))
    )
    .subscribe((sportTabs: ISportConfigTab[]) => {
      if (this.sport && this.sport.config) {
        this.sportTabs = sportTabs;
        // shouldSaveTab - param to set/get tab to/from storage (football only)
        this.shouldSaveTab = this.privateSportName === 'football' && this.extension !== 'olympics';

        this.initialStorageTab = this.getSportTab() || 'matches';

        this.selectTabSport();
        this.hideSpinner();
      } else {
        this.navigationService.handleHomeRedirect('slp');
      }
    }, error => {
      this.hideSpinner();
      this.navigationService.handleHomeRedirect('slp');
      console.warn('SportMain', error.error || error);
    });
  }

  private destroySportData(): void {
    clearTimeout(this.loadTimeout);
  }

  /**
   * Load segment
   * @private
   */
  private loadComponent(): void {
    this.destroySportData();
    this.showSpinner();
    this.loadTimeout = setTimeout(() => {
      this.loadSportData();
    }, this.timeService.oneSecond);
  }

  private initModel(): void {
    this.config = this.sport && this.sport.getConfig();
    this.privateSportName = this.config && this.config.name;
    this.categoryId = (this.config && this.config.request.categoryId) || '';
    this.extension = (this.config && this.config.extension) || '';
    this.shouldSaveTab = false;
    this.url = this.location.path();
    this.sportPath = (this.config && (this.config.path || this.privateSportName)) || {};
    this.baseUrl = this.url.substring(0, this.url.indexOf(this.sportPath) + this.sportPath.length);

    // Allow inner content for 'football'
    this.topBarInnerContent = this.privateSportName === 'football';

    // Check if to show 'Bet Filter' in header
    this.displayCBLink = this.privateSportName === 'football';
  }

  /**
   * Get or set tab depending on url
   */
  private processUrl(display: string, event?: Event): void {
    let tab;
    if( this.route.snapshot['_routerState'] && this.route.snapshot['_routerState'].url.includes('golf_matches')) {
      this.defaultTab = "golf_matches";
    }
    else{
      this.configuredTabs && this.filterTabs(this.configuredTabs)
    }

    if (this.shouldNavigatedToTab()) {
      tab = this.getSportTab();
      if (tab) {
        if (this.router.url === this.baseUrl) {
          this.sportActiveTab = { id: `tab-${this.initialStorageTab}` };
          this.defaultTab = this.initialStorageTab;
          this.setSportTab(this.initialStorageTab);
        } else {
          this.sportActiveTab = { id: `tab-${tab}` };
          this.defaultTab = tab;
        }
      } else if (this.defaultTab) {
        this.sportActiveTab = { id: `tab-${this.defaultTab}` };
      }
    } else if (this.isDefaultUrl() || display) {
      tab = display || this.defaultTab;
      this.sportActiveTab = { id: `tab-${tab}` };
      this.setSportTab(tab);
    }
    if(this.sportName=='golf' && event){
      this.gtmDataOnSelectedTabLoads();
    }
  }

  /**
   * Check if it's sport default url
   */
  private isDefaultUrl(): boolean {
    return this.getPath().indexOf(this.sportName) !== -1 && this.getPath().indexOf(this.defaultTab) !== -1;
  }

  /**
   * Set tab to storage
   */
  private setSportTab(tab: string): void {
    if (this.shouldSaveTab && this.User.status) {
      this.Storage.set(this.getTabStorageName(), tab);
    }
  }

  /**
   * Get tab from storage
   */
  private getSportTab(): void | string {
    const savedTab: string = this.Storage.get(this.getTabStorageName());
    return (!this.shouldSaveTab || !this.User.status) ? undefined
      : _.find(this.sportTabs, t => t.name === savedTab && !t.hidden) && savedTab;
  }

  /**
   * Get current url
   */
  private getPath(): string {
    return this.location.path().replace(/-/g, '');
  }

  /**
   * Storage name for tab
   */
  private getTabStorageName(): string {
    return `${this.baseUrl}-tab-${this.User.username}`;
  }

  private getIsEnhancedMultiplesEnabled(): Observable<boolean> {
    return this.cmsService.getToggleStatus('EnhancedMultiples');
  }
  /**
   * Hide/Show quick sswitch window
   */
  changeMatchToggle() {
    this.changeMatch = !this.changeMatch;
  }
  gtmDataOnSelectedTabLoads(){
    const gtmData = {
      'event': 'pageView',
      'page.referrer': window.location.hostname+this.baseUrl,
      'page.url': window.location.href,
      'page.host': window.location.hostname, 
      'page.pathQueryAndFragment': 'en'+window.location.pathname,
      'page.name': 'en'+window.location.pathname 
    }
    this.gtmService.push(gtmData.event, gtmData);
  }
  /**
   * Event handler for sportEventMain
   * @param output
   */
  handleSportEvent(output: ILazyComponentOutput): void {
    if (output.output === 'quickSwitchHandler') {
      this.quickSwitchEnabled(output.value);
    }
    if (output.output === 'typeId') {
      this.typeId = output.value;
    }
  }
  /**
   * Sets isQuickSwitchEnabled value to true/false
   * @param flag 
   */
  quickSwitchEnabled(flag: boolean) {
    this.isQuickSwitchEnabled = flag;
  }
  /**
   * Close quick switch window
   * @param flag 
   */
  handleQuickSwitchEvent(output: ILazyComponentOutput): void {
    if (output.output === 'closeQuickSwitchPanel') {
      this.changeMatch = false;
    }
  }
}
