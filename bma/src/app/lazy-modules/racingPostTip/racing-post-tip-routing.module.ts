import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { RacingPostTipComponent } from '@lazy-modules/racingPostTip/components/racingpostTip/racing-post-tip.component';

const routes: Routes = [
  {
    path: '',
    component: RacingPostTipComponent,
    data: {
      segment: 'racingPost'
    }
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RacingPostTipRoutingModule { }
