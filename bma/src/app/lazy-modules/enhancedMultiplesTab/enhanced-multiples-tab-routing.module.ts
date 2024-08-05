import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { EnhancedMultiplesTabComponent } from '@lazy-modules-module/enhancedMultiplesTab/components/enhanced-multiples-tab.component';

const routes: Routes = [{
  path: '',
  component: EnhancedMultiplesTabComponent
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LazyEnhancedMultiplesTabRoutingModule { }
