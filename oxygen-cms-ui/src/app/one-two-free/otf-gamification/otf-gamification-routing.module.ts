import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { GamificationDetailsComponent } from './gamification-details/gamification-details.component';
import { GamificationListComponent } from './gamification-list/gamification-list.component';

const gamificationRoutes: Routes = [
  {
    path: 'create',
    component: GamificationDetailsComponent
  },
  {
    path: 'gamification/:id',
    component: GamificationDetailsComponent
  }, {
    path: '',
    component: GamificationListComponent,
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(gamificationRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class OtfGamificationRoutingModule { }
