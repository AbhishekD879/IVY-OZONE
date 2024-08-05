import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SportEventComponent } from '@sb/components/sportEvent/sport-event.component';
import { DesktopSportTabsPageComponent } from '@coralDesktop/sb/components/SportTabsPage/sport-tabs-page.component';
import {
  PrivateMarketsTermsAndConditionsComponent
} from '@app/sb/components/privateMarketsTab/private-markets-terms-and-conditions.component';

// Overridden app components
// eslint-disable-next-line max-len
import { DesktopSportMatchesPageComponent } from '@coralDesktop/sb/components/sportMatchesPage/sport-matches-page.component';
import { SportMainComponent } from '@coralDesktop/sb/components/sportMain/sport-main.component';
import { CanDeactivateGuard } from '@core/guards/can-deactivate-guard.service';
import { LoggedInGuard } from '@core/guards/logged-in-guard.service';

export const routes: Routes = [
  {
    path: 'sport/:sport',
    component: SportMainComponent,
    data: {
      segment: 'sport'
    },
    children: [{
      path: 'matches',
      pathMatch: 'full',
      redirectTo: 'matches/today'
    }, {
      path: 'golf_matches',
      pathMatch: 'full',
      redirectTo: 'golf_matches/allEvents'
    }, {
      path: 'playerbets',
      pathMatch: 'full',
      redirectTo: '/playerbets'
    }, {
      path: ':display',
      component: DesktopSportTabsPageComponent,
      data: {
        segment: 'sport.display'
      }
    }, {
      path: ':display/:tab',
      component: DesktopSportMatchesPageComponent,
      data: {
        segment: 'sport.matches.tab'
      }
    }],
  },
  {
    path: 'event/:sport',
    component: SportEventComponent,
  },
  {
    path: 'event/:sport/:className/:typeName/:eventName/:id',
    pathMatch: 'full',
    redirectTo: 'event/:sport/:className/:typeName/:eventName/:id/main-markets'
  },
  {
    path: 'event/:sport/:className/:typeName/:eventName/:id/:market',
    component: SportMainComponent,
    canDeactivate: [CanDeactivateGuard],
    data: {
      segment: 'eventMain'
    },
    children: [{
      path: ':pitch',
      component: SportMainComponent,
      data: {
        segment: 'eventMain'
      }
    },
    {
      path: ':pitch/:formation/:player1',
      component: SportMainComponent,
      data: {
        segment: 'eventMain'
      }
    },
    {
      path: ':pitch/:formation/:player1/:player2',
      component: SportMainComponent,
      data: {
        segment: 'eventMain'
      }
    },{
      path: ':pitch/:formation/:player1/:player2/:player3',
      component: SportMainComponent,
      data: {
        segment: 'eventMain'
      }
    },{
      path: ':pitch/:formation/:player1/:player2/:player3/:player4',
      component: SportMainComponent,
      data: {
        segment: 'eventMain'
      }
    },{
      path: ':pitch/:formation/:player1/:player2/:player3/:player4/:player5',
      component: SportMainComponent,
      data: {
        segment: 'eventMain'
      }
    }]
  },
  {
    path: 'event/:sport/:className/:typeName/:eventName/:id/:market/:live',
    component: SportMainComponent,
    data: {
      segment: 'eventMain'
    }
  },
  {
    path: 'competitions/:sport',
    pathMatch: 'full',
    redirectTo: '/sport/:sport/competitions'
  },
  {
    path: 'competitions/:sport/:className',
    pathMatch: 'full',
    redirectTo: '/sport/:sport/competitions'
  },

  // Coupons lazy loading
  {
    path: 'coupons',
    loadChildren: () => import('@lazy-modules/couponsPage/coupons-page.module').then(m => m.LazyCouponsPageModule)
  },
  {
    path: 'private-markets',
    children: [
      {
        path: 'terms-conditions',
        component: PrivateMarketsTermsAndConditionsComponent,
        data: {
          segment: 'privateMarketsTeamsAndConditions'
        }
      }]
  },
  {
    path: 'football-jackpot-receipt',
    canActivate: [LoggedInGuard],
    loadChildren: () => import('@lazy-modules-module/jackpot/jackpot.module').then(m => m.JackpotModule)
  },
  {
    path: 'event/:sport/:className/:typeName/:eventName/:id',
    pathMatch: 'full',
    redirectTo: 'event/:sport/:className/:typeName/:eventName/:id/all-markets'
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: []
})
export class SbRoutingModule { }
