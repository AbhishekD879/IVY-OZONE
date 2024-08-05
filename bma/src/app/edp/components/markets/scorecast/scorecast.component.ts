import { Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import * as _ from 'underscore';

import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { BetslipSelectionsDataService } from '@core/services/betslipSelectionsData/betslip-selections-data';
import { PriceOddsButtonAnimationService } from '@shared/components/priceOddsButton/price-odds-button.animation.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ScorecastService } from './scorecast.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IScorecastMarket, IScoreCastMarkets, ITeam } from './scorecast.model';
import { IGroupedOutcome } from '@shared/models/scorecast.model';
import { IPrice } from '@core/models/price.model';
import { ITeams, ITeamsScores } from '@core/models/team.model';
import { LocaleService } from '@core/services/locale/locale.service';
import { IOutcome } from '@core/models/outcome.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { AbstractOutletComponent } from '@app/shared/components/abstractOutlet/abstract-outlet.component';
import { ScorecastDataService } from '@app/core/services/scorecastData/scorecast-data.service';

const TYPE = 'SCORECAST';

@Component({
  selector: 'scorecast',
  templateUrl: 'scorecast.component.html'
})
export class ScorecastComponent extends AbstractOutletComponent implements OnInit {
  @Input() eventEntity: ISportEvent;
  @Input() markets: IMarket[];
  @Input() memoryId: number | string;
  @Input() memoryLocation: string;
  @Input() isExpanded: boolean;

  @ViewChild('scoreH', { static: true }) scoreH: ElementRef;
  @ViewChild('scoreA', { static: true }) scoreA: ElementRef;

  scorecastMarkets: IScoreCastMarkets | any = {};
  selectedScorecastMarket: IScorecastMarket | any = {};
  selectedGoalscorerTeam: ITeam | any = {};
  selectedGoalscorerOutcome: IGroupedOutcome | any = {};
  selectedCorrectScoreOutcome: IGroupedOutcome | any = {};
  scorecastMarketsArray: { [key: string]: IScorecastMarket[]; } | any = {};
  cashoutAvail: boolean;
  teamsArray: ITeam[] = [];
  teams: ITeams | any = {};
  correctScore: IMarket;
  selectedGoalscorerTeamScorers: IOutcome[];
  cumulativeOdd: IPrice;
  cumulativeOddPriceToShow = {};
  goalscorerOutcomes: IOutcome[];
  scorecastScoresTeamH: number[];
  scorecastScoresTeamA: number[];
  scorecastKeys: string[];
  selectedScorecastTab: string;
  isDesktop: boolean;
  constructor(
    protected fracToDecFactory: FracToDecService,
    protected scorecastService: ScorecastService,
    protected betSlipSelectionsData: BetslipSelectionsDataService,
    protected priceOddsButtonService: PriceOddsButtonAnimationService,
    protected pubsubService: PubSubService,
    protected localeService: LocaleService,
    protected filterService: FiltersService,
    protected scorecastDataService: ScorecastDataService
    ) {
      super();
    }

