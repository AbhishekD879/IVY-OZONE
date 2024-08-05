import { Component, Input, OnInit } from '@angular/core';
import * as _ from 'underscore';
import { ITeams, ITeamsScores } from '@core/models/team.model';
import { IMarket } from '@core/models/market.model';
import { CorrectScoreService } from './correct-score.service';
import { IOutcome } from '@core/models/outcome.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { FiltersService } from '@core/services/filters/filters.service';
@Component({
  selector: 'correct-score',
  templateUrl: 'correct-score.component.html',
})
export class CorrectScoreComponent implements OnInit {
  @Input() market: IMarket;
  @Input() eventEntity: ISportEvent;
  @Input() isExpanded: boolean;
  @Input() memoryId: number | string;
  @Input() memoryLocation: string;
  @Input() marketGroup: IMarket[];
  combinedOutcome: {outcome: IOutcome};
  allShown: boolean;
  filterValueType: string;
  teamsObg: {teams: ITeams};
  teamHScores: number[];
  teamAScores: number[];
  groupedOutcomes: IOutcome[][] = [];
  marketOutcomes: IOutcome[] = [];
  defaultOutcomes: IOutcome [][] = [];
  otherSingleSelection: IOutcome = null;
  scoreType: string = 'all';
  showDefault: boolean = true;
  private anyOtherMarkets: IOutcome[] = [];
  constructor(protected correctScoreService: CorrectScoreService, protected filterService: FiltersService) {}

  /**
   * Initial operations
   */
  ngOnInit(): void {
    this.filterValueType = 'main';
    this.allShown = false;
    this.marketOutcomes = this.getScoredOutcome(this.market.outcomes);
    this.teamsObg = { teams: this.correctScoreService.getTeams(this.marketGroup) };
    this.teamsObg.teams.teamH.score = this.getMaxValues().teamH[0];
    this.teamsObg.teams.teamA.score = this.getMaxValues().teamA[0];
    this.onScoreChange();
    this.teamHScores = this.getMaxValues().teamH;
    this.teamAScores = this.getMaxValues().teamA;
    const groupedOutcomeObj  = this.filterService.groupBy([ ...this.marketOutcomes, ...this.anyOtherMarkets],'outcomeMeaningMinorCode');
    for (const key in groupedOutcomeObj) {
      if(groupedOutcomeObj[key].length) {
       this.groupedOutcomes.push(groupedOutcomeObj[key]);
      }
    }
    this.getDefaultArray(this.groupedOutcomes);
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @return {number}
   */
  trackByIndex(index: number): number {
    return index;
  }

  filteredName(entity: IOutcome): string {
    return !entity.outcomeMeaningScores? entity.name: this.filterService.getScoreFromName(entity.name);
  }

  /**
   * Get options for score select
   * @return {object} team scores
   */
  getMaxValues(): ITeamsScores {
    return this.correctScoreService.getMaxScoreValues(this.marketOutcomes);
  }
  /**
   * Assign outcome, based on scores
   */
  onScoreChange(value?: number, team?: string): void {
    if (value && team) {
      this.teamsObg.teams[team].score = Number(value);
    }

    this.combinedOutcome = {
      outcome: this.correctScoreService.getCombinedOutcome(this.teamsObg.teams, this.marketOutcomes, this.eventEntity, this.market)
    };
  }

  public changeAccordionState(accordionState: boolean): void {
    this.isExpanded = accordionState;
  }
  /**
   * Toggle showing all outcomes or selects only
   */
  toggleShow(): void {
    if (this.filterValueType === 'all') {
      this.allShown = false;
      this.filterValueType = 'main';
      this.showDefault = true;
    } else {
      this.allShown = true;
      this.filterValueType = 'all';
      this.showDefault = false;
    }
  }

  /**
   * Check if bet button should be disabled
   * @returns {Boolean}
   */
  isButtonDisabled(): boolean {
    const outcome = this.combinedOutcome.outcome;
    return !(_.has(outcome, 'prices') && outcome.prices.length) ||
      outcome.outcomeStatusCode === 'S' || this.isMarketOrEventSuspended();
  }

  /**
   *  Check if show all button is enabled
   * @returns {Boolean}
   */
  isShowAllButton(): boolean {
    return this.groupedOutcomes?.length && (this.eventEntity.categoryId === '16' || this.eventEntity.categoryId === '22' ||
      (this.eventEntity.categoryId !== '16' && this.eventEntity.categoryId !== '22' && (this.groupedOutcomes[0]?.length > 4 || this.groupedOutcomes[1]?.length > 4 || this.groupedOutcomes[2]?.length > 4)))
  }

  /**
   * Check if event or market is suspended
   * @returns {Boolean}
   */
  isMarketOrEventSuspended(): boolean {
    return this.eventEntity.eventStatusCode === 'S' || this.market.marketStatusCode === 'S';
  }
  /**
   * outcomes with scores & any other markets
   * @returns IOutcome[]
   */
  private getScoredOutcome(outcomes:IOutcome[]):IOutcome[] {
    const filters: string[] = ['H', 'D', 'A'];
    const filteredOutcomes: IOutcome[] = [];
    outcomes.forEach((outcome: IOutcome) => {
      if (filters.includes(outcome.originalOutcomeMeaningMinorCode) && !outcome.outcomeMeaningScores) {
        this.anyOtherMarkets.push(outcome);
      } else if (outcome.originalOutcomeMeaningMinorCode === 'O' && !outcome.outcomeMeaningScores) {
        this.otherSingleSelection = outcome;
      } else {
        filteredOutcomes.push(outcome);
      }
    });
    return filteredOutcomes;
  }
  /**
   * Default array creation
   * @returns IOutcome[][]
   */
  private getDefaultArray(data: IOutcome[][]): void {
    for (let i = 0; i < data.length; i++) {
      this.defaultOutcomes.push(data[i].slice(0, 4));
    }
  }
}
