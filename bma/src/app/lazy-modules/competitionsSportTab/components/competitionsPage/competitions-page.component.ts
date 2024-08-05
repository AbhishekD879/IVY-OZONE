import {
  AfterViewInit,
  ChangeDetectorRef,
  Component,
  ElementRef,
  OnDestroy,
  OnInit,
  Renderer2,
  ViewChild
} from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { from, Observable, Subscription } from 'rxjs';
import { map, concatMap, mergeMap } from 'rxjs/operators';
import * as _ from 'underscore';

import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { StorageService } from '@core/services/storage/storage.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { CurrentMatchesService } from '@sb/services/currentMatches/current-matches.service';
import { UpdateEventService } from '@core/services/updateEvent/update-event.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { COMPETITIONS_TABS } from '@lazy-modules/competitionsSportTab/contstants/competitions.constant';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { ISportEvent } from '@core/models/sport-event.model';
import { IStatsSeasonMatchSeason } from '@app/stats/models/season-match/season.model';
import { ICompetitionCategory } from '@lazy-modules/competitionsSportTab/components/competitionsSportTab/competitions.model';
import { IGroupedByDateItem, IGroupedByDateObj, ITypeSegment } from '@app/inPlay/models/type-segment.model';
import {
  ICompetitionPage,
  ICompetitionPageTab
} from '@lazy-modules/competitionsSportTab/components/competitionsPage/competitions-page.model';
import { ICompetitionsConfig } from '@core/services/cms/models/system-config';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { GamingService } from '@core/services/sport/gaming.service';
import { ISportConfig, ISportTabs } from '@app/core/services/cms/models';
import { ILazyComponentOutput } from '@shared/components/lazy-component/lazy-component.model';
import { ICompetitionFilter } from '@lazy-modules/competitionFilters/models/competition-filter';
import { CompetitionFiltersService } from '@lazy-modules/competitionFilters/services/competitionFilters/competition-filters.service';
import { IAutoSeoData } from '@app/core/services/cms/models/seo/seo-page.model';
import { ISportConfigTab } from '@app/core/services/cms/models';
import { RoutingHelperService } from '@app/core/services/routingHelper/routing-helper.service';
import { DeviceService } from '@app/core/services/device/device.service';

@Component({
  selector: 'competitions-page',
  templateUrl: 'competitions-page.component.html'
})
export class CompetitionsPageComponent extends AbstractOutletComponent implements OnInit, OnDestroy, AfterViewInit {

  @ViewChild('competitionsHeader', {static: true}) competitionsHeader: ElementRef;
  @ViewChild('competitionsList', {static: true}) competitionsList: ElementRef;

  mainCategories: ICompetitionCategory[] = [];
  allCategories: ICompetitionCategory[] = [];
  allCategoriesClasses: string[];
  competitionTabs: ICompetitionPageTab[] = [];
  showSwitchers: boolean = false;
  isShowCompetitions: boolean = false;
  isOnHomePage: boolean = false;
  isLoaded: boolean = false;
  showSpinnerInDropdown: boolean;
  typeName: string;
  typeId: string;
  classId: string;
  sportName: string;
  sportId: string | number;
  seasonId: string;
  sportDefaultPath: string;
  titleIconSvg: string;
  titleIconSvgId: string;
  leaguesLink: string;
  eventsByCategory: ITypeSegment;
  eventsByCategoryCopy: ITypeSegment;
  groupedByDate: IGroupedByDateObj;
  outrights: ISportEvent[];
  activeTab: { id: string; name: string } = {
    id: 'tab-competition-matches',
    name: 'matches'
  };
  isTierOne: boolean;
  sport: GamingService;

  timeFilter: ICompetitionFilter;
  competitionFilters: ICompetitionFilter[] = [];
  isSportEventFiltersEnabled: boolean;
  displayFilters = false;

  protected readonly window: any;
  private document: any;
  private resizeListener: Function;

