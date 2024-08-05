import { YourcallMarketsService } from '@yourcall/services/yourCallMarketsService/yourcall-markets.service';
import { Injectable } from '@angular/core';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import environment from '@environment/oxygenEnvConfig';
import { IRemoteBetslipBet } from '@app/core/services/remoteBetslip/remote-betslip.constant';
import { BYBBet } from '@app/yourCall/models/bet/byb-bet';
import { DSBet } from '@app/yourCall/models/bet/ds-bet';
import { IYourcallBetPlacement } from '@app/yourCall/models/betslip-data.model';
import { Subject } from 'rxjs/internal/Subject';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';

@Injectable({ providedIn: 'root' })
export class BybSelectedSelectionsService {
    public selectedSelectionsSet: any = new Set();
    public brand: string;
    public byb: string;
    public dimension65: string;
    public eventEntity;
    public marketFilterBYB;
    public duplicateIdd = new Set<string>();
    public betPlacementSubject$ = new Subject<boolean>();
    private digitKeyBoardStatus:boolean=false;
    private stakeFromQb:number=0;
    public isBetPlaceClicked: boolean;

    constructor(
        public gtmService: GtmService,
        public yourcallMarketsService : YourcallMarketsService,
        protected pubsub: PubSubService,) {
        this.byb = environment.brand === 'bma' ? 'build your bet' : 'bet builder';
        this.brand = environment.brand === 'bma' ? 'Build Your Bet' : 'Bet Builder';
        this.dimension65 = environment.brand === 'bma' ? 'Build Your Bet' : 'Bet Builder';

          this.pubsub.subscribe('byb_keyBoardPress', this.pubsub.API.DIGIT_KEYBOARD_KEY_PRESSED, () => {
            this.stakeFromQb = 0;
          });
          this.pubsub.subscribe('byb_digit_status', this.pubsub.API.LUCKY_DIP_KEYPAD_PRESSED, (status) => {
            this.digitKeyBoardStatusInit(status);
        })
        this.pubsub.subscribe('byb_quickStake', this.pubsub.API.QB_QUICKSTAKE_PRESSED_DIGIT_KEYBOARD, () => {
            this.stakeFromQb = this.digitKeyBoardStatus?2:1;
          });
    }

    digitKeyBoardStatusInit(status) {
        this.digitKeyBoardStatus =  this.isBetPlaceClicked?this.digitKeyBoardStatus:!status;
    }

    betPlacementSucess() {
        this.betPlacementSubject$.next(true);
    }

    callGTM(key, data) {
        switch (key) {
            case ('toggle'):
                this.bybToggleGTM();
                break;

            case ('expand-collapse'):
                this.bybExpandCollapseGTM(data);
                break;

            case ('add-selection'):
                this.bybAddSelectionGTM(data);
                break;

            case ('open-close'):
                this.bybOpenCloseQuickBetGTM(data);
                break;

            case ('remove-selection'):
                this.bybRemoveSelectionGTM(data);
                break;

            case ('add-bet'):
                this.bybAddBetGTM(data);
                break;

            case ('show-stats'):
                this.bybStatsGTM(data);
                break;

            case ('edit-bet'):
                this.bybEditQuickBetGTM(data);
                break;

        }
    }

    bybToggleGTM() {
        this.gtmService.push('trackEvent', {
            eventAction: 'toggle',
            eventCategory: this.byb,
            eventLabel: this.marketFilterBYB,
            dimension28: this.eventEntity.categoryId, //e.g. "16"
            dimension29: this.eventEntity.typeId, //e.g. "25230"
            dimension30: this.eventEntity.id //e.g. "18880309“
        });
    }

    bybExpandCollapseGTM(data) {
        this.gtmService.push('trackEvent', {
            eventAction: data.action ? 'expand' : 'collapse',
            eventCategory: this.byb,
            eventLabel: data.marketName, //“Match Booking Pts“, “Total Corners” or “Goalscorer”
            dimension28: this.eventEntity.categoryId, //e.g. "16"
            dimension29: this.eventEntity.typeId, //e.g. "25230"
            dimension30: this.eventEntity.id, //e.g. "18880309“
            dimension91: this.marketFilterBYB
        });
    }

    bybAddSelectionGTM(data) {
        this.gtmService.push('trackEvent', {
            eventAction: 'add to quickbet',
            eventCategory: 'quickbet',
            eventLabel: 'success', //“Match Booking Pts“, “Total Corners” or “Goalscorer”
            dimension91: this.marketFilterBYB,
            ecommerce: {
                add: {
                    products: [{
                        category: this.eventEntity.categoryId, //e.g. "16"
                        variant: this.eventEntity.typeId, //e.g. "25230"
                        brand: this.brand,
                        name: this.eventEntity.name, // e.g. “Watford v Chelsea" 
                        dimension60: this.eventEntity.id, //e.g. "18880309“
                        dimension61: data.selectionName, // e.g. “Match Betting 90 mins CHELSEA“, “R. Lukaku To Have 5+ Shots” or “D. Rose To Make 2+ Tackles”
                        dimension62: this.eventEntity.eventIsLive ? 1 : 0, //e.g. pre-event = 0, in-play = 1
                        dimension63: 1, // Always 1
                        dimension64: 'EDP',
                        dimension65: this.brand,
                        quantity: 1 // Always 1
                    }]
                }
            }
        });
    }

