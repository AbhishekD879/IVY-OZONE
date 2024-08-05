import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { YcStaticBlocksListComponent } from './yc-static-blocks-list/yc-static-blocks-list.component';
import { YcStaticBlocksEditComponent } from './yc-static-blocks-edit/yc-static-blocks-edit.component';

const YCStaticBlocksRoutes: Routes = [
  {
    path: '',
    component: YcStaticBlocksListComponent,
    children: []
  },
  { path: ':id',  component: YcStaticBlocksEditComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(YCStaticBlocksRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class YourCallStaticBlocksRoutingModule { }
