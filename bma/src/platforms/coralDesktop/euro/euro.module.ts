import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { EuroRoutingModule } from '@coralDesktop/euro/euro.routing.module';
import {
    DesktopMatchRewardsMainComponent
} from '@coralDesktop/euro/components/matchRewardsMain/match-rewards-main.component';
import { DesktopMatchRewardsComponent } from '@coralDesktop/euro/components/matchRewards/match-rewards.component';
import { MatchRewardsMainComponent } from '@app/euro/components/matchRewardsMain/match-rewards-main.component';
import { EuroDialogComponent } from '@app/euro/components/euroDialog/euro-dialog.component';

import { TermsAndCondComponent } from '@app/euro/components/termsAndConditions/terms-and-cond.component';
import { EuroCongratsDialogComponent } from '@app/euro/components/euroCongratsDialog/euro-congrats-dialog.component';
import { MatchRewardsComponent } from '@app/euro/components/matchRewards/match-rewards.component';

@NgModule({
    imports: [SharedModule, EuroRoutingModule,
    ],
    declarations: [DesktopMatchRewardsMainComponent, DesktopMatchRewardsComponent, MatchRewardsMainComponent,
        TermsAndCondComponent, EuroDialogComponent, EuroCongratsDialogComponent,MatchRewardsComponent],
    exports: [DesktopMatchRewardsMainComponent, DesktopMatchRewardsComponent,MatchRewardsComponent],
    schemas: [
        NO_ERRORS_SCHEMA
    ]
})

export class EuroModule { }
