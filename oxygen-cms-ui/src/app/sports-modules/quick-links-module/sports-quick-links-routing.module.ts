import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {QuickLinksModuleComponent} from './quick-links-module/quick-links-module.component';
import {
  SportsQuickLinksEditComponent
} from '@app/sports-modules/quick-links-module/sports-quick-links/sports-quick-links-edit/sports-quick-links-edit.component';

const routes: Routes = [
  {
    path: ':moduleId',
    component: QuickLinksModuleComponent,
    children: []
  },
  {
    path: ':moduleId/:linkId',
    component: SportsQuickLinksEditComponent,
    children: []
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
export class SportsQuickLinksRoutingModule { }
