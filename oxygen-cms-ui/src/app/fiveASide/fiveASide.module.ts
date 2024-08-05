import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../shared/shared.module';
import { FiveASideRoutingModule } from './fiveASide-routing.module';
import {FiveASideCreateComponent} from '@app/fiveASide/fiveASide-create/fiveASide-create.component';
import {FiveASideEditComponent} from '@app/fiveASide/fiveASide-edit/fiveASide-edit.component';
import {FiveASideListComponent} from '@app/fiveASide/fiveASide-list/fiveASide-list.component';
import {FiveASideApiService} from '@app/fiveASide/services/fiveASide.api.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    FiveASideRoutingModule,
    FormsModule,
    ReactiveFormsModule
  ],
  declarations: [
    FiveASideCreateComponent,
    FiveASideEditComponent,
    FiveASideListComponent
  ],
  providers: [
    FiveASideApiService
  ],
  entryComponents: [
    FiveASideCreateComponent
  ]
})
export class FiveASideModule { }
