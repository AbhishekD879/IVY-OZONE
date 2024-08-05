import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {
  DesktopMatchRewardsMainComponent
 } from '@coralDesktop/euro/components/matchRewardsMain/match-rewards-main.component';

export const routes: Routes = [
    {
      path: '',
      component: DesktopMatchRewardsMainComponent,
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
export class EuroRoutingModule { }
