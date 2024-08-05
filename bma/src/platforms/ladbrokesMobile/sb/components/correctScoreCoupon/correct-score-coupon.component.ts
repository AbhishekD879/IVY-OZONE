import { Component } from '@angular/core';
import {
  CorrectScoreCouponComponent as AppCorrectScoreCouponComponent
} from '@sb/components/correctScoreCoupon/correct-score-coupon.component';

@Component({
  selector: 'correct-score-coupon',
  templateUrl: 'correct-score-coupon.component.html',
  styleUrls: [
    '../../../../../app/sb/components/correctScoreCoupon/correct-score-coupon.component.scss',
    './correct-score-coupon.component.scss'
  ]
})
export class CorrectScoreCouponComponent extends AppCorrectScoreCouponComponent {}
