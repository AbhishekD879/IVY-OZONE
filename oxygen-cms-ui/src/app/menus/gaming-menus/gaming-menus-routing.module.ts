import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { GamingMenusListComponent } from './gaming-menus-list/gaming-menus-list.component';
import { GamingMenusEditComponent } from './gaming-menus-edit/gaming-menus-edit.component';

const routes: Routes = [
  {
    path: 'gaming-submenus',
    component: GamingMenusListComponent,
    children: []
  },
  {
    path: 'gaming-submenus/:id', component: GamingMenusEditComponent
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
export class GamingMenusRoutingModule { }
