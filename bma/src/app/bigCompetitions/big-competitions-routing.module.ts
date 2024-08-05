import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { BigCompetitionComponent } from '@app/bigCompetitions/components/bigCompetition/big-competition.component';
import { BigCompetitionTabsComponent } from '@app/bigCompetitions/components/bigCompetitionTabs/big-competition-tabs.component';

export const routes: Routes = [{
  path: '',
  data: {
    segment: 'bigCompetition'
  },
  children: [
    {
      path: ':name',
      component: BigCompetitionComponent,
      data: {
        segment: 'bigCompetition'
      },
      children: [
        {
          path: ':tab',
          component: BigCompetitionTabsComponent,
          data: {
            segment: 'bigCompetition.tab'
          }
        },
        {
          path: ':tab/:subTab',
          component: BigCompetitionTabsComponent,
          data: {
            segment: 'bigCompetition.subtab'
          }
        }
      ]
    }
  ]
}];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: []
})
export class BigCompetitionsRoutingModule { }
