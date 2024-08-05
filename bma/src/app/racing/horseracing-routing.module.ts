import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';

import { RacingEventMainComponent } from '@racing/components/racingEventMain/racing-event-main.component';
import { RacingTabsMainComponent } from '@racing/components/racingTabsMain/racing-tabs-main.component';
import { RacingMainComponent } from '@racing/components/racingMain/racing-main.component';
import { ForecastTricastGuard } from '@racing/guards/forecast-tricast-guard.service';
import { CanDeactivateGuard } from '@core/guards/can-deactivate-guard.service';

export const routes: Routes = [
  {
    path: '',
    component: RacingMainComponent,
    data: {
      segment: 'horseracing'
    },
    children: [{
      path: '',
      component: RacingTabsMainComponent,
        data: {
          segment: 'horseracing.display'
        },
      },
      {
        path: ':display',
        component: RacingTabsMainComponent,
        data: {
          segment: 'horseracing.display'
        },
      },
      {
        path: ':display/:filter',
        component: RacingTabsMainComponent,
        data: {
          segment: 'horseracing.display'
        },
      },
      {
        path: ':className/:typeName/:eventName/:id',
        component: RacingEventMainComponent,
        canDeactivate: [CanDeactivateGuard],
        data: {
          segment: 'horseracing.eventMain'
        }
      },
      {
        path: ':className/:typeName/:eventName/:id/:market',
        component: RacingEventMainComponent,
        canDeactivate: [CanDeactivateGuard],
        data: {
          segment: 'horseracing.eventMain.market'
        },
        canActivate: [ForecastTricastGuard]
      },
      {
        path: ':className/:typeName/:eventName/:id/:market/:marketType',
        component: RacingEventMainComponent,
        canDeactivate: [CanDeactivateGuard],
        data: {
          segment: 'horseracing.eventMain.market.marketType'
        }
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HorseracingRoutingModule {}
