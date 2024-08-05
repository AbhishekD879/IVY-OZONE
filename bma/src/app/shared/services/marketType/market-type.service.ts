import * as _ from 'underscore';
import { Injectable } from '@angular/core';
import { IMarket } from '@core/models/market.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IEventMarketConfig } from '@app/core/models/event-market-config.model';

@Injectable()
export class MarketTypeService {
  /**
   * The list of marketMeaningMajor codes of 'Over/Under' type:
   * - 'L' - Higher/lower;
   * - 'I' - Higher/lower with split line.
   *
   * @type {Array}
   */
 private overUndeMeaningMajorCodes = ['L', 'I'];

 /**
  * The list of combined market's meaning codes for 'Home/Draw/Away' type:
  * - '-|MR' - Match result (W/D/W);
  * - '-|H1' - 1st half result;
  * - '-|H2' - 2nd half result.
  *
  * @type {String}
  */
 private matchResultMeaningCodes = ['-|MR', '-|H1', '-|H2'];
 
 /**
  * The list of market "templateMarketName" properties
  * for 'Home/Draw/Away' and 'Home/Away/No Goal' types:
  * @type {[string]}
  */
 private homeDrawAwayTemplateMarketNames = ['Extra-Time Result', 'Next Team to Score'];
 
 /**
  * The list of market "templateMarketName" properties
  * for '1/Draw/2' types:
  * @type {[string]}
  */
 private oneDrawTwoTemplateMarketNames: Array<string> = ['Fight Betting'];
 
 /**
  * The list of market "templateMarketName" properties
  * for '1/TIE/2' type:
  * @type {[string]}
  */
 private OneTieTwoMarketNames: Array<string> = ['60 Minutes Betting', '60 Minute Betting', '2 Ball Betting', 'Most 180s', 'Hole Head To Head', 'Hole Winner'];
 private matchResultNames: Array<string> = ['Match Result', 'Match Betting'];
 
 /**
  * The list of DispSortName fields for 'Yes/No' type:
  * - 'BO' - Both/One/Neither Team to Score;
  * - 'GB' - Score Goal in Both Halves.
  *
  * @type {Array}
  */
 private yesNoDispSortNames = ['BO', 'GB'];
 
 private sport = {
   dartsId: '13',
   boxingId: '9'
 };
  private readonly marketNameRegexp: RegExp = /\|/g;

  isMatchResultType(marketEntity: IMarket): boolean {
    return marketEntity && _.contains(this.matchResultMeaningCodes, this.combineMeaningCode(marketEntity));
  }

  isHomeDrawAwayType(marketEntity: IMarket): boolean {
    return marketEntity && (_.contains(this.homeDrawAwayTemplateMarketNames, marketEntity.templateMarketName)
      || marketEntity.outcomes && marketEntity.outcomes.length === 3);
  }

  /**
   * Checks if any event contains Market with 'Match result' type
   */
  someEventsAreMatchResultType(events: ISportEvent[], selectedMarketName: string, isFilteredByTemplateMarketName: boolean): boolean {
    // If no market is selected - check if any market is Match Result
    if (!selectedMarketName) {
      return _.some(events, event => {
        return _.some(event.markets, this.isMatchResultType.bind(this));
      });
    }
    // If market is selected - test if matching markets are Match Result
    return _.some(events, event => {
      let market;

      if (isFilteredByTemplateMarketName) {
        market = _.findWhere(event.markets, { templateMarketName: selectedMarketName });
      } else {
        market = _.findWhere(event.markets, { name: selectedMarketName });
      }
      return this.isMatchResultType(market);
    });
  }

  isOverUnderType(marketEntity: IMarket): boolean {
    return marketEntity && _.contains(this.overUndeMeaningMajorCodes, marketEntity.marketMeaningMajorCode);
  }
  // if categoryId equals 13 &  (for Darts Sport)
  isOneTieTwoType(marketEntity: IMarket, categoryId: string): boolean {
    return marketEntity && marketEntity.outcomes.length === 3
      && (this.OneTieTwoMarketNames.includes(marketEntity.templateMarketName)
        || (this.matchResultNames.includes(marketEntity.templateMarketName) && categoryId === this.sport.dartsId));
  }

  // if categoryId equals 9 & (for Boxing Sport)
  isOneDrawTwoType(marketEntity: IMarket, categoryId: string): boolean {
    return marketEntity && marketEntity.outcomes.length === 3
      && (this.oneDrawTwoTemplateMarketNames.includes(marketEntity.templateMarketName)
      && categoryId === this.sport.boxingId);
  }

  isYesNoType(marketEntity: IMarket): boolean {
    return marketEntity && _.contains(this.yesNoDispSortNames, marketEntity.dispSortName);
  }

  isHeader2Columns(marketEntity: IMarket): boolean {
    return !!marketEntity && (!this.isMatchResultType(marketEntity)
                            && !this.isHomeDrawAwayType(marketEntity)
                            || this.isOverUnderType(marketEntity)
                            || this.isYesNoType(marketEntity));
  }

  /**
   * Combines 'marketMeaningMajorCode' and 'marketMeaningMinorCode' codes.
   */
  combineMeaningCode(marketEntity: IMarket): string {
    return `${marketEntity.marketMeaningMajorCode}|${marketEntity.marketMeaningMinorCode}`;
  }

  getDisplayMarketConfig(sportMarketNames: string, markets: IMarket[] | string[]): IEventMarketConfig {
    const eventMarketConfig: IEventMarketConfig = {} as any;
    if (typeof (markets[0]) === 'string' && (markets as string[]).includes('Match Result')) { 
      (markets as string[]).push('Match Betting'); 
    }
    if (sportMarketNames) {
      const primaryMarketNames: string[] = sportMarketNames.replace(this.marketNameRegexp, '').split(',');
      const displayMarketNames: string[] = [];
      const displayMarkets: IMarket[] = [];
      primaryMarketNames.forEach((primaryMarketName: string) => {
        if (typeof (markets[0]) === 'string') {
          (markets as string[]).includes(primaryMarketName) && displayMarketNames.push(primaryMarketName);
        } else {
          const displayMarket = (markets as IMarket[]).find((market: IMarket) => {
            return (market.templateMarketName === primaryMarketName || market.name === primaryMarketName);
          });
          displayMarket && displayMarkets.push(displayMarket);
          displayMarket && displayMarketNames.push(primaryMarketName);
        }
      });

      eventMarketConfig.displayMarketName = displayMarketNames.shift();
      eventMarketConfig.displayMarket = displayMarkets.length && displayMarkets.shift();
    }

    return eventMarketConfig;
  }

  extractMarketNameFromEvents(events: ISportEvent[], isFilterByTemplateMarketName?: boolean): string[] {
    const marketNames = _.reduce(events, (accumulator, event) => {
      const eventMarketNames = (event.markets || []).map(market => {
        if (isFilterByTemplateMarketName) {
          if (market.templateMarketName === 'Match Betting') {
            market.templateMarketName = 'Match Result';
          }
          return market.templateMarketName;
        }

        return market.name;
      });

      accumulator.push(...eventMarketNames);

      return accumulator;
    }, []);
    return marketNames;
  }
}
