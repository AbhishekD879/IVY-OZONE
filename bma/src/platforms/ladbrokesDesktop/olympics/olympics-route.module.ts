import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

// Overridden app components
import { OlympicsPageComponent } from '@ladbrokesDesktop/olympics/components/olympicsPage/olympics-page.component';
import { SportMainComponent } from '@ladbrokesDesktop/sb/components/sportMain/sport-main.component';
import { DesktopSportMatchesPageComponent } from '@ladbrokesDesktop/sb/components/sportMatchesPage/sport-matches-page.component';
import { SportTabsPageComponent } from '@sbModule/components/SportTabsPage/sport-tabs-page.component';

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
      component: SportTabsPageComponent,
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
