import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {SplashPageConfigComponent} from '@app/timeline/splash-page/splash-page-config.component';

const routes: Routes = [
  {
    path: '',
    component: SplashPageConfigComponent,
    children: []

  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SplashPageRoutingModule { }
