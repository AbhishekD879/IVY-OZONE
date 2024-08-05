import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';

import { RacingTabsMainComponent } from '@racingModule/components/racingTabsMain/racing-tabs-main.component';
import { RacingMainComponent } from '@racingModule/components/racingMain/racing-main.component';
import { LadbrokesRacingEventMainComponent } from '@ladbrokesMobile/racing/components/racingEventMain/racing-event-main.component';
import { NextRacesTabGuard } from '@ladbrokesMobile/racing/guards/next-races-tab-guard.service';
import { ForecastTricastGuard } from '@racing/guards/forecast-tricast-guard.service';
import { CanDeactivateGuard } from '@core/guards/can-deactivate-guard.service';


const routes: Routes = [
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
        }
      },
      {
        path: ':display',
        component: RacingTabsMainComponent,
        data: {
          segment: 'horseracing.display'
        },
      },
      {
        path: ':display/next',
        loadChildren: () => import('@ladbrokesMobile/lazy-modules/lazyNextRacesTab/lazyNextRacesTab.module')
        .then(m => m.LazyNextRacesTabModule),
        data: {
          segment: 'horseracing.display'
        },
        canActivate: [NextRacesTabGuard]
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
        component: LadbrokesRacingEventMainComponent,
        canDeactivate: [CanDeactivateGuard],
        data: {
          segment: 'horseracing.eventMain'
        }
      },
      {
        path: ':className/:typeName/:eventName/:id/:market',
        component: LadbrokesRacingEventMainComponent,
        canDeactivate: [CanDeactivateGuard],
        data: {
          segment: 'horseracing.eventMain.market'
        },
        canActivate: [ForecastTricastGuard]
      },
      {
        path: ':className/:typeName/:eventName/:id/:market/:marketType',
        component: LadbrokesRacingEventMainComponent,
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
