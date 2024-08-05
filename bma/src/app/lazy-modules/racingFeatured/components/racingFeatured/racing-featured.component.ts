import { Input, Component, ChangeDetectorRef, OnInit, OnDestroy, Output, EventEmitter, OnChanges } from '@angular/core';
import { Router } from '@angular/router';

import { Subscription } from 'rxjs';

import { FeaturedModuleComponent } from '@app/featured/components/featured-module/featured-module.component';

import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { TemplateService } from '@shared/services/template/template.service';
import { FeaturedModuleService } from '@featured/services/featuredModule/featured-module.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CommentsService } from '@core/services/comments/comments.service';
import { WsUpdateEventService } from '@core/services/wsUpdateEvent/ws-update-event.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { PromotionsService } from '@promotions/services/promotions/promotions.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { UserService } from '@core/services/user/user.service';
import { EventService } from '@app/sb/services/event/event.service';
import { VirtualSharedService } from '@shared/services/virtual/virtual-shared.service';
import { RacingGaService } from '@racing/services/racing-ga.service';
import { StorageService } from '@core/services/storage/storage.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IRaceGridMeeting } from '@core/models/race-grid-meeting.model';
import { ISystemConfig } from '@core/services/cms/models';
import { IFeaturedModel } from '@featured/models/featured.model';

import { defaultModules, FLAGS } from './constant';
import { HorseracingService } from '@coreModule/services/racing/horseracing/horseracing.service';
import { GreyhoundService } from '@coreModule/services/racing/greyhound/greyhound.service';
import { RoutingState } from '@shared/services/routingState/routing-state.service';
import { BuildUtilityService } from '@core/services/buildUtility/build-utility.service';
import environment from '@environment/oxygenEnvConfig';
import { TimeService } from '@core/services/time/time.service';
import { IOutputModule } from '@featured/models/output-module.model';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { horseracingConfig } from '@app/core/services/racing/config/horseracing.config';
import { greyhoundConfig } from '@app/core/services/racing/config/greyhound.config';
import { DeviceService } from '@app/core/services/device/device.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';
import { ISportConfigTab } from '@app/core/services/cms/models';
import { VirtualEntryPointsService } from '@app/racing/services/virtual-entry-points.service';

@Component({
  selector: 'racing-featured',
  templateUrl: './racing-featured.component.html'
})
export class RacingFeaturedComponent extends FeaturedModuleComponent implements OnInit, OnDestroy, OnChanges {
  @Input() racing: IRaceGridMeeting;
  @Input() sectionTitle: Object;
  @Input() responseError?;
  @Input() sportName: string;
  @Input() eventsOrder: string[];
  @Input() filter: string;
  @Input() displayNextRaces: boolean;
  @Input() sportModule: string;
  @Input() isExtraPlaceAvailable: boolean;
  @Input() offersAndFeaturedRacesTitle: string;
  @Input() display?: string;
  @Input() hostContext: string;
  @Input() compName: string;
  @Output() readonly featuredLoaded: EventEmitter<IRaceGridMeeting> = new EventEmitter();
  @Output() readonly nextRacesLoaded: EventEmitter<void> = new EventEmitter();

  isTotePoolsAvailable: boolean = false;
  isHorseracingVirtualsEnabled: boolean = false;
  races: {[key: string]: Partial<IRaceGridMeeting> & {racingType: string}};
  sysConfigSubscription: Subscription;
  noEvents: boolean;
  invokeFeatured: boolean = true;
  allEvents: ISportEvent[] = [];
  reloadEventsModule: boolean;
  inspiredVirtualsDataReady: boolean;
  showFeaturedModules: boolean = false;
  isExtraPlaceDataAvailable: boolean = false;
  modulesTmp: IOutputModule[] = [];
  private readonly HORSE_RACING_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;
  private eventsForSchema: ISportEvent[];
  private schemaUrlsConfig = [
    '/horse-racing',
    '/greyhound-racing',
    horseracingConfig.tabs[0].url,
    greyhoundConfig.tabs[0].url,
    greyhoundConfig.tabs[1].url
  ];
  private schemaUrl: string;
  private readonly RACING_TODAY:string = 'racing.today';
  private readonly SB_TODAY:string = 'sb.today';
  private readonly RACING_TOMMOROW: string = 'racing.tomorrow';
  private readonly SB_TOMMOROW: string = 'sb.tomorrow';
  
