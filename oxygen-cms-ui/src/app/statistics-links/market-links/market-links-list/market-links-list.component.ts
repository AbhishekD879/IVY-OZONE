import { Component, OnInit, OnDestroy } from '@angular/core';
import { MarketLink } from '@root/app/client/private/models/marketLink.model';
import { DataTableColumn } from '@root/app/client/private/models';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { AppConstants } from '@root/app/app.constants';
import { MarketLinksCreateComponent } from '../market-links-create/market-links-create.component';
import { StatisticLinksService } from '../../service/statistic-links.service';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { ActiveInactiveExpired } from '@root/app/client/private/models/activeInactiveExpired.model';
import { HttpResponse } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'app-market-links-list',
  templateUrl: './market-links-list.component.html',
  styleUrls: ['./market-links-list.component.scss']
})
export class MarketLinksListComponent implements OnInit, OnDestroy {
  marketLinksData: MarketLink[] = [];
  searchField: string = '';
  getDataError: string = undefined;

  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Market name',
      property: 'marketName',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Link name',
      property: 'linkName'
    },
    {
      name: 'Tab key',
      property: 'tabKey'
    },
    {
      name: 'Overlay Key',
      property: 'overlayKey'
    },
    {
      name: 'Enabled',
      property: 'enabled',
      type: 'boolean'
    }
  ];
  filterProperties: Array<string> = [
    'marketName'
  ];

  private linksListSubscription$: Subscription;
  private createLinkSubscription$: Subscription;
  private removeLinkSubscription$: Subscription;

  constructor(
    public snackBar: MatSnackBar,
    private dialog: MatDialog,
    private router: Router,
    private statisticLinksService: StatisticLinksService,
    private dialogService: DialogService
  ) { }

  get linksAmount(): ActiveInactiveExpired {
    const activeLinks = this.marketLinksData && this.marketLinksData.filter(link => link.enabled);
    const activeLinksAmount = activeLinks && activeLinks.length;
    const inactiveLinksAmount = this.marketLinksData.length - activeLinksAmount;

    return {
      active: activeLinksAmount,
      inactive: inactiveLinksAmount
    };
  }

  ngOnInit(): void {
    this.linksListSubscription$ = this.statisticLinksService.getMarketLinksList()
      .subscribe((data: any) => {
        this.marketLinksData = data.body;
      }, error => {
        this.getDataError = error.message;
      });
  }

  ngOnDestroy(): void {
    this.linksListSubscription$ && this.linksListSubscription$.unsubscribe();
    this.createLinkSubscription$ && this.createLinkSubscription$.unsubscribe();
    this.removeLinkSubscription$ && this.removeLinkSubscription$.unsubscribe();
  }

  createLeagueLink(): void {
    const dialogRef = this.dialog.open(MarketLinksCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {}
    });

    dialogRef.afterClosed().subscribe(newMarketLink => {
      if (newMarketLink) {
        this.createLinkSubscription$ = this.statisticLinksService.createMarketLink(newMarketLink)
          .map((marketLink: HttpResponse<MarketLink>) => {
            return marketLink.body;
          })
          .subscribe((marketLink: MarketLink) => {
            if (marketLink) {
              this.marketLinksData.push(marketLink);
              this.router.navigate([`/statistics-links/market-links/${marketLink.id}`]);
            }
          });
      }
    });
  }

  /**
   * handle deleting market link
   * @param {LeagueLink} link
   */
  removeLink(link: MarketLink): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Market Link',
      message: 'Are You Sure You Want to Remove Market Link?',
      yesCallback: () => {
        this.sendRemoveRequest(link);
      }
    });
  }

  /**
   * Send DELETE API request
   * @param {MarketLink} link
   */
  sendRemoveRequest(link: MarketLink): void {
    this.removeLinkSubscription$ = this.statisticLinksService.deleteMarketLink(link.id)
      .subscribe((data: any) => {
        this.marketLinksData.splice(this.marketLinksData.indexOf(link), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Market Link is Removed.'
        });
      });
  }
}
