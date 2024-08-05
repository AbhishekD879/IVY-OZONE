import { TinymceComponent } from './../../shared/tinymce/tinymce.component';
import { Component, OnInit, ViewChild } from '@angular/core';
import { Feature } from '../../client/private/models/feature.model';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { DialogService } from '../../shared/dialog/dialog.service';
import { ApiClientService } from '../../client/private/services/http/index';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { HttpResponse } from '@angular/common/http';
import { DateRange } from '../../client/private/models/dateRange.model';
import { AppConstants } from '../../app.constants';
import { MatSnackBar } from '@angular/material/snack-bar';
import * as _ from 'lodash';

@Component({
  templateUrl: './feature-edit.component.html',
  styleUrls: ['./feature-edit.component.scss']
})
export class FeatureEditComponent implements OnInit {

  public isLoading: boolean = true;
  public feature: Feature;
  @ViewChild('actionButtons') actionButtons;
  @ViewChild('htmlMarkup') editor: TinymceComponent;

  constructor(
    public snackBar: MatSnackBar,
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService
  ) { }

  ngOnInit(): void {
    this.loadInitData();
  }

  handleDateUpdate(data: DateRange) {
    this.feature.validityPeriodStart = data.startDate;
    this.feature.validityPeriodEnd = data.endDate;
  }

  public onShowModeChanged(mode): void {
    this.feature.showToCustomer = mode.value;
  }

  public revertChanges(): void {
    this.loadInitData();
  }

  public update(desc: string): void {
    this.feature.description = desc;
  }

  public uploadFeatureImage(formData: FormData): void {
    this.apiClientService
        .feature()
        .postNewFeatureImage(this.feature.id, formData)
        .map((featureResponse: HttpResponse<Feature>) => {
          return featureResponse.body;
        })
        .subscribe((feature: Feature) => {
          this.feature = _.extend(feature, _.pick(this.feature, 'shortDescription', 'description',
            'showToCustomer', 'validityPeriodEnd', 'validityPeriodStart'));
          this.snackBar.open('Image Was Uploaded.', 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
        });
  }

  public removeImage(): void {
    this.apiClientService
        .feature()
        .removeFeatureImage(this.feature.id)
        .map((featureResponse: HttpResponse<Feature>) => {
          return featureResponse.body;
        })
        .subscribe((feature: Feature) => {
          this.feature = _.extend(feature, _.pick(this.feature, 'shortDescription', 'description',
            'showToCustomer', 'validityPeriodEnd', 'validityPeriodStart'));
          this.snackBar.open('Image Was Removed.', 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
        });
  }

  public removeFeature(): void {
    this.apiClientService
        .feature()
        .remove(this.feature.id).subscribe(() => {
      this.router.navigate(['/features/']);
    });
  }

  public saveChanges(): void {
    this.apiClientService
        .feature()
        .edit(this.feature)
        .map((response: HttpResponse<Feature>) => {
          return response.body;
        })
        .subscribe((feature: Feature) => {
          this.feature = feature;
          this.actionButtons.extendCollection(this.feature);
          this.dialogService.showNotificationDialog({
            title: `Feature Saving`,
            message: `Feature is Saved.`
          });
    });
  }

  public isValidForm(feature: Feature): boolean {
    return !!(feature.title &&
      feature.title.length > 0 &&
      feature.validityPeriodStart && feature.validityPeriodStart.length > 0 &&
      feature.validityPeriodEnd && feature.validityPeriodEnd.length > 0);
  }

  private showHideSpinner(toShow: boolean = true): void {
    toShow ? this.globalLoaderService.showLoader() : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

  private loadInitData(isLoading: boolean = true): void {
    this.showHideSpinner();
    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService
      .feature()
      .getById(params['id'])
      .map((featureResponse: HttpResponse<Feature>) => {
        return featureResponse.body;
      }).subscribe((feature: Feature) => {
        this.feature = feature;
        if (this.editor) {
          this.editor.update(this.feature.description);
        }
        this.showHideSpinner(false);
      }, () => {
        this.showHideSpinner(false);
      });
    });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeFeature();
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

  public onShowToCustomerChange(value: string): void {
    this.feature.showToCustomer = value;
  }
}
