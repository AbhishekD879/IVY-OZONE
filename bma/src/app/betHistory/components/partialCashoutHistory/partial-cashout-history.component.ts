import { Component, Input, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import * as _ from 'underscore';

import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { TimeService } from '@core/services/time/time.service';

import { IBetTermsChange } from '@app/bpp/services/bppProviders/bpp-providers.model';

@Component({
  selector: 'partial-cashout-history',
  templateUrl: 'partial-cashout-history.component.html',
  styleUrls: ['./partial-cashout-history.component.scss']
})
export class PartialCashoutHistoryComponent implements OnInit, OnChanges {

  @Input() terms: IBetTermsChange[];
  @Input() currencySymbol: string;

  hasCashouts: boolean;
  remainingStake: number;
  totalCashedOut: string;
  totalCashOutStake: string;

  private readonly NOT_DISPLAY_HISTORY: string [] = ['ODDS_BOOST', 'ORIGINAL_VALUES', 'PRICE_TOLERANCE'];

  constructor(private timeFactory: TimeService,
              private toolsService: CoreToolsService) {
  }

  ngOnInit(): void {
    this.initialize();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.terms && changes.terms.currentValue) {
      this.initialize();
    }
  }

  get partialHistory(): IBetTermsChange[] {
    return _.filter(this.terms, (item: IBetTermsChange) => {
      return !!item.stake.value && Number(item.stake.value) > 0 && !this.NOT_DISPLAY_HISTORY.includes(item.reasonCode);
    });
  }
  set partialHistory(value:IBetTermsChange[]){}

  /**
   * Returns local date from string
   * @param date string
   * @return {*}
   */
  getDate(date: string): Date {
    return this.timeFactory.getLocalDateFromString(date);
  }

  trackByBetTermsChange(index: number, item: IBetTermsChange): string {
    return `${index}${item.date}${item.changeNo}${item.stake.value}`;
  }

  private initialize() {
    this.hasCashouts = this.checkIfHasPartialChashouts(this.terms);
    if (this.hasCashouts) {
      this.calcSummary();
    }
  }

  private checkIfHasPartialChashouts(terms: IBetTermsChange[]): boolean {
    return terms && _.some(terms, (term: IBetTermsChange) => term.reasonCode === 'PARTIAL_CASHOUT' && !!term.stake.value);
  }

  /**
   * in terms array
   * first element has reasonCode = "ORIGINAL_VALUES"
   * second optionally might have reasonCode = "ODDS_BOOST"
   * calculate total by reasonCode = PARTIAL_CASHOUT
   */
  private calcSummary(): void {
    this.remainingStake = _.last(this.terms).stake.value;

    _.each(this.terms, (item: IBetTermsChange, i: number, arr: IBetTermsChange[]) => {
      if (this.NOT_DISPLAY_HISTORY.includes(item.reasonCode)) {
        return;
      }
      item.stakeUsed = this.toolsService.roundTo((arr[i - 1].stake.value - item.stake.value), 2).toFixed(2);
    });

    this.totalCashedOut = this.getTotalByFieldName(this.terms, 'cashoutValue');
    this.totalCashOutStake = this.getTotalByFieldName(this.terms, 'stakeUsed');
  }

  private getTotalByFieldName(terms: IBetTermsChange[], fieldName: string): string {
    return terms.filter((term: IBetTermsChange) => {
      return !this.NOT_DISPLAY_HISTORY.includes(term.reasonCode);
    }).reduce((sum: number, current: IBetTermsChange) => {
      return this.toolsService.roundTo(sum + Number(current[fieldName]), 2);
    }, 0).toFixed(2);
  }
}
