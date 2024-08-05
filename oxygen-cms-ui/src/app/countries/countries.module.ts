import { NgModule } from '@angular/core';
import { SharedModule } from '../shared/shared.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { ContriesListEditComponent } from './contries-list-edit/contries-list-edit.component';
import { CountriesConfigurationRoutingModule } from './countries-routing.module';
import { CountriesListGroupComponent } from './countries-list-group/countries-list-group.component';


@NgModule({
  imports: [
    CountriesConfigurationRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    SharedModule
  ],
  declarations: [
    ContriesListEditComponent,
    CountriesListGroupComponent
  ]
})
export class CountriesModule { }
