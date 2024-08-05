import { Injectable } from '@angular/core';
import {
  IBybSelection,
  IBybSelectionProgress,
  IBybSelectionStatus,
  IConditions
} from '@lazy-modules/bybHistory/models/byb-selection.model';
import { IBetHistoryBet } from '@app/betHistory/models/bet-history.model';
import { IBetHistoryOutcome, IExternalStatsLink } from '@core/models/outcome.model';
import {
  DOUBLE_TEAMS,
  PERIODS,
  STATS_CATEGORIES,
  STATS_CATEGORIES_SINGULAR,
  STATUSES,
  TEAMS,
  BET_STATUSES,
  BET_STATS_LIMIT
} from '@lazy-modules/bybHistory/constants/byb-5aside-markets-config.constant';
import {
  PLAYER_STATS, StatCategoryUtilityService
} from '@lazy-modules/bybHistory/services/betTrackingRules/stat-category-utility.service';
import {
  ICardsInfo,
  IGoalInfo,
  IPlayer,
  IPlayersSimple,
  IRedCardsByTeams,
  IScore,
  IScoreboardStatsUpdate,
  IScoreByTeams,
  IScoreByTime,
  ITeams
} from '@lazy-modules/bybHistory/models/scoreboards-stats-update.model';

@Injectable()
export class BetTrackingRulesHelperService {
  constructor(protected statCategoryUtilityService: StatCategoryUtilityService) {}

  /**
   * Get particular stats category object from statCategoryUtilityService
   * e.g. getScore, getAssists
   * @param selection
   * @param update
   */
  protected getStatCategoryObj(selection: IBybSelection, update: IScoreboardStatsUpdate): any {
    const handler = this.statCategoryUtilityService[`get${selection.config.statCategory}`]; // Get stats from statCategoryUtilityService

    if (!handler) {
      console.warn(`No ${selection.config.statCategory} were found in statCategoryUtilityService`);
      return {};
    }

    return handler(selection.config.generalInformationRequired, update);
  }

  /**
   * Get progress of selection
   * @param selection  Byb selection
   * @param bet        History bet
   * @param current    current progress value
   */
  protected getSelectionProgress(selection: IBybSelection, bet: IBetHistoryBet, current: number): IBybSelectionProgress {
    const stats = this.getExternalStatsLink(selection);

    if (!stats) {
      return null;
    }

    const target = this.parseStatValue(stats.statValue);
    const isSettled = bet.settled === BET_STATUSES.SETTLED;
    const statsCaterories = isSettled && current === 1 || !isSettled && target === 1 ? STATS_CATEGORIES_SINGULAR : STATS_CATEGORIES;

    const desc = isSettled ? `${current} ${statsCaterories[stats.statCategory]}` :
      `${current} of ${target} ${ statsCaterories[stats.statCategory]}`;

    return { current, target, desc };
  }

  /**
   * Get progress of selection for Booking
   * @param selection  Byb selection
   * @param bet        History bet
   * @param current    current progress value
   * @returns {IBybSelectionStatus}
   */
  protected getBookingSelectionProgress(selection: IBybSelection, bet: IBetHistoryBet, current: number): IBybSelectionProgress {
    const stats = this.getExternalStatsLink(selection);

    if (!stats) {
      return null;
    }

    let target = this.parseStatValue(stats.statValue);
    let updatedTarget: number = target;
    const isSettled: boolean = bet.settled === BET_STATUSES.SETTLED;
    const statsCaterories = this.currentTargetValidate(isSettled, current, target);
    if (this.isUnder(stats.statValue)) {
      updatedTarget = this.underBookingCalculation(target);
    } else if (this.isOver(stats.statValue)) {
      updatedTarget = this.overBookingCalculation(target);
    }
    target = updatedTarget;

    const desc = isSettled ? `${current} ${statsCaterories[stats.statCategory]}` :
    `${current} of ${target} ${ statsCaterories[stats.statCategory]}`;

    return { current, target, desc };
  }

  protected getPlayerScoredInPeriodInfo(update: IScoreboardStatsUpdate, playerId: string) {
    const allGoals: IGoalInfo[] = this.statCategoryUtilityService.getAllGoals(update),
      playerScoredInPeriodInfo = {};

    [PERIODS['1ST_HALF'], PERIODS['2ND_HALF']].forEach((period: string) => {
      const goalsInPeriod = allGoals.filter(goalInfo => goalInfo.period === period);
      playerScoredInPeriodInfo[period] = goalsInPeriod.filter(goalInfo => goalInfo.player &&
        goalInfo.player.providerId === playerId).length;
    });
    return playerScoredInPeriodInfo;
  }

