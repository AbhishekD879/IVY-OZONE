import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {HttpResponse} from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';

import {DialogService} from '../../../shared/dialog/dialog.service';
import {DesktopQuickLink} from '../../../client/private/models/desktopquicklink.model';
import {ApiClientService} from '../../../client/private/services/http';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {Breadcrumb} from '../../../client/private/models/breadcrumb.model';
import {AppConstants} from '../../../app.constants';
import * as _ from 'lodash';

@Component({
  templateUrl: './desktop-quick-links-edit.component.html',
  styleUrls: ['./desktop-quick-links-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class DesktopQuickLinksEditComponent implements OnInit {

  public desktopQuickLink: DesktopQuickLink;
  public form: FormGroup;
  public breadcrumbsData: Breadcrumb[];
  @ViewChild('actionButtons') actionButtons;

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar
  ) { }

  ngOnInit() {
    this.loadInitData();
  }

  loadInitData(): void {
    this.globalLoaderService.showLoader();
    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService.desktopQuickLink()
        .findOne(params['id'])
        .map((data: HttpResponse<DesktopQuickLink>) => {
          return data.body;
        })
        .subscribe((desktopQuickLink: DesktopQuickLink) => {
          this.desktopQuickLink = desktopQuickLink;
          this.form = new FormGroup({
            disabled: new FormControl(!this.desktopQuickLink.disabled, []),
            isAtoZQuickLink: new FormControl(this.desktopQuickLink.isAtoZQuickLink, []),
            title: new FormControl(this.desktopQuickLink.title, [Validators.required]),
            target: new FormControl(this.desktopQuickLink.target, [Validators.required])
          });
          this.breadcrumbsData = [{
            label: `Desktop Quick Links`,
            url: `/quick-links/desktop-quick-links/`
          }, {
            label: this.desktopQuickLink.title,
            url: `/quick-links/desktop-quick-links/${this.desktopQuickLink.id}`
          }];
          this.globalLoaderService.hideLoader();
        }, error => {
          console.error(error.message);
          this.globalLoaderService.hideLoader();
        });
    });
  }

  save(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.desktopQuickLink()
      .update(this.desktopQuickLink)
      .map((data: HttpResponse<DesktopQuickLink>) => {
        return data.body;
      })
      .subscribe((data: DesktopQuickLink) => {
        this.desktopQuickLink = data;
        this.actionButtons.extendCollection(this.desktopQuickLink);
        this.dialogService.showNotificationDialog({
          title: 'Desktop Quick Link',
          message: 'Desktop Quick Link is Saved.'
        });
        this.globalLoaderService.hideLoader();
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  revert(): void {
    this.loadInitData();
  }

  remove(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.desktopQuickLink()
      .delete(this.desktopQuickLink.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/quick-links/desktop-quick-links/']);
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  uploadIconHandler(file): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.desktopQuickLink()
      .uploadIcon(this.desktopQuickLink.id, file)
      .map((data: HttpResponse<DesktopQuickLink>) => {
        return data.body;
      })
      .subscribe((data: DesktopQuickLink) => {
        this.desktopQuickLink = _.extend(data, _.pick(this.desktopQuickLink, 'title', 'target'));
        this.snackBar.open(`Icon Uploaded.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  removeIconHandler(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.desktopQuickLink()
      .removeIcon(this.desktopQuickLink.id)
      .map((data: HttpResponse<DesktopQuickLink>) => {
        return data.body;
      })
      .subscribe((data: DesktopQuickLink) => {
        this.desktopQuickLink = _.extend(data, _.pick(this.desktopQuickLink, 'title', 'target'));
        this.snackBar.open(`Icon Deleted.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.remove();
        break;
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
}
