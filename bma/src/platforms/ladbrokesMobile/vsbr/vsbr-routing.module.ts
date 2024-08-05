import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';

// Overridden
import { VirtualSportsPageComponent } from '@vsbrModule/components/virtualSportsPage/virtual-sports-page.component';
import {
  VirtualSportClassesComponent } from '@vsbrModule/components/virtualSportClasses/virtual-sport-classes.component';
  import {
    MobileVirtualHomePageComponent
  } from '@ladbrokesMobile/vsbr/components/virtualHomePage/virtual-home-page.component';
import { VirtualsGuard } from '@app/vsbr/guards/virtuals.guard';


const routes: Routes = [
  {
    path: '',
    component: MobileVirtualHomePageComponent,
    canActivate:[VirtualsGuard],
    data: {
      segment: 'virtual-sports'
    },
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
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: []
})
export class VsbrRoutingModule {}
