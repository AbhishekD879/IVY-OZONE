import {Component, OnInit, ViewChild} from '@angular/core';
import {EndPage} from '@app/client/private/models/end-page.model';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {EndPageApiService} from '@app/quiz/service/end-page.api.service';
import {ActivatedRoute} from '@angular/router';
import {DialogService} from '@app/shared/dialog/dialog.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import {HttpErrorResponse, HttpResponse} from '@angular/common/http';
import {AppConstants, Brand} from '@app/app.constants';
import {ErrorService} from '@app/client/private/services/error.service';
import {QuizApiService} from '@app/quiz/service/quiz.api.service';
import * as _ from 'lodash';
import { BrandService } from '@app/client/private/services/brand.service';

@Component({
  selector: 'end-page-edit',
  styleUrls: ['./end-page-edit-component.scss'],
  templateUrl: './end-page-edit.component.html'
})
export class EndPageEditComponent implements OnInit {

  @ViewChild('actionButtons') actionButtons;
  endPage: EndPage;

  breadcrumbsData: Breadcrumb[];
  id: string;
  getDataError: string;
  isBrandLads: boolean;

  backgroundImageToUpload: File;

  constructor(private endPageApiService: EndPageApiService,
              private quizApiService: QuizApiService,
              private route: ActivatedRoute,
              private dialogService: DialogService,
              private errorService: ErrorService,
              private snackBar: MatSnackBar,
              private brandService: BrandService) {
    this.isBrandLads = this.brandService.brand === Brand.LADBROKES;
  }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');
    this.loadInitialData();
  }

  isValidModel(endPage): boolean {
    return endPage.id.length > 0 && endPage.title.trim().length > 0 && 
    (!endPage.successMessage || !(endPage.successMessage.length>40)) &&
    (!endPage.errorMessage || !(endPage.errorMessage.length>75)) &&
    (!endPage.redirectionButtonLabel || !(endPage.redirectionButtonLabel.length>35));
  }

  private loadInitialData(): void {
    this.endPageApiService.getEndPage(this.id).subscribe((resp: any) => {
      this.endPage = resp.body;
      this.breadcrumbsData = [{
        label: `End Page`,
        url: `/question-engine/end-page/`
      }, {
        label: this.endPage.title,
        url: `/question-engine/end-page/edit/${this.endPage.id}`
      }];
    }, error => {
      this.getDataError = error.message;
    });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeEndPage();
        break;
      case 'save':
        this.saveEndPageChanges();
        this.endPage.isChanged = false;
        break;
      case 'revert':
        this.revertEndPageChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  private removeEndPage(): void {
    this.quizApiService.getQuizzesByBrand()
      .subscribe((data: any) => {
        const quizzes = data.body;
        const anyQuiz = quizzes.filter(quiz => quiz.endPage && quiz.endPage.id === this.endPage.id);

        if (anyQuiz && anyQuiz.length > 0) {
          const quizNames = _.map(anyQuiz, 'title');
          this.dialogService.showConfirmDialog({
            title: 'Remove End Page',
            message: 'This end page is used by already configured [' + quizNames.length
              + '] quizzes and this change will affect this configuration. Are you sure?',
            yesCallback: () => {
              removeEndPage.call(this);
            }
          });
        } else {
          removeEndPage.call(this);
        }

      });

    function removeEndPage() {
      this.endPageApiService.deleteEndPage(this.endPage.id)
        .subscribe((data: any) => {
          this.dialogService.showNotificationDialog({
            title: 'Remove Completed',
            message: 'End Page is Removed.'
          });
          this.router.navigate(['/question-engine/end-page/']);
        });
    }

  }

  private saveEndPageChanges(): void {
    this.endPageApiService.updateEndPage(this.endPage)
      .map((response: HttpResponse<EndPage>) => {
        return response.body;
      })
      .subscribe((data: EndPage) => {
        this.endPage = data;

        if (this.backgroundImageToUpload) {
          this.endPageApiService.uploadBackground(this.endPage.id, this.backgroundImageToUpload)
            .map((response: HttpResponse<EndPage>) => {
              this.backgroundImageToUpload = null;
              return response.body;
            })
            .subscribe(body => {
              this.endPage = body;
              this.actionButtons.extendCollection(this.endPage);
              this.showNotification('End Page Changes are Saved.');
            }, (error: HttpErrorResponse) => {
              this.errorService.emitError('End Page Updated, but Images are not uploaded. Error: ' + error.error.message);
            });
        } else {
          this.actionButtons.extendCollection(this.endPage);
          this.showNotification('End Page Changes are Saved.');
        }
      });
  }

  showNotification(message): void {
    this.snackBar.open(message, 'Ok!', {
      duration: AppConstants.HIDE_DURATION,
    });
  }

  private revertEndPageChanges(): void {
    this.loadInitialData();
  }

  prepareToUploadFile(event): void {
    const file = event.target.files[0];
    const fileType = file.type;
    const supportedTypes = ['image/svg', 'image/svg+xml'];

    if (supportedTypes.indexOf(fileType) === -1) {
      this.dialogService.showNotificationDialog({
        title: 'Error. Unsupported file type.',
        message: 'Supported \"svg\".'
      });
    } else {
      this.backgroundImageToUpload = file;
      this.endPage.isChanged = true;
    }
  }

  handleUploadImageClick(event): void {
    const input = event.target.previousElementSibling.querySelector('input');

    input.click();
  }

  removeImage(): void {
    this.endPage.backgroundSvgImage = null;
    this.backgroundImageToUpload = null;
  }

  updateSubmitMessage(html: string) {
    this.endPage.submitMessage = html;
  }
}
