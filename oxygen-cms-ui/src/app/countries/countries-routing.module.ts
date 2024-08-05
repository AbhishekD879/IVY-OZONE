import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ContriesListEditComponent } from './contries-list-edit/contries-list-edit.component';

const countriesConfigurationRoutes: Routes = [
  {
    path: '',
    component: ContriesListEditComponent
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(countriesConfigurationRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class CountriesConfigurationRoutingModule { }
