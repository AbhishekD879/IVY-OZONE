import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OddsBoostPageComponent } from '@oddsBoost/components/oddsBoostPage/odds-boost-page.component';
import { equalPathMatcher } from '@core/services/routesMatcher/routes-matcher.service';
import { OddsBoostGuard } from '@core/guards/oddsboost-guard.service';
import { SUPER_BOOST_URL } from '@oddsBoost/constants/odds-boost.constant';

const routes: Routes = [
  {
    matcher: equalPathMatcher,
    component: OddsBoostPageComponent,
    canActivate: [OddsBoostGuard],
    data: {
      segment: SUPER_BOOST_URL,
      path: SUPER_BOOST_URL,
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
