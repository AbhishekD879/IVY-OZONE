import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { BYBSwitchersListComponent } from './byb-switchers-list/byb-switchers-list.component';
import { BYBSwitchersEditComponent } from './byb-switchers-edit/byb-switchers-edit.component';

const BYBSwitchersRoutes: Routes = [
  {
    path: '',
    component: BYBSwitchersListComponent,
    children: []
  },
  { path: ':id',  component: BYBSwitchersEditComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(BYBSwitchersRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class BYBSwitchersRoutingModule { }
