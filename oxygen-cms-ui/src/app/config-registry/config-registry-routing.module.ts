import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ConfigRegistryListComponent } from '@app/config-registry/config-registry-list/config-registry-list.component';


const registryRoutes: Routes = [
    { path: '', component: ConfigRegistryListComponent }
];

@NgModule({
    imports: [
        RouterModule.forChild(registryRoutes)
    ],
    exports: [
        RouterModule
    ]
})
export class ConfigRegistryRoutingModule { }