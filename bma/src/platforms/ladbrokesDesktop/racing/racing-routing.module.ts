import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';

import { RacingTabsMainComponent } from '@ladbrokesMobile/racing/components/racingTabsMain/racing-tabs-main.component';
import { DesktopRacingMainComponent } from './components/racingMain/racing-main.component';
import { BuildYourRaceCardPageComponent } from './components/buildYourRaceCardPage/build-your-race-card-page.component';
import { GreyhoundNextRacesTabGuard } from '@ladbrokesMobile/racing/guards/greyhound-next-races-tab-guard.service';
import { NextRacesTabGuard } from '@ladbrokesMobile/racing/guards/next-races-tab-guard.service';
import { GermanSupportGuard } from '@app/core/guards/german-support-guard.service';
import { LadbrokesRacingEventMainComponent } from '@ladbrokesMobile/racing/components/racingEventMain/racing-event-main.component';
import { ForecastTricastGuard } from '@racing/guards/forecast-tricast-guard.service';
import { CanDeactivateGuard } from '@core/guards/can-deactivate-guard.service';

export const routes: Routes = [
  {
    path: 'horse-racing',
    component: DesktopRacingMainComponent,
    canActivate: [GermanSupportGuard],
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
        path: ':display/next',
        loadChildren: () => import('@ladbrokesDesktop/lazy-modules/lazyNextRacesTab/lazyNextRacesTab.module')
        .then(m => m.LazyNextRacesTabModule),
        data: {
          segment: 'horseracing.nextRaces'
        },
        canActivate: [NextRacesTabGuard]
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
  },

  {
    path: 'greyhound-racing',
    canActivate: [GermanSupportGuard],
    component: DesktopRacingMainComponent,
    data: {
      segment: 'greyhound'
    },
    children: [{
      path: ':display/next',
      loadChildren: () => import('@ladbrokesDesktop/lazy-modules/lazyNextRacesTab/lazyNextRacesTab.module')
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
export class RacingRoutingModule {}
