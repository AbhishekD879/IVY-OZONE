import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DesktopBetFinderComponent } from '@coralDesktop/bf/components/betFinder/bet-finder.component';
import { DesktopBetFinderResultComponent } from '@coralDesktop/bf/components/betFinderResults/bet-finder-result.component';

export const routes: Routes = [{
  path: 'bet-finder',
  component: DesktopBetFinderComponent,
  data: {
    segment: 'betFinder'
  }
},
  {
    path: 'bet-finder/results',
    component: DesktopBetFinderResultComponent,
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
export class BetfinderRoutingModule {}
