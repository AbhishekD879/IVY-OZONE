import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { LadbrokesAzSportsPageComponent } from '@ladbrokesDesktop/lazy-modules/aToZMenu/components/az-sports-page.component';

const routes: Routes = [{
  path: '',
  component: LadbrokesAzSportsPageComponent
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LazyAToZSportPageRoutingModule { }
