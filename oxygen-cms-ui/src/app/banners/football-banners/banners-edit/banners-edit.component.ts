import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {HttpResponse} from '@angular/common/http';

import {DialogService} from '../../../shared/dialog/dialog.service';
import {ApiClientService} from '../../../client/private/services/http/index';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {Football3DBanner} from '../../../client/private/models/football3dbanner.model';
import {DateRange} from '../../../client/private/models/dateRange.model';
import {Breadcrumb} from '../../../client/private/models/breadcrumb.model';
import {AppConstants} from '../../../app.constants';
import { MatSnackBar } from '@angular/material/snack-bar';
import * as _ from 'lodash';

@Component({
  selector: 'app-banners-edit',
  templateUrl: './banners-edit.component.html',
  styleUrls: ['./banners-edit.component.scss']
})
export class BannersEditComponent implements OnInit {

  public isLoading: boolean = false;
  public banner: Football3DBanner;
  public breadcrumbsData: Breadcrumb[];
  @ViewChild('actionButtons') actionButtons;

  constructor(
    public snackBar: MatSnackBar,
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService
  ) {
  }

  ngOnInit() {
    this.loadInitData();
  }

  public uploadFootballBanner(formData: FormData): void {
    this.apiClientService
        .footballBannersService()
        .postNewFootball3DBannerImage(this.banner.id, formData)
        .map((bannerResponse: HttpResponse<Football3DBanner>) => {
          return bannerResponse.body;
        })
        .subscribe((banner: Football3DBanner) => {
          this.banner = _.extend(banner, _.pick(this.banner, 'disabled', 'name', 'description',
            'displayDuration', 'validityPeriodEnd', 'validityPeriodStart'));

          this.snackBar.open('Image Was Uploaded.', 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
        });
  }

  public removeFootballBanner(): void {
    this.apiClientService
        .footballBannersService()
        .deleteFootball3DBanner(this.banner.id).subscribe(() => {
      this.router.navigate(['/banners/football-banners/']);
    });
  }

  public revertChanges(): void {
    this.loadInitData();
  }

  public saveChanges(): void {
    this.apiClientService.footballBannersService()
        .putFootball3DBannerChanges(this.banner)
        .map((response: HttpResponse<Football3DBanner>) => {
          return response.body;
        })
        .subscribe((banner: Football3DBanner) => {
          this.banner = banner;
          this.actionButtons.extendCollection(this.banner);
          this.dialogService.showNotificationDialog({
            title: `Football 3D Banner Saving`,
            message: `Football 3D Banner is Saved.`
          });
    });
  }

  public handleDateUpdate(data: DateRange): void {
    this.banner.validityPeriodStart = data.startDate;
    this.banner.validityPeriodEnd = data.endDate;
  }

  public remove(): void {
    this.apiClientService
        .footballBannersService()
        .removeFootball3DBannerImage(this.banner.id)
        .map((bannerResponse: HttpResponse<Football3DBanner>) => {
          return bannerResponse.body;
        })
        .subscribe((banner) => {
          this.banner = _.extend(banner, _.pick(this.banner, 'disabled', 'name', 'description',
            'displayDuration', 'validityPeriodEnd', 'validityPeriodStart'));

          this.snackBar.open('Image Was Removed.', 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
        });
  }

  public isValidForm(banner): boolean {
    return !!(banner.name &&
      banner.name.length > 0 &&
      banner.validityPeriodStart && banner.validityPeriodStart.length > 0 &&
      banner.validityPeriodEnd && banner.validityPeriodEnd.length > 0);
  }

  private showHideSpinner(toShow: boolean = true): void {
    toShow ? this.globalLoaderService.showLoader() : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

  private loadInitData(isLoading: boolean = true): void {
    this.showHideSpinner();
    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService.footballBannersService().getSingleFootball3DBanner(params['id'])
      .map((bannerResponse: HttpResponse<Football3DBanner>) => {
        return bannerResponse.body;
      }).subscribe((banner: Football3DBanner) => {
        this.banner = banner;
        this.breadcrumbsData = [{
          label: '3D Football Banners',
          url: '/banners/football-banners'
        }, {
          label: this.banner.name,
          url: `/banners/sport-banners/${this.banner.id}`
        }];
        this.showHideSpinner(false);
      }, () => {
        this.showHideSpinner(false);
      });
    });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeFootballBanner();
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

}
