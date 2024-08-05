import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { OnboardingCouponMarketSwitcherComponent } from './onboarding-coupon-market-switcher/onboarding-coupon-market-switcher.component';
import { FirstBetOnBoardingOverlayComponent } from './first-bet-on-boarding-overlay/first-bet-on-boarding-overlay.component';
import { OnboardingCouponStatWidgetComponent } from './onboarding-coupon-stat-widgets/onboarding-coupon-stat-widgets.component';
import { OnboardingMystableComponent } from './onboarding-mystable/onboarding-mystable.component';


const contestRoutes: Routes = [

  {
    path: 'first-bet-placement',
    component: FirstBetOnBoardingOverlayComponent,
  },
  {
    path: 'onboarding-coupon-stat-widget',
    component: OnboardingCouponStatWidgetComponent,
  },
  {
    path: 'onboarding-coupon-market-switcher-widget',
    component: OnboardingCouponMarketSwitcherComponent,
  },
  {
    path: 'onboarding-mystable',
    component: OnboardingMystableComponent,
  }
];

@NgModule({
    imports: [
        RouterModule.forChild(contestRoutes)
    ],
    exports: [RouterModule]
})
export class OnBoardingOverlayRoutingModule {
}