import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ConfigRegistryListComponent } from '@app/config-registry/config-registry-list/config-registry-list.component';
import { ConfigRegistryRoutingModule } from '@app/config-registry/config-registry-routing.module';
import { ConfigRegistryDetailsComponent } from '@app/config-registry/config-registry-details/config-registry-details.component';
import { SharedModule } from '../shared/shared.module';
import { ConfigRegistryApiService } from '@app/config-registry/services/config-registry.api.service';



@NgModule({
  declarations: [ConfigRegistryListComponent,
    ConfigRegistryDetailsComponent],
  imports: [
    ConfigRegistryRoutingModule,
    CommonModule,SharedModule
  ],providers: [ConfigRegistryApiService]
})
export class ConfigRegistryModule { }
