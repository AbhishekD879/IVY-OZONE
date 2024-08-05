import { Component, OnInit } from '@angular/core';

import { Router } from '@angular/router';
import * as _ from 'lodash';
import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import { StatContentInfo, StatContentType } from '@app/client/private/models/statContentInfo.model';
import { ApiClientService } from '@root/app/client/private/services/http';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { forkJoin } from 'rxjs/observable/forkJoin';

@Component({
  selector: 'app-stat-content-list',
  templateUrl: './stat-content-list.component.html',
  styleUrls: ['./stat-content-list.component.scss']
})
export class StatContentListComponent implements OnInit {
  public searchFieldActive: string = '';
  public statContentInfoList: StatContentInfo[];
  public searchableProperties: string[] = [
    'title'
  ];
  getDataError: string;
  public multyRemoveFlag: boolean = false;

  public dataTableColumns: DataTableColumn[] = [
    {
      name: 'Title',
      property: 'title',
      link: {
        hrefProperty: 'id',
        path: 'edit'
      },
      type: 'link',
      width: 2
    },
    {
      name: 'Type',
      property: 'marketType',
      width: 2
    },
    {
      name: 'Event Id',
      property: 'eventId',
      width: 1
    },
    {
      name: 'Market Id',
      property: 'marketId',
      width: 1
    },
    {
      name: 'Start Date',
      property: 'startTime',
      type: 'date',
      width: 1
    },
    {
      name: 'End Date',
      property: 'endTime',
      type: 'date',
      width: 1
    },
    {
      name: 'Enabled',
      property: 'enabled',
      type: 'boolean',
      width: 1
    },
  ];
  constructor(
    private router: Router,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
  ) { }

  ngOnInit(): void {
    this.loadStaticalContent();
  }

  public createStatisticalContent(): void {
    this.router.navigate([`/stat-content-info/add`]);
  }

  private loadStaticalContent() {
    this.globalLoaderService.showLoader();
    this.apiClientService.statContentInfoService().
      findAllByBrand()
      .map(response => {
        return response.body;
      })
      .subscribe((data: StatContentInfo[]) => {
        this.statContentInfoList = data;
        this.statContentInfoList.forEach((item) => {
          Object.entries(StatContentType).forEach(([key, value]) => {
            if (key == item.marketType) {
              item.marketType = value;
            }
          });
        })
        this.multyRemoveFlag = true;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.getDataError = error.message;
        this.globalLoaderService.hideLoader();
      });
  }

  public removeContent(staticalContent: StatContentInfo): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Statistical Content Information',
      message: 'Are You Sure You Want to Remove Statistical Content Information?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.statContentInfoService().remove(staticalContent.id).subscribe(() => {
          this.globalLoaderService.hideLoader();
          this.statContentInfoList = this.statContentInfoList.filter(s => s.id !== staticalContent.id);
          this.dialogService.showNotificationDialog({
            title: 'Remove Completed',
            message: 'Statistical Content Information is Removed.'
          });
        });
      }
    });
  }


  removeHandlerMulty(staticalContentIds: string[]) {
    this.dialogService.showConfirmDialog({
      title: `Remove Statistical Content Informations (${staticalContentIds.length})`,
      message: 'Are You Sure You Want to Remove Statistical Content Informations?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        forkJoin(staticalContentIds.map(id => this.apiClientService.statContentInfoService().remove(id)))
          .subscribe(() => {
            staticalContentIds.forEach((id) => {
              const index = _.findIndex(this.statContentInfoList, { id: id });
              this.statContentInfoList.splice(index, 1);
            });
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }
}
