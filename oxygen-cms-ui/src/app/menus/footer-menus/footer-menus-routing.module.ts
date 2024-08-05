import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { FooterMenusListComponent } from './footer-menus-list/footer-menus-list.component';
import { FooterMenusEditComponent } from './footer-menus-edit/footer-menus-edit.component';

const routes: Routes = [
  {
    path: 'footer-menus',
    component: FooterMenusListComponent,
    children: []
  },
  {
    path: 'footer-menus/:id', component: FooterMenusEditComponent
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
export class FooterMenusRoutingModule { }
