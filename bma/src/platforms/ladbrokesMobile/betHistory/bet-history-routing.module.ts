import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { RetailFeatureGuard } from '@core/guards/retail-feature-guard.service';

import { equalPathMatcher } from '@core/services/routesMatcher/routes-matcher.service';
import { BetHistoryPageWrapperComponent } from '@app/betHistory/components/betHistoryPageWrapper/bet-history-page-wrapper.component';
import { InShopBetsPageWrapperComponent } from '@app/betHistory/components/inShopBetsPageWrapper/in-shop-bets-page-wrapper.component';
import { CashOutPageWrapperComponent } from '@app/betHistory/components/cashoutPageWrapper/cash-out-page-wrapper.component';
import { OpenBetsPageWrapperComponent } from '@app/betHistory/components/openBetsPageWrapper/open-bets-page-wrapper.component';
import { CashOutTabGuard } from '@core/guards/cashout-tab-guard.service';
import { IRetailConfig } from '@app/core/services/cms/models/system-config';
import { IRouteData } from '@app/core/models/route-data.model';
import { CanDeactivateGuard } from '@app/core/guards/can-deactivate-guard.service';

const routes: Routes = [{
  matcher: equalPathMatcher,
  component: CashOutPageWrapperComponent,
  canActivate: [CashOutTabGuard],
  canDeactivate: [CanDeactivateGuard],
  data: {
    segment: 'tabs.cashout',
    path: 'cashout'
  }
}, {
  matcher: equalPathMatcher,
  component: OpenBetsPageWrapperComponent,
  canDeactivate: [CanDeactivateGuard],
  data: {
    segment: 'tabs.openbets',
    path: 'open-bets'
  }
}, {
  matcher: equalPathMatcher,
  component: BetHistoryPageWrapperComponent,
  data: {
    segment: 'tabs.betHistory',
    path: 'bet-history'
  }
}, {
  matcher: equalPathMatcher,
  component: InShopBetsPageWrapperComponent,
  canActivate: [RetailFeatureGuard],
  data: {
    segment: 'tabs.inShopBets',
    path: 'in-shop-bets',
    feature: 'shopBetHistory'
   } as IRouteData<IRetailConfig>
}];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: []
})
export class BetHistoryRoutingModule {
}
