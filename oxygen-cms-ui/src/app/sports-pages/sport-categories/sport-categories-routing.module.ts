import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import {PendingChangesGuard} from '../../client/private/classes/PendingChangesGuard.class';
import {SportCategoriesListComponent} from './sport-categories-list/sport-categories-list.component';
import {SportCategoriesEditComponent} from './sport-categories-edit/sport-categories-edit.component';
import {SportTabEditComponent} from '@app/sports-pages/sport-categories/sport-tab-edit/sport-tab-edit.component';

const routes: Routes = [
  {
    path: '',
    component: SportCategoriesListComponent,
    children: []
  },
  {
    path: ':id', component: SportCategoriesEditComponent,
    canDeactivate: [PendingChangesGuard]
  },
  {
    path: ':id/sports-module',
    loadChildren: () => import('app/sports-modules/sports-modules.module').then(m => m.SportsModulesModule)
  },
  {
    path: ':id/sport-tab/:sportTabId', component: SportTabEditComponent
  },
  {
    path: ':id/sport-tab/:sportTabId/insightsTab',
    loadChildren: () => import('app/sports-pages/sport-categories/insights/insights.module').then(m => m.InsightsModule)
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: [PendingChangesGuard]
})
export class SportCategoriesRoutingModule { }