  ngOnInit(): void {
    this.applyData();

    if (!this.selectedGoalscorerTeamScorers || !this.correctScore) {
      return;
    }

    this.goalscorerOutcomes = this.filterService.orderBy(_.filter(this.selectedGoalscorerTeamScorers,
      (value: IOutcome) => value.outcomeStatusCode !== 'S'), ['prices[0].priceDec', 'name']);
    this.scorecastScoresTeamH = this.getMaxValues().teamH;
    this.scorecastScoresTeamA = this.getMaxValues().teamA;
    this.scorecastKeys = Object.keys(this.scorecastMarkets);
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @return {number}
   */
  trackByIndex(index: number): number {
    return index;
  }

  /**
   * @param {number} index
   * @param {IOutcome} outcome
   * @returns {string}
   */
  trackById(index: number, outcome: IOutcome): string {
    return `${index}-${outcome.id}`;
  }

  getGoalscorerOutcomes(): IOutcome[] {
    return this.filterService.orderBy(_.filter(this.selectedGoalscorerTeamScorers, (value: IOutcome) => value.outcomeStatusCode !== 'S'),
      ['prices[0].priceDec', 'name']);
  }

  getSwitcherText(value: IScoreCastMarkets): string {
    return this.localeService.getString(`sb.${value.localeName}`);
  }

  /**
   * Get options for score select
   * @return {object} team scores
   */
  getMaxValues(): ITeamsScores {
    return this.scorecastService.getMaxScoreValues(this.correctScore.outcomes);
  }

  /**
   * select Scorecast Market
   * @param scorecastMarketName
   */
  selectScorecastMarket(scorecastMarketName: string): void {
    this.selectedScorecastTab = this.getSwitcherText(this.scorecastMarkets[scorecastMarketName])
    this.scorecastService.setGtmData(this.selectedScorecastTab);
    if (_.has(this.scorecastMarkets, scorecastMarketName)) {
      this.selectedScorecastMarket = this.scorecastMarkets[scorecastMarketName];
    }

    // selection default home team
    const teamEntity = _.find(this.teamsArray, (team: ITeam) => {
      const teamsGoalscorersLength = this.selectedScorecastMarket.teamsGoalscorers && this.selectedScorecastMarket.teamsGoalscorers[team.name].length;
      return team.outcomeMeaningMinorCode !== 2 && teamsGoalscorersLength;
    });

    this.selectGoalscorerTeam(teamEntity);

    if (this.correctScore) {
      this.resetSelectedScore();
    }
  }

  resetTeamsScores(): void {
    this.teams = {
      teamH: { name: this.teamsArray[0].name, score: this.getMaxValues().teamH[0] },
      teamA: { name: this.teamsArray[1].name, score: this.getMaxValues().teamA[0] }
    };
  }
  /**
   * selects Goalscorer Team
   * selects Goalscorer Team
   * @param teamEntity
   */
  selectGoalscorerTeam(teamEntity: ITeam): void {
    if (this.teamsArray.indexOf(teamEntity) !== -1) {
      this.selectedGoalscorerTeam = teamEntity;
      this.selectedGoalscorerTeamScorers = this.selectedScorecastMarket.teamsGoalscorers[teamEntity.name];
      this.goalscorerOutcomes = this.getGoalscorerOutcomes();
      this.selectedGoalscorerOutcome.outcome = this.goalscorerOutcomes[0];
    }

    this.buildCumulativeOdd();
  }

  /**
   * if no goalscorer outcome selected - select first not suspended
   */
  goalscorerChanged(outcomeName: string): void {
    this.selectedGoalscorerOutcome.outcome = _.find(this.selectedGoalscorerTeamScorers, (scorer: IOutcome) => scorer.name === outcomeName);
    if (!this.selectedGoalscorerOutcome.outcome) {
      this.selectedGoalscorerOutcome.outcome = _.find(this.selectedGoalscorerTeamScorers, (s: IOutcome) => s.outcomeStatusCode !== 'S');
    }

    this.buildCumulativeOdd();
  }

  /**
   * get correct outcome depending on selected score
   */
  selectCorrectScore(value?: string, team?: string): void {
    if (value && team) {
      this.teams[team].score = value;
    }

    this.selectedCorrectScoreOutcome.outcome =
      this.scorecastService.getCombinedOutcome(this.teams, this.correctScore.outcomes);
    this.buildCumulativeOdd();
  }

  /**
   * builds Cumulative Odd
   */
  buildCumulativeOdd(): void {
    if (this.isTwoOutcomesSelected()) {
      this.cumulativeOdd = this.scorecastService.getCombinedOutcomePrices(this.selectedScorecastMarket.scorecasts,
        this.selectedGoalscorerOutcome.outcome.id, this.selectedCorrectScoreOutcome.outcome.id);
      this.cumulativeOddPriceToShow = this.cumulativeOdd &&
        this.fracToDecFactory.getFormattedValue(this.cumulativeOdd.priceNum, this.cumulativeOdd.priceDen);
    } else {
      this.cumulativeOdd = this.cumulativeOddPriceToShow = null;
    }
  }

  /**
   * check if selection is added to betslip
   * @returns {Boolean}
   */
  isInBetslip(): boolean {
    if (!this.isTwoOutcomesSelected()) {
      return false;
    }
    const selectionIds = [this.selectedGoalscorerOutcome.outcome.id, this.selectedCorrectScoreOutcome.outcome.id];
    const qbSelectionIds = [this.selectedCorrectScoreOutcome.outcome.id, this.selectedGoalscorerOutcome.outcome.id];
    return this.betSlipSelectionsData.contains(selectionIds, qbSelectionIds);
  }

  /**
   * Add cumulative odd to betslip
   * @param {Object} event
   */
  addToMultiples(event: Event): void {
        const gtmData = {
      selectedScorecastTab: this.selectedScorecastTab.toLowerCase(),
      quantity: 1,
      name: `${this.teamsArray[0].name} vs ${this.teamsArray[1].name}`,
      teamname: this.selectedGoalscorerTeam.name.toLowerCase(),
      dimension60: this.eventEntity.id.toString(),
      dimension61: this.selectedGoalscorerOutcome.outcome.id.toString(),
      dimension62: this.eventEntity.eventIsLive ? 1 : 0,
      dimension64:this.eventEntity.categoryName.toLowerCase(),
      metric1: 0,
      playerName :this.selectedGoalscorerOutcome.outcome.alphabetName.toLowerCase(),
      result: `${this.teams['teamH'].score}-${this.teams['teamA'].score}`
    }
    this.scorecastService.setBetslipGtmData(gtmData);
    this.scorecastDataService.setScorecastData({
      eventLocation: 'scorecast',
      name: gtmData.name,
      teamname: gtmData.teamname,
      playerName : gtmData.playerName,
      result: gtmData.result,
      dimension60: this.eventEntity.id.toString(),
      dimension61: this.selectedGoalscorerOutcome.outcome.id.toString(),
      dimension62: this.eventEntity.eventIsLive ? 1 : 0,
      dimension64:this.eventEntity.categoryName.toLowerCase(),
    })
    const GTMObject = {
      categoryID: this.eventEntity && this.eventEntity.categoryId,
      typeID: this.eventEntity && this.eventEntity.typeId,
      eventID: this.eventEntity && this.eventEntity.id,
      selectionID: this.isTwoOutcomesSelected() &&
        `${this.selectedGoalscorerOutcome.outcome.id},${this.selectedCorrectScoreOutcome.outcome.id}`
    };

    this.priceOddsButtonService.animate(event).then(() => {
      const addToBetSlipObject = {
        type: TYPE,
        outcomes: [this.selectedGoalscorerOutcome.outcome,
        this.selectedCorrectScoreOutcome.outcome],
        price: this.cumulativeOdd,
        additional: {
          scorecastMarketId: _.has(this.selectedScorecastMarket, 'market') &&
            this.selectedScorecastMarket.market.id
        },
        GTMObject
      };

      this.pubsubService.publish(this.pubsubService.API.ADD_TO_BETSLIP_BY_SELECTION, addToBetSlipObject);
    });
  }

  /**
   * check if scorecast should be disabled
   * @returns {Boolean}
   */
  isScorecastDisabled(market: IScorecastMarket): boolean {
    return this.isEventSuspended || this.isScorecastMarketSuspended(market);
  }

  /**
   * Check if goalscorer and correct score outcomes are selected
   * @returns {Boolean}
   */
  protected isTwoOutcomesSelected(): boolean {
    return !!(this.selectedGoalscorerOutcome.outcome && this.selectedCorrectScoreOutcome.outcome);
  }

  /**
   * check if goalscorer should be disabled
   * @returns {Boolean}
   */
  get isGoalscorerDisabled(): boolean {
    return this.isEventSuspended || this.isScorecastMarketSuspended() || this.isGoalScorerMarketSuspended;
  }
  set isGoalscorerDisabled(value:boolean){}

  /**
   * check if score should be disabled
   * @returns {Boolean}
   */
  get isScoreDisabled(): boolean {
    return this.isEventSuspended || this.isScorecastMarketSuspended() ||
      this.isGoalScorerMarketSuspended || this.isCorrectScoreMarketSuspended;
  }
set isScoreDisabled(value:boolean){}
  /**
   * check if add to betslip button should be disabled
   * @returns {Boolean}
   */
  get isAddToBetslipDisabled(): boolean {
    return !this.cumulativeOdd || this.isEventSuspended || this.isScorecastMarketSuspended() ||
      this.isGoalScorerMarketSuspended || this.isCorrectScoreMarketSuspended || this.isCorrectScoreOutcomeSuspended;
  }
set isAddToBetslipDisabled(value:boolean){}
  private resetSelectedScore(): void {
    this.scoreH.nativeElement.options.selectedIndex = 0;
    this.scoreA.nativeElement.options.selectedIndex = 0;

    this.resetTeamsScores();
    this.selectCorrectScore();
  }

  /**
   * check if event is suspended
   * @returns {Boolean}
   */
  private get isEventSuspended(): boolean {
    return this.eventEntity.eventStatusCode === 'S';
  }
private set isEventSuspended(value:boolean){}
  /**
   * check if goalscorer market is suspended
   * @returns {Boolean}
   */
  private get isGoalScorerMarketSuspended(): boolean {
    return this.selectedScorecastMarket && this.selectedScorecastMarket.goalscorerMarket &&
      this.selectedScorecastMarket.goalscorerMarket.marketStatusCode === 'S';
  }
private set isGoalScorerMarketSuspended(value:boolean){}
  /**
   * check if correct score market is suspended
   * @returns {Boolean}
   */
  private get isCorrectScoreMarketSuspended(): boolean {
    return this.correctScore && this.correctScore.marketStatusCode === 'S';
  }
private set isCorrectScoreMarketSuspended(value:boolean){}
  /**
   * check if correct score outcome is suspended
   * @returns {Boolean}
   */
  private get isCorrectScoreOutcomeSuspended(): boolean {
    return this.selectedCorrectScoreOutcome &&
      this.selectedCorrectScoreOutcome.outcome &&
      this.selectedCorrectScoreOutcome.outcome.outcomeStatusCode === 'S';
  }
private set isCorrectScoreOutcomeSuspended(value:boolean){}
  /**
   * check if scorecast market is suspended
   * @returns {Boolean}
   */
  private isScorecastMarketSuspended(scorecastMarket = this.selectedScorecastMarket): boolean {
    return scorecastMarket && scorecastMarket.market && scorecastMarket.market.marketStatusCode === 'S';
  }

  /**
   * set initial data
   */
  private applyData(): void {
    let markets: IMarket[] = _.compact([
      this.scorecastService.getMarketByMarketNamePattern(this.markets, '^first\\sgoal\\s?scorecast$'),
      this.scorecastService.getMarketByMarketNamePattern(this.markets, '^last\\sgoal\\s?scorecast$')
    ]);

    if (!markets.length) {
      return;
    }

    this.cashoutAvail = this.scorecastService.isAnyCashoutAvailable(markets,
      [{ cashoutAvail: 'Y' }]);
    this.teamsArray = this.scorecastService.getTeams(this.markets);

    // sorting array as First Goal Scorecast must be first and then default
    markets = _.sortBy(markets, 'name');

    // building scorecastMarkets object with respective teams goalscorers
    _.each(markets, (scorecastMarket: IMarket) => {
      const namePrefix = scorecastMarket.name.split(' ')[0],
        goalscorerMarket = this.scorecastService.getMarketByMarketNamePattern(this.markets,
          `^${namePrefix}\\sgoal\\s?scorer$`);

      if (scorecastMarket.id && goalscorerMarket) {
        this.scorecastMarkets[scorecastMarket.name] = {
          name: scorecastMarket.name,
          localeName: scorecastMarket.name.replace(/\s/g, ''),
          scorecasts: scorecastMarket.outcomes,
          teamsGoalscorers: this.scorecastService.getMarketOutcomesByTeam(this.teamsArray, goalscorerMarket),
          market: scorecastMarket,
          goalscorerMarket
        };
      }
    });

    // selected scorer by default
    this.selectScorecastMarket(this.scorecastService.getDefaultScorecastMarketName(this.scorecastMarkets));

    // building correctScore object with respective
    this.correctScore = this.scorecastService.getMarketByMarketNamePattern(this.markets, '^Correct Score$');

    this.resetTeamsScores();
    this.selectCorrectScore();
  }
}
