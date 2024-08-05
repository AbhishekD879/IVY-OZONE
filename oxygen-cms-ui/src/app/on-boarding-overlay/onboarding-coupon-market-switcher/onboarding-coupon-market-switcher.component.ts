import { Component, OnInit } from '@angular/core';
import * as _ from 'lodash';
import { onboarding_ms_widget } from '../onboarding-coupon-stat-widgets/on-boarding-overlay.constants';
import { OnboardingCouponStatWidgetComponent } from '../onboarding-coupon-stat-widgets/onboarding-coupon-stat-widgets.component';


@Component({
  selector: 'app-onboarding-coupon-market-switcher',
  templateUrl: '../onboarding-coupon-stat-widgets/onboarding-coupon-stat-widgets.component.html',
  styleUrls: ['../onboarding-coupon-stat-widgets/onboarding-coupon-stat-widgets.component.html']
})
export class OnboardingCouponMarketSwitcherComponent extends OnboardingCouponStatWidgetComponent
 implements OnInit {
  readonly ONBOARDING_STAT: {[key: string]: string} = onboarding_ms_widget;
  apiEndpoint = 'couponAndMarketSwitcherWidget';
  fieldOrItemName ='couponMarketSwitcherPage';
}
