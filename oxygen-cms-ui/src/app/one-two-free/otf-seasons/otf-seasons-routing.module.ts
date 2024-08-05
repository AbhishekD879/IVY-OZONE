import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SeasonEditComponent } from './season-edit/season-edit.component';
import { SeasonViewComponent } from './season-view/season-view.component';

const seasonRoutes: Routes = [
  {
    path: 'create',
    component: SeasonEditComponent
  },
  {
    path: 'season/:id',
    component: SeasonEditComponent
  },
  {
    path: '',
    component: SeasonViewComponent,
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(seasonRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class OtfSeasonsRoutingModule { }
