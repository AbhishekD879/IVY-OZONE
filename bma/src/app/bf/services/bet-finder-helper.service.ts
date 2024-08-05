import { of as observableOf,  Observable } from 'rxjs';
import { mergeMap, map, catchError } from 'rxjs/operators';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { StorageService } from '@core/services/storage/storage.service';
import environment from '@environment/oxygenEnvConfig';
import { BF_CONSTANTS } from '../constants/config';

import { IBFConstants } from '../models/bf-constants.model';
import { IRacesListResponse, IRunner, IMeeting } from '../models/races-list.model';
import { IFilters } from '../models/filters.model';
import { UserService } from '@app/core/services/user/user.service';
import { IFiveASideBetModel, IFiveASideBetSuperModel } from '@app/betHistory/models/five-aside-bet.model';

@Injectable({
  providedIn: 'root'
})
export class BetFinderHelperService {
  savedFilters: IFilters = null;
  BET_FINDER_ENDPOINT: string;
  bfConstants: IBFConstants;

  constructor(
    private storageService: StorageService,
    private fracToDecService: FracToDecService,
    private http: HttpClient,
    private userService: UserService,
  ) {
    this.BET_FINDER_ENDPOINT = environment.BET_FINDER_ENDPOINT;
    this.bfConstants = BF_CONSTANTS;
    this.parseOdds = this.parseOdds.bind(this);
  }

  /**
   * Set Filters
   * Set currently selected filters, into the variable for reuse.
   *
   */
  setFilters(filters: IFilters): void {
    this.savedFilters = filters;
  }

  /**
   * Get Runners
   * Call getRacesList method and return filtered runners.
   *
   * @return {array} - list of filtered runners.
   */
  getRunners(): Observable<IRunner[]> {
    return this.getRacesList().pipe(
      map((res: IRacesListResponse) => {
        const filters = this.savedFilters || this.storageService.get('betFinderFilters') || {
          meetingShort: 'All',
          minPrice: 0,
          maxPrice: 1000
        };

        if (!res || !res.cypher) {
          console.warn('No results found');
          return [];
        }

        filters.meetingShort = this.getMeeting(filters.meetingShort, res.cypher.meetings).courseShort;
        return this.filterRunners(res.cypher.runners, filters);
      }));
  }

  /**
   * Filter Runners.
   * Filter runners by all the filters.
   *
   * @param {array} runners - list of unfiltered runners.
   * @param {object} filters - current filters.
   * @return {array} - list of filtered runners.
   */
  filterRunners(runners: IRunner[], filters: IFilters): IRunner[] {
    return runners
      .filter(runner => this.filterByStars(runner, filters.starSelection))
      .filter(runner => this.filterByFormButtons(runner, filters))
      .filter(runner => this.filterByProvenButtons(runner, filters))
      .filter(runner => this.filterBySuperComputer(runner.supercomputerSelection, filters))
      .filter(runner => this.filterByMeeting(runner, filters.meetingShort))
      .filter(runner => this.filterByName(runner, filters.runnerName))
      .filter(runner => this.filterByPriceButtons(runner, filters));
  }

  /**
   * getRacesList
   * Call getRacesList service.
   *
   * @return {object} - promise
   */
  getRacesList(): Observable<IRacesListResponse | null[]> {
    return this.getData().pipe(
      map((data: HttpResponse<any>) => data.body),
      mergeMap(this.parseOdds),
      catchError(err => observableOf([])));
  }

  /**
   * Get the contestids for the five a side bets
   * @returns IFiveASideBetModel[]
   */
   public getContestIdsForFiveASideBets(betIds: string[]): Observable<IFiveASideBetModel[]> {
    const FIVEASIDE_BETS_PATH = environment.SHOWDOWN_MS;
    const BRAND = environment.brand;
    const params = {
      userId: this.userService.username,
      token: this.userService.bppToken,
      betIds: betIds,
      brand: BRAND
    };
    const FIVEASIDE_BETS_URL =  `${FIVEASIDE_BETS_PATH}/${BRAND}/mybets-widget`;
    return this.http.post<IFiveASideBetSuperModel>(FIVEASIDE_BETS_URL, params, { observe: 'response' }).pipe(
    map((response: HttpResponse<IFiveASideBetSuperModel>) => response.body.myBetWidgetInfo));
  }

  private getData<T>(): Observable<HttpResponse<T>> {
    return this.http.get<T>(this.BET_FINDER_ENDPOINT, { observe: 'response' });
  }

  /**
   * Get meeting.
   * If saved meeting still exists in the response return it, otherwise return defaul meeting.
   * @param {string} meeting - short name for the meeting.
   * @param {array} meetings - array of meetings available in the response.
   * @return {string} - short name for a saved or default meeting.
   */
  private getMeeting(meeting: string, meetings: IMeeting[]): IMeeting {
    return _.find(meetings, { courseShort: meeting }) || { courseShort: 'All' };
  }

