import * as _ from 'underscore';
import { Component, Input, Output, OnInit, OnChanges, SimpleChanges, OnDestroy, EventEmitter, ChangeDetectorRef, ViewEncapsulation } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import { MarketTypeService } from '@shared/services/marketType/market-type.service';
import { OddsCardHeaderService } from '@shared/components/oddsCardHeader/odds-card-header.service';
import { IMarket } from '@core/models/market.model';
import { TemplateService } from '@shared/services/template/template.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { IScoreUpdateEventOptions } from '@core/models/update-options.model';
import { ScoreParserService } from '@core/services/scoreParser/score-parser.service';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { ISportInstance, ISportConfig } from '@core/services/cms/models';
import { Subscription } from 'rxjs';
import { SportsConfigHelperService } from '@app/sb/services/sportsConfig/sport-config-helper.service';
import { handicapTemplateMarketName } from '@app/shared/constants/odds-card-constant';
import environment from '@environment/oxygenEnvConfig';
import { scoreLabels } from '@shared/enums/odds-card-header.enum';
@Component({
  selector: 'odds-card-header',
  templateUrl: 'odds-card-header.component.html',
  styleUrls: ['odds-card-header.component.scss'],
  encapsulation: ViewEncapsulation.None
})

export class OddsCardHeaderComponent implements OnInit, OnChanges, OnDestroy {
  @Input() events: ISportEvent[];
  @Input() selectedMarket?: string;
  @Input() dateTitle: string;
  @Input() isFilterByTemplateMarketName: boolean;
  @Input() isFavorite?: boolean;
  @Input() hideOddsTitles?: boolean = false;
  @Input() isHeaderAlwaysVisible?: boolean = false;
  @Input() isScoreHeader?: boolean = true;
  @Input() sportConfig?: ISportConfig;
  @Input() undisplayedMarket?: IMarket;
  @Input() moduleId?: string;
  @Output() readonly initialized?: EventEmitter<string> = new EventEmitter();
  @Input() isMarketSwitcherConfigured: boolean;

  showOddsCardHeader: boolean;
  headTitles: Array<string> | string;
  scoreHeaders: Array<string>;
  eventScoreLabel: boolean;
  dartsOnlyLegs: boolean;
  isListTemplate: boolean;
  isMultiMarketTemplate: boolean;
  showTootltip: boolean;
  toolTipArgs: {[key: string]: string};
  readonly scoreLabels = scoreLabels;

  protected uniqueId: string;
  private hasOutcomeStatusTrue: boolean;
  private availableOddsHeader: boolean;
  private oddsCardHeader: string | void;
  private sportName: string;
  private sportsConfigSubscription: Subscription;
  private cachedEventsIds: number[];
  
  constructor(
    private marketTypeService: MarketTypeService,
    private templateService: TemplateService,
    private oddsCardHeaderService: OddsCardHeaderService,
    private pubSubService: PubSubService,
    private coreToolsService: CoreToolsService,
    private scoreParserService: ScoreParserService,
    private sportsConfigService: SportsConfigService,
    private sportConfigHelperService: SportsConfigHelperService,
    private changeDetectorRef: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    this.uniqueId = this.coreToolsService.uuid();
    if (!this.events) {
      this.events = [];
    } else {
      this.cachedEventsIds = this.events.map(event => event.id);
    }
    this.sportName = this.events.length && this.sportConfigHelperService.getSportConfigName(this.events[0].categoryName);

    this.hasOutcomeStatusTrue = this.events[0] ? this.events[0].outcomeStatus : false;

    if (!this.sportConfig && this.sportName) {
      this.sportsConfigSubscription = this.sportsConfigService.getSport(this.sportName).subscribe((sportInstance: ISportInstance) => {
        this.sportConfig = sportInstance && sportInstance.sportConfig;
        this.initHeader();
      });
    } else {
      this.initHeader();
    }

    // subscribe to score updates to show S/G/P labels in header
    this.pubSubService.subscribe(
      `oddsCardHeader_${this.uniqueId}`,
      this.pubSubService.API.EVENT_SCORES_UPDATE,
      (options: IScoreUpdateEventOptions) => {
        if (this.events.find((event: ISportEvent) => event.id === options.event.id)) {
          this.initHeader();
        }
      }
    );

    this.pubSubService.subscribe(`oddsCardHeader_${this.uniqueId}`, this.pubSubService.API.DELETE_EVENT_FROM_CACHE, (eventId: number) => {
      const eventIndex = this.cachedEventsIds.indexOf(eventId) ;
      if (eventIndex !== -1) {
        this.cachedEventsIds.splice(eventIndex, 1);
        this.initHeader();
      }
    });

    this.pubSubService.subscribe(`oddsCardHeader_${this.uniqueId}`, this.pubSubService.API.WS_EVENT_UPDATE, () => {
      this.initHeader();
      this.changeDetectorRef.detectChanges();
    });
    this.checkDartEventOnlyLeg();
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(`oddsCardHeader_${this.uniqueId}`);
    this.sportsConfigSubscription && this.sportsConfigSubscription.unsubscribe();
    this.cachedEventsIds = null;
  }

