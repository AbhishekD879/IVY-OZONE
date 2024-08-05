import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import * as _ from 'underscore';

import { FiltersService } from '@core/services/filters/filters.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { GtmService } from '@core/services/gtm/gtm.service';

import { JackpotReceiptPageService } from '@lazy-modules/jackpot/services/jackpot-receipt-page.service';
import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';

import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcome } from '@core/models/outcome.model';

@Component({
  selector: 'jackpot-receipt',
  styleUrls: [ 'jackpot-receipt.component.scss'],
  templateUrl: 'jackpot-receipt.component.html'
})
export class JackpotReceiptPageComponent implements OnInit {
  receiptData: ISportEvent[] = [];
  totalStake: number;
  totalLines: number;
  betReceiptNumber: string;

  constructor(
    private jackpotReceiptPageService: JackpotReceiptPageService,
    private sbFiltersService: SbFiltersService,
    private filtersService: FiltersService,
    private gtmService: GtmService,
    private localeService: LocaleService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.receiptData = this.jackpotReceiptPageService.getReceiptData;
    this.totalStake = this.jackpotReceiptPageService.getTotalStake;
    this.totalLines = this.jackpotReceiptPageService.getTotalLines;
    this.betReceiptNumber = this.jackpotReceiptPageService.getBetReceiptNumber;

    if ( this.receiptData && this.receiptData.length > 0) {
      // send data customer places a bet successfully
      this.gtmService.push('trackEvent', {
        eventCategory: 'betslip',
        eventAction: 'place bet',
        eventLabel: 'success',
        betID: this.betReceiptNumber
      });
    } else {
      this.goToPage();
    }
  }

  /**
   * Got to Jackpot page
   */
  goToPage(): void {
    this.router.navigate(['sport', 'football', 'jackpot']);
  }

  /**
   * Sort outcomes
   * @param {IOutcome[]} outcomes
   * @returns {IOutcome[]}
   */
  sortOutcomes(outcomes: IOutcome[]): IOutcome[] {
    return _.sortBy(outcomes, 'outcomeMeaningMinorCode');
  }

  /**
   * Set Currency
   * @param {number} value
   * @param {boolean} isToFixed
   */
  setCurrency(value: number, isToFixed: boolean = false): void {
    const val: number | string = isToFixed ? value.toFixed(2) : value;
    return this.filtersService.setCurrency(val, '£');
  }

  /**
   * Set Button Title
   * @param {string} text
   * @returns {string}
   */
  setButtonText(text: string): string {
    return this.localeService.getString(this.sbFiltersService.outcomeMinorCodeName(text) as string);
  }
}
