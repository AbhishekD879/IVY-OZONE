import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';

import { FeaturedTabComponent } from '@featured/components/featured-tab/featured-tab.component';

const routes: Routes = [
  {
    path: '',
    component: FeaturedTabComponent,
    data: {
      segment: 'home'
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
export class DesktopFeaturedRoutingModule {}