  /**
   * Parse string value as number
   * @param statValue string value
   * Rules:
   * statValue = ">0.5" => 1
   * statValue = "<0.5" => 0
   * statValue = ">=1" => 1
   * statValue = "1" => 1
   * statValue = "=1" => 1
   * @private
   * @returns {number}
   */
  protected parseStatValue(statValue: string): number {
    const pattern = new RegExp(/[\=\>\<]+/, 'g');

    if (statValue.includes('=') || statValue.includes('<')) {
      return Math.floor(Number(statValue.replace(pattern, '')));
    } else {
      return Math.ceil(Number(statValue.replace(pattern, '')));
    }
  }

  /**
   * Get team which scored first in chosen period
   * @param team
   * @param update
   * @param period
   */
  protected getTeamScoredFirst(update: IScoreboardStatsUpdate, period: string): string {
    const periodFilters = {
      [PERIODS['1ST_HALF']]: goalInfo => goalInfo.period === PERIODS['1ST_HALF'],
      [PERIODS['2ND_HALF']]: goalInfo => goalInfo.period === PERIODS['2ND_HALF'],
      [PERIODS.total]: () => true
    };

    const allGoals: IGoalInfo[] = this.statCategoryUtilityService.getAllGoals(update),
      goalsInPeriod = allGoals.filter(periodFilters[period]);

    return goalsInPeriod.length ? goalsInPeriod[0].team : undefined;
  }

  /**
   * Get Team via externalStatsLink contestantId or { home: 1, away: 5 } by outcome name
   * @param selection
   * @param update
   * @private
   * @returns {string}
   */
  protected getTeamByExternalStatsLink(selection: IBybSelection, update: IScoreboardStatsUpdate): string {
    const externalStatsLink: IExternalStatsLink = this.getExternalStatsLink(selection);
    const homeId = update.home && update.home.providerId;
    const awayId = update.away && update.away.providerId;

    if (externalStatsLink && externalStatsLink.contestantId === homeId) {
      return TEAMS.HOME;
    } else if (externalStatsLink && externalStatsLink.contestantId === awayId) {
      return TEAMS.AWAY;
    } else {
      return TEAMS.DRAW;
    }
  }

  /**
   * Get Team Correct Scores by outcome name
   * @param selection
   * @param update
   * @returns IScoreByTime
   */
  protected getTeamCorrectScores(selection: IBybSelection, update: IScoreboardStatsUpdate): IScoreByTime {
    const teamFromSelection = this.statCategoryUtilityService.getHomeAwayTeamByContestantId(update, selection);
    const selectionName = selection.part.outcome[0].name;
    const scoresExtracted = selectionName.match(/\d*-\d*/g); // (1-2)
    const selectionTeamsValue = scoresExtracted[0].split('-');

    if (teamFromSelection === TEAMS.AWAY ) {
      return {home: +selectionTeamsValue[1], away: +selectionTeamsValue[0]};
    } else {
      return {home: +selectionTeamsValue[0], away: +selectionTeamsValue[1]};
    }
  }

  /**
   * Get goals by team and period
   * @param {IGoalInfo[]} goals
   * @param {string} period aka '15:00' | '30:00' | '60:00' | '75:00'
   * @param {string} periodStart for ranges 0-30 | 30 - 60
   * @private
   * @returns { home: IGoalInfo[], away: IGoalInfo[] }
   */
  protected getGoalsByTeamAndPeriod(goals: IGoalInfo[], period: string, periodStart: string = ''): { [key: string]: IGoalInfo[] } {
    return {
      [TEAMS.HOME]: goals.filter((goal: IGoalInfo) => {
        return goal.team === TEAMS.HOME && (periodStart
          ? this.isPeriodReached(goal.time, periodStart) && !this.isPeriodReached(goal.time, period)
          : !this.isPeriodReached(goal.time, period));
      }),
      [TEAMS.AWAY]: goals.filter((goal: IGoalInfo) => {
        return goal.team === TEAMS.AWAY && (periodStart
          ? this.isPeriodReached(goal.time, periodStart) && !this.isPeriodReached(goal.time, period)
          : !this.isPeriodReached(goal.time, period));
      })
    };
  }

