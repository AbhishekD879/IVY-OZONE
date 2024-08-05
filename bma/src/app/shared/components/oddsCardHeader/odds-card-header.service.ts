import * as _ from 'underscore';
import { Injectable } from '@angular/core';
import { LocaleService } from '@core/services/locale/locale.service';
import environment from '@environment/oxygenEnvConfig';
import { oddsCardConstant, handicapTemplateMarketName } from '@sharedModule/constants/odds-card-constant';
import { OUTRIGHTS_CONFIG } from '@core/constants/outrights-config.constant';
import { IOutrightsConfig } from '@shared/models/outrights-config.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { ISportConfig } from '@core/services/cms/models';
import { MarketTypeService } from '@app/shared/services/marketType/market-type.service';
import { IEventMarketConfig } from '@app/core/models/event-market-config.model';

@Injectable()
export class OddsCardHeaderService {

  private readonly marketTypes: Array<string> = oddsCardConstant.MARKET_TYPES;
  private readonly OUTRIGHTS_CONFIG: IOutrightsConfig = OUTRIGHTS_CONFIG;
  private readonly racingData: any = environment.CATEGORIES_DATA.racing;

  constructor(
    private locale: LocaleService,
    private coreTools: CoreToolsService,
    private marketTypeService: MarketTypeService
  ) {}

  /**
   * Check if all events in section are special
   * For such events we don't show fixture header
   */
  isSpecialSection(eventEntities: ISportEvent[], sportConfig: ISportConfig): boolean {
    return _.every(eventEntities, event => {
      return this.isSpecialEvent(event, sportConfig);
    });
  }

  /**
   * Get event sport name
   */
  getSportName(event: ISportEvent): string {
    return event.categoryName.toLowerCase().replace(/\s|\/|\|/g, '');
  }

  /**
   * Check if event is special
   * For such events we don't show fixture header
   */
  isSpecialEvent(event: ISportEvent, sportConfig: ISportConfig): boolean {
    if (!sportConfig) {
      return;
    }
    let sortCodeList; // Checks if event - OutRight.
    sortCodeList = this.OUTRIGHTS_CONFIG.sportSortCode;
    if (this.isOutrightSport(event.categoryCode, sportConfig)) {
      sortCodeList = this.OUTRIGHTS_CONFIG.outrightsSportSortCode;
    }
    if(event.categoryCode.toLowerCase() === environment.CATEGORIES_DATA.golfSport &&
        (environment.CATEGORIES_DATA.specialMarkets.includes(event.typeName) ||
        (event.drilldownTagNames && event.drilldownTagNames.includes(environment.CATEGORIES_DATA.specialTagCode)))) {
      sortCodeList = this.OUTRIGHTS_CONFIG.outrightsSportSortCode;
    }

    // Checks if event - Enhance Multiples.
    const isEnhanceMultiples =
    _.contains(sportConfig.specialsTypeIds, Number(event.typeId));

    const isOutright = sortCodeList.indexOf(event.eventSortCode) !== -1;
    let inHandicapMathResult: boolean;
    // The below method returns always the first match of market not based on the selected market
    // this.marketTypeService.getDisplayMarketConfig(sportMarketNames, marketNames)
    if (!environment.CATEGORIES_DATA.categoryIds.includes(event.categoryId)) {
      const displyMarketConfig: IEventMarketConfig =
        this.marketTypeService.getDisplayMarketConfig(sportConfig.config.request.marketTemplateMarketNameIntersects, event.markets);
      inHandicapMathResult = displyMarketConfig && displyMarketConfig.displayMarketName === handicapTemplateMarketName;
    }

    // check if event special (Enhance Multiples or OutRight).
    return isEnhanceMultiples || isOutright || inHandicapMathResult;
  }

  /**
   * Check templateMarketName
   */
  isHomeDrawAwayMarketType(templateMarketName: string): boolean {
    return _.contains(this.marketTypes, templateMarketName);
  }

  isRacing(sportId: string): boolean {
    return _.some(this.racingData, (elem: { id: string; }) => elem.id === sportId);
  }

