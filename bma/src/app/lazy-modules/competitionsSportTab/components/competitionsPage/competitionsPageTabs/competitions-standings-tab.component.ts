import { throwError, of, from as observableFrom, Observable } from 'rxjs';
import { catchError, map, switchMap } from 'rxjs/operators';
import { Component, Input, OnInit } from '@angular/core';
import * as _ from 'underscore';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { IStatsBRCompetitionSeason, IStatsCompetitions, IStatsResults } from '@app/stats/models';
import { IStatsRow, IStatsRowValue } from '@app/stats/models/row.model';
import { IAllSeasons } from '@app/stats/models/br-competition-season.model';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';

@Component({
  selector: 'competitions-standings-tab',
  templateUrl: './competitions-standings-tab.component.html',
  styleUrls: ['./competitions-standings-tab.component.scss']
})
export class CompetitionsStandingsTabComponent extends AbstractOutletComponent implements OnInit {

  @Input() typeId: string;
  @Input() classId: string;
  @Input() seasonId: string;
  @Input() sportId?: number | string;
  @Input() isLoaded: boolean;

  tableLimit: number = 5;
  seasonIndex: number = 0;
  showLimit: boolean = false;
  seasons: IAllSeasons[] = [];
  competitionId: string;
  competitions: IStatsCompetitions[];
  competitionName: string;
  competitionYear: string;
  showTabs: boolean;
  activeTab: IStatsCompetitions;
  result: IStatsResults;
  tableData: IStatsRow[];

  private isFirstTimeCollapsed: boolean = false;
  private isShowAllClicked: boolean = false;

  constructor(
    private commandService: CommandService,
    private pubSubService: PubSubService
  ) {
    super()/* istanbul ignore next */;
  }

  ngOnInit(): void {
    const params = _.pick(this, ['typeId', 'classId', 'sportId']);
    this.showSpinner();
    this.sendGTM('view league table');

    observableFrom(this.commandService.executeAsync(this.commandService.API.GET_LEAGUE_TABLE, [params], {}))
      .pipe(switchMap((competitions: IStatsBRCompetitionSeason) => {
        if (competitions.status === 'Mapping not found') {
          return throwError('Mapping not found');
        }

        this.competitionId = competitions.competitionId.toString();
        this.competitions = _.filter(competitions.allCompetitions,
          (competition: IStatsCompetitions) => this.filterCompetition(competition));
        this.competitions = _.sortBy(this.competitions, 'id');
        this.competitionName = competitions.competitionName;
        this.seasons = competitions.allSeasons;

        if (this.seasons && this.seasons.length) {
          const index = _.findIndex(this.seasons, { id: this.seasonId });
          this.seasonIndex = index < 0 ? 0 : index;
          this.createTabsForCurrentSeason();
          return this.getCurrentSeason(this.seasons[this.seasonIndex]);
        }
        return throwError('Seasons not found');
      })).subscribe(() => {
        this.hideSpinner();
        }, err => {
        this.handleDefaultError(err);
      });
  }

  trackById(index: number, statsRow: IStatsRow): string {
    return `${index}_${statsRow.id}`;
  }

  /**
   * Change group for table widget
   * @param tab - selected tab data
   */
  changeGroup({ tab }): void {
    this.activeTab = tab;
    this.competitionId = tab.id;

    this.getCurrentSeason(this.seasons[this.seasonIndex]).subscribe(null, (err) => console.warn(err));
    this.sendGTM('change league');
  }

  /**
   * Filtered competitions
   * @param {IStatsCompetitions} competition
   * @return boolean
   */
  filterCompetition(competition: IStatsCompetitions): boolean {
    const nameSplit = competition.name.split(',').join(' ');
    competition.title = nameSplit.trim();
    return !competition.name.match(/playoff|knockout|qualification|preliminary round/i);
  }

  /**
   * Get value for table from row
   * @param {IStatsRowValue[]} values
   * @param {string} tableKey
   * @return string
   */
  getTableValue(values: IStatsRowValue[], tableKey: string): string {
    const obj: IStatsRowValue = _.findWhere(values, { key: tableKey });
    return obj && obj.value;
  }