  /**
   * Get Team Stats from both home and away team by period
   * Stat - Corners | Cards
   * @param {string} period
   * @param {ITeams} statsCategoryObj
   * @param {string} stat
   * @private
   * @returns { home?: number, away?: number }
   */
  protected getTeamStatsByPeriod(period: string, statsCategoryObj: ITeams, stat: string): { home?: number, away?: number } {
    switch (period) {
    case PERIODS.total: // TOTAL STAT
      return {
        home: statsCategoryObj.home.total[stat],
        away: statsCategoryObj.away.total[stat]
      };
    case PERIODS['1ST_HALF']: // 1ST HALF STAT
      return {
        home: statsCategoryObj.home[PERIODS['1ST_HALF']][stat],
        away: statsCategoryObj.away[PERIODS['1ST_HALF']][stat]
      };
    case PERIODS['2ND_HALF']: // 2ND HALF STATS
      if (statsCategoryObj.home[PERIODS['2ND_HALF']]) {
        return {
          home: statsCategoryObj.home[PERIODS['2ND_HALF']][stat],
          away: statsCategoryObj.away[PERIODS['2ND_HALF']][stat]
        };
      }

      return { home: 0, away: 0 };
    default:
      return  {};
    }
  }

  /**
   * Check if selection is UNDER X.Y
   * @param {string} statValue
   * @private
   * @returns {boolean}
   */
  protected isUnder(statValue: string): boolean {
    return statValue.includes('<');
  }

  /**
   * Check if selection is OVER X.Y
   * @param {string} statValue
   * @private
   * @returns {boolean}
   */
  protected isOver(statValue: string): boolean {
    return statValue.includes('>');
  }

  /**
   * Check if selection is EQUAL
   * @param {string} statValue
   * @private
   * @returns {boolean}
   */
  protected isEqual(statValue: string): boolean {
    return statValue.includes('=');
  }

  /**
   * Get status for MATCH BETTING markets
   * @param goalsObj
   * @param bet
   * @param team
   * @param period
   * @param currentPeriod
   */
  protected getMatchBettingStatus(goalsObj: IScoreByTeams, team: string,
                                period: string, currentPeriod?: string): string {
    let status = '';

    if (goalsObj.score[period]) {
      const { home, away } = goalsObj.score[period];
      const conditions = {
        [ TEAMS.DRAW ]: home === away,
        [ TEAMS.AWAY ]: home < away,
        [ TEAMS.HOME ]: home > away
      };

      if (this.isFirstHalf(period)) {
        status = this.getFirstHalfBettingStatus(conditions, team, currentPeriod);
      } else {
        status = this.getFullMatchStatus(conditions, team);
      }
    } else {
      status = STATUSES.LOSING;
    }

    return status;
  }

  /**
   * Get full match status
   * @param conditions
   * @param team
   */
  protected getFullMatchStatus(conditions: { [key: string]: boolean }, team: string): string {
    let status = '';

    if (conditions[team]) {
      status =  STATUSES.WINNING;
    } else {
      status = STATUSES.LOSING;
    }

    return status;
  }

  /**
   * Get status for first half betting markets
   * @param conditions
   * @param team
   * @param period
   */
  protected getFirstHalfBettingStatus(conditions: { [key: string]: boolean }, team: string, period: string): string {
    let status = '';
    const currentPeriod = this.statCategoryUtilityService.getCurrentPeriod(period);
    const isFirstHalf = this.isFirstHalf(currentPeriod);
    const isSecondHalfOrTotal = this.isSecondHalfOrTotal(currentPeriod);

    if (conditions[team] && isFirstHalf) {
      status =  STATUSES.WINNING;
    } else if (conditions[team] && isSecondHalfOrTotal) {
      status = STATUSES.WON;
    } else if (isFirstHalf) {
      status = STATUSES.LOSING;
    } else {
      status = STATUSES.LOSE;
    }

    return status;
  }

  /**
   * Get status for Double Chance markets
   * @param goalsObj
   * @param bet
   * @param team
   * @param period
   * @param currentPeriod
   */
  protected getDoubleChanceStatus(
    goalsObj: IScoreByTeams,
    team: string,
    period: string,
    currentPeriod?: string
  ): string {
    let status = '';

    if (goalsObj.score[period]) {
      const { home, away } = goalsObj.score[period];
      const conditions = {
        [ DOUBLE_TEAMS.HOME_OR_DRAW ]: home >= away,
        [ DOUBLE_TEAMS.AWAY_OR_DRAW ]: home <= away,
        [ DOUBLE_TEAMS.HOME_OR_AWAY ]: home !== away
      };

      if (this.isFirstHalf(period)) {
        status = this.getFirstHalfBettingStatus(conditions, team, currentPeriod);
      } else {
        status = this.getFullMatchStatus(conditions, team);
      }
    } else {
      status = STATUSES.LOSING;
    }

    return status;
  }

