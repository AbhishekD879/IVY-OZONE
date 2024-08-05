import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { ConnectMenusListComponent } from './connect-menus-list/connect-menus-list.component';
import { ConnectMenusEditComponent } from './connect-menus-edit/connect-menus-edit.component';

const routes: Routes = [
  {
    path: 'connect-menus',
    component: ConnectMenusListComponent,
    children: []
  },
  {
    path: 'connect-menus/:id', component: ConnectMenusEditComponent
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
export class ConnectMenusRoutingModule { }
