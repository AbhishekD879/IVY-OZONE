import {
  ChangeDetectorRef,
  ChangeDetectionStrategy,
  Component,
  EventEmitter,
  Input,
  OnChanges,
  OnDestroy,
  OnInit,
  Output,
  SimpleChanges
} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable, Subscription } from 'rxjs';
import { map } from 'rxjs/operators';
import * as _ from 'underscore';

import { IReloadDataParams } from '@app/inPlay/models/reload-data-params.model';
import { IRequestParams } from '@app/inPlay/models/request.model';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IScrollVisibility } from '@app/shared/components/stickyVirtualScroller/sticky-virtual-scroller.model';

import { InplayMainService } from '@inplayModule/services/inplayMain/inplay-main.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
import { StickyVirtualScrollerService } from '@app/shared/components/stickyVirtualScroller/sticky-virtual-scroller.service';
import { GamingService } from '@core/services/sport/gaming.service';
import { ICompetitionsConfig } from '@core/services/cms/models/system-config';
import environment from '@environment/oxygenEnvConfig';
import { ILazyComponentOutput } from '@app/shared/components/lazy-component/lazy-component.model';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { LocaleService } from '@core/services/locale/locale.service';

@Component({
  selector: 'single-sport-section',
  templateUrl: 'single-sport-section.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  styleUrls: ['./single-sport-section.component.scss']
})
export class SingleSportSectionComponent implements OnInit, OnDestroy, OnChanges {
  @Input() filter: string;
  @Input() eventsBySports: ISportSegment;
  @Input() showExpanded: boolean;
  @Input() inner: any;
  @Input() expandedLeaguesCount: number;
  @Input() gtmModuleTitle?: string;
  @Input() virtualScroll: boolean;
  @Input() liveLabel: boolean;
  @Input() isHR: boolean = false;

  @Output() readonly reloadData: EventEmitter<IReloadDataParams> = new EventEmitter();
  @Output() readonly collapseSportEmitter: EventEmitter<boolean> = new EventEmitter();

  /**
   * Flags for control events during Competition data request process.
   * example "typeId":boolean
   * {
   *    '141':true
   * }
   * @type {object}
   */
  competitionRequestInProcessFlags = {};
  competitionsWithPages: ICompetitionsConfig;

  /**
   * IsExpanded Flags for competitions sections.
   * @type {object}
   * {
   *   "competitionId": boolean
   * }
   */
  expandedFlags = {};
  competitionsAvailability: { [key: string]: string } = {};
  isAllExpanded = false;
  isLoading: boolean = false;
  scrollSportUId: string;
  subscriptionFlags = {};
  sportName: string;
  selectedMarketName: string;
  categoryId: string;
  topLevelType: string;
  isMarketSelectorAvailable: boolean;
  sportInstance: GamingService;
  isMarketSwitcherConfigured: boolean = false;
  skeletonShow: Array<boolean> = [];
  HREvents = [];
  readonly HORSE_RACING_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;
  viewFullRaceText: string = '';

  /**
   * Constant with sports data
   */
  private CATEGORIES_DATA: any = environment.CATEGORIES_DATA;
  private syncName: string;
  private marketSwitcherConfigSubscription: Subscription;
  private mstimeout: number;
  private msinittimeout: number;
  private detectListener: number;
  private inPlayReloadListner: number;
  private inPlayEventUpdateListener:  number;

  constructor(
    private inPlayMainService: InplayMainService,
    private pubsubService: PubSubService,
    private changeDetectorRef: ChangeDetectorRef,
    private routingHelperService: RoutingHelperService,
    private activatedRoute: ActivatedRoute,
    private cmsService: CmsService,
    private coreToolService: CoreToolsService,
    private stickyVirtualScrollerService: StickyVirtualScrollerService,
    private windowRef: WindowRefService,
    public locale: LocaleService
  ) {
    this.syncName = `inplay-single-sport_${this.coreToolService.uuid()}`;
    this.reloadSportData = this.reloadSportData.bind(this);
  }

