import { Input, Component, OnInit } from '@angular/core';
import * as _ from 'underscore';

import { CommandService } from '@core/services/communication/command/command.service';

import { IStatsMatchResultGroupedMatches } from '@app/stats/models/match-result/grouped-matches.model';
import { IStatsMatchResult } from '@app/stats/models/match-result/match-result.model';

@Component({
  selector: 'competitions-results-tab',
  templateUrl: 'competitions-results-tab.component.html',
  styleUrls: ['competitions-results-tab.component.scss']
})
export class CompetitionsResultsTabComponent implements OnInit {
  @Input() seasonId: string;
  @Input() isLoaded: boolean;

  results: { title: string; matches: IStatsMatchResult[] }[] = [];
  isShowMoreAvailable: boolean = false;
  isSpinnerVisible: boolean = false;
  isLoadingMore: boolean = false;

  private limit: number = 8;
  private skip: number = 0;

  constructor(private commandService: CommandService) {}

  ngOnInit(): void {
    this.loadResultsData();
  }

  /**
   * Load Results Data
   */
  loadResultsData(doLoadMore: boolean = false): void {
    if (this.seasonId) {
      if (doLoadMore) {
        this.isLoadingMore = true;
      } else {
        this.isSpinnerVisible = true;
      }

      this.commandService.executeAsync(this.commandService.API.GET_MATCHES_BY_SEASON, [this.seasonId, this.skip, this.limit], {})
        .then((result: IStatsMatchResultGroupedMatches) => {
          this.skip += this.limit - 1;
          this.isShowMoreAvailable = result.showButton;
          this.extendResultsData(result.matches);
          this.isSpinnerVisible = false;
          this.isLoadingMore = false;
        }, error => {
          this.isSpinnerVisible = false;
          this.isLoadingMore = false;
          console.warn('Results Data:', error.error || error);
        });
    } else {
      this.isSpinnerVisible = false;
      this.results = [];
    }
  }

  /**
   * Extend Results Data
   * @param { [key: string]: IStatsMatchResult[] } matches
   */
  extendResultsData(matches: { [key: string]: IStatsMatchResult[] }): void {
    _.each(matches, (value: IStatsMatchResult[], key: string) => {
      const results = _.findWhere(this.results, { title: key });
      if (results) {
        results.matches = this.sortResultsData(results.matches.concat(value));
      } else {
        this.results.push({
          title: key,
          matches: this.sortResultsData(value)
        });
      }
    });
  }

  /**
   * Sort results data
   * @param {IStatsMatchResult[]} data
   * @returns {IStatsMatchResult[]}
   */
  sortResultsData(data: IStatsMatchResult[]): IStatsMatchResult[] {
    return _(data).chain().sortBy((team: IStatsMatchResult) => {
      return team.teamA.name.toLowerCase();
    }).sortBy((team: IStatsMatchResult) => {
      return -team.date;
    }).value();
  }
}

