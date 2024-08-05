import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { IsPropertyAvailableService } from '@sb/services/isPropertyAvailable/is-property-available.service';
import { CashOutLabelService } from '@core/services/cashOutLabel/cash-out-label.service';
import { ScoreMarketService } from '@edp/services/scoreMarket/score-market.service';
import { IOutcomesByTeam, IScorecast, IScoreCastMarkets, ITeam, IScorecastMarket } from '@edp/components/markets/scorecast/scorecast.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { ITeams, ITeamsScores } from '@core/models/team.model';
import { IPrice } from '@core/models/price.model';
import { GtmService } from '@core/services/gtm/gtm.service';

@Injectable()
export class ScorecastService {
  constructor(
    protected scoreMarketService: ScoreMarketService,
    protected isPropertyAvailableService: IsPropertyAvailableService,
    protected cashOutLabelService: CashOutLabelService,
    protected gtmService: GtmService
  ) {}

  /**
   * returns combined price based on correctScore
   * @param {Array} scorecastMarketScorecasts
   * @param {String} goalscorerOutcomeId
   * @param {String} correctScoreOutcomeId
   * @returns {(Object|undefined)}
   */
   getCombinedOutcomePrices(
     scorecastMarketScorecasts: IScorecast[],
     goalscorerOutcomeId: string,
     correctScoreOutcomeId: string
  ): IPrice | null {
    const outcomeCombinations: Object = this.getOutcomeCombinations(scorecastMarketScorecasts, goalscorerOutcomeId);
    if (_.has(outcomeCombinations, correctScoreOutcomeId)) {
      return {
        priceType: 'LP',
        priceNum: outcomeCombinations[correctScoreOutcomeId][1],
        priceDen: outcomeCombinations[correctScoreOutcomeId][2],
        priceDec: outcomeCombinations[correctScoreOutcomeId][3]
      };
    }
    return null;
  }

  /**
   * return outcomes which are teams from MR or MH market if MR is not configured correctly
   * @param {Array} markets
   * @returns {Array}
   */
  getTeams(markets: IMarket[]): any[] {
    return this.scoreMarketService.getTeams(markets);
  }

  /**
   * returns marketEntity which Name matched with given MarketMame Pattern
   * @param {Array} marketsArray
   * @param {String} patternString
   * @returns {(Object|undefined)}
   */
  getMarketByMarketNamePattern(marketsArray: IMarket[], patternString: string): IMarket | undefined {
    const pattern: RegExp = new RegExp(patternString, 'i'),
      marketsArrayLength: number = marketsArray.length;
    let i = 0;

    for (; i < marketsArrayLength; i++) {
      if (pattern.test(marketsArray[i].name)) {
        break;
      }
    }
    return i >= marketsArrayLength ? undefined : marketsArray[i];
  }

  /**
   * return outcomesByTeam based on market name
   * @param {Object} marketEntity
   * @param {Array} teamsArray
   * @returns {Object}
   */
  getMarketOutcomesByTeam(teamsArray: ITeam[], marketEntity: IMarket): IOutcomesByTeam {
    const outcomesByTeam: IOutcomesByTeam = {};
    _.each(teamsArray, (teamEntity: ITeam) => {
      outcomesByTeam[teamEntity.name] = marketEntity.outcomes.filter((outcomeEntity: IOutcome) => {
        return outcomeEntity.outcomeMeaningMinorCode === teamEntity.outcomeMeaningMinorCode;
      });
    });
    return outcomesByTeam;
  }

  /**
   * returns first not suspended scorecast market property name
   * @param {Object} scorecastMarkets
   * @returns {String}
   */
  getDefaultScorecastMarketName(scorecastMarkets: IScoreCastMarkets): string {
    const marketName: string = _.findKey(scorecastMarkets,
      (m: IScorecastMarket) => m.market.marketStatusCode !== 'S' && m.goalscorerMarket.marketStatusCode !== 'S');
    return marketName || Object.keys(scorecastMarkets)[0];
  }

  /**
   * Find combined outcome by team scores result.
   * @param {Object} teams
   * @param {Array} outcomes
   * @returns {(Object|undefined)}
   */
  getCombinedOutcome(teams: ITeams, outcomes: IOutcome[]): IOutcome {
    return this.scoreMarketService.getCombinedOutcome(teams, outcomes);
  }

  /**
   * Find max available scores for teams.
   * @param {Array} outcomes
   * @returns {Object}
   */
  getMaxScoreValues(outcomes: IOutcome[]): ITeamsScores {
    return this.scoreMarketService.getMaxScoreValues(outcomes);
  }

  /**
   * get function to check if cashout is available
   * @returns {Function}
   */
  get isAnyCashoutAvailable(): Function {
    return this.isPropertyAvailableService.isPropertyAvailable(
      this.cashOutLabelService.checkCondition.bind(this.cashOutLabelService));
  }
  set isAnyCashoutAvailable(value:Function){}

  /**
   * returns outcome combinations based on goalscorer
   * @param {Array} scorecasts
   * @param {String} goalscorerOutcomeId
   * @returns {Object}
   */
  private getOutcomeCombinations(scorecasts: IScorecast[], goalscorerOutcomeId: string): Object {
    const combinations = {};
    const foundScorecast = _.findWhere(scorecasts, { scorerOutcomeId: goalscorerOutcomeId });
    const combinationsArray = (foundScorecast && foundScorecast.scorecastPrices.split(',')) || [];

    let groupId;

    combinationsArray.splice(-1, 1);
    for (let i = 0, combinationsArrayLength = combinationsArray.length; i < combinationsArrayLength; i++) {
      if ((i % 4) === 0) {
        groupId = combinationsArray[i];
        combinations[groupId] = [];
        combinations[groupId].push(groupId);
      } else {
        combinations[groupId].push(combinationsArray[i]);
      }
    }
    return combinations;
  }
  setGtmData(switcherText: string): void {
    const gtmData = {
        'event': 'Event.Tracking',
        'component.CategoryEvent': 'scorecast',
        'component.LabelEvent': 'scorecast',
        'component.ActionEvent': 'click',
        'component.PositionEvent': 'not applicable',
        'component.LocationEvent': 'Regular Time',
        'component.EventDetails': switcherText.toLowerCase(),
        'component.URLClicked': 'not applicable'
    };
    this.gtmService.push(gtmData.event, gtmData);
  }

  setBetslipGtmData(eventData: any): void {
        const scorerGtmData = {
      'event': 'Event.Tracking',
      'component.CategoryEvent': 'scorecast',
      'component.LabelEvent': 'scorecast',
      'component.ActionEvent': 'select',
      'component.PositionEvent': `scorecast;${eventData.teamname};${eventData.playerName};${eventData.result}`,
      'component.LocationEvent': 'Regular Time',
      'component.EventDetails': eventData.selectedScorecastTab,
      'component.URLClicked': 'not applicable'
      } 
    this.gtmService.push(scorerGtmData.event, scorerGtmData) 
  }
    
}