  ngOnChanges(changes: SimpleChanges) {

    if ((changes.events && changes.events.currentValue !== changes.events.previousValue)) {
      this.cachedEventsIds = this.events.map(event => event.id);
    }

    // watch events and market to update header when event undisplayed/finished, related Feature tab
    if ((changes.selectedMarket || changes.events && changes.events.currentValue !== changes.events.previousValue)
      || (changes.undisplayedMarket && !changes.undisplayedMarket.currentValue.isDisplayed)
    ) {
      this.initHeader();
    }
  }

  /**
   * Logic to show/hide score headers (S/G/P)
   */
  showScoreHeaders(sportId: string): void {
    this.scoreHeaders = null;
    if (this.isScoreHeader && this.oddsCardHeaderService.isEventsHaveScores(this.events)) {
      this.scoreHeaders = this.scoreParserService.getScoreHeaders(sportId);
      if (this.scoreHeaders) {
        this.oddsCardHeaderService.sortEventsByScores(this.events);
      }
    }
  }
  /**
   * Check if dart event has Sets & legs Or Only legs
   */
  private checkDartEventOnlyLeg(): void {
    this.eventScoreLabel = false;
    this.dartsOnlyLegs = false;
     if(this.scoreHeaders && this.events.length && this.events[0].categoryId === '13' &&
      !this.events[0].comments.teams.home.score) {
        this.eventScoreLabel = false;
        this.dartsOnlyLegs = true;
      } else if(this.scoreHeaders && this.events.length) {
        this.eventScoreLabel = true;
        this.dartsOnlyLegs = false;
      }
  }

