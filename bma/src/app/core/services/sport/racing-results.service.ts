import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { LoadByPortionsService } from '@app/ss/services/load-by-portions.service';
import { SiteServerRequestHelperService } from '@core/services/siteServerRequestHelper/site-server-request-helper.service';
import { LocaleService } from '@core/services/locale/locale.service';

import { IEventsIds, IRacingResult, IRuleDeductionResponse, INcastDividendResponse } from '@sb/models/dividends.model';
import { IRacingEvent } from '@core/models/racing-event.model';
import { IOutcome } from '@core/models/outcome.model';
import { IDividend } from '@core/models/dividend.model';
import { IRuleDeduction } from '@core/models/rule-deduction.model';
import { IRacingMarket } from '@core/models/racing-market.model';
import {
  IRacingResultedEventResponse,
  IResultedOutcomeResponse,
  IRacingResultedPriceResponse,
  IResultedMarketResponse
} from '@core/models/racing-result-response.model';
import { dividendsTypes, pricesTypes } from '@core/services/racing/constants/racing.constants';

import { HorseracingService } from '@coreModule/services/racing/horseracing/horseracing.service';
import { GreyhoundService } from '@coreModule/services/racing/greyhound/greyhound.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { TemplateService } from '@shared/services/template/template.service';
import { IRaceResultRunnersData } from '../racing/racingPost/racing-post.model';

@Injectable()
export class RacingResultsService {
  constructor(private loadByPortionsService: LoadByPortionsService,
              private localeService: LocaleService,
              private siteServerRequestHelperService: SiteServerRequestHelperService,
              private siteServer: SiteServerService,
              private horseRacingService: HorseracingService,
              private greyhoundService: GreyhoundService,
              private routingState: RoutingState,
              private templateService: TemplateService
  ) {}

  /**
   * GetRacing results, map data to event, add favourite labels,
   * filter outcomes by positions and nonrunners,
   * fetch dividends and rules 4 deduction for WEW market with results
   */
  getRacingResults(event: IRacingEvent, isFullResultsRequired: boolean): Promise<IRacingEvent> {
    const requestParams = this.racingService.getConfig().request;
    delete requestParams.resultedOutcomeResultCodeNotEquals;
    delete requestParams.resultedMarketPriceTypeCodesIntersects;
    delete requestParams.resultedPriceTypeCodeToDisplay;

    return this.siteServer.loadResultsOfEvent(requestParams, event)
      .then((response: IRacingResultedEventResponse[]) => {

          // W, P, L, V resultCodes runners
          this.mapResultsToOutcomes(response, event);

          if (event.resultedWEWMarket.hasPositions) {
            this.findNonRunners(event.resultedWEWMarket);

            if (event.resultedWEWMarket.hasResults) {         // if SP price is, Favourites can be calculated
              // remove V and with no SP price runners
              this.removeVoidRunners(event.resultedWEWMarket, event);
              
              // all W, P, L runners with SP price take part in favourite calculation
              this.racingService.addFavouriteLabelToOutcomesWithResults(event.resultedWEWMarket.outcomes);
            }
            
            if(isFullResultsRequired) {
              // hadle all L runners and with and without position 
              this.loseRunners(event.resultedWEWMarket);
            }

            // remove L runners and with no position
            this.removeLoseRunners(event.resultedWEWMarket);
            this.sortOutcomesByPositions(event.resultedWEWMarket);
            this.getRacingRulesAndDividends(event, event.resultedWEWMarket,
              event.resultedWEWMarket.nonRunners && event.resultedWEWMarket.nonRunners.length > 0);

          } else {
            // handle all V runners, event is canceled, all become non runners
              this.makeVoidMarket(event.resultedWEWMarket);
            event.voidResult = true;
          }

        return Promise.resolve(event);
      });
  }

  /**
   * Fetches dividends and rules4deduction for resulted event
   * The structure of response:
   * Array of racingResult -> children -> i: finalPosition(ignored) or ncastDivident or rule4deduction
   * Map result into event,
   * leave dividends for winners only and configured in TI (FC/TC enable)
   * filter rule 4 deduction if at least one non runner exists
   */
  getRacingRulesAndDividends(event: IRacingEvent, resultedMarket: IRacingMarket, existNonRunner: boolean): void {
    this.loadByPortionsService
      .get((data: IEventsIds) => this.siteServerRequestHelperService.getRacingResultsForEvent(data, true),
        {}, 'eventsIds', [ event.id ])
      .then((response: IRacingResult[]) => {
        this.mapRulesDividendsToOutcomes(response, resultedMarket, existNonRunner);
        this.filterDividends(resultedMarket);
        this.filterRulesDeduction(resultedMarket);
      });
  }

