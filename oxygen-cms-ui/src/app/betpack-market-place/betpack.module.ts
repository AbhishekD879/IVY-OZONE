import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from '@app/shared/shared.module';
import { BetPackMarketService } from '@app/client/private/services/http/bet-pack-market.service';
import { SportsSurfaceBetsService } from '@app/sports-modules/surface-bets/surface-bets.service';
import { BannerComponent } from '@app/betpack-market-place/banner/banner.component';
import { BetPackRoutingModule } from '@app/betpack-market-place/betpack-routing.module';
import { BetPackTokenComponent } from '@app/betpack-market-place/betpack-token/betpack-token.component';
import { BetPackCreateComponent } from '@app/betpack-market-place/create-betpack/bet-pack-create.component';
import { BetPackEditComponent } from '@app/betpack-market-place/edit-betpack/bet-pack-edit.component';
import { FilterCreateComponent } from '@app/betpack-market-place/filter/create-filter/filter-create.component';
import { EditFilterComponent } from '@app/betpack-market-place/filter/edit-filter/edit-filter.component';
import { FilterComponent } from '@app/betpack-market-place/filter/filter.component';
import { BetPackListComponent } from '@app/betpack-market-place/list-betpack/bet-pack-list.component';
import { StaticFieldComponent } from '@app/betpack-market-place/static-fields/betpack-static-fields.component';
import { CreateOnboardComponent } from './onboarding-betpack/create-onboard/create-onboard.component'
import { BetpackOnboardService } from '../client/private/services/betpack-onboard.service';
import { EditOnboardComponent } from './onboarding-betpack/edit-onboard/edit-onboard.component';
import { OnboardingBetpackComponent } from './onboarding-betpack/onboarding-betpack.component';

@NgModule({
    imports: [SharedModule, BetPackRoutingModule, FormsModule, ReactiveFormsModule],
    providers: [BetPackMarketService, SportsSurfaceBetsService,BetpackOnboardService],
    declarations: [
        FilterComponent,
        BetPackCreateComponent,
        BetPackEditComponent,
        BetPackListComponent,
        BannerComponent,
        FilterCreateComponent,
        EditFilterComponent,
        StaticFieldComponent,
        BetPackTokenComponent,
        OnboardingBetpackComponent,
        CreateOnboardComponent,
        EditOnboardComponent
    ],
    entryComponents: [
        FilterCreateComponent,
        BetPackEditComponent,
        BetPackCreateComponent
    ]
})
export class BetPackModule { }
