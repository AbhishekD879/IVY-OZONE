import { NgModule } from '@angular/core';
import { FiveASideShowdownRoutingModule } from '@app/five-a-side-showdown/five-a-side-showdown-routing.module';
import { ContestManagerComponent } from '@app/five-a-side-showdown/components/contest-manager/contest-manager.component';
import { PrizePoolComponent } from '@app/five-a-side-showdown/components/prize-pool/prize-pool.component';
import { PayTableComponent } from '@app/five-a-side-showdown/components/pay-table/pay-table.component';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@app/shared/shared.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { EditContestComponent } from '@app/five-a-side-showdown/components/edit-contest/edit-contest.component';
import { AddEditPrizeComponent } from '@app/five-a-side-showdown/components/add-edit-prize/add-edit-prize.component';
import { ContestManagerService } from '@app/client/private/services/http/contestManager.service';
import { AddContestComponent } from '@app/five-a-side-showdown/components/add-contest/add-contest.component';
import { FaqComponent } from '@app/five-a-side-showdown/components/faq/faq.component';
import { TermsAndConditionsComponent } from '@app/five-a-side-showdown/components/terms-and-conditions/terms-and-conditions.component';
import { AddEditFaqComponent } from '@app/five-a-side-showdown/components/add-edit-faq/add-edit-faq.component';
import { FAQService } from '@app/client/private/services/http/faq.service';
import { TermsAndConditionsService } from '@app/client/private/services/http/termsAndConditions.service';
import { WelcomeOverlayComponent } from '@app/five-a-side-showdown/components/welcome-overlay/welcome-overlay.component';

@NgModule({
    imports: [FiveASideShowdownRoutingModule, CommonModule,
        SharedModule,
        FormsModule,
        ReactiveFormsModule],
    declarations: [ContestManagerComponent,
        PrizePoolComponent,
        PayTableComponent,
        EditContestComponent,
        AddEditPrizeComponent,
        AddContestComponent,
        FaqComponent,
        TermsAndConditionsComponent,
        AddEditFaqComponent,
        WelcomeOverlayComponent],
    providers: [
        ContestManagerService,
        FAQService,
        TermsAndConditionsService
    ]
})
export class FiveASideShowdownModule {

}