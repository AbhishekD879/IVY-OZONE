import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { equalPathMatcher } from '@core/services/routesMatcher/routes-matcher.service';
import { LoggedInGuard } from '@core/guards/logged-in-guard.service';
import { IncorrectPatternComponent } from './components/incorrectPattern/incorrect-pattern.component';
import { AddToBetslipComponent } from './components/addToBetslip/add-to-betslip.component';
import { VoucherComponent } from '@betslipModule/components/voucher/voucher.component';

const routes: Routes = [
  {
  matcher: equalPathMatcher,
  component: VoucherComponent,
  canActivate: [LoggedInGuard],
  data: {
    segment: 'voucherCode',
    path: 'voucher-code'
  }
}, {
  matcher: equalPathMatcher,
  component: AddToBetslipComponent,
  data: {
    segment: 'addToBetSlip',
    path: 'betslip/add/:outcomeId'
  }
}, {
  matcher: equalPathMatcher,
  component: IncorrectPatternComponent,
  data: {
    segment: 'betSlipUnavailable',
    path: 'betslip/unavailable'
  }
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
export class BetslipRoutingModule { }
