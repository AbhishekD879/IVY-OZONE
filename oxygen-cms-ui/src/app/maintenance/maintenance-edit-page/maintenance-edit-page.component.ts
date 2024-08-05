import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {HttpResponse} from '@angular/common/http';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';

import {DialogService} from '../../shared/dialog/dialog.service';
import {MaintenancePage} from '../../client/private/models/maintenancepage.model';
import {GlobalLoaderService} from '../../shared/globalLoader/loader.service';
import {ApiClientService} from '../../client/private/services/http';
import {DateRange} from '../../client/private/models/dateRange.model';
import {Breadcrumb} from '../../client/private/models/breadcrumb.model';
import {AppConstants} from '../../app.constants';
import * as _ from 'lodash';

@Component({
  templateUrl: './maintenance-edit-page.component.html',
  styleUrls: ['./maintenance-edit-page.component.scss'],
  providers: [
    DialogService
  ]
})
export class MaintenanceEditPageComponent implements OnInit {

  public isLoading: boolean = false;
  public maintenancePage: MaintenancePage;

  public form: FormGroup;

  public breadcrumbsData: Breadcrumb[];

  @ViewChild('actionButtons') actionButtons;

  constructor(
    private router: Router,
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,
    private activatedRoute: ActivatedRoute,
    private dialogService: DialogService,
    private snackBar: MatSnackBar) { }

  ngOnInit(): void {
    this.form = new FormGroup({
      pageName: new FormControl('', [Validators.required]),
      pageTargetUri: new FormControl('', [Validators.required])
    });

    this.loadInitData();
  }

  private loadInitData(isLoading: boolean = true): void {
    this.globalLoaderService.showLoader();
    this.isLoading = isLoading;

    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService
          .maintenance()
          .getById(params['id'])
          .map((maintenancePage: HttpResponse<MaintenancePage>) => {
            return maintenancePage.body;
          }).subscribe((maintenancePage: MaintenancePage) => {
            this.maintenancePage = maintenancePage;
            this.breadcrumbsData = [{
              label: `Maintenance`,
              url: `/maintenance`
            }, {
              label: this.maintenancePage.name,
              url: `/maintenance/${this.maintenancePage.id}`
            }];
            this.globalLoaderService.hideLoader();
            this.isLoading = false;
          }, () => {
            this.globalLoaderService.hideLoader();
            this.isLoading = false;
          });
    });
  }

  handleDateUpdate(data: DateRange): void {
    this.maintenancePage.validityPeriodStart = data.startDate;
    this.maintenancePage.validityPeriodEnd = data.endDate;
  }

  removePage(): void {
    this.apiClientService.maintenance()
      .remove(this.maintenancePage.id)
      .subscribe(() => {
        this.router.navigate(['/maintenance']);
      });
  }

  revertChanges(): void {
    this.loadInitData();
  }

  saveChanges(): void {
    this.apiClientService.maintenance()
      .edit(this.maintenancePage)
      .map((response: HttpResponse<MaintenancePage>) => {
        return response.body;
      })
      .subscribe((page: MaintenancePage) => {
        this.maintenancePage = page;
        this.actionButtons.extendCollection(this.maintenancePage);
        this.dialogService.showNotificationDialog({
          title: `Maintenance Page`,
          message: `Maintenance Page is Saved.`
        });
      });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removePage();
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

  public isValidForm(maintenancePage: MaintenancePage): boolean {
    return maintenancePage.name && maintenancePage.name.length > 0 &&
            maintenancePage.targetUri && maintenancePage.targetUri.length > 0;
  }

  public uploadImageHandler(file) {
    this.globalLoaderService.showLoader();
    this.apiClientService.maintenance()
      .uploadImage(this.maintenancePage.id, file)
      .map((data: HttpResponse<MaintenancePage>) => {
        return data.body;
      })
      .subscribe((data: MaintenancePage) => {
        this.maintenancePage = _.extend(data, _.pick(this.maintenancePage, 'desktop', 'mobile', 'tablet', 'name',
          'targetUri', 'validityPeriodEnd', 'validityPeriodStart'));
        this.snackBar.open(`Image Uploaded.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  public removeImageHandler() {
    this.globalLoaderService.showLoader();
    this.apiClientService.maintenance()
      .removeImage(this.maintenancePage.id)
      .map((data: HttpResponse<MaintenancePage>) => {
        return data.body;
      })
      .subscribe(data => {
        this.maintenancePage = _.extend(data, _.pick(this.maintenancePage, 'desktop', 'mobile', 'tablet', 'name',
          'targetUri', 'validityPeriodEnd', 'validityPeriodStart'));
        this.snackBar.open(`Image Deleted.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, error => {
        console.error(error.maintenancePage);
      });
  }
}
