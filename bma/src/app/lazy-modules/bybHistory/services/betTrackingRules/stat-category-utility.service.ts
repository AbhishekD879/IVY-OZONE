import { Injectable } from '@angular/core';
import { BindDecorator } from '@core/decorators/bind-decorator/bind-decorator.decorator';
import {
  IGoalInfo, IGoals,
  IPlayer, IPlayersSimple,
  IScoreboardStatsUpdate,
  IScoreByPlayer, IScoreByTeams,
  ITeam, ITeams,
  ICardsByPlayer,
  IRedCardsByTeams,
  IPlayerCards,
  IPlayers, ICardsInfo
} from '@lazy-modules/bybHistory/models/scoreboards-stats-update.model';
import { IBybSelection } from '@lazy-modules/bybHistory/models/byb-selection.model';
import {
  CARDS_INDEX,
  DOUBLE_TEAMS,
  PERIODS,
  TEAMS
} from '@lazy-modules/bybHistory/constants/byb-5aside-markets-config.constant';

/**
 * This utility service will be using to get statistic from DATA HUB JSON base on StatCategory from Banach
 *
 * DATA HUB JSON structure for Football(OPTA provider)
 * - https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SDM&title=Football+Scoreboard
 *
 * Available StatCategory values
 *
 * Score
 * Corners
 * RedCards
 * CardIndex
 * Booking
 * Shots
 * ShotsOnTarget
 * Assists
 * Passes
 * Tackles
 * Offsides
 * Crosses
 * goalConceded
 */

export enum PLAYER_STATS {
  ASSISTS = 'assists',
  PASSES = 'passes',
  SHOTS = 'shots',
  TACKLES = 'tackles',
  CARDS = 'cards',
  GOALS = 'goals',
  OFFSIDES = 'offsides',
  GOALS_CONCEDED = 'goalConceded',
  CROSSES = 'crosses',
  SECOND_YELLOW = 'secondYellow',
  SHOTS_WOODWORK = 'shotsWoodwork',
  SHOTS_OUTSIDE_BOX = 'shotsOutsideBox',
  GOALS_OUTSIDE_BOX = 'goalsOutsideBox',
  GOALS_INSIDE_BOX = 'goalsInsideBox',
}

export enum TEAM_STATS {
  CARDS = 'cards',
  CORNERS = 'corners'
}

@Injectable({ providedIn: 'root' })
export class StatCategoryUtilityService {

  /**
   * Get object with goals stats
   * @param generalInformationRequired
   * @param update
   */
  @BindDecorator
  getScore(generalInformationRequired: string, update: IScoreboardStatsUpdate): IScoreByTeams | IScoreByPlayer {
    switch (generalInformationRequired) {
      case 'team':
      case 'teams':
        return this.getScoreByTeams(update);
      case 'player':
        return this.getScoreByPlayer(update);
    }
  }

  /**
   * Get goals by teams, extend object with teams info(providerId, name)
   */
  getScoreByTeams(update: IScoreboardStatsUpdate): IScoreByTeams {
    const score = JSON.parse(JSON.stringify(update.score));

    return {
      score,
      away: update.away,
      home: update.home
    };
  }

  /**
   * Get all cards in match sorted by timestamp and extended with team property
   * @param update
   */
  getAllCards(update: IScoreboardStatsUpdate): ICardsInfo[] {
    const cards = (this.getBooking('player', update) as ICardsByPlayer).cards;

    [TEAMS.HOME, TEAMS.AWAY].forEach((team: string) => {
      cards[team.toLowerCase()].forEach((goalInfo: IGoalInfo) => {
        goalInfo.team = team;
      });
    });

    return cards[TEAMS.HOME.toLowerCase()]
      .concat(cards[TEAMS.AWAY.toLowerCase()])
      .sort((firstCard: IGoalInfo, secondCard: IGoalInfo) => new Date(firstCard.timestamp) > new Date(secondCard.timestamp) ? 1 : -1);
  }

