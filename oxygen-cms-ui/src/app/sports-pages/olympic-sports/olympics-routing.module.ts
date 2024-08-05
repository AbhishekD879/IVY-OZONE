import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import {OlympicsPagesListPageComponent} from './olympic-sports-page/pageComponent/olympics.page.component';
import {SingleOlympicsPageComponent} from './single-olympics-page/pageComponent/olympics.page.component';

const promotionsRoutes: Routes = [
  {
    path: '',
    component: OlympicsPagesListPageComponent,
    children: [

    ]
  },
  { path: ':id',  component: SingleOlympicsPageComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(promotionsRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class WidgetsRoutingModule { }
