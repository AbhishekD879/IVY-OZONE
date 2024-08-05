import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { GamingService } from '@core/services/sport/gaming.service';

import { ICoupon } from '@sb/components/couponsListSportTab/coupons.model';
import { Subscription } from 'rxjs';

@Component({
  selector: 'coupons-list-sport-tab',
  templateUrl: 'coupons-list-sport-tab.component.html'
})
export class CouponsListSportTabComponent implements OnInit, OnDestroy {
  @Input() sport: { coupons: Function };

  couponsList: ICoupon[] = [];
  isResponseError: boolean = false;
  isLoaded: boolean = false;

  private sportsConfigSubscription: Subscription;

  constructor(
    private sportsConfigService: SportsConfigService,
    private activatedRoute: ActivatedRoute,
    private routingState: RoutingState
  ) {}

  ngOnInit(): void {
    this.loadCouponsData();
  }

  ngOnDestroy(): void {
    this.sportsConfigSubscription && this.sportsConfigSubscription.unsubscribe();
  }

  /**
   * Load Coupons Data
   */
  private loadCoupons(): void {
    this.isLoaded = false;
    this.isResponseError = false;

    this.sport.coupons().then((coupons: ICoupon[]) => {
      this.couponsList = coupons;
      this.isLoaded = true;
      this.isResponseError = false;
    }).catch(error => {
      this.loadDefaultData();
      console.warn('Coupons Data:', error && error.error || error);
    });
  }

  private loadCouponsData(): void {
    if (this.sport) {
      this.loadCoupons();
    } else {
      const sportName = this.routingState.getRouteParam('sport', this.activatedRoute.snapshot);
      if (sportName) {
        this.sportsConfigSubscription = this.sportsConfigService.getSport(sportName)
          .subscribe((sport: GamingService) => {
            this.sport = sport;
            this.loadCoupons();
          }, error => {
            this.loadDefaultData();
            console.warn('SportMain', error.error || error);
          });
      } else {
        this.loadDefaultData();
      }
    }
  }

  private loadDefaultData(): void {
    this.couponsList = [];
    this.isLoaded = true;
    this.isResponseError = true;
  }
}

