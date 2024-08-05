import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';

import { ToteEventPageComponent } from './components/toteEventPage/tote-event-page.component';
import { ToteTabsResultsComponent } from './components/toteTabsResults/tote-tabs-results.component';
import { ToteInfoComponent } from './components/toteInfo/tote-info.component';
import { TotePageComponent } from './components/totePage/tote-page.component';
import { ToteSportComponent } from './components/toteSport/tote-sport.component';
import { TOTE_CONFIG } from '@app/tote/tote.constant';

const defaultSportUrl = `${TOTE_CONFIG.DEFAULT_TOTE_SPORT}/${TOTE_CONFIG.filters[0]}`,
  resultFilters = `results/${TOTE_CONFIG.resultFilters[0]}`;

const routes: Routes = [
  {
    path: 'information',
    component: ToteInfoComponent,
    data: {
      segment: 'toteInfo'
    }
  }, {
    path: 'event/:id',
    component: ToteEventPageComponent,
    data: {
      segment: 'tote.event'
    }
  }, {
    path: '',
    component: TotePageComponent,
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
        redirectTo: resultFilters,
        pathMatch: 'prefix',
      },
      {
        path: ':sport',
        redirectTo: defaultSportUrl,
        pathMatch: 'prefix',
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
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ToteRoutingModule {}