  /**
   * Returns horseracing or greyhound service
   */
  private get racingService(): HorseracingService | GreyhoundService {
    const segment = this.routingState.getCurrentSegment();
    return segment.indexOf('horseracing') >= 0 ? this.horseRacingService : this.greyhoundService;
  }

  private set racingService(value: HorseracingService | GreyhoundService){}

  /**
   * Saves nonRunners in separate market property
   */
  private findNonRunners(market: IRacingMarket): void {
    market.nonRunners = market.outcomes.filter((outcome: IOutcome) =>
      outcome.results.resultCode === 'V' && outcome.name.indexOf('N/R') !== -1);
    market.nonRunners.forEach((outcome: IOutcome) => {
      outcome.nonRunner = true;
      outcome.name = outcome.name.replace('N/R', '');
    });
  }

  /**
   * Removes outcomes with resultCode Void (=nonRunners)
   */
  private removeVoidRunners(market: IRacingMarket, event: IRacingEvent): void {
    if (event.isUKorIRE && event.categoryCode === 'GREYHOUNDS') {
      market.outcomesWithoutPrices = market.outcomes.filter((outcome: IOutcome) =>
      outcome.results.resultCode !== 'V' && !outcome.results.priceDec);
    }
    market.outcomes = market.outcomes.filter((outcome: IOutcome) =>
      outcome.results.resultCode !== 'V' && outcome.results.priceDec);
  }


    /**
   * Removes outcomes with resultCode Lose and adding to unplaced
   */
     private loseRunners(market: IRacingMarket): void {
      let Position = []
      let Without_Position = []
      Position = market.outcomes.filter((outcome: IOutcome) =>
      outcome.results.resultCode === 'L' && outcome.results.position);
      Without_Position = market.outcomes.filter((outcome: IOutcome) =>
      outcome.results.resultCode === 'L' && !outcome.results.position);
      market.unPlaced = Position.concat(Without_Position);
    }
    
  /**
   * Removes outcomes with resultCode Lose
   */
  private removeLoseRunners(market: IRacingMarket): void {
    market.outcomes = market.outcomes.filter((outcome: IOutcome) =>
  outcome.results.resultCode !== 'L' && outcome.results.position);
  }

  /**
   * Map positions from one-api in placed section
   */
  mapResultPositionPlaced(winHorses: IOutcome[], resultedHorsesData:IRaceResultRunnersData[]) {
    winHorses.forEach((horse: IOutcome) => {
      resultedHorsesData.forEach((item:IRaceResultRunnersData) => {
        if (item.saddle === horse.runnerNumber) {
            const isHorseExists = resultedHorsesData.find(rData => rData.saddle === horse.runnerNumber);
            if (isHorseExists) {
              horse.results.position = isHorseExists.position;
              horse.position = isHorseExists.position;
            }
        }
      });
    });
    return { winHorses, resultedHorsesData}
  }

  /**
   * Map positions from one-api in Unplaced section
   */
  mapResultPositionUnplaced(loseHorses:IOutcome[], resultedHorsesData:IRaceResultRunnersData[], event:IRacingEvent) {
    loseHorses.forEach((horse: IOutcome) => {
      resultedHorsesData.forEach((item:IRaceResultRunnersData) => {
        if (item.saddle === horse.runnerNumber) {
            const isHorseExists = resultedHorsesData.find(rData => rData.saddle === horse.runnerNumber);
            if (isHorseExists) {
              horse.results.position = isHorseExists.position;
              horse.position = isHorseExists.position;
              if (isHorseExists.position === "0") {
                horse.results.resultCode = isHorseExists.raceOutcomeCode;
                horse.resultCode = isHorseExists.raceOutcomeCode;
              }
            }
        }
      });
    });
    event.resultedWEWMarket.outcomes = _.sortBy(event.resultedWEWMarket.outcomes, (outcome: IOutcome) => +outcome.results.position);
    event.resultedWEWMarket.unPlaced = _.sortBy(event.resultedWEWMarket.unPlaced, (outcome: IOutcome) => +outcome.results.position);
    let positions = []
    let without_position = []
    positions = event.resultedWEWMarket.unPlaced.filter(position =>
      position.results.position !== '0' && position.results.resultCode === "L" && position.results.position !== "");
    without_position = event.resultedWEWMarket.unPlaced.filter(position =>
      position.results.position === '0' || position.results.position === "");
    event.resultedWEWMarket.unPlaced = positions.concat(without_position);

    return { loseHorses, resultedHorsesData, event}
  }

