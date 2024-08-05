import { HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ApiClientService } from '@app/client/private/services/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { IModuleData, SAVE_MODULE_DIALOG } from '../models/module-manager';
import { AppConstants } from '@app/app.constants';
import { DataTableColumn } from '@app/client/private/models';
import { ModulesBonusSuppressionComponent } from '../modules-bonus-suppression/modules-bonus-suppression.component';
import { ErrorService } from '@app/client/private/services/error.service';
import { BONUS_SUPPRESSION_ERROR_LABELS } from '@root/app/five-a-side-showdown/constants/contest-manager.constants';

@Component({
  selector: 'app-modules-configuration',
  templateUrl: './modules-configuration.component.html',
  styleUrls: ['./modules-configuration.component.scss']
})
export class ModulesConfigurationComponent implements OnInit {

  public moduleList: IModuleData[] = [];

  public searchField: string = '';

  public moduleListColumns: Array<DataTableColumn> = [
    {
      name: 'Module Name',
      property: 'moduleName',
      type: 'custom',
      customOnClickHandler: (colData) => {
        this.editModule(colData)
      }
    },
    {
      name: 'Alias Module Names',
      property: 'aliasModuleDisplayNames'
    },
    {
      name: 'Sub Modules Enabled',
      property: 'subModuleEnabled',
      type: 'boolean'
    }
  ];

  public filterProperties: Array<string> = [
    'name'
  ];

  constructor(private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private apiClientService: ApiClientService,
    private errorService: ErrorService
  ) { }

  ngOnInit(): void {
    this.getModules();
  }

  /**
   * Load the modules for the Bonus Suppression Manager
   */
  private getModules() {
    this.showHideSpinner();
    this.apiClientService
      .bonusSuppressionService()
      .getModules()
      .map((response: HttpResponse<IModuleData[]>) => {
        return response.body;
      })
      .subscribe(
        (bonusSupData: IModuleData[]) => {
          this.moduleList = bonusSupData;
          bonusSupData.forEach((b: any) => b.aliasModuleDisplayNames = b.aliasModules.map((alias: any) => {
            return alias.title;
          }));
          this.showHideSpinner(false);
        },
        (error) => {
          this.errorService.emitError(BONUS_SUPPRESSION_ERROR_LABELS.loadingBonusSupModules);
          this.showHideSpinner(false);
        }
      );
  }

  editModule(colData: IModuleData) {
    colData.modules = this.moduleList
    this.dialogService.showCustomDialog(ModulesBonusSuppressionComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: SAVE_MODULE_DIALOG.updateTitle,
      yesOption: SAVE_MODULE_DIALOG.yesOption,
      noOption: SAVE_MODULE_DIALOG.noOption,
      data: { dialogType: 'edit', dialogData: colData },
      yesCallback: (data: IModuleData) => {
        this.showHideSpinner();
        this.apiClientService
          .bonusSuppressionService()
          .updateModule(colData.id, data)
          .map((response: HttpResponse<IModuleData>) => {
            return response.body;
          })
          .subscribe(
            (savedcontest: IModuleData) => {              
              this.showHideSpinner(false);
              this.getModules();
              this.dialogService.showNotificationDialog({
                title: 'Successfully Updated!',
                message: 'Bonus Suppression Module is Updated Successfully.'
              });
            },
            (error) => {
              this.showHideSpinner(false);
              this.errorService.emitError(
                BONUS_SUPPRESSION_ERROR_LABELS.editingBonusSupModule
              );
            }
          );
      },
      noCallback: () => {}
    });
  }

  createBonusSupModule(): void {
    this.dialogService.showCustomDialog(ModulesBonusSuppressionComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: SAVE_MODULE_DIALOG.title,
      yesOption: SAVE_MODULE_DIALOG.yesOption,
      noOption: SAVE_MODULE_DIALOG.noOption,
      data: { dialogType: 'new', dialogData: { modules: this.moduleList } },
      yesCallback: (data: IModuleData) => {
        this.showHideSpinner();
        this.apiClientService
          .bonusSuppressionService()
          .createModule(data)
          .map((response: HttpResponse<IModuleData>) => {
            return response.body;
          })
          .subscribe(
            (savedcontest: IModuleData) => {
              this.showHideSpinner(false);
              this.getModules();
              this.dialogService.showNotificationDialog({
                title: 'Successfully Saved!',
                message: 'Bonus Suppression Module is Saved Successfully.'
              });
            },
            (error) => {
              this.showHideSpinner(false);
              this.errorService.emitError(
                BONUS_SUPPRESSION_ERROR_LABELS.editingBonusSupModule
              );
            }
          );
      },
      noCallback: () => {}
    });
  }

  removeModule(data) {
    this.dialogService.showConfirmDialog({
      title: 'Remove Module',
      message: 'Are You Sure You Want to Remove Module?',
      yesCallback: () => {
        this.showHideSpinner();
        this.apiClientService
          .bonusSuppressionService()
          .removeModuleById(data.id)
          .map((response: HttpResponse<void>) => {
            return response.body;
          })
          .subscribe(
            (data: any) => {
              this.showHideSpinner(false);
              this.getModules();
              this.dialogService.showNotificationDialog({
                title: 'Remove Completed',
                message: 'Module is Removed.'
              });
            },
            (error) => {
              this.showHideSpinner(false);
              this.errorService.emitError(
                BONUS_SUPPRESSION_ERROR_LABELS.editingBonusSupModule
              );
            }
          );
      }
    });
  }

  public showHideSpinner(toShow: boolean = true): void {
    toShow
      ? this.globalLoaderService.showLoader()
      : this.globalLoaderService.hideLoader();
  }

}
