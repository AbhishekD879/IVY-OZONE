import {Component, OnInit} from '@angular/core';
import {HttpResponse} from '@angular/common/http';

import {BrandsAPIService} from '../service/brands.api.service';
import {Brand} from '../../../client/private/models';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import {AddBrandComponent} from '../add-brand/add-brand.component';
import {DialogService} from '../../../shared/dialog/dialog.service';
import {ActiveInactiveExpired} from '../../../client/private/models/activeInactiveExpired.model';
import {DataTableColumn} from '../../../client/private/models/dataTableColumn';
import {AppConstants} from '../../../app.constants';
import {Order} from '../../../client/private/models/order.model';

@Component({
  selector: 'brands-list',
  templateUrl: './brands-list.component.html',
  styleUrls: ['./brands-list.component.scss']
})
export class BrandsListComponent implements OnInit {
  brandsData: Array<Brand>;
  getDataError: string;
  searchField: string = '';
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Title',
      property: 'title',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Brand Code',
      property: 'brandCode'
    },
    {
      name: 'Disabled',
      property: 'disabled',
      type: 'boolean'
    }
  ];

  filterProperties: Array<string> = [
    'title'
  ];

  constructor(
    public snackBar: MatSnackBar,
    private dialogService: DialogService,
    private dialog: MatDialog,
    private brandsAPIService: BrandsAPIService
  ) {}

  createBrand(): void {
    const dialogRef = this.dialog.open(AddBrandComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {}
    });

    dialogRef.afterClosed().subscribe(newBrand => {
      if (newBrand) {
        this.brandsAPIService.createBrand(newBrand)
          .map((brand: HttpResponse<Brand>) => {
            return brand.body;
          })
          .subscribe((brand: Brand) => {
            if (brand) {
              this.brandsData.push(brand);
              this.dialogService.showNotificationDialog({
                title: 'Save Completed',
                message: 'Brand is Created and Stored.'
              });
            }
          });
      }
    });
  }

  get brandsAmount(): ActiveInactiveExpired {
    const activeBrands = this.brandsData && this.brandsData.filter(brand => brand.disabled === false);
    const activePromosAmount = activeBrands && activeBrands.length;
    const inactiveBrandsAmount = this.brandsData.length - activePromosAmount;

    return {
      active: activePromosAmount,
      inactive: inactiveBrandsAmount
    };
  }

  /**
   * handle deleting brand
   * @param {Brand} brand
   */
  removeBrand(brand: Brand): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Brand',
      message: 'Are You Sure You Want to Remove Brand?',
      yesCallback: () => {
        this.sendRemoveRequest(brand);
      }
    });
  }

  /**
   * Send DELETE API request
   * @param {Brand} brand
   */
  sendRemoveRequest(brand: Brand): void {
    this.brandsAPIService.deleteBrand(brand.id)
      .subscribe((data: any) => {
        this.brandsData.splice(this.brandsData.indexOf(brand), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Brand is Removed.'
        });
      });
  }

  reorderHandler(newOrder: Order): void {

    this.brandsAPIService.postNewBrandsOrder(newOrder)
      .subscribe(() => {
        this.snackBar.open('Brands Order Saved!', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
    });
  }

  ngOnInit(): void {
    this.brandsAPIService.getBrandsListData()
      .subscribe((data: any) => {
        this.brandsData = data.body;
      }, error => {
        this.getDataError = error.message;
      });
  }
}