  limitRows(): void {
    if (this.result && this.result.rows && this.showLimit) {
      this.tableData = this.result.rows.slice(0, this.tableLimit);
    } else {
      this.tableData = this.result && this.result.rows;
    }
  }

  /**
   * Go to next season
   */
  goToNext(): void {
    // Check seasonIndex to valid value to avoid setting seasonIndex > seasons.length(when user clicking goToNext element too fast)
    if (this.seasonIndex + 1 < this.seasons.length) {
      this.showSpinner();
      ++this.seasonIndex;
      this.createTabsForCurrentSeason();
      const season: IAllSeasons = this.seasons[this.seasonIndex];
      this.getCurrentSeason(season).subscribe(() => this.hideSpinner(), err => this.handleDefaultError(err));
      this.sendGTM('change season');
    }
  }

  /**
   * Go to prev season
   */
  goToPrev(): void {
    // Check seasonIndex to valid value to avoid setting seasonIndex < 0(when user clicking goToPrev element too fast)
    if (this.seasonIndex - 1 >= 0) {
      this.showSpinner();
      --this.seasonIndex;
      this.createTabsForCurrentSeason();
      const season: IAllSeasons = this.seasons[this.seasonIndex];
      this.getCurrentSeason(season).subscribe(() => this.hideSpinner(), err => this.handleDefaultError(err));
      this.sendGTM('change season');
    }
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
    return this.result === null || !this.seasons.length;
  }
  /**
   * Get table title
   */
  getTableTitle(): string {
    return this.seasons && this.seasons[this.seasonIndex] && this.seasons[this.seasonIndex].name;
  }

  private createTabsForCurrentSeason(): void {
    const seasonCompetitionIds = this.seasons && this.seasons[this.seasonIndex] && this.seasons[this.seasonIndex].competitionIds,
      shownCompetitions = _.reject(this.competitions, (competition: IStatsCompetitions): boolean =>
        competition.hidden = (competition['type'] == 'parent' && seasonCompetitionIds.length>1) || !_.contains(seasonCompetitionIds, competition.id)),
      selectedCompetition = _.findWhere(shownCompetitions, { id: this.competitionId });
      
      this.showTabs = this.competitions.length > 1 &&  this.competitions.filter(ele=> ele.hidden === false).length > 1;

    if (selectedCompetition) {
      this.activeTab = selectedCompetition;
    } else {
      this.activeTab = shownCompetitions[0];
      this.competitionId = shownCompetitions[0] && shownCompetitions[0].id;
    }
  }

  private handleDefaultError(err) {
    this.hideSpinner();
    console.warn(err);
  }

  /**
   * send GTM tracking, when user click on eventName
   * @param {String} eventName - event name
   */
  private sendGTM(eventName: string): void {
    this.pubSubService.publish(this.pubSubService.API.PUSH_TO_GTM, ['trackEvent', {
      eventCategory: 'football',
      eventAction: 'league table',
      eventLabel: `${eventName}`
    }]);
  }

  /**
   * Get current season results
   * @param {Object} currentSeason
   * @private
   */
  private getCurrentSeason(currentSeason: IAllSeasons): Observable<any> {
    if (!this.competitionId) {
      this.result = null;
      return throwError('competitionId is undefined');
    }

    const currentSeasonYear = currentSeason && currentSeason.year;
    const params = {
      areaId: currentSeason && currentSeason.areaId,
      competitionId: this.competitionId,
      seasonId: currentSeason && currentSeason.id,
      sportId: currentSeason && currentSeason.sportId
    };

    this.competitionYear = currentSeasonYear && currentSeason.year.indexOf('/') === 2 ? `20${currentSeason.year}` : currentSeasonYear;

    return observableFrom(this.commandService.executeAsync(this.commandService.API.GET_RESULT_TABLES, [params], [])).pipe(
      map((results: IStatsResults[]) => {
        this.result = results[0];
        this.limitRows();
        return of(null);
      }), catchError((err) => {
        this.result = null;
        return throwError(err);
      }));
  }

}
