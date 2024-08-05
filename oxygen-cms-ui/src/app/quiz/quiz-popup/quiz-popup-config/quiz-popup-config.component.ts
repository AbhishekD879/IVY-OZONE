import {Component, OnInit, ViewChild} from '@angular/core';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {ActionButtonsComponent} from '@app/shared/action-buttons/action-buttons.component';
import {QuizPopupApiService} from '@app/quiz/service/quiz-popup.api.service';
import { MatSelectChange } from '@angular/material/select';

import * as _ from 'lodash';
import {BrandService} from '@app/client/private/services/brand.service';
import {QuizPopupConfig} from '@app/client/private/models/quizPopupConfig.model';

@Component({
  selector: 'quiz-popup-config',
  templateUrl: './quiz-popup-config.component.html',
  styleUrls: ['./quiz-popup-config.component.scss']
})
export class QuizPopupConfigComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  quizPopupInitialObj: QuizPopupConfig = {
    brand: '',
    id: '',
    createdAt: '',
    createdBy: '',
    createdByUserName: '',
    updatedAt: '',
    updatedBy: '',
    updatedByUserName: '',

    enabled: false,
    pageUrls: '',

    popupTitle: '',
    popupText: '',
    quizId: '',
    yesText: '',
    remindLaterText: '',
    dontShowAgainText: ''
  };

  quizPopup: QuizPopupConfig;

  quizzes: {id: string, title: string}[];

  constructor(private dialogService: DialogService,
              private brandService: BrandService,
              private api: QuizPopupApiService) {
    this.quizPopup = this.empty();
  }

  ngOnInit() {
    this.load();
  }


  private load() {
    this.api
      .getQuizzes()
      .subscribe(quizzes => {
        this.quizzes = quizzes.body ? quizzes.body.filter(quiz => quiz.active) : [];
      });

    this.api.getOneByBrand()
      .subscribe((data: {body: QuizPopupConfig}) => {
        this.quizPopup = data.body;
        this.actionButtons.extendCollection(this.quizPopup);
      }, error => {
        if (error.status === 404) {
          this.quizPopup = this.empty();
        } else {
          console.log(error);
          this.dialogService.showNotificationDialog({
            title: 'Error occurred',
            message: 'Ooops... Something went wrong, please contact support team'
          });
        }
      });
  }

  setQuizId(event: MatSelectChange): void {
    this.quizPopup.quizId = event.value;
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

  verifyQuizPopupData(quizPopup: QuizPopupConfig): boolean {
    return (!!quizPopup.quizId) && (!!quizPopup.pageUrls);
  }

  private shouldConfirmationDialogBeShown() {
    const headerOrTitlePresent = (this.quizPopup.popupTitle || this.quizPopup.popupText);
    const anyBtnTextPresent = (this.quizPopup.yesText || this.quizPopup.remindLaterText || this.quizPopup.dontShowAgainText);

    return !(headerOrTitlePresent && anyBtnTextPresent);
  }

  private empty(): QuizPopupConfig {
    const popup = _.cloneDeep(this.quizPopupInitialObj);
    popup.brand = this.brandService.brand;

    return popup;
  }

  private save() {
    if (this.shouldConfirmationDialogBeShown()) {
      this.dialogService.showConfirmDialog({
        title: 'Are you sure to save this config?',
        message: 'Either modal title or text AND at least one button text should present for popup.',
        yesCallback: () => {
          if (this.quizPopup.createdAt) {
            this.sendRequest('update');
          } else {
            this.sendRequest('create');
          }
        }
      });
    } else if (this.quizPopup.createdAt) {
      this.sendRequest('update');
    } else {
      this.sendRequest('create');
    }
  }

  private revert() {
    this.load();
  }

  private sendRequest(requestType) {
    this.api[requestType](this.quizPopup)
      .subscribe((data: {body: QuizPopupConfig}) => {
        this.quizPopup = data.body;
        this.actionButtons.extendCollection(this.quizPopup);
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
