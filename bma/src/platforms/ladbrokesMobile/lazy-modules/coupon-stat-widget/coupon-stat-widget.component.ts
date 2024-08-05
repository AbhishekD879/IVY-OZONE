import { Component} from '@angular/core';
import { CouponStatWidgetComponent } from '@app/lazy-modules/coupon-stat-widget/components/coupon-stat-widget/coupon-stat-widget.component';

@Component({
  selector: 'coupon-stat-widget',
  templateUrl: './coupon-stat-widget.component.html',
  styleUrls: ['../../../../../src/app/lazy-modules/coupon-stat-widget/components/coupon-stat-widget/coupon-stat-widget.component.scss'
              ,'./coupon-stat-widget.component.scss']
})
export class LadbrokesMobileCouponStatWidgetComponent extends CouponStatWidgetComponent {
}