  ngOnInit(): void {
    this.categoryId = this.eventsBySports.categoryId;
    this.isHR = this.categoryId == this.HORSE_RACING_CATEGORY_ID;
    this.topLevelType = this.inPlayMainService.getTopLevelTypeParameter(this.filter);


    // Filter Enhanced Multiples
    if (this.eventsBySports.eventsByTypeName && this.eventsBySports.eventsByTypeName.length) {
      this.eventsBySports.eventsByTypeName = this.eventsBySports.eventsByTypeName.filter(competitionSection => {
        return competitionSection.typeName !== 'Enhanced Multiples';
      });
    }

    // Subscribing to the event sports data for the live now and upcoming filters
    this.pubsubService.subscribe(
      `EVENT_BY_SPORTS_SUBSCRIBE_${this.filter}`,
      `${this.pubsubService.API.EVENT_BY_SPORTS_CHANNEL}_SINGLE`,
      (data: { [key: string]: ISportSegment }) => {
        this.eventsBySports = data[this.filter];
        this.changeDetectorRef.detectChanges();
      }
    );

    this.cmsService.getCompetitions(this.activatedRoute.snapshot.paramMap.get('sport') || '')
      .subscribe((cmsData: ICompetitionsConfig) => {
        this.competitionsWithPages = cmsData;
        this.setCompetitionPagesAvailability();
        this.changeDetectorRef.markForCheck();
      });

    this.sportName = this.inPlayMainService.getSportName(this.eventsBySports);

    this.marketSwitcherConfigSubscription = this.cmsService.getMarketSwitcherFlagValue(this.sportName)
    .subscribe((flag: boolean) => {
      this.isMarketSwitcherConfigured = flag;
      this.changeDetectorRef.markForCheck();
    });

    this.inPlayMainService.getSportConfigSafe(this.sportName).subscribe((sportInstance: GamingService) => {
      this.sportInstance = sportInstance;
      this.extendSectionData();
      this.changeDetectorRef.markForCheck();
    });

    this.pubsubService.subscribe(this.syncName, `INPLAY_COMPETITION_REMOVED:${this.categoryId}:${this.topLevelType}`,
      (removedCompetition: ITypeSegment) => {
        this.processInitialData();
        this.subscriptionFlags[removedCompetition.typeId] = false;
        if (this.isMarketSelectorAvailable && !this.eventsBySports.eventsByTypeName.length && !this.isFirstMarketSelected()) {
          this.reloadSportData({
            useCache: false,
            additionalParams: {
              marketSelector: this.eventsBySports.marketSelectorOptions[0]
            }
          });
          this.changeDetectorRef.detectChanges();
        }

        if (this.inner) {
          // get first type section (after removed) to check if it is subscribed on updates
          const nextCompetitionSection = this.eventsBySports.eventsByTypeName && this.eventsBySports.eventsByTypeName[0];
          // subscribe if not subscribed
          if (nextCompetitionSection && !this.subscriptionFlags[nextCompetitionSection.typeId]) {
            this.loadCompetionSection(nextCompetitionSection, this.eventsBySports.eventsByTypeName)
              .subscribe(() => {
                this.expandedFlags[nextCompetitionSection.typeId] = true;
                nextCompetitionSection.isExpanded = true;
                this.changeDetectorRef.detectChanges();
              });
          }
        }

        this.calculateIsAllExpanded();
        this.changeDetectorRef.detectChanges();
      });

    this.pubsubService.subscribe(this.syncName, `INPLAY_COMPETITION_ADDED:${this.categoryId}:${this.topLevelType}`,
      (addedCompetition: ITypeSegment) => {
        this.processInitialData();
        if (this.inner) {
          if (addedCompetition.events.length === 0) {
            const sectionsArray = this.eventsBySports.eventsByTypeName;
            sectionsArray.splice(sectionsArray.indexOf(addedCompetition), 1);
          }

          this.setCompetitionPagesAvailability();

          if (!this.virtualScroll) {
            this.inPlayMainService.subscribeForUpdates(addedCompetition.events);
          }

          // Reset state of added accordion on SLP
          this.expandedFlags[addedCompetition.typeId] = this.inner;
        } else if (!this.inner && !this.virtualScroll) {
          if (this.expandedFlags[addedCompetition.typeId]) {
            this.inPlayMainService.subscribeForUpdates(addedCompetition.events);
          }
        }
        this.calculateIsAllExpanded();
        addedCompetition.isExpanded = this.expandedFlags[addedCompetition.typeId];
        this.changeDetectorRef.detectChanges();
      });

      this.pubsubService.subscribe(this.syncName, `INPLAY_COMPETITION_UPDATED:${this.categoryId}:${this.topLevelType}`, () => {
        this.expandedFlags = {};
        this.processInitialData();
        this.changeDetectorRef.detectChanges();
      });

    this.scrollSportUId = this.coreToolService.uuid();
    this.processInitialData();
    this.checkIfMarketSelectorAvailable();

     // Update Events and run digest manually using timeout
     this.pubsubService.subscribe(`inplaySectionLiveUpdate_${this.filter}`,
     this.pubsubService.API.WS_EVENT_LIVE_UPDATE,
       (eventId, message) => {
        this.detectListener = this.windowRef.nativeWindow.setTimeout(() => {
           this.changeDetectorRef.detectChanges();
        });
       });

    // Update inplay section reloaded data and run digest manually using timeout
    this.pubsubService.subscribe('inplaySectionDataReLoad',
    this.pubsubService.API.INPLAY_DATA_RELOADED,
      () => {
       this.inPlayReloadListner = this.windowRef.nativeWindow.setTimeout(() => {
          this.changeDetectorRef.detectChanges();
       });
    });

    this.pubsubService.subscribe(`inplayEventUpdate_${this.filter}`, this.pubsubService.API.WS_EVENT_UPDATE, (event: ISportEvent) => {
      this.inPlayEventUpdateListener = this.windowRef.nativeWindow.setTimeout(() => {
        this.changeDetectorRef.detectChanges();
      });
    });
    this.viewFullRaceText = this.locale.getString('racing.viewFullRace');
  }

