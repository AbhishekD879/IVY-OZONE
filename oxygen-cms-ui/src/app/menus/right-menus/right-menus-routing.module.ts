import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { RightMenusListComponent } from './right-menus-list/right-menus-list.component';
import { RightMenusEditComponent } from './right-menus-edit/right-menus-edit.component';

const routes: Routes = [
  {
    path: 'right-menus',
    component: RightMenusListComponent,
    children: []
  },
  {
    path: 'right-menus/:id', component: RightMenusEditComponent
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
export class RightMenusRoutingModule { }
