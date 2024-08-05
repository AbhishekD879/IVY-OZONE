import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import { PopularbetsComponent } from './popular-bets.component';
import { PopularAccasWidgetComponent } from './popular-accas-widget/popular-accas-widget.component';
import { PopularAccasWidgetCardComponent } from './popular-accas-widget-card/popular-accas-widget-card.component';
const popularBetsModuleRoutes: Routes = [
  {
    path: '',
    children: [ {
    path: 'bet-slip',
    component: PopularbetsComponent
    },
    {
    path: 'bet-receipt',
    component: PopularbetsComponent
    },
    {
      path: 'popular-accas-widget',
      component: PopularAccasWidgetComponent
    },
    { path: 'popular-accas-widget/add', component: PopularAccasWidgetCardComponent },
    {
      path: 'popular-accas-widget/:id',  component: PopularAccasWidgetCardComponent
    },]
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(popularBetsModuleRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class PopularBetsRoutingModule { }