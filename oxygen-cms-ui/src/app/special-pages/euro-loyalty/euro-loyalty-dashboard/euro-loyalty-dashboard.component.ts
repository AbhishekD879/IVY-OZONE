import { HttpResponse } from '@angular/common/http';
import { Component, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { IConfigGroup, IEuroLoyalty, ITierInfo } from '@app/client/private/models/euroLoyalty.model';
import { ApiClientService } from '@app/client/private/services/http';
import { BrandService } from '@app/client/private/services/brand.service';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { EuroLoyaltyValidationService } from '@app/special-pages/euro-loyalty/euro-loyalty-dashboard/euro-loyalty-dashboard.validation.service';
import {​​​​​​​​ TinymceComponent }​​​​​​​​ from '@app/shared/tinymce/tinymce.component';
import { EuroLoyaltyConstants, EuroLoyaltyValues } from '@app/special-pages/euro-loyalty/euro-loyalty-dashboard/euroLoyalty.constant';
import { SpecialPagesValidationService } from '../../validators/special-pages.validation.service';

@Component({
  selector: 'app-euro-loyalty-dashboard',
  templateUrl: './euro-loyalty-dashboard.component.html',
  styleUrls: ['./euro-loyalty-dashboard.component.scss']
})

export class EuroLoyaltyDashboardComponent implements OnInit {
  public readonly EUROLOYAL = EuroLoyaltyConstants;
  public euroLoyalty: IEuroLoyalty = EuroLoyaltyValues;
  public form: FormGroup;

  public configGroup: IConfigGroup = {
    items: []
  };

  // backup items to revert form state after any changes
  backupEuroLoyalty: IEuroLoyalty = this.euroLoyalty;

  // backup items to revert group state after any changes
  configGroupBackup: IConfigGroup = this.configGroup;

  // flag after some changes was made in group. enables save and revert button
  isDataChanged: boolean;

  // flag for showing max error message
  limitExceeded: boolean = false;

  // flag for viewing "add new item" form
  isAddingItem: boolean = false;

  // flag for saving/updating
  updateForm: boolean = false;

  // flag to hide/show remove button
  deleteButton: boolean;

  // editable state of config group table
  isEditOn: boolean = false;

  // new config property object , before adding to group
  newItem: ITierInfo;

  // possible properties types
  typeOptions: Array<string>;

  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  @ViewChild('howItWorksEditor') howItWorksEditor: TinymceComponent;
  @ViewChild('termsAndConditionsEditor') termsAndConditionsEditor: TinymceComponent;

  constructor(
    private apiClientService: ApiClientService,
    private euroLoyaltyValidationService: EuroLoyaltyValidationService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private brandService: BrandService,
    public specialPagesValidationService: SpecialPagesValidationService
  ) {
      this.isValidForm = this.isValidForm.bind(this);
  }

  ngOnInit(): void {
    this.initForm();
    this.globalLoaderService.showLoader();
    this.loadInitData();
  }

  /**
   * Initializes the form
   * @returns - {void}
   */
  initForm(): void {
    this.form = new FormGroup({
      tierName: new FormControl('', []),
      offerIdSeq: new FormControl('', []),
      freeBetPositionSequence: new FormControl('', []),
      fullTermsURI: new FormControl(this.euroLoyalty.fullTermsURI, []),
      howItWorks: new FormControl(this.euroLoyalty.howItWorks, [
        Validators.minLength(1),
        Validators.required
      ]),
      termsAndConditions: new FormControl(this.euroLoyalty.termsAndConditions, [
        Validators.minLength(1),
        Validators.required])
    });
    this.euroLoyalty.brand = this.brandService.brand;
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
      tierName: '',
      offerIdSeq: '',
      freeBetPositionSequence: ''
    };
  }

  /**
   * Sort the order of locations entered.
   * @param - {string} text
   * @returns - {array} array of sorted locations
   */
  updateLocationOrder(text: string):  number[] {
    const numArray = text.split(',').map(Number);
    return numArray.sort((freebet1, freebet2) => {​
      return freebet1 - freebet2;
    }​);
  }

  /**
   * Submit form with new config property.
   * @returns - {void}
   */
  submitNewProperty(): void {
    this.configGroup.items.push(this.newItem);
    this.updateEuroLoyaltyTierInfo(this.configGroup.items);
    this.sortConfig(this.configGroup.items, this.EUROLOYAL.labels.TierName);
    this.finishAddingNewItem();
    this.isDataChanged = true;

    this.euroLoyalty.tierInfo = this.configGroup.items;
    this.configGroupBackup = JSON.parse(JSON.stringify(this.configGroup));
    this.resetEditState();
  }

  /**
   * Save all group changes.
   * renew items in backup for future reverts.
   * @returns - {void}
   */
  saveConfigGroupChanges(): void {
    let saveChanges: boolean = true;
    this.updateEuroLoyaltyTierInfo(this.configGroup.items);
    this.sortConfig(this.configGroup.items, this.EUROLOYAL.labels.TierName);
    this.configGroup.items.forEach((config: ITierInfo, itemIndex: number) => {
      if (!this.euroLoyaltyValidationService
          .isValidConfigProperty(config, this.specialPagesValidationService
            .isUnique(config.tierName, this.configGroup.items,
              this.EUROLOYAL.labels.TierName, itemIndex))) {
        saveChanges = false;
      }
    });
    if (saveChanges) {
      this.euroLoyalty.tierInfo = this.configGroup.items;
      this.configGroupBackup = JSON.parse(JSON.stringify(this.configGroup));
      this.resetEditState();
    }
  }

  /**
    * remove property from config group
    * @param - {number} itemIndex
    * @returns - {void}
    */
  removePropertyFromGroup(itemIndex: number): void {
    if (this.configGroup.items.length !== 1) {
      const notificationMessage = this.EUROLOYAL.messages.removePropertyPromptMsg;

      this.dialogService.showConfirmDialog({
        title: this.EUROLOYAL.messages.removePropertyTitle,
        message: notificationMessage,
        yesCallback: () => {
          this.configGroup.items.splice(itemIndex, 1);
          this.sortConfig(this.configGroup.items, this.EUROLOYAL.labels.TierName);
          this.euroLoyalty.tierInfo = this.configGroup.items;
          this.isDataChanged = true;
        }
      });
    } else {
      this.isEditOn = true;
    }
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
    this.apiClientService.euroLoyalty()
      .getConfig().map((response: HttpResponse<IEuroLoyalty>) => {
        return response.body;
      }).subscribe((euroLoyalty: IEuroLoyalty) => {
        this.hideLoading();
        if (!euroLoyalty.pageName) {
          this.updateForm = false;
          this.deleteButton = false;
          this.configGroup.items = [];
          this.form.reset();
          this.howItWorksEditor.update('');
          this.termsAndConditionsEditor.update('');
        } else {
          this.updateForm = true;
          this.deleteButton = true;
          this.euroLoyalty = euroLoyalty;
          this.backupEuroLoyalty = JSON.parse(JSON.stringify(this.euroLoyalty));
          this.configGroup.items = this.euroLoyalty.tierInfo;
          this.howItWorksEditor.update(this.euroLoyalty.howItWorks);
          this.termsAndConditionsEditor.update(this.euroLoyalty.termsAndConditions);
        }
      }, (error) => {
        console.error(error.message);
        this.updateForm = true;
        this.hideLoading();
      });
  }

  /**
   * Updates the content in rich text box fields
   * @param - {string} htmlMarkup
   * @param - {string} eventType
   * @returns - {void}
   */
  updateText(htmlMarkup: string, eventType: string): void {
    switch (eventType) {
      case this.EUROLOYAL.labels.HowItWorksText:
        this.euroLoyalty.howItWorks = htmlMarkup;
        break;
      case this.EUROLOYAL.labels.TermsAndConditionsText:
        this.euroLoyalty.termsAndConditions = htmlMarkup;
        break;
      default:
        console.error(this.EUROLOYAL.errors.UnhandledAction);
        break;
    }
  }

  /**
   * Updates the limit exceeds flag
   * @param - {string} msg
   * @returns - {void}
   */
  checkLimit(msg: string): void {
    this.limitExceeded = msg ? true : false;
  }

  /**
   * Action handler to manage save, revert and remove buttons
   * @param - {string} event
   * @returns - {void}
   */
  actionsHandler(event: string): void {
    switch (event) {
      case this.EUROLOYAL.actions.Save:
        this.saveChanges();
        break;
      case this.EUROLOYAL.actions.Revert:
        this.loadBackupForm();
        break;
      case this.EUROLOYAL.actions.Remove:
        this.removeConfig();
        break;
      default:
        console.error(this.EUROLOYAL.errors.UnhandledAction);
        break;
    }
  }

  /**
   * Hides loader
   * @returns - {void}
   */
  hideLoading(): void {
    this.globalLoaderService.hideLoader();
  }

  /**
   * Updates euroloyalty value and checks if updation is required or save
   * @returns - {void}
   */
  saveChanges(): void {
    this.deleteButton = true;
    this.euroLoyalty.tierInfo = this.configGroupBackup.items;
    this.updateForm ? this.updateConfig() : this.saveConfig();
  }

  /**
   * Populates the field with stored euroloyalty data
   * @returns - {void}
   */
  loadBackupForm(): void {
    this.euroLoyalty = this.backupEuroLoyalty;
    this.howItWorksEditor.update(this.euroLoyalty.howItWorks);
    this.termsAndConditionsEditor.update(this.euroLoyalty.termsAndConditions);
  }

  /**
   * Updates the previously saved config
   * @returns - {void}
   */
  updateConfig(): void {
    this.apiClientService.euroLoyalty()
    .updateConfig(this.euroLoyalty)
    .map((response: HttpResponse<IEuroLoyalty>) => {
      return response.body;
    })
    .subscribe((data: IEuroLoyalty) => {
      this.euroLoyalty = data;
      this.actionButtons.extendCollection(this.euroLoyalty);
      this.dialogService.showNotificationDialog({
        title: this.EUROLOYAL.messages.configTitle,
        message: this.EUROLOYAL.messages.configUpdateMsg
      });
    });
  }

  /**
   * Saves the new config
   * @returns - {void}
   */
  saveConfig(): void {
    this.apiClientService.euroLoyalty()
    .saveConfig(this.euroLoyalty)
    .map((response: HttpResponse<IEuroLoyalty>) => {
      return response.body;
    })
    .subscribe((data: IEuroLoyalty) => {
      this.euroLoyalty = data;
      this.actionButtons.extendCollection(this.euroLoyalty);
      this.dialogService.showNotificationDialog({
        title: this.EUROLOYAL.messages.configTitle,
        message: this.EUROLOYAL.messages.configSaveMsg
      });
    });
    this.updateForm = true;
  }

  /**
   * Removes the previously saved config
   * @returns - {void}
   */
  removeConfig(): void {
    this.apiClientService.euroLoyalty()
    .deleteConfig()
    .subscribe(() => {
      this.dialogService.showNotificationDialog({
        title: this.EUROLOYAL.messages.removeConfigTitle,
        message: this.EUROLOYAL.messages.configRemoveMsg
      });
      this.loadInitData();
    });
    this.updateForm =  false;
    this.deleteButton = false;
  }

  /**
   * Validates if required fields are entered
   * @param - {IEuroLoyalty} euroLoyalty
   * @returns - {boolean}
   */
  isValidForm(euroLoyalty: IEuroLoyalty): boolean {
    return !!(euroLoyalty.howItWorks
        && euroLoyalty.termsAndConditions
        && this.configGroupBackup
        && this.configGroupBackup.items
        && this.configGroupBackup.items.length > 0);
  }

  /**
   * Converts freebet location and freebet position sequence into array of numbers
   * @param - {ITierInfo[]} items
   * @returns - {void}
   */
  updateEuroLoyaltyTierInfo(items: ITierInfo[]): void {
    items.forEach((item) => {
      item.offerIdSeq =
        (!Array.isArray(item.offerIdSeq))
        ? item.offerIdSeq.split(',')
          .map(Number)
          .sort((freebet1, freebet2) => {​
            return freebet1 - freebet2;
          }​)
        : item.offerIdSeq;
      item.freeBetPositionSequence =
        (!Array.isArray(item.freeBetPositionSequence))
        ? item.freeBetPositionSequence.split(',')
          .map(Number)
          .sort((freebet1, freebet2) => {​
            return freebet1 - freebet2;
          }​)
        : item.freeBetPositionSequence;
    });
  }

  /**
   * Sorts the array of objects by provided input value
   * @param - {ITierInfo[]} items
   * @param - {string} key
   * @returns - {void}
   */
  sortConfig(items: ITierInfo[], key: string): void {
    items.sort((item1, item2) => (item1[key] > item2[key]) ? 1 : ((item2[key] > item1[key]) ? -1 : 0));
  }
}

