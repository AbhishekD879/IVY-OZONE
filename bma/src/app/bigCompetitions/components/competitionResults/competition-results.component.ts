import { Component, Input, OnInit } from '@angular/core';
import * as _ from 'underscore';

import { ISportEvent } from '@core/models/sport-event.model';
import { ICompetitionModules, IResultsGroups, IResultsMatches } from '@app/bigCompetitions/services/bigCompetitions/big-competitions.model';

@Component({
  selector: 'competition-results',
  templateUrl: './competition-results.html',
  styleUrls: ['competition-results.component.scss']

})
export class CompetitionResultsComponent implements OnInit {
  @Input() moduleConfig: ICompetitionModules;

  matchesAmount: number = 0;
  limit: number = 0;
  showMoreAvailable: boolean;

  constructor() { }

  ngOnInit(): void {
    _.each(this.moduleConfig.results, (group: IResultsGroups) => {
      group.limit = this.matchesAmount;
      group.matches = _.chain(group.matches)
        .each((match: IResultsMatches) => {
          match.index = ++this.matchesAmount;
        })
        .sortBy((match: IResultsMatches) => match.teamA.name)
        .value();
    });

    this.showMore();
  }

  trackByEvent(index: number, event: ISportEvent): string {
    return `${index}${event.id}`;
  }

  trackByGroup(index: number, group: IResultsGroups): string {
    return `${index}${group.date}`;
  }

  /**
   * Show next amount of results.
   */
  showMore(): void {
    this.limit += this.moduleConfig.maxDisplay;
    this.showMoreAvailable = this.limit < this.matchesAmount;
  }
  getHeaderClass() {
    return (this.moduleConfig?.brand?.brand === 'Coral' &&
      this.moduleConfig?.brand?.device === 'Mobile') ? 'forced-chevron-up-and-styles' : '';
  }
  /**
   * Checks if date group should be visible with current limit.
   * @param {Object} group
   * @return {boolean}
   */
  isGroupVisible(group: IResultsGroups): boolean {
    return this.limit > group.limit;
  }

  /**
   * Checks if result event should be visible with current limit.
   * @param {Object} event
   * @return {boolean}
   */
  isEventVisible(event: ISportEvent): boolean {
    return this.limit >= event.index;
  }
}
