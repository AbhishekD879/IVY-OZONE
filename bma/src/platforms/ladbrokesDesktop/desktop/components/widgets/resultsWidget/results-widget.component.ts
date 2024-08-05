
import {from as observableFrom } from 'rxjs';
import { Component, Input, OnInit, ViewEncapsulation } from '@angular/core';
import * as _ from 'underscore';

import { CommandService } from '@core/services/communication/command/command.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import environment from '@environment/oxygenEnvConfig';
import { IMatchesByDate } from '@desktop/models/results-widget.model';
import {
  IStatsMatchResult,
  IStatsMatchResultGroupedMatches,
  IStatsSeasons
} from '@app/stats/models';
import { IStatsMatchResultGroup } from '@app/stats/models/match-result/grouped-matches.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IWidgetParams } from '@desktop/models/wigets.model';

@Component({
  selector: 'results-widget',
  templateUrl: './results-widget.component.html',
  styleUrls: ['./results-widget.component.scss'],
  // eslint-disable-next-line
  encapsulation : ViewEncapsulation.None
})
export class ResultsWidgetComponent implements OnInit {
  @Input() params: IWidgetParams;

  showMoreAvailable = false;
  widgetTitle = 'Results';
  loader = false;
  matchesByDate: IStatsMatchResultGroup = {};
  matchesByDateArray: IMatchesByDate[];

  private sportId = environment.CATEGORIES_DATA.footballId;
  private isFirstTimeCollapsed = false;
  private seasonId = null;
  private skip = 0;
  private limit = 4;

  constructor(
    private commandService: CommandService,
    private pubSubService: PubSubService
  ) { }

  ngOnInit(): void {
    observableFrom(this.commandService
      .executeAsync(this.commandService.API.GET_SEASON, [this.sportId, this.params.classId, this.params.typeId], {}))
      .subscribe((season: IStatsSeasons) => {
        this.pubSubService.publish(this.pubSubService.API.WIDGET_VISIBILITY, { results: !_.isEmpty(season) });

        if (season.id) {
          this.seasonId = season.id;
          this.showMore();
          this.limit = 9;
          this.skip = -5; // -5 to reset skip in next show more -5+8=3 next skip shoud be 3
        }
      }, err => {
        console.warn(err);
      });
  }

  trackByDate(index: number, matchGroup: IMatchesByDate): string {
    return matchGroup.date;
  }

  trackById(index: number, event: ISportEvent): number {
    return event.id;
  }

  /**
   * send GTM tracking, Collapse
   */
  sendCollapseGTM(): void {
    if (this.isFirstTimeCollapsed) {
      return;
    }
    this.sendGTM('collapse');
    this.isFirstTimeCollapsed = true;
  }

  /**
   * send GTM tracking, when user click Show more
   */
  sendShowMoreGTM(): void {
    this.sendGTM('show more');
  }

  /**
   * Loads matches
   */
  showMore(): void {
    this.loader = true;

    observableFrom(this.commandService
      .executeAsync(this.commandService.API.GET_MATCHES_BY_SEASON, [this.seasonId, this.skip, this.limit], {}))
      .subscribe((matches: IStatsMatchResultGroupedMatches) => {
        this.skip += this.limit - 1;
        this.showMoreAvailable = matches.showButton;
        this.extendByDate(this.matchesByDate, matches.matches);
        this.matchesByDateArray = this.matchesToArray(this.matchesByDate);
        this.loader = false;
      }, err => {
        console.warn(err);
      });
  }

  /**
   * Check if date has matches
   */
  hasMatchesByDate(): boolean {
    return _.isEmpty(this.matchesByDate);
  }

  /**
   * send GTM tracking, when user click on eventName
   * @param {String} eventName - event name
   */
  private sendGTM(eventName: string): void {
    this.pubSubService.publish(this.pubSubService.API.PUSH_TO_GTM, ['trackEvent', {
      eventCategory: 'widget',
      eventAction: 'results',
      eventLabel: `${eventName}`
    }]);
  }

  /**
   * Extends object by date
   */
  private extendByDate(expandableMatchesObject: IStatsMatchResultGroup, requestedMatchesObject: IStatsMatchResultGroup): void {
    _.each(requestedMatchesObject, (value: IStatsMatchResult[], key: string) => {
      if (expandableMatchesObject[key]) {
        expandableMatchesObject[key].push(...value);
      } else {
        expandableMatchesObject[key] = value;
      }
    });
  }

  private matchesToArray(matchesByDate): IMatchesByDate[] {
    const result = [];

    for (const matchesDate in matchesByDate) {
      if (matchesByDate.hasOwnProperty(matchesDate)) {
        const orderedMatches = _.chain(matchesByDate[matchesDate])
          .sortBy(item => item.teamA.name.toLowerCase())
          .sortBy(item => -item.date)
          .value();

        result.push({
          date: matchesDate,
          matches: orderedMatches
        });
      }
    }

    return result;
  }
}
