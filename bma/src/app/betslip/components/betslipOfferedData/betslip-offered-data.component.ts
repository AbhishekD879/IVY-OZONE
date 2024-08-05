import { ChangeDetectionStrategy, Component, Input, OnInit } from '@angular/core';
import { IBetslipLeg } from '@betslip/models/betslip-bet-data.model';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';

@Component({
  selector: 'betslip-offered-data',
  templateUrl: './betslip-offered-data.component.html',
  styleUrls: ['./betslip-offered-data.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class BetslipOfferedDataComponent implements OnInit  {
  @Input() stake: string;
  @Input() price: string;
  @Input() returns: number | string;
  @Input() eachWay: boolean;
  @Input() currencySymbol: string;
  @Input() oldPrice: IBetslipLeg[];

  @Input() isSp: boolean;
  @Input() isStakeChanged: boolean;
  @Input() isOddsChanged: boolean;
  @Input() isTraderChangedLegType: boolean;
  @Input() isOddsTypeChanged?: boolean;

  @Input() multiplePriceChanged?: string[];

  oldPriceText: string;
  isPrevPriceSP: boolean;
  isPriceChanged: boolean = false;

  constructor(
    protected fracToDecService: FracToDecService
  ) {}

  ngOnInit(): void {
    if (this.isOddsChanged) {
      if (this.isSp) {
        this.oldPriceText = this.price;
      } else {
        if (this.isOddsTypeChanged) {
          this.isPrevPriceSP = true;
        } else {
          const num = this.oldPrice[0].price.priceNum,
                den = this.oldPrice[0].price.priceDen;
          this.oldPriceText = num && <string>this.fracToDecService.getFormattedValue(num, den);
        }
      }
    }
  }
}
