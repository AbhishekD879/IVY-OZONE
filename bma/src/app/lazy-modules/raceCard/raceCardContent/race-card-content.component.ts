import * as _ from 'underscore';

import { Component, OnInit, OnDestroy, ElementRef, Input, ChangeDetectorRef, SimpleChanges } from '@angular/core';
import { Router } from '@angular/router';

import { RacingGaService } from '@app/racing/services/racing-ga.service';
import { TemplateService } from '@shared/services/template/template.service';
import { CarouselService } from '@app/shared/directives/ng-carousel/carousel.service';
import { Carousel } from '@app/shared/directives/ng-carousel/carousel.class';
import { IMarket } from '@core/models/market.model';
import { RendererService } from '@shared/services/renderer/renderer.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { ISilkStyleModel } from '@core/services/raceOutcomeDetails/silk-style.model';
import { IOutcome } from '@core/models/outcome.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { RaceOutcomeDetailsService } from '@core/services/raceOutcomeDetails/race-outcome-details.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { VirtualSharedService } from '@shared/services/virtual/virtual-shared.service';
import { EventService } from '@app/sb/services/event/event.service';
import { DatePipe } from '@angular/common';
import { NextRacesHomeService } from '@lazy-modules/lazyNextRacesTab/components/nextRacesHome/next-races-home.service';
import { racing } from '@app/lazy-modules/locale/translations/en-US/racing.lang';
import { GtmService } from '@core/services/gtm/gtm.service';
import { SortByOptionsService } from '@app/racing/services/sortByOptions/sort-by-options.service';
import { NEXT_RACES_HOME_CONSTANTS } from '@app/lazy-modules/lazyNextRacesTab/constants/next-races-home.constants';
import environment from '@environment/oxygenEnvConfig';

