import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { RacingEdpListComponent } from './racing-edp-list/racing-edp-list.component';
import { EditRacingEdpMarketComponent } from './edit-racing-edp-market/edit-racing-edp-market.component';

const routes: Routes = [
  {
    path: '',
    component: RacingEdpListComponent
  },
  {
    path: ':id',
    component: EditRacingEdpMarketComponent
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class RacingEdpMarketsRoutingModule { }
