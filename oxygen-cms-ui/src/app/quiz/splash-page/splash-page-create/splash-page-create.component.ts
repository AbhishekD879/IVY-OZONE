import {Component, OnInit} from '@angular/core';
import {SplashPage} from '@app/client/private/models/splash-page.model';
import {BrandService} from '@app/client/private/services/brand.service';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {SplashPageApiService} from '@app/quiz/service/splash-page.api.service';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {Router} from '@angular/router';
import {Filename} from '@app/client/public/models/filename.model';
import {HttpErrorResponse} from '@angular/common/http';
import {ErrorService} from '@app/client/private/services/error.service';

@Component({
  selector: 'app-splash-page-create',
  templateUrl: './splash-page-create.component.html'
})
export class SplashPageCreateComponent implements OnInit {
  public breadcrumbsData: Breadcrumb[];
  newSplashPage: SplashPage;
  backgroundFileName: string = '';
  logoFileName: string = '';
  footerFileName: string = '';
  backgroundFile: File;
  logoFile: File;
  footerFile: File;

  constructor(private brandService: BrandService,
              private splashPageServiseApi: SplashPageApiService,
              private dialogService: DialogService,
              private router: Router,
              private errorService: ErrorService) { }

  ngOnInit() {
    this.newSplashPage = {
      id: '',
      title: '',
      strapLine: '',
      paragraphText1: '',
      paragraphText2: '',
      paragraphText3: '',
      playForFreeCTAText: '',
      seeYourSelectionsCTAText: '',
      seePreviousSelectionsCTAText: '',
      loginToViewCTAText: '',
      backgroundSvgFile: {} as Filename,
      backgroundSvgFilename: '',
      logoSvgFile: {} as Filename,
      logoSvgFilename: '',
      footerSvgFile: {} as Filename,
      footerSvgFilename: '',
      footerText: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      brand: this.brandService.brand,
      updatedByUserName: '',
      createdByUserName: '',
      showPreviousGamesButton: false,
      isChanged: false
    };
    this.breadcrumbsData = [{
      label: `Splash Page`,
      url: `/question-engine/splash-pages`
    }, {
      label: 'Create Splash Page',
      url: `/question-engine/splash-pages/create/`
    }];
  }

  isValidModel(): boolean {
    return this.newSplashPage.title.trim().length > 0;
  }

  public updateText(htmlMarkup: string, index: number): void {
    this.newSplashPage['paragraphText' + index] = htmlMarkup;
  }

  public saveSplashPageChanges(): void {
    const self = this;

    this.splashPageServiseApi.createSplashPage(this.newSplashPage).subscribe(data => {
      this.newSplashPage.id = data.body.id;

      if (this.backgroundFile || this.logoFile || this.footerFile) {
        this.splashPageServiseApi.uploadSvgFiles(this.newSplashPage.id, this.backgroundFile, this.logoFile, this.footerFile)
          .subscribe(resp => {
            this.finishSplashPageCreation();
          }, (error: HttpErrorResponse) => {
              self.router.navigate([`question-engine/splash-pages/splash-page/${self.newSplashPage.id}`]).then(() => {
                this.errorService.emitError('Splash Page Created, but Images are not uploaded. Error: ' + error.error.message);
              });
            });
      } else {
        this.finishSplashPageCreation();
      }
    });
  }

  finishSplashPageCreation(): void {
    const self = this;
    this.dialogService.showNotificationDialog({
      title: 'Save Completed',
      message: 'Splash Page is Created and Stored.',
      closeCallback() {
        self.router.navigate([`question-engine/splash-pages/splash-page/${self.newSplashPage.id}`]);
      }
    });
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
  }

  handleUploadImageClick(event, fieldName): void {
    const input = event.target.previousElementSibling.querySelector('input');

    input.click();
  }

  removeImage(event, fieldName): void {
    this.newSplashPage[fieldName] = undefined;
    if (fieldName === 'logoSvgFile') {
      this.logoFileName = undefined;
      this.logoFile = undefined;
    } else if (fieldName === 'backgroundSvgFile') {
      this.backgroundFileName = undefined;
      this.backgroundFile = undefined;
    } else if (fieldName === 'footerSvgFile') {
      this.footerFileName = undefined;
      this.footerFile = undefined;
    }
  }

  getButtonName(fileName): string {
    return fileName.length > 0 ? 'Change File' : 'Upload File';
  }
}

