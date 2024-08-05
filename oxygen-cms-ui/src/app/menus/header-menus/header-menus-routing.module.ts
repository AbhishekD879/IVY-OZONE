import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { HeaderMenusListComponent } from './header-menus-list/header-menus-list.component';
import { HeaderMenusEditComponent } from './header-menus-edit/header-menus-edit.component';

const routes: Routes = [
  {
    path: 'header-menus',
    component: HeaderMenusListComponent,
    children: []
  },
  {
    path: 'header-menus/:id', component: HeaderMenusEditComponent
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
export class HeaderMenusRoutingModule { }
