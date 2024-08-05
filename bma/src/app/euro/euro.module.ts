import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { EuroRoutingModule } from '@euro/euro.routing.module';

import { MatchRewardsMainComponent } from '@app/euro/components/matchRewardsMain/match-rewards-main.component';
import { MatchRewardsComponent } from '@app/euro/components/matchRewards/match-rewards.component';
import { TermsAndCondComponent } from '@app/euro/components/termsAndConditions/terms-and-cond.component';
import { EuroDialogComponent } from '@app/euro/components/euroDialog/euro-dialog.component';
import { EuroCongratsDialogComponent } from '@app/euro/components/euroCongratsDialog/euro-congrats-dialog.component';

@NgModule({
    imports: [SharedModule, EuroRoutingModule],
    declarations: [MatchRewardsMainComponent,
    MatchRewardsComponent, TermsAndCondComponent, EuroDialogComponent, EuroCongratsDialogComponent],
    exports: [MatchRewardsMainComponent,MatchRewardsComponent, TermsAndCondComponent, EuroDialogComponent, EuroCongratsDialogComponent],
    schemas: [
        NO_ERRORS_SCHEMA
    ]
})

export class EuroModule { }
