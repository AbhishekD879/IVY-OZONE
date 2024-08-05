import { Injectable } from '@angular/core';
import {
  IBybSelection,
  IBybSelectionProgress,
  IBybSelectionStatus
} from '@lazy-modules/bybHistory/models/byb-selection.model';
import { IBetHistoryBet } from '@app/betHistory/models/bet-history.model';
import { IBetHistoryOutcome } from '@core/models/outcome.model';
import {
  ODD_EVEN,
  PERIODS,
  STATUSES,
  TEAMS,
  PLAYER_SHOTS,
  BET_STATUSES,
  HALF_LABELS,
  PRE_PLAY
} from '@lazy-modules/bybHistory/constants/byb-5aside-markets-config.constant';
import {
  PLAYER_STATS,
  StatCategoryUtilityService,
  TEAM_STATS
} from '@lazy-modules/bybHistory/services/betTrackingRules/stat-category-utility.service';
import { BindDecorator } from '@core/decorators/bind-decorator/bind-decorator.decorator';
import {
  IPlayer,
  IPlayerCards,
  IScoreboardStatsUpdate,
  IScoreByTeams,
  ITeams
} from '@lazy-modules/bybHistory/models/scoreboards-stats-update.model';
import environment from '@environment/oxygenEnvConfig';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { BetTrackingRulesHelperService } from '@bybHistoryModule/services/betTrackingRules/bet-tracking-rules-helper.service';

@Injectable({ providedIn: 'root' })
export class BetTrackingRulesService extends BetTrackingRulesHelperService {
  private readonly OPTA_ENV: string = environment.OPTA_SCOREBOARD.ENV;

  constructor(protected statCategoryUtilityService: StatCategoryUtilityService,
    private windowRefService: WindowRefService) {
    super(statCategoryUtilityService);
  }

  /**
   * Get Match Betting market actual status base on opta statistics
   * @param selection
   * @param update
   */
  @BindDecorator
  matchBettingStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    const goalsObj = this.getStatCategoryObj(selection, update);
    const team = this.statCategoryUtilityService.getHomeAwayTeamByContestantId(update, selection);

    if (this.secondHalfPrePlay(selection, update)) {
      return { status: PRE_PLAY.PRE_PLAY_2H };
    }

    if (!team || !Object.keys(goalsObj.score).length || !update.period) {
      // Team name is different in OB and OPTA, should not show any statuses if no team were found
      return { status: '' };
    }

    let status = '';

    switch (selection.config.period) {
      case PERIODS.total:
      case PERIODS['2ND_HALF']:
        status = this.getMatchBettingStatus(goalsObj, team, selection.config.period);
        break;
      case PERIODS['1ST_HALF']:
        status = this.getMatchBettingStatus(goalsObj, team, selection.config.period, update.period);
        break;
    }