  private rawCompetitionTabs: ICompetitionPageTab[] = [];
  private detectListener: number;
  private getDataSubscription: Subscription;
  private pClassName: string;
  private pTypeName: string;
  private sportsConfigSubscription: Subscription;
  private cmsConfigSubscription: Subscription;
  private autoSeoData: IAutoSeoData = { name: '' };
  targetTab: ISportConfigTab;
  private competitionUrl: string;
  constructor(
    private activatedRoute: ActivatedRoute,
    private currentMatchesService: CurrentMatchesService,
    private filterService: FiltersService,
    private commandService: CommandService,
    private windowRef: WindowRefService,
    private cmsService: CmsService,
    protected renderer: Renderer2,
    private storageService: StorageService,
    private router: Router,
    private changeDetectorRef: ChangeDetectorRef,
    private pubsubService: PubSubService,
    private domToolsService: DomToolsService,
    private sportsConfigService: SportsConfigService,    
    private competitionFiltersService: CompetitionFiltersService,
    private routingHelperService: RoutingHelperService,
    private deviceService: DeviceService,
    // eslint-disable-next-line
    private updateEventService: UpdateEventService // needed for events subscription on init of this dependency
  ) {
    super()/* istanbul ignore next */;
    this.isOnHomePage = _.isEmpty(this.activatedRoute.snapshot.params);
    this.sportName = this.activatedRoute.snapshot.paramMap.get('sport');
    this.mainCategories = this.storageService.get(`competitionsMainClasses_${this.sportName}`);
    this.allCategoriesClasses = this.storageService.get(`competitionsAZClasses_${this.sportName}`);

    this.sportDefaultPath = `sport/${this.sportName}/competitions`;
    this.window = this.windowRef.nativeWindow;
    this.document = this.windowRef.document;
  }

  ngOnInit(): void {
    this.changeDetectorRef.detach();
    this.detectListener = this.windowRef.nativeWindow.setInterval(() => {
      this.changeDetectorRef.detectChanges();
    }, 500);

    this.competitionFiltersService.selectedMarket = '';
    this.getSportEventFiltersAvailability();

    this.pubsubService.subscribe('competitionsPage', this.pubsubService.API.DELETE_EVENT_FROM_CACHE, (eventId: string) => {
      this.deleteEvent(eventId);
    });

    this.pubsubService.subscribe('competitionsPage', this.pubsubService.API.CHANGE_STATE_CHANGE_COMPETITIONS, state => {
        this.showCompetitionsList(state);
      });

    this.sportsConfigSubscription = this.activatedRoute.params
      .pipe(
        concatMap((params: Params) => {
          this.pTypeName = params.typeName;
          this.pClassName = params.className;
          return this.sportsConfigService.getSport(this.sportName);
        }),
        concatMap((sportInstance: GamingService) => {
          this.isTierOne = sportInstance.sportConfig.config.tier === 1;
          this.sport = sportInstance;
          this.sportId = sportInstance.sportConfig.config.request.categoryId;
          return this.cmsService.getSportTabs(this.sportId);
        })
      )
    .subscribe((sportTabs: ISportTabs) => {
      this.seasonId = '';
      this.showSpinner();
      this.isLoaded = false;

      this.competitionFilters = this.competitionFiltersService.formTimeFilters('competitions', sportTabs.tabs);
      this.targetTab = sportTabs.tabs.find((tab: ISportConfigTab) => tab.id.includes('competitions'));
      this.initCompetitions();
      this.removeSchemaForCompetitions();
      this.loadCompetitionsData(this.pTypeName, this.pClassName, this.sport.sportConfig);
    }, error => {
      console.warn('Competitions Page', error.error || error);
    });
  }

