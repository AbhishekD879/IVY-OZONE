import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {SsoPage} from '@app/client/private/models/ssopage.model';
import {SsoApiService} from '../../service/sso.api.service';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import {AppConstants} from '@app/app.constants';
import {HttpResponse} from '@angular/common/http';
import * as _ from 'lodash';

// @ts-ignore
declare var tinymce: any;

@Component({
  selector: 'single-sso-page',
  templateUrl: './sso.page.component.html',
  styleUrls: ['./sso.page.component.scss']
})
export class SsoPageComponent implements OnInit {
  ssoPage: SsoPage;
  id: string;
  @ViewChild('actionButtons') actionButtons;
  public breadcrumbsData: Breadcrumb[];

  constructor(
    public snackBar: MatSnackBar,
    private dialogService: DialogService,
    private route: ActivatedRoute,
    private router: Router,
    private ssoAPIService: SsoApiService
  ) {}

  loadInitialData() {
    // load current ssoPage data
    this.ssoAPIService.getSingleSsoPageData(this.id)
      .map((data: HttpResponse<SsoPage>) => data.body)
      .subscribe((data: SsoPage) => {
        this.ssoPage = data;
        this.breadcrumbsData = [{
          label: `SSO`,
          url: `/sso-page`
        }, {
          label: this.ssoPage.title,
          url: `/sso-page/${this.ssoPage.id}`
        }];
      }, error => {
        this.router.navigate(['/sso-pages']);
      });
  }

  /**
   * Upload file on input change event.
   * @param event
   */
  uploadImage(formData: FormData) {
    this.ssoAPIService.postNewSsoPageImage(this.ssoPage.id, formData)
      .map((data: HttpResponse<SsoPage>) => data.body)
      .subscribe((data: SsoPage) => {
        // update uploaded image name to show inside input
        this.ssoPage = _.extend(data, _.pick(this.ssoPage, 'disabled', 'title', 'openLink', 'showOnAndroid',
          'showOnIOS', 'targetAndroid', 'targetIOS'));
        this.snackBar.open('Image Was Uploaded.', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  removeImage(): void {
    this.ssoAPIService.removeSsoPageImage(this.ssoPage.id)
      .map((data: HttpResponse<SsoPage>) => data.body)
      .subscribe((data: SsoPage) => {
        this.ssoPage = _.extend(data, _.pick(this.ssoPage, 'disabled', 'title', 'openLink', 'showOnAndroid',
          'showOnIOS', 'targetAndroid', 'targetIOS'));
        this.snackBar.open('Image Was Removed.', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  private revertChanges(): void {
    this.loadInitialData();
  }

  public isValidForm(ssoPage: SsoPage): boolean {
    return ssoPage.title && ssoPage.title.length > 0;
  }

  /**
   * Send DELETE API request
   * @param {SsoPage} ssoPage
   */
  private removeElement(): void {
    this.ssoAPIService.deleteSsoPage(this.ssoPage.id)
      .subscribe((data: HttpResponse<void>) => {
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'SsoPage is Removed.'
        });
        this.router.navigate(['/sso-page']);
      });
  }

  /**
   * Make PUT request to server to update
   */
  private saveChanges(): void {
    this.ssoAPIService
        .putSsoPageChanges(this.ssoPage)
        .map((response: HttpResponse<SsoPage>) => {
          return response.body;
        })
        .subscribe((data: SsoPage) => {
          this.ssoPage = data;
          this.actionButtons.extendCollection(this.ssoPage);
          this.dialogService.showNotificationDialog({
            title: 'Upload Completed',
            message: 'SsoPage Changes are Saved.'
          });
        });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeElement();
        break;
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');

    this.loadInitialData();
  }
}
