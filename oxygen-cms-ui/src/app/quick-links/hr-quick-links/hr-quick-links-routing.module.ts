import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { HrQuickLinksListComponent } from './hr-quick-links-list/hr-quick-links-list.component';
import { HrQuickLinksEditComponent } from './hr-quick-links-edit/hr-quick-links-edit.component';

const routes: Routes = [
  {
    path: 'hr-quick-links',
    component: HrQuickLinksListComponent,
    children: []
  },
  {
    path: 'hr-quick-links/:id', component: HrQuickLinksEditComponent
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class HrQuickLinksRoutingModule { }
