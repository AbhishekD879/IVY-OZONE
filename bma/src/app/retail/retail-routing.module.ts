import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { equalPathMatcher } from '@core/services/routesMatcher/routes-matcher.service';
import { RetailPageComponent } from '@platform/retail/components/retailPage/retail-page.component';
import { ShopLocatorComponent } from '@app/retail/components/shopLocator/shop-locator.component';
import { BetTrackerComponent } from '@app/retail/components/betTracker/bet-tracker.component';
import { BetFilterComponent } from '@platform/retail/components/betFilter/bet-filter.component';
import { RetailFeatureGuard } from '@core/guards/retail-feature-guard.service';
import { IRetailConfig } from '@app/core/services/cms/models/system-config';
import { IRouteData } from '@app/core/models/route-data.model';

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

export class RetailRoutingModule { } // TODO: move to coral
