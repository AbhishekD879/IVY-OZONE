import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { NavigationPointsListComponent } from './navigation-points-list/navigation-points-list.component';
import { NavigationPointsEditComponent } from './navigation-points-edit/navigation-points-edit.component';

const routes: Routes = [
  {
    path: 'navigation-points',
    component: NavigationPointsListComponent,
    children: []
  },
  {
    path: 'navigation-points/add',
    component: NavigationPointsEditComponent
  },
  {
    path: 'navigation-points/:id',
    component: NavigationPointsEditComponent
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
export class NavigationPointsRoutingModule { }
