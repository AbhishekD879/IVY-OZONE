
import { of as observableOf, from as observableFrom,  Observable, throwError } from 'rxjs';

import { catchError, map, concatMap } from 'rxjs/operators';
import { Component, Input, OnInit } from '@angular/core';
import * as _ from 'underscore';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CommandService } from '@core/services/communication/command/command.service';
import {
  IStatsBRCompetitionSeason,
  IStatsCompetitions,
  IStatsResults
} from '@app/stats/models';
import { IStatsRow, IStatsRowValue } from '@app/stats/models/row.model';
import { IWidgetParams } from '@desktop/models/wigets.model';
import { IAllSeasons } from '@app/stats/models/br-competition-season.model';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'table-widget',
  templateUrl: './table-widget.component.html',
  styleUrls: ['./table-widget.component.scss']
})
export class TableWidgetComponent implements OnInit {
  @Input() params: IWidgetParams;

  tableTitle: string = 'League Table';
  tableLimit: number = 5;
  seasonIndex: number = 0;
  showLimit: boolean = true;
  seasons: IAllSeasons[] = [];
  competitionId: string;
  competitions: IStatsCompetitions[];
  activeTab: IStatsCompetitions;
  result: IStatsResults;
  tableData: IStatsRow[];

  private sportId: number = Number(environment.CATEGORIES_DATA.footballId);
  private isFirstTimeCollapsed: boolean = false;
  private isShowAllClicked: boolean = false;

  constructor(
    private commandService: CommandService,
    private pubSubService: PubSubService
  ) {}

  ngOnInit(): void {
    this.params.sportId = this.sportId;

    observableFrom(this.commandService.executeAsync(this.commandService.API.GET_LEAGUE_TABLE, [this.params], {})).pipe(
      concatMap((competitions: IStatsBRCompetitionSeason) => {
        if (competitions.status === 'Mapping not found') {
          return throwError('Mapping not found');
        }
        this.competitionId = competitions.competitionId.toString();

        this.competitions = _.filter(competitions.allCompetitions,
          (competition: IStatsCompetitions) => this.filterCompetition(competition));
        this.competitions = _.sortBy(this.competitions, 'id');

        this.seasons = competitions.allSeasons;
        this.setSeasonIndex(this.seasons);
        this.createTabsForCurrentSeason();

        if (this.seasons[this.seasonIndex]) {
          this.getCurrentSeason(this.seasons[this.seasonIndex]).subscribe(null, (err) => console.warn(err));
        } else {
          return observableOf(null);
        }
        return observableOf(this.competitions[0]);
      }))
      .subscribe(() => {
        this.handleWidgetVisibiliy();
      }, () => {
        this.handleWidgetVisibiliy();
      });
  }

  trackById(index: number, statsRow: IStatsRow): string {
    return `${index}_${statsRow.id}`;
  }

  /**
   * Change group for table widget
   * @param {object} tab - selected tab data
   */
  changeGroup({ tab }): void {
    this.activeTab = tab;
    this.competitionId = tab.id;

    this.getCurrentSeason(this.seasons[this.seasonIndex]).subscribe(null, (err) => console.warn(err));
    this.sendGTM('change league');
  }

  /**
   * Filtered competitions
   * @param competition
   * @return {object|null}
   */
  filterCompetition(competition: IStatsCompetitions): boolean {
    competition.title = competition.name.split(',').join(' ');
    return !competition.name.match(/playoff|knockout|qualification|preliminary round/i);
  }

  /**
   * Check widget availibility to show/hide widget column
   */
  handleWidgetVisibiliy(): void {
    this.pubSubService.publish(this.pubSubService.API.WIDGET_VISIBILITY, { table: !_.isEmpty(this.seasons) });
  }

  /**
   * Get value for table from row
   * @param {Object} values
   * @param {String} tableKey
   * @return {Object} value
   */
  getTableValue(values: IStatsRowValue[], tableKey: string): string {
    const obj: IStatsRowValue = _.findWhere(values, { key: tableKey });
    return obj && obj.value;
  }

