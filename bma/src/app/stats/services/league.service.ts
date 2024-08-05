import { Observable, of as observableOf, throwError as observableThrowError } from 'rxjs';
import { catchError, concatMap, map, mergeMap } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { StatsPointsProvider } from './stats-points.provider';
import { CommandService } from '@core/services/communication/command/command.service';
import {
  IStatsAreas,
  IStatsAreasAndCompetitions,
  IStatsCompetitions,
  IStatsIdsConfig,
  IStatsRequestParams,
  IStatsResults,
  IStatsSeasons
} from '../models';

@Injectable()
export class LeagueService {
  private ids: IStatsIdsConfig;
  private areas: IStatsAreas[];
  private competitions: IStatsCompetitions[] = [];
  private seasons: IStatsSeasons[] = [];
  private areasAndCompetitionsData: Observable<IStatsAreasAndCompetitions>;

  constructor(
    private statsPointsProvider: StatsPointsProvider,
    private commandService: CommandService) {
    this.ids = {
      sportId: '1',
      areaId: '',
      competitionId: '',
      seasonId: '',
      rows: []
    };
  }

  registerCommand(): void {
    this.commandService.register(this.commandService.API.GET_COMPETITION_AND_SEASON,
      (params: IStatsRequestParams) => this.getCompetitionAndSeason(params).toPromise());

    this.commandService.register(this.commandService.API.GET_SEASONS,
      (params: IStatsRequestParams) => this.getSeasons(params).toPromise());

    this.commandService.register(this.commandService.API.GET_RESULT_TABLES,
      (params: IStatsRequestParams) => this.getResultsTables(params).toPromise());

    this.commandService.register(this.commandService.API.GET_LEAGUE_TABLE,
      (params: IStatsRequestParams) => this.statsPointsProvider.leagueTableCompetitionSeason(params).toPromise());
  }

  /**
   * Get areas
   * @returns {Promise}
   */
  getAreas(): Observable<IStatsAreas[]> {
    return this.areas ? observableOf(this.areas) : this.statsPointsProvider.leagueTableAreas(_.pick(this.ids, 'sportId')).pipe(
      map(result => {
        this.areas = _.sortBy(result, area => Number(area.id));
        return this.areas;
      }),
      catchError(error => this.errorHandler('leagueTableAreas', error)));
  }

  /**
   * Get results tables
   * @param {Object} params
   * @returns {Promise}
   */
  getResultsTables(params: IStatsRequestParams): Observable<IStatsResults[]> {
    return this.statsPointsProvider.leagueTableResults(params).pipe(
      catchError(error => this.errorHandler('leagueTableResults', error)));
  }

  getCompetitionAndSeason(params: IStatsRequestParams): Observable<IStatsSeasons> {
    return this.getCompetitionAndSeasons(params)
      .pipe(map(allSeasons => this.getCurrentSeason(null, allSeasons)),
      catchError(() => observableOf({} as IStatsSeasons)));
  }

  /**
   * Get area name and list of competitions for this area
   * @param {string} areaId
   * @returns {Promise}
   */
  getAreaAndCompetitions(areaId: string): Observable<{value: IStatsAreasAndCompetitions }> {
    this.ids.areaId = areaId; // area_id1
    return this.getAreas().pipe(
      concatMap(() => this.getCompetitions()),
      map(() => this.returnData(areaId)),
      catchError(() => observableOf({ value: { area: '', competitions: [] } })));
  }

  /**
   * Get results table
   * @param {string} competitionId
   * @param {string} seasonId
   * @returns {Promise}
   */
  getStandings(competitionId: string, seasonId: string): Observable<string | IStatsResults[]> {
    const season = this.getCurrentSeason(seasonId, this.seasons) || {};

    if (!this.competitions.length || !season) {
      return observableOf([]);
    }

    const competitionIndex = _.findIndex(this.competitions, item => item.id === competitionId);
    const index = competitionIndex !== -1 ? competitionIndex : 0;

    this.ids.competitionId = this.competitions[index].id;
    this.ids.seasonId = season['id'];

    return this.ids.seasonId ? this.getResultsTables(this.ids).pipe(
      mergeMap(result => this.getCorrectResults(result)),
      catchError(() => observableOf([]))) : observableOf([]);
  }

