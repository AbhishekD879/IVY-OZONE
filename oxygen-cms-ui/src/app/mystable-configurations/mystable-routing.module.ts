import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MystableConfigurationsComponent } from '@app/mystable-configurations/mystable-configurations.component';


const routes: Routes = [
  {
    path: '',
    component: MystableConfigurationsComponent,
    children: []
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MystableRoutingModule { }