  /**
   * Filter By Stars
   * Filter runners by star rating.
   *
   * @param {object} runner - current runner information.
   * @param {string} starSelection - current filter startSelection.
   * @return {boolean} - whether runner qualify through the filter.
   */
  private filterByStars(runner: IRunner, starSelection: number): boolean {
    return !starSelection || runner.starRating === starSelection.toString();
  }

  /**
   * Filter By Buttons
   * Filter runners by any checkbox button.
   *
   * @param {object} runner - current runner information.
   * @param {string} button - current filter button value.
   * @param {object} filters - current filters.
   * @return {boolean} - whether runner qualify through the filter.
   */
  private filterByButton(runner: IRunner, button: string, filters: IFilters): boolean {
    return !filters[button] || runner[button] === 'Y';
  }

  /**
   * Filter By Proven Buttons
   * Filter runners by proven checkbox buttons.
   *
   * @param {object} runner - current runner information.
   * @param {object} filters - current filters.
   * @return {boolean} - whether runner qualify through the filter.
   */
  private filterByProvenButtons(runner: IRunner, filters: IFilters): boolean {
    return _.every(this.bfConstants.provenButtons, button => this.filterByButton(runner, button, filters));
  }

  /**
   * Filter By Form Buttons
   * Filter runners by form checkbox buttons.
   *
   * @param {object} runner - current runner information.
   * @param {object} filters - current filters.
   * @return {boolean} - whether runner qualify through the filter.
   */
  private filterByFormButtons(runner: IRunner, filters: IFilters): boolean {
    return _.every(this.bfConstants.formButtons, button => this.filterByButton(runner, button, filters));
  }

  /**
   * Filter By Supercomputer Buttons
   * Filter runners by supercomputer radio button.
   *
   * @param {string} value - current runner cupercomputer information.
   * @param {object} filters - current filters.
   * @return {boolean} - whether runner qualify through the filter.
   */
  private filterBySuperComputer(value: string, filters: IFilters): boolean {
    let selected = '';

    _.each(this.bfConstants.computerButtons, (button: string) => {
      selected = filters[button] ? button.slice(0, 1).toUpperCase() : selected;
    });

    return !selected || value === selected;
  }

  /**
   * Filter By Meeting
   * Filter runners by meeting.
   *
   * @param {object} runner - current runner information.
   * @param {object} meeting - current filter meeting value.
   * @return {boolean} - whether runner qualify through the filter.
   */
  private filterByMeeting(runner: IRunner, meeting: string): boolean {
    return meeting === 'All' || meeting === runner.courseShort;
  }

  /**
   * Filter By Name
   * Filter runners by jockey, trainer or horse name.
   *
   * @param {object} runner - current runner information.
   * @param {string} runnerName - current filter runnerName value.
   * @return {boolean} - whether runner qualify through the filter.
   */
  private filterByName(runner: IRunner, runnerName: string): boolean {
    return !runnerName ||
      runner.horseName.toLowerCase().indexOf(runnerName.toLowerCase()) > -1 ||
      runner.jockeyName.toLowerCase().indexOf(runnerName.toLowerCase()) > -1 ||
      runner.trainerName.toLowerCase().indexOf(runnerName.toLowerCase()) > -1;
  }

  /**
   * Filter By Price.
   * Filter runners by price range.
   *
   * @param {object} runner - current runner information.
   * @param {object} filters - current filters.
   * @return {boolean} - whether runner qualify through the filter.
   */
  private filterByPriceButtons(runner: IRunner, filters: IFilters): boolean {
    return _.every(this.bfConstants.oddsButtons, (button: string) => !filters[button]) ||
      _.some(this.bfConstants.oddsButtons, button => filters[button] && runner[button] === 'Y');
  }

  /**
   * Parse Odds.
   * Calculate runners decimal odds and set min and max prices.
   *
   * @param {object} res - response received from the getRacesList request.
   * @return {object} - modified response.
   */
  private parseOdds(res: IRacesListResponse): Observable<IRacesListResponse> {
    _.each(res.cypher.runners, (runner: IRunner) => {
      const frac = runner.odds.split('/');
      runner.decimalOdds = frac.length > 1 ? Number(this.fracToDecService.getDecimal(+frac[0], +frac[1])) : 0;
      this.setOddsRange(runner);
    });

    return observableOf(res);
  }

  /**
   * Set Odds Range.
   * Set range where odds belong to.
   *
   * @param {object} runner - runner object.
   */
  private setOddsRange(runner: IRunner): void {
    if (runner.decimalOdds >= 0 && runner.decimalOdds <= 2) {
      runner.odds0 = 'Y';
    } else if (runner.decimalOdds <= 4.5) {
      runner.odds1 = 'Y';
    } else if (runner.decimalOdds <= 8.5) {
      runner.odds4 = 'Y';
    } else if (runner.decimalOdds <= 15) {
      runner.odds8 = 'Y';
    } else if (runner.decimalOdds <= 29) {
      runner.odds16 = 'Y';
    } else {
      runner.odds32 = 'Y';
    }
  }


}
