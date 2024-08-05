import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DesktopBetFinderComponent } from '@ladbrokesDesktop/bf/components/betFinder/bet-finder.component';
import { DesktopBetFinderResultComponent } from '@ladbrokesDesktop/bf/components/betFinderResults/bet-finder-result.component';
import { IRouteData } from '@app/core/models/route-data.model';
import { ILadbrokesRetailConfig } from '@ladbrokesMobile/core/services/cms/models/system-config';
import { GermanSupportGuard } from '@app/core/guards/german-support-guard.service';

export const routes: Routes = [{
  path: 'bet-finder',
  canActivate: [GermanSupportGuard],
  component: DesktopBetFinderComponent,
  data: {
    segment: 'betFinder',
    feature: 'raceBetFinder'
  } as IRouteData<ILadbrokesRetailConfig>
},
  {
    path: 'bet-finder/results',
    canActivate: [GermanSupportGuard],
    component: DesktopBetFinderResultComponent,
    data: {
      segment: 'betFinderResults',
      feature: 'raceBetFinder'
    } as IRouteData<ILadbrokesRetailConfig>
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