  /**
   * Get locale from string
   *
   * @param {string} arr
   * @returns {Array}
   */
  getLocale(arr: string): Array<string> | string {
    return arr ? _.map(arr.split(','), item => {
      return +item ? item : this.locale.getString(`sb.${item}`);
    }) : '';
  }


  /**
   * Check for showing/hiding component (should contain minimum one market)
   */
  showComponent(marketNames: string[], selectedMarket?: string): boolean {
    if (marketNames.length === 0) {
      return false;
    }

    if (!selectedMarket) {
      return true;
    }

    return _.intersection(selectedMarket.split(','), marketNames).length > 0;
  }

  /**
   * Get market by template market name
   */
  getMarketByTemplateMarketName(eventMarkets: IMarket[], selectedMarket: string, isFilterByTemplateMarketName: boolean): IMarket {
    if (isFilterByTemplateMarketName && selectedMarket) {
      return _.find(eventMarkets, eventMarket => (selectedMarket.toLowerCase() === eventMarket.name.toLowerCase() || selectedMarket.toLowerCase() === eventMarket.templateMarketName.toLowerCase()));
    }
    return eventMarkets[0];
  }

  /**
   * Get odds card header by view type
   */
  getHeaderByMarketName(isFootballMarket: boolean, market: IMarket): string | void {
    let header;
    const templateMarketName = market && market.templateMarketName.toLowerCase();
    if(isFootballMarket){
    if (this.isHomeDrawAwayMarketType(market.templateMarketName)) {
      header = 'homeDrawAwayType';
    }

    if (templateMarketName === 'to win to nil') {
      header = 'homeAwayType';
    }

    if (templateMarketName === 'score goal in both halves') {
      header = 'yesNoType';
    }
  }
    return header;
  }

  /**
   * Get odds card header by view type
   */
  getHeaderByViewType(viewType: string, outcomesCount: number, sportName: string): string | void {
    let header;

    if (viewType === 'Scorer' ||
      viewType === 'WDW' ||
      outcomesCount === 3
    ) {
      header = sportName === 'golf' ? 'oneThreeType' : 'homeDrawAwayType';
    }
    return header;
  }

  /**
   * Checks if any event shown has comments with scores
   * @param events
   * @returns {boolean}
   */
  isEventsHaveScores(events: ISportEvent[]): boolean {
    return events.some((event: ISportEvent) => this.isEventHasScore(event));
  }

  /**
   * Sort events so those with comments and scores would be displayed first
   * @param events
   */
  sortEventsByScores(events: ISportEvent[]): void {
    events.sort((a: ISportEvent, b: ISportEvent) => {
      const aHasScores = this.isEventHasScore(a);
      const bHasScores = this.isEventHasScore(b);
      if (aHasScores && !bHasScores) {
        return -1;
      }
      if (!aHasScores && bHasScores) {
        return 1;
      }
      return 0;
    });
  }

  /**
   * Checks if single event has scores
   * @param event ISportEvent
   * @returns {boolean}
   */
  private isEventHasScore(event: ISportEvent): boolean {
    return this.coreTools.hasOwnDeepProperty(event, 'comments.teams.home.score') ||
      this.coreTools.hasOwnDeepProperty(event, 'comments.teams.player_1');
  }

  /**
   * Checks if sport is outright
   */
  private isOutrightSport(categoryCode: string, sportConfig: ISportConfig): boolean {
    if (categoryCode && categoryCode.toLowerCase() === environment.CATEGORIES_DATA.golfSport) {
      return _.indexOf(this.OUTRIGHTS_CONFIG.outrightsSports, categoryCode) !== -1;
    }
    return _.indexOf(this.OUTRIGHTS_CONFIG.outrightsSports, categoryCode) !== -1 || sportConfig.config.isOutrightSport;
  }

  /**
   * Abbreviations for SLP where market name is long
   * @param title 
   * @returns string : Market Name
   */
  getMultiTemplateHeader(title): string {
    if (title === '60 Minute Betting') {
      return '60 Min'
    } else {
      const translatedTitle = this.locale.getString('sb.' + title.toLowerCase().replace(/[^\w]/g, ""));
      return translatedTitle === 'KEY_NOT_FOUND' ? title : translatedTitle;
    }
  }
}
