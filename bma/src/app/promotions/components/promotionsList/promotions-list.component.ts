import { Observable } from 'rxjs';
import { mergeMap } from 'rxjs/operators';
import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import * as _ from 'underscore';

import { PromotionsService } from '@promotions/services/promotions/promotions.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IPromotionsSiteCoreBanner, ISpPromotion } from '@promotions/models/sp-promotion.model';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { IPromotionsList, IPromotionSection } from '@core/services/cms/models';
import { ISiteCoreTeaserFromServer } from '@app/core/models/aem-banners-section.model';
import { IPromotion } from '@core/services/cms/models/promotion/promotion.model';
import { UserService } from '@core/services/user/user.service';
import { BonusSuppressionService } from '@core/services/BonusSuppression/bonus-suppression.service';
import { rgyellow } from '@bma/constants/rg-yellow.constant';

@Component({
  selector: 'promotions-list',
  templateUrl: './promotions-list.component.html',
  styleUrls: ['../../assets/styles/main.scss']
})
export class PromotionsListComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  @Input() promotions?: ISpPromotion[];
  @Input() isRetail?: boolean;
  @Input() skipGrouped?: boolean = false;

  validPromotions: ISpPromotion[];
  groupedPromotions: IPromotionsList;
  lastLoginStatus: boolean;
  sendGTM: Function;
  availableGroupedPromotions: boolean;
  siteCorePromotions: ISiteCoreTeaserFromServer[];
  userFlag:boolean = false;
  private readonly componentName = 'PromotionsListComponent';
  private readonly moduleName = rgyellow.PROMOTIONS;

  constructor(
    public promotionsService: PromotionsService,
    public pubSubService: PubSubService,
    public userService: UserService,
    protected bonusSuppressionService: BonusSuppressionService
  ) {
    super();
    this.lastLoginStatus = this.promotionsService.isUserLoggedIn();
    this.sendGTM = this.promotionsService.sendGTM;
  }

  ngOnInit(): void {
    this.showSpinner();
    // GetPromotions from sitecore
    this.promotionsService.getPromotionsFromSiteCore().subscribe((response: IPromotionsSiteCoreBanner[]) => {
      this.siteCorePromotions = response.length > 0 ? response[0].teasers : [];
      this.initPromotionsList();
    });
    if (this.promotions) {
      this.init();
    } else {
      this.getPromotionsRequest().subscribe((res: IPromotionsList) => {
        this.setPromotions(res);
        this.init();
      }, () => {
        this.showError();
      });
    }
    this.pubSubService.subscribe(this.componentName, this.pubSubService.API.USER_CLOSURE_PLAY_BREAK, (val) => {
      this.userFlag= val;
        });
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.componentName);
  }

  trackPromotionBy(index: number, promotion: ISpPromotion): string | any{
    return promotion.id;
  }

  trackGroupBy(index: number, group: IPromotionSection): string {
    return `${group.name}_${index}`;
  }

  private init(): void {
    this.pubSubService.subscribe(this.componentName, this.pubSubService.API.SESSION_LOGIN, () => {
        if (!this.bonusSuppressionService.checkIfYellowFlagDisabled(this.moduleName)) {
          this.bonusSuppressionService.navigateAwayForRGYellowCustomer();
        }
      this.getPromotionsRequest().subscribe((res: IPromotionsList) => {
        this.setPromotions(res);
        this.initPromotionsList();
      });
    });

    // Waits for logout - here is the main case - server unexpectedly log out User from App
    this.pubSubService.subscribe(this.componentName, [this.pubSubService.API.SESSION_LOGOUT], () => {
      this.initPromotionsList();
    });

    // start of receiving and setting promos
    this.initPromotionsList();
  }

  private initPromotionsList(): void {
    if (this.promotions) {
      const filteredByOfferIdPromotions = this.promotionsService.filterByOfferId(this.promotions);
      this.validPromotions = this.promotionsService.preparePromotions(filteredByOfferIdPromotions,
        this.siteCorePromotions);
    }

    if (this.groupedPromotions) {
      this.availableGroupedPromotions = false;

      _.each(this.groupedPromotions.promotionsBySection, section => {
        const filteredByOfferIdPromotions = this.promotionsService.filterByOfferId(section.promotions as ISpPromotion[]);

        section.availablePromotions = this.promotionsService.preparePromotions(filteredByOfferIdPromotions, this.siteCorePromotions);
        this.availableGroupedPromotions = this.availableGroupedPromotions ? this.availableGroupedPromotions
          : section.availablePromotions.length > 0;
      });
    }

    this.hideSpinner();
  }

  private setPromotions(data: IPromotionsList) {
    if (!this.skipGrouped) {
      if (data.promotionsBySection) {
        this.groupedPromotions = data;
        this.groupedPromotions.promotionsBySection.forEach((section: IPromotionSection) => {
          section.promotions = section.promotions.filter((promotion: IPromotion) => {
            return this.bonusSuppressionService.checkIfYellowFlagDisabled(this.moduleName, promotion.title);
          });
        });
      } else {
        this.promotions = data.promotions as ISpPromotion[];
      }
    }

  }

  private getPromotionsRequest(): Observable<IPromotionsList> {
    if (this.isRetail) {
      return this.promotionsService.promotionsRetailData();
    }

    return this.promotionsService.isGroupBySectionsEnabled().pipe(
      mergeMap((res: boolean) => {
        return res ? this.promotionsService.promotionsGroupedData() :
          this.promotionsService.promotionsDigitalData();
      })
    );
  }
/* Redirection for RSS based on playBreaks/self exclusion /closed account -F2P */

  setTargetUriforRss(promotion){
    if(promotion.promoKey == 'racingsuperseries' && this.userFlag) {
      return '/promotions/details/exclusion';
      }else{
        return '/'+promotion.targetUri;
      }

  } 
}
