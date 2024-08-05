import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';

import { FreebetsComponent } from '@freebetsModule/components/freebets/freebets.component';
import { FreebetDetailsComponent } from '@app/freebets/components/freebetDetails/freebet-details.component';

const routes: Routes = [{
  path: '',
  component: FreebetsComponent,
  pathMatch: 'full',
  data: {
    segment: 'freebets'
  }
}, {
  path: ':betId',
  component: FreebetDetailsComponent,
  pathMatch: 'full',
  data: {
    segment: 'freebetDetails'
  }
}];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: []
})
export class FreebetsRoutingModule {

}