  /**
   * Get status for Correct Score markets
   * @param goalsObj
   * @param team
   * @param period
   * @param currentPeriod
   */
  protected getCorrectScoreStatus(
    goalsObj: IScoreByTeams,
    objTeams: IScoreByTime,
    period: string,
    currentPeriod?: string
  ): string {
    let status = '';

    if (goalsObj.score[period]) {
      const { home, away } = goalsObj.score[period];
      const conditions = {
        forWining: objTeams.home === home && objTeams.away === away,
        forLosing: objTeams.home < home || objTeams.away < away
      };

      if (this.isFirstHalf(period)) {
        return this.getFirstHalfCorrectScoreStatus(conditions, currentPeriod);
      } else {
        return this.getTotalCorrectScoreStatus(conditions);
      }
    } else {
      status = STATUSES.LOSING;
    }

    return status;
  }

  /**
   * Calculate status for Correct Score(1st Half) by parameters
   * @param conditions
   * @param currentPeriod
   */
  protected getFirstHalfCorrectScoreStatus(conditions, currentPeriod): string {
    const isFirstHalf = this.isFirstHalf(currentPeriod);
    const isHalfTime = this.isHalfTime(currentPeriod);
    const isSecondHalfOrTotal = this.isSecondHalfOrTotal(currentPeriod);
    let status = '';

    if (conditions.forWining && (isFirstHalf || isHalfTime)) {
      status = STATUSES.WINNING;
    } else if (conditions.forWining && isSecondHalfOrTotal) {
      status = STATUSES.WON;
    } else if (conditions.forLosing) {
      status = STATUSES.LOSE;
    } else {
      status = STATUSES.LOSING;
    }

    return status;
  }

  /**
   * Calculate status for Correct Score by parameters
   * @param conditions
   */
  protected getTotalCorrectScoreStatus(conditions): string {
    let status = '';

    if (conditions.forWining) {
      status = STATUSES.WINNING;
    } else if (conditions.forLosing) {
      status = STATUSES.LOSE;
    } else {
      status = STATUSES.LOSING;
    }

    return status;
  }

  /**
   * Get status for Red Card markets
   * @param outcomeName
   * @param cardsObj
   * @param period
   * @param currentPeriod
   */
  protected getFullRedsStatus(outcomeName: string, cardsObj: IRedCardsByTeams,
                            period: string, currentPeriod: string): string {
    const isYesOutcome = outcomeName === BET_STATUSES.OUTCOME_NAME_YES;
    const isRedCard = cardsObj.away.periods[period] && cardsObj.away.periods[period].redCards
      || cardsObj.home.periods[period] && cardsObj.home.periods[period].redCards;

    if (this.isFirstHalf(period)) { // 1ST HALF
      return  this.getFirstHalfRedCardsStatus(!!isRedCard, isYesOutcome, currentPeriod);
    }

    return this.getTotalRedCardsStatus(!!isRedCard, isYesOutcome);
  }

  /**
   * Get status for Red Card by participant
   * @param cards
   * @param isYesOutcome
   */
  protected getRedCardsParticipantStatus(cards: number, isYesOutcome: boolean): string {
    const isRedCard = cards > 0;

    return this.getTotalRedCardsStatus(isRedCard, isYesOutcome);
  }

  /**
   * Calculate status for Red Card by parameters
   * @param isRedCard
   * @param isYesOutcome
   */
  protected getTotalRedCardsStatus(isRedCard: boolean, isYesOutcome: boolean): string {
    let status;

    if (isRedCard) {
      status = isYesOutcome ? STATUSES.WINNING : STATUSES.LOSING ;
    } else {
      status = isYesOutcome ? STATUSES.LOSING : STATUSES.WINNING;
    }

    return status;
  }

