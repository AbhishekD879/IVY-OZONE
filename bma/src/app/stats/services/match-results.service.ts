
import { Observable, throwError } from 'rxjs';

import { mergeMap, map } from 'rxjs/operators';
import { Injectable } from '@angular/core';

import * as _ from 'underscore';

import { StatsPointsProvider } from './stats-points.provider';
import { TimeService } from '@core/services/time/time.service';
import { CommandService } from '@core/services/communication/command/command.service';

import {
  IStatsMatchResult,
  IStatsMatchResultGoal,
  IStatsMatchResultPage,
  IStatsSeasonMatch,
  IStatsSeasons,
  IStatsMatchResultScorer,
  IStatsMatchResultGroupedMatches,
  IStatsMatchResultMatchesWithGoalScorers,
  IStatsBRCompetitionSeason,
} from '../models';

@Injectable()
export class MatchResultsService {
  static readonly STEP: number = 7; // Step For Dates

  constructor(private statsPointsProvider: StatsPointsProvider,
              private timeService: TimeService,
              private commandService: CommandService) {}

  registerCommand(): void {
    this.commandService.register(this.commandService.API.GET_SEASON,
      (sportId: string, classId: string, typeId: string) => this.getSeason(sportId, classId, typeId).toPromise());

    this.commandService.register(this.commandService.API.GET_MATCHES_BY_SEASON,
      (seasonId: string, skip: number, limit: number) => {
        return this.getMatchesBySeasonByPage(seasonId, skip, limit).toPromise();
      });

    this.commandService.register(this.commandService.API.GET_RESULTS_BY_PAGE,
      (page: number) => Promise.resolve(this.getPage(page)));

    this.commandService.register(this.commandService.API.GET_MATCHES_BY_DATE,
      (date: Date) => this.getMatchesByDate(date).toPromise());
  }

  /**
   * Get seasons
   * @param  {String} sportId - openBat category id
   * @param  {String} classId    - openBat class id
   * @param  {String} typeId     - openBat type id
   * @return {Object}            - object with seasons by competition
   */
  getSeason(sportId: string, classId: string, typeId: string): Observable<IStatsSeasons | {}>  {
    return this.statsPointsProvider.leagueTableCompetitionSeason({
      sportId,
      classId,
      typeId
    }).pipe(mergeMap(data => this.getSeasonByCompetition(data)));
  }

  /**
   * Get matches by seasons by page grouped by date
   * @param  {String} seasonId - openBat string id
   * @param  {Number} skip     - number of skiped matches
   * @param  {Number} limit    - limit of matches
   * @return {Promise}         - return of all matches grouped by date
   */
  getMatchesBySeasonByPage(seasonId: string, skip: number, limit: number): Observable<IStatsMatchResultGroupedMatches> {
    return this.statsPointsProvider.seasonMatches(seasonId, skip, limit).pipe(
      map(res => this.getGoalScorersIds(res)), // Gets goalscorerers from match doc
      map(res => this.getPlayerDetails(res)),
      map(matches => {
        _.each(matches, match => {
          this.createResultsFromGoalString(match);
        });
        return {
          showButton: matches.length % limit === 0,
          matches
        };
      }),
      map(res => this.groupByDate(res)));
  }

  /**
   * Gets page according to step if step is 7 then it will give array of dates with 7 days
   * @param  {Number} page - page number wich should are requested
   * @return {Array}       - array of dates which have to be displayed
   */
  getPage(page: number) {
    const startDate = new Date();
    const res = [];

    if (page !== 0) { // If page is 0 we should return dates starting from now
      startDate.setDate(startDate.getDate() - page * MatchResultsService.STEP);
    }

    res.push(this.create(startDate)); // end start date to results

    for (let i = 1; i < MatchResultsService.STEP; i++) { // aggregate all dates to array.
      const date = new Date(startDate.getTime());
      date.setDate(startDate.getDate() - i);
      res.push(this.create(date));
    }

    return res;
  }

  /**
   * Send request to spark stats centre application
   * @param  {Date} date - date for which we should request data from stats centre application
   * @return {Promise}      [description]
   */
  getMatchesByDate(date: Date): Observable<IStatsMatchResult[]> {
    const requestDate = new Date(date.getTime()).toISOString().substring(0, 10);

    return this.statsPointsProvider.matchesByDate({
      startdate: requestDate,
      enddate: requestDate
    }).pipe(map(result => this.getGoalScorersIds(result)), // Gets goalscorerers from match doc
      map(result => this.getPlayerDetails(result)),
      map(result => this.groupByCompetition(result)), // group matches by competitions
      map(result => this.sortByDisplayOrder(result))); // sort matches by displayOrder
  }

