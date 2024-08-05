import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@sharedModule/shared.module';
import { LadbrokesDesktopCouponStatWidgetComponent as CouponStatWidgetComponent  } from '@ladbrokesDesktop/lazy-modules/coupon-stat-widget/coupon-stat-widget.component';

@NgModule({
  declarations: [
    CouponStatWidgetComponent
  ],
  imports: [
    CommonModule,
    SharedModule
  ],
  exports:[],
  schemas:[NO_ERRORS_SCHEMA]
})
export class CouponStatWidgetModule {
  static entry=CouponStatWidgetComponent;
}
