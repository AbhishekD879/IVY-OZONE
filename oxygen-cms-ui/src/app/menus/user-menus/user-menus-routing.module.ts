import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { UserMenusListComponent } from './user-menus-list/user-menus-list.component';
import { UserMenusEditComponent } from './user-menus-edit/user-menus-edit.component';

const routes: Routes = [
  {
    path: 'user-menus',
    component: UserMenusListComponent,
    children: []
  },
  {
    path: 'user-menus/:id', component: UserMenusEditComponent
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
export class UserMenusRoutingModule { }
