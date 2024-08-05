import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { LadbrokesMobileBetFinderComponent } from '@ladbrokesMobile/bf/components/betFinder/bet-finder.component';
import { LadbrokesMobileBetFinderResultComponent } from '@ladbrokesMobile/bf/components/betFinderResult/bet-finder-result.component';

const routes: Routes = [{
  path: '',
  component: LadbrokesMobileBetFinderComponent,
  data: {
    segment: 'betFinder'
  }
}, {
  path: 'results',
  component: LadbrokesMobileBetFinderResultComponent,
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
