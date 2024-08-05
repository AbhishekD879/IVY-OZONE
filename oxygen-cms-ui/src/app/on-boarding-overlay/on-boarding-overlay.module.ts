import {NgModule} from '@angular/core';
import {SharedModule} from '../shared/shared.module';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { OnBoardingOverlayRoutingModule } from './on-boarding-overlay-routing.module';
import { FirstBetOnBoardingOverlayComponent } from './first-bet-on-boarding-overlay/first-bet-on-boarding-overlay.component';
import { OnboardingCouponStatWidgetComponent } from './onboarding-coupon-stat-widgets/onboarding-coupon-stat-widgets.component';
import { OnboardingCouponMarketSwitcherComponent } from './onboarding-coupon-market-switcher/onboarding-coupon-market-switcher.component';
import { OnboardingMystableComponent } from './onboarding-mystable/onboarding-mystable.component';

@NgModule({
  imports: [
    SharedModule,
    FormsModule,
    ReactiveFormsModule,
    OnBoardingOverlayRoutingModule
  ],

  declarations: [
    FirstBetOnBoardingOverlayComponent,
    OnboardingCouponStatWidgetComponent,
    OnboardingCouponMarketSwitcherComponent,
    OnboardingMystableComponent
  ],
  exports:[]
})
export class OnBoardingOverlayModule {
}