@Component({
    selector: 'race-card-content',
    templateUrl: './race-card-content.component.html',
    styleUrls: ['../../../shared/components/raceCard/next-races.scss',
    '../../../shared/components/raceCard/next-races-carousel.scss',
    './race-card-content.component.scss'],
    providers: [CarouselService]
  })

  export class RaceCardContentComponent implements OnInit, OnDestroy {
    @Input() raceData: ISportEvent[];
    @Input() viewFullRaceText?: string;
    @Input() trackGaDesktop?: boolean;
    @Input() trackGa?: boolean;
    @Input() raceWidget?: string;
    @Input() raceIndex?: number | string;
    @Input() raceOrigin?: string = '';
    @Input() raceMaxSelections?: number;
    @Input() showTimer?: boolean;
    @Input() showBriefHeader?: boolean;
    @Input() fluid?: boolean;
    @Input() gtmModuleTitle?: string;
    @Input() hideNonRunners?: boolean;
    @Input() hostContext?: string;
    @Input() isEventOverlay?:boolean;
    @Input() showHeader?: boolean = true;
    @Input() isNextRacesModule?: boolean;
    
    disableScroll: boolean;
    showCarouselButtons: boolean;
    eventCategory: string;
    raceCarousel: string;
    isFitSize: boolean;
    terms: Array<string>;
    marketOutcomesMap: {[key: string]: IOutcome[]} = {};
    isVirtual: boolean = false;
    isRacing: boolean = true;
    seeAllRaceText: string;
    nextRacesTitle:string;
  
    private resizeListener: Function;
    private raceMarkets: string[] = [];
    private isHR: boolean;
    private channelName: string;
  
    constructor(
      private elementRef: ElementRef,
      private domTools: DomToolsService,
      public raceOutcomeData: RaceOutcomeDetailsService,
      private routingHelperService: RoutingHelperService,
      private windowRef: WindowRefService,
      private commandService: CommandService,
      protected locale: LocaleService,
      private sbFiltersService: SbFiltersService,
      private filtersService: FiltersService,
      private renderer: RendererService,
      private carouselService: CarouselService,
      private pubSubService: PubSubService,
      private router: Router,
      private templateService: TemplateService,
      private virtualSharedService: VirtualSharedService,
      private datePipe: DatePipe,
      private nextRacesHomeService: NextRacesHomeService,
      private eventService: EventService,
      private changeDetectorRef: ChangeDetectorRef,
      private gtmService: GtmService,
      private sortByOptionsService: SortByOptionsService
    ) {
      this.trackEvent = this.trackEvent.bind(this);
    }
  
    ngOnInit(): void {
      const raceWidget = this.raceWidget ? 'widget' : 'container';
      this.raceIndex = this.raceIndex || 0;
        this.raceOrigin = this.raceOrigin ? `?origin=${this.raceOrigin}` : this.isEventOverlay ? `?origin=next-races` :'';
        this.isHR = this.raceData[0]?.categoryCode === 'HORSE_RACING' || this.raceData[0]?.competitionSection?.categoryCode === 'HORSE_RACING';
        this.channelName = `RaceCardComponent${this.raceData[0]?.id ? this.raceData[0].id : ''}`;

        this.viewFullRaceText = this.locale.getString(this.viewFullRaceText || 'sb.viewFullRace');
        this.eventCategory = this.windowRef.nativeWindow.location.pathname === '/' ? 'home' : 'widget';

        this.raceCarousel = `race-carousel-${raceWidget}-${this.raceIndex}`;
        this.seeAllRaceText = this.locale.getString('sb.seeAll');
        this.nextRacesTitle = racing.nextRaces

        if (!this.isHR) {
          this.setTrapNumbers();
        }
        this.processOutcomes();

        // Generate Each Way terms for events
        this.generateEachWayTerms();

        // re-sort outcomes on price change event
        this.pubSubService.subscribe(this.channelName, this.pubSubService.API.OUTCOME_UPDATED, (market: IMarket) => {
          if (this.raceMarkets.includes(market.id)) {
            this.processOutcomes(market);
          }
        });

        this.windowRef.nativeWindow.setTimeout(() => {
          this.initShowCarouselButtons();
        }, 0);

        this.resizeListener = this.renderer.renderer.listen(this.windowRef.nativeWindow, 'resize', () => {
          this.initShowCarouselButtons();
        });

        this.isVirtual = this.raceData && this.raceData.length && this.virtualSharedService.isVirtual(this.raceData[0]?.categoryId);
    }
  
    isStreamLabelShown(event: ISportEvent): boolean {
      const liveStreamAvailable: boolean = this.eventService.isLiveStreamAvailable(event).liveStreamAvailable;
      return liveStreamAvailable;
    }
  
    generateEachWayTerms(): void {
      this.terms = [];
      _.each(this.raceData, (event: ISportEvent) => {
        if (event && event.markets && event.markets[0] && this.showEchWayTerms(event.markets[0])) {
          this.terms.push(this.generateTerms(event.markets[0]));
        }
      });
    }
  
    ngOnChanges(changes: SimpleChanges) {
      if(changes.raceData?.currentValue) {
        this.ngOnInit();
      }
    }
    ngOnDestroy(): void {
      typeof this.resizeListener === 'function' && this.resizeListener();
      this.pubSubService.unsubscribe(this.channelName);
    }
  
    isEventVirtual(event: ISportEvent): boolean {
      return this.virtualSharedService.isVirtual(event.categoryId);
    }
    /**
   * Checks if Virtual Races Available  For this Event
   * @param {ISportEvent[]} event
   * @returns {boolean} 
   */
    isVirtualSignpost(event): boolean {
     return event && event.categoryId === environment.CATEGORIES_DATA.virtuals[0].id;
    } 
    trackByEvents(i: number, event: ISportEvent): string {
      return `${event.id}_${event.name}_${event.categoryId}_${event.markets && event.markets.length}`+i;
    }
  
    trackByMarkets(i: number, market: IMarket): string {
      return `${market.id}_${market.name}_${market.marketStatusCode}`;
    }
  
    trackByOutcomes(i: number, outcome: IOutcome): string {
      return `${outcome.id}_${outcome.name}_${outcome.runnerNumber}`;
    }
  
    removeLineSymbol(name: string): string {
      return this.filtersService.removeLineSymbol(name);
    }
  
    getEventName(event: ISportEvent): string {
      if(event.categoryCode === 'VIRTUAL') {
        return event.originalName;
      }
      const name = event.localTime ? `${event.localTime} ${event.typeName}` : event.name;
      return event.nameOverride || name;
    }
  
    formEdpUrl(eventEntity: ISportEvent): string {
      if(eventEntity)
      {
      return `${this.routingHelperService.formEdpUrl(eventEntity)}${this.raceOrigin}`;
      }
    }
  
    nextRacesGATracker(event: ISportEvent, value:string) {
      this.gtmService.push('trackEvent', {
          eventID: event.id,
          eventAction: 'meetings',
          typeID: event.typeId,
          eventCategory: event.categoryId == "21" ? NEXT_RACES_HOME_CONSTANTS.HORSE_RACING_LOWERCASE : NEXT_RACES_HOME_CONSTANTS.GREYHOUNDS_LOWERCASE,
          categoryID: event.categoryId,
          eventLabel: `navigation – ${value}`,
        });
    }
  
    trackEvent(entity: ISportEvent, value?): void {
      const isVirtual = this.virtualSharedService.isVirtual(entity.categoryId);
      if (this.trackGaDesktop || isVirtual) {
        const name = entity.localTime ? `${entity.localTime} ${entity.typeName}` : entity.name;
        const eventName = entity.nameOverride || name;
  
        this.commandService.executeAsync(this.commandService.API.RACING_GA_SERVICE).then((racingGaService: RacingGaService) => {
          racingGaService.sendGTM(`full race card - ${eventName}`, this.eventCategory, entity.categoryId === '39');
        });
      }
  
      if (this.trackGa && !this.trackGaDesktop) {
        this.commandService.executeAsync(this.commandService.API.RACING_GA_SERVICE).then((racingGaService: RacingGaService) => {
          racingGaService.trackNextRace(entity.categoryName);
        });
      }
  
      const link = isVirtual ? this.virtualSharedService.formVirtualEventUrl(entity) : this.formEdpUrl(entity);
      this.router.navigateByUrl(link);
      
      if(this.isEventOverlay){
        this.nextRacesGATracker(entity, value.toLowerCase());     
        this.pubSubService.publish('MEETING_OVERLAY_FLAG',{id:entity.id,flag: false});
       }
    }
  
    showEchWayTerms(market: IMarket): boolean {
      return !!(market && market.eachWayPlaces && market.eachWayFactorDen && market.eachWayFactorNum);
    }
  
    /**
     * Generate string with Each way terms
     *
     * @param {object} market
     */
    generateTerms(market: IMarket): string {
      return this.templateService.genTerms(market, 'sb.newOddsAPlacesExtended');
    }
  
    isGenericSilk(eventEntity: ISportEvent, outcomeEntity: IOutcome): boolean {
      return this.raceOutcomeData.isGenericSilk(eventEntity, outcomeEntity);
    }
  
    isGreyhoundSilk(eventEntity: ISportEvent, outcomeEntity: IOutcome): boolean {
      return this.raceOutcomeData.isGreyhoundSilk(eventEntity, outcomeEntity);
    }
  
    isNumberNeeded(eventEntity: ISportEvent, outcomeEntity: IOutcome): boolean {
      return this.raceOutcomeData.isNumberNeeded(eventEntity, outcomeEntity);
    }
  
    getRunnerNumber(outcomeEntity: IOutcome): string {
      return outcomeEntity.runnerNumber || outcomeEntity.racingFormOutcome && outcomeEntity.racingFormOutcome.draw;
    }
  
    getSilkStyle(raceData: ISportEvent[], outcomeEntity: IOutcome): ISilkStyleModel {
      return this.raceOutcomeData.getSilkStyle(raceData, outcomeEntity);
    }
  
    nextSlide(): void {
      this.carousel.next();
      this.changeDetectorRef.detectChanges();
      if (this.trackGaDesktop) {
        this.commandService.executeAsync(this.commandService.API.RACING_GA_SERVICE).then((racingGaService: RacingGaService) => {
          racingGaService.sendGTM('navigate right', this.eventCategory);
        });
      }
    }
  
    prevSlide(): void {
      this.carousel.previous();
      this.changeDetectorRef.detectChanges();
      if (this.trackGaDesktop) {
        this.commandService.executeAsync(this.commandService.API.RACING_GA_SERVICE).then((racingGaService: RacingGaService) => {
          racingGaService.sendGTM('navigate left', this.eventCategory);
        });
      }
    }
  
    getGoing(going: string): string {
      return this.nextRacesHomeService.getGoing(going);
    }
  
    getDistance(distance: string): string {
      return this.nextRacesHomeService.getDistance(distance);
    }
  
    get showNext(): boolean {
      return this.carousel && this.carousel.currentSlide < this.carousel.slidesCount - 1;
    }
    set showNext(value:boolean){}
    get showPrev(): boolean {
      return this.carousel && this.carousel.currentSlide > 0;
    }
    set showPrev(value:boolean){}
  
    /**
     * Sort and filter outcomes of market(s)
     * providing updatedMarket parameter will process only appropriate market, otherwise - all existing
     *
     * @param updatedMarket
     */
     protected processOutcomes(updatedMarket?: IMarket): void {
      this.raceData.forEach((event: ISportEvent) => {
        event && event.markets?.forEach((market: IMarket) => {
          if (updatedMarket) {
            if (updatedMarket.id === market.id) {
  
              _.each(market.outcomes, (outcome: IOutcome) => {
                const updatedOutcomeObj = _.find(updatedMarket.outcomes, (updatedOutcome: IOutcome) => updatedOutcome.id === outcome.id);
                outcome.prices = updatedOutcomeObj && updatedOutcomeObj.prices || outcome.prices;
              });
  
              const selectedOption: string = this.sortByOptionsService.get();
              this.marketOutcomesMap[market.id] = selectedOption === 'Racecard' ? market.outcomes : this.applyFilters(market);
              return true;
            }
          } else {
            this.raceMarkets.push(market.id);
            this.marketOutcomesMap[market.id] = this.applyFilters(market);
          }
        });
      });
      this.changeDetectorRef.detectChanges();
    }
  
    private applyFilters(market: IMarket): IOutcome[] {
      const orderedOutcomes = this.sbFiltersService.orderOutcomeEntities(
        market.outcomes,
        market.isLpAvailable,
        true,
        true,
        this.hideNonRunners,
        false,
        !this.isHR
      );
      return this.raceMaxSelections ? orderedOutcomes.slice(0, this.raceMaxSelections) : orderedOutcomes;
    }
  
    private initShowCarouselButtons(): void {
      const carouselSlides = this.raceData.length;
      const carouselOuterWidth = this.domTools.getWidth(this.elementRef.nativeElement.querySelector('.race-card-carousel'));
      const slideWidth = this.domTools.getWidth(this.elementRef.nativeElement.querySelector('.slide'));
      const allSlidesWidth = carouselSlides * slideWidth;
      const minSlidesOffset = 20; // Arrows appear when there is minimum 2 slides on carousel. One slide has 10px of margin.
      const isFitSize = carouselOuterWidth >= allSlidesWidth + minSlidesOffset;
  
      this.disableScroll = this.isFitSize = isFitSize;
      this.showCarouselButtons = (carouselOuterWidth <= allSlidesWidth);
  
      this.changeDetectorRef.detectChanges();
    }
  
    private get carousel(): Carousel {
      return this.carouselService.get(this.raceCarousel);
    }
    private set carousel(value:Carousel){}
  
    private setTrapNumbers(): void {
      this.raceData && this.raceData.forEach((event: ISportEvent) => {
        event && event.markets && event.markets.forEach((market: IMarket) => {
          market.outcomes && market.outcomes.forEach((outcome: IOutcome) => {
            if (outcome.runnerNumber) {
              const index = outcome.name.search(/(\(RES\))/);
              outcome.trapNumber = index !== -1 ? outcome.displayOrder : Number(outcome.runnerNumber);
            }
          });
        });
      });
    }
  }