  /**
   * Get all goals in match sorted by order of scoring and extended with period and team properties
   * @param update
   */
  getAllGoals(update: IScoreboardStatsUpdate): IGoalInfo[] {
    const getGoalsCount: Function = (score) => score ? score.home + score.away : 0,
      goalsInPeriodMap = {},
      scoreInfo = this.getScoreByPlayer(update);

    [PERIODS['1ST_HALF'], PERIODS['2ND_HALF']].forEach((period: string) => {
      goalsInPeriodMap[period] = getGoalsCount(update.score[period]);
    });

    [TEAMS.HOME, TEAMS.AWAY].forEach((team: string) => {
      scoreInfo[team.toLowerCase()].forEach((goalInfo: IGoalInfo) => {
        goalInfo.team = team;
      });
    });

    const goalsCountInMainTime = goalsInPeriodMap[PERIODS['1ST_HALF']] + goalsInPeriodMap[PERIODS['2ND_HALF']],
      allGoals: IGoalInfo[] = scoreInfo[TEAMS.HOME.toLowerCase()]
        .concat(scoreInfo[TEAMS.AWAY.toLowerCase()])
        .sort((firstGoal: IGoalInfo, secondGoal: IGoalInfo) => new Date(firstGoal.timestamp) > new Date(secondGoal.timestamp)  ? 1 : -1);

    allGoals.forEach((goal: IGoalInfo, index: number) => {
      const goalNumber = index + 1;
      if (goalNumber <= goalsInPeriodMap[PERIODS['1ST_HALF']]) {
        goal.period = PERIODS['1ST_HALF'];
      } else if (goalNumber <= goalsCountInMainTime) {
        goal.period = PERIODS['2ND_HALF'];
      }
    });

    return allGoals;
  }

  /**
   * Get goals by player
   */
  getScoreByPlayer(update: IScoreboardStatsUpdate): IScoreByPlayer  {
    const goalsObj = update.goals;
    update.goals.away.forEach((goal: IGoalInfo) => {
      this.extendGoalWihPlayerInfo(goal, update, goalsObj);
    });
    update.goals.home.forEach((goal: IGoalInfo) => {
      this.extendGoalWihPlayerInfo(goal, update, goalsObj);
    });

    return goalsObj as IScoreByPlayer;
  }

  /**
   * Extend Goal object wih player info, combine IGoals and IPlayer model to have all needed stats and info
   * @param goal
   * @param update
   * @param goalsObj
   */
  extendGoalWihPlayerInfo(goal: IGoalInfo, update: IScoreboardStatsUpdate, goalsObj: IGoals): void {
    let player = update.players.home[goal.scorer];

    if(!player) {
      // Away team
      player = update.players.away[goal.scorer];
      goalsObj.away.forEach((goalInfo: IGoalInfo) => {
        if (goalInfo.scorer === player.id) {
          // Extend goal info with scorer info
          goalInfo.player = player;
        }
      });
    } else {
      goalsObj.home.forEach((goalInfo: IGoalInfo) => {
        if (goalInfo.scorer === player.id) {
          // Extend goal info with scorer info
          goalInfo.player = player;
        }
      });
    }
  }

  /**
   * Get object with corners stats
   * @param generalInformationRequired - team|teams
   * @param {IScoreboardStatsUpdate} update
   * @returns {ITeams}
   */
  @BindDecorator
  getCorners(generalInformationRequired: string, update: IScoreboardStatsUpdate): ITeams {
    return this.getTeamStats(generalInformationRequired, update, TEAM_STATS.CORNERS);
  }

  /**
   * Get object with cards stats
   * @param generalInformationRequired - team | teams | player
   * @param {IScoreboardStatsUpdate} update
   * @returns {ITeams | ICardsByPlayer}
   */
  getBooking(generalInformationRequired: string, update: IScoreboardStatsUpdate): ITeams | ICardsByPlayer {
    switch (generalInformationRequired) {
      case 'team':
      case 'teams':
        return this.getTeamStats(generalInformationRequired, update, TEAM_STATS.CARDS);
      case 'player':
        return this.getCardsByPlayer(update);
    }
  }

