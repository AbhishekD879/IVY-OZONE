import { HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ApiClientService } from '@app/client/private/services/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { IBonusSuppressionModule , SAVE_MODULE_DIALOG } from '../models/module-manager';
import { ErrorService } from '@app/client/private/services/error.service';
import { BONUS_SUPPRESSION_ERROR_LABELS } from '@app/five-a-side-showdown/constants/contest-manager.constants';
import { AppConstants } from '@root/app/app.constants';
import { AddEditBonusSuppressionModulesComponent } from '../add-edit-bonus-suppression-modules/add-edit-bonus-suppression-modules.component';
import { DataTableColumn } from '@root/app/client/private/models';

@Component({
  selector: 'app-manage-bonus-suppression-modules',
  templateUrl: './manage-bonus-suppression-modules.component.html',
  styleUrls: ['./manage-bonus-suppression-modules.component.scss']
})
export class ManageBonusSuppressionModulesComponent implements OnInit {

  public moduleList: IBonusSuppressionModule[] = [];

  // public subModuleList: SubModule[] = [];

  public searchField:string = '';

  public bonusSuppressionGlobalToggle: boolean;

  public moduleListColumns: Array<DataTableColumn> = [
    // {
    //   name: 'Module Name',
    //   property: 'id',
    //   type: 'custom',
    //   customOnClickHandler: (colData) => {
    //     this.editBonusSupModule(colData)
    //   }
    // },
    {
      name: 'Risk Level',
      property: 'riskLevelDesc',
      type: 'custom',
      customOnClickHandler: (colData) => {
        this.editBonusSupModule(colData)
      }
    },
    {
      name: 'Reason Code',
      property: 'reasonDesc',
      type: 'custom',
      customOnClickHandler: (colData) => {
        this.editBonusSupModule(colData)
      }
    },
    {
      name: 'Enabled',
      property: 'enabled',
      type: 'boolean'
    }
  ];

  public filterProperties: Array<string> = [
    'riskLevelDesc', 'reasonDesc'
  ];

  constructor(private globalLoaderService: GlobalLoaderService,
              private dialogService: DialogService,
              private apiClientService: ApiClientService,
              private errorService: ErrorService
              ) { }

  ngOnInit(): void {
    this.getBonusSuppressionModules();
    this.getGlobalSwitchData();
  }

  /**
   * Load the modules for the Bonus Suppression Manager
   */
  private getBonusSuppressionModules() {
    this.showHideSpinner();
    this.apiClientService
      .bonusSuppressionService()
      .getAllBonusSuppresionModules()
      .map((response: HttpResponse<IBonusSuppressionModule[]>) => {
        return response.body;
      })
      .subscribe(
        (bonusSupData: IBonusSuppressionModule[]) => {
          this.moduleList = bonusSupData;
          // this.bonusSuppressionGlobalToggle = bonusSupData.globalBonusSuppresion;
          this.showHideSpinner(false);
        },
        (error) => {
          this.errorService.emitError(BONUS_SUPPRESSION_ERROR_LABELS.loadingBonusSupModules);
          this.showHideSpinner(false);
        }
      );
  }

  /**
   * Click handler for the contest creation
   */
   createBonusSuppression(): void {
    this.dialogService.showCustomDialog(AddEditBonusSuppressionModulesComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: SAVE_MODULE_DIALOG.title,
      yesOption: SAVE_MODULE_DIALOG.yesOption,
      noOption: SAVE_MODULE_DIALOG.noOption,
      data: { dialogType: 'new', dialogData: {} },
      yesCallback: (data: IBonusSuppressionModule) => {
        this.showHideSpinner();
        this.apiClientService
          .bonusSuppressionService()
          .createBonusSuppresionModule(data)
          .map((response: HttpResponse<IBonusSuppressionModule>) => {
            return response.body;
          })
          .subscribe(
            (savedcontest: IBonusSuppressionModule) => {
              this.showHideSpinner(false);
              this.getBonusSuppressionModules();
            },
            (error) => {
              this.showHideSpinner(false);
              this.errorService.emitError(
                BONUS_SUPPRESSION_ERROR_LABELS.createBonusSupModule
              );
            }
          );
      },
      noCallback: () => {}
    });
  }

  editBonusSupModule(colData: IBonusSuppressionModule) {
    this.dialogService.showCustomDialog(AddEditBonusSuppressionModulesComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: SAVE_MODULE_DIALOG.title,
      yesOption: SAVE_MODULE_DIALOG.yesOption,
      noOption: SAVE_MODULE_DIALOG.noOption,
      data: { dialogType: 'edit', dialogData: colData },
      yesCallback: (data: IBonusSuppressionModule) => {
        this.showHideSpinner();
        this.apiClientService
          .bonusSuppressionService()
          .updateBonusSuppresionModuleByID(colData.id, colData)
          .map((response: HttpResponse<IBonusSuppressionModule>) => {
            return response.body;
          })
          .subscribe(
            (savedcontest: IBonusSuppressionModule) => {
              this.showHideSpinner(false);
              this.getBonusSuppressionModules();
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
      title: 'Remove Configuration',
      message: 'Are You Sure You Want to Remove Configuration?',
      yesCallback: () => {
        this.showHideSpinner();
        this.apiClientService
          .bonusSuppressionService()
          .deleteBonusSuppresionModuleByID(data.id)
          .map((response: HttpResponse<void>) => {
            return response.body;
          })
          .subscribe(
            (data: any) => {
              this.showHideSpinner(false);
              this.getBonusSuppressionModules();
              this.dialogService.showNotificationDialog({
                title: 'Remove Completed',
                message: 'Configuration is Removed.'
              });
            },
            (error) => {
              this.showHideSpinner(false);
              this.errorService.emitError(
                BONUS_SUPPRESSION_ERROR_LABELS.removingBonusSupModule
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

  private getGlobalSwitchData() {
    this.apiClientService
      .bonusSuppressionService()
      .getGlobalSwitch()
      .map((response: HttpResponse < void > ) => {
        return response.body;
      })
      .subscribe(
        (data: any) => {
          this.bonusSuppressionGlobalToggle = data.rgyEnabled;
        },
        (error) => {
        }
      );
  }
  public toggleGlobalSwitch() {
    this.apiClientService
      .bonusSuppressionService()
      .toggleGlobalSwitch(!this.bonusSuppressionGlobalToggle)
      .map((response: HttpResponse < void > ) => {
        return response.body;
      })
      .subscribe(
        (data: any) => {
          this.bonusSuppressionGlobalToggle = data.rgyEnabled;
        },
        (error) => {
        }
      );
  }
}
