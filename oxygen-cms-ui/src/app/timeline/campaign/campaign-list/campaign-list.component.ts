import { Component, OnInit } from '@angular/core';
import {DataTableColumn} from '@app/client/private/models/dataTableColumn';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {Router} from '@angular/router';
import {forkJoin} from 'rxjs/observable/forkJoin';
import * as _ from 'lodash';
import {CampaignApiService} from '@app/timeline/service/campaign-api.service';
import {Campaign} from '@app/client/private/models/campaign.model';

@Component({
  selector: 'campaign-list',
  templateUrl: './campaign-list.component.html',
  styleUrls: ['./campaign-list.component.scss']
})
export class CampaignListComponent implements OnInit {

  campaignData: Array<Campaign>;
  searchField: string = '';
  getDataError: string;
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Name',
      property: 'name',
      link: {
        hrefProperty: 'id',
        path: 'edit'
      },
      type: 'link'
    },
    {
      name: 'Status',
      property: 'status'
    },
    {
      name: 'Start Date',
      property: 'displayFrom',
      type: 'date'
    },
    {
      name: 'End Date',
      property: 'displayTo',
      type: 'date'
    },
    {
      name: 'Last modified by',
      property: 'updatedByUserName'
    },
    {
      name: 'Created Date',
      property: 'createdAt',
      type: 'date'
    }
  ];

  filterProperties: Array<string> = [
    'name'
  ];

  paginationLimitOptions: number[] = [5, 10, 25, 50];
  paginationLimit: number = this.paginationLimitOptions[1];

  constructor(private dialogService: DialogService,
              private campaignApiService: CampaignApiService,
              private globalLoaderService: GlobalLoaderService,
              private router: Router) { }

  ngOnInit() {
    this.loadCampaigns();
  }

  loadCampaigns() {
    this.globalLoaderService.showLoader();
    this.campaignApiService.getCampaignsByBrandWithOrdering('createdAt,desc')
      .subscribe((data: any) => {
        this.campaignData = data.body;
        this.campaignData.forEach(campaign => campaign.highlighted = campaign.displayed);
        this.globalLoaderService.hideLoader();
      }, error => {
        this.getDataError = error.message;
        this.globalLoaderService.hideLoader();
      });
  }

  removeCampaign(campaign: Campaign) {
    this.dialogService.showConfirmDialog({
      title: 'Remove Campaign',
      message: 'Are You Sure You Want to Remove Campaign?',
      yesCallback: () => {
        this.sendRemoveRequest(campaign);
      }
    });
  }

  sendRemoveRequest(campaign: Campaign) {
    this.campaignApiService.deleteCampaign(campaign.id)
      .subscribe((data: any) => {
        this.campaignData.splice(this.campaignData.indexOf(campaign), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Campaign is Removed.'
        });
      });
  }

  removeHandlerMulti(campaignIds: string[]) {
    this.dialogService.showConfirmDialog({
      title: `Remove Campaigns (${campaignIds.length})`,
      message: 'Are You Sure You Want to Remove Campaigns?',
      yesCallback: () => {
        removeMultiCampaigns.call(this);
      }
    });

    function removeMultiCampaigns() {
      this.globalLoaderService.showLoader();
      forkJoin(campaignIds.map(id => this.campaignApiService.deleteCampaign(id)))
        .subscribe(() => {
          campaignIds.forEach((id) => {
            const index = _.findIndex(this.campaignData, {id: id});
            this.campaignData.splice(index, 1);
          });
          this.globalLoaderService.hideLoader();
        });
    }
  }

  openCreateCampaign() {
    this.router.navigateByUrl('timeline/campaign/create');
  }
}
