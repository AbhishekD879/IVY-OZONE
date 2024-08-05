import { Component  } from '@angular/core';

import { CouponsListComponent as AppCouponsListComponent  } from '@app/sb/components/couponsList/coupons-list.component';

@Component({
  selector: 'coupons-list',
  styleUrls: ['./coupons-list.component.scss'],
  templateUrl: './coupons-list.component.html'
})
export class CouponsListComponent extends AppCouponsListComponent {}
