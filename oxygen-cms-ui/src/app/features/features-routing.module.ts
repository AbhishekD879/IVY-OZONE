import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { FeatureListComponent } from './feature-list/feature-list.component';
import { FeatureEditComponent } from './feature-edit/feature-edit.component';

const FeaturesrsRoutes: Routes = [
  {
    path: '',
    component: FeatureListComponent,
    children: []
  },
  { path: ':id',  component: FeatureEditComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(FeaturesrsRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class FeaturesRoutingModule { }
