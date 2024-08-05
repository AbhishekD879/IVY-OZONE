import {Component, OnInit, ViewChild} from '@angular/core';

import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {ActivatedRoute, Router} from '@angular/router';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {HttpResponse} from '@angular/common/http';
import {AppConstants} from '@app/app.constants';
import {CampaignApiService} from '@app/timeline/service/campaign-api.service';
import {Campaign, CampaignStatus} from '@app/client/private/models/campaign.model';
import {DateRange} from '@app/client/private/models/dateRange.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatSelectChange } from '@angular/material/select';

@Component({
  selector: 'campaign-edit',
  styleUrls: ['./campaign-edit-component.scss'],
  templateUrl: './campaign-edit.component.html'
})
export class CampaignEditComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons;
  campaign: Campaign;

  breadcrumbsData: Breadcrumb[];
  id: string;
  getDataError: string;

  campaignStatusesRef = CampaignStatus;
  campaignStatuses(): Array<string> {
    return Object.keys(this.campaignStatusesRef);
  }

  constructor(private campaignApiService: CampaignApiService,
              private route: ActivatedRoute,
              private router: Router,
              private dialogService: DialogService,
              private snackBar: MatSnackBar) {
  }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');
    this.loadInitialData();
  }

  setStatus(status: MatSelectChange) {
    this.campaign.status = status.value;
  }

  isValidModel(campaign: Campaign): boolean {
    const idValid: boolean = campaign.id.length > 0;
    const titleValid: boolean = campaign.name.trim().length > 0;
    const displayFromValid: boolean = campaign.displayFrom.trim().length > 0;
    const displayToValid: boolean = campaign.displayTo.trim().length > 0;
    const initialNumberOfMessagesValid: boolean = campaign.messagesToDisplayCount !== undefined;

    return idValid && titleValid && displayFromValid && displayToValid && initialNumberOfMessagesValid;
  }

  private loadInitialData(): void {
    this.campaignApiService.getCampaign(this.id).subscribe((resp: any) => {
      this.campaign = resp.body;

      this.breadcrumbsData = [{
        label: `Campaigns`,
        url: `/timeline/campaign`
      }, {
        label: this.campaign.name,
        url: `/timeline/campaign/edit/${this.campaign.id}`
      }];
    }, error => {
      this.getDataError = error.message;
    });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeCampaign();
        break;
      case 'save':
        this.saveCampaignChanges();
        this.campaign.isChanged = false;
        break;
      case 'revert':
        this.revertCampaignChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  private removeCampaign(): void {
    this.campaignApiService.deleteCampaign(this.campaign.id)
      .subscribe((data: any) => {
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Campaign is Removed.'
        });
        this.router.navigate(['/timeline/campaign']);
      });
  }

  handleDisplayDateUpdate(data: DateRange): void {
    this.campaign.displayFrom = new Date(data.startDate).toISOString();
    this.campaign.displayTo = new Date(data.endDate).toISOString();
  }

  private saveCampaignChanges(): void {
    this.campaignApiService.updateCampaign(this.campaign)
      .map((response: HttpResponse<Campaign>) => {
        return response.body;
      })
      .subscribe((data: Campaign) => {
        this.campaign = data;
        this.actionButtons.extendCollection(this.campaign);
        this.showNotification('Campaign Changes are Saved.');
      });
  }

  showNotification(message): void {
    this.snackBar.open(message, 'Ok!', {
      duration: AppConstants.HIDE_DURATION,
    });
  }

  private revertCampaignChanges(): void {
    this.loadInitialData();
  }

  goToPostsPage() {
    this.router.navigateByUrl(`/timeline/post/by-campaign/${this.campaign.id}`);
  }

  goToSpotlightPostsPage() {
    this.router.navigateByUrl(`/timeline/post/spotlight/by-campaign/${this.campaign.id}`);
  }

  republishPosts() {
    this.campaignApiService.republishPosts(this.campaign.id)
      .subscribe(response => this.dialogService.showNotificationDialog({
          title: 'Republishing Completed',
          message: 'Posts have been sucessfully republished'
        }),
        error => this.getDataError = error.message
      );
  }
}