    // NOTE: If selection.config.template === binary THEN only { status } should be returned,
    // NOTE IF selection.config.template === range THEN { status, progress } should be returned
    return { status };
  }

  /**
   * Get Handicap Betting market actual status base on opta statistics
   * @param selection
   * @param update
   */
  @BindDecorator
  handicapBettingStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {

    if (!update.period || !Object.keys(update.score).length) {
      return { status: '' };
    }

    const goalsObj = this.getStatCategoryObj(selection, update);
    const { statValue } = this.getExternalStatsLink(selection);
    const selectedHandicapValue = Math.abs(this.parseStatValue(statValue));
    if (selection.config.period === PERIODS['2ND_HALF'] && !goalsObj.score[PERIODS['2ND_HALF']]) {
      goalsObj.score[PERIODS['2ND_HALF']] = { home: 0, away: 0 };
    }
    const team = this.getTeamByExternalStatsLink(selection, update);
    const selectionName = selection.part.outcome[0].name;
    const handicap = selectionName.includes('(-') ? -1 * selectedHandicapValue : selectedHandicapValue; // Detect handicap sign
    const goalsWithHandicapObj = this.statCategoryUtilityService.applyHandicapValue(goalsObj, team, handicap, selection.config.period);
    let status;

    switch (selection.config.period) {
      case PERIODS.total:
      case PERIODS['2ND_HALF']:
        status = this.getMatchBettingStatus(goalsWithHandicapObj, team, selection.config.period);
        break;
      case PERIODS['1ST_HALF']:
        status = this.getMatchBettingStatus(goalsWithHandicapObj, team, selection.config.period, update.period);
        break;
    }

    return { status };
  }

  /**
   * Get ||PLAYER TO OUTSCORE THE OPPOSITION|| status based on opta statistics
   * @param selection
   * @param update
   */
  @BindDecorator
  playerToOutscoreStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    if (!update.players || !update.players.home || !update.players.away) {
      return { status: '' };
    }
    const teamScore = this.statCategoryUtilityService.getScoreByTeams(update);
    const { name } = (selection.part.outcome[0] as IBetHistoryOutcome);
    const player = this.statCategoryUtilityService.getPlayerByName(name, update.players);
    // player not found this market
    if (!player || !Object.keys(teamScore.score).length) {
      return { status: '' };
    }
    const oppositeTeam =
      player.homeAwaySide.toLowerCase() === TEAMS.HOME.toLowerCase() ? TEAMS.AWAY.toLowerCase() : TEAMS.HOME.toLowerCase();

    if (player.goals > teamScore.score.total[oppositeTeam]) {
      status = STATUSES.WINNING;
    } else {
      status = STATUSES.LOSING;
    }

    return { status };
  }

  /**
   * Get cleanSheet status based on opta statistics
   * @param selection
   * @param update
   */
  @BindDecorator
  cleanSheetStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    const goalsObj = this.getStatCategoryObj(selection, update);
    const team = this.getTeamByExternalStatsLink(selection, update);
    let status = '';
    const oppositeTeam = team.toLowerCase() === 'home' ? 'away' : 'home';

    if (goalsObj.score && goalsObj.score.total && goalsObj.score.total[oppositeTeam] === 0) {
      status = STATUSES.WINNING;
    } else if (goalsObj.score && goalsObj.score.total) {
      status = STATUSES.LOSE;
    }

    return { status };
  }

  /**
   * Get double chance market actual status base on opta statistics
   * @param selection
   * @param update
   * @param bet
   */
  @BindDecorator
  doubleChanceStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    let status = '';

    if (!Object.keys(update.score).length || (selection.config.period === PERIODS['1ST_HALF'] && !update.period)) {
      return { status };
    }
    const goalsObj = this.getStatCategoryObj(selection, update);
    const doubleTeam = this.statCategoryUtilityService.getDoubleHomeAwayTeamByContestantId(update, selection);

    if (!doubleTeam || !update.period || !Object.keys(goalsObj.score).length) {
      return { status };
    }

    switch (selection.config.period) {
      case PERIODS.total:
      case PERIODS['2ND_HALF']:
        status = this.getDoubleChanceStatus(goalsObj, doubleTeam, selection.config.period);
        break;
      case PERIODS['1ST_HALF']:
        status = this.getDoubleChanceStatus(goalsObj, doubleTeam, selection.config.period, update.period);
        break;
    }

    return { status };
  }

  /**
   * Get correct score market actual status base on opta statistics
   * @param selection
   * @param update
   */
  @BindDecorator
  correctScoreStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    let status = '';

    if (!Object.keys(update.score).length || (selection.config.period === PERIODS['1ST_HALF'] && !update.period)) {
      return { status };
    }
    const goalsObj = this.getStatCategoryObj(selection, update);
    const objTeams = this.getTeamCorrectScores(selection, update);

    if (selection.config.period === PERIODS['2ND_HALF'] && !goalsObj.score[PERIODS['2ND_HALF']]) {
      goalsObj.score[PERIODS['2ND_HALF']] = { home: 0, away: 0 };
    }
    if (!objTeams) {
      return { status };
    }

    switch (selection.config.period) {
      case PERIODS.total:
        status = this.getCorrectScoreStatus(goalsObj, objTeams, selection.config.period);
        break;
      case PERIODS['2ND_HALF']:
        status = this.getCorrectScoreStatus(goalsObj, objTeams, selection.config.period);
        break;
      case PERIODS['1ST_HALF']:
        status = this.getCorrectScoreStatus(goalsObj, objTeams, selection.config.period, update.period);
        break;
    }

    return { status };
  }

  /**
   * Get Red Cards by periods market actual status based on opta statistics
   * @param selection
   * @param update
   */
  @BindDecorator
  redCardsStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    const cardsObj = this.getStatCategoryObj(selection, update);

    if (!cardsObj.home.periods || !cardsObj.away.periods || !update.period) {
      return { status: '' };
    }

    const status = this.getFullRedsStatus(selection.part.outcome[0].name, cardsObj, selection.config.period, update.period);
    return { status };
  }

  /**
   * Get Red Cards status by player based on OPTA statistics
   * @param selection
   * @param update
   */
  @BindDecorator
  redCardsPlayerStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    const cardsObj = this.getStatCategoryObj(selection, update);
    const { playerId } = this.getExternalStatsLink(selection);
    const player = this.statCategoryUtilityService.getPlayerById(cardsObj, playerId);
    let status = '';
    const isNoRedCardSelection = this.isUnder(selection.part.outcome[0].externalStatsLink.statValue);
    // player not found
    if ((!player && !isNoRedCardSelection) || !update.cards.home || !update.cards.away) {
      return { status: '' };
      // NO RED CARD selection
    } else if (!player && isNoRedCardSelection) {
      status = this.getNoRedCardsSelectionStatus(update);
    } else if (player.cards.red > 0) {
      status = STATUSES.WON;
    } else {
      status = STATUSES.LOSING;
    }

    return { status };
  }

  /**
   * Get Shown Card status by player based on OPTA statistics
   * @param selection
   * @param update
   */
  @BindDecorator
  shownCardStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate,): IBybSelectionStatus {
    if (!update.players || !update.players.home || !update.players.away) {
      return { status: '' };
    }
    const players = this.statCategoryUtilityService.getPlayerStats(selection.config.generalInformationRequired, update, PLAYER_STATS.CARDS);
    const { playerId } = this.getExternalStatsLink(selection);
    const player = this.statCategoryUtilityService.getPlayerById(players, playerId);
    if (!player || !player.cards) {
      return { status: '' };
    }
    let status = '';
    if (player.cards.red > 0 || player.cards.yellow > 0) {
      status = STATUSES.WON;
    } else {
      status = STATUSES.LOSING;
    }

    return { status };
  }

  /**
   * Get Red Cards by teams market actual status based on opta statistics
   * @param selection
   * @param update
   */
  @BindDecorator
  redCardsParticipantStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    let status = '';

    if (!update.players || !update.players.home || !update.players.away) {
      return { status };
    }
    const cardsObj = this.getStatCategoryObj(selection, update),
      team = this.getTeamByExternalStatsLink(selection, update),
      isYesOutcome = selection.part.outcome[0].name === BET_STATUSES.OUTCOME_NAME_YES;

    status = this.getRedCardsParticipantStatus(cardsObj[team.toLowerCase()].periods.total.redCards, isYesOutcome);

    return { status };
  }

  /**
   * Get Total Goals market actual status based on opta statistics
   * @param selection
   * @param update
   * @param bet
   */
  @BindDecorator
  totalGoalsStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate, bet: IBetHistoryBet): IBybSelectionStatus {

    if (this.secondHalfPrePlay(selection, update)) {
      return { status: PRE_PLAY.PRE_PLAY_2H };
    }

    if (!update.period) {
      return { status: '' };
    }

    const goalsCategoryObj = this.getStatCategoryObj(selection, update) as IScoreByTeams;
    const team = this.getTeamByExternalStatsLink(selection, update);
    const { statValue } = this.getExternalStatsLink(selection);
    const { home, away } = goalsCategoryObj.score[selection.config.period] || { home: 0, away: 0 };
    const currentGoals = {
      [TEAMS.DRAW]: home + away,
      [TEAMS.HOME]: home,
      [TEAMS.AWAY]: away
    };
    const progress: IBybSelectionProgress = this.getSelectionProgress(selection, bet, currentGoals[team]);
    const { current, target } = progress;
    let status: string;

    switch (selection.config.period) {
      case PERIODS.total:
      case PERIODS['2ND_HALF']:
        status = this.isUnder(statValue)
          ? this.getUnderTotalMarketsStatus(current, target)
          : this.isEqual(statValue)
            ? this.getEqualTotalMarketsStatus(current, target)
            : this.getOverTotalMarketsStatus(current, target);
        break;
      case PERIODS['1ST_HALF']:
        status = this.isUnder(statValue)
          ? this.getUnderFirstHalfMarketsStatus(current, target, update.period)
          : this.isEqual(statValue)
            ? this.getEqualFirstHalfMarketsStatus(current, target, update.period)
            : this.getOverFirstHalfMarketsStatus(current, target, update.period);
        break;
    }

    return { status, progress };
  }

  /**
   * Get Total Cards markets actual status based on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @param {IBetHistoryBet} bet
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  totalCards(selection: IBybSelection, update: IScoreboardStatsUpdate, bet: IBetHistoryBet): IBybSelectionStatus {
    if (!this.isUpdatePlayersDataValid(update)) {
      return { status: '' };
    }

    const statsCategoryObj = this.statCategoryUtilityService.getCardIndex('player', update);
    const { statValue } = this.getExternalStatsLink(selection);

    // get all cards from all players from all teams
    const cards: IPlayerCards = this.statCategoryUtilityService.getCardsFromPlayers(statsCategoryObj, TEAMS.DRAW);
    const totalCards = cards.yellow + cards.red;

    const progress: IBybSelectionProgress = this.getSelectionProgress(selection, bet, totalCards);
    const { target, current } = progress;
    const status = this.isUnder(statValue)
      ? this.getUnderTotalMarketsStatus(current, target)
      : this.isEqual(statValue)
        ? this.getEqualTotalMarketsStatus(current, target)
        : this.getOverTotalMarketsStatus(current, target);

    return { status, progress };
  }

  /**
   * Get Total Goals by player markets actual status based on opta statistics
   * @param selection
   * @param update
   * @param bet
   */
  @BindDecorator
  totalGoalsByPlayerStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate, bet: IBetHistoryBet): IBybSelectionStatus {
    if (!this.isUpdatePlayersDataValid(update)) {
      return { status: '' };
    }
    const { playerId, statValue } = this.getExternalStatsLink(selection);
    const players = this.statCategoryUtilityService.getPlayerStats(selection.config.generalInformationRequired, update, PLAYER_STATS.GOALS);
    const player = this.statCategoryUtilityService.getPlayerById(players, playerId);

    if (!player) {
      // Don't show indicators and progress bar when no player were found
      return { status: '' };
    }

    const selectedValue = this.parseStatValue(statValue);
    const status = this.isOver(statValue)
      ? this.getOverTotalMarketsStatus(player.goals, selectedValue)
      : this.getEqualTotalMarketsStatus(player.goals, selectedValue);
    const progress = this.getSelectionProgress(selection, bet, +player.goals);

    return { status, progress };
  }

  /**
   * Get SCORE A GOAL IN BOTH HALVES by player markets actual status based on opta statistics
   * @param selection
   * @param update
   */
  @BindDecorator
  scoreAGoalInBothHalvesHandler(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {

    if (this.secondHalfPrePlay(selection, update)) {
      return { status: PRE_PLAY.PRE_PLAY_2H };
    }

    if (!Object.keys(update.score).length) {
      return { status: '' };
    }

    const { statValue } = this.getExternalStatsLink(selection);
    const goalsObj = this.getStatCategoryObj(selection, update) as IScoreByTeams;
    const currentPeriod = this.statCategoryUtilityService.getCurrentPeriod(update.period);
    const isFirstHalf = this.isFirstHalf(currentPeriod);
    const isSecondHalf = this.isSecondHalfOrTotal(currentPeriod);
    const conditions = {
      [PERIODS['1ST_HALF']]: (goalsObj.score[PERIODS['1ST_HALF']].home + goalsObj.score[PERIODS['1ST_HALF']].away) > 0,
      [PERIODS['2ND_HALF']]: goalsObj.score[PERIODS['2ND_HALF']]
        && ((goalsObj.score[PERIODS['2ND_HALF']].home + goalsObj.score[PERIODS['2ND_HALF']].away) > 0)
    };
    const isScoredInFirstHalf = conditions[PERIODS['1ST_HALF']];
    const isScoredInBothHalves = conditions[PERIODS['1ST_HALF']] && conditions[PERIODS['2ND_HALF']];
    let status;

    if (isScoredInBothHalves) {
      status = this.isUnder(statValue) ? STATUSES.LOSE : STATUSES.WON;
    } else if (!isScoredInBothHalves && (isFirstHalf || (isScoredInFirstHalf && isSecondHalf))) {
      status = this.isUnder(statValue) ? STATUSES.WINNING : STATUSES.LOSING;
    } else {
      status = this.isUnder(statValue) ? STATUSES.WON : STATUSES.LOSE;
    }

    return { status };
  }

  /**
   * Get Both Teams to score in 1st/2nd half status based on opta statistics
   * @param selection
   * @param update
   */
  @BindDecorator
  bothTeamsToScoreByHalvesStatusHandler(selection: IBybSelection,
    update: IScoreboardStatsUpdate): IBybSelectionStatus {
    const goalsObj = this.getStatCategoryObj(selection, update);

    if (this.secondHalfPrePlay(selection, update)) {
      return { status: PRE_PLAY.PRE_PLAY_2H };
    }

    let status = '';
    switch (selection.config.period) {
      case PERIODS.total: // both teams to score in 1st and 2nd half
        status = this.bothTeamsBothHalves(goalsObj.score, update, selection);
        break;
      case PERIODS['1ST_HALF']:
      case PERIODS['2ND_HALF']:
        status = this.bothTeamsHalfScoredStatus(goalsObj.score, update, selection);
        break;
    }
    return { status };
  }

  /**
   * Get both teams to score in match status based on opta statistics
   * @param selection
   * @param update
   */
  @BindDecorator
  bothTeamsToScoreStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    const goalsObj = this.getStatCategoryObj(selection, update);
    const { statValue } = this.getExternalStatsLink(selection);

    let status = '';

    if (!Object.keys(goalsObj.score).length) {
      return { status };
    }

    if (!!goalsObj.score.total.away && !!goalsObj.score.total.home) {
      status = this.isUnder(statValue) ? STATUSES.LOSE : STATUSES.WON;
    } else {
      status = this.isUnder(statValue) ? STATUSES.WINNING : STATUSES.LOSING;
    }
    return { status };
  }

  /**
   * Get Total Tackles market actual status base on opta statistics
   * @param selection
   * @param update
   * @param bet
   */
  @BindDecorator
  totalTacklesStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate, bet: IBetHistoryBet): IBybSelectionStatus {
    return this.isUpdatePlayersDataValid(update) ?
      this.getPlayerStatusAndProgress(selection, update, bet, PLAYER_STATS.TACKLES) : { status: '' };
  }

  /**
   * Get Total Shots market actual status base on opta statistics
   * @param selection
   * @param update
   * @param bet
   */
  @BindDecorator
  totalShotsStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate, bet: IBetHistoryBet): IBybSelectionStatus {
    return this.isUpdatePlayersDataValid(update) ?
      this.getPlayerStatusAndProgress(selection, update, bet, PLAYER_STATS.SHOTS, PLAYER_SHOTS.TOTAL) : { status: '' };
  }

  /**
   * Get Total Shots On Target market actual status base on opta statistics
   * @param selection
   * @param update
   * @param bet
   */
  @BindDecorator
  totalShotsOnTargetStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate, bet: IBetHistoryBet): IBybSelectionStatus {
    return this.isUpdatePlayersDataValid(update) ?
      this.getPlayerStatusAndProgress(selection, update, bet, PLAYER_STATS.SHOTS, PLAYER_SHOTS.ON_TARGET) : { status: '' };
  }

  /**
   * Get Total Assists market actual status base on opta statistics
   * @param selection
   * @param update
   * @param bet
   */
  @BindDecorator
  totalAssistsStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate, bet: IBetHistoryBet): IBybSelectionStatus {
    return this.getPlayerStatusAndProgress(selection, update, bet, PLAYER_STATS.ASSISTS);
  }

  /**
   * Get Total Passes market actual status base on opta statistics
   * @param selection
   * @param update
   * @param bet
   */
  @BindDecorator
  totalPassesStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate, bet: IBetHistoryBet): IBybSelectionStatus {
    return this.getPlayerStatusAndProgress(selection, update, bet, PLAYER_STATS.PASSES);
  }

  /**
   * Get Total Crosses market actual status base on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @param {IBetHistoryBet} bet
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  totalCrossesStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate, bet: IBetHistoryBet): IBybSelectionStatus {
    return this.getPlayerStatusAndProgress(selection, update, bet, PLAYER_STATS.CROSSES);
  }

  /**
   * Get Total Offsides market actual status base on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @param {IBetHistoryBet} bet
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  totalOffsidesStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate, bet: IBetHistoryBet): IBybSelectionStatus {
    return this.getPlayerStatusAndProgress(selection, update, bet, PLAYER_STATS.OFFSIDES);
  }

  /**
   * Get GOALS INSIDE BOX market actual status base on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @param {IBetHistoryBet} bet
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  goalsInsideBoxStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate, bet: IBetHistoryBet): IBybSelectionStatus {
    return this.getPlayerStatusAndProgress(selection, update, bet, PLAYER_STATS.GOALS_INSIDE_BOX);
  }

  /**
   * Get GOALS OUTSIDE BOX market actual status base on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @param {IBetHistoryBet} bet
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  goalsOutsideBoxStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate, bet: IBetHistoryBet): IBybSelectionStatus {
    return this.getPlayerStatusAndProgress(selection, update, bet, PLAYER_STATS.GOALS_OUTSIDE_BOX);
  }

  /**
   * Get shotsWoodwork market actual status base on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @param {IBetHistoryBet} bet
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  shotsWoodworkStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate, bet: IBetHistoryBet): IBybSelectionStatus {
    return this.getPlayerStatusAndProgress(selection, update, bet, PLAYER_STATS.SHOTS_WOODWORK);
  }

  /****************** CORNERS BLOCK LOGIC ******************/
  /**
   * Get CORNERS MATCH BET market actual status base on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  cornersMatchBetStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    const statsCategoryObj = this.getStatCategoryObj(selection, update) as ITeams;

    let status: string;

    if (statsCategoryObj.home && statsCategoryObj.away) {
      const team = this.statCategoryUtilityService.getHomeAwayTeamByContestantId(update, selection);

      if (!team || !update.period || !(statsCategoryObj.home[selection.config.period] && statsCategoryObj.away[selection.config.period])) {
        // Team name is different in OB and OPTA, should not show any statuses if no team were found
        return { status: '' };
      }

      const { home, away } = this.getTeamStatsByPeriod(selection.config.period, statsCategoryObj, TEAM_STATS.CORNERS);
      const conditions = {
        [TEAMS.DRAW]: home === away,
        [TEAMS.AWAY]: home < away,
        [TEAMS.HOME]: home > away
      };

      if (this.isFirstHalf(selection.config.period)) { // 1ST HALF
        status = this.getFirstHalfBettingStatus(conditions, team, update.period);
      } else {  // TOTAL | 2ND HALF
        status = this.getFullMatchStatus(conditions, team);
      }
    } else {
      status = STATUSES.LOSING;
    }

    // NOTE: If selection.config.template === binary THEN only { status } should be returned,
    // NOTE IF selection.config.template === range THEN { status, progress } should be returned
    return { status };
  }

  /**
   * Get {PARTICIPANT_{N}} {{N} HALF}} TOTAL CORNERS market actual status base on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @param {IBetHistoryBet} bet
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  totalCornersStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate, bet: IBetHistoryBet): IBybSelectionStatus {
    const statsCategoryObj = this.getStatCategoryObj(selection, update) as ITeams;

    if (this.secondHalfPrePlay(selection, update)) {
      return { status: PRE_PLAY.PRE_PLAY_2H };
    }
    if (!update.period) {
      return { status: '' };
    }

    let status: string;

    const team = this.getTeamByExternalStatsLink(selection, update);
    const { statValue } = this.getExternalStatsLink(selection);
    const { home, away } = this.getTeamStatsByPeriod(selection.config.period, statsCategoryObj, TEAM_STATS.CORNERS);

    const progress: IBybSelectionProgress = this.getSelectionProgress(
      selection,
      bet,
      team.includes(TEAMS.HOME) ? home :  // PARTICIPANT_1 TOTAL CORNERS IN TOTAL | 1ST HALF | 2ND HALF
        team.includes(TEAMS.AWAY) ? away :  // PARTICIPANT_2 TOTAL CORNERS IN TOTAL | 1ST HALF | 2ND HALF
          home + away  // TOTAL CORNERS IN TOTAL
    );

    const { current, target } = progress;

    if (this.isFirstHalf(selection.config.period)) { // 1ST HALF  for TOTAL | [PARTICIPANT_1 | PARTICIPANT_2] TOTAL
      status = this.isUnder(statValue)
        ? this.getUnderFirstHalfMarketsStatus(current, target, update.period)
        : this.getOverFirstHalfMarketsStatus(current, target, update.period);
    } else {  // TOTAL | 2ND HALF for TOTAL | [PARTICIPANT_1 | PARTICIPANT_2] TOTAL
      status = this.isUnder(statValue)
        ? this.getUnderTotalMarketsStatus(current, target)
        : this.getOverTotalMarketsStatus(current, target);
    }

    // NOTE: If selection.config.template === binary THEN only { status } should be returned,
    // NOTE IF selection.config.template === range THEN { status, progress } should be returned
    return { status, progress };
  }
  /****************** END of CORNERS BLOCK LOGIC ******************/

  /**
   * Get TOTAL GOALS ODD/EVEN market actual status base on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  totalGoalsOddsEvenStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    const statsCategoryObj = this.getStatCategoryObj(selection, update);
    let status: string;

    if (!update.period) {
      return { status: '' };
    }

    if (statsCategoryObj.score[selection.config.period]) {
      const { home, away } = statsCategoryObj.score[selection.config.period],
        goalsCount = home + away,
        isEvenGoalsCount = goalsCount % 2 === 0;

      const conditions = {
        [ODD_EVEN.ODD]: !isEvenGoalsCount,
        [ODD_EVEN.EVEN]: isEvenGoalsCount,
      };

      if (this.isFirstHalf(selection.config.period)) {
        status = this.getFirstHalfBettingStatus(conditions, selection.title, update.period);
      } else {  // TOTAL | 2ND HALF
        status = this.getFullMatchStatus(conditions, selection.title);
      }
    } else {
      status = STATUSES.LOSING;
    }

    return { status };
  }

  /**
   * Get Build Your Bet market actual status after '15:00' | '30:00' | '60:00' | '75:00' minutes base on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  getResultAfterNMinutes(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    if (!update.time) {
      return { status: '' };
    }
    const team = this.getTeamByExternalStatsLink(selection, update);

    // should be removed after resolving BMA-58840
    if (!team) {
      return { status: '' };
    }
    const period = PERIODS[selection.config.period];
    const periodReached = this.isPeriodReached(update.time, period);
    const goalsStat = this.getGoalsByTeamAndPeriod(this.statCategoryUtilityService.getAllGoals(update), period);

    return { status: this.getRangeMarketStatus(goalsStat, periodReached, team) };
  }

  /**
   * Get Build Your Bet MOST GOALS [0 - 30 | 30 - 60] MINUTES market actual status base on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  mostGoalsInRange(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    if (!update.time) {
      return { status: '' };
    }
    const team = this.getTeamByExternalStatsLink(selection, update);

    // should be removed after resolving BMA-58840
    if (!team) {
      return { status: '' };
    }

    let period: string;
    let periodStart: string;

    if (this.isFirstHalf(selection.config.period)) {
      period = PERIODS['30 mins'];
    } else {
      periodStart = PERIODS['30 mins'];
      period = PERIODS['60 mins'];
    }

    const periodReached = this.isPeriodReached(update.time, period);
    const goalsStat = this.getGoalsByTeamAndPeriod(this.statCategoryUtilityService.getAllGoals(update), period, periodStart);

    return { status: this.getRangeMarketStatus(goalsStat, periodReached, team) };
  }

  /**
   * Get Build Your Bet TO WIN TO NIL market actual status base on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  toWinToNil(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    const statsCategoryObj = this.getStatCategoryObj(selection, update) as IScoreByTeams;
    const team = this.statCategoryUtilityService.getHomeAwayTeamByContestantId(update, selection);

    if (!team || !(Object.keys(statsCategoryObj.score).length && statsCategoryObj.score[selection.config.period])) {
      // Team name is different in OB and OPTA, should not show any statuses if no team were found
      return { status: '' };
    }

    const { home, away } = statsCategoryObj.score[selection.config.period];
    const conditions = {
      [TEAMS.HOME]: away === 0,
      [TEAMS.AWAY]: home === 0
    };
    const teamScoreIsZero = (): boolean => team.includes(TEAMS.HOME) ? home === 0 : away === 0;

    let status: string;

    if (conditions[team] && !teamScoreIsZero()) {
      status = STATUSES.WINNING;  // the selected team scores at least 1 goal and match is going
    } else if (conditions[team] && teamScoreIsZero()) {
      status = STATUSES.LOSING; // no team scores and the match is going
    } else {
      status = STATUSES.LOSE; // no team scores and the match is over OR the opposite team scores
    }

    return { status };
  }

  /**
   * Get Build Your Bet TEAM TO GET 1ST GOAL market actual status base on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  teamToGetFirstGoal(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    if (!this.isUpdateGoalsDataValid(update)) {
      return { status: '' };
    }
    return this.teamToGetFirstOrSecondGoalStatus(selection, update, true);
  }

  /**
   * Get Build Your Bet TEAM TO GET 2nd GOAL market actual status base on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  teamToGetSecondGoal(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    if (!this.isUpdateGoalsDataValid(update)) {
      return { status: '' };
    }
    return this.teamToGetFirstOrSecondGoalStatus(selection, update);
  }

  /**
   * Get Build Your Bet PLAYER TO GET FIRST BOOKING market actual status base on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  playerToGetFirstBooking(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    if (!update.players || !update.players.home || !update.players.away || !update.teams || !update.teams.home || !update.teams.away) {
      return { status: '' };
    }
    const playerName = selection.part.outcome[0].name;
    const player = this.statCategoryUtilityService.getPlayerByName(playerName, update.players);

    if (!player) {
      return { status: '' };
    }

    const allCards = this.statCategoryUtilityService.getAllCards(update);
    let status: string;

    if (allCards.length && allCards[0].player === player.id) {
      status = STATUSES.WON;
    } else
      if (!allCards.length) {
        status = STATUSES.LOSING;
      } else {
        status = STATUSES.LOSE;
      }

    return { status };
  }

  /**
   * Get Build Your Bet TEAM TO GET 1ST BOOKING market actual status base on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  teamToGetFirstBooking(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    if (!update.teams || !update.teams.home || !update.teams.away) {
      return { status: '' };
    }
    const allCards = this.statCategoryUtilityService.getAllCards(update);
    const team = this.getTeamByExternalStatsLink(selection, update);
    const isNoCardsCase = selection.title.toLocaleLowerCase() === TEAMS.NO_CARDS;
    const conditions = {
      [TEAMS.HOME]: this.isFirstBooking(allCards, TEAMS.HOME),
      [TEAMS.AWAY]: this.isFirstBooking(allCards, TEAMS.AWAY),
    };
    let status: string;

    if (isNoCardsCase) {
      status = this.getNoStatsCategorySelectionStatus(!allCards.length);
    } else
      if (conditions[team]) {
        status = STATUSES.WON;
      } else
        if (!allCards.length) {
          status = STATUSES.LOSING;
        } else {
          status = STATUSES.LOSE;
        }

    return { status };
  }

  /**
   * Get Shots Outside Box market actual status based on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @param {IBetHistoryBet} bet
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  shotsOutsideBoxStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate,
    bet: IBetHistoryBet): IBybSelectionStatus {
    return this.getPlayerStatusAndProgress(selection, update, bet, PLAYER_STATS.SHOTS_OUTSIDE_BOX);
  }

  /**
   * Get First Teams To Score market actual status based on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @param {IBetHistoryBet} bet
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  firstTeamToScore(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    let status: string = '';

    if (this.secondHalfPrePlay(selection, update)) {
      return { status: PRE_PLAY.PRE_PLAY_2H };
    }

    if (!Object.keys(update.score).length) {
      return { status };
    }
    const statsCategoryObj = this.getStatCategoryObj(selection, update);
    const team = this.getTeamByExternalStatsLink(selection, update);
    const isNoGoalCase = selection.title === TEAMS.NO_GOAL;

    if (statsCategoryObj.score[selection.config.period]) {
      const { home, away } = statsCategoryObj.score[selection.config.period];
      const noGoalsScored = !home && !away,
        teamScoredFirst = this.getTeamScoredFirst(update, selection.config.period);

      const conditions = {
        [TEAMS.AWAY]: teamScoredFirst === TEAMS.AWAY,
        [TEAMS.HOME]: teamScoredFirst === TEAMS.HOME,
        [TEAMS.NO_GOAL]: noGoalsScored
      };

      if (teamScoredFirst && !isNoGoalCase) {
        status = conditions[team] ? STATUSES.WON : STATUSES.LOSE;
      } else if (isNoGoalCase && !noGoalsScored) {
        status = STATUSES.LOSE;
      } else if (this.isFirstHalf(selection.config.period)) {
        status = this.getFirstHalfBettingStatus(conditions, isNoGoalCase ? TEAMS.NO_GOAL : team, update.period);
      } else {  // TOTAL | 2ND HALF
        status = this.getFullMatchStatus(conditions, this.validateGoalCase(isNoGoalCase, team));
      }
    } else if (isNoGoalCase) {
      status = STATUSES.WINNING;
    } else {
      status = STATUSES.LOSING;
    }

    return { status };
  }

  /**
   * Get First Teams To Score market actual status based on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  teamToScoreInBothHalves(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    if (!Object.keys(update.score).length) {
      return { status: '' };
    }
    const statsCategoryObj = this.getStatCategoryObj(selection, update);
    const team = this.getTeamByExternalStatsLink(selection, update);
    const getScoreInPeriod = (score, teamName: string) => score ? score[teamName.toLowerCase()] : 0;
    const getScoredInBothHalves = (teamName: string) => !!getScoreInPeriod(statsCategoryObj.score[PERIODS['1ST_HALF']], teamName)
      && !!getScoreInPeriod(statsCategoryObj.score[PERIODS['2ND_HALF']], teamName);
    const conditions = {
      [TEAMS.AWAY]: getScoredInBothHalves(TEAMS.AWAY),
      [TEAMS.HOME]: getScoredInBothHalves(TEAMS.HOME),
    };
    const status = conditions[team] ? STATUSES.WON : this.getFullMatchStatus(conditions, team);

    return { status };
  }

  /**
   * Get First Teams To Score market actual status based on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  halfToProduceFirstGoal(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    if (!Object.keys(update.score).length) {
      return { status: '' };
    }
    const getGoalsCount: Function = (score) => score ? score.home + score.away : 0,
      goalsInPeriodMap = {};

    [PERIODS['1ST_HALF'], PERIODS['2ND_HALF'], PERIODS.total].forEach((period: string) => {
      goalsInPeriodMap[period] = getGoalsCount(update.score[period]);
    });

    let status: string;

    const isFirstHalf = selection.title === HALF_LABELS['1ST_HALF'],
      isGoalScoredInFirstHalf = !!goalsInPeriodMap[PERIODS['1ST_HALF']];

    const conditions = {
      [HALF_LABELS['1ST_HALF']]: isGoalScoredInFirstHalf,
      [HALF_LABELS['2ND_HALF']]: !isGoalScoredInFirstHalf && !!goalsInPeriodMap[PERIODS['2ND_HALF']],
      [HALF_LABELS.NO_GOALS]: !goalsInPeriodMap[PERIODS.total]
    };

    if (selection.title === HALF_LABELS.NO_GOALS) {
      status = !conditions[HALF_LABELS.NO_GOALS] ? STATUSES.LOSE
        : this.getFullMatchStatus(conditions, selection.title);
    } else if (isFirstHalf) {
      status = conditions[HALF_LABELS['1ST_HALF']] ? STATUSES.WON :
        this.getFirstHalfBettingStatus(conditions, selection.title, update.period);
    } else if (conditions[HALF_LABELS['1ST_HALF']]) {
      status = STATUSES.LOSE;
    } else {  // TOTAL | 2ND HALF
      status = conditions[HALF_LABELS['2ND_HALF']] ? STATUSES.WON
        : this.getFullMatchStatus(conditions, selection.title);
    }

    return { status };
  }

  /**
   * Get Player To Score In Both Halves market actual status based on opta statistics
   * @param selection
   * @param update
   */
  @BindDecorator
  playerToScoreInBothHalves(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    if (!this.isUpdateGoalsDataValid(update)) {
      return { status: '' };
    }
    const { playerId } = this.getExternalStatsLink(selection);
    let status = '';
    const playerScoredInPeriodInfo = this.getPlayerScoredInPeriodInfo(update, playerId);

    if (update.period === PERIODS['1ST_HALF']) {
      status = STATUSES.LOSING;
    } else {
      if (playerScoredInPeriodInfo[PERIODS['1ST_HALF']] && playerScoredInPeriodInfo[PERIODS['2ND_HALF']]) {
        status = STATUSES.WON;
      } else if (playerScoredInPeriodInfo[PERIODS['1ST_HALF']]) {
        status = STATUSES.LOSING;
      } else {
        status = STATUSES.LOSE;
      }
    }

    return { status };
  }

  /**
   * Get Player To Score In 1st/2nd half market actual status based on opta statistics
   * @param selection
   * @param update
   * @param bet
   */
  @BindDecorator
  playerToScoreInPeriod(selection: IBybSelection, update: IScoreboardStatsUpdate, bet: IBetHistoryBet): IBybSelectionStatus {
    if (!this.isUpdateGoalsDataValid(update)) {
      return { status: '' };
    }
    const { playerId } = this.getExternalStatsLink(selection);
    let status = '';
    const conditions = this.getPlayerScoredInPeriodInfo(update, playerId);
    if (this.isFirstHalf(selection.config.period)) {
      status = conditions[selection.config.period] ? STATUSES.WON :
        this.getFirstHalfBettingStatus(conditions, selection.config.period, update.period);
    } else {  // TOTAL | 2ND HALF
      status = conditions[selection.config.period] ? STATUSES.WON :
        this.getFullMatchStatus(conditions, selection.config.period);
    }

    const progress: IBybSelectionProgress = this.getSelectionProgress(selection, bet, conditions[selection.config.period]);

    return { status, progress };
  }


  /**
   * Get Participant [1 | 2] to Score N+ Goals market actual status based on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @param {IBetHistoryBet} bet
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  participantToScoreNGoals(selection: IBybSelection, update: IScoreboardStatsUpdate, bet: IBetHistoryBet): IBybSelectionStatus {
    if (!Object.keys(update.score).length) {
      return { status: '' };
    }

    const statsCategoryObj = this.getStatCategoryObj(selection, update);
    const statsPeriod = statsCategoryObj.score[selection.config.period];
    if (!statsPeriod) {
      return { status: '' };
    }

    const team = this.getTeamByExternalStatsLink(selection, update);
    const { statValue } = this.getExternalStatsLink(selection);
    const { home, away } = statsPeriod;

    const progress: IBybSelectionProgress = this.getSelectionProgress(
      selection,
      bet,
      team.includes(TEAMS.HOME)
        ? home // PARTICIPANT_1 TOTAL SCORE
        : away  // PARTICIPANT_2 TOTAL SCORE
    );

    const { current, target } = progress;

    const status: string = this.isUnder(statValue)
      ? this.getUnderTotalMarketsStatus(current, target)
      : this.getOverTotalMarketsStatus(current, target);

    return { status, progress };
  }

  /**
   * get WIN N HALVES markets actual status based on opta statistics
   * @param selection
   * @param update
   */
  @BindDecorator
  winHalvesStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    const statsCategoryObj = this.getStatCategoryObj(selection, update);
    const team: string = this.statCategoryUtilityService.getHomeAwayTeamByContestantId(update, selection);

    if (!team || !(Object.keys(statsCategoryObj.score).length && statsCategoryObj.score[PERIODS['1ST_HALF']]) || !update.period) {
      // Team name is different in OB and OPTA, should not show any statuses if no team were found
      return { status: '' };
    }

    const currentPeriod: string = this.statCategoryUtilityService.getCurrentPeriod(update.period);

    const { home, away } = statsCategoryObj.score[PERIODS['1ST_HALF']];
    const { home: homeSecond, away: awaySecond } = statsCategoryObj.score[PERIODS['2ND_HALF']] || { home: 0, away: 0 };

    const conditionsFirst = {
      [TEAMS.AWAY]: home < away,
      [TEAMS.HOME]: home > away
    };
    const conditionsSecond = {
      [TEAMS.HOME]: homeSecond > awaySecond,
      [TEAMS.AWAY]: homeSecond < awaySecond
    };

    const status: string = selection.config.isBoth
      ? this.getWinBothHalvesStatus(team, currentPeriod, conditionsFirst, conditionsSecond)
      : this.getWinEitherHalfStatus(team, currentPeriod, conditionsFirst, conditionsSecond);

    return { status };
  }

  /**
   * Get MATCH|PARTICIPANT_1|PARTICIPANT_2 Booking Points markets actual status based on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @param {IBetHistoryBet} bet
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  matchBookingPointsStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate, bet: IBetHistoryBet): IBybSelectionStatus {
    const statsCategoryObj = this.getStatCategoryObj(selection, update);
    const team = this.getTeamByExternalStatsLink(selection, update);
    const cards: IPlayerCards = this.statCategoryUtilityService.getCardsFromPlayers(statsCategoryObj, team);
    const bookingPoints = this.statCategoryUtilityService.getBookingPoints(cards);
    const { statValue } = this.getExternalStatsLink(selection);
    
    const actualTarget: number = this.parseStatValue(statValue);

    const progress: IBybSelectionProgress = this.getBookingSelectionProgress(selection, bet, bookingPoints);

    const { current } = progress;

    const status: string = this.isUnder(statValue)
      ? this.getUnderBookingStatus(current, actualTarget)
      : this.isEqual(statValue)
        ? this.getEqualTotalMarketsStatus(current, actualTarget)
        : this.getOverTotalMarketsStatus(current, actualTarget, true);

    return { status, progress };
  }

  /**
   * Get FIRST|LAST|ANYTIME GOALSCORER markets actual status based on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  goalscorersStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate): IBybSelectionStatus {
    const playerName = selection.part.outcome[0].name;
    let player: IPlayer;
    if (selection.part.outcome[0].externalStatsLink) {
      const playerId = selection.part.outcome[0].externalStatsLink.playerId;
      player = this.statCategoryUtilityService.getPlayerFromNameId(playerName, playerId, update.players);
    } else {
      player = this.statCategoryUtilityService.getPlayerByName(playerName, update.players);
    }
    const isNoGoalscorer = playerName.toLowerCase() === 'no goalscorer'; // Special case for LAST GOALSCORER market

    if (!player && !isNoGoalscorer) {
      // Don't show indicators when no player were found
      return { status: '' };
    }

    const allGoals = this.statCategoryUtilityService.getAllGoals(update);
    const conditions = {
      [PERIODS.first]: allGoals.length && player && allGoals[0].scorer === player.id,
      [PERIODS.last]: allGoals.length && player && allGoals[allGoals.length - 1].scorer === player.id,
      [PERIODS.total]: player && allGoals.find(goal => goal.scorer === player.id)
    };
    let status: string;

    if (isNoGoalscorer) {
      status = this.getNoStatsCategorySelectionStatus(!allGoals.length);
    } else if (!allGoals.length) {
      status = STATUSES.LOSING;
    } else if (selection.config.period === PERIODS.first) {
      status = conditions[selection.config.period] ? STATUSES.WON : STATUSES.LOSE;
    } else if (selection.config.period === PERIODS.last) { // Last goalscorer && match is in progress
      status = conditions[PERIODS.last] ? STATUSES.WINNING : STATUSES.LOSING;
    } else {  // Anytime goalscorer && match is in progress
      status = conditions[selection.config.period] ? STATUSES.WON : STATUSES.LOSING;
    }

    return { status };
  }

  /**
   * Get PLAYER TOTAL GOALS CONCEDED|PLAYER TO KEEP A CLEAN SHEET markets actual status based on opta statistics
   * @param {IBybSelection} selection
   * @param {IScoreboardStatsUpdate} update
   * @param {IBetHistoryBet} bet
   * @returns {IBybSelectionStatus}
   */
  @BindDecorator
  goalsConcededStatusHandler(selection: IBybSelection, update: IScoreboardStatsUpdate, bet: IBetHistoryBet): IBybSelectionStatus {
    const preMatchOptaStats =
      JSON.parse(this.windowRefService.nativeWindow.localStorage.getItem(`scoreBoards_${this.OPTA_ENV}_prematch_${update.obEventId}`));
    const { playerId, statValue } = this.getExternalStatsLink(selection);
    const playersStats =
      this.statCategoryUtilityService.getPlayerStats(selection.config.generalInformationRequired, update, PLAYER_STATS.GOALS_CONCEDED);
    const player = this.statCategoryUtilityService.getPlayerById(playersStats, playerId);

    // NOTE: preMatchOptaStats will be available in localStorage only 3h from the start of the match
    if (preMatchOptaStats && player) {
      const isPlayerPlaying = !!preMatchOptaStats.data.participants[player.team].lineup
        .find(playerPlaying => playerPlaying.id === player.id && !playerPlaying.substitute);
      if (!isPlayerPlaying) {
        // Don't show indicators when no player is not playing in the match
        return { status: '' };
      }
    }
    if (!preMatchOptaStats && !player) {
      // Don't show indicators when no player and no preMatchOptaStats were found
      return { status: '' };
    }
    const goalConceded = player ? player.goalConceded : 0;
    const progress = this.getSelectionProgress(selection, bet, goalConceded);
    const { current, target } = progress;

    const status: string = this.isOver(statValue)
      ? this.getOverTotalMarketsStatus(current, target)
      : this.getEqualTotalMarketsStatus(current, target);

    return { status, progress };
  }

  private isUpdateGoalsDataValid(update: IScoreboardStatsUpdate): boolean {
    return !!(update.goals && Object.keys(update.goals).length);
  }

  private isUpdatePlayersDataValid(update: IScoreboardStatsUpdate): boolean {
    return !!(update.players && update.players.home && update.players.away);
  }

  /**
   * Validate goal
   * @param isNoGoalCase
   * @param team
   */
  private validateGoalCase(isNoGoalCase: boolean, team: string): string {
    return isNoGoalCase ? TEAMS.NO_GOAL : team;
  }

  /**
   * Filter 2h selection during 1h and ht
   * @param selection
   * @param update
   * @returns status
   */
  private secondHalfPrePlay(selection: IBybSelection, update: IScoreboardStatsUpdate): boolean {
    const periodValidate: boolean = selection.config.period !== update.period;
    const secondHalfCheck: boolean = selection.config.period === PERIODS['2ND_HALF'];
    const filter1hAndHt: boolean = (update.period === PERIODS.halftime || update.period === PERIODS['1ST_HALF']);
    return secondHalfCheck && periodValidate && filter1hAndHt && update.period !== PERIODS['2ND_HALF'];
  }
}
