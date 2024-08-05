import { NgModule } from '@angular/core';
import { ArcConfigurationsComponent } from '@app/arc-configurations/arc-configurations.component';
import { RouterModule, Routes } from '@angular/router';


const arcRoutes: Routes = [
    { path: '', component: ArcConfigurationsComponent }
];

@NgModule({
    imports: [
        RouterModule.forChild(arcRoutes)
    ],
    exports: [
        RouterModule
    ]
})
export class ArcConfirgurationsRoutingModule { }