import { of as observableOf, Observable, throwError } from 'rxjs';

import { catchError, mergeMap, map, delay } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import * as _ from 'underscore';

import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { TimeService } from '@core/services/time/time.service';
import { IBet, IReadBetRequest, IReadBetResponse } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IBirResponse, IParsedBirResponse, IReducedBetError } from './bir.model';

@Injectable({ providedIn: BetslipApiModule })
export class BirService {
  readonly betProvider = 'OpenBetBir';
  private birResponse: IBirResponse;

  constructor(
    private timeService: TimeService,
    private bppService: BppService,
    private pubSubService: PubSubService
  ) {}

  get birBets(): IBet[] {
    return _.filter(this.birResponse.bets, (bet: IBet): boolean => bet.provider === 'OpenBetBir');
  }
  set birbets(value:IBet[]){}
  get birBetsIds(): number[] {
    return _.map(_.filter(this.birResponse.bets, (bet: IBet): boolean => bet.provider === 'OpenBetBir'),
      (bet: IBet): number => bet.id);
  }
  set birBetsIds(value:number[]){}
  /**
   * executes Bit response
   */
  exectuteBIR(birResponse: IBirResponse): Observable<IParsedBirResponse> {
    this.birResponse = birResponse;

    const nonBirIds = this.getNonBirIds(birResponse);

    return this.wait(this.birBets, this.birBetsIds).pipe(
      mergeMap((idArray: number[]) => this.sendReadBetRequest(this.buildReadBetRequest(idArray))),
      map((readBetResponse: IReadBetResponse) => this.parseResponse(nonBirIds, readBetResponse)));
  }

  /**
   * get ids from bets that do not have provider === 'OpenBetBir'
   */
  private getNonBirIds(birResponse: IBirResponse): number[] {
    return _.map(_.filter(birResponse.bets, (bet: IBet): boolean => bet.provider !== 'OpenBetBir'),
      (bet: IBet): number => bet.id);
  }

  /**
   * set time out before sending readBet request
   * @params{array} bets
   * @params{array} bit Ids array
   * @returns{promise}
   */
  private wait(bets: IBet[], idArray: number[]): Observable<number[]> {
    const seconds = Number(_.max(bets, (bet: IBet): number => {
        return Number(bet.confirmationExpectedAt);
      }).confirmationExpectedAt) + 1;

    console.warn(`BIR exception, I will wait for : ${seconds} seconds`);
    this.pubSubService.publishSync(this.pubSubService.API.SET_BIR_COUNTDOWN_TIMER, seconds);

    return observableOf(idArray).pipe(delay(this.timeService.secondsToMiliseconds(seconds)));
  }

  /**
   * Builds read bet request object
   * @params{array} bir ids
   * @return{object} request object
   */
  private buildReadBetRequest(idArray: number[]): IReadBetRequest {
    return <IReadBetRequest>{
      betRef: _.map(idArray, (id: number) => {
        return { id: id.toString(), provider: 'OpenBetBir' };
      })
    };
  }

  /**
   * Send read bet request
   * @params{object} request object
   * @returns{promise} readBet response with settled bets
   */
  private sendReadBetRequest(request: IReadBetRequest): Observable<IReadBetResponse> {
    return (this.bppService.send('readBet', request) as Observable<IReadBetResponse>).pipe(
      catchError(error => {
        this.bppService.showErrorPopup('betPlacementError');
        return throwError(error);
      }));
  }

  /**
   * Get bet receipt id's from response
   * merge nonBir receipt id's saved before sending bir request
   * @{array} id's of non Bir bets
   * @{object} readBet response
   */
  private parseResponse(nonBirIds: number[], readBetResponse: IReadBetResponse): IParsedBirResponse {
    readBetResponse.bet = readBetResponse.bet.map((bet: IBet) => {
      bet.provider = this.betProvider;
      return bet;
    });
    const ids = _.reduceRight(readBetResponse.bet, (idsArray: number[], bet: IBet): number[] => {
      idsArray.push(bet.id);
      return idsArray;
    }, []);

    return {
      errs: this.reduceErrors(readBetResponse),
      ids: ids.concat(nonBirIds || []),
      bets: readBetResponse.bet
    };
  }

  private reduceErrors(response: IReadBetResponse): IReducedBetError[] {
    const err = response.betError;

    return err ? [{
      subCode: err.subErrorCode,
      code: err.code,
      price: err.price,
      outcomeRef: err.outcomeRef
    }] : [];
  }
}
