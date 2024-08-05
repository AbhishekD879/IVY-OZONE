import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import {
  of as observableOf,
  forkJoin as observableForkJoin,
  Subscription,
  SubscriptionLike as ISubscription, Observable
} from 'rxjs';
import { mergeMap, map, switchMap } from 'rxjs/operators';
import { ActivatedRoute, Router, NavigationEnd } from '@angular/router';

import { Component, OnInit, OnDestroy, ChangeDetectorRef, AfterViewChecked } from '@angular/core';
import { TemplateService } from '@shared/services/template/template.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { ISportCategory, ISystemConfig } from '@core/services/cms/models';
import { IInitialSportConfig } from '@core/services/sport/config/initial-sport-config.model';
import { RoutesDataSharingService } from '@racing/services/routesDataSharing/routes-data-sharing.service';
import { HorseracingService } from '@coreModule/services/racing/horseracing/horseracing.service';
import { GreyhoundService } from '@coreModule/services/racing/greyhound/greyhound.service';
import { GtmService } from '@coreModule/services/gtm/gtm.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { IBreadcrumb } from '@app/shared/models/breadcrumbs.model';
import { IGroupedSportEvent, ISportEvent } from '@app/core/models/sport-event.model';
import { IRacingHeader } from '@app/shared/models/racing-header.model';
import { PubSubService } from '@coreModule/services/communication/pubsub/pubsub.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { ISportConfigTab} from '@app/core/services/cms/models/sport-config-tab.model';
import { IRaceGridMeeting } from '@app/core/models/race-grid-meeting.model';
import { NEXT_RACES_HOME_CONSTANTS } from '@app/lazy-modules/lazyNextRacesTab/constants/next-races-home.constants';
import {VirtualEntryPointsService } from '@app/racing/services/virtual-entry-points.service';
@Component({
  selector: 'racing-main-component',
  templateUrl: './racing-main.component.html'
})
export class RacingMainComponent extends AbstractOutletComponent implements OnInit, OnDestroy , AfterViewChecked {

  defaultTab: string;
  racingInstance: any;
  config: ISystemConfig;
  url: string;
  racingPath: string;
  baseUrl: string;
  breadcrumbsItems: IBreadcrumb[];
  quickNavigationItems: IGroupedSportEvent[];
  sportEventsData: ISportEvent[];  
  eventsOrder: Array<string>;
  sportModule: string;
  sectionTitle: Object;
  filter: string;
  display:string;
  races: {[key: string]: Partial<IRaceGridMeeting> & {racingType?: string}};
  // races: any;

  // expected data are boolean, other
  racingData: [(HorseracingService | GreyhoundService), boolean, ISystemConfig] | [(HorseracingService | GreyhoundService), boolean];

  racingName: string;
  racingIconId: string;
  racingIconSvg: string;
  racingId: string;

  activeTab: { [id: string]: string } = {};
  racingDefaultPath: string;
  topBarInnerContent: boolean;
  categoryId: string;

  isSpecialsPresent: boolean;
  racingTabs: any;
  hasSubHeader: boolean = false;
  isBetFilterLinkAvailable: boolean = true;
  isEnhancedMultiplesEnabled: boolean = false;
  showMeetings: boolean;
  eventEntity: ISportEvent;
  meetingsTitle: {[key: string]: string};
  isHRDetailPage: boolean;
  topBarIndex: number;
  isChildComponentLoaded: boolean = false;
  sportTabs: ISportConfigTab[];
  isExtraPlaceAvailable:boolean = false;
  nextRacesComponentEnabled:boolean = false;
  offersAndFeaturedRacesTitle:string;
  isMarketAntepost: boolean = false;
  targetTab:ISportConfigTab;
  lastBannerEnabled:boolean;
  accorditionNumber:number;
  protected editMyAccaUnsavedOnEdp: boolean;
  protected readonly RACING_MAIN_COMPONENT: string = 'RacingMainComponent';
  protected racingMainSubscription: ISubscription;
  protected navigationServiceSubscription: Subscription;
  private routeChangeListener: Subscription;

  private timeOutListener;
  private intervalValue: number = 100;
  private horseRacingsubscription: Subscription;
  protected isRouteRequestSuccess = true;

  constructor(
    public route: ActivatedRoute,
    public templateService: TemplateService,
    public routingHelperService: RoutingHelperService,
    public routesDataSharingService: RoutesDataSharingService,
    public router: Router,
    public horseRacingService: HorseracingService,
    public greyhoundService: GreyhoundService,
    public routingState: RoutingState,
    public cms: CmsService,
    public changeDetRef: ChangeDetectorRef,
    public windowRefService: WindowRefService,
    protected gtmService: GtmService,
    protected pubSubService: PubSubService,
    protected navigationService: NavigationService,
    protected vEPService: VirtualEntryPointsService
  ) {
    super();
  }

