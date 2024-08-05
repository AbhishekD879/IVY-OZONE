import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { BrandService } from '@app/client/private/services/brand.service';
import { DataTableColumn } from '@root/app/client/private/models';
import { ApiClientService } from '@app/client/private/services/http';
import { HttpResponse } from '@angular/common/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ErrorService } from '@app/client/private/services/error.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { BONUS_SUPPRESSION_ERROR_LABELS } from '@app/five-a-side-showdown/constants/contest-manager.constants';
import { IModuleData, ModulesDialogData, SAVE_MODULE_DIALOG, IAliasModuleNamesData, IAliasModulesTagsData } from '../models/module-manager';

@Component({
  selector: 'app-modules-bonus-suppression',
  templateUrl: './modules-bonus-suppression.component.html',
  styleUrls: ['./modules-bonus-suppression.component.scss']
})
export class ModulesBonusSuppressionComponent implements OnInit {

  public moduleName = "";
  private dataChangedInUpdate = false;
  moduleNames: IModuleData[] = [];
  public subModuleRowId;
  public selectedSubModuleId = "";
  public subModules = [];
  public subModuleData: IModuleData;
  public dialogLabels = SAVE_MODULE_DIALOG;
  public filterProperties: Array<string> = ['name'];
  public searchField: string = '';
  public moduleListColumns: Array<DataTableColumn> = [
    {
      name: 'Module Name',
      property: 'moduleName',
      type: 'custom',
      customOnClickHandler: (colData, value, index) => {
        this.editSubModule(colData, value, index)
      }
    },
  ];
  aliasModules: IAliasModulesTagsData[];
  aliasModuleIds: any[];
  subModuleEnabled: boolean = false;
  selectedValues = [];
  UserDataValue: any[] = [];;
  dataLoading: boolean = true

  constructor(@Inject(MAT_DIALOG_DATA) public modalData: ModulesDialogData,
    private brandService: BrandService,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private errorService: ErrorService,
    private dialogRef: MatDialogRef<ModulesBonusSuppressionComponent>) { }

  ngOnInit(): void {
    this.initForm();
  }

  addTagFn = (name) => {
    var matched = this.UserDataValue.filter(aliasName => {
      if (aliasName.title.toLowerCase().split(':')[1] === name.toLowerCase())
        return aliasName;
    });
    if (matched.length > 0)
      return false;
    else {
      this.aliasModules.push({ id: '', title: name, addTag: true });
      return { id: '', title: name, addTag: true };
    }
  }

  initForm() {
    this.moduleNames = this.modalData.data.dialogData.modules;
    this.aliasModules = [];
    this.getAliasModulesNameData();
    if (this.modalData.data.dialogType === 'new') {
      this.subModuleData = {
        brand: this.brandService.brand,
        id: '',
        moduleName: '',
        aliasModuleNames:'',
        aliasModules: this.aliasModules,
        subModuleEnabled: false,
        subModules: []
      }
    } else {
      this.moduleName = this.modalData.data.dialogData.moduleName;
      this.modalData.data.dialogData.aliasModules.forEach(a => (a.id == null) ? a.id = ('custom_' + a.title) : true);
      this.aliasModuleIds = this.modalData.data.dialogData.aliasModules.map(a => a.id);
      this.subModuleEnabled = this.modalData.data.dialogData.subModuleEnabled;
      this.subModuleData = this.modalData.data.dialogData
      this.subModules = this.modalData.data.dialogData.subModules ? JSON.parse(JSON.stringify(this.modalData.data.dialogData.subModules)) : [];
    }
  }

  /**
   * Returns the added module instance
   * @returns {IModuleData}
   */
  saveModule(): IModuleData {
    Object.assign(this.subModuleData, {
      moduleName: this.moduleName,
      aliasModules: this.aliasModules.concat(this.UserDataValue.filter(aliasName => {
        if (this.aliasModuleIds && this.aliasModuleIds.indexOf(aliasName.id) >= 0)
          return aliasName;
      }).map(alias => {
        var cust = { id: (alias.id.indexOf('custom_') < 0 ? alias.id : null), title: alias.title, addTag: alias.addTag };
          return cust;
      })),
      subModuleEnabled: this.subModuleEnabled,
      subModuleIds: this.subModules.map(item => item.id)
    })
    delete this.subModuleData.modules
    return this.subModuleData;
  }

  /**
   * Click handler for closing of modal dialog
   */
  closeDialog(): void {
    if (this.checkButtonEnable()) {
      this.dialogService.showConfirmDialog({
        title: 'Cancelation',
        message: 'Are you sure,You do not want to change anything?',
        yesCallback: () => {
          this.dialogRef.close({ closeCallback: true });
          this.showHideSpinner(false);
        }
      });
    }
    else {
      this.dialogRef.close({ closeCallback: true });
    }
  }

  createSubModule() {
    this.dataChanged();
    const moduleInfo = this.moduleNames.filter(item => (item.id === this.selectedSubModuleId));
    if (this.subModuleRowId > -1) {
      this.subModules[this.subModuleRowId] = {
        id: moduleInfo[0].id,
        moduleName: moduleInfo[0].moduleName
      }
      this.subModuleRowId = undefined
    } else {
      this.subModules.push({
        id: this.selectedSubModuleId,
        moduleName: moduleInfo[0].moduleName
      })
    }
    this.selectedSubModuleId = "";
  }

  editSubModule(data, event, index) {
    this.subModuleRowId = index
    this.selectedSubModuleId = this.subModules[this.subModuleRowId].id
  }

  removeSubModule(data) {
    const index = this.subModules.findIndex(item => (item.name === data.name));
    this.subModules.splice(index, 1);
    this.dataChanged();
  }

  checkButtonEnable() {
    return this.moduleName && (this.subModuleEnabled ? this.subModules.length > 0 : true) && (this.modalData.data.dialogType == 'new' ? true : this.dataChangedInUpdate)
  }

  dataChanged() {
    this.dataChangedInUpdate = true;
  }

  dataSelectChanged() {
    this.dataChanged();
  }

  public showHideSpinner(toShow: boolean = true): void {
    toShow
      ? this.globalLoaderService.showLoader()
      : this.globalLoaderService.hideLoader();
    this.dataLoading = toShow;
  }

  /**
* Load the alias modules for the Bonus Suppression module
*/
  private getAliasModulesNameData() {
    this.showHideSpinner();
    this.apiClientService
      .bonusSuppressionService()
      .getAliasModulesName()
      .map((response: HttpResponse<IAliasModuleNamesData[]>) => {
        return response.body;
      })
      .subscribe(
        (aliasNamesData: IAliasModuleNamesData[]) => {
          Object.keys(aliasNamesData).forEach(key => {
            aliasNamesData[key].forEach(aliasName => {
              aliasName.title = key + ":" + aliasName.title;
              this.UserDataValue.push(aliasName);
            })
          });
          this.showHideSpinner(false);
          if(this.modalData.data.dialogData.aliasModules){
            var customValues = this.modalData.data.dialogData.aliasModules.filter(a => {
              if (!this.UserDataValue.some(({ id }) => id == a.id))
                return a;
            });
            this.UserDataValue = this.UserDataValue.concat(customValues);
        }

        },
        (error) => {
          this.errorService.emitError(BONUS_SUPPRESSION_ERROR_LABELS.loadingBonusSupModules);
          this.showHideSpinner(false);
        }
      );
  }

}