  /**
   * Get cards by Player, extend object with providerId, id
   */
  getCardsByPlayer(update: IScoreboardStatsUpdate): ICardsByPlayer {
    return {
      cards: update.cards,
      away: { providerId: update.away.providerId, id: update.away.id },
      home: { providerId: update.home.providerId, id: update.home.id }
    };
  }

  /**
   * Get object with CardIndex stats
   * @param generalInformationRequired - team|teams
   * @param {IScoreboardStatsUpdate} update
   * @returns {ITeams}
   */
  @BindDecorator
  getCardIndex(generalInformationRequired: string, update: IScoreboardStatsUpdate): IPlayersSimple {
    return this.getPlayerStats('player', update, TEAM_STATS.CARDS);
  }

  /**
   * Get object with shots on target stats
   * @param generalInformationRequired - player
   * @param {IScoreboardStatsUpdate} update
   * @return {IPlayersSimple}
   */
  @BindDecorator
  getShotsOnTarget(generalInformationRequired: string, update: IScoreboardStatsUpdate): IPlayersSimple {
    return this.getPlayerStats(generalInformationRequired, update, PLAYER_STATS.SHOTS);
  }

  /**
   * Get object with shots stats
   * @param generalInformationRequired - player
   * @param {IScoreboardStatsUpdate} update
   * @return {IPlayersSimple}
   */
  @BindDecorator
  getShots(generalInformationRequired: string, update: IScoreboardStatsUpdate): IPlayersSimple {
    return this.getPlayerStats(generalInformationRequired, update, PLAYER_STATS.SHOTS);
  }

  /**
   * Get object with assist stats
   * @param generalInformationRequired - player
   * @param {IScoreboardStatsUpdate} update
   * @return {IPlayersSimple}
   */
  @BindDecorator
  getAssists(generalInformationRequired: string, update: IScoreboardStatsUpdate): IPlayersSimple {
    return this.getPlayerStats(generalInformationRequired, update, PLAYER_STATS.ASSISTS);
  }

  /**
   * Get object with passes stats
   * @param generalInformationRequired - player
   * @param {IScoreboardStatsUpdate} update
   * @return {IPlayersSimple}
   */
  @BindDecorator
  getPasses(generalInformationRequired: string, update: IScoreboardStatsUpdate): IPlayersSimple {
    return this.getPlayerStats(generalInformationRequired, update, PLAYER_STATS.PASSES);
  }

  /**
   * Get object with tackles stats
   * @param generalInformationRequired - player
   * @param {IScoreboardStatsUpdate} update
   * @return {IPlayersSimple}
   */
  @BindDecorator
  getTackles(generalInformationRequired: string, update: IScoreboardStatsUpdate): IPlayersSimple {
    return this.getPlayerStats(generalInformationRequired, update, PLAYER_STATS.TACKLES);
  }

  /**
   * Get object with crosses stats
   * @param generalInformationRequired - player
   * @param {IScoreboardStatsUpdate} update
   * @return {IPlayersSimple}
   */
  @BindDecorator
  getCrosses(generalInformationRequired: string, update: IScoreboardStatsUpdate): IPlayersSimple {
    return this.getPlayerStats(generalInformationRequired, update, PLAYER_STATS.CROSSES);
  }

  /**
   * Get object with offsides stats
   * @param generalInformationRequired - player
   * @param {IScoreboardStatsUpdate} update
   * @return {IPlayersSimple}
   */
  @BindDecorator
  getOffsides(generalInformationRequired: string, update: IScoreboardStatsUpdate): IPlayersSimple {
    return this.getPlayerStats(generalInformationRequired, update, PLAYER_STATS.OFFSIDES);
  }

