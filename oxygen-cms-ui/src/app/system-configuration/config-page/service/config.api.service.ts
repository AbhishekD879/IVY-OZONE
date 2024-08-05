import {Injectable} from '@angular/core';
import {IConfigGroup} from '../models/IConfigGroup';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {ApiClientService} from '../../../client/private/services/http/index';
import {DialogService} from '../../../shared/dialog/dialog.service';

@Injectable()
export class SystemConfigAPIService {
  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,
    private dialogService: DialogService) {
  }

  /**
   * Get configuration data.
   * @returns {Observable<HttpResponse<Brand[]>>}
   */
  getConfigurationData() {
    const getData = this.apiClientService.brandConfig().findAllByBrand();
    return getData;
  }

  /**
   * Save new config group to server.
   * @param {IConfigGroup} configGroup
   */
  postNewGroup(configGroup: IConfigGroup) {
    // API POST CALL
    this.globalLoaderService.showLoader();
    return this.apiClientService
      .brandConfig()
      .postNewSystemConfigurationGroupByBrand(configGroup)
      .subscribe((data) => {
        // LISTEN for GROUP_ID in RESPONSE
        configGroup.id = data.body.id;

        this.globalLoaderService.hideLoader();
        this.dialogService.showNotificationDialog({
          title: 'Config Saved'
        });
      }, (error) => this.handleRequestError(error));
  }

  /**
   * Save present config group changes to server.
   * @param {IConfigGroup} configGroup
   */
  putGroupChanges(configGroup) {
    // API CALL PUT
    this.globalLoaderService.showLoader();
    this.apiClientService
      .brandConfig()
      .putSystemConfigurationGroupUpdateByBrand(configGroup)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();

        this.dialogService.showNotificationDialog({
          title: 'Config Saved'
        });
      }, error => this.handleRequestError(error));
  }

  /**
   * Remove present config group.
   * @param {IConfigGroup} configGroup
   */
  deleteConfigGroup(configGroup) {
    // API CALL DELETE with /configGroup.id
    this.globalLoaderService.showLoader();
    this.apiClientService
      .brandConfig()
      .deleteSystemConfigurationGroupByBrand(configGroup.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.dialogService.showNotificationDialog({
          title: 'Config Saved',
          message: 'Config Group is Removed.'
        });
      }, error => this.handleRequestError(error));
  }

  /**
   * Handle networking error.
   * Notify user.
   */
  handleRequestError(error) {
    this.globalLoaderService.hideLoader();
  }
}
