import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataTableColumn } from '@app/client/private/models';
import { Fanzone } from '@app/client/private/models/fanzone.model';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { FanzonesAPIService } from '@app/fanzone/services/fanzones.api.service';
import { FANZONE_LIST } from '@app/fanzone/constants/fanzone.constants';
import * as _ from 'lodash';

@Component({
  selector: 'app-fanzones',
  templateUrl: './fanzones.component.html'
})
export class FanzonesComponent implements OnInit {
  public readonly FANZONE_LIST = FANZONE_LIST;

  fanzoneData: Fanzone[] = [];
  searchField: string = '';

  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Fanzone Name',
      property: 'name',
      link: {
        hrefProperty: 'id',
        path: 'fanzone/'
      },
      type: 'link',
      width: 2
    },
    {
      name: 'Team Id',
      property: 'teamId'
    },
    {
      name: 'Competition IDs',
      property: 'primaryCompetitionId'
    },
    {
      name: 'Enabled',
      property: 'active',
      type: 'boolean'
    },
  ];

  filterProperties: Array<string> = [
    'name',
    'teamId',
    'openBetId',
    'active'
  ];

  constructor(
    public router: Router,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private fanzonesAPIService: FanzonesAPIService
  ) { }

  ngOnInit(): void {
    this.getFanzonesList();
  }

  /**
   * Route to Create Fanzone Page
   * @returns void
   */
  createFanzone(): void {
    this.router.navigate(['fanzones/create']);
  }

  /**
   * handles deleting fanzone
   * @param {Fanzone} fanzone
   */
  removeFanzone(fanzone: Fanzone) {
    this.dialogService.showConfirmDialog({
      title: 'Remove Fanzone',
      message: 'Are You Sure You Want to Remove Fanzone?',
      yesCallback: () => {
        this.sendRemoveRequest(fanzone);
      }
    });
  }

  /**
   * Removes multiple fanzones
   * @param fanzoneIds string[]
   */
  removeHandlerMulty(fanzoneIds: string[]) {
    this.dialogService.showConfirmDialog({
      title: `Remove Fanzones (${fanzoneIds.length})`,
      message: 'Are You Sure You Want to Remove Fanzones?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.fanzonesAPIService.deleteFanzone(fanzoneIds)
          .subscribe(() => {
            fanzoneIds.forEach((id) => {
              const index = this.fanzoneData.findIndex(fanzone => fanzone.id === id);
              this.fanzoneData.splice(index, 1);
            });
            this.globalLoaderService.hideLoader();
          }, error => {
            console.error(error.message);
          });
      }
    });
  }

  /**
   * Send DELETE API request
   * @param {Fanzone} fanzone
   */
  sendRemoveRequest(fanzone: Fanzone): void {
    this.fanzonesAPIService.deleteFanzone(fanzone.id)
      .subscribe((data: any) => {
        this.fanzoneData.splice(this.fanzoneData.indexOf(fanzone), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Fanzone is Removed.'
        });
      }, error => {
        console.error(error.message);
      });
  }

  /**
   * get Fanzones List
   * returns void
   */
  getFanzonesList(): void {
    this.fanzonesAPIService.getAllFanzones().subscribe((fanzoneList: any) => {
      this.fanzoneData = fanzoneList.body;
    }, error => {
      console.error(error.message);
    });
  }

}
