import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router'; 
import { BetsbasedonmoduleComponent } from './bets-based-on-your-module/bets-based-on-module.component';


const routes: Routes = [
  {
    path:':moduleId', component: BetsbasedonmoduleComponent  
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class sportFanzoneRoutingModule { }
