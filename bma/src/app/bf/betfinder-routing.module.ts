import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { BetFinderComponent } from '@app/bf/components/betFinder/bet-finder.component';
import { BetFinderResultComponent } from '@app/bf/components/betFinderResult/bet-finder-result.component';

export  const routes: Routes = [{
  path: '',
  component: BetFinderComponent,
  data: {
    segment: 'betFinder'
  }
}, {
  path: 'results',
  component: BetFinderResultComponent,
  data: {
    segment: 'betFinderResults'
  }
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
export class BetfinderRoutingModule { }
