import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { RacingRoutingModule } from './racing-routing.module';
import { SharedModule } from '@app/shared/shared.module';
import { RacingModulePageComponent } from './racing-module-page/racing-module-page.component';


@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    RacingRoutingModule
  ],
  declarations: [ RacingModulePageComponent ],

  entryComponents: [ RacingModulePageComponent ],
  providers: [],
  exports: []
})
export class RacingModule { }