  bannerBeforeAccorditionHeader: string;
  targetTab: ISportConfigTab;
  lastBannerEnabled:boolean;
  accorditionNumber:number;

  constructor(
    protected locale: LocaleService,
    protected filtersService: FiltersService,
    protected windowRef: WindowRefService,
    protected pubsub: PubSubService,
    protected featuredModuleService: FeaturedModuleService,
    protected templateService: TemplateService,
    protected commentsService: CommentsService,
    protected wsUpdateEventService: WsUpdateEventService,
    protected sportEventHelper: SportEventHelperService,
    protected cmsService: CmsService,
    protected promotionsService: PromotionsService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected routingHelperService: RoutingHelperService,
    public router: Router,
    public gtmService: GtmService,
    protected awsService: AWSFirehoseService,
    public user: UserService,
    public eventService: EventService,
    protected virtualSharedService: VirtualSharedService,
    private racingGaService: RacingGaService,
    protected storage: StorageService,
    private horseRacingService: HorseracingService,
    private greyhoundService: GreyhoundService,
    private routingState: RoutingState,
    private buildUtilityService: BuildUtilityService,
    private timeService: TimeService,
    protected deviceService: DeviceService,
    protected bonusSuppressionService: BonusSuppressionService,
    protected vEPService : VirtualEntryPointsService
  ) {
    super(
      locale, filtersService, windowRef, pubsub, featuredModuleService, templateService, commentsService,
      wsUpdateEventService, sportEventHelper, cmsService, promotionsService, changeDetectorRef, routingHelperService,
      router, gtmService, awsService, user, eventService, virtualSharedService, bonusSuppressionService, deviceService, storage
    );
  }

  ngOnInit(): void {
    super.ngOnInit();
    this.sysConfigSubscription = this.cmsService.getSystemConfig()
      .subscribe((config: ISystemConfig) => {
        this.isHorseracingVirtualsEnabled = this.setHorseracingVirtualSportsSwitcher(config);
        this.isTotePoolsAvailable = this.setIntTotePool(config)
          && Number(this.sportId) === Number(environment.CATEGORIES_DATA.racing.horseracing.id);
      });
      if(!this.displayNextRaces){
        this.pubsub.publish(this.pubsub.API.RACING_NEXT_RACES_LOADED, true);
        this.showFeaturedModules = true;
      }      

    this.vEPService.targetTab.subscribe((tab: ISportConfigTab | null) => {
      this.targetTab = tab;
      this.changeDetectorRef.detectChanges();
    });

    this.vEPService.lastBannerEnabled.subscribe((lbe: boolean) => {
      this.lastBannerEnabled = lbe;
    });
  
    this.vEPService.accorditionNumber.subscribe((accNum: number) => {
      this.accorditionNumber = accNum;
    });
  }

  ngOnChanges(changes): void {
    if (changes.display && !changes['display'].firstChange) {
      this.reloadEventsModule = true;
      this.changeDetectorRef.detectChanges();
      this.removeSchemaForHRGHEvents();
      this.groupEvents();
    }
  }


  ngOnDestroy(): void {
    super.ngOnDestroy();
    this.racingGaService.reset();
    this.sysConfigSubscription && this.sysConfigSubscription.unsubscribe();
    this.removeSchemaForHRGHEvents();
  }

  setIntTotePool(config: ISystemConfig): boolean {
    if (config.InternationalTotePool && config.InternationalTotePool.Enable_International_Totepools) {
      return config.InternationalTotePool.Enable_International_Totepools;
    } else {
      return false;
    }
  }

  /**
   * Set horseracing Virtual Sports Switcher
   * @params {Object} config
   */
  setHorseracingVirtualSportsSwitcher(config: ISystemConfig): boolean {
    if (config.VirtualSports && config.VirtualSports['virtual-horse-racing']) {
      return config.VirtualSports['virtual-horse-racing'];
    } else {
      return false;
    }
  }

  trackModule(moduleName: string, sport: string): void {
    this.racingGaService.trackModule(moduleName, sport);
  }

  reloadComponent(): void {
    this.ngOnDestroy();
    this.ngOnInit();
  }

  init(featured: IFeaturedModel): void {
    this.inspiredVirtualsDataReady = false;

    super.init(featured);
    this.noEvents = true;

    const racingEventsModules = this.featuredModuleData.modules.filter((module) => module['@type'] === 'RacingEventsModule');
    if (!racingEventsModules.length) {
      this.loadDefaultModules();  // ss-request
      this.showFeaturedModules = true;
    } else {
      this.groupEvents(true);
    }
  }

