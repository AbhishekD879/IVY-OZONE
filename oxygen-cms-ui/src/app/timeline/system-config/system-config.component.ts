import {Component, OnInit, ViewChild} from '@angular/core';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {ActionButtonsComponent} from '@app/shared/action-buttons/action-buttons.component';


import * as _ from 'lodash';

import {BrandService} from '@app/client/private/services/brand.service';

import {TimelineSystemConfig} from '@app/client/private/models/timelineSystemConfig';
import {TimelineSystemConfigApiService} from '@app/timeline/service/timeline-system-config-api.service';


@Component({
  selector: 'timeline-system-config',
  templateUrl: './system-config.component.html',
  styleUrls: []
})

export class SystemConfigComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  systemConfigInitialObj: TimelineSystemConfig = {
    brand: '',
    id: '',

    createdAt: '',
    createdBy: '',
    createdByUserName: '',
    updatedAt: '',
    updatedBy: '',
    updatedByUserName: '',

    enabled: false,
    pageUrls: ''
  };


  systemConfig: TimelineSystemConfig;


  constructor(private dialogService: DialogService,
              private brandService: BrandService,
              private api: TimelineSystemConfigApiService) {
    this.systemConfig = this.empty();
  }


  ngOnInit() {
    this.load();
  }

  private load() {
    this.api.getOneByBrand()
      .subscribe((data: {body: TimelineSystemConfig}) => {
        this.systemConfig = data.body;
        this.actionButtons.extendCollection(this.systemConfig);
      }, error => {
        if (error.status === 404) {
          this.systemConfig = this.empty();
        } else {
          console.log(error);
          this.dialogService.showNotificationDialog({
            title: 'Error occurred',
            message: 'Ooops... Something went wrong, please contact support team'
          });
        }
      });
  }


  actionsHandler(event): void {
    switch (event) {
      case 'save':
        this.save();
        break;
      case 'revert':
        this.revert();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }


  verifySystemConfigData(timelineSystemConfig: TimelineSystemConfig): boolean {
    return (!!timelineSystemConfig.pageUrls);
  }

  private empty(): TimelineSystemConfig {
    const config = _.cloneDeep(this.systemConfigInitialObj);
    config.brand = this.brandService.brand;

    return config;
  }


  private save() {
    if (this.systemConfig.createdAt) {
      this.sendRequest('update');
    } else {
      this.sendRequest('create');
    }
  }


  private revert() {
    this.load();
  }


  private sendRequest(requestType) {
    this.api[requestType](this.systemConfig)
      .subscribe((data: {body: TimelineSystemConfig}) => {
        this.systemConfig = data.body;
        this.actionButtons.extendCollection(this.systemConfig);
        this.dialogService.showNotificationDialog({
          title: 'Success',
          message: 'Your changes have been saved'
        });
      }, error => {
        console.log(error);
        this.dialogService.showNotificationDialog({
          title: 'Error on saving',
          message: 'Ooops... Something went wrong, please contact support team'
        });
      });
  }
}
