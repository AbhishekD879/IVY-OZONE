import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { YcLeaguesListComponent } from './yc-leagues-list/yc-leagues-list.component';
import { YcLeaguesEditComponent } from './yc-leagues-edit/yc-leagues-edit.component';

const YCLeaguesRoutes: Routes = [
  {
    path: '',
    component: YcLeaguesListComponent,
    children: []
  },
  { path: ':id',  component: YcLeaguesEditComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(YCLeaguesRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class YourCallLeaguesRoutingModule { }
