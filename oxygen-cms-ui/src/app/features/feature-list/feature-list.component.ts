import {Component, OnInit} from '@angular/core';
import {HttpResponse} from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';

import {DialogService} from '../../shared/dialog/dialog.service';
import {ApiClientService} from '../../client/private/services/http';
import {GlobalLoaderService} from '../../shared/globalLoader/loader.service';
import {Feature} from '../../client/private/models/feature.model';
import {FeatureCreateComponent} from '../feature-create/feature-create.component';
import {AppConstants} from '../../app.constants';
import {ActiveInactiveExpired} from '../../client/private/models/activeInactiveExpired.model';
import {Order} from '../../client/private/models/order.model';

@Component({
  selector: 'app-feature-list',
  templateUrl: './feature-list.component.html',
  styleUrls: ['./feature-list.component.scss']
})
export class FeatureListComponent implements OnInit {

  public isLoading: boolean = false;
  public searchField: string = '';
  public features: Feature[] = [];

  public searchableProperties: string[] = [
    'title'
  ];
  public dataTableColumns: any[] = [
    {
      name: 'Title',
      property: 'title',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Validity Period Start',
      property: 'validityPeriodStart',
      type: 'date'
    },
    {
      name: 'Validity Period End',
      property: 'validityPeriodEnd',
      type: 'date'
    },
    {
      name: 'Show To Customer',
      property: 'showToCustomer',
    }
  ];

  constructor(
    private snackBar: MatSnackBar,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService
  ) { }

  ngOnInit() {
    this.showHideSpinner();
    this.apiClientService
        .feature()
        .findAllByBrand()
        .map((features: HttpResponse<Feature[]>) => {
          return features.body;
        }).subscribe((features: Feature[]) => {
          this.features = features;
          this.showHideSpinner(false);
        }, () => {
          this.showHideSpinner(false);
        });
  }

  get featuresAmount(): ActiveInactiveExpired {
    const activePromos = this.features && this.features.filter(f => f.disabled === false);
    const activePromosAmount = activePromos && activePromos.length;
    const inactivePromosAmount = this.features.length - activePromosAmount;

    return {
      active: activePromosAmount,
      inactive: inactivePromosAmount
    };
  }

  public reorderHandler(newOrder: Order): void {

    this.apiClientService
        .feature()
        .postNewFeatureOrder(newOrder)
        .subscribe(() => {
      this.snackBar.open('Feature Order Saved!!', 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      });
    });
  }

  public createFeature(): void {
    this.dialogService.showCustomDialog(FeatureCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Feature',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (feature: Feature) => {
        this.apiClientService.feature()
            .add(feature)
            .subscribe((result: HttpResponse<Feature>) => {
          this.features.push(result.body);
          this.dialogService.showNotificationDialog({
            title: 'Save Completed',
            message: 'New Feature is Created and Stored.'
          });
        }, () => {
          console.error('Can not create feature');
        });
      }
    });
  }

  public removeFeature(feature: Feature): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Feature',
      message: 'Are You Sure You Want to Remove Feature?',
      yesCallback: () => {
        this.features = this.features.filter((l) => {
          return l.id !== feature.id;
        });
        this.apiClientService
            .feature()
            .remove(feature.id).subscribe(() => {
          this.dialogService.showNotificationDialog({
            title: 'Remove Completed',
            message: 'Feature is Removed.'
          });
        });
      }
    });
  }

  private showHideSpinner(toShow: boolean = true): void {
    toShow ? this.globalLoaderService.showLoader() : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

}
