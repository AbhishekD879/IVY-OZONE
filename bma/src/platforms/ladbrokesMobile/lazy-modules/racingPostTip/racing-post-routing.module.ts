import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {
  LadbrokesRacingPostTipComponent
} from '@ladbrokesMobile/lazy-modules/racingPostTip/components/racingPostTip/racing-post-tip.component';

const routes: Routes = [
  {
    path: '',
    component: LadbrokesRacingPostTipComponent,
    data: {
      segment: 'racingPostTip'
    }
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LadbrokesRacingTipRoutingModule { }
