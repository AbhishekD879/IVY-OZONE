import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ParentSportsListComponent } from './parent-sports/parent-sports-list/parent-sports-list.component';
import { ParentSportsEditComponent} from '@app/virtual-sports/parent-sports/parent-sports-edit/parent-sports-edit.component';
import {ChildSportsEditComponent} from '@app/virtual-sports/child-sports/child-sports-edit/child-sports-edit.component';


const routes: Routes = [
  {
    path: '',
    component: ParentSportsListComponent
  },
  {
    path: ':id',
    component: ParentSportsEditComponent
  },
  {
    path: ':id/child-sport/:childSportId',
    component: ChildSportsEditComponent
  },
  {
    path: 'child-sport/:childSportId',
    component: ChildSportsEditComponent
  },
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class VirtualSportsRoutingModule { }
