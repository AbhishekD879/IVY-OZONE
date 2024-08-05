import * as _ from 'lodash';

import {Component, OnInit} from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

import {ApiClientService} from '@app/client/private/services/http';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {Router} from '@angular/router';

import {DesktopQuickLink} from '@app/client/private/models/desktopquicklink.model';
import {DesktopQuickLinksCreateComponent} from '../desktop-quick-links-create/desktop-quick-links-create.component';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {DataTableColumn} from '@app/client/private/models/dataTableColumn';
import {HttpResponse} from '@angular/common/http';
import {AppConstants} from '@app/app.constants';
import {Order} from '@app/client/private/models/order.model';

@Component({
  templateUrl: './desktop-quick-links-list.component.html',
  styleUrls: ['./desktop-quick-links-list.component.scss']
})
export class DesktopQuickLinksListComponent implements OnInit {

  public desktopQuickLinks: Array<DesktopQuickLink>;
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
      'name': 'Uri',
      'property': 'target'
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
    this.apiClientService.desktopQuickLink()
      .findAllByBrand()
      .map((response: HttpResponse<DesktopQuickLink[]>) => {
        return response.body;
      })
      .subscribe((data: DesktopQuickLink[]) => {
        this.desktopQuickLinks = data;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.error = error.message;
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  createDesktopQuickLink() {
    this.dialogService.showCustomDialog(DesktopQuickLinksCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Desktop Quick Link',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (desktopQuickLink: DesktopQuickLink) => {
        this.globalLoaderService.showLoader();
        this.apiClientService.desktopQuickLink()
          .save(desktopQuickLink)
          .map((response: HttpResponse<DesktopQuickLink>) => {
            return response.body;
          })
          .subscribe((data: DesktopQuickLink) => {
            this.desktopQuickLinks.push(data);
            this.globalLoaderService.hideLoader();
            this.router.navigate([`/quick-links/desktop-quick-links/${data.id}`]);
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  removeHandler(desktopQuickLink: DesktopQuickLink): void {
    this.dialogService.showConfirmDialog({
      title: 'Desktop quick link',
      message: 'Are You Sure You Want to Remove Desktop Quick Link?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.desktopQuickLink()
          .delete(desktopQuickLink.id)
          .subscribe(() => {
            _.remove(this.desktopQuickLinks, {id: desktopQuickLink.id});
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
      .desktopQuickLink()
      .reorder(newOrder)
      .subscribe(() => {
        this.snackBar.open(`Desktop quick link order saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }
}
