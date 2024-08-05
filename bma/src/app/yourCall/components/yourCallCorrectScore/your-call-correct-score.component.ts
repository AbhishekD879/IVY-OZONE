import { IYourcallSelection } from './../../models/selection.model';
import { Component, OnChanges, Input, OnInit } from '@angular/core';
import * as _ from 'underscore';

import { YourcallMarketsService } from '../../services/yourCallMarketsService/yourcall-markets.service';
import { YourCallMarketGroupItem } from '@yourcall/models/markets/yourcall-market-group-item';
import { IYourcallBYBEventResponse } from '@yourcall/models/byb-events-response.model';
import { YourcallDashboardService } from '../../services/yourcallDashboard/yourcall-dashboard.service';
import environment from '@environment/oxygenEnvConfig';

@Component({
  selector: 'yourcall-correct-score',
  templateUrl: './your-call-correct-score.component.html',
  styleUrls: ['./your-call-correct-score.component.scss']
})
export class YourCallCorrectScoreComponent implements OnChanges, OnInit {

  @Input() market: YourCallMarketGroupItem;
  @Input() game: IYourcallBYBEventResponse;

  groupedMarkets: IYourcallSelection[][];
  filterValueType: string;
  allShown: boolean;
  selectedValueHome: number;
  selectedValueAway: number;
  scoreHome: string[];
  scoreAway: string[];
  betButtonText: string = 'ADD TO BET BUILDER';
  currentSelection: any;
  isCoral: boolean;

  constructor(
    private yourCallMarketsService: YourcallMarketsService,
    private yourcallDashboardService: YourcallDashboardService
  ) { }

  ngOnInit(): void {
    this.isCoral = environment && environment.brand === 'bma';
    this.yourCallMarketsService.betPlacedStatus$.subscribe(selection => {
      if (selection) {
        this.resetDropdown();
        this.betButtonText = 'ADD TO BET BUILDER';
      }
    });
  }
  ngOnChanges(): void {
    // set default values
    this.groupMarkets();
    this.getSelectionValues('scoreHome', 'bettingValue1', 0, 'selectedValueHome');
    this.getSelectionValues('scoreAway', 'bettingValue2', 2, 'selectedValueAway');
    this.betButtonText = this.getSelectedSlectionVal() ? 'ADDED' : 'ADD TO BET BUILDER';
    this.onScoreChange();
    if (this.yourCallMarketsService.isRestoredNeeded(this.market.key)) {
      this.yourCallMarketsService.restoreBet(this.market);
    }
  }

  /**
   * Toggle showing all outcomes or selects only
   */
  toggleShow(): void {
    if (this.filterValueType === 'all') {
      this.allShown = false;
      this.filterValueType = 'main';
    } else {
      this.allShown = true;
      this.filterValueType = 'all';
    }
  }

  /**
   * Group Markets , filter out Ininity value
   * @private
   */
  groupMarkets(): void {
    // this.currentSelection = null;
    this.yourCallMarketsService.betRemovalsubject$.subscribe(selection => {
      if(this.yourCallMarketsService.selectedSelectionsSet.has(selection)) {
        this.yourCallMarketsService.selectedSelectionsSet.delete(selection);
      }
      if(this.currentSelection.id === selection) {
        this.betButtonText = this.getSelectedSlectionVal() ? 'ADDED' : 'ADD TO BET BUILDER' ;
      }
    });
    const data = _.groupBy(_.reject((this.market.selections as IYourcallSelection[]), (sel: IYourcallSelection) => {
      return sel.odds === 'Infinity';
    }), 'relatedTeamType');
    this.groupedMarkets = [data[1], data[0], data[2]];
    this.betButtonText = this.getSelectedSlectionVal() ? 'ADDED' : 'ADD TO BET BUILDER' ;
  }

  /**
   * Get possible scores for the match
   * @param item
   * @returns {string}
   */
  getScores(item: IYourcallSelection): string {
    return (item.relatedTeamType === 1) ? `${Math.floor(Number(item.bettingValue1))} - ${Math.floor(Number(item.bettingValue2))}`
      : `${Math.floor(Number(item.bettingValue2))} - ${Math.floor(Number(item.bettingValue1))}`;
  }

  /**
   * Action performed on button click
   * @param value {object}
   */
  selectValue(value: IYourcallSelection): void {
    this.yourCallMarketsService.selectValue(this.market, value);
  }

  /**
   * Check if value is selected
   * @param value {object}
   * @returns {boolean}
   */
  isSelected(value: IYourcallSelection): boolean {
    return this.yourCallMarketsService.isSelected(this.market, value);
  }

