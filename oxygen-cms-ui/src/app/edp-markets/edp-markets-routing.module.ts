import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { EdpListComponent } from './edp-list/edp-list.component';
import { EditEdpMarketComponent } from './edit-edp-market/edit-edp-market.component';

const edpMarketsConfigurationRoutes: Routes = [
  {
    path: '',
    component: EdpListComponent
  },
  { path: ':id',  component: EditEdpMarketComponent },
];

@NgModule({
  imports: [
    RouterModule.forChild(edpMarketsConfigurationRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class EdpMarketsRoutingModuleModule { }
