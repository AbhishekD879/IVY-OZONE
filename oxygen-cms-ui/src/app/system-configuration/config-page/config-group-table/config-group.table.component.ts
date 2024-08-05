import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {IConfigGroup} from '../models/IConfigGroup';
import {IConfigItem} from '../models/IConfigItem';
import {ConfigItemType, TypeValues} from '../models/configTypes';

@Component({
  selector: 'config-group-table',
  templateUrl: './config-group.table.component.html',
  styleUrls: ['./config-group.table.component.scss']
})

export class ConfigGroupTableComponent implements OnInit {
  @Output() applyConfigChanges = new EventEmitter();
  @Output() callRemoveConfigGroup = new EventEmitter();
  @Input() configGroup: IConfigGroup;

  // backup items to revert group state after any changes
  configGroupBackup: IConfigGroup;

  // flag after some changes was made in group. enebles save and revert button
  isDataChanged: boolean;

  // flag for viewing "add new item" form
  isAddingItem: boolean = false;

  // ediable state of config group table
  isEditOn: boolean = false;

  // new config property object , before adding to group
  newItem: IConfigItem = {};

  // possible properties types
  typeOptions: Array<string>;

  constructor(private dialogService: DialogService) {}

  toggleTableEdit() {
    this.isEditOn = !this.isEditOn;
  }

  /**
   * Show add new item form and reset new property data.
   */
  startAddingNewItem() {
    this.isAddingItem = true;
    this.newItem = {
      name: '',
      type: ConfigItemType.input,
      value: ''
    };
  }

  isSimpleConfigItemType(configItem) {
    return configItem.type !== 'checkbox' &&
              configItem.type !== 'daterange' &&
              configItem.type !== 'input with multiselect';
  }

  /**
   * Finish adding new item, reset entered new property data.
   */
  finishAddingNewItem() {
    this.isAddingItem = false;
    this.newItem = {
      name: '',
      type: '',
      value: ''
    };
  }

  /**
   * Set new property type
   * @param value
   */
  setItemType(value) {
    this.isDataChanged = true;
    this.newItem.value = '';
    this.newItem.type = ConfigItemType[value];
  }

  /**
   * View information about possible values for chosen property type
   * @param configParamType
   * @returns {any}
   */
  possibleValueFor(configParamType) {
    return TypeValues[configParamType];
  }

  /**
   * transform property name to camelCase. remove all spaces.
   * @param {string} propertyName
   * @return {string}
   */
  textToCamelCase(text: string): string {
    return text.replace(/(\s)(.)|(\s)$/g, function (a, a1, a2) {
      return (a2 && a2.toUpperCase()) || '';
    });
  }

  /**
   * Submit form with new config property.
   */
  submitNewProperty() {
    if (this.isValidConfigProperty(this.newItem)) {
      this.configGroup.items.push(this.newItem);
      this.finishAddingNewItem();
      this.isDataChanged = true;
    }
  }

  /**
   * Look for duplicated properties names in config group
   * @returns {Array<string>}
   */
  duplicatedGroupPropertiesNames(): Array<string> {
    const duplicatedNames = [];

    this.configGroup.items.sort().forEach((configProperty, i) => {
      if (this.configGroup.items[i + 1] && configProperty.name === this.configGroup.items[i + 1].name) {
          if (duplicatedNames.indexOf(configProperty.name) === -1) {
            duplicatedNames.push(configProperty.name);
          }
      }
    });

    return duplicatedNames;
  }

  /**
   * Look for empty property names in group
   * @returns {Array<IConfigItem>}
   */
  emptyGroupPropertiesNames(): Array<IConfigItem> {
    return this.configGroup.items.filter(configProperty => configProperty.name.length === 0);
  }

  // TODO refactor this method
  isGroupValid(): boolean {
    let isValid = true;
    const duplicatedGroupPropertiesNames = this.duplicatedGroupPropertiesNames();
    const emptyGroupPropertiesNames = this.emptyGroupPropertiesNames();

    let errorMessage = '';

    if (duplicatedGroupPropertiesNames.length > 0) {
      isValid = false;
      errorMessage = `Names ${duplicatedGroupPropertiesNames.join(',')} are Duplicated`;
    }

    if (emptyGroupPropertiesNames.length > 0) {
      isValid = false;
      errorMessage = `Group Has Properties With No Name`;
    }

    if (!isValid) {
      this.dialogService.showNotificationDialog({
        title: 'Saving Error',
        message: errorMessage
      });
    }

    return isValid;
  }

