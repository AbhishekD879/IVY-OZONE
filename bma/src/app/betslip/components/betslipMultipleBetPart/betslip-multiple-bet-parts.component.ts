import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { IBetslipLeg } from '@betslip/models/betslip-bet-data.model';
import { UserService } from '@core/services/user/user.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { IPrice } from '@core/models/price.model';

@Component({
  selector: 'betslip-multiple-bet-parts',
  templateUrl: './betslip-multiple-bet-parts.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class BetslipMultipleBetPartsComponent {
  @Input() oldLegs: IBetslipLeg[];

  constructor(
    private userService: UserService,
    private fracToDecService: FracToDecService
  ) {}

  trackByIndex(index: number): number {
    return index;
  }

  /**
   * Returns changed odds in correct format
   * @param price {IPrice}
   * @return {string}
   */
  formatOdds(price: IPrice): string {
    if (!price) {
      return '';
    }

    if (price.priceType === 'SP') {
      return price.priceType;
    }

    return this.userService.oddsFormat === 'frac'
      ? (`${price.priceNum}/${price.priceDen}`)
      : (Number(this.fracToDecService.getDecimal(price.priceNum, price.priceDen))).toFixed(2);
  }
}
