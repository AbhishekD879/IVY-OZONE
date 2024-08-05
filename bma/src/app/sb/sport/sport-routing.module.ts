import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { SportMainComponent } from '@sbModule/components/sportMain/sport-main.component';
import { SportTabsPageComponent } from '@sb/components/sportTabsPage/sport-tabs-page.component';
import { GermanSupportSportTabGuard } from '@core/guards/german-support-sport-tab-guard.service';
import { SportMatchesPageComponent } from '@sb/components/sportMatchesPage/sport-matches-page.component';

const routes: Routes = [
  {
    path: ':sport',
    component: SportMainComponent,
    data: {
      segment: 'sport'
    },
    children: [{
      path: 'matches',
      component: SportMatchesPageComponent,
      data: {
        segment: 'sport.matches'
      }
    }, 
    {
      path: 'golf_matches',
      component: SportMatchesPageComponent,
      data: {
        segment: 'sport.golf_matches'
      }
    },
    {
      path: ':display',
      component: SportTabsPageComponent,
      canActivate: [GermanSupportSportTabGuard],
      data: {
        segment: 'sport.display'
      }
    }, {
      path: ':display/:tab',
      pathMatch: 'full',
      redirectTo: 'matches'
    }],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LazySportRoutingModule { }
