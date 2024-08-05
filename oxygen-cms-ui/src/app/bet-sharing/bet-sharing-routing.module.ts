import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import { ShareCardComponent } from './share-card/share-card.component';
const betSharingModuleRoutes: Routes = [
  {
    path: '',
    component: ShareCardComponent
  },
  { path: ':id',  component: ShareCardComponent }

];

@NgModule({
  imports: [
    RouterModule.forChild(betSharingModuleRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class BetSharingRoutingModule { }
