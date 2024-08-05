import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { FeaturedModulesListComponent } from './featured-modules-list/featured-modules-list.component';
import { FeaturedModuleComponent } from './featured-module/featured-module.component';

const FeaturedTabRoutes: Routes = [
  {
    path: '',
    component: FeaturedModulesListComponent
  },
  {
    path: 'edit/:id',  component: FeaturedModuleComponent
  },
  {
    path: 'add',  component: FeaturedModuleComponent
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(FeaturedTabRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class FeaturedTabRoutingModule { }
