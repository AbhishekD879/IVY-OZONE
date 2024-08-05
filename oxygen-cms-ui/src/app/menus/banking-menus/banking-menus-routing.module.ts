import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { BankingMenusListComponent } from './banking-menus-list/banking-menus-list.component';
import { BankingMenusEditComponent } from './banking-menus-edit/banking-menus-edit.component';

const routes: Routes = [
  {
    path: 'banking-menus',
    component: BankingMenusListComponent,
    children: []
  },
  {
    path: 'banking-menus/:id', component: BankingMenusEditComponent
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
export class BankingMenusRoutingModule { }
