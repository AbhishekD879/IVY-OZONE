import {Component, OnInit} from '@angular/core';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {IConfigData} from '../models/IConfigData';
import {IConfigGroup} from '../models/IConfigGroup';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {SystemConfigAPIService} from '../service/config.api.service';
import {ControlParams} from '@app/client/private/models/dialog.model';

@Component({
  selector: 'app-config-page',
  templateUrl: './config.page.component.html',
  styleUrls: ['./config.page.component.scss'],
  providers: [SystemConfigAPIService]
})
export class ConfigPageComponent implements OnInit {
  /**
   * main config object
   */
  public configData: IConfigData;

  /**
   * config groups
   */
  public configGroupsArray;

  /**
   * loading data flag
   */
  public isLoading: boolean;

  /**
   * Group search string
   * @type {string}
   */
  public searchField: string = '';

  /**
   * Temporary store new created groups to send POST request to server.
   * @type {array[]}
   */
  public newGroups: Array<IConfigGroup> = [];

  constructor(
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private systemConfigAPIService: SystemConfigAPIService
  ) {}

  /**
   * Create new group empty object
   * add it to groups list
   */
  createNewConfigGroup() {
    const newGroup = {
      id: null,
      name: '',
      items: [],
      initialDataConfig: true
    };

    this.dialogService.showPromptDialog({
      width: '325px',
      title: 'Add New Config Group',
      controls: [
        {
          name: 'groupName',
          type: 'text',
          value: newGroup.name,
          label: 'Group Name',
          required: true
        },
        {
          name: 'initialDataConfig',
          type: 'checkbox',
          value: newGroup.initialDataConfig,
          label: 'Initial'
        }
      ],
      hint: `"Initial" checkbox should be used to include/exclude config from /initial-data response.`,
      yesCallback: data => {
        // check group name for uniqueness
        const newGroupName = this.getControlValue(data, 'groupName');
        if (!this.isGroupNameValid(newGroupName)) {
          return this.dialogService.showNotificationDialog({
            title: 'Group Add Error',
            message: 'Group Name Should Not Contain Special Characters and Should Be Unique.',
            closeCallback: () => {
              this.createNewConfigGroup();
            }
          });
        }

        newGroup.name = newGroupName;
        newGroup.initialDataConfig = this.getControlValue(data, 'initialDataConfig');
        this.configGroupsArray.unshift(newGroup);
        this.newGroups.push(newGroup);
      }
    });
  }

  /**
   * Get control value after submitting
   * @returns {any}
   */
  getControlValue(data: Array<ControlParams>, name: string) {
    const field = data.find(item => item.name === name);
    return field && field.value;
  }

  /**
   * Validate group name during creation
   * @param groupName
   * @returns {any | boolean}
   */
  isGroupNameValid(groupName) {
    return groupName && groupName.length > 0 &&
      this.isGroupNameUniq(groupName) &&
      this.notContainSpecialCharacters(groupName);
  }

  /**
   * group name should not contain any special character
   * @param groupName
   * @returns {boolean}
   */
  notContainSpecialCharacters(groupName) {
    return !groupName.match(/[`~!@#$%^&*()|+\-=?;:'".,<>\{\}\[\]\\\/]/gi);
  }

  /**
   * group name should be unique
   * @param groupName
   */
  isGroupNameUniq(groupName) {
    return this.configGroupsArray.every(item => item.name.toLowerCase() !== groupName.toLowerCase());
  }

  /**
   * Groups list to view on page
   * could be filtered with search bar.
   * @returns {any}
   */
  public get configGroupsList() {
    if (this.searchField.length > 0) {
      return this.configGroupsArray.filter((item) => {
        return ~item.name.toLowerCase().indexOf(this.searchField.toLowerCase());
      });
    } else {
      return this.configGroupsArray;
    }
  }

  /**
   * Is group was not saved before.
   * @param {IConfigGroup} configGroup
   * @returns {boolean}
   */
  isNewGroup(configGroup: IConfigGroup) {
    return this.newGroups.some(group => group.name.toLowerCase() === configGroup.name.toLowerCase());
  }

  /**
   * New group will be not "new" after first update,
   * so next updates will be as PUT instead of POST.
   * @param configGroup
   */
  removeNewGroup(configGroup) {
    const index = this.newGroups.indexOf(configGroup);
    if (index !== -1) {
      this.newGroups.splice(index, 1);
    }
  }

  /**
   * Apply changes after changing Group.
   * save data to server
   */
  applyConfigGroupChanges(configGroup: IConfigGroup) {
    if (this.isNewGroup(configGroup)) {
      this.removeNewGroup(configGroup);
      return this.systemConfigAPIService.postNewGroup(configGroup);
    } else if (configGroup.id !== null && configGroup.id !== undefined) {
      this.systemConfigAPIService.putGroupChanges(configGroup);
    } else {
      this.dialogService.showNotificationDialog({
        title: 'Save error',
        message: 'Config Group Won`t Be Saved'
      });
    }
  }

  /**
   * Remove group from main list and send DELETE request.
   * @param {IConfigGroup} configGroup
   */
  callRemoveConfigGroup(configGroup: IConfigGroup) {
    const index = this.configGroupsArray.indexOf(configGroup);

    if (index !== -1 && configGroup.id) {
      // remove group from groups array
      this.configGroupsArray.splice(index, 1);

      // make request
      this.systemConfigAPIService.deleteConfigGroup(configGroup);
    } else if (index !== -1 && !configGroup.id) {
      // remove group from groups array
      this.configGroupsArray.splice(index, 1);
    } else {
      this.dialogService.showNotificationDialog({
        title: 'Config Save Error',
        message: 'Couldn`t Find Group to Remove, Please Reload Page and Try Again.'
      });
    }
  }

  /**
   * initial method. get load from server
   */
  ngOnInit() {
    this.isLoading = true;
    this.globalLoaderService.showLoader();
    this.systemConfigAPIService.getConfigurationData()
      .map((data: any) => {
        data.body.config
          .sort((a, b) => {
            if (a.initialDataConfig === b.initialDataConfig) {
              return a.name < b.name ? -1 : 1;
            } else {
              return a.initialDataConfig ? -1 : 1;
            }
          });
        return data;
      })
      .subscribe((data: any) => {
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
        // main config object
        this.configData = data.body;

        // config groups list
        this.configGroupsArray = data.body.config;
      }, () => {
        this.isLoading = false;
        this.globalLoaderService.hideLoader();
      });
  }
}