  /**
   * Calculate status for Red Card(1st Half) by parameters
   * @param isRedCard
   * @param isYesOutcome
   * @param period
   */
  protected getFirstHalfRedCardsStatus(isRedCard: boolean, isYesOutcome: boolean, period: string): string {
    let status = '';
    const currentPeriod = this.statCategoryUtilityService.getCurrentPeriod(period);
    const isFirstHalf = this.isFirstHalf(currentPeriod);
    const isSecondOrTotal = this.isSecondHalfOrTotal(currentPeriod);

    if (isRedCard && isFirstHalf) {
      status = isYesOutcome ? STATUSES.WINNING : STATUSES.LOSING ;
    } else if (isRedCard && isSecondOrTotal) {
      status = isYesOutcome ? STATUSES.WON : STATUSES.LOSE;
    } else if (isFirstHalf) {
      status = isYesOutcome ? STATUSES.LOSING : STATUSES.WINNING;
    } else {
      status = isYesOutcome ? STATUSES.LOSE : STATUSES.WON;
    }

    return status;
  }

  /**
   * Get player status and progress base on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @param {IBetHistoryBet} bet
   * @param {string} stat - depends on PLAYER_STATS
   * @param {string} playerShots - depends on PLAYER_SHOTS
   */
  protected getPlayerStatusAndProgress(
    selection: IBybSelection,
    update: IScoreboardStatsUpdate,
    bet: IBetHistoryBet,
    stat: string,
    playerShots?: string
  ): IBybSelectionStatus {
    const goalsObj = this.getStatCategoryObj(selection, update);
    const { playerId, statValue } = this.getExternalStatsLink(selection);
    const optaStatValue = this.getOptaStatValue(goalsObj, playerId, stat, playerShots);
    if (optaStatValue === null) { // if no player and respective stat found, then no status
      return { status: '' };
    }

    const selectedValue = this.parseStatValue(statValue);
    const status = this.getOverTotalMarketsStatus(optaStatValue, selectedValue);
    const progress = this.getSelectionProgress(selection, bet, +optaStatValue);

    return { status, progress };
  }

  /**
   * Get opta stat value
   * @param {IPlayersSimple} goalsObj
   * @param {string} playerId
   * @param {string} stat - depends on PLAYER_STATS
   * @param {string} playerShots - depends on PLAYER_SHOTS
   */
  protected getOptaStatValue(goalsObj: IPlayersSimple, playerId: string, stat: string, playerShots?: string): number {
    if (
      goalsObj &&
      (goalsObj.home && goalsObj.home.length ||
        goalsObj.away && goalsObj.away.length)
    ) {
      const player = goalsObj.home.find((p: IPlayer) => p.providerId === playerId) ||
        goalsObj.away.find((p: IPlayer) => p.providerId === playerId);

      if (player) {
        const playerStat = player[stat];
        return stat === PLAYER_STATS.SHOTS ? playerStat && playerStat[playerShots] : playerStat;
      }
    }

    return null;
  }

  /**
   * Get TOTAL/2nd HALF UNDER Markets status
   * @param currentValue
   * @param target
   * @param isStrictConditions
   */
  protected getUnderTotalMarketsStatus(currentValue: number, target: number, isStrictConditions?: boolean): string {
    const condition = isStrictConditions ? target > currentValue : target >= currentValue;
    if (condition) {
      return STATUSES.WINNING;
    }

    return STATUSES.LOSE;
  }

  /**
   * Get UNDER Markets status for Booking Points
   * @param currentValue
   * @param target
   * @param isStrictConditions
   * @returns { status }
   */
  protected getUnderBookingStatus(currentValue: number, target: number): string {
    const possibleTarget: boolean = target === BET_STATS_LIMIT.LEAST_POSSIBLE_POINT;
    const conditionMore = possibleTarget ? target >= currentValue : target > currentValue;

    if (conditionMore) {
      return STATUSES.WINNING;
    }

    return STATUSES.LOSE;
  }

  /**
   * Get First Half UNDER Markets status
   * @param currentValue
   * @param target
   * @param period
   */
  protected getUnderFirstHalfMarketsStatus(currentValue: number, target: number, period: string): string {
    const currentPeriod = this.statCategoryUtilityService.getCurrentPeriod(period);
    const isFirstHalf = this.isFirstHalf(currentPeriod);
    const isSecondHalfOrTotal = this.isSecondHalfOrTotal(currentPeriod);

    if (target >= currentValue && isSecondHalfOrTotal) {
      return STATUSES.WON;
    } else if (target >= currentValue && isFirstHalf) {
      return STATUSES.WINNING;
    }

    return STATUSES.LOSE;
  }