  /**
   * Get object with GOALS_INSIDE_BOX stats
   * @param generalInformationRequired - player
   * @param {IScoreboardStatsUpdate} update
   * @return {IPlayersSimple}
   */
  @BindDecorator
  getGoalsInsideBox(generalInformationRequired: string, update: IScoreboardStatsUpdate): IPlayersSimple {
    return this.getPlayerStats(generalInformationRequired, update, PLAYER_STATS.GOALS_INSIDE_BOX);
  }
  /**
   * Get object with GOALS_OUTSIDE_BOX stats
   * @param generalInformationRequired - player
   * @param {IScoreboardStatsUpdate} update
   * @return {IPlayersSimple}
   */
  @BindDecorator
  getGoalsOutsideBox(generalInformationRequired: string, update: IScoreboardStatsUpdate): IPlayersSimple {
    return this.getPlayerStats(generalInformationRequired, update, PLAYER_STATS.GOALS_OUTSIDE_BOX);
  }

  /**
   * Get object with Shots Outside Box stats
   * @param generalInformationRequired - player
   * @param {IScoreboardStatsUpdate} update
   * @return {IPlayersSimple}
   */
  @BindDecorator
  getShotsOutsideBox(generalInformationRequired: string, update: IScoreboardStatsUpdate): IPlayersSimple {
    return this.getPlayerStats(generalInformationRequired, update, PLAYER_STATS.SHOTS_OUTSIDE_BOX);
  }

  /**
   * Get object with shotsWoodwork stats
   * @param generalInformationRequired - player
   * @param {IScoreboardStatsUpdate} update
   * @return {IPlayersSimple}
   */
  @BindDecorator
  getShotsWoodwork(generalInformationRequired: string, update: IScoreboardStatsUpdate): IPlayersSimple {
    return this.getPlayerStats(generalInformationRequired, update, PLAYER_STATS.SHOTS_WOODWORK);
  }

  /**
   * Get object by provided stat param
   * @param {string} generalInformationRequired - should be player
   * @param {IScoreboardStatsUpdate} update
   * @param {string} stat - depends on PLAYER_STATS
   * @return {IPlayersSimple}
   */
  getPlayerStats(generalInformationRequired: string, update: IScoreboardStatsUpdate, stat: string): IPlayersSimple {
    if (generalInformationRequired.includes('player')) {
      const { home, away } = update.players;

      return {
        home: Object.values(home).map((homePlayer: IPlayer): IPlayer => {
          const { id, providerId } = homePlayer;

          return { id, providerId, [stat]: homePlayer[stat], team: TEAMS.HOME.toLowerCase() } as IPlayer;
        }),
        away: Object.values(away).map((awayPlayer: IPlayer): IPlayer => {
          const { id, providerId } = awayPlayer;

          return { id, providerId, [stat]: awayPlayer[stat],  team: TEAMS.AWAY.toLowerCase() } as IPlayer;
        })
      };
    } else {
      return {} as IPlayersSimple;
    }
  }

  /**
   * Get object with red cards stats
   * @param generalInformationRequired - teams | player
   * @param {IScoreboardStatsUpdate} update
   * @returns { IRedCardsByTeams | IPlayersSimple }
   */
  @BindDecorator
  getRedCards(generalInformationRequired: string, update: IScoreboardStatsUpdate): IRedCardsByTeams | IPlayersSimple {
    switch (generalInformationRequired) {
      case 'teams':
      case 'team':
        return this.getRedsByTeams(update);
      case 'player':
        return this.getPlayerStats(generalInformationRequired, update, PLAYER_STATS.CARDS);
    }
  }

