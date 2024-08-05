import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {
  FeaturedEventsModuleComponent
} from '@app/sports-modules/featured-events-module/featured-events-module/featured-events-module.component';

const routes: Routes = [
  {
    path: ':moduleId',
    component: FeaturedEventsModuleComponent,
    children: []
  },
  {
    path: ':moduleId/featured-modules',
    loadChildren: () => import('app/featured-tab/featured-tab.module').then(m => m.FeaturedTabModule)
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
export class FeaturedEventsModuleRoutingModule { }
