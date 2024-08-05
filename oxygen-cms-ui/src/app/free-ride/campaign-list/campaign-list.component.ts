import { Component, OnInit } from '@angular/core';
import { FreeRideAPIService } from '../services/free-ride.api.service';
import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { Router } from '@angular/router';
import * as _ from 'lodash';
import { Campaign } from '@app/client/private/models/freeRideCampaign.model';

@Component({
  selector: 'app-campaign-list',
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
        path: '/free-ride/campaign/'
      },
      type: 'link'
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

  constructor(public router: Router,
    private dialogService: DialogService,
    private freeRideAPIService: FreeRideAPIService,
    private globalLoaderService: GlobalLoaderService) { }

  ngOnInit(): void {
    this.loadCampaigns();
  }

   /**
   * Load List of Campaigns
   */
  loadCampaigns() {
    this.globalLoaderService.showLoader();
    this.freeRideAPIService.getCampaignsByBrandWithOrdering('createdAt,desc')
      .subscribe((data: any) => {
        console.log(data);
        this.campaignData = data;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.getDataError = error.message;
        this.globalLoaderService.hideLoader();
      });
    this.globalLoaderService.hideLoader();
  }

   /**
   * Remove Campaign Check
   */
  removeCampaign(campaign: Campaign) {
    if (campaign.isPotsCreated && this.isCampaignActive(campaign)) {
      this.dialogService.showNotificationDialog({
        title: 'Remove Campaign',
        message: 'Active campaign cannot be deleted'
      });
    } else {
      this.dialogService.showConfirmDialog({
        title: 'Remove Campaign',
        message: 'Are You Sure You Want to Remove Campaign?',
        yesCallback: () => {
          this.sendRemoveRequest(campaign);
        }
      });
    }
  }

  /**
   * Checks if campaign is active
   */
  isCampaignActive(campaign: Campaign): boolean {
    return (new Date().toDateString()) === (new Date(campaign.displayTo).toDateString()) &&
      (new Date(campaign.displayTo)).getTime() > (new Date()).getTime();
  }

   /**
   * Remove Campaign Call
   */
  sendRemoveRequest(campaign: Campaign) {
    this.freeRideAPIService.deleteCampaign(campaign.id)
      .subscribe((data: any) => {
        this.campaignData.splice(this.campaignData.indexOf(campaign), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Campaign is Removed.'
        });
      });
  }

   /**
   * Navigate to Campaign Edit
   */
  openCreateCampaign() {
    this.router.navigateByUrl('free-ride/campaign/create');
  }
}