  /**
   * Get red cards by teams, extend object with teams info(providerId, name)
   * @param {IScoreboardStatsUpdate} update
   * @return {IRedCardsByTeams}
   */
  getRedsByTeams(update: IScoreboardStatsUpdate): IRedCardsByTeams {
    const { home, away } = update.teams;

    return {
      away: {
        id: update.away.id,
        providerId: update.away.providerId,
        periods: Object.keys(away)
          .reduce((previous: ITeam, key: string) => ({...previous, [key]: {redCards: away[key].cards.red}}), {} as ITeam)
      },
      home: {
        id: update.home.id,
        providerId: update.home.providerId,
        periods: Object.keys(home)
          .reduce((previous: ITeam, key: string) => ({...previous, [key]: {redCards: home[key].cards.red}}), {} as ITeam)
        }
      }
    ;
  }

  /**
   * Get red cards by players, extend object with teams info(providerId, name)
   * @param generalInformationRequired
   * @param {IScoreboardStatsUpdate} update
   * @return {IRedCardsByTeams}
   */
  @BindDecorator
  getRedCardsByTeamWithYellowCardsWorkAround(generalInformationRequired: string, update: IScoreboardStatsUpdate) {
    const { home, away } = update.players;
    const awayCards = this.getRedCardsByPlayer(away);
    const homeCards = this.getRedCardsByPlayer(home);

    return {
      away: {
        id: update.away.id,
        providerId: update.away.providerId,
        periods: awayCards
      },
      home: {
        id: update.home.id,
        providerId: update.home.providerId,
        periods: homeCards
      }
    };
  }

  /**
   * Get team status(home/away/draw) by ContestandId
   * @param  {IScoreboardStatsUpdate} update
   * @param  {IBybSelection} selection
   * @returns string
   */
  getHomeAwayTeamByContestantId(update: IScoreboardStatsUpdate, selection: IBybSelection): string {
    if (!update.home && !update.away) {
      return null;
    }
    const selectionName = selection.part.outcome[0].name.toLowerCase();
    const contestantId = selection.part.outcome[0].externalStatsLink?.contestantId;
    const { home, away } = update;
    const isDrawSelection = selectionName.includes(TEAMS.DRAW.toLowerCase());
    if (isDrawSelection) {
      return TEAMS.DRAW;
    } else if (contestantId === home.providerId) {
      return TEAMS.HOME;
    } else if (contestantId === away.providerId) {
      return TEAMS.AWAY;
    }
    return null; // Team name is different in OB and OPTA, should not show stats for such selections
  }
  /**
   * Get team status(home/away/draw) by outcome name
   * @param  {IScoreboardStatsUpdate} update
   * @param  {IBybSelection} selection
   * @returns string
   */
  getHomeAwayTeamByName(update: IScoreboardStatsUpdate, selection: IBybSelection): string {
    if (!update.home && !update.away) {
      return null;
    }
    const selectionName = selection.part.outcome[0].name.toLowerCase();
    const { home, away } = update;
    const homeTeamName = this.removeDiacritical(home.name.toLowerCase());
    const awayTeamName = this.removeDiacritical(away.name.toLowerCase());
    const isDrawSelection = selectionName.includes(TEAMS.DRAW.toLowerCase());

    if (homeTeamName.includes(selectionName) || selectionName.includes(homeTeamName)) {
      return TEAMS.HOME;
    } else if (awayTeamName.includes(selectionName) || selectionName.includes(awayTeamName)) {
      return TEAMS.AWAY;
    } else if (isDrawSelection) {
      return TEAMS.DRAW;
    }

    return null; // Team name is different in OB and OPTA, should not show stats for such selections
  }