  /**
   * @param {object} params
   * @returns {Promise}
   */
  getSeasons(params: IStatsRequestParams): Observable<IStatsSeasons[]> {
    return this.statsPointsProvider.leagueTableSeasons(_.pick(params, 'sportId', 'areaId', 'competitionId')).pipe(
      map(result => {
        this.seasons = _.sortBy(result, season => -new Date(this.clearDate(season.startDate)).getTime());
        return this.seasons;
      }),
      catchError(() => {
        this.seasons = [];
        return observableOf(this.seasons);
      }));
  }

  private returnData(areaId: string): any {
    const selectedArea = _.findWhere(this.areas, { id: areaId });
    const area = selectedArea ? selectedArea.name : '';
    this.areasAndCompetitionsData = observableOf({ area:area, competitions:  this.competitions });
    this.areasAndCompetitionsData.subscribe();
    return this.areasAndCompetitionsData;
  }

  /**
   * Compare competitions by uniqIdentifier and name
   * @param {Object}
   * @param {Object}
   * @returns {Number}
   */
  private compareByUniqIdentifierAndName(a: IStatsCompetitions, b: IStatsCompetitions): number {
    if (Number(a.uniqIdentifier) > Number(b.uniqIdentifier) ||
      (a.uniqIdentifier === b.uniqIdentifier && a.name > b.name)) {
      return 1;
    }
    if (Number(a.uniqIdentifier) < Number(b.uniqIdentifier) ||
      (a.uniqIdentifier === b.uniqIdentifier && a.name < b.name)) {
      return -1;
    }
    return 0;
  }

  /**
   * Set rows to data object
   * @param {Array} resultTables
   * @returns {Object}
   */
  private getCorrectResults(resultTables: IStatsResults[]): Observable<IStatsResults[] | string> {
    if (!resultTables.length) {
      return this.errorHandler('getSeasonId', 'There is no standings');
    }
    return observableOf(_.sortBy(resultTables, table => Number(table.tableId)));
  }

  /**
   * Return season by id or the active one
   * @param {string} seasonId
   * @param {Array} ISeasons[]
   * @returns {Object}
   */
  private getCurrentSeason(seasonId: string, seasons: IStatsSeasons[]): IStatsSeasons {
    if (seasonId) {
      return _.find(seasons, { id: seasonId }) || seasons[0];
    }

    return _.find(seasons, season => {
      const today = Date.now();
      const start = new Date(season.startDate).getTime();
      const end = new Date(season.endDate).getTime();
      return (start < today && end > today) || seasons[0];
    });
  }

  /**
   * On error update data object to return the correct one
   * @param {string}
   * @param {string}
   * @returns {Promise}
   */
  private errorHandler(serviceName: string, error: string): Observable<null[]> {
    console.warn(`Error: ${serviceName}`, error);
    return observableThrowError([]);
  }

  /**
   * Replacing unnecessary space in the date. Needed to fix betradar issue.
   * "2015-08-07T00:00:00 02:00" -> "2015-08-0.7T00:00:00+02:00"
   * @param {string}
   * @returns {string}
   */
  private clearDate(date: string): string {
    return date.replace(/ /ig, '+');
  }

  private getCompetitionAndSeasons(params: IStatsRequestParams): Observable<any> {
    return this.statsPointsProvider.leagueTableCompetitionSeason(params).pipe(
      mergeMap(result => {
        // if mapping not found
        if (!result.sportId || !result.areaId || !result.competitionId) {
          return <null[]>[];
        }

        return this.statsPointsProvider.leagueTableSeasons(_.pick(result, 'sportId', 'areaId', 'competitionId'));
      }),
      catchError(error => this.errorHandler('getCompetitionAndSeason', error)));
  }

  /**
   * Get competitions
   * @returns {Promise}
   */
  private getCompetitions(): Observable<IStatsCompetitions[]> {
    return this.statsPointsProvider.leagueTableCompetitions(_.pick(this.ids, 'sportId', 'areaId')).pipe(
      map(result => {
        result.sort(this.compareByUniqIdentifierAndName);
        this.competitions = result;
        // eslint-disable-next-line
        console.log(this.competitions);
      }),
      catchError(error => {
        this.competitions = [];
        // eslint-disable-next-line
        console.log(error);
        return observableOf(error);
      }));
  }
}
