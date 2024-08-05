import {
  ChangeDetectorRef,
  Component,
  EventEmitter,
  Input,
  OnChanges,
  OnDestroy,
  OnInit,
  Output,
  SimpleChanges,
  ChangeDetectionStrategy
} from '@angular/core';

import { InplayMainService } from '@app/inPlay/services/inplayMain/inplay-main.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

import environment from '@environment/oxygenEnvConfig';
import { CmsService } from '@coreModule/services/cms/cms.service';

import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import { IReloadDataParams } from '@app/inPlay/models/reload-data-params.model';
import { IRequestParams } from '@app/inPlay/models/request.model';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { CoreToolsService } from '@app/core/services/coreTools/core-tools.service';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { GamingService } from '@core/services/sport/gaming.service';
import { Subscription } from 'rxjs';
import { ILazyComponentOutput } from '@app/shared/components/lazy-component/lazy-component.model';
import { LocaleService } from '@core/services/locale/locale.service';

@Component({
  selector: 'single-sport-section',
  templateUrl: 'single-sport-section.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class SingleSportSectionComponent implements OnInit, OnDestroy, OnChanges {
  @Input() filter: string;
  @Input() eventsBySports: ISportSegment;
  @Input() showExpanded: boolean;
  @Input() inner: any;
  @Input() expandedLeaguesCount: number;
  @Input() gtmModuleTitle?: string;
  @Input() resetDropdown: boolean;

  @Output() readonly reloadData: EventEmitter<IReloadDataParams> = new EventEmitter();

  sport: GamingService;
  categoryId: string;
  topLevelType: string;
  isMarketSwitcherConfigured: boolean = false;
  /**
   * Flags for control events during Competition data request process.
   * example "typeId":boolean
   * {
   *    '141':true
   * }
   * @type {object}
   */
  competitionRequestInProcessFlags = {};

  /**
   * IsExpanded Flags for competitions sections.
   * @type {object}
   * {
   *   "competitionId": boolean
   * }
   */
  expandedFlags = {};
  HREvents = [];
  isHR: boolean = false;
  readonly HORSE_RACING_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;
  viewFullRaceText: string = '';

  /**
   * Constant with sports data
   */
  private CATEGORIES_DATA: any = environment.CATEGORIES_DATA;
  private detectListener: number;
  private syncName: string;
  private sportsConfigSubscription: Subscription;
  private marketSwitcherConfigSubscription: Subscription;

  constructor(
    private inPlayMainService: InplayMainService,
    private pubSubService: PubSubService,
    private windowRef: WindowRefService,
    private changeDetectorRef: ChangeDetectorRef,
    private coreToolService: CoreToolsService,
    private sportsConfigService: SportsConfigService,
    private cmsService: CmsService,
    public locale: LocaleService
  ) {
    this.syncName = `inplay-single-sport_${this.coreToolService.uuid()}`;
    this.reloadSportData = this.reloadSportData.bind(this);
  }

  ngOnInit(): void {
    this.categoryId = this.eventsBySports.categoryId;
    this.isHR = this.categoryId == this.HORSE_RACING_CATEGORY_ID;
    this.topLevelType = this.inPlayMainService.getTopLevelTypeParameter(this.filter);

    const sportName = this.inPlayMainService.getSportName(this.eventsBySports);

    this.marketSwitcherConfigSubscription = this.cmsService.getMarketSwitcherFlagValue(sportName)
    .subscribe((flag: boolean) => {
      this.isMarketSwitcherConfigured = flag;
      this.changeDetectorRef.markForCheck();
    });

    this.sportsConfigSubscription = this.sportsConfigService.getSport(sportName).subscribe((sportInstance: GamingService) => {
      this.sport = sportInstance;
      this.changeDetectorRef.markForCheck();
    });

    // Filter Enhanced Multiples
    if (this.eventsBySports.eventsByTypeName && this.eventsBySports.eventsByTypeName.length) {
      this.eventsBySports.eventsByTypeName = this.eventsBySports.eventsByTypeName.filter(competitionSection => {
        return competitionSection.typeName !== 'Enhanced Multiples';
      });
    }

    this.pubSubService.subscribe(this.syncName, `INPLAY_COMPETITION_ADDED:${this.categoryId}:${this.topLevelType}`, addedCompetition => {
      this.expandedFlags = {};
      this.setExpandedFlags();

      if (this.expandedFlags[addedCompetition.typeId]) {
        this.inPlayMainService.subscribeForUpdates(addedCompetition.events);
        addedCompetition.isExpanded = true;
      }
      this.changeDetectorRef.detectChanges();
    });

    this.pubSubService.subscribe(this.syncName, `INPLAY_COMPETITION_REMOVED:${this.categoryId}:${this.topLevelType}`, () => {
      this.expandedFlags = {};
      this.setExpandedFlags();
      if (this.isMarketSelectorVisible() && !this.eventsBySports.eventsByTypeName.length
        && !['Main Market', 'Match Betting'].includes(this.eventsBySports.marketSelector)) {
        this.reloadSportData({
          useCache: false,
          additionalParams: {
            marketSelector: this.eventsBySports.marketSelectorOptions[0]
          }
        });
      }
      this.changeDetectorRef.detectChanges();
    });

    this.pubSubService.subscribe(this.syncName, `INPLAY_COMPETITION_UPDATED:${this.categoryId}:${this.topLevelType}`, () => {
      this.expandedFlags = {};
      this.setExpandedFlags();
      this.changeDetectorRef.detectChanges();
    });

    this.pubSubService.subscribe(this.syncName, this.pubSubService.API.DELETE_EVENT_FROM_CACHE, eventId => {
      this.inPlayMainService.clearDeletedEventFromType(this.eventsBySports, eventId);
      this.changeDetectorRef.markForCheck();
    });

    this.setExpandedFlags();

    // Update Events and run digest manually using timeout
    this.pubSubService.subscribe('inplaySectionLiveUpdate',
    this.pubSubService.API.WS_EVENT_LIVE_UPDATE,
      (eventId, message) => {
        this.detectListener = this.windowRef.nativeWindow.setTimeout(() => {
          this.changeDetectorRef.detectChanges();
        });
    });
    this.viewFullRaceText = this.locale.getString('racing.viewFullRace');
  }

  ngOnDestroy(): void {
    this.inPlayMainService.unsubscribeForSportCompetitionUpdates(this.eventsBySports);
    this.inPlayMainService.unsubscribeForEventsUpdates(this.eventsBySports);
    this.pubSubService.unsubscribe(this.syncName);
    this.pubSubService.unsubscribe('inplaySectionLiveUpdate');
    this.eventsBySports.eventsByTypeName = [];
    this.windowRef.nativeWindow.clearTimeout(this.detectListener);
    this.sportsConfigSubscription && this.sportsConfigSubscription.unsubscribe();
    this.marketSwitcherConfigSubscription && this.marketSwitcherConfigSubscription.unsubscribe();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.eventsBySports) {
      this.expandedFlags = {};
      this.setExpandedFlags();
      this.changeDetectorRef.markForCheck();
    }
  }

  initMarketSelector(isLast: boolean = true): void {
    if(isLast) {
      setTimeout(()=> {
        this.changeDetectorRef.detectChanges();
      }, 1000);
    }
  }

  trackByTypeId(index: number, item: any): string {
    return item.typeId;
  }

  trackByEventId(index: number, item: any): string {
    return item.id + index;
  }

  /**
   * Clean Expanded flags before reload data from Ms
   * Set Expanded flags after reloading data.
   * @param {{}} options - { useCache, additionalParams }
   */
  reloadSportData(options: IReloadDataParams): void {
    this.expandedFlags = {};

    this.reloadData.emit(options);
    setTimeout(()=> {
      this.changeDetectorRef.detectChanges();
    }, 1000);
  }


  handleSportData(event: ILazyComponentOutput) {
    this.reloadSportData(event.value);
  }
  /**
   * set Expanded flags to manage loading data when section being expanded
   */
  setExpandedFlags(): void {
    if (!this.eventsBySports || !this.eventsBySports.eventsByTypeName) {
      return;
    }

    this.categoryId = this.eventsBySports.categoryId;
    this.isHR = this.categoryId == this.HORSE_RACING_CATEGORY_ID;
    this.HREvents = [];
    this.eventsBySports.eventsByTypeName.forEach((competitionSection, index) => {
      if(!this.isHR) {    
        const isExpanded = this.expandedLeaguesCount === undefined || index < this.expandedLeaguesCount;
        competitionSection.showCashoutIcon = isExpanded;

        if (this.expandedFlags[competitionSection.typeId] === undefined) {
          this.expandedFlags[competitionSection.typeId] = isExpanded;
        }
      } else if(competitionSection.events?.length) {
        competitionSection.events.map((eventData: ISportEvent)=> {
          eventData.compIndex= index;
          this.HREvents.push(eventData);
        })
        this.HREvents.sort((event: ISportEvent, nextEvent: ISportEvent) => new Date(event.startTime).getTime() - new Date(nextEvent.startTime).getTime());      
        if(this.eventsBySports.eventsByTypeName.length===index+1) {
          this.HREvents.forEach((eventData: ISportEvent, eventIndex: number)=>{
            if(eventIndex < this.expandedLeaguesCount && eventData.markets){
              this.expandedFlags[eventData.id] = true;
              eventData.isExpanded = true;
              this.inPlayMainService.subscribeForUpdates([eventData]);
            }
          })
        }
      }
    });
    this.changeDetectorRef.markForCheck();
  }

  /**
   * Toggle expand/collapse state of league section.
   * @param {object} competitionSection
   * @param {array} sectionsArray
   */
  toggleCompetitionSection(competitionSection: ITypeSegment, sectionsArray: ITypeSegment[] | ISportEvent): void {
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
      return;
    }

    if (isExpanded) {
      this.competitionRequestInProcessFlags[competitionSection.typeId] = true;

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

      this.inPlayMainService._getCompetitionData(requestParams, this.eventsBySports.categoryCode)
        .subscribe((competitionEvents: ISportEvent[]) => {
          this.competitionRequestInProcessFlags[competitionSection.typeId] = false;

          if (competitionEvents.length === 0) {
            sectionsArray = sectionsArray as ITypeSegment[];
            sectionsArray.splice(sectionsArray.indexOf(competitionSection), 1);
          } else {
            // check for aggregateMarkets
            this.inPlayMainService.checkAggregateMarkets(requestParams, competitionSection, competitionEvents);
            
            competitionSection.eventsIds = competitionEvents.map((event: ISportEvent) => event.id);
            let eventToBeAdd;
            competitionSection.events.forEach((eventData: ISportEvent)=>{
              if(eventData.id===(sectionsArray as ISportEvent).id){
                eventData.isExpanded=true;
                eventData.competitionSection = competitionSection;
                eventToBeAdd = eventData;
            }});
            this.HREvents.splice(this.HREvents.indexOf(sectionsArray), 1, eventToBeAdd);

            // subscribe only if user not collapsed section during request
            if (!this.isHR && this.expandedFlags[competitionSection.typeId]) {
              this.inPlayMainService.subscribeForUpdates(competitionSection.events);
            } else {
              sectionsArray = sectionsArray as ISportEvent;
              this.inPlayMainService.subscribeForUpdates([sectionsArray]);
            }
          }
          this.changeDetectorRef.markForCheck();
        });
    } else {
      if (!this.isHR) {
        this.inPlayMainService.unsubscribeForEventsUpdates(competitionSection);
      } else {
        sectionsArray = sectionsArray as ISportEvent;
        this.inPlayMainService.unsubscribeForEventUpdates(sectionsArray);
      }
    }
  }

  /**
   * Check rules to show marketSelector
   * @returns {boolean}
   */
  isMarketSelectorVisible(): boolean {
    const sportCategoryId = this.eventsBySports ? parseInt(this.categoryId, 10) : null;
    return this.eventsBySports &&
      this.eventsBySports.marketSelectorOptions &&
      this.CATEGORIES_DATA.tierOne.includes(sportCategoryId.toString()) &&
      this.filter === 'livenow' &&
      !this.inner;
  }

  /**
   * Check if to show cashout label
   * @param {Array} events
   * @returns {Boolean}
   */
  isCashoutAvailable(events: ISportEvent[], showIcon: boolean): boolean {
    return this.inPlayMainService.isCashoutAvailable(events) && showIcon;
  }

  /**
   * Get competition title text
   * @param {object} competitionSectionData
   * @returns {string}
   */
  getSectionTitle(competitionSectionData: ITypeSegment): string {
    if (this.inner) {
      return competitionSectionData.typeSectionTitleAllSports || '';
    }

    return competitionSectionData.typeSectionTitleOneSport || '';
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