  ngOnInit(): void {
    this.isChildComponentLoaded = false;
    this.getTopBarData();
    this.addChangeDetection();
    this.racingMainSubscription = observableForkJoin([
      observableOf(this.racingService.getSport()),
      this.racingService.isSpecialsAvailable(this.router.url, true)
    ]).pipe(
      mergeMap((racingData: [(HorseracingService | GreyhoundService), boolean]): Observable<void> => {
        this.racingData = racingData;
        this.initModel();

        // Workaround, related to SEO Static Blocks
        // Needed if 'sb' module is initialized and user types /:static path into address bar
        return this.racingInstance ? observableOf(null) : observableOf();
      }),
      map(() => {
        this.defaultTab = (this.racingName === 'greyhound') ? 'today' : 'featured';
        this.applyRacingConfiguration(this.racingInstance);
        this.selectTabRacing();
      }),
      switchMap(() => this.routesDataSharingService.activeTabId),
      map(id => {
        if (id) {
          this.activeTab = { id };
        }
      }),
      switchMap(() => this.routesDataSharingService.hasSubHeader),
      map(hasSubHeader => this.hasSubHeader = hasSubHeader),
      switchMap(() => this.racingId ? this.templateService.getIconSport(this.racingId) : observableOf(null)),
    ).subscribe((icon: ISportCategory) => {
      if (icon) {
        this.racingIconId = icon.svgId;
        this.racingIconSvg = icon.svg;
      }
      this.hideSpinner();
      this.hideError();
    }, () => {
      this.showError();
    });

    this.horseRacingsubscription = this.router.events.subscribe(() => {
      this.isHRDetailPage = this.isHorseRacingDetailPage();
    });
    this.navigationServiceSubscription = this.navigationService.changeEmittedFromChild.subscribe(loaded => {
      this.isChildComponentLoaded = loaded;
    });
    this.pubSubService.subscribe(this.RACING_MAIN_COMPONENT, this.pubSubService.API.RACING_NEXT_RACES_LOADED, (loaded: boolean) => {
      this.isChildComponentLoaded = loaded;
    });

    this.pubSubService.subscribe(this.RACING_MAIN_COMPONENT, this.pubSubService.API.EMA_UNSAVED_ON_EDP, (unsaved: boolean) => {
      this.editMyAccaUnsavedOnEdp = unsaved;
    });
    this.pubSubService.subscribe(this.RACING_MAIN_COMPONENT, this.pubSubService.API.ROUTE_CHANGE_STATUS, (status: boolean) => {
      this.isRouteRequestSuccess = status;
    });

    this.getSystemConfig();
  }


  ngAfterViewChecked(): void {
      this.vEPService.findBannerAccordition();
  }
  /**
 * Check if edit my acca is in progress for changing route
 * @returns {boolean}
 */
  canChangeRoute(): boolean {
    return !this.editMyAccaUnsavedOnEdp;
  }

  /**
   * open edit my acca pop-up if edit is in progress while changing route
   */
  onChangeRoute(): void {
    this.pubSubService.publish(this.pubSubService.API.EMA_OPEN_CANCEL_DIALOG);
  }

  goToDefaultPage(): void {
    if ((this.racingName === 'horseracing' && this.router.url === '/horse-racing' && this.racingDefaultPath === '/horse-racing/featured') ||
    (this.racingName === 'greyhound' && this.router.url === '/greyhound-racing' && ((this.defaultTab === 'today' && this.racingDefaultPath === '/greyhound-racing/today') || (this.defaultTab === 'races' && this.racingDefaultPath === '/greyhound-racing/races/next')))) {
      return;
    }
    this.router.navigateByUrl(this.racingDefaultPath);
  }

  getSystemConfig(): void {
    this.cms.getToggleStatus('EnhancedMultiples').subscribe((isEnhancedMultiplesEnabled: boolean) => {
      this.isEnhancedMultiplesEnabled = isEnhancedMultiplesEnabled;
    });
    this.cms.getSystemConfig(false)
      .subscribe((config: ISystemConfig) => {
        if (config.BetFilterHorseRacing && !config.BetFilterHorseRacing.enabled) {
          this.isBetFilterLinkAvailable = false;
        }

        if (config.featuredRaces && config.featuredRaces.enabled) {
          this.isExtraPlaceAvailable = true;
          this.offersAndFeaturedRacesTitle = 'OFFERS AND FEATURED RACES';
        }
        this.nextRacesComponentEnabled = config && config.NextRacesToggle
          && config.NextRacesToggle.nextRacesComponentEnabled === true;
        //this.defaultAntepostTab = config && config.defaultAntepostTab && config.defaultAntepostTab.tabName;
      });
  }

