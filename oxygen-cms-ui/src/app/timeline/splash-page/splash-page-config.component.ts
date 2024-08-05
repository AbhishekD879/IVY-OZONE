import {Component, OnInit, ViewChild} from '@angular/core';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {ActionButtonsComponent} from '@app/shared/action-buttons/action-buttons.component';


import * as _ from 'lodash';

import {BrandService} from '@app/client/private/services/brand.service';

import {TimelineSplashPageConfig} from '@app/client/private/models/timelineSplashPageConfig';
import {TimelineSplashConfigApiService} from '@app/timeline/service/timeline-splash-config-api.service';
import {TinymceComponent} from '@app/shared/tinymce/tinymce.component';


@Component({
  selector: 'timeline-splash-config',
  templateUrl: './splash-page-config.component.html',
  styleUrls: []
})
export class SplashPageConfigComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  @ViewChild('text') headerTextEditor: TinymceComponent;

  systemConfigInitialObj: TimelineSplashPageConfig = {
    brand: '',
    id: '',

    createdAt: '',
    createdBy: '',
    createdByUserName: '',
    updatedAt: '',
    updatedBy: '',
    updatedByUserName: '',

    showSplashPage: false,
    text: ''
  };


  config: TimelineSplashPageConfig;


  constructor(private dialogService: DialogService,
              private brandService: BrandService,
              private api: TimelineSplashConfigApiService) {
  }


  ngOnInit() {
    this.load();
  }

  updateText(data) {
    this.config.text = data;
  }

  private load() {
    this.api.getOneByBrand()
      .subscribe((data: {body: TimelineSplashPageConfig}) => {
        this.config = data.body;
        if (this.headerTextEditor) {
          this.headerTextEditor.update(this.config.text);
        }
        this.actionButtons.extendCollection(this.config);
      }, error => {
        if (error.status === 404) {
          this.config = this.empty();
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

  verifySplashPageConfigData(timelineSplashPageConfig: TimelineSplashPageConfig): boolean {
    return !!timelineSplashPageConfig;
  }

  private empty(): TimelineSplashPageConfig {
    const popup = _.cloneDeep(this.systemConfigInitialObj);
    popup.brand = this.brandService.brand;

    return popup;
  }


  private save() {
    if (this.config.createdAt) {
      this.sendRequest('update');
    } else {
      this.sendRequest('create');
    }
  }


  private revert() {
    this.load();
  }


  private sendRequest(requestType) {
    this.api[requestType](this.config)
      .subscribe((data: {body: TimelineSplashPageConfig}) => {
        this.config = data.body;
        this.actionButtons.extendCollection(this.config);
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