  /**
   * React on score change
   */
  onScoreChange(): void {
    this.getSelectedObj() || this.checkForNull();
  }

  /**
   * Add selection to dashboard
   */
  addToDashboard(): void {
    const selected = this.getSelectedObj() || this.checkForNull();

    if (selected) {
      this.selectValue(selected);
      if(this.yourCallMarketsService.selectedSelectionsSet.has(selected.id)) {
        this.yourCallMarketsService.selectedSelectionsSet.delete(selected.id);
      } else {
        this.yourCallMarketsService.selectedSelectionsSet.add(selected.id);
      }
    } else {
      this.resetDropdown();
    }

    this.updateSelectionSet();
    this.betButtonText = this.getSelectedSlectionVal() ? 'ADDED' : 'ADD TO BET BUILDER' ;
  }

  /**
   * update Set
   */
  updateSelectionSet(): void {
    this.yourCallMarketsService.selectedSelectionsSet = new Set();
    this.yourcallDashboardService.items.forEach(combinationSelection => {
      this.yourCallMarketsService.selectedSelectionsSet.add(combinationSelection.selection?.id);
    });
  }

  trackByMarket(index: number, market: IYourcallSelection[]): string {
    return `${index}${market.map((s: IYourcallSelection) => `${s.odds}${s.id}${s.title}`).join('-')}`;
  }

  trackBySelection(index: number, market: IYourcallSelection): string {
    return `${index}${market.title}${market.id}${market.displayOrder}`;
  }

  rotateA(currState: number) {
    this.selectedValueAway += currState;
    this.selectedValueAway = this.selectedValueAway % (this.scoreAway.length);
    if (this.selectedValueAway < 0) {
      this.selectedValueAway += this.scoreAway.length;
    }
    this.onScoreChange();
    this.betButtonText = this.getSelectedSlectionVal() ? 'ADDED' : 'ADD TO BET BUILDER' ;
  }

  rotateH(currState: number) {
    this.selectedValueHome += currState;
    this.selectedValueHome = this.selectedValueHome % (this.scoreHome.length);
    if (this.selectedValueHome < 0) {
      this.selectedValueHome += this.scoreHome.length;
    }
    this.onScoreChange();
    this.betButtonText = this.getSelectedSlectionVal() ? 'ADDED' : 'ADD TO BET BUILDER' ;
  }

  public getSelectedSlectionVal(): boolean {
    let isSelectionAvail = false;
    this.currentSelection = null;
    _.find((this.market.selections as IYourcallSelection[]), (el: IYourcallSelection) => {
     if(((Number(el.bettingValue1) === Number(this.selectedValueHome)) &&
        (Number(el.bettingValue2) === Number(this.selectedValueAway)))) {
          this.currentSelection = el;
          isSelectionAvail = true;
          // return this.yourCallMarketsService.selectedSelectionsSet.has(el.id) ? true : false;
        }
    });
    if(!this.selectedValueHome && !this.selectedValueAway && !isSelectionAvail) {
      const el =_.findWhere((this.market.selections as IYourcallSelection[]), { bettingValue2: null });
      if(el) {
        this.currentSelection = el;
      }
    }
    return this.yourCallMarketsService.selectedSelectionsSet.has(this.currentSelection?.id) ? true : false;
  }
  /**
   * Set dropdowns to default values
   * @private
   */
  private resetDropdown(): void {
    this.selectedValueHome = 0;
    this.selectedValueAway = 0;
  }

  /**
   * Find selection
   * @private
   */
  private getSelectedObj(): IYourcallSelection {
    return _.find((this.market.selections as IYourcallSelection[]), (el: IYourcallSelection) => {
      return (Number(el.bettingValue1) === Number(this.selectedValueHome)) &&
        (Number(el.bettingValue2) === Number(this.selectedValueAway));
    });
  }

  /**
   * Null is returned for 90min period in case of Draw 0-0
   * @returns {object|undefined}
   * @private
   */
  private checkForNull(): IYourcallSelection {
    return (!this.selectedValueHome && !this.selectedValueAway)
      ? _.findWhere((this.market.selections as IYourcallSelection[]), { bettingValue2: null }) : undefined;
  }

  /**
   * Get values for team for selections
   * @param team
   * @param type
   * @param index
   * @private
   */
  private getSelectionValues(team: string, type: string, index: number, selectedValue: string) {
    this[team] = _.sortBy(_.uniq(_.map(_.pluck(this.groupedMarkets[index], type), Number)));
    this[team].unshift(0);

    this[selectedValue] = this[team][0];
  }
}
