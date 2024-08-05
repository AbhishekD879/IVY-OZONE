import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { InplayHomeTabComponent } from '@bma/components/inlayHomeTab/inplay-home-tab.component';

const routes: Routes = [
  {
    path: '',
    component: InplayHomeTabComponent,
    data: {
      segment: 'inPlay'
    }
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: []
})
export class InplayHomeTabRoutingModule {}

