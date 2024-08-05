
import { Order } from '@app/client/private/models/order.model';
import { HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import * as _ from 'lodash';

import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { ApiClientService } from '@app/client/private/services/http';
import { TableColumn } from '@app/client/private/models/table.column.model';
import { AppConstants } from '@app/app.constants';
import { AddNavigationGroupComponent } from '@app/promotions/add-navigation-group/add-navigation-group.component';
import { PromotionsNavigationGroup } from '@app/client/private/models/promotions-navigation.model';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigations.component.html',
  styleUrls: ['./navigations.component.scss']
})
export class NavigationsComponent implements OnInit {

  public searchField: string = '';
  public isLoading: boolean = false;
  public navigationGroup: PromotionsNavigationGroup[];

  filterProperties: Array<string> = [
    'title'
  ];

  dataTableColumns: Array<TableColumn> = [
    {
      name: 'Name',
      property: 'title',
      link: {
        hrefProperty: 'id',
        path: '/promotions/navigation/'
      },
      type: 'link'
    },
    {
      name: 'Promotions IDs',
      property: 'promotionIds'
    },
    {
      name: 'Last Updated At',
      property: 'updatedAt',
      type: 'date'
    },
    {
      name: 'Enabled',
      property: 'status',
      type: 'boolean'
    }
  ];

  constructor(
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private snackBar: MatSnackBar,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.globalLoaderService.showLoader();
    this.isLoading = true;
    this.apiClientService
      .promotionsNavigationsService()
      .findAllByBrand()
      .map((data: HttpResponse<PromotionsNavigationGroup[]>) => {
        return data.body;
      }).subscribe((navigationGroup: any) => {
        this.navigationGroup = navigationGroup;
        this.hideSpinner();
      });
  }

  /**
   * Reorder offers
   * @param {newOrder} Order
   * 
   */
  reorderHandler(newOrder: Order) {
    console.log(newOrder, '$$newOrder')
    this.apiClientService
      .promotionsNavigationsService()
      .postNewPromotionsNavigationsOrder(newOrder)
      .subscribe(() => {
        this.snackBar.open('New Promotions Navigations Order Saved!!', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  /**
  * Creates New Navigation Group
  * @param null
  * @returns {this.navigationGroup} PromotionsNavigationGroup
  */
  addNavigationGroup(): void {
    this.dialogService.showCustomDialog(AddNavigationGroupComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Static Block',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (navGroupData: any) => {
        this.apiClientService.promotionsNavigationsService()
          .add(navGroupData)
          .map((result: HttpResponse<any>) => result.body)
          .subscribe((result: any) => {
            this.navigationGroup.unshift(result);
            this.router.navigate([`/promotions/navigation/${result.id}`]);
          }, () => {
            console.error('Can not create static block');
          });
      }
    });
  }


  /**
  * Removes Navigation Group
  * @param {navigationGroup} PromotionsNavigationGroup
  * @returns null
  */
  removeNavigationGroup(navigationsGroup: PromotionsNavigationGroup): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Static Block',
      message: `Are You Sure You Want to Remove Navigation Group ${navigationsGroup.title}`,
      yesCallback: () => {
        this.apiClientService
          .promotionsNavigationsService()
          .remove(navigationsGroup.id, navigationsGroup.promotionIds.length > 0 ? navigationsGroup.promotionIds : `""`).subscribe(data => {
            this.navigationGroup.splice(this.navigationGroup.indexOf(navigationsGroup), 1);
            this.dialogService.showNotificationDialog({
              title: 'Remove Completed',
              message: 'Navigation is Removed.'
            });
          });
      }
    });
  }

  private hideSpinner(): void {
    this.isLoading = false;
    this.globalLoaderService.hideLoader();
  }

}
