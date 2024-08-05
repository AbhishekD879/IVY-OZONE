import { Component, OnInit, ViewChild, OnDestroy } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { LeagueLink } from '@root/app/client/private/models';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { StatisticLinksService } from '../../service/statistic-links.service';
import { HttpResponse } from '@angular/common/http';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'app-league-links-edit',
  templateUrl: './league-links-edit.component.html',
  styleUrls: ['./league-links-edit.component.scss']
})
export class LeagueLinksEditComponent implements OnInit, OnDestroy {
  getDataError: string;
  public leagueLink: LeagueLink;
  public breadcrumbsData: Breadcrumb[];
  public pattern = /^(\s*|\d+)$/;
  @ViewChild('actionButtons') actionButtons;
  private routeSubscription$: Subscription;
  private linkSubscription$: Subscription;
  private removeLinkSubscription$: Subscription;
  private saveLinkSubscription$: Subscription;
  private linksListSubscription$: Subscription;
  couponIdsOptions: Array<number> = [];

  constructor(
    private activatedRoute: ActivatedRoute,
    private dialogService: DialogService,
    private router: Router,
    private statisticLinksService: StatisticLinksService
  ) { }

  ngOnInit(): void {
    this.loadInitData();
    this.loadInitDataLinksData();
  }

  ngOnDestroy(): void {
    this.routeSubscription$ && this.routeSubscription$.unsubscribe();
    this.linkSubscription$ && this.linkSubscription$.unsubscribe();
    this.removeLinkSubscription$ && this.removeLinkSubscription$.unsubscribe();
    this.saveLinkSubscription$ && this.saveLinkSubscription$.unsubscribe();
    this.linksListSubscription$ && this.linksListSubscription$.unsubscribe();
  }

  updateCouponIds(values: Array<number>): void {
    this.leagueLink.couponIds = values;
  }

  saveChanges(): void {
    this.saveLinkSubscription$ = this.statisticLinksService
        .putLeagueLinkChanges(this.leagueLink)
        .map((leagueLink: HttpResponse<LeagueLink>) => {
          return leagueLink.body;
        })
        .subscribe((leagueLink: LeagueLink) => {
          this.leagueLink = leagueLink;
          this.actionButtons.extendCollection(this.leagueLink);
          this.dialogService.showNotificationDialog({
            title: `League Link`,
            message: `League Link is Saved`
          });
    });
  }

  revertChanges(): void {
    this.loadInitData();
  }

  removeLeagueLink(): void {
    this.removeLinkSubscription$ = this.statisticLinksService.deleteLeagueLink(this.leagueLink.id)
        .subscribe(() => {
      this.router.navigate(['/statistics-links/league-links']);
    });
  }

  isValidForm = (leagueLink: LeagueLink) => {
    return leagueLink.linkName.length > 0 &&
    this.isCorrectName(leagueLink.linkName) &&
    leagueLink.couponIds.length > 0 &&
    !!leagueLink.dhLeagueId &&
    !!leagueLink.obLeagueId &&
    this.isNumber(leagueLink.dhLeagueId) &&
    this.isNumber(leagueLink.obLeagueId);
  }

  isCorrectName(value: string): boolean {
    return (/^[A-Za-z][A-Za-z0-9]*/ as RegExp).test(value);
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeLeagueLink();
        break;
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  public isNumber(value: any): boolean {
    return this.pattern.test(value);
  }

  private loadInitData(): void {
    this.getDataError = '';

    this.routeSubscription$ = this.activatedRoute.params.subscribe((params: Params) => {
      this.linkSubscription$ = this.statisticLinksService.getSingleLeagueLink(params['id'])
        .map((leagueLink: HttpResponse<LeagueLink>) => {
          return leagueLink.body;
        })
        .subscribe((leagueLink: LeagueLink) => {
          this.leagueLink = leagueLink;
          this.breadcrumbsData = [{
            label: `League Links`,
            url: `/statistics-links/league-links`
          }, {
            label: this.leagueLink.linkName,
            url: `/statistics-links/league-links/${this.leagueLink.id}`
          }];
        }, error => {
            this.getDataError = error.message;
        });
    });
  }

  private loadInitDataLinksData() {
    this.linksListSubscription$ = this.statisticLinksService.getLeagueLinksList()
      .subscribe((data: any) => {
        this.getDefaultCouponIdsList(data.body);
      });
  }

  private getDefaultCouponIdsList(leagueLinksData: LeagueLink[]): void {
    const couponIds = leagueLinksData.reduce((acc, x) => acc.concat(x.couponIds), []);
    this.couponIdsOptions = couponIds.filter((value, index, self) => self.indexOf(value) === index);
  }

}
