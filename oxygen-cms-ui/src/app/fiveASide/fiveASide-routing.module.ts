import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import {FiveASideListComponent} from '@app/fiveASide/fiveASide-list/fiveASide-list.component';
import {FiveASideEditComponent} from '@app/fiveASide/fiveASide-edit/fiveASide-edit.component';

const FiveASideRoutes: Routes = [
  {
    path: '',
    component: FiveASideListComponent,
    children: []
  },
  { path: ':id',  component: FiveASideEditComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(FiveASideRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class FiveASideRoutingModule { }
