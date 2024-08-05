import { Component, OnInit, ViewChild } from '@angular/core';
import { TabNameConfigurationApiService } from '../service/tabNameConfiguration.api.service';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { TabNameConfigurationData } from '../constants/otf.model';

@Component({
    selector: 'app-tab-name-configuration',
    templateUrl: './tab-name-configuration.component.html',
})
export class TabNameConfigurationComponent implements OnInit {
    @ViewChild('actionButtons') actionButtons;
    tabNameConfiguration = new TabNameConfigurationData();
    getDataError: string;
    errorMessage: string;
    id: string;
    isReady: boolean;

    constructor(
        private tabNameConfigurationApiService: TabNameConfigurationApiService,
        private dialogService: DialogService,
    ) {
        this.isValidModel = this.isValidModel.bind(this);
    }

    isValidModel(tabNameConfiguration : TabNameConfigurationData) {
        return tabNameConfiguration && tabNameConfiguration.currentTabLabel &&
            tabNameConfiguration.currentTabLabel.length > 0 &&
            !(tabNameConfiguration.currentTabLabel.length > 50) &&
            tabNameConfiguration.previousTabLabel &&
            tabNameConfiguration.previousTabLabel.length > 0 &&
            !(tabNameConfiguration.previousTabLabel.length > 50)
    }

    ngOnInit() {
        this.loadTabNameConfigData();
    }

    loadTabNameConfigData() {
        this.tabNameConfigurationApiService.getTabNameConfigurationData()
            .subscribe((data: any) => {
                this.tabNameConfiguration = data.body;
                this.isReady = true;
            }, error => {
                this.getDataError = error.message;
            });
    }

    /**
   * Make POST request to server to Save
   */
    saveTabNameConfigChanges() {
    /* Create Flow */
    if (!this.tabNameConfiguration.id) {
        this.tabNameConfigurationApiService.saveTabNameConfigurationData(this.tabNameConfiguration).subscribe(data => {
            this.tabNameConfiguration = data.body;
            this.successDialog('Saved');
            this.actionButtons.extendCollection(this.tabNameConfiguration);
          })
        }
        else
        {
          this.tabNameConfigurationApiService.updateTabNameConfigurationData(this.tabNameConfiguration).subscribe(data => {
            this.tabNameConfiguration = data.body;
            this.actionButtons.extendCollection(this.tabNameConfiguration);
            this.successDialog('Updated');
          })
        }
    }

      /**
  * Confirmation dialog on successful creation or updation of My Badges data
  *  @param: type
  */
  successDialog(type: string) {
    this.dialogService.showNotificationDialog({
      title: 'Tab Names',
      message: 'Tab Names ' + type + ' Succesfully!! '
    });
  }

    /**
  * Action Handler for Action buttons 
  *  @param: event
  */
    actionsHandler(event): void {
        switch (event) {
            case 'save':
                this.saveTabNameConfigChanges();
                break;
            case 'revert':
                this.loadTabNameConfigData();
                break;
            default:
                console.error('Unhandled Action');
                break;
        }
    }

}
