import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {StaticTextOtfListComponent} from './static-text-list/static-text-list.page.component';
import {StaticTextOtfComponent} from './static-text-edit/pageComponent/static-text-edit.component';

const staticTextOtfConfigurationRoutes: Routes = [
  {
    path: '',
    component: StaticTextOtfListComponent,
    children: []
  },
  { path: ':id',
    component: StaticTextOtfComponent
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(staticTextOtfConfigurationRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class StaticTextOtfRoutingModule { }
