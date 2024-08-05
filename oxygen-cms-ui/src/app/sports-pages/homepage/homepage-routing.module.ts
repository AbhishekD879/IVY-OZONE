import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import {HomePageComponent} from './homepage-page/home.page.component';
import {FeaturedModulesListComponent} from '@app/featured-tab/featured-modules-list/featured-modules-list.component';

const routes: Routes = [
  {
    path: '',
    component: HomePageComponent,
    children: []
  },
  {
    path: 'sports-module',
    loadChildren: () => import('app/sports-modules/sports-modules.module').then(m => m.SportsModulesModule)
  },
  {
    path: 'featured-modules',
    component: FeaturedModulesListComponent
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
export class HomepageRoutingModule { }
