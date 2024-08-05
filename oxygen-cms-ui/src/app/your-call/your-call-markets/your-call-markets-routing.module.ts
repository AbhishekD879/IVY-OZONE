import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { YcMarketsListComponent } from './yc-markets-list/yc-markets-list.component';
import { YcMarketsEditComponent } from './yc-markets-edit/yc-markets-edit.component';

const YCMarketsRoutes: Routes = [
  {
    path: '',
    component: YcMarketsListComponent,
    children: []
  },
  { path: ':id',  component: YcMarketsEditComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(YCMarketsRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class YourCallMarketsRoutingModule { }