  /**
   * return the EDP URL of the selected event
   * @param eventEntity event object
   * @returns
   */
  formEdpUrl(eventEntity: ISportEvent): string {
    return `${this.routingHelperService.formEdpUrl(eventEntity)}`;
  }

  ngOnChanges(changes: SimpleChanges): void {
    const eventsBySports = changes && changes.eventsBySports && changes.eventsBySports.currentValue;
    if (eventsBySports && Object.keys(eventsBySports).length) {
      this.processInitialData(eventsBySports);
      this.extendSectionData(true);
    }
  }

  ngOnDestroy(): void {
    this.inPlayMainService.unsubscribeForSportCompetitionUpdates(this.eventsBySports);
    this.inPlayMainService.unsubscribeForEventsUpdates(this.eventsBySports);
    this.pubsubService.unsubscribe(this.syncName);
    this.pubsubService.unsubscribe(`EVENT_BY_SPORTS_SUBSCRIBE_${this.filter}`);
    this.eventsBySports.eventsByTypeName = [];
    this.stickyVirtualScrollerService.stick(false, true);
    this.windowRef.nativeWindow.clearTimeout(this.msinittimeout);
    this.windowRef.nativeWindow.clearTimeout(this.mstimeout);
    this.windowRef.nativeWindow.clearTimeout(this.detectListener);
    this.windowRef.nativeWindow.clearTimeout(this.inPlayReloadListner);
    this.windowRef.nativeWindow.clearTimeout(this.inPlayEventUpdateListener);
    this.pubsubService.unsubscribe(`inplaySectionLiveUpdate_${this.filter}`);
    this.pubsubService.unsubscribe('inplaySectionDataReLoad');
    this.pubsubService.unsubscribe(`inplayEventUpdate_${this.filter}`);
    this.marketSwitcherConfigSubscription && this.marketSwitcherConfigSubscription.unsubscribe();
  }

  initMarketSelector(): void {
    this.msinittimeout = this.windowRef.nativeWindow.setTimeout(() => {
      this.changeDetectorRef.detectChanges();
    }, 1000);
  }

  goToCompetition(competitionSection: ITypeSegment): string {
    const competitionPageUrl = this.routingHelperService.formCompetitionUrl({
      sport: this.activatedRoute.snapshot.paramMap.get('sport'),
      typeName: competitionSection.typeName,
      className: competitionSection.className
    });
    return competitionPageUrl;
  }

  trackByTypeId(index: number, item: any): string {
    return item.typeId;
  }

  trackByEventId(index: number, item: any): string {
    return item.id + index;
  }