  /**
   * Get TOTAL/2nd HALF OVER Markets status
   * @param currentValue
   * @param target
   * @param isStrictConditions
   */
  protected getOverTotalMarketsStatus(currentValue: number, target: number, isStrictConditions?: boolean): string {
    const conditionMore = isStrictConditions ? currentValue > target : currentValue >= target;
    const conditionLess = isStrictConditions ? currentValue <= target : currentValue < target;

    if (conditionLess) {
      return STATUSES.LOSING;
    } else if (conditionMore) {
      return STATUSES.WON;
    }

    return STATUSES.LOSE;
  }

  /**
   * Get First Half OVER Markets status
   * @param currentValue
   * @param target
   * @param period
   */
  protected getOverFirstHalfMarketsStatus(currentValue: number, target: number, period: string): string {
    const currentPeriod = this.statCategoryUtilityService.getCurrentPeriod(period);
    const isFirstHalf = this.isFirstHalf(currentPeriod);

    if (currentValue < target && isFirstHalf) {
      return STATUSES.LOSING;
    } else if (currentValue >= target) {
      return STATUSES.WON;
    }

    return STATUSES.LOSE;
  }

  /**
   * Get TOTAL/2nd HALF EXACT Markets status
   * @param current
   * @param target
   */
  protected getEqualTotalMarketsStatus(current: number, target: number): string {
    if (current === target) {
      return  STATUSES.WINNING;
    } else if (target > current) {
      return  STATUSES.LOSING;
    }

    return  STATUSES.LOSE;
  }

  /**
   * Get 1ST HALF EXACT Markets status
   * @param current
   * @param target
   * @param period
   */
  protected getEqualFirstHalfMarketsStatus(current: number, target: number, period: string): string {
    const currentPeriod = this.statCategoryUtilityService.getCurrentPeriod(period);
    const isFirstHalf = this.isFirstHalf(currentPeriod);

    if (current === target && !isFirstHalf) {
      return STATUSES.WON;
    } else if (current === target && isFirstHalf) {
      return  STATUSES.WINNING;
    } else if (target > current && isFirstHalf) {
      return  STATUSES.LOSING;
    }

    return  STATUSES.LOSE;
  }

  /**
   * Get status for No Cards selection(TO BE SEND OFF market)
   * @param update
   */
  protected getNoRedCardsSelectionStatus(update: IScoreboardStatsUpdate): string {
    const isHomeRedCards = update.cards.home.find(card => card.type === 'red');
    const isAwayRedCards = update.cards.away.find(card => card.type === 'red');
    const isNoRedsCards = !isHomeRedCards && !isAwayRedCards;

    if (isNoRedsCards) {
      return STATUSES.WINNING;
    }

    return this.getNoStatsCategorySelectionStatus(isNoRedsCards);
  }

  /**
   * Get status for No Stats Category(e.g. red cards, goals etc) selection
   * @param condition
   */
  protected getNoStatsCategorySelectionStatus(condition: boolean): string {
    if (condition) {
      return STATUSES.WINNING;
    }
    return STATUSES.LOSE;
  }

  /**
   * Get Ranged Market Status for '15:00' | '30:00' | '60:00' | '75:00' | '0 - 30' | '30 - 60' ranges
   * @param goalsStat
   * @param {boolean} periodReached
   * @param {string} team
   * @private
   * @returns {string}
   */
  protected getRangeMarketStatus(
    goalsStat: { [key: string]: IGoalInfo[] }, periodReached: boolean, team: string): string {
    const home = goalsStat[TEAMS.HOME].length;
    const away = goalsStat[TEAMS.AWAY].length;
    const conditions = {
      [TEAMS.DRAW]: home === away,
      [TEAMS.AWAY]: home < away,
      [TEAMS.HOME]: home > away
    };

    let status: string;

    if (conditions[team] && !periodReached) {
      status = STATUSES.WINNING;
    } else if (conditions[team] && periodReached) {
      status = STATUSES.WON;
    } else if (!periodReached) {
      status = STATUSES.LOSING;
    } else {
      status = STATUSES.LOSE;
    }

    return status;
  }

  protected isFirstHalf(period: string): boolean {
    return period === PERIODS['1ST_HALF'];
  }
  /**
   * @param  {string} period
   * @returns boolean
   */
  protected isHalfTime(period: string): boolean {
    return period === PERIODS['halftime'];
  }

  protected isSecondHalfOrTotal(period: string): boolean {
    return period === PERIODS['2ND_HALF'] || period === PERIODS.total;
  }

  protected getExternalStatsLink(selection: IBybSelection): IExternalStatsLink {
    return (selection.part.outcome[0] as IBetHistoryOutcome).externalStatsLink;
  }

