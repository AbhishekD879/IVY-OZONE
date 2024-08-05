import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from '@root/app/shared/shared.module';
import { TabNameConfigurationComponent } from './tab-name-configuration.component';
import { TabNameConfigurationRoutingModule } from './tab-name-configuration-routing.module';
import { TabNameConfigurationApiService } from '../service/tabNameConfiguration.api.service';

@NgModule({
  declarations: [TabNameConfigurationComponent],
  imports: [
    CommonModule,
    TabNameConfigurationRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    SharedModule
  ],

  providers: [TabNameConfigurationApiService]
})
export class TabNameConfigurationModule { }
