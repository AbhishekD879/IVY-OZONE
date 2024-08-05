import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DesktopSportTabsPageComponent } from '@coralDesktop/sb/components/SportTabsPage/sport-tabs-page.component';

// Overridden app components
import { OlympicsPageComponent } from '@coralDesktop/olympics/components/olympicsPage/olympics-page.component';
import { SportMainComponent } from '@coralDesktop/sb/components/sportMain/sport-main.component';
import { DesktopSportMatchesPageComponent } from '@coralDesktop/sb/components/sportMatchesPage/sport-matches-page.component';

export const routes: Routes = [
  {
    path: 'olympics',
    component: OlympicsPageComponent,
    data: {
      segment: 'olympics'
    }
  },
  {
    path: 'olympics/:sport',
    component: SportMainComponent,
    data: {
      segment: 'olympicsSport'
    },
    children: [{
      path: '',
      pathMatch: 'full',
      redirectTo: 'matches/today'
    }, {
      path: 'matches',
      pathMatch: 'full',
      redirectTo: 'matches/today'
    }, {
      path: ':display',
      component: DesktopSportTabsPageComponent,
      data: {
        segment: 'olympicsSport.display'
      }
    }, {
      path: ':display/:tab',
      component: DesktopSportMatchesPageComponent,
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
