import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EventHubListPageComponent } from '@app/sports-pages/event-hub/components/event-hub-list-page/event-hub-list.page.component';
import { EventHubPageComponent } from '@app/sports-pages/event-hub/components/event-hub-page/event-hub.page.component';

const routes: Routes = [
  {
    path: '',
    component: EventHubListPageComponent,
    children: []
  },
  {
    path: ':hubId',
    component: EventHubPageComponent
  },
  {
    path: ':hubId/sports-module',
    loadChildren: () => import('app/sports-modules/sports-modules.module').then(m => m.SportsModulesModule)
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
export class EventHubRoutingModule { }
