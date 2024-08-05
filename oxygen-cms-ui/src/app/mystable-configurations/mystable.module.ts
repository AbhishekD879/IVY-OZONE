import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MystableRoutingModule } from '@app/mystable-configurations/mystable-routing.module';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import { SharedModule } from '@app/shared/shared.module';
import { MystableConfigurationsComponent } from '@app/mystable-configurations/mystable-configurations.component';

@NgModule({
  declarations: [MystableConfigurationsComponent],
  imports: [
    SharedModule,
    CommonModule,
    MystableRoutingModule,
    MatSlideToggleModule
  ]
})
export class MystableModule { }
