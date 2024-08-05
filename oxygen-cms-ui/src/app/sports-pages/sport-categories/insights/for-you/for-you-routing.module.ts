import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { foryoumainComponent } from './for-you-main/for-you-main.component';
import { ForyoupersonalizedComponent } from './for-you-personalized/for-you-personalized.component';
const routes: Routes = [
  {
    path: '', component: foryoumainComponent
  },
  {
    path: 'for-you-personalized-bets/:forYouid', component: ForyoupersonalizedComponent
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
export class ForYouRoutingModule {}
