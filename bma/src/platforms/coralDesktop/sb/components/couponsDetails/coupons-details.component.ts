import { Component, ViewEncapsulation } from '@angular/core';
import { CouponsDetailsService } from '@app/sb/components/couponsDetails/coupons-details.service';

import { CouponsDetailsComponent as CoreCouponsDetailsComponent } from '@sb/components/couponsDetails/coupons-details.component';

@Component({
  // eslint-disable-next-line
  encapsulation : ViewEncapsulation.None,
  selector: 'coupons-details',
  templateUrl: './coupons-details.component.html',
  styleUrls: ['../../../../../app/sb/components/couponsDetails/coupons-details.component.scss'],
  providers: [CouponsDetailsService]
})
export class CouponsDetailsComponent extends CoreCouponsDetailsComponent {
  protected getStickyElementsHeight(): number {
    const headerElement = this.windowRefService.document.querySelector('header');
    return !headerElement ? 0 : this.domToolsService.getHeight(headerElement);
  }
}
