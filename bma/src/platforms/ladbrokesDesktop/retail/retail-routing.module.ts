import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { equalPathMatcher } from '@core/services/routesMatcher/routes-matcher.service';
import { BetFilterComponent } from '@ladbrokesMobile/retail/components/betFilter/bet-filter.component';
import { RetailFeatureGuard } from '@core/guards/retail-feature-guard.service';
import { IRetailConfig } from '@app/core/services/cms/models/system-config';
import { IRouteData } from '@app/core/models/route-data.model';
import { RetailPageComponent } from '@ladbrokesDesktop/retail/components/retailPage/retail-page.component';
import { BetTrackerComponent } from '@retail/components/betTracker/bet-tracker.component';
import { ShopLocatorComponent } from '@retail/components/shopLocator/shop-locator.component';
import { ILadbrokesRetailConfig } from '@ladbrokesMobile/core/services/cms/models/system-config';
import { DigitalCouponsComponent } from '@ladbrokesMobile/retail/components/digitalCoupons/digital-coupons.component';
import { SavedBetCodesComponent } from '@ladbrokesMobile/retail/components/savedBetCodes/saved-betcodes.component';

const routes: Routes = [
  {
    matcher: equalPathMatcher,
    component: RetailPageComponent,
    data: {
      segment: 'retailMain',
      path: 'retail',
      feature: 'upgrade'
    } as IRouteData<IRetailConfig>
  },
  {
    matcher: equalPathMatcher,
    component: BetFilterComponent,
    canActivate: [RetailFeatureGuard],
    data: {
      segment: 'betFilter',
      path: 'bet-filter',
      feature: 'footballFilter'
    } as IRouteData<IRetailConfig>
  },
  {
    matcher: equalPathMatcher,
    component: BetFilterComponent,
    canActivate: [RetailFeatureGuard],
    data: {
      segment: 'betFilter',
      path: 'bet-filter/:child',
      feature: 'footballFilter'
    } as IRouteData<IRetailConfig>
  },
  {
    matcher: equalPathMatcher,
    component: BetFilterComponent,
    canActivate: [RetailFeatureGuard],
    data: {
      segment: 'betFilter',
      path: 'bet-filter/:child/:child',
      feature: 'footballFilter'
    } as IRouteData<IRetailConfig>
  },
  {
    matcher: equalPathMatcher,
    component: BetTrackerComponent,
    canActivate: [RetailFeatureGuard],
    data: {
      segment: 'betTracker',
      path: 'bet-tracker',
      feature: 'shopBetTracker'
    } as IRouteData<IRetailConfig>
  },
  {
    matcher: equalPathMatcher,
    component: ShopLocatorComponent,
    canActivate: [RetailFeatureGuard],
    data: {
      segment: 'shopLocator',
      path: 'shop-locator',
      feature: 'shopLocator'
    } as IRouteData<IRetailConfig>
  },
  {
    matcher: equalPathMatcher,
    component: DigitalCouponsComponent,
    canActivate: [RetailFeatureGuard],
    data: {
      segment: 'coupons',
      path: 'digital-coupons',
      feature: 'digitalCoupons'
    } as IRouteData<ILadbrokesRetailConfig>
  },
  {
    matcher: equalPathMatcher,
    component: SavedBetCodesComponent,
    canActivate: [RetailFeatureGuard],
    data: {
      segment: 'savedBetCodes',
      path: 'saved-betcodes',
      feature: 'savedBetCodes'
    } as IRouteData<ILadbrokesRetailConfig>
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: []
})
export class RetailRoutingModule {
}
