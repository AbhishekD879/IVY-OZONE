import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import {AssetManagementListComponent} from '@app/asset-management/asset-management-list/asset-management-list.component';
import {AssetManagementEditComponent} from '@app/asset-management/asset-management-edit/asset-management-edit.component';

const AssetManagementRoutes: Routes = [
  {
    path: '',
    component: AssetManagementListComponent,
    children: []
  },
  { path: ':id',  component: AssetManagementEditComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(AssetManagementRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class AssetManagementRoutingModule { }
