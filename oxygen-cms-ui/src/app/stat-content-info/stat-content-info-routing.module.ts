import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { StatContentListComponent } from './stat-content-list/stat-content-list.component';
import { StatContentComponent } from './stat-content/stat-content.component';

const StatContentRoutes: Routes = [
  {
    path: '',
    component: StatContentListComponent
  },
  {
    path: 'edit/:id',  component: StatContentComponent
  },
  {
    path: 'add',  component: StatContentComponent
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(StatContentRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class StatContentInfoRoutingModule { }