  /**
   * Get season by competition
   * @param  {Object} competition - object with seasons by competition
   * @return {Object}             - object with season from competition
   */
  private getSeasonByCompetition(competition: IStatsBRCompetitionSeason): Observable<IStatsSeasons | string | null> {
    if (competition.sportId && competition.areaId && competition.competitionId) {
      return this.statsPointsProvider.leagueTableSeasons({
        sportId: String(competition.sportId),
        areaId: String(competition.areaId),
        competitionId: String(competition.competitionId)
      }).pipe(map(seasons => {
        if (!seasons || !seasons.length) { return null; }
        const today = Date.now();
        const activeSeason = seasons.find(season => new Date(season.startDate).getTime() < today &&
          new Date(season.endDate).getTime() > today);
        return activeSeason || seasons[seasons.length - 1];
      }));
    }
    return throwError(competition.status);
  }

  /**
   * Gets player details
   * @param  {Object} matchesWithGoalScorers - object with goalscorers players ids and stats centre matches.
   * @return {Promise}                       - promise with players details.
   */
  private getPlayerDetails(matchesWithGoalScorers: IStatsMatchResultMatchesWithGoalScorers): IStatsMatchResult[] {
    if (matchesWithGoalScorers.goalScorerIds &&
        matchesWithGoalScorers.goalScorerIds.length > 0) {
        matchesWithGoalScorers.matches.forEach(match => {
          match.teamA.goalScorers = this.createGoalScorerStr(match.teamA.goals);
          match.teamB.goalScorers = this.createGoalScorerStr(match.teamB.goals);
        });

        return matchesWithGoalScorers.matches;
    }
    return matchesWithGoalScorers.matches;
  }

  /**
   * Get grouped by date matches with correction date property
   * @param  {Object} matches - object with requested matches
   * @return {Object}         - Object with requested matches but with correctionDate property
   */
  private groupByDate(matchesObj: { showButton: boolean, matches: IStatsMatchResult[] }): IStatsMatchResultGroupedMatches {
    // delete 8s match
    if (matchesObj.showButton) {
      matchesObj.matches.splice(-1);
    }

    const matchesWithCorrectionDate = _.map(matchesObj.matches, match => {
      match.correctionDate = this.getDateStrting(match.date);
      return match;
    });

    const matches = _.groupBy(matchesWithCorrectionDate, 'correctionDate');

    return { showButton: matchesObj.showButton, matches };
  }

  /**
   * Create object with which UI should work.
   * @param  {String} date - date of matches
   * @return {Object}    - object with needed properties
   */
  private create(date: string | Date): IStatsMatchResultPage {
    return {
      date,
      loadingMatches: false,
      competitions: [],
      opened: false,
      dateString: this.getDateStrting(Number(date))
    };
  }

  /**
   * Group matches by competitions.
   * @param  {Array} matches - array with matches
   * @return {Array}         - array with competitions and matches assigned to that competition.
   */
  private groupByCompetition(matches: IStatsMatchResult[]): IStatsMatchResult[] {
    const groupedCompetititons = _.reduce(matches, (competitions, match) => {
      this.createResultsFromGoalString(match);

      let inArray = _.findLastIndex(competitions, { id: match.competition.id }); // Check if such competition already in the array
      if (inArray === -1) { // If competition is not in array adds it to array.
        competitions.push({
          id: match.competition.id,
          name: match.competition.name,
          displayOrder: match.competition.displayOrder,
          matches: [],
          opened: false
        });
        inArray = competitions.length - 1;
      }
      competitions[inArray].matches.push(match); // Adds match to competition.

      return competitions;
    }, []);

    return groupedCompetititons;
  }

  /**
   * Sorts competitons by display order.
   * @param  {Array} competitions - array with competitions.
   * @return {Array}              - array with competitions sorted by display order.
   */
  private sortByDisplayOrder(competitions: IStatsMatchResult[]): IStatsMatchResult[] {
    return competitions.sort((a, b) => a.displayOrder * 1 >= b.displayOrder * 1 ? 1 : -1);
  }