  loadAllCompetitions(categoryName: string): void {
    if (!(this.allCategories && this.allCategories.length)) {
      this.getClasses(this.allCategoriesClasses, categoryName)
        .subscribe((result: ICompetitionCategory[]) => {
          this.allCategories = _.sortBy(result, (item: ICompetitionCategory) => item.class.name.toLowerCase());
          if (this.allCategories.length) {
            this.allCategories[0].loading = false;
          } else {
            this.allCategories = [{ loading: false }] as ICompetitionCategory[];
          }
        }, error => {
          console.warn('A-Z Competitions:', error);
          this.allCategories = [{ loading: false }] as ICompetitionCategory[];
        });
    } else {
      this.allCategories[0].loading = false;
    }
  }

  getClasses(ids: string[], categoryName: string): Observable<ICompetitionCategory[] | any[]> {
    return from(categoryName === 'football' ?
      this.currentMatchesService.getFootballClasses(ids) : this.currentMatchesService.getOtherClasses(ids, this.sportId.toString()));
  }

  favIconDown() {
    this.windowRef.document.getElementById('fav-icon').classList.add('fav-icon-active');
  }
  favIconUp() {
    this.windowRef.document.getElementById('fav-icon').classList.add('fav-icon-inactive');
  }

  ngOnDestroy(): void {
    this.windowRef.nativeWindow.clearInterval(this.detectListener);

    this.resizeListener && this.resizeListener();
    this.pubsubService.unsubscribe('competitionsPage');

    this.getDataSubscription && this.getDataSubscription.unsubscribe();
    // unSubscribe LS Updates via liveServe PUSH updates (iFrame)!
    this.currentMatchesService.unSubscribeForUpdates();
    this.sportsConfigSubscription && this.sportsConfigSubscription.unsubscribe();
    this.cmsConfigSubscription && this.cmsConfigSubscription.unsubscribe();
    this.removeSchemaForCompetitions();
  }

  ngAfterViewInit() {
    this.handleDomElements();
  }

  /**
   * Load Competitions
   * @param {string} typeName
   * @param {string} className
   * @param {ISportConfig} sportConfig
   */
  loadCompetitionsData(typeName: string, className: string, sportConfig: ISportConfig): void {
    this.changeDetectorRef.detectChanges();

    this.getDataSubscription = from(this.currentMatchesService.getTypeEventsByClassName(typeName, className, sportConfig))
      .pipe(
        map((result: ICompetitionPage) => {
          this.typeName = result.data.type.name;  // Type name
          this.typeId = result.data.type.id;
          this.classId = result.data.type.classId;
          this.compitetionAutoSeoData();
          // Load Leagues Data
          this.isFootball() && this.loadLeaguesData(sportConfig.config.request.categoryId, result.data.type.classId, this.typeId);
          // Group by date
          this.eventsByCategory = this.sport.arrangeEventsBySection(result.data.events, true)[0];
          this.eventsByCategoryCopy = { ...this.eventsByCategory };
          this.deviceService.isRobot() && this.schemaForCompetitions(this.eventsByCategoryCopy);
          this.displayFilters = this.eventsByCategory !== undefined;

          // unsubscribe from previous competition events
          this.currentMatchesService.unSubscribeForUpdates();
          // subscribe LS Updates via WS;
          this.currentMatchesService.subscribeForUpdates(result.data.events);
          this.changeDetectorRef.detectChanges();

          this.outrights = this.filterService.orderBy(result.outrights, ['startTime', 'displayOrder', 'name']);
          this.generateSwitchers();
          this.selectFirstTab();

          const categoryName = (this.eventsByCategory && this.eventsByCategory.categoryName) ||
            (!_.isEmpty(this.outrights) && this.outrights[0].categoryName);
          if (categoryName) {
            this.cmsService.getItemSvg(categoryName)
              .subscribe(icon => {
                this.titleIconSvg = icon.svg;
                this.titleIconSvgId = icon.svgId;
              });
          }

          this.isLoaded = true;
          this.hideSpinner();
          return this.eventsByCategory;
        })
      )
      .subscribe(
        () => {},
        error => {
        this.isLoaded = true;

        if (error.noEventsFound) {
          this.hideSpinner();
        } else {
          this.showError();
        }

        console.warn('Competitions Data:', error.error || error);
      });
  }