  /**
   * Creates outcomes from response results (resultedOutcomes with W, P, L, V resultCodes)
   * response.length && response[0].resultedEvent ? response[0].resultedEvent.children[0] : undefined;
   */
  private mapResultsToOutcomes(response: IRacingResultedEventResponse[], event: IRacingEvent): void {
    const responseMarket = this.getWinOrEachWay(response);
    if (responseMarket) {
      // preparing IMarket instance for event
      const resultedMarket: IRacingMarket = _.extend({}, responseMarket.resultedMarket);
      if (responseMarket.resultedMarket.children && responseMarket.resultedMarket.children.length) {
        resultedMarket.outcomes = [];
        _.forEach(responseMarket.resultedMarket.children, (value: IResultedOutcomeResponse) => {
          resultedMarket.outcomes.push(this.createResultedOutcome(value, resultedMarket, event));
        });
      } else {
        throw new Error('No results in resulted market');
      }
      delete resultedMarket.children;
      const drilldownTagNames =  response && response[0].resultedEvent.drilldownTagNames;
      const drilldownTagNamesArray = drilldownTagNames && drilldownTagNames.split(",");
      if(drilldownTagNamesArray && drilldownTagNamesArray.includes('EVFLAG_AVD')){
        event.isReplayStreamAvailable = true;
      }else {
        event.isReplayStreamAvailable = false;
      }
      event.resultedWEWMarket = _.extend({}, resultedMarket);
      this.formMarketInfo(event);
    } else {
      throw new Error('No resultedMarket in response');
    }
  }

  /**
   * There is some lack of market info needed for Racing results page UI (terms, drilldownTags, cashoutAvail, viewType)
   * We can form terms manually, but other properties to borrow from
   * event.sortedMarkets[0] if its id = resultedWEWMarket.id otherwise return nulls
   */
  private formMarketInfo(event: IRacingEvent): void {
    const wewMarket = event.resultedWEWMarket,
       isWewInEvent = event.sortedMarkets[0] ? event.sortedMarkets[0].id === wewMarket.id : false;

    wewMarket.terms = this.templateService.genTerms(event.resultedWEWMarket);
    if (!wewMarket.cashoutAvail) {
      wewMarket.cashoutAvail = isWewInEvent ? event.sortedMarkets[0].cashoutAvail : '';
    }
    if (!wewMarket.viewType) {
      wewMarket.viewType = isWewInEvent ? event.sortedMarkets[0].viewType : '';
    }
    if (!wewMarket.drilldownTagNames) {
      wewMarket.drilldownTagNames = isWewInEvent ? event.sortedMarkets[0].drilldownTagNames : '';
    }
  }

  /**
   * Prepares IOutcome instance for event market
   */
  private createResultedOutcome(value: IResultedOutcomeResponse, market: IRacingMarket, event: IRacingEvent): IOutcome {
    const resultedOutcome = _.extend({}, value.resultedOutcome);
    // fill outcome with results
    if (value.resultedOutcome.resultCode !== 'V') {
      const spPrice = _.find(value.resultedOutcome.children,
        (prItem: IRacingResultedPriceResponse) =>
          (prItem.resultedPrice.priceTypeCode === pricesTypes.SP || event.isVirtual) && prItem.resultedPrice.priceDec);
      if (spPrice) {
        resultedOutcome.results = spPrice.resultedPrice;
        if (!market.hasResults) {
          market.hasResults = true;                 // if at least one priceDec exists in result market
        }
      } else {
        resultedOutcome.results = {};
      }
      if (value.resultedOutcome.position) {
        if (!market.hasPositions) {
          market.hasPositions = true;                 // if at least one position exists
        }
        resultedOutcome.results.position = value.resultedOutcome.position;
      }
    } else {
      resultedOutcome.results = {};
    }
    resultedOutcome.results.resultCode = value.resultedOutcome.resultCode;

    delete resultedOutcome.children;
    return resultedOutcome;
  }

  /**
   * Extends event with rule4deductions and dividends,
   * Rule 4 deductions available if at least one non runner exists
   */
  private mapRulesDividendsToOutcomes(rawServerResponse: IRacingResult[], resultedMarket: IRacingMarket, existNonRunner: boolean): void {
    const responseResults = rawServerResponse[0].racingResult.children;
    resultedMarket.dividends = [];
    resultedMarket.rulesFourDeduction = existNonRunner ? [] : null;
    _.forEach(responseResults, (value: INcastDividendResponse | IRuleDeductionResponse) => {
      if (value) {
        if (resultedMarket.ncastTypeCodes && (value as INcastDividendResponse).ncastDividend &&
          resultedMarket.id === (value as INcastDividendResponse).ncastDividend.marketId) {
          resultedMarket.dividends.push({
            type: (value as INcastDividendResponse).ncastDividend.type,
            name: this.localeService.getString(`racing.dividend${(value as INcastDividendResponse).ncastDividend.type}`),
            value: (value as INcastDividendResponse).ncastDividend.dividend,
            runnerNumbers: (value as INcastDividendResponse).ncastDividend.runnerNumbers
          });
        }
        if ((value as IRuleDeductionResponse).rule4Deduction && resultedMarket.id ===
          (value as IRuleDeductionResponse).rule4Deduction.marketId && existNonRunner) {
          resultedMarket.rulesFourDeduction.push((value as IRuleDeductionResponse).rule4Deduction);
        }
      }
    });
  }

