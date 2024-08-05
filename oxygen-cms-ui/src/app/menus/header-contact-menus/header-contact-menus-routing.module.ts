import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { HeaderContactMenusListComponent } from './header-contact-menus-list/header-contact-menus-list.component';
import { HeaderContactMenusEditComponent } from './header-contact-menus-edit/header-contact-menus-edit.component';

const routes: Routes = [
  {
    path: 'header-contact-menus',
    component: HeaderContactMenusListComponent,
    children: []
  },
  {
    path: 'header-contact-menus/:id', component: HeaderContactMenusEditComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class HeaderContactMenusRoutingModule { }
