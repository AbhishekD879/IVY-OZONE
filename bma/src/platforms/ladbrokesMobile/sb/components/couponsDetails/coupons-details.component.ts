import { Component, ViewEncapsulation } from '@angular/core';

import { CouponsDetailsComponent as CoralCouponsDetailsComponent } from '@sb/components/couponsDetails/coupons-details.component';

@Component({
  // eslint-disable-next-line
  encapsulation : ViewEncapsulation.None,
  selector: 'coupons-details',
  templateUrl: './coupons-details.component.html',
  styleUrls: ['../../../../../app/sb/components/couponsDetails/coupons-details.component.scss']
})
export class CouponsDetailsComponent extends CoralCouponsDetailsComponent {}
