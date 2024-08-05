import { Component, Input, OnInit } from '@angular/core';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { CmsService } from '@core/services/cms/cms.service';
import { ISystemConfig } from '@app/core/services/cms/models';
import { IMarket } from '@app/core/models/market.model';
import { EXTRA_PLACE_CONSTANTS } from '@lazy-modules/extraPlaceSignposting/extraplace.constants';
import { IOutcomeDetailsResponse } from '@root/app/bpp/services/bppProviders/bpp-providers.model';
import environment from '@environment/oxygenEnvConfig';
@Component({
    selector: 'extra-place-signposting',
    templateUrl: './extra-place-signposting.component.html',
    styleUrls: ['./extra-place-signposting.component.scss']
})

export class ExtraPlaceSignpostingComponent implements OnInit {
    @Input() eventData?: ISportEvent;
    @Input() betSlipData?: IOutcomeDetailsResponse;
    @Input() origin?: string;
    @Input() marketData?: IMarket;
    @Input() isBetHistory?: boolean;
    @Input() index?: number;
    extraPlaceName: string;
    nonRunnerMessage: string;
    brand: string = environment.brand;

    constructor(private cmsService: CmsService) { }

    ngOnInit() {
        if (this.isMyBetsPage() && this.isNonRunnerEvent()) {
            this.buildNonRunnerMessage();
        } else if (this.isExtraPlaceOfferedEvent()) {
            const data = EXTRA_PLACE_CONSTANTS.EXTRA_PLACE_DATA[this.getOrigin()];
            const referenceEachWayTerms=this[data].referenceEachWayTerms;
            if(Array.isArray(referenceEachWayTerms)){
              this[data].referenceEachWayTerms=referenceEachWayTerms[0];
            }
            this.extraPlaceSignposting(this[data].eachWayPlaces, this[data].referenceEachWayTerms && this[data].referenceEachWayTerms.places || this[data].previousOfferedPlaces);
        }
    }

    /**
     * getOrigin() to get and covert the origin into uppercase
     * @returns {string}
     */
    private getOrigin(): string {
        return this.origin && this.origin.toUpperCase();
    }

    /**
     * isNonRunnerEvent() to track the extraplace once offered after removed
     * @returns {boolean}
     */
    isNonRunnerEvent(): boolean {
        return this.marketData && this.marketData.referenceEachWayTerms && this.marketData.eachWayPlaces <= this.marketData.referenceEachWayTerms.places;
    }

    /**
     * isExtraPlaceOfferedEvent() to check the event is offered with extra place
     *  @returns {boolean}
     */
    private isExtraPlaceOfferedEvent(): boolean {
        const data = EXTRA_PLACE_CONSTANTS.EXTRA_PLACE_DATA[this.getOrigin()];
        const drilldownTagnames = this[data] && (this[data].drilldownTagNames);
        return drilldownTagnames && (drilldownTagnames.includes(EXTRA_PLACE_CONSTANTS.EXTRA_PLACE_MARKET_FLAG));
    }

    /**
     * isMyBetsPage() to check the event is from MyBets
     *  @returns {boolean}
     */
    isMyBetsPage(): boolean {
        return this.origin === EXTRA_PLACE_CONSTANTS.MY_BETS.OPEN_BETS ||
            this.origin === EXTRA_PLACE_CONSTANTS.MY_BETS.SETTLED_BETS ||  this.origin === EXTRA_PLACE_CONSTANTS.MY_BETS.CASHOUT_BETS;
    }

    /**
     * extraPlaceSignposting() to construct the extraplace message
     */
    extraPlaceSignposting(eachWayPlaces, places): void {
        const extraPlaceName = this.getExtraPlaceName(eachWayPlaces, places);
        this.extraPlaceName = extraPlaceName.trim();
    }

    private getExtraPlaceName(eachWayPlaces, places): string {
        return `${(this.origin !='betslip') ? EXTRA_PLACE_CONSTANTS.PAYING : ''} ${eachWayPlaces} ${EXTRA_PLACE_CONSTANTS.PLACES_INSTED_OF} ${places}`;
    }

    /**
     * buildNonRunnerMessage() to get the nonrunner message from cms
     * @returns {void}
     */
    private buildNonRunnerMessage(): void {
        this.cmsService.getCmsInitData().subscribe((configs: ISystemConfig) => {
            const sportsConfigs = configs.sportCategories;
            sportsConfigs.forEach(element => {
                if (this.eventData && (this.isHorseRacing(element)|| this.isGolf(element))) {
                    this.nonRunnerMessage = element.messageLabel;
                }
            });
        });
    }

     /**
     * isHorseRacing() to check for Horse racing
     * @returns {boolean}
     */
    private isHorseRacing(config):boolean{
       return this.eventData.categoryName === EXTRA_PLACE_CONSTANTS.HORSE_RACING.CATEGORY_NAME && config.imageTitle === EXTRA_PLACE_CONSTANTS.HORSE_RACING.IMAGE_TITLE

    }

    /**
     * isGolf() to check for Golf
     * @returns {boolean}
     */
   private isGolf(config):boolean{
        return this.eventData.categoryName === EXTRA_PLACE_CONSTANTS.GOLF.CATEGORY_NAME && config.imageTitle === EXTRA_PLACE_CONSTANTS.GOLF.IMAGE_TITLE
     }

    /**
        * isMyBetsEpr to EPR for MyBets
        * @returns {boolean}
        */
    isMyBetsEpr(): boolean {
        return this.isMyBetsPage() && !this.isNonRunnerEvent() && this.isBetHistory;
    }
}
