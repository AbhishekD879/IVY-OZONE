import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';

import { RacingTabsMainComponent } from '@racingModule/components/racingTabsMain/racing-tabs-main.component';
import { RacingMainComponent } from '@racingModule/components/racingMain/racing-main.component';
import { LadbrokesRacingEventMainComponent } from '@ladbrokesMobile/racing/components/racingEventMain/racing-event-main.component';
import { GreyhoundNextRacesTabGuard } from '@ladbrokesMobile/racing/guards/greyhound-next-races-tab-guard.service';
import { ForecastTricastGuard } from '@racing/guards/forecast-tricast-guard.service';

const routes: Routes = [
  {
    path: '',
    component: RacingMainComponent,
    data: {
      segment: 'greyhound'
    },
    children: [
      {
        path: ':display/next',
        loadChildren: () => import('@ladbrokesMobile/lazy-modules/lazyNextRacesTab/lazyNextRacesTab.module')
        .then(m => m.LazyNextRacesTabModule),
        data: {
          segment: 'greyhound.nextRaces'
        },
        canActivate: [GreyhoundNextRacesTabGuard]
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
        component: LadbrokesRacingEventMainComponent,
        data: {
          segment: 'greyhound.eventMain'
        }
      },
      {
        path: ':className/:typeName/:eventName/:id/:market',
        component: LadbrokesRacingEventMainComponent,
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
