import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {HttpResponse} from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';

import {DialogService} from '@app/shared/dialog/dialog.service';
import {HRQuickLink} from '@app/client/private/models/hrquicklink.model';
import {ApiClientService} from '@app/client/private/services/http';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {DateRange} from '@app/client/private/models/dateRange.model';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {AppConstants} from '@app/app.constants';
import * as _ from 'lodash';

@Component({
  templateUrl: './hr-quick-links-edit.component.html',
  styleUrls: ['./hr-quick-links-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class HrQuickLinksEditComponent implements OnInit {

  public hrQuickLink: HRQuickLink;
  public form: FormGroup;
  public raceTypes: Array<string> = ['horse racing', 'greyhound racing'];
  public linkTypes: Array<string> = ['url', 'selection'];
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
      this.apiClientService.hrQuickLink()
        .findOne(params['id'])
        .map((data: HttpResponse<HRQuickLink>) => {
          return data.body;
        })
        .subscribe((hrQuickLink: HRQuickLink) => {
          this.hrQuickLink = hrQuickLink;
          this.form = new FormGroup({
            title: new FormControl(this.hrQuickLink.title, [Validators.required]),
            body: new FormControl(this.hrQuickLink.body, [Validators.required]),
            raceType: new FormControl(this.hrQuickLink.raceType, [Validators.required]),
            linkType: new FormControl(this.hrQuickLink.linkType, [Validators.required]),
            target: new FormControl(this.hrQuickLink.target, []),
            disabled: new FormControl(!this.hrQuickLink.disabled, [])
          });
          this.breadcrumbsData = [{
            label: `HR Quick Links`,
            url: `/quick-links/quick-links`
          }, {
            label: this.hrQuickLink.title,
            url: `/quick-links/quick-links/${this.hrQuickLink.id}`
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
    this.apiClientService.hrQuickLink()
      .update(this.hrQuickLink)
      .map((data: HttpResponse<HRQuickLink>) => {
        return data.body;
      })
      .subscribe((data: HRQuickLink) => {
        this.hrQuickLink = data;
        this.actionButtons.extendCollection(this.hrQuickLink);
        this.dialogService.showNotificationDialog({
          title: 'HR Quick Link',
          message: 'HR Quick Link is Saved.'
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
    this.apiClientService.hrQuickLink()
      .delete(this.hrQuickLink.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/quick-links/quick-links/']);
      }, error => {
        console.error(error.message);
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

  uploadIconHandler(file): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.hrQuickLink()
      .uploadIcon(this.hrQuickLink.id, file)
      .map((data: HttpResponse<HRQuickLink>) => {
        return data.body;
      })
      .subscribe((data: HRQuickLink) => {
        this.hrQuickLink = _.extend(data, _.pick(this.hrQuickLink, 'title', 'target', 'body', 'raceType',
          'linkType', 'validityPeriodEnd', 'validityPeriodStart'));
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
    this.apiClientService.hrQuickLink()
      .removeIcon(this.hrQuickLink.id)
      .map((data: HttpResponse<HRQuickLink>) => {
        return data.body;
      })
      .subscribe((data: HRQuickLink) => {
        this.hrQuickLink = _.extend(data, _.pick(this.hrQuickLink, 'title', 'target', 'body', 'raceType',
          'linkType', 'validityPeriodEnd', 'validityPeriodStart'));
        this.snackBar.open(`Icon Deleted.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }

  onRaceTypeChanged(): void {
    this.hrQuickLink.raceType = this.form.value.raceType;
  }

  onLinkTypeChanged(): void {
    this.hrQuickLink.linkType = this.form.value.linkType;
  }

  handleDateUpdate(data: DateRange) {
    this.hrQuickLink.validityPeriodStart = data.startDate;
    this.hrQuickLink.validityPeriodEnd = data.endDate;
  }
}
