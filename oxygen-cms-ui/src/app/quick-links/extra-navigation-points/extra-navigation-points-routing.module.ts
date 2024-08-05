import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ExtraNavigationPointsEditComponent } from '@app/quick-links/extra-navigation-points/extra-navigation-points-edit/extra-navigation-points-edit.component';
import { ExtraNavigationPointsListComponent } from '@app/quick-links/extra-navigation-points/extra-navigation-points-list/extra-navigation-points-list.component';

const routes: Routes = [
  {
    path: 'extra-navigation-points',
    component: ExtraNavigationPointsListComponent,
    children: []
  },
  {
    path: 'extra-navigation-points/:id',
    component: ExtraNavigationPointsEditComponent
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

export class ExtraNavigationPointsRoutingModule { }
