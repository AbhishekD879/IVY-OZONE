import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { HeaderSubMenusListComponent } from './header-sub-menus-list/header-sub-menus-list.component';
import { HeaderSubMenusEditComponent } from './header-sub-menus-edit/header-sub-menus-edit.component';

const routes: Routes = [
  {
    path: 'header-submenus',
    component: HeaderSubMenusListComponent,
    children: []
  },
  {
    path: 'header-submenus/:id', component: HeaderSubMenusEditComponent
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
export class HeaderSubMenusRoutingModule { }
