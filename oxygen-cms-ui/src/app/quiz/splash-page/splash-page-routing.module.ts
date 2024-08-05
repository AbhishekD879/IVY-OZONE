import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {SplashPageListComponent} from '@app/quiz/splash-page/splash-page-list/splash-page-list.component';
import {SplashPageEditComponent} from '@app/quiz/splash-page/splash-page-edit/splash-page-edit.component';
import {SplashPageCreateComponent} from '@app/quiz/splash-page/splash-page-create/splash-page-create.component';

const routes: Routes = [
  {
    path: '',
    component: SplashPageListComponent
  },
  {
    path: 'splash-page/:id',
    component: SplashPageEditComponent
  },
  {
    path: 'create',
    component: SplashPageCreateComponent
  }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SplashPageRoutingModule { }
