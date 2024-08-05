import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import {SharedModule} from '@app/shared/shared.module';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {SystemConfigRoutingModule} from '@app/timeline/system-config/system-config-routing.module';
import {SystemConfigComponent} from '@app/timeline/system-config/system-config.component';
import {TimelineSystemConfigApiService} from '@app/timeline/service/timeline-system-config-api.service';
import { MatTableModule } from '@angular/material/table';

@NgModule({
  imports: [
    CommonModule,
    SystemConfigRoutingModule,
    SharedModule,
    FormsModule,
    ReactiveFormsModule,
    MatTableModule
  ],
  providers: [TimelineSystemConfigApiService],
  declarations: [SystemConfigComponent],
  entryComponents: [SystemConfigComponent]
})
export class SystemConfigModule { }
