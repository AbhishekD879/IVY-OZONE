import {Component, OnInit, ViewChild} from '@angular/core';
import {SplashPage} from '@app/client/private/models/splash-page.model';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {SplashPageApiService} from '@app/quiz/service/splash-page.api.service';
import {ActivatedRoute} from '@angular/router';
import {DialogService} from '@app/shared/dialog/dialog.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import {HttpErrorResponse, HttpResponse} from '@angular/common/http';
import {AppConstants} from '@app/app.constants';
import {ErrorService} from '@app/client/private/services/error.service';
import {QuizApiService} from '@app/quiz/service/quiz.api.service';
import * as _ from 'lodash';

@Component({
  selector: 'app-splash-page-edit',
  templateUrl: './splash-page-edit.component.html'
})
export class SplashPageEditComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons;

  splashPage: SplashPage;
  public breadcrumbsData: Breadcrumb[];
  id: string;
  getDataError: string;

  backgroundFileName: string;
  logoFileName: string;
  footerFileName: string;
  backgroundFile: File;
  logoFile: File;
  footerFile: File;

  constructor(private splashPageApiServcie: SplashPageApiService,
              private quizApiService: QuizApiService,
              private route: ActivatedRoute,
              private dialogService: DialogService,
              private errorService: ErrorService,
              private snackBar: MatSnackBar) { }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');
    this.loadInitialData();
  }

  isValidModel(splashPage): boolean {
    return splashPage.id.length > 0 && splashPage.title.trim().length > 0;
  }

  public updateText(htmlMarkup: string, index: number): void {
    this.splashPage['paragraphText' + index] = htmlMarkup;
  }

  private loadInitialData(): void {
    this.splashPageApiServcie.getSplashPage(this.id).subscribe((resp: any) => {
      this.splashPage = resp.body;
      this.backgroundFileName = this.splashPage.backgroundSvgFilename;
      this.logoFileName = this.splashPage.logoSvgFilename;
      this.footerFileName = this.splashPage.footerSvgFilename;
      this.breadcrumbsData = [{
        label: `Splash Page`,
        url: `/question-engine/splash-pages`
      }, {
        label: this.splashPage.title,
        url: `/question-engine/splash-pages/splash-page/${this.splashPage.id}`
      }];
    }, error => {
      this.getDataError = error.message;
    });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeSplashPage();
        break;
      case 'save':
        this.saveSplashPageChanges();
        break;
      case 'revert':
        this.revertSplashPageChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  private removeSplashPage(): void {
    this.quizApiService.getQuizzesByBrand()
      .subscribe((data: any) => {
        const quizzes = data.body;
        const anyQuiz = quizzes.filter(quiz => quiz.splashPage && quiz.splashPage.id === this.splashPage.id);

        if (anyQuiz && anyQuiz.length > 0) {
          const quizNames = _.map(anyQuiz, 'title');
          this.dialogService.showConfirmDialog({
            title: 'Remove Splash Page',
            message: 'This splash page is used by already configured [' + quizNames.length
              + '] quizzes and this change will affect this configuration. Are you sure?',
            yesCallback: () => {
              removeSpPage.call(this);
            }
          });
        } else {
          removeSpPage.call(this);
        }

      });

    function removeSpPage() {
      this.splashPageApiServcie.deleteSplashPage(this.splashPage.id)
        .subscribe((data: any) => {
          this.dialogService.showNotificationDialog({
            title: 'Remove Completed',
            message: 'Splash Page is Removed.'
          });
          this.router.navigate(['/question-engine/splash-pages/']);
        });
    }
  }

  private saveSplashPageChanges(): void {
    this.splashPageApiServcie.updateSplashPage(this.splashPage)
      .map((response: HttpResponse<SplashPage>) => {
        return response.body;
      })
      .subscribe((data: SplashPage) => {
        this.splashPage = data;

        if (this.backgroundFile || this.logoFile || this.footerFile) {
          this.splashPageApiServcie.uploadSvgFiles(this.splashPage.id, this.backgroundFile, this.logoFile, this.footerFile)
            .map((response: HttpResponse<SplashPage>) => {
              return response.body;
            })
            .subscribe((spPage: SplashPage) => {
              this.splashPage = spPage;
              this.clearPredefinedFiles();
              this.actionButtons.extendCollection(this.splashPage);
              this.showNotification('Splash Page Changes are Saved.');
            }, (error: HttpErrorResponse) => {
              this.clearPredefinedFiles();
              this.actionButtons.extendCollection(this.splashPage);
              this.errorService.emitError('Splash Page Updated, but Images are not uploaded. Error: ' + error.error);
            });
        } else {
          this.actionButtons.extendCollection(this.splashPage);
          this.showNotification('Splash Page Changes are Saved.');
        }
      });
  }

  private clearPredefinedFiles() {
    this.backgroundFile = undefined;
    this.backgroundFileName = this.splashPage.backgroundSvgFile ? this.splashPage.backgroundSvgFile.originalname : '';
    this.logoFile = undefined;
    this.logoFileName = this.splashPage.logoSvgFile ? this.splashPage.logoSvgFile.originalname : '';
    this.footerFile = undefined;
    this.footerFileName = this.splashPage.footerSvgFile ? this.splashPage.footerSvgFile.originalname : '';
  }

  showNotification(message): void {
    this.snackBar.open(message, 'Ok!', {
      duration: AppConstants.HIDE_DURATION,
    });
  }


  private revertSplashPageChanges(): void {
    this.loadInitialData();
  }

  prepareToUploadFile(event, fieldName): void {
    const file = event.target.files[0];
    const fileType = file.type;
    const supportedTypes = ['image/svg', 'image/svg+xml'];

    if (supportedTypes.indexOf(fileType) === -1) {
      this.dialogService.showNotificationDialog({
        title: 'Error. Unsupported file type.',
        message: 'Supported \"svg\".'
      });

      return;
    }
    if (fieldName === 'logoSvgFile') {
      this.logoFileName = file.name;
      this.logoFile = file;
    } else if (fieldName === 'backgroundSvgFile') {
      this.backgroundFileName = file.name;
      this.backgroundFile = file;
    } else if (fieldName === 'footerSvgFile') {
      this.footerFileName = file.name;
      this.footerFile = file;
    }

    this.splashPage.isChanged = true;

  }

  handleUploadImageClick(event, fieldName): void {
    const input = event.target.previousElementSibling.querySelector('input');

    input.click();
  }

  removeImage(event, fieldName): void {
    this.splashPage[fieldName] = undefined;
    if (fieldName === 'logoSvgFile') {
      this.logoFileName = undefined;
      this.logoFile = undefined;
      this.splashPage.logoSvgFilename = undefined;
    } else if (fieldName === 'backgroundSvgFile') {
      this.backgroundFileName = undefined;
      this.backgroundFile = undefined;
      this.splashPage.backgroundSvgFilename = undefined;
    } else if (fieldName === 'footerSvgFile') {
      this.footerFileName = undefined;
      this.footerFile = undefined;
      this.splashPage.footerSvgFilename = undefined;
    }
  }

  getButtonName(fileName): string {
    return fileName && fileName.length > 0 ? 'Change File' : 'Upload File';
  }
}
