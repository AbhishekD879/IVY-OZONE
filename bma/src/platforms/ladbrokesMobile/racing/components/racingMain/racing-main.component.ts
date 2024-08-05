import { Component, OnInit, ChangeDetectorRef, OnDestroy } from '@angular/core';

import {
  RacingMainComponent as CoralRacingMainComponent
} from '@racing/components/racingMain/racing-main.component';
import { ActivatedRoute, Router } from '@angular/router';
import { TemplateService } from '@shared/services/template/template.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { RoutesDataSharingService } from '@racing/services/routesDataSharing/routes-data-sharing.service';
import { HorseracingService } from '@coreModule/services/racing/horseracing/horseracing.service';
import { GreyhoundService } from '@coreModule/services/racing/greyhound/greyhound.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { CmsService } from '@ladbrokesMobile/core/services/cms/cms.service';
import { forkJoin as observableForkJoin, of as observableOf, Subscription } from 'rxjs';
import { ISportCategory, ISystemConfig } from '@core/services/cms/models';
import { IInitialSportConfig } from '@core/services/sport/config/initial-sport-config.model';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { map, switchMap, mergeMap } from 'rxjs/operators';
import { GtmService } from '@core/services/gtm/gtm.service';
import { IRacingHeader } from '@app/shared/models/racing-header.model';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { FreeRideHelperService } from '@lazy-modules/freeRideHelper/freeRideHelper.service';
import { UserService } from '@core/services/user/user.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';
import { VirtualEntryPointsService } from '@app/racing/services/virtual-entry-points.service';


@Component({
  selector: 'racing-main-component',
  templateUrl: './racing-main.component.html'
})
export class RacingMainComponent extends CoralRacingMainComponent implements OnInit, OnDestroy {
  isNextRacesEnabled: boolean;
  isNextRacesTabEnabled: boolean;
  initialTab: string;
  private routeListener: Subscription;

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
    public user: UserService,
    public changeDetRef: ChangeDetectorRef,
    public windowRefService: WindowRefService,
    public freeRideHelperService: FreeRideHelperService,
    protected gtmService: GtmService,
    protected pubSubService: PubSubService,
    protected navigationService: NavigationService,
    protected bonusSuppressionService: BonusSuppressionService,
    protected vEPService : VirtualEntryPointsService
  ) {
    super(
      route,
      templateService,
      routingHelperService,
      routesDataSharingService,
      router,
      horseRacingService,
      greyhoundService,
      routingState,
      cms,
      changeDetRef,
      windowRefService,
      gtmService,
      pubSubService,
      navigationService,
      vEPService    
    );
  }

  ngOnInit(): void {
    this.isChildComponentLoaded = false;
    this.isHRDetailPage = this.isHorseRacingDetailPage();
    this.pubSubService.subscribe(this.RACING_MAIN_COMPONENT, 'TOP_BAR_DATA', (topBar: IRacingHeader) => {
      const breadCrumbsList = topBar.breadCrumbs;
      this.quickNavigationItems = topBar.quickNavigationItems;
      this.eventEntity = topBar.eventEntity;
      this.meetingsTitle = topBar.meetingsTitle;
      this.sportEventsData = topBar.sportEventsData;
      this.isMarketAntepost = topBar.isMarketAntepost;
      if(this.sportEventsData.length) {
        this.racesGroupByFlagAndClassType();
        this.changeDetRef.detectChanges();
      }
      if (this.isDetailPage) { this.isChildComponentLoaded = true; }
      const breadCrumbsLength = breadCrumbsList.length;
      if (breadCrumbsLength && this.isHRDetailPage) {
        const displayName = breadCrumbsList[breadCrumbsLength - 1].name;
        breadCrumbsList[breadCrumbsLength - 1].name = displayName.length > 7 ?
          `${breadCrumbsList[breadCrumbsLength - 1].name.substring(0, 7)}...` : displayName;
        if (breadCrumbsList[0].name === 'Greyhounds') {
          breadCrumbsList[0].targetUri = this.defaultTab === 'today' ? '/greyhound-racing/today' : '/greyhound-racing/races/next';
        }
      }
      this.breadcrumbsItems = breadCrumbsList;
    });
    this.addChangeDetection();
    this.racingMainSubscription = observableForkJoin([
      observableOf(this.racingService.getSport()),
      this.racingService.isSpecialsAvailable(this.router.url),
      this.cms.getSystemConfig(false)
    ]).pipe(
      mergeMap((racingData: [(HorseracingService | GreyhoundService), boolean, ISystemConfig]) => {
        this.racingData = racingData;
        this.initModel();

        let nextRacesToggle;
        if (this.racingName === 'greyhound') {
          nextRacesToggle = 'GreyhoundNextRacesToggle';
        } else if (this.racingName === 'horseracing') {
          nextRacesToggle = 'NextRacesToggle';
        }
        this.isNextRacesTabEnabled = this.racingData && this.racingData[2]
          && this.racingData[2][nextRacesToggle]
          && this.racingData[2][nextRacesToggle].nextRacesTabEnabled === true;
        this.isNextRacesEnabled = this.racingData && this.racingData[2]
          && this.racingData[2][nextRacesToggle]
          && this.racingData[2][nextRacesToggle].nextRacesComponentEnabled === true;
        this.initialTab = this.isNextRacesTabEnabled ? 'races' : 'today';
        this.defaultTab = (this.racingName === 'greyhound') ? this.initialTab : 'featured';
        // Workaround, related to SEO Static Blocks
        // Needed if 'sb' module is initialized and user types /:static path into address bar
        return this.racingInstance ? observableOf(null) : observableOf();
      }),
      map(() => {
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
    this.routeListener = this.router.events.subscribe(() => {
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
    super.getSystemConfig();
  }

  /**
   * Set racing configuration to model from racing config constant, for example: 'HORSERACING_CONFIG'
   * @param racingInstance
   */
  applyRacingConfiguration(racingInstance: any) {
    const racingConfiguration: IInitialSportConfig = racingInstance.getGeneralConfig();

    this.routingHelperService.formSportUrl(this.racingName,
      this.racingName === 'horseracing' ? 'featured' : (this.racingName === 'greyhound' ? (this.defaultTab === 'today' ? 'today' : 'races/next') : 'today'))
      .subscribe((url: string) => {
        this.racingDefaultPath = url;
      });

    this.racingId = racingConfiguration.config.request.categoryId;

    // Racing tabs information
    this.racingTabs = racingInstance
      .configureTabs(this.racingName, racingConfiguration.tabs, this.isSpecialsPresent, this.isNextRacesTabEnabled);

    this.routesDataSharingService.setRacingTabs(this.racingName, this.racingTabs);

    this.activeTab = {
      id: racingInstance.getGeneralConfig().tabs[0].id
    };
  }

  isHomeUrl(): boolean {
    const routeParams = this.router.url.split('?');
    return ['/greyhound-racing'].includes(routeParams[0]);
  }
  ngOnDestroy(): void {
    super.ngOnDestroy();
    this.pubSubService.unsubscribe(this.RACING_MAIN_COMPONENT);
    this.routeListener && this.routeListener.unsubscribe();
    this.navigationServiceSubscription && this.navigationServiceSubscription.unsubscribe();
    this.navigationService.emitChangeSource.next(null);
  }
}
