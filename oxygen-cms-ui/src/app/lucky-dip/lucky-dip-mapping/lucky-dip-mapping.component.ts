import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { DataTableColumn } from '@app/client/private/models';
import { DialogService } from '@app/shared/dialog/dialog.service';
import * as _ from 'lodash';
import { LUCKYDIP_MAPPING_CONST } from '@app/lucky-dip/constants/luckydip.constants';
import { ApiClientService } from '@root/app/client/private/services/http';
import { ILuckyDipMapping } from '../lucky-dip-v2.model';
import { Order } from '@app/client/private/models/order.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppConstants } from '@app/app.constants';

@Component({
  selector: 'app-lucky-dip-mapping',
  templateUrl: './lucky-dip-mapping.component.html'
})

export class LuckyDipMappingComponent {
  
  public readonly LUCKYDIP_MAPPING_CONST = LUCKYDIP_MAPPING_CONST;

  luckyDipMapping: ILuckyDipMapping[] = [];
  searchField: string = '';

  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Category/Sport ID',
      property: 'categoryId',
      width: 2,
      link: {
        hrefProperty: 'id',
        path: 'edit'
      },
      type: 'link'
    },
    {
      name: 'Active',
      property: 'active',
      type: 'boolean',
      alignment: 'center',
    }
  ];

  filterProperties: Array<string> = [
    'categoryId',
  ];

  constructor(
    public router: Router,
    private dialogService: DialogService,
    private apiClientService: ApiClientService,
    public snackBar: MatSnackBar
  ) { }

  ngOnInit(): void {
    this.getLuckyDipMappingList();
  }

  /**
   * Route to Create LuckyDip Page
   * @returns void
   */
  createLuckyDipMapping(): void {
    this.router.navigate(['lucky-dip/mapping-create']);
  }

  /**
   * handles deleting LuckyDip
   * @param {LuckyDip} LuckyDip
   */
  removeLuckyDipMapping(luckyDipMapping: ILuckyDipMapping) {
    this.dialogService.showConfirmDialog({
      title: 'Remove LuckyDipMapping',
      message: 'Are You Sure You Want to Remove LuckyDipMapping?',
      yesCallback: () => {
        this.sendRemoveRequest(luckyDipMapping);
      }
    });
  }

  /**
   * Send DELETE API request
   * @param {ILuckyDipMapping} LuckyDip
   * returns void
   */
  sendRemoveRequest(luckyDipMapping: ILuckyDipMapping): void {
    this.apiClientService.luckyDipService().deleteLuckyDipMapping(luckyDipMapping.id)
      .subscribe(() => {
        this.luckyDipMapping.splice(this.luckyDipMapping.indexOf(luckyDipMapping), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'LuckyDipMapping is Removed.'
        });
      }, error => {
        console.error(error.message);
      });
  }

  /**
   * get LuckyDipMapping List
   * returns void
   */
  getLuckyDipMappingList(): void {
    this.apiClientService
      .luckyDipService()
      .getAllLuckyDipMappingData()
      .subscribe((luckyDipMappingList: ILuckyDipMapping) => {
        this.luckyDipMapping = JSON.parse(JSON.stringify(luckyDipMappingList));
      }, error => {
        console.error(error.message);
      });
  }

  isValidCreate(): boolean
  {
    if(this.luckyDipMapping.length < 50)
    {
      return true;
    }
    return false;
  }

  public reorderHandler(order: Order) {
    this.apiClientService.luckyDipService().reOrder(order)
      .subscribe((data: any) => {
        this.snackBar.open('LuckyDip Hub Page Management Order Saved!!', 'OK!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

}

