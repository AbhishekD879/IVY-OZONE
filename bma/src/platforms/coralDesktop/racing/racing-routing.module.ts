import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';

import { RacingEventMainComponent } from '@racing/components/racingEventMain/racing-event-main.component';
import { RacingTabsMainComponent } from '@racing/components/racingTabsMain/racing-tabs-main.component';
import { DesktopRacingMainComponent } from '@coralDesktop/racing/components/racingMain/racing-main.component';
import { BuildYourRaceCardPageComponent } from '@coralDesktop/racing/components/buildYourRaceCardPage/build-your-race-card-page.component';
import { ForecastTricastGuard } from '@racing/guards/forecast-tricast-guard.service';
import { CanDeactivateGuard } from '@core/guards/can-deactivate-guard.service';

export const routes: Routes = [
  {
    path: 'horse-racing',
    component: DesktopRacingMainComponent,
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
        path: 'build-your-own-race-card/:ids',
        component: BuildYourRaceCardPageComponent,
        canDeactivate: [CanDeactivateGuard],
        data: {
          segment: 'horseracing.buildYourRaceCard'
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
  },

  {
    path: 'greyhound-racing',
    component: DesktopRacingMainComponent,
    data: {
      segment: 'greyhound'
    },
    children: [{
        path: '',
        component: RacingTabsMainComponent,
        data: {
          segment: 'greyhound.display'
        }
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
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [RouterModule]
})
export class RacingRoutingModule {}