  /**
   * Checks if match time is greater than the given period
   * @param time - 'mm:ss'
   * @param period - One from Periods enum variable '15:00' | '30:00' | '60:00' | '75:00'
   * @private
   * @returns boolean
   */
  protected isPeriodReached(time: string, period: string): boolean {
    if (time === period) {  // e.g. 15:00 === 15:00
      return true;
    }

    const current = time.split(':').map(Number);
    const target = period.split(':').map(Number);

    if (current[0] > target[0]) { // e.g. 16:00 > 15:00
      return true;
    } else {  // e.g. 15:01 > 15:00
      return current[0] === target[0] && current[1] > target[1];
    }
  }

  /**
   * Get status for 1ST/2ND half
   * @param scores
   * @param update
   * @param selection
   */
  protected bothTeamsHalfScoredStatus(scores: IScore, update: IScoreboardStatsUpdate, selection: IBybSelection): string {
    const { statValue } = this.getExternalStatsLink(selection);
    const selectionPeriod = selection.config.period;
    const currentPeriod = this.statCategoryUtilityService.getCurrentPeriod(update.period);
    const isFirstHalf = this.isFirstHalf(currentPeriod);
    let status;
    if (scores[selectionPeriod] && !!scores[selectionPeriod].away && !!scores[selectionPeriod].home) {
      status = this.isUnder(statValue) ? STATUSES.LOSE : STATUSES.WON;
    } else if ((scores[selectionPeriod] && (scores[selectionPeriod].away === 0 || scores[selectionPeriod].home === 0)) &&
      (selectionPeriod === PERIODS['1ST_HALF'] && !isFirstHalf)) {
      status = this.isUnder(statValue) ?  STATUSES.WON : STATUSES.LOSE;
    }  else {
      status = this.isUnder(statValue) ? STATUSES.WINNING : STATUSES.LOSING;
    }
    return status;
  }


  /**
   * Get status for both teams both halves
   * @param scores
   * @param update
   * @param selection
   */
  protected bothTeamsBothHalves(scores: IScore, update: IScoreboardStatsUpdate, selection: IBybSelection): string {
    let status;
    const { statValue } = this.getExternalStatsLink(selection);
    const isYesOutcome = !this.isUnder(statValue);
    const scored = {
      [PERIODS['1ST_HALF']]: !!scores[PERIODS['1ST_HALF']].away && !!scores[PERIODS['1ST_HALF']].home,
      [PERIODS['2ND_HALF']]: scores[PERIODS['2ND_HALF']] && !!scores[PERIODS['2ND_HALF']].away && !!scores[PERIODS['2ND_HALF']].home
    };
    if (scored[PERIODS['1ST_HALF']] && scored[PERIODS['2ND_HALF']]) { // (1:1) and (1:1)
      status = isYesOutcome ? STATUSES.WON : STATUSES.LOSE;
      // IF  Selection = "No", period = "2h",  score: 1h: (0:1) AND score: 2h: (1:1), THEN Bet WON"
      // or score: 2h: (1:0)
      // IF  Selection = "YES", period = "2h",  score: 1h: (0:1) , THEN Bet LOSE"
    } else if (this.validateTeamsBothHalves(update, scored)) {
      status = isYesOutcome ? STATUSES.LOSE : STATUSES.WON;
    } else {
      status = isYesOutcome ? STATUSES.LOSING : STATUSES.WINNING;
    }
    return status;
  }

  /**
   * Get match status for TEAM TO GET 2nd GOAL market or TEAM TO GET 1ST GOAL market
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @param {Boolean} isFirstGoal
   * @returns {IBybSelectionStatus}
   */
  protected teamToGetFirstOrSecondGoalStatus(
    selection: IBybSelection,
    update: IScoreboardStatsUpdate,
    isFirstGoal?: boolean
  ): IBybSelectionStatus {
    const allGoals = this.statCategoryUtilityService.getAllGoals(update);
    const team = this.getTeamByExternalStatsLink(selection, update);
    const isNoGoalCase = selection.title === TEAMS.NO_GOAL;
    const conditions = {
      [TEAMS.HOME]: this.isGoal(allGoals, isFirstGoal ? 0 : 1, TEAMS.HOME),
      [TEAMS.AWAY]: this.isGoal(allGoals, isFirstGoal ? 0 : 1, TEAMS.AWAY),
    };
    let status: string;

    if (isNoGoalCase) {
      status = this.getNoStatsCategorySelectionStatus(!allGoals.length);
    } else
    if (conditions[team]) {
      status = STATUSES.WON;
    } else
    if (!allGoals.length || (allGoals.length === 1 && !isFirstGoal)) {
      status = STATUSES.LOSING;
    } else {
      status = STATUSES.LOSE;
    }

    return { status };
  }

