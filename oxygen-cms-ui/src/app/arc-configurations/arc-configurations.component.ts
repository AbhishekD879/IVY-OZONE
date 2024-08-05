import { HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { IArcConfig, ISportAction, IARC, IMasterGroup, ILink, IValues } from '@app/client/private/models/arcConfig.model';
import { ApiClientService } from '@app/client/private/services/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ArcConfigurationConstants, ArcConfigurationValues } from '@app/arc-configurations/arc-configuration.constant';
import { BrandService } from '@app/client/private/services/brand.service';
import { ArcSportActionsPopUpComponent } from '@app/arc-configurations/arc-sport-actions-pop-up/arc-sport-actions-pop-up.component';
import { MatDialog } from '@angular/material/dialog';
import { AppConstants } from '@app/app.constants';

@Component({
  selector: 'app-arc-configurations',
  templateUrl: './arc-configurations.component.html',
  styleUrls: ['./arc-configurations.component.scss']
})

export class ArcConfigurationsComponent implements OnInit {

  public readonly ARCCONFIG = ArcConfigurationConstants;
  public arcConfigValues: IARC = ArcConfigurationValues;
  public form: FormGroup;
  public links: ILink[];

  public configGroup: IARC = {
    items: []
  };
  isDataChanged: boolean = false;
  isAddingItem: boolean = false;
  isEditOn: boolean = false;
  addArc: boolean = false;
  newItem: IArcConfig;
  MROptions: Array<string>;
  MOHOptions: Array<string>;
  SportOptions: Array<ISportAction>;

  constructor(
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private brandService: BrandService,
    private dialog: MatDialog,
  ) {
    this.links = [{
      label: this.ARCCONFIG.labels.arcconfguration,
      path: '/arc-configurations'
    }];
  }

  ngOnInit(): void {
    this.initForm();
    this.globalLoaderService.showLoader();
    this.getData();
    this.loadInitData();
  }
  /**
   * Initializes the form
   * @returns - {void}
   */
  initForm(): void {
    this.form = new FormGroup({
      profile: new FormControl('', []),
      modelRiskLevel: new FormControl('', []),
      reasonCode: new FormControl('', []),
      sportsActions: new FormControl('', []),
      frequency: new FormControl('', [])
    });
  }
  /**
   * @returns void
   */
  getData(): void {
    this.apiClientService.arcConfig().
      getMasterData().map((response: HttpResponse<IMasterGroup[]>) => response.body)
      .subscribe((masterDatavalue: IMasterGroup[]) => {
       masterDatavalue.find(x => {
        if (x.masterLineName === 'modelRiskLevel') {
          this.MROptions = x.values.map((MRValues: IValues) => (MRValues.id + ' - ' + MRValues.name));
        }
        if (x.masterLineName === 'reasonCodes') {
          this.MOHOptions = x.values.map((MOHValues: IValues) => (MOHValues.id + ' - ' + MOHValues.name));
        }
        if (x.masterLineName === 'sportActions') {
          const sportAction = x.values.map((sportValues: IValues) => ({ 'action': sportValues.name, 'messagingContent': '', gcLink: '', 'enabled': false }));
          this.SportOptions = sportAction.splice(4, 2);
        }
      });
      }, (error) => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  /**
   * Toggle editing option.
   * @returns - {void}
   */
  toggleTableEdit(): void {
    this.isEditOn = !this.isEditOn;
  }
  /**
   * Show add new item form and reset new property data.
   * @returns - {void}
   */
  startAddingNewItem(): void {
    this.updateNewItem(true);
  }
  /**
   * Finish adding new item, reset entered new property data.
   * @returns - {void}
   */
  finishAddingNewItem(): void {
    this.updateNewItem(false);
  }
  /**
  * Update the flag in new item
  * @param - {boolean} flag
  * @returns - {void}
  */
  updateNewItem(flag: boolean): void {
    this.isAddingItem = flag;
    this.newItem = {
      profile: '',
      modelRiskLevel: '',
      reasonCode: '',
      sportsActions: [],
      frequency: '0',
      enabled: false,
      brand: this.brandService.brand,
    };
  }
  /**
   * Submit form with new config property.
   * @returns - {void}
   */
  submitNewProperty(): void {
    this.configGroup.items.push(this.newItem);
    this.finishAddingNewItem();
    this.isDataChanged = true;
    this.addArc = true;
    this.arcConfigValues.items = this.configGroup.items;
    this.resetEditState();
  }
  /**
   * Save all group changes.
   * renew items in backup for future reverts.
   * @returns - {void}
   */
  saveConfigGroupChanges(): void {
    this.arcConfigValues.items = this.configGroup.items;
    this.addArc = true;
    this.resetEditState();
  }
  /**
   * @returns boolean
   */
  isEmpty(): boolean {
    return this.arcConfigValues.items.some((arcConfigValue: IArcConfig) => arcConfigValue.frequency === '');
  }
  
  /**
   * Reset flags.
   * @returns - {void}
   */
  resetEditState(): void {
    this.isDataChanged = false;
    this.isAddingItem = false;
    this.isEditOn = false;
  }

  /**
   * Load data on page load
   * @returns - {void}
   */
  loadInitData(): void {
    this.apiClientService.arcConfig()
      .getConfig().map((response: HttpResponse<IArcConfig[]>) => response.body)
      .subscribe((arcConfigValues: IArcConfig[]) => {
        this.globalLoaderService.hideLoader();
        if (!arcConfigValues) {
          this.configGroup.items = [];
          this.form.reset();
        } else {
          this.arcConfigValues.items = arcConfigValues;
          this.arcConfigValues.items.map((arcConfigValue: IArcConfig) => {
            arcConfigValue.reasonCode = this.MOHOptions.filter((MOHValues) => Number(MOHValues.split(' - ')[0]) === Number(arcConfigValue.reasonCode))[0];
            arcConfigValue.modelRiskLevel = this.MROptions.filter((MRValues) => Number(MRValues.split(' - ')[0]) === Number(arcConfigValue.modelRiskLevel))[0];
          });
          this.configGroup.items = this.arcConfigValues.items;
        }
      }, (error) => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }
  /**
   * Saves the new config
   * @returns - {void}
   */
  saveChanges(): void {
    this.arcConfigValues.items.map((arcConfigValue: IArcConfig) => {
      arcConfigValue.reasonCode = Number(arcConfigValue.reasonCode.toString().split(' - ')[0]);
      arcConfigValue.modelRiskLevel = Number(arcConfigValue.modelRiskLevel.toString().split(' - ')[0]);
    });
    this.apiClientService.arcConfig()
      .updateConfig(this.arcConfigValues.items)
      .subscribe(() => {
        this.loadInitData();
        this.dialogService.showNotificationDialog({
          title: this.ARCCONFIG.messages.configTitle,
          message: this.ARCCONFIG.messages.configSaveMsg
        });
      });
    this.addArc = false;
  }
  /**
   * Removes the previously saved config
   * @returns - {void}
   */
  removeConfig(arcRemove: IArcConfig): void {
    this.dialogService.showConfirmDialog({
      title: this.ARCCONFIG.messages.removePropertyTitle,
      message: this.ARCCONFIG.messages.removePropertyPromptMsg,
      yesCallback: () => {
        const test = arcRemove.modelRiskLevel.toString().split(' - ')[0] + '/' + arcRemove.reasonCode.toString().split(' - ')[0];
        this.apiClientService.arcConfig().deleteConfig(test).subscribe(() => {
          this.loadInitData();
        });
      }
    });
  }
  /**
   * @param  {IArcConfig} property
   * @returns boolean
   */
  isValidConfigProperty(property: IArcConfig): boolean {
    return property.reasonCode.toString().length > 0 && property.modelRiskLevel.toString().length > 0 && !this.isUnique() && property.frequency.length > 0;
  }
  /**
   * @param  {string} profile
   * @param  {IArcConfig[]} objectItems
   * @param  {number} index?
   * @returns boolean
   */
  isUnique(): boolean {
    const test = this.autoProfile();
    return test === '.' || this.arcConfigValues.items.some((arcValue: IArcConfig) => arcValue.profile === test);
  }



  /**
   * @param  {ISportAction[]} sport
   * @returns any
   */
  joinActions(sport: ISportAction[]): any {
    return sport.map((items) => items.action);
  }

  /**
   * @param  {ISportAction[]} sportAction
   */
  openSportConfig(sportAction: ISportAction[]) {
    this.dialog.open(ArcSportActionsPopUpComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: { sports: sportAction, sportsArray: JSON.parse(JSON.stringify(this.SportOptions)) }
    });
  }

  /**
   * @returns string
   */
  autoProfile(): string {
    this.newItem.profile = (this.newItem.modelRiskLevel.toString()).split(' - ')[0] + '.'
      + (this.newItem.reasonCode.toString()).split(' - ')[0];
    return this.newItem.profile;
  }


}