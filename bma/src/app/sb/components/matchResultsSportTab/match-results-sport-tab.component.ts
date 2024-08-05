import { Component, OnInit } from '@angular/core';
import * as _ from 'underscore';

import { CommandService } from '@core/services/communication/command/command.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { IDate } from '@sb/components/matchResultsSportTab/date.model';
import { ICompetition } from '@sb/components/matchResultsSportTab/competition.model';

@Component({
  selector: 'match-results-sport-tab',
  templateUrl: 'match-results-sport-tab.html'
})
export class MatchResultsSportTabComponent implements OnInit {

  dates: IDate[];
  private page: number = 0;

  constructor(
    private commandService: CommandService,
    private filtersService: FiltersService
  ) { }

  ngOnInit() {
    this.showMoreDates();
  }

  /**
   * loadMatchesByDate()
   * @param {IDate} matchDate
   */
  loadMatchesByDate(matchDate: IDate): void {
    matchDate.opened = !matchDate.opened;

    if (!matchDate.competitions.length) {
      matchDate.loadingMatches = true;

      this.commandService.executeAsync(this.commandService.API.GET_MATCHES_BY_DATE, [matchDate.date], [])
        .then((competitionsMatches: ICompetition[]) => {
          matchDate.loadingMatches = false;
          matchDate.competitions = competitionsMatches;
        }, () => {
          matchDate.loadingMatches = false;
          matchDate.noResults = true;
        });
    }
  }

  /**
   * showMoreDates()
   */
  showMoreDates(): void {
    this.commandService.executeAsync(this.commandService.API.GET_RESULTS_BY_PAGE, [this.page], [])
      .then((results: IDate[]) => {
        this.dates = this.dates.concat(results);

        _.forEach(this.dates, (date: IDate) => {
          _.forEach(date.competitions, (competition: ICompetition) => {
            competition.matches = this.filtersService.orderBy(competition.matches, ['-date', 'teamA.name']);
          });
        });

        this.page += 1;
      });
  }

  /**
   * Track by function
   * @param {number} index
   * @returns {number}
   */
  trackDatesByFn(index: number): number {
    return index;
  }

  /**
   * Track by function
   * @param {number} index
   * @returns {number}
   */
  trackCompetitionsByFn(index: number): number {
    return index;
  }

  /**
   * Track by function
   * @param {number} index
   * @returns {number}
   */
  trackMatchesByFn(index: number): number {
    return index;
  }
}
