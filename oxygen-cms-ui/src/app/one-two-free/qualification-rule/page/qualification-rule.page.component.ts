import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {QualificationRule} from '@app/client/private/models/qualificationRule.model';
import {QualificationRuleAPIService} from '@app/one-two-free/service/qualificationRule.api.service';
import {BrandService} from '@app/client/private/services/brand.service';
import {HttpErrorResponse} from '@angular/common/http';
import {ActionButtonsComponent} from '@app/shared/action-buttons/action-buttons.component';

import * as _ from 'lodash';

@Component({
  selector: 'qualification-rule-page',
  templateUrl: './qualification-rule.page.component.html',
  styleUrls: ['./qualification-rule.page.component.scss']
})
export class QualificationRulePageComponent implements OnInit {
  @ViewChild('csvUpload') private csvUpload: ElementRef;
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  qualificationRule: QualificationRule;
  csvFileName: string = '';
  csvFile: File;
  _: any = _;

  constructor(private api: QualificationRuleAPIService,
              private dialogService: DialogService,
              private brandService: BrandService) {

  }

  ngOnInit(): void {
    this.load();
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

  private load() {
    this.api.getOneByBrand()
      .subscribe((data: any) => {
        this.qualificationRule = data.body;
        this.csvFileName = this.parseCsvFileName(this.qualificationRule.blacklistedUsersPath);
        this.populateRecurringUsersList();
      }, error => {
        if (error.status === 404) {
          this.qualificationRule = this.empty();
        } else {
          console.log(error);
          this.openErrorDialog();
        }
      });
  }

  private parseCsvFileName(blacklistedUsersPath: string) {
    const arr = blacklistedUsersPath ? blacklistedUsersPath.split('/') : [];
    return arr && arr.length > 0 ? arr[arr.length - 1] : '';
  }

  private save() {
    if (this.isNotValid()) {
      this.dialogService.showNotificationDialog({
        title: 'Error on saving',
        message: 'Check if all data present and is valid'
      });
    } else {
      this.qualificationRule.recurringUsers = {};
      this.qualificationRule.recurringUsersList
        .filter(user => !_.isEmpty(user.username))
        .forEach(user => this.qualificationRule.recurringUsers[user.username] = user.enabled);

      if (this.qualificationRule.createdAt) {
        if (this.onlyFileNameInPath(this.qualificationRule.blacklistedUsersPath)) {
          this.qualificationRule.blacklistedUsersPath = '';
        }
        this.sendRequest('update');
      } else {
        this.sendRequest('create');
      }
    }
  }

  private sendRequest(requestType) {
    this.api[requestType](this.qualificationRule)
      .subscribe((data: any) => {
        this.qualificationRule = data.body;
        this.populateRecurringUsersList();
        this.actionButtons.extendCollection(this.qualificationRule);
        this.proceedDataSaving();
      }, error => {
        console.log(error);
        this.openErrorDialog();
      });
  }

  private populateRecurringUsersList() {
    if (_.isEmpty(this.qualificationRule.recurringUsers)) {
      this.qualificationRule.recurringUsersList = [{
        username: '',
        enabled: false
      }];
    } else {
      this.qualificationRule.recurringUsersList = [];
      _.keys(this.qualificationRule.recurringUsers)
        .forEach(username => this.qualificationRule.recurringUsersList.push(
          {
            username: username,
            enabled: this.qualificationRule.recurringUsers[username]
          }
        ));
    }
  }

  private proceedDataSaving() {
    if (this.csvFile) {
      this.uploadBlacklistedUsers();
    } else {
      this.openSuccessDialog();
    }
  }

  private uploadBlacklistedUsers(): void {
      this.api.uploadBlacklistedUsers(this.csvFile).subscribe(resp => {
        this.qualificationRule = resp.body;
        this.actionButtons.extendCollection(this.qualificationRule);
        this.openSuccessDialog();
      }, (error: HttpErrorResponse) => {
        this.csvFileName = this.parseCsvFileName(this.qualificationRule.blacklistedUsersPath);
        console.log(error);
        this.dialogService.showNotificationDialog({
          title: 'Error on file uploading',
          message: 'Something went wrong, please try again'
        });
      });
  }

  private revert() {
    const input = this.csvUpload.nativeElement;
    input.value = '';
    this.load();
  }

  private isNotValid() {
    return this.qualificationRule.daysToCheckActivity < 0;
  }

  private openErrorDialog() {
    this.dialogService.showNotificationDialog({
      title: 'Error on saving',
      message: 'Ooops... Something went wrong, please contact support team'
    });
  }

  private openSuccessDialog() {
    this.dialogService.showNotificationDialog({
      title: 'Success',
      message: 'Your changes have been saved'
    });
  }

  private empty(): QualificationRule {
    return {
      brand: this.brandService.brand,
      createdAt: '',
      createdBy: '',
      createdByUserName: '',
      daysToCheckActivity: null,
      blacklistedUsersPath: '',
      enabled: false,
      id: '',
      message: '',
      updatedAt: '',
      updatedBy: '',
      updatedByUserName: '',
      recurringUsers: {},
      recurringUsersList: [{
        username: '',
        enabled: false
      }]
    };
  }

  public verifyQualificationRuleData(qualificationRule: QualificationRule): boolean {
    return true;
  }

  prepareToUploadFile(event): void {
    const file = event.target.files[0];
    const fileType = file.type;
    const supportedTypes = ['text/csv'];

    if (supportedTypes.indexOf(fileType) === -1) {
      this.dialogService.showNotificationDialog({
        title: 'Error. Unsupported file type.',
        message: 'Supported \"csv\".'
      });

      return;
    }

    this.csvFileName = file.name;
    this.csvFile = file;
    this.qualificationRule.blacklistedUsersPath = file.name;
  }

  handleUploadImageClick(): void {
    const input = this.csvUpload.nativeElement;

    input.click();
  }

  removeImage(): void {
    const input = this.csvUpload.nativeElement;
    input.value = '';

    this.qualificationRule.blacklistedUsersPath = '';
    this.csvFileName = undefined;
    this.csvFile = undefined;
  }

  getButtonName(fileName): string {
    return fileName && fileName.length > 0 ? 'Change File' : 'Upload File';
  }

  private onlyFileNameInPath(blacklistedUsersPath: string) {
    return blacklistedUsersPath && blacklistedUsersPath.split('/').length === 1;
  }

  addRecurringUser() {
    this.qualificationRule.recurringUsersList.push({
      username: '',
      enabled: false
    });
  }

  removeRecurringUser(username: string) {
    _.remove(this.qualificationRule.recurringUsersList, function (user) {
      return user.username === username;
    });
  }
}
