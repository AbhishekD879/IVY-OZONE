import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';

import { VirtualSportClassesComponent } from './components/virtualSportClasses/virtual-sport-classes.component';
import { VirtualSportsPageComponent } from './components/virtualSportsPage/virtual-sports-page.component';
import { VirtualHomePageComponent } from './components/virtualHomePage/virtual-home-page.component';
import { NgOptimizedImage } from '@angular/common';
import { VirtualsGuard } from '@app/vsbr/guards/virtuals.guard';

const routes: Routes = [
  {
    path: '',
    component: VirtualHomePageComponent,
    canActivate: [VirtualsGuard],
    data: {
      segment: 'virtual-sports'
    }
  },
  {
    path: 'sports',
    component: VirtualSportsPageComponent,
    data: {
      segment: 'virtual-sports.sports'
    },
    children: [
      {
        path: ':category',
        component: VirtualSportClassesComponent,
        data: {
          segment: 'virtual-sports.category'
        }
      },
      {
        path: ':category/:alias',
        component: VirtualSportClassesComponent,
        data: {
          segment: 'virtual-sports.class'
        }
      },
      {
        path: ':category/:alias/:eventId',
        component: VirtualSportClassesComponent,
        data: {
          segment: 'virtual-sports.vhrEvent'
        }
      }
    ]
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes),
    NgOptimizedImage
  ],
  exports: [
    RouterModule
  ],
  providers: []
})
export class VsbrRoutingModule {}
