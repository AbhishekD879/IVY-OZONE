import { Component, Input, OnInit } from '@angular/core';

import { ISportEvent } from '@core/models/sport-event.model';
import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { ScoreParserService } from '@core/services/scoreParser/score-parser.service';
import { ITypedScoreData } from '@core/services/scoreParser/models/score-data.model';

@Component({
  selector: 'inplay-score',
  templateUrl: 'inplay-score.component.html'
})
export class InplayScoreComponent implements OnInit {
  @Input() event: ISportEvent;

  isTennis: boolean;
  boxScore: ITypedScoreData;
  isHalfTime: boolean;
  isPenalties: boolean;

  constructor(
    private sportEventHelper: SportEventHelperService,
    private scoreParserService: ScoreParserService
  ) {
  }

  ngOnInit() {
    // Check this values only once while initialisation is done, then update when clock is provided
    this.isTennis = this.sportEventHelper.isTennis(this.event);
    this.onClockUpdate();

    if (this.isBoxScoreType && this.event.comments) {
      const teams = this.event.comments.teams;
      const originalName = `${teams.home.name} ${teams.home.score} v ${teams.away.name} ${teams.away.score}`;
      this.boxScore = this.scoreParserService.parseScores(originalName, 'BoxScore');
    }
  }

  trackByIndex(index): number {
    return index;
  }

  public onClockUpdate(): void {
    this.isHalfTime = this.sportEventHelper.isHalfTime(this.event);
    this.isPenalties = this.sportEventHelper.isPenalties(this.event);
  }

  /**
   * Returns tennis set scores
   * @returns {object}
   */
  get tennisScores(): { [key: string]: number }[] {
    return this.sportEventHelper.getTennisSetScores(this.event);
  }
  set tennisScores(value:{ [key: string]: number }[]){}

  /**
   * Get score for team
   * @param {String} teamType
   * @param {boolean} isPenalty
   * @return {number|string}
   */
  getOddsScore(teamType: string, isPenalty: boolean = false): number | string {
    return this.sportEventHelper.getOddsScore(this.event, teamType, isPenalty);
  }

  /**
   * Returns current points for team
   * @param teamType
   * @returns {number}
   */
  getCurrentPoints(teamType: string): number {
    return this.sportEventHelper.getEventCurrentPoints(this.event, teamType);
  }

  /** Returns whether is score type a BoxScore
   * @returns {boolean}
   */
  get isBoxScoreType(): boolean {
    return this.scoreParserService.getScoreType(this.event.categoryId) === 'BoxScore';
  }
  set isBoxScoreType(value:boolean){}

  /**
   * Check if odds scores are present
   * @returns {boolean}
   */
  isEventHasOddsScores(): boolean {
    return this.sportEventHelper.isEventHasOddsScores(this.event);
  }

  /**
   * Returns tennis score for player
   * @param playerType
   * @returns {string}
   */
  getTennisScoreForPlayer(playerType: string): string {
    return this.sportEventHelper.getTennisScoreForPlayer(this.event, playerType);
  }

  /**
   * Check if event has current points
   * @returns {boolean}
   */
  isEventHasCurrentPoints(): boolean {
    return this.sportEventHelper.isEventHasCurrentPoints(this.event);
  }

  /**
   * Check if event is live
   * @returns {boolean}
   */
  isLive(): boolean {
    return this.sportEventHelper.isLive(this.event);
  }

  /**
   * Check if event has clock allowed;
   * @returns {boolean}
   */
  isClockAllowed(): boolean {
    return !!this.event.initClock;
  }

  /**
   * Build string of set number
   * @returns {string}
   */
  getTennisSetIndex(): string {
    return this.sportEventHelper.getTennisSetIndex(this.event);
  }
}