  /**
   * Get double team (home or draw/away or draw/home or away) by outcome name
   * @param update
   * @param selection
   * @returns string
   */
  getDoubleHomeAwayTeamByContestantId(update: IScoreboardStatsUpdate, selection: IBybSelection): string {
    const selectionName = selection.part.outcome[0].name.toLowerCase();
    const contestantId =  selection.part.outcome[0].externalStatsLink?.contestantId;
    const { home, away } = update;
    if (contestantId === home.providerId && selectionName.includes(TEAMS.DRAW.toLowerCase())) {
      return DOUBLE_TEAMS.HOME_OR_DRAW;
    } else
    if (contestantId === away.providerId && selectionName.includes(TEAMS.DRAW.toLowerCase())) {
      return DOUBLE_TEAMS.AWAY_OR_DRAW;
    } else
    if (contestantId === home.providerId || contestantId === away.providerId) {
      return DOUBLE_TEAMS.HOME_OR_AWAY;
    }

    return null;
  }

  /**
   * Get current period
   * 1h (first half)
   * ht (half time)
   * 2h (second half)
   * ert (end of regular time)
   * et1h (extra time first half)
   * etht (extra time half time)
   * et2h (extra time second half)
   * pen (penalties)
   * fin (finished)
   * eet (extra time full time)"
   * @param currentPeriod
   */
  getCurrentPeriod(currentPeriod: string): string {
    const totalPeriods = ['ert', 'et1h', 'etht', 'et2h', 'pen', 'fin', 'eet'];
    const secondHalfPeriods = ['2h', 'ht'];

    if (totalPeriods.includes(currentPeriod)) {
      return PERIODS.total;
    } else if (secondHalfPeriods.includes(currentPeriod)) {
      return PERIODS['2ND_HALF'];
    }

    return PERIODS['1ST_HALF'];
  }

  /**
   * Get player by playerId
   * @param players
   * @param playerId
   */
  getPlayerById(players: IPlayersSimple, playerId: string): IPlayer {
    const homePlayer = this.findPlayerByIdAndTeam(players, playerId, TEAMS.HOME.toLowerCase());

    return homePlayer || this.findPlayerByIdAndTeam(players, playerId, TEAMS.AWAY.toLowerCase());
  }

  /**
   * Get player info based on name
   * @param name
   * @param players
   */
  getPlayerByName(name: string, players: IPlayers): IPlayer {
    return this.getPlayerByTeamPosition(name, players, TEAMS.HOME) || this.getPlayerByTeamPosition(name, players, TEAMS.AWAY);
  }

  /**
   * Get player info based on name/id
   * @param name
   * @param playerId
   * @param players
   */
  getPlayerFromNameId(name: string, playerId: string, players: IPlayers): IPlayer {
    return this.getPlayerByNameId(name, playerId, players, TEAMS.HOME) || this.getPlayerByNameId(name, playerId, players, TEAMS.AWAY);
  }

  /**
   * Add handicap value to proper team amount of goals.
   * RULES:
   * Selection Home (+1) -> score[period].home = score[period].home + 1
   * Selection Home (-1) -> score[period].home = score[period].home - 1
   * Selection Draw (+2) -> score[period].home = score[period].home + 2
   * Selection Draw (-2) -> score[period].home = score[period].home - 2
   * Selection Away (+3) -> score[period].away = score[period].away + 3
   * Selection Away (-3) -> score[period].away = score[period].away - 3
   * @param goalsObj
   * @param team - Home|Draw|Away
   * @param handicap
   * @param period - 1h|2h|total
   */
  applyHandicapValue(goalsObj: IScoreByTeams, team: string, handicap: number, period: string): IScoreByTeams {
    if (goalsObj.score[period]) {
      const correctTeam = team === TEAMS.DRAW ? TEAMS.HOME : team;
      goalsObj.score[period][correctTeam.toLowerCase()] += handicap;
    }

    return goalsObj;
  }

  /**
   * Get cards(red and yellow) from all players according to selected team(Home|Draw|Away)
   * @param players
   * @param team
   */
  getCardsFromPlayers(players: IPlayersSimple, team: string): IPlayerCards {
    const cards = {
      yellow: 0,
      red: 0
    };

    if (players[team.toLowerCase()]) {
      this.calculateSumOfPlayersCards(cards, players, team);
    } else {
      [TEAMS.HOME, TEAMS.AWAY].forEach((teamPosition: string) => {
        this.calculateSumOfPlayersCards(cards, players, teamPosition);
      });
    }

    return cards;
  }