  get isDetailPage(): boolean {
    const currentSegment = this.routingState.getCurrentSegment();
    return currentSegment === 'horseracing.eventMain' ||
      currentSegment === 'horseracing.eventMain.market' ||
      currentSegment === 'horseracing.eventMain.market.marketType' ||
      currentSegment === 'greyhound.eventMain' ||
      currentSegment === 'greyhound.eventMain.market' ||
      currentSegment === 'horseracing.buildYourRaceCard';
  }
  set isDetailPage(value:boolean){}

  ngOnDestroy(): void {
    this.timeOutListener && this.windowRefService.nativeWindow.clearInterval(this.timeOutListener);
    this.routeChangeListener && this.routeChangeListener.unsubscribe();
    this.racingMainSubscription && this.racingMainSubscription.unsubscribe();
    this.pubSubService.unsubscribe(this.RACING_MAIN_COMPONENT);
    this.horseRacingsubscription && this.horseRacingsubscription.unsubscribe();
    this.navigationServiceSubscription && this.navigationServiceSubscription.unsubscribe();
    this.navigationService.emitChangeSource.next(null);
  }

  addChangeDetection(): void {
    this.changeDetRef.detach();
    this.timeOutListener = this.windowRefService.nativeWindow.setInterval(() => {
      this.changeDetRef.detectChanges();
    }, this.intervalValue);
  }

  get racingService(): HorseracingService | GreyhoundService {
    const segment = this.routingState.getCurrentSegment();

    return segment.indexOf('horseracing') >= 0 ? this.horseRacingService : this.greyhoundService;
  }
  set racingService(value: HorseracingService | GreyhoundService){}

  initModel(): void {
    this.racingInstance = (this.racingData && this.racingData[0]) || this.racingData;
    this.config = this.racingInstance && this.racingInstance.getConfig();
    const generalConfig = this.racingInstance.getGeneralConfig();
    this.isSpecialsPresent = this.racingData && this.racingData[1];
    this.racingName = this.config && this.config.name;
    this.categoryId = (this.config && this.config.request.categoryId) || '';
    this.url = this.router.url;
    this.racingPath = (this.config && (this.config.path || this.racingName)) || '';
    this.baseUrl = this.url.substring(0, this.url.indexOf(this.racingPath) + this.racingPath.length);
    this.display = this.route.snapshot.params['display'];
    this.filter = this.route.snapshot.params['filter'];
     this.sectionTitle = generalConfig.sectionTitle;
    // Events ordering
    this.eventsOrder = generalConfig.order.EVENTS_ORDER;
    this.sportModule = generalConfig.config.sportModule;
    // Allow inner content for 'horseracing'
    this.topBarInnerContent = this.racingName === 'horseracing';
  }

