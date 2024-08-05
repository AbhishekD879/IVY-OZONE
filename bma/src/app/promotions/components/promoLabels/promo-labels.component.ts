import { ChangeDetectionStrategy, Component, Input, OnInit } from '@angular/core';
import * as _ from 'underscore';

import { PROMO_LABELS_CONFIG } from './promo-labels.constant';

import { ISportEvent } from '@core/models/sport-event.model';
import { IPromoLabelsConfig } from './promo-labels-config.model';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { STRATEGY_TYPES } from '@app/core/constants/strategy-types.constant';

@Component({
  selector: 'promo-labels',
  templateUrl: './promo-labels.component.html',
  styleUrls: ['./promo-labels.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PromoLabelsComponent implements OnInit {
  promoLabels: IPromoLabelsConfig[] = [];
  isPromoSignpostingEnabled: boolean = false;
  isQuickbet: boolean = false;
  changeStrategy = STRATEGY_TYPES.ON_PUSH;
  @Input() isBogEnabled: boolean;
  @Input() luckyDip: boolean;
  @Input() cashoutValue: string;
  @Input() accaInsurance: boolean;
  @Input() event: ISportEvent;
  @Input() marketId: string;
  @Input() mode: string;
  @Input() exclude?: string = '';
  @Input() origin:string;


  constructor(
    private cmsService: CmsService
  ) { }

  ngOnInit() {
    this.isQuickbet = this.mode && this.mode === 'quickbetslip';

    this.cmsService.getToggleStatus('PromoSignposting')
      .subscribe((toggleStatus: boolean) => {
        this.isPromoSignpostingEnabled = toggleStatus;

        if (this.isPromoSignpostingEnabled) {
          this.generatePromoLabels(PROMO_LABELS_CONFIG);
        }
      });
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
   * Is cashout available
   * cashoutValue can be 'Y' or number in string, for example '5.0'
   * @returns {boolean}
   */
  get isCashoutAvailable(): boolean {
    return this.cashoutValue === 'Y' || this.cashoutValue !== null && !isNaN(+this.cashoutValue);
  }
set isCashoutAvailable(value:boolean){}
  /**
   * Generate promo labels
   * @param config
   */
  private generatePromoLabels(config: IPromoLabelsConfig[]): void {
    const setFlags = [];

    if (this.event) {
      const correctMarket = this.marketId ? _.findWhere(this.event.markets, { 'id': this.marketId.toString() }) : null;

      _.each(config, (item: IPromoLabelsConfig) => {
        // Check market flags
        if (correctMarket &&
          correctMarket.drilldownTagNames &&
          correctMarket.drilldownTagNames.indexOf(item.marketFlag) !== -1 &&
          this.exclude.indexOf(item.marketFlag) === -1) {
          setFlags.push(item);
        }
      });
    }

    if (this.accaInsurance) {
      setFlags.push({ name: 'accaInsurance', id: '#acca-insurance' });
    }

    // Promo labels
    this.promoLabels = _.uniq(setFlags);
  }
}