  /**
   * Validate property name
   * @param {IConfigItem} property
   * @returns {boolean}
   */
  isNewPropertyNameValid(property: IConfigItem) {
    return property.name && property.name.length > 0 && this.isNewPropertyNameUniq(property.name);
  }

  /**
   * Validate  property when submit new one
   * @param {IConfigItem} property
   * @returns {boolean}
   */
  isValidConfigProperty(property: IConfigItem) {
    return this.isNewPropertyNameValid(property) &&
      property.type && property.type in ConfigItemType &&
      property.value !== undefined;
  }

  /**
   * check unique property name, without case sensitive.
   * @param propName
   * @returns {boolean}
   */
  isNewPropertyNameUniq(propName) {
    return this.configGroup.items.every(item => item.name.toLowerCase() !== propName.toLowerCase());
  }

  /**
   * Datepicker helper funtcion
   * transform readable date to ISOString format
   * @param {date} dateValue - dateString in "shortDate" format
   */
  transformAndSaveDate(dateValue, item) {
    const isoDate = new Date(dateValue).toISOString();
    item.value = isoDate;
    this.isDataChanged = true;
  }

  /**
   * remove property from config group
   * @param itemIndex
   */
  removePropertyFromGroup(itemIndex) {
    let notificationMessage = 'Are You Sure You Want to Remove This Property?';

    if (this.configGroup.items.length === 1) {
      notificationMessage += ' This Will Also Remove Config Group!';
    }

    this.dialogService.showConfirmDialog({
      title: 'Remove Property from Group',
      message: notificationMessage,
      yesCallback: () => {
        this.configGroup.items.splice(itemIndex, 1);
        this.isDataChanged = true;

        // remove group if there is no more properties
        if (this.configGroup.items.length === 0) {
          this.callRemoveConfigGroup.emit(this.configGroup);
        }
      }
    });
  }

  /**
   * Revert changes. got group items from backup and reset main properties array.
   */
  revertGroupChanges() {
    this.dialogService.showConfirmDialog({
      title: 'Cancel All Group Changes',
      message: 'Are You Sure You Want to Revert Group Changes?',
      yesCallback: () => {
        this.configGroup = JSON.parse(JSON.stringify(this.configGroupBackup));
        this.resetEditState();
      }
    });
  }

  /**
   * Save all group changes.
   * renew items in backup for future reverts.
   */
  saveConfigGroupChanges() {
    if (this.isGroupValid()) {
      this.transformRadioAndSelectData();
      this.configGroupBackup = JSON.parse(JSON.stringify(this.configGroup));
      this.applyConfigChanges.emit(this.configGroup);

      this.resetEditState();
    }
  }

  transformRadioAndSelectData() {
    this.configGroup.items.forEach(configItem => {
      if ((configItem.type === 'select' ||
          configItem.type === 'radio' ||
          configItem.type === 'multiselect') &&
        configItem.value.length > 0 && typeof configItem.value === 'string') {
        configItem.value = configItem.value.split(',');
      }
    });
  }

  /**
   * Remove config group.
   */
  removeConfigGroup() {
    this.dialogService.showConfirmDialog({
      title: 'Remove Config Group',
      message: 'Are You Sure You Want to Remove Group? This Action Could Not Be Reverted!',
      yesCallback: () => {
        this.callRemoveConfigGroup.emit(this.configGroup);
      }
    });
  }

  /**
   * Reset flags.
   */
  resetEditState() {
    this.isDataChanged = false;
    this.isAddingItem = false;
    this.isEditOn = false;
  }

  /**
   * main init method.
   * set initial data.
   */
  ngOnInit() {
    this.typeOptions = Object.keys(ConfigItemType);
    this.configGroupBackup = JSON.parse(JSON.stringify(this.configGroup));
    // logic for created new empty group. automatically start adding new item.
    if (!this.configGroup.items || this.configGroup.items.length === 0) {
      this.startAddingNewItem();
    }
  }
}
