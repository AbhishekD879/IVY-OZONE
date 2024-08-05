import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { BrandService } from '@app/client/private/services/brand.service';
import { DataTableColumn } from '@app/client/private/models';
import { ErrorService } from '@app/client/private/services/error.service';
import { ApiClientService } from '@app/client/private/services/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { 
  BonusSupDialogData,
  // BonusSupData,
  IBonusSuppressionModule, IModuleData, SAVE_MODULE_DIALOG } from '../models/module-manager';
import { HttpResponse } from '@angular/common/http';
import { BONUS_SUPPRESSION_ERROR_LABELS } from '@root/app/five-a-side-showdown/constants/contest-manager.constants';
import { cloneDeep } from 'lodash';

@Component({
  selector: 'app-add-edit-bonus-suppression-modules',
  templateUrl: './add-edit-bonus-suppression-modules.component.html',
  styleUrls: ['./add-edit-bonus-suppression-modules.component.scss']
})
export class AddEditBonusSuppressionModulesComponent implements OnInit {
  
  public dialogLabels = SAVE_MODULE_DIALOG;
  public selectedModuleId: string = '';
  public modules: any[] = [];
  public bonusSupModuleData: IBonusSuppressionModule;
  private dataChangedInUpdate = false;
  riskLevel = ['0 - Bonus Suppression', '1 - Problem Gambler Low', '2 - Problem Gambler  Medium', '3 - Problem Gambler High', '4 - Problem Gambler V High', '5 - At Risk Low', '6 - At Risk Medium', '7 - At Risk High'];
  reasonCode = ['0 - RGY User', '1 - Difference in spend from norm', '2 - Frequency of play', '3 - Frequency of play increase', '4 - Deposit frequency', '5 - Declined deposits', '6 - Multiple payment methods', '7 - Credit Cards', '8 - Cancelled withdrawals', '9 - Late night play', '10 - Speed of Play', '11 - Chaotic Play', '12 - Deposit Amount', '13 - Tenure*', '14 - In Session TopUp*', '15 - Variety of Games*', '16 - Frequency of Play TOSL7D', '17 - Player days'];
  moduleNames:IModuleData[] = [];
  riskLevelVal = "";
  reasonCodeVal = "";
  bonusSuppression : boolean = false;
  public moduleRowId: number;
  public moduleListColumns: Array<DataTableColumn> = [
    {
      name: 'Sub Module Name',
      property: 'moduleName',
      type: 'custom',
      customOnClickHandler: (colData, value, index) => {
        this.editModule(colData, value, index)
      }
    }
  ];
  public filterProperties: Array<string> = [
    'name'
  ];
  constructor(
    @Inject(MAT_DIALOG_DATA) public modalData: BonusSupDialogData,
    private brandService: BrandService,
    private dialogRef: MatDialogRef<AddEditBonusSuppressionModulesComponent>,
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,
    private errorService: ErrorService
  ) { }

  ngOnInit(): void {
    this.getAllModules();
  }

  getAllModules() {
    this.showHideSpinner();
    this.apiClientService
      .bonusSuppressionService()
      .getModules()
      .map((response: HttpResponse<IModuleData[]>) => {
        return response.body;
      })
      .subscribe(
        (bonusSupData: IModuleData[]) => {
          this.moduleNames = bonusSupData;
          this.showHideSpinner(false);
          this.initForm();
        },
        (error) => {
          this.errorService.emitError(BONUS_SUPPRESSION_ERROR_LABELS.loadingBonusSupModules);
          this.showHideSpinner(false);
        }
      );
    
  }

  initForm() {
    if( this.modalData.data.dialogType === 'new') {
      this.bonusSupModuleData = {
        brand: this.brandService.brand,
        id: '',
        moduleName: '',
        bonusSuppression: false,
        riskLevelCode: '',
        reasonCode: '',
        modules: []
      }
    } else {
      this.modules = this.modalData.data.dialogData.modules ? cloneDeep(this.modalData.data.dialogData.modules) : [];
      this.bonusSuppression = this.modalData.data.dialogData.enabled;
      this.riskLevelVal = this.modalData.data.dialogData.riskLevelDesc;
      this.reasonCodeVal = this.modalData.data.dialogData.reasonDesc;
      this.bonusSupModuleData = this.modalData.data.dialogData;
    }
  }

  /**
   * Click handler for closing of modal dialog
   */
   closeDialog(): void {
    this.modules = cloneDeep(this.modalData.data.dialogData.modules);
    this.dialogRef.close({closeCallback: true});
  }

  /**
   * Returns the added bonus suppression module instance
   * @returns {IBonusSuppressionModule}
   */
  saveBonusSuppresionModule(): IBonusSuppressionModule {
    Object.assign(this.bonusSupModuleData, {
      brand: this.brandService.brand,
      enabled: this.bonusSuppression,
      riskLevelDesc: this.riskLevelVal,
      reasonDesc: this.reasonCodeVal,
      moduleIds: this.modules.map(item => item.id),
      reasonCode: this.reasonCodeVal.split('-')[0].trim(),
      riskLevelCode: this.riskLevelVal.split('-')[0].trim()
    })
    return this.bonusSupModuleData;
  }

  addModule() {
    this.dataChanged();
    const moduleInfo = this.moduleNames.find(item => (item.id === this.selectedModuleId));
    const existingModule = this.modules.find(module => (module.id === moduleInfo.id));
    if (this.moduleRowId > -1) {
      this.modules[this.moduleRowId] = {
        id: moduleInfo.id,
        moduleName: moduleInfo.moduleName
      }
      this.moduleRowId = undefined
    } else if(!existingModule) {
      this.modules.push({
        id: this.selectedModuleId,
        moduleName: moduleInfo.moduleName
      })
    }

    this.selectedModuleId = ''
  }

  editModule(data, event, index) {
    this.moduleRowId = index
    this.selectedModuleId = this.modules[this.moduleRowId].id
  }

  removeSubModule(data) {
    const index = this.modules.findIndex(item => (item.id === data.id));
    this.modules.splice(index,1);
    this.dataChanged();
  }

  public showHideSpinner(toShow: boolean = true): void {
    toShow
      ? this.globalLoaderService.showLoader()
      : this.globalLoaderService.hideLoader();
  }

  checkButtonEnable() {
    return this.riskLevelVal && this.reasonCodeVal && this.modules.length > 0 && (this.modalData.data.dialogType == 'new' ?  true : this.dataChangedInUpdate)
  }

  dataChanged() {
    this.dataChangedInUpdate = true;
  }
}
