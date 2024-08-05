import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AzSportsPageLadbrokesMobileComponent } from '@ladbrokesMobile/lazy-modules/aToZMenu/az-sports-page.component';

const routes: Routes = [{
  path: '',
  component: AzSportsPageLadbrokesMobileComponent
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LazyAToZSportPageRoutingModule { }
