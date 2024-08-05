import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {SharedModule} from '../shared/shared.module';
import {DialogService} from '../shared/dialog/dialog.service';

import {ApiClientService} from '../client/private/services/http';
import {BrandService} from '../client/private/services/brand.service';
import { BonusSuppressionRoutingModule } from './bonus-suppression-routing.module';
import { ManageBonusSuppressionModulesComponent } from './manage-bonus-suppression-modules/manage-bonus-suppression-modules.component';
import { AddEditBonusSuppressionModulesComponent } from './add-edit-bonus-suppression-modules/add-edit-bonus-suppression-modules.component';
import { BonusSuppressionService } from '@app/client/private/services/http/bonusSuppression.service';
import { ModulesBonusSuppressionComponent } from './modules-bonus-suppression/modules-bonus-suppression.component';
import { ModulesConfigurationComponent } from './modules-configuration/modules-configuration.component';
import { NgSelectModule } from '@ng-select/ng-select';
import { NgOptionHighlightModule } from '@ng-select/ng-option-highlight';


@NgModule({
  declarations: [ManageBonusSuppressionModulesComponent, AddEditBonusSuppressionModulesComponent, ModulesBonusSuppressionComponent, ModulesConfigurationComponent],
  imports: [
    CommonModule,
    SharedModule,
    BonusSuppressionRoutingModule,
    NgSelectModule,
    NgOptionHighlightModule,
  ],
  providers: [
    DialogService,
    BonusSuppressionService,
    ApiClientService,
    BrandService
  ],
  entryComponents: [
    AddEditBonusSuppressionModulesComponent, ModulesBonusSuppressionComponent
  ]
})
export class BonusSuppressionModule { }


