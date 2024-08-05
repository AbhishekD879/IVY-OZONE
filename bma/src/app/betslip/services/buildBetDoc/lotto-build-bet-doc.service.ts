
import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';

import { DeviceService } from '@core/services/device/device.service';
import { ClientUserAgentService } from '@core/services/clientUserAgent/client-user-agent.service';
import { TimeSyncService } from '@core/services/timeSync/time-sync.service';
import { ILottoDraw } from '@app/lotto/models/lotto.model';
import { BetslipStakeService } from '@betslip/services/betslip/betslip-stake.service';
import { betRef, IBetslip, IDocRef, ILeg, ILottoPayload } from '@app/bpp/services/bppProviders/bpp-providers.model';
@Injectable({ providedIn: BetslipApiModule })
export class LottoBuildBetDocService {

  constructor(
    private device: DeviceService,
    private clientUserAgentService: ClientUserAgentService,
    private timeSyncService: TimeSyncService,
    private betslipStakeService: BetslipStakeService
  ) {}

  /**
   * Return constructed place bet object
   * @param {object} data // all needed data for constructiong a bet
   * @returns {object}
   */
   constructPlaceBetObj(lottoBets, currency): ILottoPayload {
    const bets = lottoBets;

    const legs = [],
    betsCountData = this.filterBystakeData(bets);
    bets.forEach(bet => {
      legs.push(this.constructLeg(bet.details, bet.details.draws[0], legs.length + 1, bet.id)); // +1 to start document id with 1
    });

    const allBetsRef = this.createBetRefData(betsCountData, legs, currency);
    /*
    * using id for mapping between accas fro multiple lines and draws 
    */
    legs.forEach(res => {
      delete res.id;
    });
    const betslipData = {
      betslip: this.constructBetslip(lottoBets, allBetsRef.length, currency),
      leg: legs,
      bet: allBetsRef
    };
    return betslipData;
  }

  createBetRefData(bets, legs, currency): betRef[] {
    const betsList = [];
    bets.forEach((bet, ind) => {
      const legItem = legs.find(leg => bet.id === leg.id);
      betsList.push(this.constructBet(bet, ind + 1, currency, legItem.documentId));
    });
    return betsList;
  }

  filterBystakeData(lottoObj) {
   return lottoObj.reduce((acc, bet) => {
        const accaData = this.modifiedAccaBetObj(bet);
          if(accaData.length) {
            acc = [...acc, ...accaData];
          }
      return acc;
  },[]);
  }

  modifiedAccaBetObj(bet) {
    const accaBets = [];
    if (bet.accaBets.length) {
      bet.accaBets.forEach(res => {
        if (res.stake) {
          accaBets.push({ ...res, ...bet.details, id: bet.id });
        }
      })
    }
    return accaBets;
  }

  /**
   * Return constructed array with bet parts
   * @param {string} amount    // 
   * e.g. '4'
   * @param {string} selName   // e.g. 'ACC4'
   * @param {number} betCount  // e.g. 2
   * @param {string} currency  // e.g. 'GBP'
   * @returns {array} betArray
   */
  private constructBet(bet, i, currency, legItemIndex): betRef {
    return {
      documentId: i,
      betTypeRef: {
        id: bet.betType
      },
      stake: {
        amount: bet.userStake,
        stakePerLine: bet.userStake,
        currencyRef: {
          id: currency
        }
      },
      lines: {
        number: bet.lines.number
      },
      legRef: [{
        documentId: legItemIndex
      }]
    }
  }

  /**
   * Return constructed array with leg parts
   * @param {string} picks    // e.g. '4|11|15'
   * @param {array} draws     // e.g. [{draw data}]
   * @returns {array} legArray
   */
  private constructLeg(bet, draw: ILottoDraw, legArrayLen, id): ILeg {

    const i = legArrayLen;
    return {
      documentId: i,
      id: id, // temporary id to find docRef for betRef
      lotteryLeg: {
        picks: bet.selections,
        gameRef: {
          id: draw.id
        },
        sortRef: {
          id: draw.sort
        },
        drawRef: {
          id: draw.drawDescriptionId
        },
        subscription: {
          number: bet.frequency,
          free: '0',
          frequency: "W"
        }
      }
    }
  }

  /**
   * Return constructed array with betRef parts
   * @param {number} betCount // e.g. 2
   * @returns {array} betRef
   */
  private createBetRef(betCount): IDocRef[] {
    const betRefData = [];

    for (let i = 1; i <= betCount; i++) {
      betRefData.push({ documentId: i });
    }

    return betRefData;
  }

  /**
   * Return constructed betslip part
   * @param {string} amount   // e.g. '2'
   * @param {number} betCount // e.g. 2
   * @param {string} currency // e.g. 'GBP'
   * @returns {object}
   */
  private constructBetslip(data, betCount, currency): IBetslip {
    const totalAmount = this.betslipStakeService.getTotalStake(data);

    return {
      clientUserAgent: this.clientUserAgentService.getId(false, true),
      isAccountBet: 'Y',
      documentId: 1,
      stake: {
        amount: totalAmount,
        currencyRef: {
          id: currency
        }
      },
      slipPlacement: {
        IPAddress: this.timeSyncService.ip,
        channelRef: this.device.channel.channelRef
      },
      betRef: this.createBetRef(betCount)
    };
  }
}
