import { Component, Input, OnInit } from '@angular/core';
import * as _ from 'underscore';
import { OutcomeTemplateHelperService } from '@app/sb/services/outcomeTemplateHelper/outcome-template-helper.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { IOutcome } from '@core/models/outcome.model';
import { IMarket } from '@core/models/market.model';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { IKnockoutEvent, ICompetitionMatchResult } from '@app/bigCompetitions/services/bigCompetitions/big-competitions.model';


@Component({
  selector: 'knockouts-card',
  templateUrl: 'knockouts-card.component.html'
})
export class KnockoutsCardComponent implements OnInit {
  @Input() cardEvent: IKnockoutEvent;
  @Input() stage: number;

  waitingWinner: boolean = false;
  isFlagPresentHome: boolean = false;
  isFlagPresentAway: boolean = false;
  isOutcomeOnStage: boolean = false;
  homeWinner: boolean;
  awayWinner: boolean;
  isResulted: boolean;
  isFinal: boolean = false;
  winnerAwayFlagLabel: string;
  winnerHomeFlagLabel: string;
  startTime: string;
  marketsCount: number;
  EDPpath: string;
  outcomes: IOutcome[] = [];
  market: IMarket;
  score: string[];
  pen: string[];
  aet: number[];


  constructor(private outcomeTemplateHelperService: OutcomeTemplateHelperService,
              private routingHelperService: RoutingHelperService,
              private coreToolsService: CoreToolsService,
              private filterService: FiltersService) {
  }

  ngOnInit(): void {
    this.isFinal = this.cardEvent.abbreviation === 'F1';

    if (this.cardEvent.startTime) {
      this.startTime = this.filterDate(this.cardEvent.startTime);
    }
    if (_.has(this.cardEvent, 'obEvent')) {
      this.marketsCount = this.cardEvent.obEvent.marketsCount - 1;
      this.EDPpath = `/${this.routingHelperService.formEdpUrl(this.cardEvent.obEvent)}`;
      this.market = this.cardEvent.obEvent.markets[0];

      this.outcomes = this.market ? this.filterService.orderBy(this.market.outcomes, ['outcomeMeaningMinorCode']) : [];
      this.setCorrectedOutcomeMeaningMinorCode();
    }

    if (_.has(this.cardEvent.participants, 'HOME')) {
      this.isFlagPresentHome = _.has(this.cardEvent.participants.HOME, 'svgId');
      this.homeWinner = _.has(this.cardEvent.participants.HOME, 'isWinner');
    }

    if (_.has(this.cardEvent.participants, 'AWAY')) {
      this.isFlagPresentAway = _.has(this.cardEvent.participants.AWAY, 'svgId');
      this.awayWinner = _.has(this.cardEvent.participants.AWAY, 'isWinner');
    }

    this.isResulted = this.cardEvent.resulted;

    if (this.isResulted) {
      this.setScores(this.cardEvent.result);
    }

    this.isAnyOutcomesOnStage();
    this.setWaitingWinnerStatus();
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @param {outcome} IOutcome
   * @return {string}
   */
  trackById(index: number, outcome: IOutcome): string {
    return `${index}${outcome.id}`;
  }

  private setScores(result: ICompetitionMatchResult): void {
    this.score = result.score;

    if (result.pen) {
      this.score = result.pen ? result.aet : result.score;
      this.pen = result.pen;
    } else if (result.aet) {
      this.aet = [Number(result.aet[0]) - Number(result.score[0]), Number(result.aet[1]) - Number(result.score[1])];
    }
  }

  /**
   * Find if one of the events has outcomes to use proper CSS class
   * Stage always has two events
   */
  private isAnyOutcomesOnStage(): void {
    if (_.has(this.stage[0], 'obEvent') && _.has(this.stage[0].obEvent, 'markets')) {
      this.isOutcomeOnStage = this.stage[0].obEvent.markets[0].outcomes.length;
    } else if (_.has(this.stage[1], 'obEvent') && _.has(this.stage[1].obEvent, 'markets')) {
      this.isOutcomeOnStage = this.stage[1].obEvent.markets[0].outcomes.length;
    }
  }

  /**
   * Set values needed for waiting winner option
   */
  private setWaitingWinnerStatus(): void {
    const defaultTeamLabel = '?';

    if (!this.cardEvent.eventId) {
      if (this.cardEvent.awayTeamRemark) {
        this.waitingWinner = true;
        this.winnerAwayFlagLabel = this.cardEvent.awayTeam || defaultTeamLabel;
      }

      if (this.cardEvent.homeTeamRemark) {
        this.waitingWinner = true;
        this.winnerHomeFlagLabel = this.cardEvent.homeTeam || defaultTeamLabel;
      }
    }
  }

  private setCorrectedOutcomeMeaningMinorCode(): void {
    this.outcomeTemplateHelperService.setOutcomeMeaningMinorCode(this.cardEvent.obEvent.markets, this.cardEvent.obEvent);
  }


  /**
   * Set correct date format
   * @param {string} date
   * @return {string} filtered
   */
  private filterDate(date: string): string {
    const d: Date = new Date(date);
    const month: string = d.toLocaleString('en-us', {month: 'long'});
    const day: number = d.getDate();
    return `${day + this.coreToolsService.getDaySuffix(day)} ${month}`;
  }
}
