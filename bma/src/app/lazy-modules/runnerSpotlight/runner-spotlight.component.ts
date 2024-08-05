import * as _ from 'underscore';
import { Component, Input, OnInit } from '@angular/core';
import { IOutcome } from '@core/models/outcome.model';
import { LocaleService } from '@core/services/locale/locale.service';
import { RacingPostService } from '@core/services/racing/racingPost/racing-post.service';

@Component({
  selector: 'runner-spotlight',
  templateUrl: './runner-spotlight.html'
})
export class RunnerSpotlightComponent implements OnInit {

  @Input() outcome: IOutcome;
  @Input() isUKorIRE: boolean;
  @Input() isGreyhoundEdp: boolean;

  details: string[] = ['officialRating', 'rprRating', 'age', 'weight'];
  noDetails: boolean;
  spotlightOverview: string;
  correctWeightValue: string;
  lastRunOverview: string;
  courseDistanceWinner: string[];

  constructor(
    protected locale: LocaleService,
    protected racingPostService: RacingPostService
  ) { }

  ngOnInit(): void {
    this.spotlightOverview = this.outcome.racingFormOutcome.overview;
    this.noDetails = _.every(this.details, detail => this.outcome.racingFormOutcome && !this.outcome.racingFormOutcome[detail]);
    this.correctWeightValue = this.correctWeight();
    this.lastRunOverview = this.racingPostService.getLastRunText(this.outcome.racingFormOutcome.form);
  }

  /**
   * correctWeight()
   * @returns {string}
   */
  correctWeight(): string {
    if (!this.outcome.racingFormOutcome.weight) {
      return '';
    }
    return this.getCorrectWeight();
  }

  /**
   * isOverview()
   * @returns {string}
   */
  isOverview(): boolean {
    return !!this.spotlightOverview;
  }

  /**
   * Return correct weight
   * @returns {string}
   */
  private getCorrectWeight(): string {
    const clearWeight = Number(this.outcome.racingFormOutcome.weight.replace(/\D+/g, '')),
    weightInStones = parseInt((clearWeight / 14).toString(), 10),
    totalWeight = weightInStones * 14,
    secondPart = clearWeight - totalWeight,
    tempStr: string = secondPart > 0 ? `-${secondPart}lb` : '';

   return `${weightInStones}st${tempStr}`;
  }

}
