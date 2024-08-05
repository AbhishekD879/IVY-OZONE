import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { VirtualSportClassesComponent } from '@ladbrokesMobile/vsbr/components/virtualSportClasses/virtual-sport-classes.component';

// Overridden
import { VirtualSportsPageComponent } from '@ladbrokesDesktop/vsbr/components/virtualSportsPage/virtual-sports-page.component';
import { DesktopVirtualHomePageComponent } from '@ladbrokesDesktop/vsbr/components/virtualHomePage/virtual-home-page.component';
import { VirtualsGuard } from '@app/vsbr/guards/virtuals.guard';

const routes: Routes = [
  {
    path: '',
    component: DesktopVirtualHomePageComponent,
    data: {
      segment: 'virtual-sports'
    },
    canActivate:[VirtualsGuard]
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
