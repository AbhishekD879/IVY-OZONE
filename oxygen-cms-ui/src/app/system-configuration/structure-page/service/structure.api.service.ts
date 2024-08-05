import { Injectable } from '@angular/core';
import { GlobalLoaderService } from '../../../shared/globalLoader/loader.service';
import { ApiClientService } from '../../../client/private/services/http/index';
import { DialogService } from '../../../shared/dialog/dialog.service';
import { forkJoin } from 'rxjs/observable/forkJoin';

@Injectable()
export class ConfigStructureAPIService {
  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,
    private dialogService: DialogService) {
  }

  /**
   * Get configuration data.
   * @returns {Observable<HttpResponse<Brand[]>>}
   */
  getStructureData() {
    const getData = forkJoin([
      this.apiClientService.publicApi().getSystemConfigByBrand(),
      this.apiClientService.brandConfig().findAllByBrand()
    ]);
    return getData;
  }

  /**
   * Save new config group to server.
   * @param {IConfigGroup} configGroup
   */
   saveConfigStructure(configStructure) {
    this.globalLoaderService.showLoader();

    this.apiClientService
      .brandConfig()
      .saveSystemConfigurateByBrand(configStructure)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();

        this.dialogService.showNotificationDialog({
          title: 'System Configuration Setup',
          message: 'Config is Saved.'
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