    bybOpenCloseQuickBetGTM(data) {
        this.gtmService.push('trackEvent', {
            eventAction: 'quickbet',
            eventCategory: this.byb,
            eventLabel: data.openClose, //e.g. “open“ or “close”
            dimension28: this.eventEntity.categoryId, //e.g. "16"
            dimension29:this.eventEntity.typeId, //e.g. "25230"
            dimension30:  this.eventEntity.id, //e.g. "18880309“
            dimension91: this.marketFilterBYB
        });
    }

    bybRemoveSelectionGTM(data) {
        const obj = {
            eventAction: 'remove',
            eventCategory: 'quickbet',
            eventLabel: data.deselect ? 'deselect' : 'quickbet',
            ecommerce: {
                remove: {
                    products: [{
                        category: this.eventEntity.categoryId, //e.g. "16"
                        variant: this.eventEntity.typeId, //e.g. "25230"
                        brand: this.brand,
                        name: this.eventEntity.name, // e.g. “Watford v Chelsea" 
                        dimension60: this.eventEntity.id, //e.g. "18880309“
                        dimension61: data.selectionName, // e.g. “Match Betting 90 mins CHELSEA“, “R. Lukaku To Have 5+ Shots” or “D. Rose To Make 2+ Tackles”
                        dimension62: this.eventEntity.eventIsLive ? 1 : 0, //e.g. pre-event = 0, in-play = 1
                        dimension63: 1, // Always 1
                        dimension64: 'EDP',
                        dimension65: this.brand,
                        quantity: 1 // Always 1
                    }]
                }
            }
        };
        if(data.deselect) {
            obj['dimension91'] = this.marketFilterBYB;
        }
        this.gtmService.push('trackEvent', obj);
    }

    bybAddBetGTM(data) {
        this.gtmService.push('trackEvent', {
            eventAction: 'add to betslip',
            eventCategory: 'quickbet',
            eventLabel: 'success',
            ecommerce: {
                add: {
                    products: [{
                        category: this.eventEntity.categoryId, //e.g. "16"
                        variant: this.eventEntity.typeId, //e.g. "25230"
                        brand: this.brand,
                        name: this.eventEntity.name, // e.g. “Watford v Chelsea"
                        dimension60: this.eventEntity.id, //e.g. "18880309“
                        dimension61: data.selectionsCnt, // e.g. “3“
                        dimension62: this.eventEntity.eventIsLive ? 1 : 0, //e.g. pre-event = 0, in-play = 1
                        dimension63: 1, // Always 1
                        dimension64: 'EDP',
                        dimension65: this.brand,
                        dimension66: 1, // Always 1
                        dimension67: data.odds, // e.g. “3.60“
                        quantity: 1, // Always 1
                    }]
                }
            }
        });
    }

    bybStatsGTM(data): void {        
        this.gtmService.push('trackEvent', {
            eventAction: 'show stats',
            eventCategory: this.byb,
            eventLabel: data.eventLabel,
            dimension28: this.eventEntity.categoryId, //e.g. "16"
            dimension29: this.eventEntity.typeId, //e.g. "25230"
            dimension30: this.eventEntity.id, //e.g. "18880309“
            dimension91: this.marketFilterBYB

        });
    }

    bybEditQuickBetGTM(data): void {
        this.gtmService.push('trackEvent', {
            eventAction: "edit quickbet",
            eventCategory: this.byb,
            eventLabel: data.eventLabel,
            dimension28: this.eventEntity.categoryId, //e.g. "16"
            dimension29: this.eventEntity.typeId, //e.g. "25230"
            dimension30: this.eventEntity.id, //e.g. "18880309“
            dimension113: data.odds //<Displayed Odds> //e.g. “3.60"
        });
    }

    placeBet(receiptData: IYourcallBetPlacement, bet: IRemoteBetslipBet, eventEntity, selection: BYBBet | DSBet) {
        const objByb = {
            eventAction: 'place bet',
                  eventCategory: 'quickbet',
                  eventLabel: 'success',
                  ecommerce: {
                      purchase: {
                          actionField: {
                              id: receiptData.receipt, //e.g. “O/16069280/0000245“
                              revenue: receiptData.totalStake, //e.g. “5.00“
                          },
                          products: [{
                              category: eventEntity.sportId, //e.g. "16"
                              variant: eventEntity.typeId, //e.g. "25230"
                              brand: this.brand,
                              name: eventEntity.name, // e.g. “Watford v Chelsea" 
                              dimension60: eventEntity.id, //e.g. "18880309“
                              dimension61: selection.selections?.length, // e.g. “3“
                              dimension62: eventEntity.eventIsLive ? 1 : 0, //e.g. pre-event = 0, in-play = 1
                              dimension63: 1, // Always 1
                              dimension64: 'EDP',
                              dimension65: this.brand,
                              dimension66: 1, // Always 1
                              dimension67: bet.price, // e.g. “3.60“
                              dimension86: 0, // e.g. no boost = 0, boosted = 1
                              dimension90: receiptData.betId, // e.g. 1022172269
                              metric1: selection.freebetValue ? selection.freebetValue : 0,
                              price: receiptData.totalStake, //e.g. "5.00"
                              quantity: 1, // Always 1
                              id: receiptData.receipt // e.g. "O/17682267/0000488"
                          }]
                      },
                      currencyCode: selection.currencyName // e.g. "GBP"
                  }
          };
          if(this.stakeFromQb){
            const dimVal=this.stakeFromQb==2?'keypad predefined stake':'predefined stake';
            objByb.ecommerce.purchase.products[0]['dimension181']=dimVal;
          }
          this.stakeFromQb=0;
          this.digitKeyBoardStatus=false;
          this.isBetPlaceClicked=false;
          this.gtmService.push('trackEvent',objByb);
    }
}