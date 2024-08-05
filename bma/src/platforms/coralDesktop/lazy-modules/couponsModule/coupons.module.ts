import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { DesktopModule } from '@desktopModule/desktop.module';
import { CouponsListService } from '@sb/components/couponsList/coupons-list.service';
import { GoalscorerCouponComponent } from '@sb/components/goalscorerCoupon/goalscorer-coupon.component';
import { CouponsDetailsService } from '@sb/components/couponsDetails/coupons-details.service';
import { GoalscorerCouponService } from '@app/sb/components/goalscorerCoupon/goalscorer-coupon.service';
import { CouponsContentSportTabComponent } from '@app/sb/components/couponsContentSportTab/coupons-content-sport-tab.component';
import { CorrectScoreCouponService } from '@sb/components/correctScoreCoupon/correct-score-coupon.service';
import { CouponsListSportTabComponent } from '@app/sb/components/couponsListSportTab/coupons-list-sport-tab.component';
import { CouponsListComponent } from '@coralDesktop/sb/components/couponsList/coupons-list.component';
import { CouponsDetailsComponent } from '@coralDesktop/sb/components/couponsDetails/coupons-details.component';
import { CorrectScoreCouponComponent } from '@coralDesktop/sb/components/correctScoreCoupon/correct-score-coupon.component';

@NgModule({
    imports: [
        SharedModule,
        DesktopModule,
    ],
    exports: [
        // CouponsDetailsComponent,
        // CouponsListComponent,
        // GoalscorerCouponComponent,
        // CouponsContentSportTabComponent,
        // CouponsListSportTabComponent,
    ],
    declarations: [
        // CouponsListSportTabComponent,
        // CouponsContentSportTabComponent,
        // CorrectScoreCouponComponent,
        // CouponsDetailsComponent,
        // CouponsListComponent,
        // GoalscorerCouponComponent,
    ],
    providers: [
        CorrectScoreCouponService,
        CouponsDetailsService,
        GoalscorerCouponService,
        CouponsListService,
    ],
    schemas: [
        NO_ERRORS_SCHEMA
    ]
})
export class CouponsModule {
    static entry = { CouponsDetailsComponent,
        CorrectScoreCouponComponent,
        CouponsContentSportTabComponent,
        CouponsListSportTabComponent,
        CouponsListComponent,
        GoalscorerCouponComponent};
}
