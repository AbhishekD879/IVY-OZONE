import { from as observableFrom, Subscription, of } from 'rxjs';
import { concatMap, switchMap } from 'rxjs/operators';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import * as _ from 'underscore';

import environment from '@environment/oxygenEnvConfig';
import { horseracingConfig } from '@core/services/racing/config/horseracing.config';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { TemplateService } from '@shared/services/template/template.service';
import { RoutesDataSharingService } from '@racing/services/routesDataSharing/routes-data-sharing.service';
import { TimeService } from '@core/services/time/time.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { DeviceService } from '@core/services/device/device.service';
import { IInitialSportConfig } from '@core/services/sport/config/initial-sport-config.model';
import { ICombinedSportEvents, IGroupedSportEvent, ISportEvent } from '@core/models/sport-event.model';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { GreyhoundService } from '@coreModule/services/racing/greyhound/greyhound.service';
import { HorseracingService } from '@coreModule/services/racing/horseracing/horseracing.service';
import { IMarket } from '@app/core/models/market.model';
import { SmartBoostsService } from '@sb/services/smartBoosts/smart-boosts.service';
import { IOutcome } from '@core/models/outcome.model';
import { IEventsOptions } from '@racing/models/racing-ga.model';
import { ISystemConfig } from '@core/services/cms/models';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { NextRacesService } from '@core/services/racing/nextRaces/next-races.service';
import { EventService } from '@sb/services/event/event.service';
import { ExtraPlaceService } from '@core/services/racing/extraPlace/extra-place.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IAutoSeoData } from '@app/core/services/cms/models/seo/seo-page.model';
import { marketDescriptionConstants } from '@app/lazy-modules/racingConstants/racing.constants';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { IStreamBetWeb } from '@app/core/services/cms/models/system-config';
import { EventVideoStreamProviderService } from '@lazy-modules/eventVideoStream/components/eventVideoStream/event-video-stream-provider.service';
import { SessionStorageService } from '@core/services/storage/session-storage.service';
@Component({
  selector: 'racing-event-main-component',
  templateUrl: './racing-event-main.component.html'
})
export class RacingEventMainComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  eventData: ISportEvent[];

  racingName: string;
  images: string;
  racingTypeNames: string[];
  racingInMeeting: ISportEvent[];
  selectedTypeName: string;
  selectedMarketPath: string | null;
  selectedMarketTypePath: string | null;
  eventEntity: ISportEvent;
  streamControl: any;
  presimStopTrackInterval: number;
  filter: string;
  racingsMap: any;
  racingEdpReady: boolean = false;
  eventId: string;
  origin: string;
  meetingsTitle: any;
  isHorseRacingScreen: boolean;
  loadFloatingMsgComp: boolean = false;
  quickNavigationItems: IGroupedSportEvent[];
  sportEventsData: ISportEvent[];
  private autoSeoData: IAutoSeoData = {};
  isDesktop: boolean;
  isStreambetAvailable: boolean;
  streamBetCmsConfig: IStreamBetWeb
  private isOutright: boolean;
  private nativePlayerCloseHandler: null | EventListenerOrEventListenerObject = null;
  private eventTypeName: string;
  private racingConfiguration: IInitialSportConfig;
  private editMyAccaUnsavedOnEdp: boolean;

  private readonly IMAGES_ENDPOINT: string = environment.IMAGES_ENDPOINT;
  private paramsSubscriber: Subscription;
  private getEventsSubscription: Subscription;
  private eventSubscription: Subscription;
  private readonly Outright: string = 'Outright';
  private readonly tagName: string = 'racingEventMain';
  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private timeService: TimeService,
    private templateService: TemplateService,
    private command: CommandService,
    private nativeBridge: NativeBridgeService,
    private deviceService: DeviceService,
    private routesDataSharingService: RoutesDataSharingService,
    private windowRef: WindowRefService,
    private horseRacingService: HorseracingService,
    private greyhoundService: GreyhoundService,
    private routingState: RoutingState,
    private smartBoostsService: SmartBoostsService,
    private cmsService: CmsService,
    private nextRacesService: NextRacesService,
    protected eventService: EventService,
    private extraPlaceService: ExtraPlaceService,
    private pubSubService: PubSubService,
    private changeDetectorRef: ChangeDetectorRef,
    private routingHelperService: RoutingHelperService,
    private eventVideoStreamProviderService: EventVideoStreamProviderService,
    private sessionStorageService: SessionStorageService
  ) {
    super();
  }

  ngOnInit(isReInit?: boolean): void {
    const segment = this.routingState.getCurrentSegment();
    this.isHorseRacingScreen = segment.indexOf('horseracing') >= 0;

    const
      racingService = this.racingService,
      isHR = racingService.getConfig().name === 'horseracing';

    this.paramsSubscriber = this.route.params.pipe(concatMap((params: Params) => {
      this.racingEdpReady = false;
      this.origin = this.route.snapshot.queryParams.origin || '';
      if (!isReInit) {
        this.selectedMarketPath = params.market || null;
        this.selectedMarketTypePath = params.marketType || null;
      }

      if (!this.state.loading) { this.showSpinner(); }
      // unSubscription from liveServe PUSH updates
      this.racingService.unSubscribeEDPForUpdates();

      this.changeDetectorRef.detectChanges();

      if (isHR) {
        return racingService.getById(params.id, false);
      } else {
        return racingService.getGreyhoundEvent(params.id, false);
      }
    }))
      .subscribe((eventData: ISportEvent[]) => {

        this.eventData = eventData;
        eventData.length && eventData[0].categoryId == '21' && this.setDrillTagName();
        this.pubSubService.publish(this.pubSubService.API.QUICKBET_EXTRAPLACE_SELECTION,eventData[0]);
        this.isDesktop = this.deviceService.isDesktop;

        this.addConnectListeners();

        if (typeof this.eventData === 'undefined' || (this.eventData && !this.eventData.length)) {
          this.racingEdpReady = true;
          this.hideSpinner();
          return;
        }

        this.racingsMap = null;
        this.images = this.IMAGES_ENDPOINT;

        this.eventId = this.route.snapshot.params['id'];
        this.racingInMeeting = [];

        // Don`t hide sport header on HR EDP and GH EDP after app is scrolled down to the footer
        this.routesDataSharingService.updatedHasSubHeader(true);

        this.racingConfiguration = this.racingService.getGeneralConfig();
        this.meetingsTitle = this.racingConfiguration.sectionTitle;
        this.presimStopTrackInterval = this.racingConfiguration.PRESIM_STOP_TRACK_INTERVAL;
        this.racingName = this.racingService.getConfig().name;
        this.eventEntity = this.racingService.sortMarketsName(this.eventData[0], horseracingConfig.MARKETS_NAME_SORT_ORDER);
        this.racingAutoseoData();
        this.eventEntity.isVirtual = this.eventEntity.typeFlagCodes && this.eventEntity.typeFlagCodes.toLowerCase().indexOf('vr') > -1;
        this.eventTypeName = this.eventEntity.typeName;
        this.selectedTypeName = this.eventTypeName;

        // Subscription for liveServe PUSH updates
        this.racingService.subscribeEDPForUpdates(this.eventEntity);
        this.eventVideoStreamProviderService.getStreamBetCmsConfig().subscribe((streamBetWeb: IStreamBetWeb) => {
          this.streamBetCmsConfig = streamBetWeb;
          const streamBetConfig = {
            streamBetCmsConfig: this.streamBetCmsConfig,
            isMobile: this.deviceService.isMobile,
            isTablet: this.deviceService.isTabletOrigin,
            isDesktop: this.deviceService.isDesktop,
            providerInfo: this.eventEntity.streamProviders,
            categoryId: this.eventEntity.categoryId,
            isIHR: this.eventEntity.drilldownTagNames?.includes(marketDescriptionConstants.EVFLAG_IHR)
          };
          // Set state of video play button on wrapper
          if (this.eventEntity.liveStreamAvailable && this.eventVideoStreamProviderService.isStreamBetAvailable(streamBetConfig, this.tagName)) {
            this.isStreambetAvailable = true;
          }
          else {
            if (this.deviceService.isWrapper) {
              if (this.eventEntity.liveStreamAvailable) {
                this.nativeBridge.onEventDetailsStreamAvailable({
                  categoryId: Number(this.eventEntity.categoryId),
                  classId: Number(this.eventEntity.classId),
                  typeId: Number(this.eventEntity.typeId),
                  eventId: Number(this.eventEntity.id)
                });
              }
            }
          }
        });

        // This object allows to call methods inside the stream directives.
        // If directive is not available 'no operation' will be performed.
        this.streamControl = {
          externalControl: true,
          playLiveSim: _.noop,
          playStream: _.noop,
          hideStream: _.noop
        };

        // Sort racing markets by tabs
        this.eventEntity.sortedMarkets = this.racingService.sortRacingMarketsByTabs(this.eventEntity.markets, this.eventId);

        this.transformSmartBoostsMarkets(this.eventEntity.markets);

        // *** Meeting selector Data functionality - start ***
        let mSEventsMethodName = 'getTypeNamesEvents'; // meeting Selector Events Method Name
        // attributes object for meeting Selector Events Method
        const mSEventsOptions: IEventsOptions = { selectedTab: this.timeService.determineDay(this.eventEntity.startTime, true) };

        if (this.racingName === 'horseracing') {
          mSEventsOptions.selectedTab = 'featured';
          mSEventsOptions.additionalEventsFromModules = [this.command.API.HR_ENHANCED_MULTIPLES_EVENTS];
          mSEventsOptions.filterByDate = this.origin && this.origin.includes('offers') ? '' : this.eventEntity.startTime;
        }

        if (this.racingName === 'horseracing' && /EVFLAG_AP/g.test(this.eventEntity.drilldownTagNames)) { // HR AntepostEvent
          mSEventsMethodName = 'getAntepostEventsByFlag';
          mSEventsOptions.drilldownTagNames = this.eventEntity.drilldownTagNames;
        }

        if (!this.deviceService.isDesktop && this.eventEntity && this.eventEntity.drilldownTagNames
            && this.eventEntity.drilldownTagNames.includes(marketDescriptionConstants.EVFLAG_IHR)) {
          this.loadFloatingMsgComp = true;
        } else {
          this.loadFloatingMsgComp = false;
        }

        this.getEventsSubscription = observableFrom(this.racingService[mSEventsMethodName](mSEventsOptions)).pipe(
          switchMap((response: ICombinedSportEvents) => {
            this.racingsMap = response.groupedByMeetings;
            this.racingTypeNames = _.sortBy(Object.keys(this.racingsMap).slice(0));
            this.quickNavigationItems = response.groupedByFlagAndData;
            this.sportEventsData = response.sportEventsData;
            return this.isHorseRacingScreen ? observableFrom(this.extraPlaceService.getEvents()) : of([]);
          }),
          switchMap((exPlaceRaces: ISportEvent[]) => {
            if (this.quickNavigationItems.length && this.isHorseRacingScreen) {
              const enhancedEvents: ICombinedSportEvents = this.racingService.navMenuGroupEnhancedRaces(exPlaceRaces);
              this.quickNavigationItems.unshift(enhancedEvents.groupedByFlagAndData[0]);
            }

            if (this.origin && this.origin.includes('offers')) {
              return this.getEventsByTimeAndStatus(this.sportEventsData);
            } else if (this.isNextRaceEvent()) {
              return this.cmsService.getSystemConfig();
            }
            return of(this.racingsMap[this.selectedTypeName]);
          }),
          switchMap((data: ISystemConfig | ISportEvent[]) => {
            if (data && (data as ISystemConfig).NextRaces) {
              const nextRacesConfig = this.nextRacesService.getNextRacesModuleConfig(this.racingName, data as ISystemConfig);
              return observableFrom(this.eventService.getNextEvents(nextRacesConfig));
            }
            return of(data as ISportEvent[]);
        /* eslint-disable */
        })).subscribe((nextRacesData: ISportEvent[]) => {
          if(nextRacesData && nextRacesData.length && nextRacesData.findIndex(res => res.id == this.eventData[0].id) == -1) {
            const resultsUrl = this.formEdpUrl(nextRacesData[0]);
            this.router.navigateByUrl(resultsUrl);
          }
          this.edpReady(nextRacesData);
          }, () => {
          this.showError();
        });
        // **** Meeting selector Data functionality - end ***

        this.getTerms(this.eventEntity);

        if (this.deviceService.isWrapper) {
          // Set button active if native player is already opened
          this.filter = this.nativeBridge.playerStatus ? 'showVideoStream' : 'hideStream';
          // Listen to native player close event
          this.nativePlayerCloseHandler = (e: CustomEvent) => {
            this.filter = e.detail.settingValue ? 'showVideoStream' : 'hideStream';
          };
          this.windowRef.document.addEventListener('CURRENT_WATCH_LIVE_STATE_CHANGED', this.nativePlayerCloseHandler);
        }
        this.hideSpinner();
      }, () => {
        this.addConnectListeners();
        this.showError();
      });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.CHANGE_MARKET, (marketPath: string) => {
      this.selectedMarketPath = marketPath;
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.CHANGE_BET_FILTER, (betFilter: string) => {
      this.selectedMarketTypePath = betFilter;
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.EMA_UNSAVED_ON_EDP, (unsaved: boolean) => {
      this.editMyAccaUnsavedOnEdp = unsaved;
    });
    this.eventSubscription = this.eventService.hrEventSubscription.subscribe(flag => {
      if(flag) {
        this.reloadComponent();
        this.eventService.hrEventSubscription.next(false);
      }
    })
  }

  formEdpUrl(eventEntity: ISportEvent): string {
    return `${this.routingHelperService.formEdpUrl(eventEntity)}?origin=${this.origin}`;
  }
  getEventsByTimeAndStatus(events: ISportEvent[]) {
    let eventsData: ISportEvent[] =  events.filter((event: ISportEvent) => {
      // Event is Open (not finished or resulted, not live event and does not have raceStage)
      const isOpen = event.raceStage !== 'O' && event.rawIsOffCode !== 'Y' && !event.isFinished && !event.isResulted;
      return event.markets.length && isOpen && (this.isEPR(event) || this.isITV(event));
    });
    return of(eventsData);
  }

  private isEPR(event: ISportEvent): boolean {
    return event.markets[0].drilldownTagNames && event.markets[0].drilldownTagNames.includes('MKTFLAG_EPR');
  }

  /**
   * ITV Event (Event Level)
   * @param event
   */
  private isITV(event: ISportEvent): boolean {
    return event.drilldownTagNames && event.drilldownTagNames.includes('EVFLAG_FRT');
  }

  addConnectListeners(): void {
    // listen to view type change
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.DEVICE_VIEW_TYPE_CHANGED_NEW, () => {
      this.isDesktop = this.deviceService.isDesktop;
    });

    // listen to becoming online
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.RELOAD_COMPONENTS, () => {
      this.reloadComponent();
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.SUCCESSFUL_LOGIN, () => {
      this.filter = 'hideStream';
    });
  }

  ngOnDestroy(): void {
    // unSubscription from liveServe PUSH updates
    this.racingService.unSubscribeEDPForUpdates();
    this.pubSubService.unsubscribe(this.tagName);

    if (this.nativePlayerCloseHandler) {
      this.windowRef.document.removeEventListener('CURRENT_WATCH_LIVE_STATE_CHANGED', this.nativePlayerCloseHandler);
    }

    this.paramsSubscriber && this.paramsSubscriber.unsubscribe();
    this.getEventsSubscription && this.getEventsSubscription.unsubscribe();
    this.eventSubscription && this.eventSubscription.unsubscribe();
  }

  /**
   * Check if edit my acca is in progress for changing route
   * @returns {boolean}
   */
  canChangeRoute(): boolean {
    this.pubSubService.publish(this.pubSubService.API.ROUTE_CHANGE_STATUS, !this.editMyAccaUnsavedOnEdp);
    return !this.editMyAccaUnsavedOnEdp;
  }

  /**
   * open edit my acca pop-up if edit is in progress while changing route
   */
  onChangeRoute(): void {
    this.pubSubService.publish(this.pubSubService.API.EMA_OPEN_CANCEL_DIALOG);
  }

  /**
   * Click on Horse Block.
   *
   * Toggle Horse Information Area.
   *
   * param {array} summary of expanded and collapsed areas.
   * param {number} market index.
   * param {number} outcome index.
   *
   */
  onExpand(expandedSummary, mIndex, oIndex) {
    const temp = !expandedSummary[mIndex][oIndex];

    for (let i = 0; i < expandedSummary[mIndex].length; i++) {
      expandedSummary[mIndex][i] = false;
    }

    expandedSummary[mIndex][oIndex] = temp;
  }

  reloadComponent(): void {
    this.showSpinner();
    this.paramsSubscriber.unsubscribe();
    this.ngOnDestroy();
    this.ngOnInit(true);
  }

  private get racingService(): HorseracingService | GreyhoundService {
    return this.isHorseRacingScreen ? this.horseRacingService : this.greyhoundService;
  }
  private set racingService(value: HorseracingService | GreyhoundService){}
  private edpReady(events: ISportEvent[]) {
    this.racingInMeeting = _.sortBy(events, 'startTime');
    this.racingEdpReady = true;
  }

  private getTerms(event: ISportEvent): void {
    _.each(event.markets, (market: IMarket) => {
      market.terms = this.templateService.genTerms(market);
    });
  }

  /**
   * format smartBoosts markets
   * @param {IMarket[]} markets
   */
  private transformSmartBoostsMarkets(markets: IMarket[]): void {
    _.each(markets, (market: IMarket) => {
      market.isSmartBoosts = this.smartBoostsService.isSmartBoosts(market);

      if (!market.isSmartBoosts) { return; }

      _.each(market.outcomes, (outcome: IOutcome) => {
        const parsedName = this.smartBoostsService.parseName(outcome.name);
        if (!parsedName.wasPrice) { return; }

        outcome.name = parsedName.name;
        outcome.wasPrice = parsedName.wasPrice;
      });
    });
  }

  private isNextRaceEvent(): boolean {
    return (this.origin && this.eventEntity.isStarted === undefined);
  }
  /**
  * Assigns autoSeoData object and publish the data for racing sport-autoseo
  */
  private racingAutoseoData(): void {
    this.isOutright = this.eventEntity.markets[0].templateMarketName == this.Outright;
    this.autoSeoData.isOutright = this.isOutright;
    this.autoSeoData.categoryName = this.eventEntity.categoryName;
    this.autoSeoData.typeName = this.eventEntity.typeName;
    this.autoSeoData.name = this.eventEntity.name;
    this.pubSubService.publish(this.pubSubService.API.AUTOSEO_DATA_UPDATED, [this.autoSeoData]);
  }

  /**
   * checkDrillDownTagName to default set tab
   * in overlay switcher
   */
  
  private setDrillTagName(): void {
    const regexp = /EVFLAG_FT|EVFLAG_IT|EVFLAG_NH/g;
    const flagKey = this.eventData[0].drilldownTagNames && this.eventData[0].drilldownTagNames.match(regexp);
    flagKey && this.sessionStorageService.set('selectedFutureTab', flagKey[0]);
  }
}