  /**
   * Switch between tabs on competiton page
   * @param {string} id
   * @param {{ name: string }} tab
   */
  tabsSwitcher({ id, tab }: { id: string, tab:{ name: string } | any}): void {
    this.activeTab.id = id;
    this.activeTab.name = tab.name;
    this.eventsByCategory = {...this.eventsByCategoryCopy};
  }

  /**
   * Go to page
   * @param {string} path
   * @returns {void | boolean}
   */
  goToPage(path: string): boolean | Promise<boolean> {
    return path ? this.router.navigateByUrl(path) : false;
  }

  /**
   * Track Events by index
   * @param {number} index
   * @returns {number}
   */
  trackByIndex(index: number): number {
    return index;
  }

  /**
   * Function for open/close dropDown
   */
  showCompetitionsList(force?: boolean): void {
    if (!_.isUndefined(force)) {
      this.isShowCompetitions = force;
    } else {
      this.isShowCompetitions = !this.isShowCompetitions;
    }

    this.calculateDropDownDimensions();
    this.scrollToTop();
  }

  isTennis(): boolean {
    return this.sportName === 'tennis';
  }

  /**
   * Updates time filter when user clicks on it
   * @param {ILazyComponentOutput} output
   */
  handleCompetitionFilterOutput(output: ILazyComponentOutput): void {
    if (output.output === 'filterChange') {
      this.timeFilter = { ...this.timeFilter, ...output.value as ICompetitionFilter };

      this.eventsByCategory = [
        ...this.competitionFiltersService.filterEvents(null, this.timeFilter, [this.eventsByCategoryCopy]) as ITypeSegment[]
      ][0];
    }
  }

  protected generateSwitchers(): void {
    this.competitionTabs = [];
    this.rawCompetitionTabs = [];

    !_.isEmpty(this.eventsByCategory) && this.addTabs('matches');
    !_.isEmpty(this.outrights) && this.addTabs('outrights');
  }

  protected handleDomElements(): void {
    this.resizeListener = this.renderer.listen(this.window, 'resize', () => this.overallRecalculation());
  }

  private initCompetitions() {
    if (!this.mainCategories && this.isTierOne) {
      this.cmsService.getCompetitions(this.sportName).pipe(mergeMap((config: ICompetitionsConfig) => {
        this.allCategoriesClasses = config['A-ZClassIDs'] && config['A-ZClassIDs'].split(',');
        return this.getClasses(config.InitialClassIDs.split(','), this.sportName);
      })).subscribe((categories: ICompetitionCategory[]) => {
        this.mainCategories = categories;
        this.loadAllCompetitions(this.sportName);
      });
    } else {
      this.loadAllCompetitions(this.sportName);
    }
  }

  private selectFirstTab(): void {
    const firstTab = this.competitionTabs[0] || { id: '', name: '' };
    this.tabsSwitcher({ id: firstTab.id, tab: { name: firstTab.name } });
  }

  private addTabs(...names: string[]): void {
    COMPETITIONS_TABS.forEach((tab, index) => names.indexOf(tab.name) >= 0 && (this.rawCompetitionTabs[index] = tab));
    this.competitionTabs = this.rawCompetitionTabs.filter(t => t);
    this.showSwitchers = this.competitionTabs.length > 1;
  }

  public isFootball(): boolean {
    return this.sportName === 'football';
  }

  /**
   * Load Leagues
   * @param {string} sportId
   * @param {string} classId
   * @param {string} typeId
   */
  private loadLeaguesData(sportId: string, classId: string, typeId: string): void {
    this.commandService.executeAsync(this.commandService.API.GET_SEASON, [sportId, classId, typeId], {})
      .then((season: IStatsSeasonMatchSeason) => {
        if (season.id) {
          this.leaguesLink = ['sportId', 'areaId', 'competitionId', 'id'].reduce((link, value) => {
            return season[value] ? `${link}/${season[value]}` : link;
          }, '/leagues');
          this.seasonId = season.id;
          this.addTabs('results', 'standings');
        } else {
          this.seasonId = '';
        }
      }, error => {
        this.leaguesLink = '/search-leagues';
        this.seasonId = '';
        console.warn('Leagues Data:', error.error || error);
      });
  }

