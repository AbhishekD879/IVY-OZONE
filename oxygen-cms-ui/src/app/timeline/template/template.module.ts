import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { TemplateRoutingModule } from './template-routing.module';
import {TemplateApiService} from '@app/timeline/service/template-api.service';
import {TemplateCreateComponent} from '@app/timeline/template/template-create/template-create.component';
import {TemplateEditComponent} from '@app/timeline/template/template-edit/template-edit.component';
import {TemplateListComponent} from '@app/timeline/template/template-list/template-list.component';
import {SharedModule} from '@app/shared/shared.module';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { MatTableModule } from '@angular/material/table';

@NgModule({
  imports: [
    CommonModule,
    TemplateRoutingModule,
    SharedModule,
    FormsModule,
    ReactiveFormsModule,
    MatTableModule
  ],
  providers: [TemplateApiService],
  declarations: [TemplateCreateComponent, TemplateEditComponent, TemplateListComponent],
  entryComponents: [TemplateCreateComponent]
})
export class TemplateModule { }
