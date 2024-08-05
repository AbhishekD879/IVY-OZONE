import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import {
  PrivateMarketsTermsAndConditionsComponent
} from '@sb/components/privateMarketsTab/private-markets-terms-and-conditions.component';
import { LoggedInGuard } from '@core/guards/logged-in-guard.service';

export const routes: Routes = [
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
