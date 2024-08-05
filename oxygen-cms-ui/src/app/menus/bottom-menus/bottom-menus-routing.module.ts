import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { BottomMenusListComponent } from './bottom-menus-list/bottom-menus-list.component';
import { BottomMenusEditComponent } from './bottom-menus-edit/bottom-menus-edit.component';

const routes: Routes = [
  {
    path: 'bottom-menus',
    component: BottomMenusListComponent,
    children: []
  },
  {
    path: 'bottom-menus/:id', component: BottomMenusEditComponent
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
export class BottomMenusRoutingModule { }
