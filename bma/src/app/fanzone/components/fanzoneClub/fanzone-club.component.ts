import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { AbstractOutletComponent } from '@app/shared/components/abstractOutlet/abstract-outlet.component';
import { CmsService } from '@app/core/services/cms/cms.service';
import { FanzoneClub, IFanzoneSiteCoreBanner } from '@app/fanzone/models/fanzone.model';
import { clubErrorMsg } from '@app/fanzone/constants/fanzoneconstants';
import { FanzoneAppModuleService } from '@app/fanzone/services/fanzone-module.service';
import { ISiteCoreTeaserFromServer } from '@app/core/models/aem-banners-section.model';
import * as _ from 'underscore';
import { ISelectionType } from '@app/core/models/selectiontype.model';
import { IFilterType } from '@app/core/models/filter-type.model';
import { SiteServerService } from '@app/core/services/siteServer/site-server.service';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { IMarket } from '@app/core/models/market.model';
import { IOutcome } from '@app/core/models/outcome.model';
import { CacheEventsService } from '@app/core/services/cacheEvents/cache-events.service';
import { UpdateEventService } from '@app/core/services/updateEvent/update-event.service';
import { ChannelService } from '@app/core/services/liveServ/channel.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { PromotionsService } from '@promotions/services/promotions/promotions.service';
@Component({
  selector: 'app-fanzone-club',
  template: ``
})

export class FanzoneAppClubComponent extends AbstractOutletComponent implements OnInit {
  clubsData: FanzoneClub[];
  showLoader: boolean = true;
  errorMessage = clubErrorMsg;
  siteCoreFanzone: ISiteCoreTeaserFromServer[];
  clubBannerLink: string = '';
  promoDescriptionContentArr: ISelectionType[] = [];
  selectionIds: string[] = [];
  channelName:string = 'fanzoneClubComponent';
  constructor(
    protected changeDetectorRef: ChangeDetectorRef,
    protected cmsService: CmsService,
    protected fanzoneModuleService: FanzoneAppModuleService,
    private siteServerService: SiteServerService,
    private cacheEventsService: CacheEventsService,
    private updateEventService: UpdateEventService,
    private channelService: ChannelService,
    private pubSubService: PubSubService,
    private promotionsService: PromotionsService) {
    super();
  }

