import { NgModule } from '@angular/core';
import { SharedModule } from '@app/shared/shared.module';
import { ArcConfigurationsComponent } from '@app/arc-configurations/arc-configurations.component';
import { ArcSportActionsPopUpComponent } from '@app/arc-configurations/arc-sport-actions-pop-up/arc-sport-actions-pop-up.component';
import { ArcConfirgurationsRoutingModule } from '@app/arc-configurations/arc-confirgurations-routing.module';
@NgModule({
    imports: [
        SharedModule,
        ArcConfirgurationsRoutingModule
    ],
    declarations: [
        ArcConfigurationsComponent,
        ArcSportActionsPopUpComponent
    ]
})
export class ArcConfigurationModule { }