import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DevLogComponent } from '@lazy-modules/devLog/components/devLog/dev-log.component';

const routes: Routes = [
  {
    path: '',
    component: DevLogComponent,
    data: {
      segment: 'devlog'
    }
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DevLogRoutingModule { }
