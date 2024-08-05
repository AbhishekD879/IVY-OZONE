import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { BybMarketsListComponent } from './byb-markets-list/byb-markets-list.component';
import { BybMarketsEditComponent } from './byb-markets-edit/byb-markets-edit.component';

const bybMarketsRoutes: Routes = [
  {
    path: '',
    component: BybMarketsListComponent,
    children: []
  },
  { path: ':id',  component: BybMarketsEditComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(bybMarketsRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class BybMarketsRoutingModule { }
