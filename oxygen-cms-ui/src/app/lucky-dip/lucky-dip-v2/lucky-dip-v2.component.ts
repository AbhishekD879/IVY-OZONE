import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataTableColumn } from '@app/client/private/models';
import { DialogService } from '@app/shared/dialog/dialog.service';
import * as _ from 'lodash';
import { LUCKYDIP_BREADCRUMB_DATA, LUCKYDIP_ERROR_LABELS, LUCKYDIP_CONST } from '@app/lucky-dip/constants/luckydip.constants';
import { ApiClientService } from '@root/app/client/private/services/http';
import { LuckyDipCloneComponent } from '@app/lucky-dip/lucky-dip-clone/lucky-dip-clone.component';
import { AppConstants } from '@root/app/app.constants';
import { SAVE_CONFIRMATION_DIALOG } from '@root/app/racing-edp-markets/constants/racing-edp.constants';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';
import { HttpResponse } from '@angular/common/http';
import { ErrorService } from '@root/app/client/private/services/error.service';
import { LuckyDipV2 } from '../lucky-dip-v2.model';

@Component({
  selector: 'lucky-dip-v2',
  templateUrl: './lucky-dip-v2.component.html'
})

export class LuckyDipV2Component implements OnInit {
  public readonly LUCKYDIP_CONST = LUCKYDIP_CONST;
  luckyDip: LuckyDipV2[] = [];
  searchField: string = '';

  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Description',
      property: 'description',
      link: {
        hrefProperty: 'id',
        path: 'edit'
      },
      type: 'link'
    },
    {
      name: 'Lucky dip config level',
      property: 'luckyDipConfigLevel'
    },
    {
      name: 'Active',
      property: 'status',
      type: 'boolean',
      alignment: 'center',
    }
  ];

  filterProperties: Array<string> = [
    'description',
    'luckyDipConfigLevel',
  ];
  isLoading: boolean;

  constructor(
    public router: Router,
    private dialogService: DialogService,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private errorService: ErrorService
  ) { }

  ngOnInit(): void {
    this.getLuckyDipList();
  }

  /**
   * Clone the LuckyDip from the LuckyDip entries
   * @param {LuckyDipV2}
   */
  cloneLuckyDip(LuckyDip: LuckyDipV2): void {
    this.createCloneLuckyDip('clone', LuckyDip);
  }

  /**
 * Click handler for the LuckyDip creation
 */
  public createCloneLuckyDip(type?: string, LuckyDipV2Data?: LuckyDipV2): void {
    this.dialogService.showCustomDialog(LuckyDipCloneComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: SAVE_CONFIRMATION_DIALOG.title,
      yesOption: SAVE_CONFIRMATION_DIALOG.yesOption,
      noOption: SAVE_CONFIRMATION_DIALOG.noOption,
      data: { dialogType: type, dialogData: LuckyDipV2Data },
      yesCallback: (luckyDip: LuckyDipV2) => {
        this.showHideSpinner();
        this.apiClientService
          .luckyDipService()
          .createLuckyDipV2(luckyDip)
          .map((response: HttpResponse<LuckyDipV2>) => {
            return response.body;
          })
          .subscribe(
            (savedLuckyDip: LuckyDipV2) => {
              this.showHideSpinner(false);
              this.router.navigate([
                `${LUCKYDIP_BREADCRUMB_DATA.edit_url}/${savedLuckyDip.id}`,
              ]);
            },
            (error) => {
              this.showHideSpinner(false);
              this.errorService.emitError(
                LUCKYDIP_ERROR_LABELS.createLuckyDipLabel
              );
            }
          );
      },
      noCallback: (data: { cloned: boolean }) => {
        data.cloned ? this.getLuckyDipList() : '';
      }
    });
  }

  /**
   * Show or Hide spinner for the api calls
   * @param {boolean} toShow
   * @returns void
   */
  public showHideSpinner(toShow: boolean = true): void {
    toShow
      ? this.globalLoaderService.showLoader()
      : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

  /**
   * Route to Create LuckyDip Page
   * @returns void
   */
  createLuckyDip(): void {
    this.router.navigate(['/lucky-dip/create']);
  }


  /*handles deleting LuckyDip
 * @param {LuckyDip} LuckyDip
 */
  removeLuckyDip(luckyDip: LuckyDipV2) {
    this.dialogService.showConfirmDialog({
      title: 'Remove luckyDip',
      message: 'Are You Sure You Want to Remove LuckyDip?',
      yesCallback: () => {
        this.sendRemoveRequest(luckyDip);
      }
    });
  }

  /**
   * Send DELETE API request
   * @param {LuckyDip} LuckyDip
   * * @returns void
   */
  sendRemoveRequest(luckyDip: LuckyDipV2): void {
    this.apiClientService.luckyDipService().deleteLuckyDip(luckyDip.id)
      .subscribe(() => {
        this.luckyDip.splice(this.luckyDip.indexOf(luckyDip), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'LuckyDip is Removed.'
        });
      }, error => {
        console.error(error.message);
      });
  }

  /**
   * get LuckyDipList List
   * returns void
   */
  getLuckyDipList(): void {
    this.apiClientService
      .luckyDipService()
      .getAllLuckyDipData()
      .subscribe((luckyDipList: LuckyDipV2) => {
        this.luckyDip = JSON.parse(JSON.stringify(luckyDipList));
        this.showHideSpinner(false);
      },
        (error) => {
          this.errorService.emitError(LUCKYDIP_ERROR_LABELS.loadingLuckyDipLabel);
          this.showHideSpinner(false);
        }
      );
  }
}
