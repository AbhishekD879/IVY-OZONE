import { Component, Input, OnInit, OnChanges, SimpleChanges } from '@angular/core';

import { ISportEvent } from '@core/models/sport-event.model';
import { TimeService } from '@core/services/time/time.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RendererService } from '@shared/services/renderer/renderer.service';

@Component({
  selector: 'live-scores',
  templateUrl: './live-scores.component.html',
  styleUrls: ['./live-scores.component.scss']
})
export class LiveScoresComponent implements OnInit, OnChanges {

  @Input() event: ISportEvent;
  // Goal animation input properties
  @Input() animatingComponentId: string;
  @Input() homeScore: string;
  @Input() awayScore: string;

  isFootball: boolean;
  animationDelay: number;
  animationClassesRemoval: number;
  constructor(
    private renderer: RendererService,
    private timeService: TimeService,
    private windowRef: WindowRefService,
  ) {
    this.animationDelay = this.timeService.animationDelay;
  }

  ngOnInit(): void {
    this.isFootball = this.event.categoryCode === 'FOOTBALL';
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (!this.isFootball) {
      return;
    }
    const homeScoreChanged = changes.homeScore && !changes.homeScore.firstChange,
      awayScoreChanged = changes.awayScore && !changes.awayScore.firstChange;

    // Run goal scored animation
    if (homeScoreChanged) {
      const newScores = [ +changes.homeScore.currentValue, +this.awayScore ],
        oldScores = [ +changes.homeScore.previousValue, +this.awayScore ];

      this.processFootballScoreChanged(newScores, oldScores);
    }

    // Run goal scored animation
    if (awayScoreChanged) {
      const newScores = [ +this.homeScore, +changes.awayScore.currentValue ],
        oldScores = [ +this.homeScore, +changes.awayScore.previousValue ];

      this.processFootballScoreChanged(newScores, oldScores);
    }

  }
  // Check currentPints for Adv value
  isAdvance(currentPoints: string | number): boolean {
    return currentPoints && isNaN(Number(currentPoints));
  }

  getScore(homeOrAway: string): string {
    const teamAlias = this.getTeamAlias(homeOrAway);
    return this.event.comments && this.event.comments.teams &&
      this.event.comments.teams[teamAlias] && this.event.comments.teams[teamAlias].score;
  }

  getGamesScore(homeOrAway: string): string | number {
    const teamAlias = this.getTeamAlias(homeOrAway);

    if (this.getSetScores()) {
      const allSetsScores = this.getSetScores() ? Object.values(this.getSetScores()) : [],
       lastSet = allSetsScores[this.runningSetIndex - 1],
       playerId = this.event.comments.teams[teamAlias].id;
      return lastSet[playerId];
    } else {
      return this.event.comments.teams[teamAlias].periodScore;
    }
  }

  currentPoints(homeOrAway: string): string | number {
    const teamAlias = this.getTeamAlias(homeOrAway);

    if (this.getSetScores()) {
      const playerId = this.event.comments.teams[teamAlias].id;
      return this.event.comments.runningGameScores[playerId];
    } else {
      return this.event.comments.teams[teamAlias].currentPoints;
    }
  }

  get runningSetIndex(): number {
    return this.event.comments && this.event.comments.runningSetIndex;
  }
  set runningSetIndex(value:number){}

  // Picking team alias depending on whether it is commentary data or no
  private getTeamAlias(homeOrAway: string): string {
    if (homeOrAway === 'home') {
      return this.getSetScores() ? 'player_1' : 'home';
    }
    return this.getSetScores() ? 'player_2' : 'away';
  }

  private getSetScores(): { [key: string]: number; }[] {
    return this.event.comments && this.event.comments.setsScores;
  }

  /**
   * Check score changing: goal or correction
   *
   * @params {[number, number]} newValue
   * @params {[number, number]} oldValue
   */
  private processFootballScoreChanged(newValue: number[], oldValue: number[]): void {
    const goalScored = newValue[0] > oldValue[0] || newValue[1] > oldValue[1];
    const goalCancelled = newValue[0] < oldValue[0] || newValue[1] < oldValue[1];

    if (goalScored) {
      this.scoreTextAnimation(true);
    } else if (goalCancelled) {
      this.scoreTextAnimation(false);
    }
  }

  /**
   * Goal/Correction animation
   *
   * @params {boolean} isGoal - true - goal / false Correction
   */
  private scoreTextAnimation(isGoal: boolean): void {
    const cardElement = document.querySelector(`.cashout-odds-card.id-${this.animatingComponentId}`);
    const cssClass = isGoal ? 'goal-change' : 'correction-change';
    this.renderer.renderer.addClass(cardElement, cssClass);

    // Classes should be removed 0.5s earlier in order to see animation of score digits change
    this.animationClassesRemoval = this.windowRef.nativeWindow.setTimeout(() => {
      this.renderer.renderer.removeClass(cardElement, cssClass);
    }, this.animationDelay - 500);
  }
}
