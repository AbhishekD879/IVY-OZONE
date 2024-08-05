import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MobileOddsBoostPageComponent } from './components/odds-boost-page/odds-boost-page.component';
import { equalPathMatcher } from '@core/services/routesMatcher/routes-matcher.service';
import { OddsBoostGuard } from '@core/guards/oddsboost-guard.service';
import { ODDS_BOOST_URL } from '@oddsBoost/constants/odds-boost.constant';

const routes: Routes = [
  {
    matcher: equalPathMatcher,
    component: MobileOddsBoostPageComponent,
    canActivate: [OddsBoostGuard],
    data: {
      segment: ODDS_BOOST_URL,
      path: ODDS_BOOST_URL,
    }
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class OddsBoostRoutingModule {}