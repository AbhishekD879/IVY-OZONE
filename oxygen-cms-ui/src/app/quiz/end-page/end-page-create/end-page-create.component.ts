import {Component, OnInit} from '@angular/core';
import {EndPage} from '@app/client/private/models/end-page.model';
import {BrandService} from '@app/client/private/services/brand.service';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {EndPageApiService} from '@app/quiz/service/end-page.api.service';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {Router} from '@angular/router';
import {HttpErrorResponse} from '@angular/common/http';
import {ErrorService} from '@app/client/private/services/error.service';
import { Brand } from '@app/app.constants';

@Component({
  selector: 'end-page-create',
  templateUrl: './end-page-create.component.html'
})
export class EndPageCreateComponent implements OnInit {
  public breadcrumbsData: Breadcrumb[];
  newEndPage: EndPage;
  backgroundImageToUpload: File;
  isBrandLads: boolean;

  constructor(private brandService: BrandService,
              private endPageServiceApi: EndPageApiService,
              private dialogService: DialogService,
              private router: Router,
              private errorService: ErrorService) {
    this.isBrandLads = this.brandService.brand === Brand.LADBROKES;
  }

  ngOnInit() {
    this.newEndPage = {
      isChanged: false,
      showAnswersSummary: false,
      backgroundSvgImage: undefined,
      gameDescription: '',
      noLatestRoundMessage: '',
      noPreviousRoundMessage: '',
      showPrizes: false,
      showResults: false,
      submitMessage: '',
      submitCta: '',
      showUpsell: false,
      id: '',
      title: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      brand: this.brandService.brand,
      updatedByUserName: '',
      createdByUserName: '',
      upsellAddToBetslipCtaText: '',
      upsellBetInPlayCtaText: '',
      successMessage: '',
      errorMessage: '',
      redirectionButtonLabel: '',
      redirectionButtonUrl: '',
      bannerSiteCoreId: ''
    };
    this.breadcrumbsData = [{
      label: `End Page`,
      url: `/question-engine/end-page`
    }, {
      label: 'Create End Page',
      url: `/question-engine/end-page/create/`
    }];
  }

  isValidModel(): boolean {
    return this.newEndPage.title.trim().length > 0 && 
    (!this.newEndPage.successMessage || !(this.newEndPage.successMessage.length>40)) &&
    (!this.newEndPage.errorMessage || !(this.newEndPage.errorMessage.length>75)) &&
    (!this.newEndPage.redirectionButtonLabel || !(this.newEndPage.redirectionButtonLabel.length>35));
  }

  public saveEndPageChanges(): void {
    const self = this;

    this.endPageServiceApi.createEndPage(this.newEndPage)
      .subscribe(data => {
        this.newEndPage.id = data.body.id;

        if (this.backgroundImageToUpload) {
          this.endPageServiceApi.uploadBackground(this.newEndPage.id, this.backgroundImageToUpload)
            .subscribe(resp => {
              this.backgroundImageToUpload = null;
              this.finishEndPageCreation();
            }, (error: HttpErrorResponse) => {
              self.router.navigate([`question-engine/end-page/edit/${self.newEndPage.id}`]).then(() => {
                this.errorService.emitError('End Page Created, but Images are not uploaded. Error: ' + error.error.message);
              });
            });
        } else {
          this.finishEndPageCreation();
        }
      });
  }

  finishEndPageCreation(): void {
    const self = this;
    this.dialogService.showNotificationDialog({
      title: 'Save Completed',
      message: 'End Page is Created and Stored.',
      closeCallback() {
        self.router.navigate([`question-engine/end-page/edit/${self.newEndPage.id}`]);
      }
    });
  }

  prepareToUploadFile(event): void {
    const file = event.target.files[0];
    const fileType = file.type;
    const supportedTypes = ['image/svg', 'image/svg+xml'];

    if (supportedTypes.indexOf(fileType) === -1) {
      this.dialogService.showNotificationDialog({
        title: 'Error. Unsupported file type.',
        message: 'Supported "svg".'
      });
    } else {
      this.backgroundImageToUpload = file;
    }
  }

  handleUploadImageClick(event): void {
    const input = event.target.previousElementSibling.querySelector('input');

    input.click();
  }

  removeImage(): void {
    this.newEndPage.backgroundSvgImage = null;
    this.backgroundImageToUpload = null;
  }

  updateSubmitMessage(html: string) {
    this.newEndPage.submitMessage = html;
  }
}