  limitRows(): void {
    if (this.result && this.result.rows && this.showLimit) {
      this.tableData = this.result.rows.slice(0, this.tableLimit);
    } else {
      this.tableData = this.result.rows;
    }
  }

  /**
   * Go to next season
   */
  goToNext(): void {
    ++this.seasonIndex;
    this.createTabsForCurrentSeason();
    const season: IAllSeasons = this.seasons[this.seasonIndex];
    this.getCurrentSeason(season).subscribe(null, (err) => console.warn(err));
    this.sendGTM('change season');
  }

  /**
   * Go to prev season
   */
  goToPrev(): void {
    --this.seasonIndex;
    this.createTabsForCurrentSeason();
    const season: IAllSeasons = this.seasons[this.seasonIndex];
    this.getCurrentSeason(season).subscribe(null, (err) => console.warn(err));
    this.sendGTM('change season');
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
   * Show all teams
   */
  showAll(): void {
    this.showLimit = !this.showLimit;
    this.limitRows();

    if (this.isShowAllClicked) {
      return;
    }
    this.sendGTM('show full table');
    this.isShowAllClicked = true;
  }

  isNoEvents(): boolean {
    return this.result === null;
  }

  private createTabsForCurrentSeason(): void {
    _.each(this.competitions, (competition: IStatsCompetitions) => {
      if (this.competitions.length >1 && competition['type'] == 'parent' && this.seasons[this.seasonIndex].competitionIds.length>1) {
        competition.hidden = true;
      } else if (!_.contains(this.seasons[this.seasonIndex].competitionIds, competition.id)) {
        competition.hidden = true;

        if (this.competitionId !== this.competitions[0].id) {
          this.competitionId = this.competitions[0].id;
          this.activeTab = this.competitions[0];
        }
      } else {
        competition.hidden = false;
      }
    });
    if (this.competitions.length >1) {
      const competion = this.competitions.find(ele => ele.hidden == false);
      this.competitionId = competion?.id;
      this.activeTab = competion;
    } else {
      this.activeTab = this.competitions[0];
    }
  }

  showTabs(competitions) {
    return competitions.filter(ele=> ele.hidden === false).length > 1;
  }

  /**
   * send GTM tracking, when user click on eventName
   * @param {String} eventName - event name
   */
  private sendGTM(eventName: string): void {
    this.pubSubService.publish(this.pubSubService.API.PUSH_TO_GTM, ['trackEvent', {
      eventCategory: 'widget',
      eventAction: 'league table',
      eventLabel: `${eventName}`
    }]);
  }

  /**
   * Get current season results
   * @param {Object} currentSeason
   * @private
   */
  private getCurrentSeason(currentSeason: IAllSeasons): Observable<void> {
    const params = {
      areaId: currentSeason.areaId,
      competitionId: this.competitionId,
      seasonId: currentSeason.id,
      sportId: currentSeason.sportId
    };

    return observableFrom(this.commandService.executeAsync(this.commandService.API.GET_RESULT_TABLES, [params], [])).pipe(
      map((results: IStatsResults[]) => {
        this.result = results[0];
        this.limitRows();
      }), catchError((err) => {
        this.result = null;

        return observableOf(err);
      }));
  }

  private setSeasonIndex(seasons: IAllSeasons[]): void {
    if (seasons.length) {
      const currentDate: Date = new Date();

      seasons.forEach((season, index) => {
        const startDate: Date = new Date(season.startDate);
        const endDate: Date = new Date(season.endDate);

        if (currentDate >= startDate && currentDate <= endDate) {
          this.seasonIndex = index;
        } else {
          const endDates: number[] = seasons.map((s) => new Date(s.endDate).getTime());
          const latestDate: number = Math.max(...endDates);

          this.seasonIndex = endDates.findIndex((date) => date === latestDate);
        }
      });
    }
  }
}