  /**
   * Sorts outcomes by position
   */
  private sortOutcomesByPositions(market: IRacingMarket): void {
    market.outcomes = _.sortBy(market.outcomes, (outcome: IOutcome) => +outcome.results.position);
    market.unPlaced = _.sortBy(market.unPlaced, (outcome: IOutcome) => +outcome.results.position);
  }

  /**
   * Sorts outcomes by runnerNumber
   */
  private makeVoidMarket(market: IRacingMarket): void {
    market.nonRunners = _.sortBy(market.outcomes, (outcome: IOutcome) => +outcome.runnerNumber);
    _.forEach(market.nonRunners, (outcome: IOutcome) => {
      outcome.nonRunner = true;
      outcome.name = outcome.name.replace('N/R', '');
    });
    market.outcomes = [];
  }

  /**
   * Leave dividends of `winners` only
   * Outcomes should be sorted by position before filterDividends
   */
  private filterDividends(market: IRacingMarket): void {
    if (market.dividends && market.dividends.length && market.ncastTypeCodes) {
      const fcWinners = market.outcomes.slice(0, 2).map(outcome => outcome.runnerNumber),
            tcWinners = market.outcomes.slice(0, 3).map(outcome => outcome.runnerNumber),
            fcWinnersStr = fcWinners.toString().concat(','),
            tcWinnersStr = tcWinners.toString().concat(',');

      // filter winners dividends
      market.dividends = market.dividends
        .filter((div: IDividend) =>
          (div.type === 'FC' && this.isNCastEnabled(market, 'FC') &&  div.runnerNumbers === fcWinnersStr) ||
          (div.type === 'TC' && this.isNCastEnabled(market, 'TC') && div.runnerNumbers === tcWinnersStr));

      // format dividend.runnerNumbers to '1st-2nd[-3rd]' based on sorted outcomes
      market.dividends.forEach((div: IDividend) => {
        div.runnerNumbers =
          div.type === 'FC' ? `${fcWinners[0]}-${fcWinners[1]}` : `${tcWinners[0]}-${tcWinners[1]}-${tcWinners[2]}`;
      });

      // show FC type first than TC
      market.dividends.sort((a: IDividend, b: IDividend) => +(a.type > b.type) || -(a.type < b.type));  // alphabetically
    }
  }

  /**
   * Checks if divident is enable in backoffice configuration
   */
  private isNCastEnabled(market: IRacingMarket, nCastCode: string): boolean {
    switch (nCastCode) {
      case dividendsTypes.FC:
        return !!market.ncastTypeCodes.match(/(?=.*SF)(?=.*CF)(?=.*RF)/);
      case dividendsTypes.TC:
        return !!market.ncastTypeCodes.match(/(?=.*CT)(?=.*TC)/);
      default:
        return false;
    }
  }

  /**
   * The only recent rule4deduction have to be shown
   * Finds max finished date (toDate)
   */
  private filterRulesDeduction(market: IRacingMarket): void {
    if (market.rulesFourDeduction && market.rulesFourDeduction.length) {
      const dates = market.rulesFourDeduction.map((rule: IRuleDeduction) => {
        return new Date(rule.toDate).getTime();
      });
      const maxToDate = Math.max(...dates);
      market.rulesFourDeduction = [market.rulesFourDeduction
        .find((rule: IRuleDeduction) => new Date(rule.toDate).getTime() === maxToDate)];
    }
  }

  /**
   * get win or eachway to show resluts
   * return {IResultedMarketResponse}
   */
  private getWinOrEachWay(response: IRacingResultedEventResponse[]): IResultedMarketResponse {
    if ((response.length && response[0].resultedEvent) && (this.checkWinOrEachWayRgx('Win or Each Way',
      response[0].resultedEvent.children[0].resultedMarket.name) ||
      this.checkWinOrEachWayRgx('win or each way', response[0].resultedEvent.children[0].resultedMarket.name))) {
      return response[0].resultedEvent.children[0];
    } else if ((response.length && response[0].resultedEvent) && (this.checkWinOrEachWayRgx('Win or Each Way',
      response[0].resultedEvent.children[1].resultedMarket.name) ||
      this.checkWinOrEachWayRgx('win or each way', response[0].resultedEvent.children[1].resultedMarket.name))) {
      return response[0].resultedEvent.children[1];
    } else {
      return undefined;
    }
  }

  private checkWinOrEachWayRgx(regExp: string, name: string): boolean {
   return new RegExp(regExp, 'g').test(name);
  }
}

