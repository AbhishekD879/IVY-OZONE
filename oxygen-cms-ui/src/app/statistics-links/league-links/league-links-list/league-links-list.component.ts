import { Component, OnInit, OnDestroy } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { LeagueLinksCreateComponent } from '../league-links-create/league-links-create.component';
import { AppConstants } from '@root/app/app.constants';
import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import { LeagueLink } from '@root/app/client/private/models';
import { ActiveInactiveExpired } from '@app/client/private/models/activeInactiveExpired.model';
import { Router } from '@angular/router';
import { StatisticLinksService } from '../../service/statistic-links.service';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HttpResponse } from '@angular/common/http';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'app-league-links-list',
  templateUrl: './league-links-list.component.html',
  styleUrls: ['./league-links-list.component.scss']
})
export class LeagueLinksListComponent implements OnInit, OnDestroy {
  leagueLinksData: LeagueLink[] = [];
  searchField: string = '';
  getDataError: string = undefined;
  couponIdsOptions: Array<number> = [];

  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Link Name',
      property: 'linkName',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'OB league ID',
      property: 'obLeagueId'
    },
    {
      name: 'Coupon IDs',
      property: 'couponIds',
      disableSorting: true
    },
    {
      name: 'DH league ID',
      property: 'dhLeagueId'
    },
    {
      name: 'Enabled',
      property: 'enabled',
      type: 'boolean'
    }
  ];
  filterProperties: Array<string> = [
    'linkName'
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
    const activeLinks = this.leagueLinksData && this.leagueLinksData.filter(link => link.enabled);
    const activeLinksAmount = activeLinks && activeLinks.length;
    const inactiveLinksAmount = this.leagueLinksData.length - activeLinksAmount;

    return {
      active: activeLinksAmount,
      inactive: inactiveLinksAmount
    };
  }

  ngOnInit(): void {
    this.linksListSubscription$ = this.statisticLinksService.getLeagueLinksList()
      .subscribe((data: any) => {
        this.leagueLinksData = data.body;
        this.getDefaultCouponIdsList();
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
    const dialogRef = this.dialog.open(LeagueLinksCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {
        couponIdsOptions: this.couponIdsOptions
      }
    });

    dialogRef.afterClosed().subscribe(newLeagueLink => {
      if (newLeagueLink) {
        this.createLinkSubscription$ = this.statisticLinksService.createLeagueLink(newLeagueLink)
          .map((leagueLink: HttpResponse<LeagueLink>) => {
            return leagueLink.body;
          })
          .subscribe((leagueLink: LeagueLink) => {
            if (leagueLink) {
              this.leagueLinksData.push(leagueLink);
              this.router.navigate([`/statistics-links/league-links/${leagueLink.id}`]);
            }
          });
      }
    });
  }

  /**
   * handle deleting league link
   * @param {LeagueLink} link
   */
  removeLink(link: LeagueLink): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove League Link',
      message: 'Are You Sure You Want to Remove League Link?',
      yesCallback: () => {
        this.sendRemoveRequest(link);
      }
    });
  }

  /**
   * Send DELETE API request
   * @param {LeagueLink} link
   */
  sendRemoveRequest(link: LeagueLink): void {
    this.removeLinkSubscription$ = this.statisticLinksService.deleteLeagueLink(link.id)
      .subscribe((data: any) => {
        this.leagueLinksData.splice(this.leagueLinksData.indexOf(link), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'League Link is Removed.'
        });
      });
  }

  private getDefaultCouponIdsList(): void {
    const couponIds = this.leagueLinksData.reduce((acc, x) => acc.concat(x.couponIds), []);
    this.couponIdsOptions = couponIds.filter((value, index, self) => self.indexOf(value) === index);
  }
}
