import * as _ from 'lodash';

import {Component, OnInit} from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import {Router} from '@angular/router';

import {ApiClientService} from '../../../client/private/services/http';
import {DialogService} from '../../../shared/dialog/dialog.service';

import {HRQuickLink} from '../../../client/private/models/hrquicklink.model';
import {HrQuickLinksCreateComponent} from '../hr-quick-links-create/hr-quick-links-create.component';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {DataTableColumn} from '../../../client/private/models/dataTableColumn';
import {AppConstants} from '../../../app.constants';
import {Order} from '../../../client/private/models/order.model';

@Component({
  templateUrl: './hr-quick-links-list.component.html',
  styleUrls: ['./hr-quick-links-list.component.scss']
})
export class HrQuickLinksListComponent implements OnInit {

  public hrQuickLinks: Array<HRQuickLink>;
  public error: string;
  public searchField: string = '';
  public dataTableColumns: Array<DataTableColumn> = [
    {
      'name': 'Title',
      'property': 'title',
      'link': {
        hrefProperty: 'id'
      },
      'type': 'link'
    },
    {
      'name': 'Race Type',
      'property': 'raceType'
    },
    {
      'name': 'Link Type',
      'property': 'linkType'
    },
    {
      'name': 'Uri or Selection Id',
      'property': 'target'
    },
    {
      'name': 'Validity Period Start',
      'property': 'validityPeriodStart',
      'type': 'datetime'
    },
    {
      'name': 'Validity Period End',
      'property': 'validityPeriodEnd',
      'type': 'date'
    }
  ];
  public searchableProperties: Array<string> = [
    'title'
  ];

  constructor(
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar,
    private router: Router
  ) { }

  ngOnInit() {
    this.globalLoaderService.showLoader();
    this.apiClientService.hrQuickLink()
      .findAllByBrand()
      .map(response => {
        return response.body;
      })
      .subscribe((data: HRQuickLink[]) => {
        this.hrQuickLinks = data;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.error = error.message;
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  createHRQuickLink(): void {
    this.dialogService.showCustomDialog(HrQuickLinksCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New HR Quick Link',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (hrQuickLink: HRQuickLink) => {
        this.globalLoaderService.showLoader();
        this.apiClientService.hrQuickLink()
          .save(hrQuickLink)
          .map(response => {
            return response.body;
          })
          .subscribe((data: HRQuickLink) => {
            this.hrQuickLinks.push(data);
            this.globalLoaderService.hideLoader();
            this.router.navigate([`/quick-links/quick-links/${data.id}`]);
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  removeHandler(hrQuickLink: HRQuickLink): void {
    this.dialogService.showConfirmDialog({
      title: 'HR Quick Link',
      message: 'Are You Sure You Want to Remove HR Quick Link?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.hrQuickLink()
          .delete(hrQuickLink.id)
          .subscribe(() => {
            _.remove(this.hrQuickLinks, {id: hrQuickLink.id});
            this.globalLoaderService.hideLoader();
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  reorderHandler(newOrder: Order): void {
    this.apiClientService
      .hrQuickLink()
      .reorder(newOrder)
      .subscribe(() => {
        this.snackBar.open(`HR quick link order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }
}
