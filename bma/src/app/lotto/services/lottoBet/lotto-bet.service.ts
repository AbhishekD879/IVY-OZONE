// import { of as observableOf,  Observable } from 'rxjs';

// // import { map, concatMap } from 'rxjs/operators';
// import { ILottoDraw, ILottoPlaceBetObj } from '../../models/lotto.model';
// import { Injectable } from '@angular/core';
// import * as _ from 'underscore';
// import { Router } from '@angular/router';

// import { BppService } from '@app/bpp/services/bpp/bpp.service';
// import { DeviceService } from '@core/services/device/device.service';
// import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
// import { LottoReceiptService } from '../lottoReceipt/lotto-receipt.service';
// import { ClientUserAgentService } from '@core/services/clientUserAgent/client-user-agent.service';
// import { TimeSyncService } from '@core/services/timeSync/time-sync.service';

// @Injectable()
// export class LottoBetService {

//   constructor(
//     private device: DeviceService,
//     private lottoReceiptService: LottoReceiptService,
//     private coreToolsService: CoreToolsService,
//     private bppService: BppService,
//     private router: Router,
//     private clientUserAgentService: ClientUserAgentService,
//     private timeSyncService: TimeSyncService
//   ) {
//   }

//   placeBet(data) {
//     return this.setReceipt(data);
//   }

//   openReceipt(): void {
//     setTimeout(() => this.router.navigate(['/lotto', 'lottery-receipt']));
//   }

//   /**
//    * Set data for receipt page
//    * @param {object} data // betplacement data object
//    * @returns {object} $promise
//    */
//   private setReceipt(data) {
//     this.lottoReceiptService.setReceipt({
//       name: data.name,
//       draws: data.draws,
//       betTypeDesc: `Match (${data.selections.split('|').length})`,
//       betSelections: data.selections.split('|').join(' '),
//       betOdds: data.odds,
//       betStakePerLine: data.amount,
//       betStake: data.amount * data.draws.length,
//       currency: this.coreToolsService.getCurrencySymbolFromISO(data.currency),
//       date: new Date()
//     });
//     return observableOf(data);
//   }

//   /**
//    * Send a request to betplacement api
//    * @param {object} data // betplacement object
//    * @returns {object} $promise
//    */
//   private sendRequest(data): Observable<any> {
//     const req = this.constructPlaceBetObj(data);
//     return (this.bppService.send('placeBet', req as any));
//   }

//   /**
//    * Return constructed place bet object
//    * @param {object} data // all needed data for constructiong a bet
//    * @returns {object}
//    */
//   private constructPlaceBetObj(data) {
//     const betCount = data.draws.length;

//     return {
//       betslip: this.constructBetslip(data.amount, betCount, data.currency),
//       leg: this.constructLeg(data.selections, data.draws),
//       bet: this.constructBet(data.amount, data.selectionName, betCount, data.currency)
//     };
//   }

//   /**
//    * Return constructed array with bet parts
//    * @param {string} amount    // e.g. '4'
//    * @param {string} selName   // e.g. 'ACC4'
//    * @param {number} betCount  // e.g. 2
//    * @param {string} currency  // e.g. 'GBP'
//    * @returns {array} betArray
//    */
//   private constructBet(amount, selName, betCount, currency) {
//     const betArray = [];

//     for (let i = 1; i <= betCount; i++) {
//       betArray.push({
//         documentId: i,
//         betTypeRef: {
//           id: selName
//         },
//         stake: {
//           amount,
//           stakePerLine: amount,
//           currencyRef: {
//             id: currency
//           }
//         },
//         lines: {
//           number: '1'
//         },
//         legRef: [{
//           documentId: i
//         }]
//       });
//     }

//     return betArray;
//   }

//   /**
//    * Return constructed array with leg parts
//    * @param {string} picks    // e.g. '4|11|15'
//    * @param {array} draws     // e.g. [{draw data}]
//    * @returns {array} legArray
//    */
//   private constructLeg(picks: string, draws: ILottoDraw[]) {
//     const legArray = [];
//     let i = 1;

//     _.forEach(draws, draw => legArray.push({
//       documentId: i++,
//       lotteryLeg: {
//         picks,
//         gameRef: {
//           id: draw.id
//         },
//         sortRef: {
//           id: draw.sort
//         },
//         drawRef: {
//           id: draw.drawDescriptionId
//         },
//         subscription: {
//           number: '1',
//           free: '0'
//         }
//       }
//     }));

//     return legArray;
//   }

//   /**
//    * Return constructed array with betRef parts
//    * @param {number} betCount // e.g. 2
//    * @returns {array} betRef
//    */
//   private createBetRef(betCount) {
//     const betRef = [];

//     for (let i = 1; i <= betCount; i++) {
//       betRef.push({ documentId: i });
//     }

//     return betRef;
//   }

//   /**
//    * Return constructed betslip part
//    * @param {string} amount   // e.g. '2'
//    * @param {number} betCount // e.g. 2
//    * @param {string} currency // e.g. 'GBP'
//    * @returns {object}
//    */
//   private constructBetslip(amount, betCount, currency) {
//     return {
//       clientUserAgent: this.clientUserAgentService.getId(false, true),
//       isAccountBet: 'Y',
//       documentId: 1,
//       stake: {
//         amount: amount * betCount,
//         currencyRef: {
//           id: currency
//         }
//       },
//       slipPlacement: {
//         IPAddress: this.timeSyncService.ip,
//         channelRef: this.device.channel.channelRef
//       },
//       betRef: this.createBetRef(betCount)
//     };
//   }
// }
