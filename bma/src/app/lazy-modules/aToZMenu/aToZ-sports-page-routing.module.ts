import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AzSportsPageComponent } from '@lazy-modules-module/aToZMenu/components/AzSportsPageComponent/az-sports-page.component';

const routes: Routes = [{
  path: '',
  component: AzSportsPageComponent
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LazyAToZSportPageRoutingModule { }