  /**
   * Set Expanded flags after reloading data.
   * @param {{}} options - { useCache, additionalParams }
   */
  reloadSportData(options: IReloadDataParams): void {
    this.reloadData.emit(options);
    this.mstimeout = this.windowRef.nativeWindow.setTimeout(() => {
      this.changeDetectorRef.detectChanges();
    }, 1000);
  }

  handleOutput(event: ILazyComponentOutput) {
    if (event.output === 'reloadData') {
      this.reloadSportData(event.value);
    }
    if (event.output === 'selectedMarketName') {
      this.selectedMarketName = event.value;
    }
  }

  setCompetitionPagesAvailability(): void {
    if (!this.eventsBySports || !this.eventsBySports.eventsByTypeName || !this.competitionsWithPages) {
      return;
    }

    const popularCompetitions = ((this.competitionsWithPages.InitialClassIDs || '').split(',') || []),
      aZCompetitions = ((this.competitionsWithPages['A-ZClassIDs'] || '').split(',') || []),
      allAvailableCompetitions = popularCompetitions.concat(aZCompetitions),
      competitionsAvailability = {};

    this.eventsBySports.eventsByTypeName.forEach((competitionSection) => {
      competitionSection.classId = competitionSection.events && competitionSection.events[0].classId;
      if (!competitionSection.classId) {
        return;
      }
      competitionsAvailability[competitionSection.classId] = _.contains(allAvailableCompetitions,
        competitionSection.classId);
    });
    this.competitionsAvailability = competitionsAvailability;
  }

  /**
   * Toggle expand/collapse state of league section.
   * @param {object} competitionSection
   * @param {array} sectionsArray
   */
  toggleCompetitionSection(competitionSection: ITypeSegment, sectionsArray: ITypeSegment[]  | ISportEvent, index: number): void {
    let isExpanded: boolean;
    if(!this.isHR) {
      isExpanded = this.expandedFlags[competitionSection.typeId] = !this.expandedFlags[competitionSection.typeId];
      competitionSection.isExpanded = isExpanded;
    } else {
      sectionsArray = sectionsArray as ISportEvent;
      competitionSection = this.eventsBySports.eventsByTypeName.find((competition: ITypeSegment)=> competition.typeId === (sectionsArray as ISportEvent).typeId)
      isExpanded = this.expandedFlags[sectionsArray.id] = !this.expandedFlags[sectionsArray.id];
      sectionsArray.isExpanded = isExpanded;
    }
    const isRequestInProcess = this.competitionRequestInProcessFlags[competitionSection.typeId];
    // if we are requesting data for specific competition, we will not subscribe/unsubscribe until request is done.
    if (isRequestInProcess && !this.isHR) {
        this.changeDetectorRef.detectChanges();
      return;
    }
    this.skeletonShow[index] = true;
    if (isExpanded) {
      this.loadCompetionSection(competitionSection, sectionsArray, false).subscribe(() => {
        // subscribe only if user not collapsed section during request
        if (!this.isHR && this.expandedFlags[competitionSection.typeId]) {
          this.inPlayMainService.subscribeForUpdates(competitionSection.events);
          this.subscriptionFlags[competitionSection.typeId] = true;
        }
        if(this.isHR && this.expandedFlags[(sectionsArray as ISportEvent).id]) {
          sectionsArray = sectionsArray as ISportEvent;
          this.inPlayMainService.subscribeForUpdates([sectionsArray]);
          this.subscriptionFlags[sectionsArray.id] = true;
        }
        this.skeletonShow[index] = false;
        this.changeDetectorRef.markForCheck();
      }, (error) => {
        console.warn(error);
        this.skeletonShow[index] = false;
          this.changeDetectorRef.detectChanges();
      });
    } else {
      if(!this.isHR) {
        this.inPlayMainService.unsubscribeForEventsUpdates(competitionSection);
        this.subscriptionFlags[competitionSection.typeId] = false;
      } else {
        sectionsArray = sectionsArray as ISportEvent;
        this.inPlayMainService.unsubscribeForEventUpdates(sectionsArray);
        this.subscriptionFlags[sectionsArray.id] = false;
      }

      this.skeletonShow[index] = false;
    }
      this.changeDetectorRef.detectChanges();
  }