  private initHeader(): void {
    let marketNames = this.marketTypeService.extractMarketNameFromEvents(this.events, this.isFilterByTemplateMarketName);
    const marketNamesList = this.marketTypeService.extractMarketNameFromEvents(JSON.parse(JSON.stringify(this.events)),true);
    marketNames = _.uniq(marketNames.concat(marketNamesList));
    if (marketNames && marketNames.includes('Match Result')) { 
      (marketNames).push('Match Betting'); 
    }
    // The below method returns always the first match of marketconfig not based on the selected market
    // this.marketTypeService.getDisplayMarketConfig(sportMarketNames, marketNames)
    if ((this.sportConfig && !environment.CATEGORIES_DATA.categoryIds.includes(this.sportConfig.config.request.categoryId))
      || (this.sportConfig && !this.isMarketSwitcherConfigured)) {
    const config = this.sportConfig.config;
    const isGolfOutright = (config.request.categoryId === environment.CATEGORIES_DATA.golfId && config.oddsCardHeaderType === '' && config.isOutrightSport);
    const intersects = isGolfOutright ? marketNames.join(',') : config.request.marketTemplateMarketNameIntersects;
    const displayMarketConfig = this.marketTypeService.getDisplayMarketConfig(intersects, marketNames);
    const hasMarket = this.selectedMarket ? _.intersection(this.selectedMarket.split(','), marketNames).length > 0 : false;
    if(!hasMarket){
      this.selectedMarket = displayMarketConfig.displayMarketName;
    }
    }
    this.isListTemplate = this.templateService.isListTemplate(this.selectedMarket);
    this.isMultiMarketTemplate = this.templateService.isMultiMarketTemplate(this.selectedMarket);
    if(this.isMultiMarketTemplate){
      this.headTitles = this.selectedMarket.split(',');
      this.toolTipArgs = {};
      this.headTitles.forEach(data => this.toolTipArgs[data] = data);
      this.isHeaderAlwaysVisible = this.oddsCardHeaderService.showComponent(marketNames, this.selectedMarket);
      this.showOddsCardHeader = this.isHeaderAlwaysVisible;
      return;
    }
    this.availableOddsHeader = this.selectedMarket !== handicapTemplateMarketName
    && this.oddsCardHeaderService.showComponent(marketNames, this.selectedMarket);
    if (this.events.length && this.availableOddsHeader) {
      const sportId = this.events[0].categoryId,
        isSpecialEvent = this.oddsCardHeaderService.isRacing(sportId) ||
          this.oddsCardHeaderService.isSpecialSection(this.events, this.sportConfig);

      if (this.sportConfig && !isSpecialEvent) {
        if (this.sportConfig.config.isMultiTemplateSport) {
          this.oddsCardHeader = this.getOddsCardHeader(this.events, this.sportName);
          this.setOddCardHeaderType(this.events, this.oddsCardHeader);
        } else {
          const oddsCardHeaderType = this.sportConfig.config.oddsCardHeaderType;
          if (oddsCardHeaderType && this.sportName !== 'football') {
            // remove this if after CMS deployment
            this.oddsCardHeader = oddsCardHeaderType;
            if (_.isObject(oddsCardHeaderType)) {
              this.oddsCardHeader = oddsCardHeaderType.outcomesTemplateType1;
            }
          } else {
            this.oddsCardHeader = this.getOddsCardHeader(this.events, this.sportName);
            this.setOddCardHeaderType(this.events, this.oddsCardHeader);
          }
        }
        this.showScoreHeaders(sportId);
        this.setHeaderContent();
        this.setOddCardHeaderType(this.events, this.oddsCardHeader);
      } else {
        this.oddsCardHeader = undefined;
        this.showOddsCardHeader = false;
      }
    } else {
      this.oddsCardHeader = undefined;
      this.showOddsCardHeader = false;
    }
    if(this.isListTemplate && this.isMarketSwitcherConfigured) {
      this.showOddsCardHeader = true;
    }
    this.undisplayedMarket = null;
    this.initialized.emit(this.moduleId);
  }

  /**
   * Set odds card header type for events
   */
  private setOddCardHeaderType(events: ISportEvent[], oddsCardHeader: string | void): void {
    _.each(events, event => {
      event.oddsCardHeaderType = oddsCardHeader;
    });
  }

  /**
   * Get market from first not special event, if there are such events
   *
   * @param {array} events
   * @returns {object|boolean}
   */
  private getFirstNotSpecialMarket(events: ISportEvent[]): IMarket | void {
    // not special events
    const filteredEvents = _.reject(events, event => {
      return this.oddsCardHeaderService.isSpecialEvent(event, this.sportConfig);
    });
    if (!filteredEvents.length || !filteredEvents[0].markets.length) {
      return undefined;
    }
    const marketNames = this.marketTypeService.extractMarketNameFromEvents(JSON.parse(JSON.stringify(filteredEvents)), this.isFilterByTemplateMarketName);
    if(this.selectedMarket && !marketNames.includes(this.selectedMarket)){
      this.selectedMarket = undefined;
    }
    let market;
    const selectedMarket = this.selectedMarket && this.selectedMarket !== handicapTemplateMarketName
      ? this.selectedMarket : filteredEvents[0].markets[0].name;

    // for filtered events, we should get filtered market to set Card Header
    if (this.isFilterByTemplateMarketName) {
      for (let i = 0; i < filteredEvents.length; i++) {
        market = _.findWhere(filteredEvents[i].markets, { templateMarketName: selectedMarket });
        if (market) {
          return market;
        }
      }
    }
    market = _.findWhere(filteredEvents[0].markets, { name: selectedMarket });

    return market;
  }

