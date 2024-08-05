import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';

import { InplayAllSportsPageComponent } from '@inplayModule/components/inplayAllSportsPage/inplay-all-sports-page.component';
import { InplaySingleSportPageComponent } from '@inplayModule/components/inplaySingleSportPage/inplay-single-sport-page.component';
import { InplayWatchLivePageComponent } from '@inplayModule/components/inplayWatchLivePage/inplay-watch-live-page.component';

import { InplayPageComponent } from '@inplayModule/components/inplayPage/inplay-page.component';

const routes: Routes = [{
  path: '',
  component: InplayPageComponent,
  data: {
    segment: 'inPlay'
  },
  children: [{
    path: '',
    component: InplaySingleSportPageComponent,
    data: {
      segment: 'inPlay.firstSport'
    }
  },
  {
    path: 'watchlive',
    component: InplayWatchLivePageComponent,
    data: {
      segment: 'inPlay.watchlive'
    }
  },
  {
    path: 'allsports',
    component: InplayAllSportsPageComponent,
    data: {
      segment: 'inPlay.allsports'
    }
  }, {
    path: ':sport',
    component: InplaySingleSportPageComponent,
    data: {
      segment: 'inPlay.sport'
    }
  }]
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class InPlayRoutingModule {}