  handleNextRacesLoaded(): void {
    this.nextRacesLoaded.emit();
    if(this.invokeFeatured && !this.deviceService.isDesktop){
      this.invokeFeatured = false;
      this.pubsub.publish(this.pubsub.API.RACING_NEXT_RACES_LOADED, true);
      this.windowRef.nativeWindow.setTimeout(() => {
        this.showFeaturedModules = true;
        this.changeDetectorRef.detectChanges();
         }, 1500);               
    }
  }  

  handleErrorOnFirstLoad(): void {
    super.handleErrorOnFirstLoad();
    this.loadDefaultModules();
  }

  /**
   * Operations on module update receiving
   * @param {Object} data
   */
  onModuleUpdate(data: IOutputModule): void {
    super.onModuleUpdate(data);
    this.groupEvents(true);
  }

  protected isSimpleModule(module): boolean {
    return super.isSimpleModule(module) || module['@type'] === 'RacingEventsModule' ||
      module['@type'] === 'InternationalToteRaceModule' || module['@type'] === 'VirtualRaceModule';
  }

  private get racingService(): HorseracingService | GreyhoundService {
    const segment = this.routingState.getCurrentSegment();

    return segment.indexOf('horseracing') >= 0 ? this.horseRacingService : this.greyhoundService;
  }

  private set racingService(value: HorseracingService | GreyhoundService){}

  private groupEvents(isMS: boolean = false): void {
    this.inspiredVirtualsDataReady = this.featuredModuleData.modules.some(module => {
      if (module['@type'] === 'VirtualRaceModule') {
        this.vEPService.virtualMarketName = module.title;
      }
      return module['@type'] === 'VirtualRaceModule'
    });
    const racingEventsModules = this.featuredModuleData.modules.filter((module) => module['@type'] === 'RacingEventsModule');

    this.races = {};
    this.allEvents = [];
    racingEventsModules.forEach((module) => {
      this.noEvents = this.noEvents && !module.data.length;
      const config = this.racingService.getConfig().request;
      if (isMS) {
        module.data = module.data.map((event) => this.buildUtilityService.msEventBuilder(event));
      }
      const filteredData = module.data.filter(event => this.display ? event.correctedDay === `sb.${this.display}` : event);
      this.allEvents.push(...filteredData);
      this.eventService.addAvailability(filteredData);
      this.racingService.addLpAvailableProp(filteredData);
      this.racingService.addPersistentInCacheProp(filteredData, config.date);
      this.races[module._id] = this.racingService.groupByFlagCodesAndClassesTypeNames(filteredData) as any;
      this.races[module._id].racingType = module.racingType;
      ['groupedRacing', 'classesTypeNames'].forEach(key => this.racing[key] = this.races[module._id][key]);
    });
    
    // GH only
    // On greyhounds, when filter is by-time, we display all events.
    // This part is just to get any available racing module with events from FEATURED MS
    // and display all events as a single racing-events component

    if(this.filter === 'by-time') {
      let racingModulesCounter = 0;
      this.featuredModuleData.modules = this.featuredModuleData.modules.reduce((acc, val) => {
        if(val['@type'] === 'RacingEventsModule' && racingModulesCounter < 1 ) {
          racingModulesCounter += 1;
          acc.push(val);
         } else if(val['@type'] !== 'RacingEventsModule') {
          acc.push(val);
         }
         
        return acc;
      }, []);
    }

    this.racing.events = this.allEvents.slice();
    this.pubsub.publish(this.pubsub.API.RACING_NEXT_RACES_LOADED, true);
    this.isExtraPlaceDataAvailable= true;
    this.changeDetectorRef.detectChanges();
    this.changeDetectorRef.markForCheck();

    // Save titles and available modules to display them properly on quick-navigation (EDP)

    const titlesMap: {[key: string]: string} = {};
    this.featuredModuleData.modules.filter(module => module['@type'] === 'RacingEventsModule')
      .forEach((module) => titlesMap[module.racingType] = module.title);
    this.storage.set('racingFeatured', titlesMap);
    if (this.racingService.config.request.categoryId === this.HORSE_RACING_CATEGORY_ID) {
      this.sortIntRaces();
    }
    this.featuredLoaded.emit(this.racing);
    this.reloadEventsModule = false;
    this.deviceService.isRobot() && this.schemaForHRGHEvents(this.allEvents);
  }