  /**
   * Calculate booking points
   * Rules:
   * 1 x yellow card = 10 points
   * 1 x red card = 25 points
   * @param cards
   */
  getBookingPoints(cards: IPlayerCards): number {
    return cards.yellow * CARDS_INDEX.yellow + cards.red * CARDS_INDEX.red;
  }

  /**
   * Calculate sum of all players cards from selected team
   * @param cards
   * @param players
   * @param team
   */
  private calculateSumOfPlayersCards(cards: IPlayerCards, players: IPlayersSimple, team: string): void {
    players[team.toLowerCase()].forEach(player => {
      cards.red += player.cards.red;
      cards.yellow += player.cards.yellow;
    });
  }

  /**
   * Find player by id in home/away team
   * @param players
   * @param playerId
   * @param team
   */
  private findPlayerByIdAndTeam(players: IPlayersSimple, playerId: string, team: string): IPlayer {
    return players[team].find(player => player.providerId === playerId);
  }

  /**
   * Get object by provided stat param
   * @param generalInformationRequired - team|teams
   * @param {IScoreboardStatsUpdate} update
   * @param {string} stat - depends on PLAYER_STATS
   * @returns {ITeams}
   */
  private getTeamStats(generalInformationRequired: string, update: IScoreboardStatsUpdate, stat: string): ITeams {
    if (generalInformationRequired.includes('team')) {  // covers both 'team' and 'teams' statCategory
      const { home, away } = update.teams;

      return {
        away: Object.keys(away)
          .reduce((previous: ITeam, key: string) => ({
            ...previous,
            [key]: {
              [stat]: away[key][stat],
              providerId: update.away.providerId,
              id: update.away.id
            }
          }), {} as ITeam),
        home: Object.keys(home)
          .reduce((previous: ITeam, key: string) => ({
            ...previous,
            [key]: {
              [stat]: home[key][stat],
              providerId: update.home.providerId,
              id: update.home.id
            }
          }), {} as ITeam),
      };
    } else {
      return {} as ITeams;
    }
  }

  /**
   * Find player by name in home/away team
   * @param name
   * @param players
   * @param homeOrAway
   */
  private getPlayerByTeamPosition(name: string, players: IPlayers, homeOrAway: string): IPlayer {
    return Object.values(players[homeOrAway.toLowerCase()]).find((val: IPlayer) => {
      if (val.name.matchName.toLowerCase().includes(name.toLowerCase())) {
        val.homeAwaySide = homeOrAway;
        return true;
      }
    }) as IPlayer;
  }

  private getRedCardsByPlayer(homeAway: { [key: string]: IPlayer }) {
    return Object.keys(homeAway)
      .reduce((previous, key) => {
        const redCardCount = homeAway[key].cards.red > 0;
        const yellowCardCount = homeAway[key].cards.yellow >= 2;
        previous.total.redCards += redCardCount || yellowCardCount ? 1 : 0;

        return previous;
      }, {
        total: {
          redCards: 0
        }
      });
  }

  /**
   * Remove Diacritical
   * Converts name Córdoba to Cordoba
   * @param name
   */
  private removeDiacritical(name: string): string {
    return name.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }

  /**
   * Find player by name/Id in home/away team
   * @param playerName
   * @param playerId
   * @param players
   * @param homeOrAway
   */
  private getPlayerByNameId(playerName: string, playerId: string, players: IPlayers, homeOrAway: string): IPlayer {
   return Object.values(players[homeOrAway.toLowerCase()]).find((val: IPlayer) => {
     if (val.name.matchName.toLowerCase().includes(playerName.toLowerCase()) || val.providerId === playerId) {
       val.homeAwaySide = homeOrAway;
       return true;
     }
   }) as IPlayer;
  }
}
