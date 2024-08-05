import { Component, Input } from '@angular/core';
import { IFreebetToken, IOffer } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { BetPackModel } from '@app/betpackReview/components/betpack-review.model';
@Component({
  selector: 'betpack-content-page',
  templateUrl: './betpack-content-page.component.html',
  styleUrls: ['./betpack-content-page.component.scss']

})
export class BetpackContentPageComponent {

  @Input() filteredBetPack: BetPackModel[];
  @Input() isMaxPurchaseLimitOver: boolean;
  @Input() getLimitsData: number;
  @Input() getFreeBets: IFreebetToken[];
  @Input() filteredBetPackEnable: Map<string, boolean>;
  @Input() accLimitFreeBets: IOffer[];
  constructor() { }
}