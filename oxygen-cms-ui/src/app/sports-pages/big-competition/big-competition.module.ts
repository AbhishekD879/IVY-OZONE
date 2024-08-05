import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {SharedModule} from '../../shared/shared.module';
import {DialogService} from '../../shared/dialog/dialog.service';

import {BigCompetitionRoutingModule} from './big-competition-routing.module';
import {BigCompetitionAPIService} from './service/big-competition.api.service';
import {BigCompetitionService} from './service/big-competition.service';

import {CompetitionEditComponent} from './competition/competition-edit/competition-edit.component';
import {CompetitionsListComponent} from './competition/competitions-list/competitions-list.component';
import {CompetitionAddComponent} from './competition/competition-add/competition-add.component';

import {TabsListComponent} from './competition-tab/tabs-list/tabs-list.component';
import {TabEditComponent} from './competition-tab/tab-edit/tab-edit.component';
import {TabAddComponent} from './competition-tab/tab-add/tab-add.component';

import {CompetitionSubTabAddComponent} from './competition-sub-tab/competition-sub-tab-add/competition-sub-tab-add.component';
import {CompetitionSubTabEditComponent} from './competition-sub-tab/competition-sub-tab-edit/competition-sub-tab-edit.component';
import {CompetitionSubTabsListComponent} from './competition-sub-tab/competition-sub-tabs-list/competition-sub-tabs-list.component';

import {CompetitionModulesListComponent} from './competition-module/competition-modules-list/competition-modules-list.component';
import {CompetitionModuleAddComponent} from './competition-module/competition-module-add/competition-module-add.component';
import {CompetitionModuleEditComponent} from './competition-module/competition-module-edit/competition-module-edit.component';
import {SpaceToDashPipe} from '../../client/private/pipes/space-to-dash.pipe';
import {AddSpaceAfterCommaPipe} from '../../client/private/pipes/addSpaceAfterComma.pipe';

import {AemModuleComponent} from './competition-module/modules/aem-module/aem-module.component';
import {OutrightModuleComponent} from './competition-module/modules/outright-module/market-list/market-list.component';
import {NexteventsModuleComponent} from './competition-module/modules/nextevents-module/nextevents-module.component';
import {NexteventsIndividualComponent} from './competition-module/modules/nextevents-individual/nextevents-individual.component';
import {PromotionsModuleComponent} from './competition-module/modules/promotions-module/promotions-module.component';
import {SpecialsModuleComponent} from './competition-module/modules/specials-module/specials-module.component';
import {SpecialsoverviewModuleComponent} from './competition-module/modules/specialsoverview-module/specialsoverview-module.component';
import {MarketDialogComponent} from './competition-module/modules/outright-module/market-dialog/market-dialog.component';

import {ParticipantCreateComponent} from './participant/participant-create/participant-create.component';
import {ParticipantEditComponent} from './participant/participant-edit/participant-edit.component';
import {ParticipantsListComponent} from './participant/participants-list/participants-list.component';
import {GroupAllComponent} from './competition-module/modules/group-all/group-all.component';
import {GroupWidgetComponent} from './competition-module/modules/group-widget/group-widget.component';
import {GroupIndividualComponent} from './competition-module/modules/group-individual/group-individual.component';
import {KnockoutsModuleComponent} from './competition-module/modules/knockouts-module/knockouts-module.component';
import {MatchesListComponent} from './competition-module/modules/knockouts-module/matches/matches-list/matches-list.component';
import {MatchCreateComponent} from './competition-module/modules/knockouts-module/matches/match-create/match-create.component';
import {ResultsModuleComponent} from './competition-module/modules/results-module/results-module.component';

import {RoundNamesAddComponent} from './competition-module/modules/knockouts-module/round-names/round-names-add/round-names-add.component';
// tslint:disable-next-line:max-line-length
import {RoundNamesEditComponent} from './competition-module/modules/knockouts-module/round-names/round-names-edit/round-names-edit.component';
import {RoundNamesListComponent} from './competition-module/modules/knockouts-module/round-names/round-names-list/round-names-list.component';
import {MatchEditComponent} from './competition-module/modules/knockouts-module/matches/match-edit/match-edit.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    BigCompetitionRoutingModule
  ],
  declarations: [
    CompetitionEditComponent,
    CompetitionAddComponent,
    CompetitionsListComponent,
    TabsListComponent,
    TabEditComponent,
    TabAddComponent,
    CompetitionSubTabAddComponent,
    CompetitionSubTabEditComponent,
    CompetitionSubTabsListComponent,
    CompetitionModulesListComponent,
    CompetitionModuleAddComponent,
    CompetitionModuleEditComponent,
    AemModuleComponent,
    OutrightModuleComponent,
    NexteventsModuleComponent,
    NexteventsIndividualComponent,
    PromotionsModuleComponent,
    SpecialsModuleComponent,
    SpecialsoverviewModuleComponent,
    ResultsModuleComponent,
    SpaceToDashPipe,
    AddSpaceAfterCommaPipe,
    ParticipantCreateComponent,
    ParticipantEditComponent,
    ParticipantsListComponent,
    MarketDialogComponent,
    GroupAllComponent,
    GroupWidgetComponent,
    GroupIndividualComponent,
    KnockoutsModuleComponent,
    MatchesListComponent,
    MatchCreateComponent,
    MatchEditComponent,
    RoundNamesListComponent,
    RoundNamesAddComponent,
    RoundNamesEditComponent
  ],
   providers: [
    DialogService,
    BigCompetitionAPIService,
    BigCompetitionService,
    SpaceToDashPipe,
    AddSpaceAfterCommaPipe
  ],
  entryComponents: [
    CompetitionAddComponent,
    TabAddComponent,
    CompetitionSubTabAddComponent,
    CompetitionModuleAddComponent,
    AemModuleComponent,
    NexteventsModuleComponent,
    NexteventsIndividualComponent,
    OutrightModuleComponent,
    PromotionsModuleComponent,
    SpecialsModuleComponent,
    SpecialsoverviewModuleComponent,
    ResultsModuleComponent,
    ParticipantCreateComponent,
    MarketDialogComponent,
    GroupWidgetComponent,
    GroupAllComponent,
    GroupIndividualComponent,
    KnockoutsModuleComponent,
    MatchCreateComponent,
    RoundNamesAddComponent
  ]
})
export class BigCompetitionModule { }
