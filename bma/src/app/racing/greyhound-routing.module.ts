import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';

import { RacingEventMainComponent } from '@racing/components/racingEventMain/racing-event-main.component';
import { RacingTabsMainComponent } from '@racing/components/racingTabsMain/racing-tabs-main.component';
import { RacingMainComponent } from '@racing/components/racingMain/racing-main.component';
import { ForecastTricastGuard } from '@racing/guards/forecast-tricast-guard.service';

const routes: Routes = [
  {
    path: '',
    component: RacingMainComponent,
    data: {
      segment: 'greyhound'
    },
    children: [{
      path: '',
      component: RacingTabsMainComponent,
        data: {
          segment: 'greyhound.display'
        },
      },
      {
        path: ':display',
        component: RacingTabsMainComponent,
        data: {
          segment: 'greyhound.display'
        },
      },
      {
        path: ':display/:filter',
        component: RacingTabsMainComponent,
        data: {
          segment: 'greyhound.display.filter'
        },
      },
      {
        path: ':className/:typeName/:eventName/:id',
        component: RacingEventMainComponent,
        data: {
          segment: 'greyhound.eventMain'
        }
      },
      {
        path: ':className/:typeName/:eventName/:id/:market',
        component: RacingEventMainComponent,
        data: {
          segment: 'greyhound.eventMain.market'
        },
        canActivate: [ForecastTricastGuard]
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class GreyhoundRacingRoutingModule {}