  /**
   * Checks first or second goal for the team
   * @param {IGoalInfo[]} allGoals
   * @param {number} goal
   * @param {TEAMS} team
   * @returns {boolean}
   */
  protected isGoal(allGoals: IGoalInfo[], goal: number, team: TEAMS): boolean {
    return allGoals.length && allGoals[goal].team === team;
  }

  /**
   * get status for win both halves
   * @param team
   * @param currentPeriod
   * @param conditionsFirst
   * @param conditionsSecond
   */
  protected getWinBothHalvesStatus(team: string,
                                 currentPeriod: string,
                                 conditionsFirst: IConditions,
                                 conditionsSecond: IConditions): string {
    switch (true) {
    case (currentPeriod === PERIODS['2ND_HALF']):
      if (!conditionsFirst[team]) {
        return STATUSES.LOSE;
      } else {
        return conditionsSecond[team] ? STATUSES.WINNING : STATUSES.LOSING;
      }
    case (currentPeriod === PERIODS.total):
      return conditionsFirst[team] && conditionsSecond[team] ? STATUSES.WON : STATUSES.LOSE;
    default:
      // 1ND_HALF case
      return STATUSES.LOSING;
    }
  }

  /**
   * get status for win either half
   * @param team
   * @param currentPeriod
   * @param conditionsFirst
   * @param conditionsSecond
   */
  protected getWinEitherHalfStatus(team: string,
                                 currentPeriod: string,
                                 conditionsFirst: IConditions,
                                 conditionsSecond: IConditions): string {
    switch (true) {
    case (currentPeriod === PERIODS['2ND_HALF']):
      if (conditionsFirst[team]) {
        return STATUSES.WON;
      } else {
        return conditionsSecond[team] ? STATUSES.WINNING : STATUSES.LOSING;
      }
    case (currentPeriod === PERIODS.total):
      return conditionsFirst[team] || conditionsSecond[team] ? STATUSES.WON : STATUSES.LOSE;
    default:
      // 1ND_HALF case
      return conditionsFirst[team] ? STATUSES.WINNING : STATUSES.LOSING;
    }
  }

  /**
   * Checks first Booking for the team
   * @param {ICardsInfo[]} allCards
   * @param {TEAMS} team
   * @returns {boolean}
   */
  protected isFirstBooking(allCards: ICardsInfo[], team: TEAMS): boolean {
    return allCards.length && allCards[0].team === team;
  }

  /**
   * To validate teams halves
   * @param update
   * @param score
   */
  private validateTeamsBothHalves(update: IScoreboardStatsUpdate, scored: {[key: string]: boolean}) {
    return (update.period !== PERIODS['1ST_HALF'] && !scored[PERIODS['1ST_HALF']]) ;
  }

  /**
   * To get the stats category
   * @param isSettled
   * @param current
   * @param target
   * @returns { any }
   */
  private currentTargetValidate(isSettled: boolean, current: number, target: number): any {
    const currentCheck: boolean = current === BET_STATS_LIMIT.INITIAL_COUNTER;
    const targetCheck: boolean = target === BET_STATS_LIMIT.INITIAL_COUNTER;
    return isSettled && currentCheck || !isSettled && targetCheck ? STATS_CATEGORIES_SINGULAR : STATS_CATEGORIES;
  }

  /**
   * To calculate target for under booking market
   * @param target
   * @returns target
   */
  private underBookingCalculation(target: number): number {
    if (target === BET_STATS_LIMIT.FIRST_POSSIBLE_POINT || target === BET_STATS_LIMIT.SECOND_POSSIBLE_POINT) {
      return target - BET_STATS_LIMIT.FIRST_POSSIBLE_POINT;
    } else {
      return target - BET_STATS_LIMIT.COUNTER;
    }
  }

  /**
   * To calculate target for over booking market
   * @param target
   * @returns target
   */
  private overBookingCalculation(target: number): number {
    if (target === BET_STATS_LIMIT.FIRST_POSSIBLE_POINT) {
      return target + BET_STATS_LIMIT.FIRST_POSSIBLE_POINT;
    } else {
      return target + BET_STATS_LIMIT.COUNTER;
    }
  }
}