  /**
   * to do initializations
   * @returns {void}
   */
  ngOnInit(): void {
    this.initFanzoneClub();
    this.pubSubService.subscribe(this.channelName, this.pubSubService.API.OUTCOME_UPDATED, () => {
      this.changeDetectorRef.detectChanges();
    });
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.channelName);
    this.cacheEventsService.clearByName('event');
    this.pubSubService.publish('UNSUBSCRIBE_LS', 'fz-dynamic-promotion');
  }

  /**
   * to get fanzone club data
   * @returns {void}
   */
  initFanzoneClub(): void {
    this.showLoader = true;
    this.showSpinner();
    this.cmsService.getFanzoneClubs().subscribe(clubs => {
      this.clubsData = clubs;
      if (clubs.length) {
        this.fanzoneModuleService.getFanzoneImagesFromSiteCore().subscribe((response: IFanzoneSiteCoreBanner[]) => {
          if (response.length > 0) {
            const [teaserResponse] = response;
            this.siteCoreFanzone = teaserResponse.teasers ?? [];
            clubs.forEach((club) => {
              this.populatePromoData(club, club.description);

              const index = this.siteCoreFanzone.findIndex(a => a.itemId === club.bannerLink);
              if (index !== -1) {
                this.clubBannerLink = this.siteCoreFanzone[index].backgroundImage.src;
                _.extend(club, { bannerImgSrc: this.clubBannerLink });
                this.showLoader = false;
                this.hideSpinner();
                this.changeDetectorRef.detectChanges();
              }
            })
          }
        }, () => {
          this.showLoader = false;
          this.showError();
        });
      }
      this.showLoader = false;
      this.changeDetectorRef.detectChanges();
      this.hideSpinner();
    })
  }

  /**
   * HTML content is added into an array and separates all the buttons as separate element of an array
   * after checking if its a button tag or normal button string
   */
  populatePromoData(club: FanzoneClub, promoDescription: string): void {
    const promoData: string = promoDescription.replace(/contenteditable="true"/g, 'contenteditable="false"').
      replace(/<button/g, '@splitButton<button').replace(/<\/button>/g, '</button>@splitButton');
    const parsedPromoDataArr: string[] = promoData.split('@splitButton');
    this.populatePromoDescContentArr(club, parsedPromoDataArr);
  }

  /**
  * selection ids are identified from the dynamic buttons id and betPackBtn
  */
  populatePromoDescContentArr(club: FanzoneClub, parsedPromoDataArr: string[]): void {
    const dynamicPriceArr = [];
    parsedPromoDataArr.forEach((parsedPromoData: string) => {
      const dynamicBtnIdIndex = parsedPromoData.search('dynamicbtn');

      if (dynamicBtnIdIndex !== -1) {
        const dynamicPriceObj = {
          isSelectionIdAvailable: true,
          selection: parsedPromoData.substr(dynamicBtnIdIndex + 11).split('\"')[0],
          eventInfo: null
        }
        this.promoDescriptionContentArr.push(dynamicPriceObj);
        dynamicPriceArr.push(dynamicPriceObj);
        this.selectionIds.push(parsedPromoData.substr(dynamicBtnIdIndex + 11).split('\"')[0]);
      } else {
        const dynamicPriceObj = {
          isSelectionIdAvailable: false,
          htmlCont: this.promotionsService.decorateLinkAndTrust(parsedPromoData)
        }
        dynamicPriceArr.push(dynamicPriceObj);
        this.promoDescriptionContentArr.push(dynamicPriceObj);
      }
    });
    _.extend(club, { dynamicPriceButton: dynamicPriceArr });
    this.getDynamicButtonDetails(this.selectionIds);
  }

  /**
 * data is fetched and added to local obj to render in template
 */
  getDynamicButtonDetails(selectionIdList: string[]): void {
    const selectedPromoContentArr: ISelectionType[] = this.promoDescriptionContentArr;
    const filters: IFilterType = {
      includeUndisplayed: true,
      priceHistory: true,
      outcomesIds: selectionIdList
    };
    this.siteServerService.getEventsByOutcomeIds(filters, true)
      .then((eventDataResponse: ISportEvent[]) => {
        const allmarkets: IMarket[] = eventDataResponse.reduce(
          (marketAccumulator: IMarket[], eventItem: ISportEvent) => [...marketAccumulator, ...eventItem.markets], []);
        const allOutcomes: IOutcome[] = allmarkets.reduce(
          (outcomeAccumulator: IOutcome[], marketItem) => [...outcomeAccumulator, ...marketItem.outcomes], []);
        allOutcomes.forEach((outcome: IOutcome) => {
          if (filters.outcomesIds.includes(outcome.id)) {
            const selectedOutcomeIndex = selectedPromoContentArr.findIndex(selectedOutcome => (selectedOutcome.selection === outcome.id));
            const marketId = allOutcomes.find((outcomeItem: IOutcome) => outcomeItem.id === outcome.id).marketId;
            const eventId = allmarkets.find((marketItem: IMarket) => marketItem.id === marketId).eventId;
            selectedPromoContentArr[selectedOutcomeIndex].eventInfo = {
              'id': outcome.id,
              'event': eventDataResponse.find((eventItem: ISportEvent) => eventItem.id.toString() === eventId),
              'market': allmarkets.find((marketItem: IMarket) => marketItem.id === marketId),
              'outcome': outcome
            };
            this.changeDetectorRef.detectChanges();
          }
        });
        this.liveConnection();
      });
    this.changeDetectorRef.detectChanges();
  }

  /**
  * handler is called whenever data is received
  */
  liveConnection(): void {
    this.cacheEventsService.store('event', 'fz-dynamic-button', this.eventsArr());
    this.updateEventService.init();
    const channel = this.channelService.getLSChannelsFromArray(this.eventsArr());
    this.pubSubService.publish('SUBSCRIBE_LS', {
      channel,
      module: 'fz-dynamic-promotion'
    });
  }

  eventsArr() {
    const eventsArr: any = [];
    this.promoDescriptionContentArr.
      forEach((outcome: ISelectionType) => {
        if (outcome.eventInfo && outcome.eventInfo.event) {
          eventsArr.push(outcome.eventInfo.event);
        }
      });
    return eventsArr;
  }


}
