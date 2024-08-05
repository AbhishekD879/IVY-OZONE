import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { SportMainComponent } from '@sbModule/components/sportMain/sport-main.component';
import { OlympicsPageComponent } from '@olympicsModule/components/olympicsPage/olympics-page.component';
import { SportMatchesPageComponent } from '@sb/components/sportMatchesPage/sport-matches-page.component';
import { SportTabsPageComponent } from '@sb/components/sportTabsPage/sport-tabs-page.component';

export const routes: Routes = [
  {
    path: '',
    component: OlympicsPageComponent,
    data: {
      segment: 'olympics'
    }
  },
  {
    path: ':sport',
    component: SportMainComponent,
    data: {
      segment: 'olympicsSport'
    },
    children: [{
      path: ':display',
      component: SportTabsPageComponent,
      data: {
        segment: 'olympicsSport.display'
      }
    }, {
      path: ':display/:tab',
      component: SportMatchesPageComponent,
      data: {
        segment: 'olympicsSport.display.tab'
      }
    }],
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
export class OlympicsRoutingModule {}