  private overallRecalculation(): void {
    this.calculateDropDownDimensions();
  }

  /**
   * Calculating dropDown dimensions depending on list size and other params, added proper scrolling
   */
  private calculateDropDownDimensions(): void {
    const competitionsListEl = this.competitionsList.nativeElement;
    let contentHeight = 0;

    this.changeDetectorRef.detectChanges();

    if (this.isShowCompetitions) {
      const pageContentEl = this.windowRef.document.querySelector('#page-content'),
        pageContentBottom = this.domToolsService.getElementBottomPosition(pageContentEl),
        competitionsHeaderBottom = this.domToolsService.getElementBottomPosition(this.competitionsHeader.nativeElement);
      contentHeight = pageContentBottom - competitionsHeaderBottom;
    }
    this.renderer.setStyle(competitionsListEl, 'min-height', `${contentHeight}px`);
  }

  /**
   * Scroll page to top
   * @param {number} position
   */
  private scrollToTop(position: number = 0): void {
    this.document.body.scrollTop = position; // For Safari
    this.document.documentElement.scrollTop = position; // For Chrome, Firefox, IE and Opera
  }

  /**
   * Delete Event
   * @param {string} eventId
   */
  private deleteEvent(eventId: string): void {
    const index = _.findIndex(this.eventsByCategory.events, { id: eventId });

    if (index !== -1) {
      this.eventsByCategory.events.splice(index, 1);
    }

    _.each(this.eventsByCategory.groupedByDate, (category: IGroupedByDateItem) => {
      const eventIndex = _.findIndex(category.events, { id: eventId });
      if (eventIndex !== -1) {
        category.events.splice(eventIndex, 1);
        if (!category.events.length) {
          delete this.eventsByCategory.groupedByDate[category.title];
        }
      }
    });
  }

  private getSportEventFiltersAvailability(): void {
    this.cmsConfigSubscription = this.competitionFiltersService.getSportEventFiltersAvailability()
      .subscribe((isAvailable: boolean) => this.isSportEventFiltersEnabled = isAvailable);
  }
  /**
   * Assigns autoSeoData object and publish the data for competitions-autoseo
   */
  private compitetionAutoSeoData(): void {
    this.autoSeoData.isOutright = false;
    this.autoSeoData.categoryName = this.sportName;
    this.autoSeoData.typeName = this.typeName;
    this.pubsubService.publish(this.pubsubService.API.AUTOSEO_DATA_UPDATED, this.autoSeoData);
  }
  /**
   * publish the events to append schemaObject
   * @param eventsByCategory 
   */
  private schemaForCompetitions(eventsByCategory: ITypeSegment): void {
    let eventsForSchema = [];
    this.competitionUrl = this.routingHelperService.formCompetitionUrl({
      sport: eventsByCategory?.categoryName, typeName: eventsByCategory?.typeName,
      className: eventsByCategory?.className
    });
    eventsForSchema = eventsByCategory?.events && this.competitionFiltersService.getSeoSchemaEvents(eventsByCategory.events);
    eventsForSchema?.length && this.pubsubService.publish(this.pubsubService.API.SCHEMA_DATA_UPDATED, [eventsForSchema, this.competitionUrl]);
  }
  /**
    * to remove the schemaScript
    */
  private removeSchemaForCompetitions(): void {
    this.deviceService.isRobot() && this.competitionUrl && this.pubsubService.publish(this.pubsubService.API.SCHEMA_DATA_REMOVED, this.competitionUrl);
  }
}