  /**
   * Set odds header content
   */
  private setHeaderContent(): void {
    this.headTitles = [];
    this.showOddsCardHeader = this.availableOddsHeader && !this.hasOutcomeStatusTrue && !!this.oddsCardHeader;

    const marketEntity = this.events.length && this.getFirstNotSpecialMarket(this.events);
    const isMatchResultMarket = this.marketTypeService.someEventsAreMatchResultType(this.events,
      this.selectedMarket, this.isFilterByTemplateMarketName);
    const isHomeDrawAwayNotMatchResult = this.oddsCardHeader === 'homeDrawAwayType' && !isMatchResultMarket;

    // yes/no header
    const isYesNoType = this.isYesNoType(isHomeDrawAwayNotMatchResult, marketEntity as IMarket);

    // over/under header
    const isOverUnderType = marketEntity && this.marketTypeService.isOverUnderType(marketEntity);

    // home/away/no goal header
    const isNextTeamToScoreType = marketEntity && marketEntity.templateMarketName === 'Next Team to Score';

    // home/draw/away header
    const isHomeDrawAwayType = !marketEntity || (marketEntity && !isNextTeamToScoreType &&
      (this.marketTypeService.isHomeDrawAwayType(marketEntity) || isMatchResultMarket));

    // 1/2 header
    const isOneTwoType = marketEntity && this.oddsCardHeader === 'oneTwoType';

    // 1/TIE/2 header
    const isOneXTwoType = marketEntity &&
      this.marketTypeService.isOneTieTwoType(marketEntity, this.sportConfig.config.request.categoryId);

    // 1/2/3 header
    const isOneTwoThreeType = this.oddsCardHeader === 'oneThreeType';

    const isBoxingFightBetting = marketEntity &&
      this.marketTypeService.isOneDrawTwoType(marketEntity, this.sportConfig.config.request.categoryId);

    // home/away header
    const isHomeAwayType = this.oddsCardHeader === 'homeAwayType' ||
      (!isOneTwoType &&
        !isNextTeamToScoreType &&
        !isHomeDrawAwayType &&
        !isOverUnderType &&
        !isYesNoType &&
        !isOneTwoThreeType &&
        !this.isListTemplate);

    const headTitles = _.findKey({
      '1,Tie,2': isOneXTwoType,
      'over,under': isOverUnderType,
      '1,2': isOneTwoType,
      '1,2,3': isOneTwoThreeType,
      'home,draw,away': isHomeDrawAwayType && !isHomeAwayType && !isBoxingFightBetting,
      'home,away,noGoal': isNextTeamToScoreType,
      'home,away': isHomeAwayType,
      'yes,no': isYesNoType,
      '1,draw,2': isBoxingFightBetting
    }, undefined);

    this.headTitles = this.oddsCardHeaderService.getLocale(headTitles);
  }

  private isYesNoType(isHomeDrawAwayNotMatchResult: boolean, marketEntity: IMarket): boolean {
    return this.oddsCardHeader === 'yesNoType' ||
      (isHomeDrawAwayNotMatchResult && marketEntity && this.marketTypeService.isYesNoType(marketEntity));
  }

  /**
   * Returns odds Card Header Type
   * @param events
   * @param sportName
   * @returns {string}
   */
  private getOddsCardHeader(events: ISportEvent[], sportName?: string): string | void {
    let oddsCardHeader;

    _.each(events, event => {
      if (this.oddsCardHeaderService.isSpecialEvent(event, this.sportConfig)) {
        return;
      }
      const currentMarkets = event.markets;
      const marketName = currentMarkets.length && currentMarkets[0].name;
      const selectedMarket = this.selectedMarket ? this.selectedMarket : marketName;
      const market = this.oddsCardHeaderService.getMarketByTemplateMarketName(currentMarkets,
        selectedMarket, this.isFilterByTemplateMarketName);
      const isFootballMarket = !!(sportName === 'football' && market);

      if (market) {
        oddsCardHeader = this.oddsCardHeaderService.getHeaderByMarketName(isFootballMarket, market);

        if (!oddsCardHeader) {
          const viewType = this.templateService.getMarketViewType(market);
          const outcomesCount = market.outcomes && market.outcomes.length;

          oddsCardHeader = this.oddsCardHeaderService.getHeaderByViewType(viewType, outcomesCount, sportName);
        }
      }
    });

    return oddsCardHeader || 'oneTwoType';
  }

  /**
   * Abbreviations for SLP where market name is long
   * @param title 
   * @returns string : Market Name
   */
  getHeader(title): string {
    const translatedTitle = this.oddsCardHeaderService.getMultiTemplateHeader(title);
    this.showTootltip = translatedTitle === title && (title.length<=12) ? false : true;
    return translatedTitle;
  }
}