  loadCompetionSection(competitionSection: ITypeSegment, sectionsArray: ITypeSegment[] | ISportEvent, silent: boolean = true): Observable<ISportEvent[]> {
    this.isLoading = !silent;
    this.competitionRequestInProcessFlags[competitionSection.typeId] = true;
    this.changeDetectorRef.markForCheck();
    const requestParams: IRequestParams = {
      categoryId: this.categoryId,
      isLiveNowType: this.filter === 'livenow' || this.filter === 'liveStream',
      topLevelType: this.inPlayMainService.getTopLevelTypeParameter(this.filter),
      typeId: competitionSection.typeId,
      // flag to detect should we modify markets marketMeaningMinorCode
      // and dispSortName in inPlayDataService(see modifyMainMarkets methods comment)
      modifyMainMarkets: true
    };

    if (competitionSection.marketSelector) {
      requestParams.marketSelector = competitionSection.marketSelector;
    }

    return this.inPlayMainService._getCompetitionData(requestParams, this.eventsBySports.categoryCode)
      .pipe(map((competitionEvents: ISportEvent[]) => {
        this.competitionRequestInProcessFlags[competitionSection.typeId] = false;

        if (competitionEvents.length === 0) {
          sectionsArray = sectionsArray as ITypeSegment[];
          sectionsArray.splice(sectionsArray.indexOf(competitionSection), 1);
        } else {
          // check for aggregateMarkets
          this.inPlayMainService.checkAggregateMarkets(requestParams, competitionSection, competitionEvents);

          let eventToBeAdd;
          competitionSection.events.forEach((eventData: ISportEvent)=>{
            if(eventData.id===(sectionsArray as ISportEvent).id){
              eventData.isExpanded=true;
              eventData.competitionSection = competitionSection;
              eventToBeAdd = eventData;
          }});
          this.HREvents.splice(this.HREvents.indexOf(sectionsArray), 1, eventToBeAdd);
          competitionSection.eventsIds = competitionEvents.map((event: ISportEvent) => event.id);
        }

        this.setCompetitionPagesAvailability();

        this.isLoading = false;
        this.changeDetectorRef.markForCheck();
        return competitionEvents;
      }));

  }

  prefetchNext(competitionSection: ITypeSegment) {
    if (this.isAllExpanded && competitionSection) {
      const isExpanded = this.expandedFlags[competitionSection.typeId];

      if (!isExpanded) {
        this.loadCompetionSection(competitionSection, this.eventsBySports.eventsByTypeName).subscribe(() => {
          this.expandedFlags[competitionSection.typeId] = true;
          competitionSection.isExpanded = true;
          this.changeDetectorRef.detectChanges();
        });
      }
    }
  }

  /**
   * Check rules to show marketSelector
   * @returns {boolean}
   */
  isMarketSelectorVisible(): boolean {
    const isEventsPresent: boolean = this.eventsBySports.eventsByTypeName && !!this.eventsBySports.eventsByTypeName.length;
    return this.isMarketSelectorAvailable && isEventsPresent;
  }

