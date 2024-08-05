import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../shared/shared.module';
import { FormsModule } from '@angular/forms';

import { OddsBoostPageComponent } from './odds-boost-page/odds-boost.page.component';
import { OddsBoostRoutingModule } from './odds-boost-routing.module';

@NgModule({
  declarations: [
    OddsBoostPageComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    FormsModule,
    OddsBoostRoutingModule
  ],
  exports: [],
  providers: [],
})
export class OddsBoostModule {}
