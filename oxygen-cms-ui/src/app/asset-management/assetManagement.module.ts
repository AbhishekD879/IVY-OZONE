import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {SharedModule} from '@app/shared/shared.module';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {AssetManagementRoutingModule} from '@app/asset-management/asset-management-routing.module';
import {AssetManagementCreateComponent} from '@app/asset-management/asset-management-create/asset-management-create.component';
import {AssetManagementEditComponent} from '@app/asset-management/asset-management-edit/asset-management-edit.component';
import {AssetManagementListComponent} from '@app/asset-management/asset-management-list/asset-management-list.component';
import {AssetManagementApiService} from '@app/asset-management/services/assetManagement.api.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    AssetManagementRoutingModule,
    FormsModule,
    ReactiveFormsModule
  ],
  declarations: [
    AssetManagementCreateComponent,
    AssetManagementEditComponent,
    AssetManagementListComponent
  ],
  providers: [
    AssetManagementApiService
  ],
  entryComponents: [
    AssetManagementCreateComponent
  ]
})
export class AssetManagementModule { }