  /**
   * Check if marketSelector is available
   * @returns {boolean}
   */
  checkIfMarketSelectorAvailable(): void {
    const sportCategoryId = parseInt(this.categoryId, 10);
    const isMarketSelectorAvailable: boolean = this.filter === 'livenow' &&
      this.eventsBySports &&
      this.eventsBySports.marketSelectorOptions &&
      this.CATEGORIES_DATA.tierOne.includes(sportCategoryId.toString()) &&
      !this.inner;
    this.isMarketSelectorAvailable = !!isMarketSelectorAvailable;
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Get competition title text
   * @param {object} competitionSectionData
   * @returns {string}
   */
  getSectionTitle(competitionSectionData: ITypeSegment): string {
    return competitionSectionData.typeName || '';
  }

  showMoreSport(competitionSections: ITypeSegment[]): void {
    if (!this.inner) {
      return;
    }
    if (this.virtualScroll) {
      const nextCompetitionSection = competitionSections[this.expandedLeaguesCount];
      this.loadCompetionSection(nextCompetitionSection, competitionSections)
        .subscribe(() => {
          this.expandedFlags[nextCompetitionSection.typeId] = true;
          nextCompetitionSection.isExpanded = true;
          this.changeDetectorRef.detectChanges();
        });
    } else {
      competitionSections.forEach((competitionSection, i) => {
        if (i > this.expandedLeaguesCount - 1) {
          this.loadCompetionSection(competitionSection, competitionSections)
            .subscribe(() => {
              this.inPlayMainService.subscribeForUpdates(competitionSection.events);
              this.expandedFlags[competitionSection.typeId] = this.subscriptionFlags[competitionSection.typeId] = true;
              competitionSection.isExpanded = true;
              this.changeDetectorRef.detectChanges();
            });
        }
      });
    }

    this.isAllExpanded = true;
  }

  handleLiveUpdatesSubscriptions(event: IScrollVisibility, competitionSection: ITypeSegment): void {
    if (event.visible) {
      if (event.reloadData) {
        this.loadCompetionSection(competitionSection, this.eventsBySports.eventsByTypeName, true).subscribe(events => {
          if (!this.subscriptionFlags[competitionSection.typeId]) {
            this.inPlayMainService.subscribeForUpdates(competitionSection.events);
            this.subscriptionFlags[competitionSection.typeId] = true;
          }
          this.changeDetectorRef.detectChanges();
        });
      } else {
        if (!this.subscriptionFlags[competitionSection.typeId]) {
          this.inPlayMainService.subscribeForUpdates(competitionSection.events);
          this.subscriptionFlags[competitionSection.typeId] = true;
        }
      }
    } else {
      this.inPlayMainService.unsubscribeForEventsUpdates(competitionSection, false);
      this.subscriptionFlags[competitionSection.typeId] = false;
    }
  }

  /**
   * extends section data and sets availibility for Competition Pages
   * @param {Boolean} setAvailability
   */
  private extendSectionData(setAvailability: boolean = false): void {
    if (this.eventsBySports && this.sportInstance) {
      this.inPlayMainService.extendSectionWithSportInstance(this.eventsBySports, this.sportInstance);
      if (setAvailability) {
        this.setCompetitionPagesAvailability();
      }
    }
  }

  /**
   * Initial sections expanding/subscription on live updates
   */
  private processInitialData(data?: ISportSegment): void {
    const eventsBySports = data || this.eventsBySports;
    this.HREvents = [];
    if (eventsBySports && eventsBySports.eventsByTypeName) {
      eventsBySports.eventsByTypeName.forEach((competitionSection: ITypeSegment, index: number) => {
        this.setExpandedFlag(competitionSection, index);
      });
    }
  }

  /**
   * set Expanded flag to manage loading data when section being expanded
   */
  private setExpandedFlag(competitionSection: ITypeSegment, index: number): void {
    const isExpanded = this.expandedLeaguesCount === undefined || index < this.expandedLeaguesCount;
    if(!this.isHR) {
      this.expandedFlags[competitionSection.typeId] = isExpanded;
      competitionSection.isExpanded = isExpanded;
    } else if(competitionSection.events?.length) {
      competitionSection.events.forEach((eventData:ISportEvent)=> {
        eventData.compIndex= index;
        this.HREvents.push(eventData);
      })
      this.HREvents.sort((event: ISportEvent, nextEvent: ISportEvent) => new Date(event.startTime).getTime() - new Date(nextEvent.startTime).getTime());
      if(this.eventsBySports.eventsByTypeName.length===index+1) {
        this.HREvents.forEach((eventData: ISportEvent, eventIndex: number)=>{
          if(eventIndex<this.expandedLeaguesCount && eventData.markets){
            if(!this.expandedFlags[eventData.id]) {
              this.inPlayMainService.subscribeForUpdates([eventData]);
            }
            this.expandedFlags[eventData.id] = true;
            eventData.isExpanded = true;
          }
        })
      }
    }
    this.skeletonShow[index] = !isExpanded;
  }

  private calculateIsAllExpanded(): void {
    const isCollapsedExists: boolean = _.some(this.expandedFlags, (isExpanded: boolean) => !isExpanded);
    this.isAllExpanded = !isCollapsedExists;
  }

  /**
   * Check if first market is selected in market selector
   */
  private isFirstMarketSelected(): boolean {
    return ['Main Market', 'Match Betting'].includes(this.selectedMarketName);
  }

  /**
   * Selectd market
   * @param {object} competitionSection
   * @returns {string}
   */
  getSelectedMarket(competitionSection: ITypeSegment): string {
    return (competitionSection.events[0].markets[0] ? competitionSection.events[0].markets[0].name : '');
  }
}
