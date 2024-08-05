import { Component, OnInit, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';
import { ApiClientService } from '@app/client/private/services/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { BrandService } from '@app/client/private/services/brand.service';
import { INetworkWIndicator, NETWORK_INDICATOR_DEFAULT_VALUS } from './network-indicator-model';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';

@Component({
  selector: 'network-indicator',
  templateUrl: './network-indicator.component.html',

})
export class NetworkIndicatorComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  @ViewChild('NetworkIndiForm') NetworkIndiForm: NgForm;
  networkIndicator: INetworkWIndicator;


  constructor(private apiService: ApiClientService,
    private dialogService: DialogService,
    private brandService: BrandService) { }

  ngOnInit(): void {
    this.loadInitialData();
    this.networkIndicator = NETWORK_INDICATOR_DEFAULT_VALUS;
  }

  private loadInitialData(): void {
    this.apiService.networkIndicatorService()
      .getDetailsByBrand()
      .subscribe((data: { body: INetworkWIndicator }) => {
        this.networkIndicator = data.body;
        this.actionButtons.extendCollection(this.networkIndicator);
      }, error => {
        if (error.status === 404) {
          this.networkIndicator = this.getDefaultValues();
        } else {
          this.dialogService.showNotificationDialog({
            title: 'Error occurred',
            message: 'Ooops... Something went wrong, please contact support team'
          });
        }
      });
  }

  /**
  * To assign default values
  * @returns {INetworkWIndicator}
  */
  private getDefaultValues(): INetworkWIndicator {
    const popup = { ...NETWORK_INDICATOR_DEFAULT_VALUS };
    popup.brand = this.brandService.brand;
    return popup;
  }

  saveChanges(): void {
    if (this.networkIndicator.createdAt) {
      this.sendRequest('updateNetworkIndicator');
    } else {
      this.sendRequest('saveNetworkIndicator');
    }
  }

  /**
   * To revert changes
   */
  revertChanges(): void {
    this.loadInitialData();
  }

  /**
 * To save and edit
 * @param {string} requestType
 */
  private sendRequest(requestType: string): void {
    this.apiService.networkIndicatorService()[requestType](this.networkIndicator)
      .map((response) => response.body)
      .subscribe((data: INetworkWIndicator) => {
        this.networkIndicator = data;
        this.actionButtons.extendCollection(this.networkIndicator);
        this.dialogService.showNotificationDialog({
          title: 'Success',
          message: 'Your changes have been saved'
        });
      }, error => {
        this.dialogService.showNotificationDialog({
          title: 'Error on saving',
          message: 'Ooops... Something went wrong, please contact support team'
        });
      });
  }
  /**
   * Action button handlers
   * @param  {string} event
   * @returns void
   */
  actionsHandler(event: string): void {
    switch (event) {
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        break;
    }
  }
}