  /**
   * Store tab and start to track route change for racing
   */
  selectTabRacing(): void {
    const display: string = this.tabDisplay;
    this.activeTab.id = `tab-${display}`;
    this.routesDataSharingService.updatedActiveTabId(this.activeTab.id);
    const currentTab = display ? this.tabDisplay : this.defaultTab;
    this.vEPService.getTabs(this.categoryId, currentTab);
    this.getEntryPointsData();

    this.routeChangeListener = this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        const displayAfterSwicth: string = this.route.snapshot.firstChild && this.route.snapshot.firstChild.params['display'];
        this.activeTab.id = `tab-${(displayAfterSwicth || this.defaultTab)}`;
        this.router.url?.includes(displayAfterSwicth) && this.vEPService.getTabs(this.categoryId,displayAfterSwicth);
        this.getEntryPointsData();
      }
    });
  }
 
  private getEntryPointsData()
  {
    this.vEPService.targetTab.subscribe((tab: ISportConfigTab | null) => {
      this.targetTab = tab;
    });

    this.vEPService.lastBannerEnabled.subscribe((lbe: boolean) => {
      this.lastBannerEnabled = lbe;
    });
  
    this.vEPService.accorditionNumber.subscribe((accNum: number) => {
      this.accorditionNumber = accNum;
    });

    this.routeChangeListener = this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        if (this.isRacingLandingPage() && event.url!==event.urlAfterRedirects) {
          this.goToDefaultPage();
        }
        const displayAfterSwicth: string = this.route.snapshot.firstChild && this.route.snapshot.firstChild.params['display'];
        this.activeTab.id = `tab-${(displayAfterSwicth || this.defaultTab)}`;
        if(event.url.includes('horse-racing')) {
          this.router.url?.includes(displayAfterSwicth) && this.vEPService.getTabs(this.categoryId,displayAfterSwicth);
        }
        this.vEPService.targetTab.subscribe((tab: ISportConfigTab | null) => {
          this.targetTab = tab;
        });
        this.vEPService.lastBannerEnabled.subscribe((lbe: boolean) => {
          this.lastBannerEnabled = lbe;
        });
        this.vEPService.accorditionNumber.subscribe((accNum: number) => {
          this.accorditionNumber = accNum;
        });
      }
    });
  }
  get tabDisplay(): string {
    const firstChild = this.route.snapshot.firstChild;

    if (!firstChild) {
      return this.defaultTab;
    }

    return firstChild.params['display'] || firstChild.routeConfig.path;
  }
  set tabDisplay(value:string){}
  /**
   * Set racing configuration to model from racing config constant, for example: 'HORSERACING_CONFIG'
   * @param racingInstance
   */
  applyRacingConfiguration(racingInstance: any) {
    const racingConfiguration: IInitialSportConfig = racingInstance.getGeneralConfig();

    this.routingHelperService.formSportUrl(this.racingName,
      this.racingName === 'horseracing' ? 'featured' : 'today').subscribe((url: string) => {
        this.racingDefaultPath = url;
    });

    this.racingId = racingConfiguration.config.request.categoryId;

    // Racing tabs information
    this.racingTabs = racingInstance.configureTabs(this.racingName, racingConfiguration.tabs, this.isSpecialsPresent);

    this.routesDataSharingService.setRacingTabs(this.racingName, this.racingTabs);

    this.activeTab = {
      id: racingInstance.getGeneralConfig().tabs[0].id
    };
  }

  /**
   * To show the meetings list and to log click event
   */
  showMeetingsList(): void {
    this.showMeetings = !this.showMeetings;
    if (this.showMeetings) {
      this.gtmService.push('trackEvent', {
        eventCategory: this.sportModule == 'horseracing' ? NEXT_RACES_HOME_CONSTANTS.HORSE_RACING_LOWERCASE : NEXT_RACES_HOME_CONSTANTS.GREYHOUNDS_LOWERCASE,
        eventAction: 'meetings',
        eventLabel: 'open'
      });
    }

    this.windowRefService.nativeWindow.scrollTo(0, 0);
    this.pubSubService.publish(this.pubSubService.API.ACTIVE_FUTURE_TAB);
  }

  /**
   * Check if it horse rading details page or Greyhound details.
   */
  protected isHorseRacingDetailPage(): boolean {
    const currentSegment = this.routingState.getCurrentSegment();
    const isHorseRacingEDP = currentSegment === 'horseracing.eventMain' ||
      currentSegment === 'horseracing.eventMain.market' ||
      currentSegment === 'horseracing.eventMain.market.marketType' ||
      currentSegment === 'greyhound.eventMain' ||
      currentSegment === 'greyhound.eventMain.market' ||
      currentSegment === 'greyhound.eventMain.market.marketType';
    this.topBarIndex = isHorseRacingEDP ? 1003 : 7;
    return isHorseRacingEDP;
  }


  /**
   * Is redirect to racing landing page
   * @returns {Boolean}
   */
  private isRacingLandingPage(): boolean {
    const routeSegment = this.routingState.getCurrentSegment();
    return ['horseracing', 'greyhound'].includes(routeSegment);
  }

  /**
   * To fetch breadcrums data on publish
   */
  private getTopBarData(): void {
    this.isHRDetailPage = this.isHorseRacingDetailPage();
    this.pubSubService.subscribe(this.RACING_MAIN_COMPONENT, 'TOP_BAR_DATA', (topBar: IRacingHeader) => {
      const breadCrumbsList = topBar.breadCrumbs;
      this.quickNavigationItems = topBar.quickNavigationItems;
      this.sportEventsData = topBar.sportEventsData;
      this.isMarketAntepost = topBar.isMarketAntepost;
      if (topBar.sportEventsData?.length) {
        this.racesGroupByFlagAndClassType();
        this.changeDetRef.detectChanges();
      }
      this.eventEntity = topBar.eventEntity;
      this.meetingsTitle = topBar.meetingsTitle;
      if (this.isDetailPage) { this.isChildComponentLoaded = true; }
      const breadCrumbsLength = breadCrumbsList.length;
      if (breadCrumbsLength && this.isHRDetailPage) {
        const displayName = breadCrumbsList[breadCrumbsLength - 1].name;
        breadCrumbsList[breadCrumbsLength - 1].name = displayName.length > 7 ?
          `${breadCrumbsList[breadCrumbsLength - 1].name.substring(0, 7)}...` : displayName;
      }
      this.breadcrumbsItems = breadCrumbsList;
    });
  }

  racesGroupByFlagAndClassType() {
    this.races = this.racingService.groupByFlagCodesAndClassesTypeNames(this.sportEventsData) as any;
  }
}