  /**
   * Check if results are present if not then set 0:0
   * @param  {Object} match - stats centre match
   */
  private createResultsFromGoalString(match: IStatsMatchResult): void {
    if (!match.result || !match.result.fullTime) {
      match.result = {
        fullTime: {
          value: '0:0'
        }
      };
    }

    const result = match.result.fullTime.value.split(':');
    match.teamA.score = result[0];
    match.teamB.score = result[1];
  }

  /**
   * Gets goalscorers player ids
   * @param  {Array} matches - array with stats centre matches
   * @return {Object}        - object with goalscorers players ids and stats centre matches
   */
  private getGoalScorersIds(matches: IStatsSeasonMatch[]): IStatsMatchResultMatchesWithGoalScorers {
    const playerIds = [];

    _.each(matches, match => {
      if (match.goals && match.goals.length > 0) {
        _.each(match.goals, goal => {
          if (goal.playerID) {
            playerIds.push(goal.playerID);
          }
        });
        match.teamA.goals = this.getTeamGoals('1', match.goals);
        match.teamB.goals = this.getTeamGoals('2', match.goals);
      } else if (match.result &&
                 match.result.goalsString &&
                 match.result.goalsString.length > 0) {
        this.getPlayerNameFromGoalString(match);
      }
    });

    return { matches, goalScorerIds: _.uniq(playerIds) };
  }

  /**
   * Gets team player goals from goal string.
   * @param  {Object} match - stats centre match.
   */
  private getPlayerNameFromGoalString(match: IStatsMatchResult): void {
    const goals = _.map(match.result.goalsString.split(', '), goalStr => {
      const values = goalStr.split(' ');
      return {
        score: values[0],
        time: values[1].replace(/\(/g, '').replace(/\)/g, '')
          .replace(/\./g, ''),
        playerLastname: values[2],
      };
    });

    const modifiedGoals = this.getGoalsByTeamByScore(goals);
    match.teamA.goals = modifiedGoals['teamA'];
    match.teamB.goals = modifiedGoals['teamB'];
  }

  /**
   * Gets goals for teams by score
   * @param  {Array} goals - array with goals from goal string
   * @return {Object}      - goals by team
   */
  private getGoalsByTeamByScore(goals: IStatsMatchResultGoal[]): { teamA: IStatsMatchResultScorer[], teamB: IStatsMatchResultScorer[]} {
    const score = {
      teamA: [],
      teamB: []
    };
    _.each(goals, goal => {
      const scorePerTeam = goal.score.split(':');
      score.teamA.push(Number(scorePerTeam[0]));
      score.teamB.push(Number(scorePerTeam[1]));
    });
    const res = {
      teamA: [],
      teamB: []
    };

    for (let i = 0; i < goals.length; i++) {
      if (i === 0) {
        if (score.teamA[i] > score.teamB[i]) {
          res.teamA.push(goals[i]);
        } else if (score.teamA[i] < score.teamB[i]) {
          res.teamB.push(goals[i]);
        }
      } else {
        if (score.teamA[i] > score.teamA[i - 1]) {
          res.teamA.push(goals[i]);
        } else if (score.teamB[i] > score.teamB[i - 1]) {
          res.teamB.push(goals[i]);
        }
      }
    }

    return res;
  }

  /**
   * Create goal scorer string.
   * @param  {Array} teamGoals - array with team goals.
   * @return {String}          - goalscorers string.
   */
  private createGoalScorerStr(teamGoals: IStatsMatchResultGoal[]): string {
    const groupedByName = _.groupBy(teamGoals, goal => `${goal.playerName}`);
    const res = [];
    _.each(groupedByName, (goals, name) => {
      const times = goals.map(goal => `${goal.time}'`).join(', ');
      res.push(`${name} ${times}`);
    });
    return res.join(', ');
  }

  /**
   * Gets goals by team.
   * @param  {String} teamNumber - number of team TeamA - 1, TeamB -2
   * @param  {Array} goals       - array with goals
   * @return {Array}             - array with goals for particular team.
   */
  private getTeamGoals(teamNumber: string, goals: IStatsMatchResultScorer[]): IStatsMatchResultScorer[] {
    return _.filter(goals, goal => goal.team === teamNumber && !!goal.playerID);
  }

  /**
   * Convert date to string 'Today, Tomorrow, format'
   * @param  {String} date - date which have to be converted.
   * @return {String}    - date string.
   */
  private getDateStrting(date: number): string | Date {
    return this.timeService.getTodayTomorrowOrDate(new Date(date), false, false);
  }
}
