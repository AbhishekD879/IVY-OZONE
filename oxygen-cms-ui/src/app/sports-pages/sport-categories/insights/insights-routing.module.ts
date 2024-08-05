import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import { SportTabPopularBetsComponent } from './sport-tab-popular-bets/sport-tab-popular-bets.component';
import { InsightsComponent } from './inisghts-tab/insights.component';
  
const routes: Routes = [
  {
    path:'', component: InsightsComponent 
  },
  {
    path:'insights-popular', component: SportTabPopularBetsComponent
  },
  {
    path: 'insights-forYou',
    loadChildren: () => import('app/sports-pages/sport-categories/insights/for-you/for-you.module').then(m => m.ForYouModule)
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],

})
export class InsightsRoutingModule { }
