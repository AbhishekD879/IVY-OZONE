import { Component, OnInit, ViewChild, OnDestroy } from '@angular/core';
import { MarketLink } from '@root/app/client/private/models/marketLink.model';
import { Breadcrumb } from '@root/app/client/private/models';
import { ActivatedRoute, Router, Params } from '@angular/router';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { StatisticLinksService } from '../../service/statistic-links.service';
import { HttpResponse } from '@angular/common/http';
import { Subscription } from 'rxjs/Subscription';
import { TAB_KEYS, OVERLAY_KEYS } from '../market-links.config';

@Component({
  selector: 'app-market-links-edit',
  templateUrl: './market-links-edit.component.html',
  styleUrls: ['./market-links-edit.component.scss']
})
export class MarketLinksEditComponent implements OnInit, OnDestroy {
  getDataError: string;
  public marketLink: MarketLink;
  public breadcrumbsData: Breadcrumb[];
  public tabKeys = TAB_KEYS;
  public overlayKeys = OVERLAY_KEYS;
  @ViewChild('actionButtons') actionButtons;
  private routeSubscription$: Subscription;
  private linkSubscription$: Subscription;
  private removeLinkSubscription$: Subscription;
  private saveLinkSubscription$: Subscription;

  constructor(
    private activatedRoute: ActivatedRoute,
    private dialogService: DialogService,
    private router: Router,
    private statisticLinksService: StatisticLinksService
  ) { }

  ngOnInit(): void {
    this.loadInitData();
  }

  ngOnDestroy(): void {
    this.routeSubscription$ && this.routeSubscription$.unsubscribe();
    this.linkSubscription$ && this.linkSubscription$.unsubscribe();
    this.removeLinkSubscription$ && this.removeLinkSubscription$.unsubscribe();
    this.saveLinkSubscription$ && this.saveLinkSubscription$.unsubscribe();
  }

  saveChanges(): void {
    this.saveLinkSubscription$ = this.statisticLinksService
        .putMarketLinkChanges(this.marketLink)
        .map((marketLink: HttpResponse<MarketLink>) => {
          return marketLink.body;
        })
        .subscribe((marketLink: MarketLink) => {
          this.marketLink = marketLink;
          this.actionButtons.extendCollection(this.marketLink);
          this.dialogService.showNotificationDialog({
            title: `Market Link`,
            message: `Market Link is Saved`
          });
    });
  }

  revertChanges(): void {
    this.loadInitData();
  }

  removeMarketLink(): void {
    this.removeLinkSubscription$ = this.statisticLinksService.deleteMarketLink(this.marketLink.id)
        .subscribe(() => {
      this.router.navigate(['/statistics-links/market-links']);
    });
  }

  isValidForm = (marketLink: MarketLink) => {
    return marketLink.marketName.length > 0 &&
      this.isCorrectName(marketLink.marketName) &&
      marketLink.linkName.length > 0 &&
      this.isCorrectName(marketLink.marketName);
  }

  isCorrectName(value: string): boolean {
    return (/^[A-Za-z][A-Za-z0-9]*/ as RegExp).test(value);
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeMarketLink();
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

  private loadInitData(): void {
    this.getDataError = '';

    this.routeSubscription$ = this.activatedRoute.params.subscribe((params: Params) => {
      this.linkSubscription$ = this.statisticLinksService.getSingleMarketLink(params['id'])
        .map((marketLink: HttpResponse<MarketLink>) => {
          return marketLink.body;
        })
        .subscribe((marketLink: MarketLink) => {
          this.marketLink = marketLink;
          this.breadcrumbsData = [{
            label: `Market Links`,
            url: `/statistics-links/market-links`
          }, {
            label: this.marketLink.linkName,
            url: `/statistics-links/market-links/${this.marketLink.id}`
          }];
        }, error => {
          this.getDataError = error.message;
        });
    });
  }

}