  private loadDefaultModules(): void {
    this.racingService.todayEventsByClasses(true).then((data) => {
      const vrc = this.featuredModuleData.modules.find(
        module => module['@type'] === 'VirtualRaceModule' && module.data && module.data[0]
          && module.data[0]['@type'] === 'VirtualRaceModuleData'
      );

      this.featuredModuleData.modules = [...defaultModules];

      if (vrc) {
        const vrcModuleIndex = this.featuredModuleData.modules.findIndex(module => module['@type'] === 'VirtualRaceModule');
        this.featuredModuleData.modules[vrcModuleIndex] = vrc;
      }

      this.featuredModuleData.modules.find(module => module._id === '1').data =
      data.groupedRacing.find(race => race.flag === FLAGS.UK) && data.groupedRacing.find(race => race.flag === FLAGS.UK).data || [];

      this.featuredModuleData.modules.find(module => module._id === '2').data =
      data.groupedRacing.find(race => race.flag !== FLAGS.UK && race.flag !== FLAGS.VR) &&
      data.groupedRacing.filter(race => race.flag !== FLAGS.UK && race.flag !== FLAGS.VR)
                        .map((race) => race.data ).reduce((acc, val) => acc.concat(val), []) || [];

      this.featuredModuleData.modules.find(module => module._id === '3').data =
      data.groupedRacing.find(race => race.flag === FLAGS.VR) && data.groupedRacing.find(race => race.flag === FLAGS.VR).data || [];

      this.groupEvents();
    });
  }
  // Sort Int races (BMA-49338)
  private sortIntRaces(): void {
    const currentDay = this.timeService.getDayI18nValue(new Date().toString()).split('.');
    const intRaces = Object.values(this.races).find(meeting => meeting.racingType === 'IR') as IRaceGridMeeting;
    this.racingService.sortRaceGroup(intRaces, `racing.${currentDay[1]}`);
  }
  /**
   * schema for Horse Racing and Grey Hounds Events
   * @param races ISportEvent[]
   */
  private schemaForHRGHEvents(races: ISportEvent[]) {
    let schemaConfig: string[];
    this.schemaUrl = this.schemaUrlsConfig.find((url:string)=> url === this.router?.url);
    const isHR: boolean = this.sportName === horseracingConfig.config.name;
    if (this.schemaUrl) {
      const sortedRaces = this.racingService.groupByFlagCodesAndClassesTypeNames(races);
      const ukraces: ISportEvent[] = sortedRaces?.groupedRacing?.find(race => race && race.flag === FLAGS.UK)?.data;
      this.cmsService.getSystemConfig().subscribe((sysConfig: ISystemConfig) => {
        schemaConfig = sysConfig?.SeoSchemaConfig?.schemaConfig
      });
      this.eventsForSchema = ukraces?.filter((event: ISportEvent) => {
        if (schemaConfig?.length === 1) {
          if (schemaConfig.includes('today')) {
            return isHR ? event.correctedDayValue === this.RACING_TODAY : event.correctedDay === this.SB_TODAY;
          }
          if (schemaConfig.includes('tomorrow')) {
            return isHR ? event.correctedDayValue === this.RACING_TOMMOROW : event.correctedDay === this.SB_TOMMOROW;
          }
        }
        if (schemaConfig?.length > 1) {
          return isHR ? (event.correctedDayValue === this.RACING_TODAY || event.correctedDayValue === this.RACING_TOMMOROW) : (event.correctedDay === this.SB_TODAY || event.correctedDay === this.SB_TOMMOROW);
        }
      });
      this.eventsForSchema?.forEach((event: ISportEvent) => {
        const edpUrl: string = event && this.routingHelperService.formEdpUrl(event);
        event.url = edpUrl && edpUrl.replace('/', '');
      });
      this.eventsForSchema && this.pubsub.publish(this.pubsub.API.SCHEMA_DATA_UPDATED, [this.eventsForSchema, this.schemaUrl]);
    }
  }
  /**
   * to remove the schemaScript
   */
  private removeSchemaForHRGHEvents(): void {
    this.deviceService.isRobot() && this.schemaUrl && this.pubsub.publish(this.pubsub.API.SCHEMA_DATA_REMOVED, this.schemaUrl);
  }



} 
