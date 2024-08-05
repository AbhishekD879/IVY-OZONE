import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import {SharedModule} from '@app/shared/shared.module';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { SplashPageConfigComponent } from '@app/timeline/splash-page/splash-page-config.component';
import {SplashPageRoutingModule} from '@app/timeline/splash-page/splash-page-routing.module';
import {TimelineSplashConfigApiService} from '@app/timeline/service/timeline-splash-config-api.service';
import { MatTableModule } from '@angular/material/table';

@NgModule({
  imports: [
    CommonModule,
    SplashPageRoutingModule,
    SharedModule,
    FormsModule,
    ReactiveFormsModule,
    MatTableModule
  ],
  providers: [TimelineSplashConfigApiService],
  declarations: [SplashPageConfigComponent],
  entryComponents: [SplashPageConfigComponent]
})
export class SplashPageModule { }
