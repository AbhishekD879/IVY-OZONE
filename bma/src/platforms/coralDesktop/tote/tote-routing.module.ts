import { ToteEventPageComponent } from '@app/tote/components/toteEventPage/tote-event-page.component';
import { ToteTabsResultsComponent } from '@app/tote/components/toteTabsResults/tote-tabs-results.component';
import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { ToteSportComponent } from '@app/tote/components/toteSport/tote-sport.component';

// Overridden app components
import { DesktopTotePageComponent } from '@coralDesktop/tote/components/totePage/tote-page.component';
import { DesktopToteInfoComponent } from '@coralDesktop/tote/components/toteInfo/tote-info.component';
import { TOTE_CONFIG } from '@app/tote/tote.constant';

const defaultSportUrl = `${TOTE_CONFIG.DEFAULT_TOTE_SPORT}/${TOTE_CONFIG.filters[0]}`;

const routes: Routes = [
  {
    path: 'information',
    component: DesktopToteInfoComponent,
    data: {
      segment: 'toteInfo'
    }
  },
  {
    path: 'event/:id',
    component: ToteEventPageComponent,
    data: {
      segment: 'tote.event'
    }
  }, {
    path: '',
    component: DesktopTotePageComponent,
    data: {
      segment: 'tote'
    },
    children: [
      {
        path: '',
        redirectTo: defaultSportUrl,
        pathMatch: 'prefix',
      },
      {
        path: 'results',
        component: ToteTabsResultsComponent,
        data: {
          segment: 'results'
        }
      },
      {
        path: ':sport',
        component: ToteSportComponent,
        data: {
          segment: 'sport'
        }
      },
      {
        path: 'results/:filter',
        component: ToteTabsResultsComponent,
        data: {
          segment: 'results'
        }
      },
      {
        path: ':sport/:filter',
        component: ToteSportComponent,
        data: {
          segment: 'sport'
        }
      }
    ]
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ToteRoutingModule {}
