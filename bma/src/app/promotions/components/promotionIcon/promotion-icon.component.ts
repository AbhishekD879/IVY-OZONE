import { from as observableFrom, of as observableOf, Observable } from 'rxjs';
import { mergeMap } from 'rxjs/operators';
import { Component, OnInit, OnDestroy, Input, Output, EventEmitter, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import * as _ from 'underscore';
import { PromotionsService } from '@promotions/services/promotions/promotions.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { ISpPromotion } from '@promotions/models/sp-promotion.model';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { DRILLDOWNTAGNAMES } from '@promotions/constants/tag-names-config.constant';
import { gaTrackingSignPostingConfig} from '@app/lazy-modules/racingConstants/racing.constants';
import { ILazyComponentOutput } from '@app/shared/components/lazy-component/lazy-component.model';
import { DeviceService } from '@frontend/vanilla/core';
@Component({
  selector: 'promotion-icon',
  templateUrl: './promotion-icon.component.html',
  styleUrls: ['./promotion-icon.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PromotionIconComponent implements OnInit, OnDestroy {

  @Input() type: string;
  @Input() eventId: number;
  @Input() display: string;
  @Input() mode: string = 'md';
  @Input() typeId: number | string;
  @Input() cashoutAvailable?: boolean = false;
  @Input() buildYourBetAvailable: boolean;
  @Input() isGpAvailable: boolean;
  @Input() bogIconStyle: boolean;
  @Input() isHeaderBIRAvailable: boolean = false;
  @Input() showBIRSignPost: boolean = true;
  @Input() eventDrillDownTags: string;
  @Input() isAnyIconAvailable: boolean = false;
  @Input() accordionTitle?: any;
  @Input() sport?: any;
  @Input() marketName?: string;
  @Input() disablePopUp?: boolean = false;
  @Input() eventName?: string = '';
  @Input() isTwoUpSettlementDone?:number = -1;

  @Output() readonly setPromotionIconStatus: EventEmitter<boolean> = new EventEmitter<boolean>();

  iconsCount: number = 0;
  isPromoSignpostingEnabled: boolean = false;
  available: boolean = false;
  promoIcons: ISpPromotion[] = [];
  signPostFilteredObj:ISpPromotion[] = [];
  isFlagChecked: boolean = false;
  isBYBChecked: boolean = false;
  isBogCmsEnabled: boolean = false;
  singleSignPost:boolean=false;
  mulSignPosts:boolean=true;
  signflag:boolean=true;
  signPost:string[]=[];
  BOG_MARKET_FLAG: string = 'MKTFLAG_BOG';
  protected readonly BIR_FLAG: string = DRILLDOWNTAGNAMES.HR_BIR;
  protected BIR_PromoIcon: ISpPromotion;
  private componentName;
  signpostIconDisplay: string;
  public isMobile: boolean;

  constructor(
    protected cmsService: CmsService,
    private promotionsService: PromotionsService,
    private pubSubService: PubSubService,
    private coreToolsService: CoreToolsService,
    private commandService: CommandService,
    private changeDetectorRef: ChangeDetectorRef,
    protected device: DeviceService,
  ) {
    this.componentName = `PromotionIconComponent${this.coreToolsService.uuid()}`;
    this.isMobile = this.device.isMobile;
  }

  checkBybIcon(): Observable<any|boolean> {
    // Check if Byb icon available for Featured module
    if (this.buildYourBetAvailable !== undefined) {
      if (this.buildYourBetAvailable) {
        this.updateIconsCount(1);
        this.signPost.push('buildYourBetAvailable');
      }
      return observableOf(this.buildYourBetAvailable);
    }

    if (!this.typeId) {
      return observableOf(this.buildYourBetAvailable);
    }
    // Check if Byb icon available for other places

    if (this.eventId) {
      return observableFrom(this.commandService
        .executeAsync(this.commandService.API.DS_WHEN_YC_READY, ['isEnabledYCIcon', true], {}))
        .pipe(mergeMap(() => observableFrom(this.commandService
          .executeAsync(this.commandService.API.DS_IS_AVAILABLE_FOR_EVENTS, [this.eventId], {}))));
    }

    return observableFrom(this.commandService
      .executeAsync(this.commandService.API.DS_WHEN_YC_READY, ['isEnabledYCIcon', true], {}))
      .pipe(mergeMap(() => observableFrom(this.commandService
        .executeAsync(this.commandService.API.DS_IS_AVAILABLE_FOR_COMPETITION, [this.typeId], {}))));
  }

  lazyPromotionComponentLoaded() {
    this.changeDetectorRef.markForCheck();
  }

  /**
   * OnInit controller function
   */
  ngOnInit(): void {
    if (this.cashoutAvailable) {
      this.updateIconsCount(1);
      this.signPost.push('cashoutAvailable');
    }

    this.cmsService.getToggleStatus('PromoSignposting')
      .subscribe((toggleStatus: boolean) => {
        this.isPromoSignpostingEnabled = toggleStatus;

        if (!this.isPromoSignpostingEnabled) {
          return;
        }

        this.pubSubService.subscribe(
            this.componentName, this.pubSubService.API.SESSION_LOGIN, () => this.processFlags()
        );
        this.processFlags();
      }, () => {}, () => {
        this.isFlagChecked = true;
        this.changeDetectorRef.markForCheck();
      });

    this.checkBybIcon().subscribe((isByBAvailable: boolean) => {
      this.buildYourBetAvailable = isByBAvailable;
      if (!this.buildYourBetAvailable) {
        return;
      }
      this.updateIconsCount(1);
    }, () => {}, () => {
      this.isBYBChecked = true;
      this.changeDetectorRef.markForCheck();
    });

    if (this.isGpAvailable) {
      this.cmsService.isBogFromCms().subscribe((isBog: boolean) => {
        this.updateIconsCount(1);
        this.isBogCmsEnabled = isBog;
        this.signPost.push('isGpAvailable');
      });
    }
  }

  /**
   * Destructor
   */
  ngOnDestroy(): void {
    if (this.isPromoSignpostingEnabled) {
      this.pubSubService.unsubscribe(this.componentName);
    }
  }

  /**
   * On click promotion icon action
   * @param event
   * @param {Object} icon
   */
  iconAction(event: MouseEvent, icon: ISpPromotion, flag: string = null): void {
    event.stopPropagation();
    event.preventDefault();
    const type = icon['templateMarketName'] === this.marketName ? this.marketName : icon[`${this.type}LevelFlag`];
    const iconFlag = flag || type;
    this.pubSubService.publish(this.pubSubService.API.TWO_UP_TRACKING, { action: 'open', eventName: this.eventName, marketName: this.marketName });
    this.promotionsService.openPromotionDialog(iconFlag);
    iconFlag && gaTrackingSignPostingConfig[iconFlag] && this.promotionsService.trackSignPosting(icon.title, iconFlag, icon.marketLevelFlag);
  }

  /**
   * On icon count updated from lazy icon component
   * @param {ILazyComponentOutput} event
   */ 
  handleLazyPromotionIconEvent(event: ILazyComponentOutput): void {
    if(event.output === 'iconCountUpdated') {
      this.updateIconsCount(event.value);
      this.changeDetectorRef.detectChanges();
    }
  }

  trackByPromoIcon(index: number, item: ISpPromotion): string {
    return `${index}${item.flagName}${item.iconId}${item.promoKey}`;
  }

  /**
   * On click bog icon action
   */
  bogAction(event: MouseEvent): void {
    event.stopPropagation();
    event.preventDefault();
    this.promotionsService.openPromotionDialog(this.BOG_MARKET_FLAG);
    this.promotionsService.trackBogDialog(this.BOG_MARKET_FLAG, 'ok');
  }

  /**
   * Find promotion icons
   */
  private processFlags(): void {
    this.available = false;
    const previousPromoIconsCount = this.promoIcons.length;
    const promoIcons = this.promoIcons = [];
    const index = this.signPost.indexOf('#two-up');
    if (index > -1) {
      this.signPost.splice(index, 1);
    }
    const flags = this.parseFlags(this.display);
    this.promotionsService.getSpPromotionData()
      .subscribe((data: ISpPromotion[]) => {
        if ((this.isHeaderBIRAvailable || this.showBIRSignPost) && !this.BIR_PromoIcon) {
          this.BIR_PromoIcon = data.find((promo: ISpPromotion) => promo['eventLevelFlag'] === this.BIR_FLAG);
        }
        _.each(flags, (flagName: string) => {
          _.each(data, (promo: ISpPromotion) => {
            if ((promo['marketName'] && promo['marketName'].includes(this.marketName)) || promo[`${this.type}LevelFlag`] === flagName) {
              if (!this.signPost.includes('#two-up')) {
                promoIcons.push(promo);
                this.signPost.push(promo.iconId);
                this.available = true;
                this.setPromotionIconStatus.emit(this.available);
              }
            }
          });
        });
        this.promoIcons = promoIcons.filter(icon => icon.iconId);
        this.updateIconsCount(this.promoIcons.length - previousPromoIconsCount);
      });
  }

  /**
   * Parsing drilldownTagNames
   * @param {string} drilldownTagNames
   * @returns {Array} array with available flags
   */
   protected parseFlags(drilldownTagNames: string): string[] {
    return drilldownTagNames ? _.without(drilldownTagNames.split(','), '') : [];
  }

  protected updateIconsCount(iconsCount) {
    this.iconsCount += iconsCount;
    this.mode = (this.mode === 'sm' && this.iconsCount > 1) ? 'mini' : this.mode;
    if (this.accordionTitle != undefined) {
      if (this.iconsCount > 2 && this.type === 'market' && this.accordionTitle.length > 35 && this.sport === 'sport') {
        this.singleSignPost = true;
        this.mulSignPosts = false;
      }
    }
    this.changeDetectorRef.markForCheck();
    if(this.signPost[0]!='cashoutAvailable'){
      this.signpostIconDisplay=this.signPost[0];
    }else{
    this.signpostIconDisplay=this.signPost[1];
    }
    this.signPostFilter();
  }
  private mulSignPostsClick(event: Event) {
    event.stopPropagation();
    this.singleSignPost = false;
    this.mulSignPosts = true;
    this.signflag = false;
  }

  private signPostFilter() {
    if (this.signpostIconDisplay !== undefined) {
      if (this.signpostIconDisplay !== 'cashoutAvailable' && this.signpostIconDisplay !== 'buildYourBetAvailable' && this.signpostIconDisplay !== 'isGpAvailable') {
        this.promoIcons.forEach((data) => {
          if (data.iconId === this.signpostIconDisplay) {
            this.signPostFilteredObj.push(data);
          }
        });
      }
    }
  }

}
