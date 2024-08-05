import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LottoDetailsComponent } from './lotto-details/lotto-details.component';
import { LottoListComponent } from './lotto-list/lotto-list.component';
import { LOTTO_ROUTES } from './lotto.constants';
const routes: Routes =[
  {
    path: '',
    component: LottoListComponent,
    children: []
  },
  { path: LOTTO_ROUTES.add, component: LottoDetailsComponent},
  {
    path: LOTTO_ROUTES.details, component: LottoDetailsComponent 
  }
]
@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class LottoRoutingModule { }
