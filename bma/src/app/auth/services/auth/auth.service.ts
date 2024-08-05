import { BehaviorSubject, from, from as observableFrom, Observable, of, throwError } from 'rxjs';
import { catchError, concatMap, first, map, mergeMap } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { IFreebetToken, IRespAccountValidate } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { ITempTokenResponse } from '@vanillaInitModule/models/temp-token-reponse.interface';
import { TempTokenService } from '@vanillaInitModule/services/tempToken/temp-token.service';
import { ITempToken } from '@authModule/services/auth/auth.model';
import { UserService } from '@core/services/user/user.service';
import { StorageService } from '@coreModule/services/storage/storage.service';
import { DeviceService } from '@coreModule/services/device/device.service';
import { BppAuthService } from '@app/bpp/services/bppProviders/bpp-auth.service';
import { ProxyHeadersService } from '@app/bpp/services/proxyHeaders/proxy-headers.service';
import { SessionService } from '@authModule/services/session/session.service';
import { CommandService } from '@app/core/services/communication/command/command.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CmsService } from '@core/services/cms/cms.service';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { UserPreferenceProvider } from '@app/bma/components/userSettings/user-settings.service';
import * as _ from 'underscore';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  sessionLoggedIn: Observable<null>;
  innerSessionLoggedIn = new BehaviorSubject(null);
  toteFreeBets = [];
  toteBetPacks = [];
  betIds = {toteClassId: '321',horseRacing: '223',hrCategory: '21'};

  constructor(
    private tempTokenService: TempTokenService,
    private userService: UserService,
    private bppAuthService: BppAuthService,
    private storage: StorageService,
    private proxyHeadersService: ProxyHeadersService,
    private device: DeviceService,
    private sessionService: SessionService,
    private commandService: CommandService,
    private pubsub: PubSubService,
    private cmsService: CmsService,
    private awsService: AWSFirehoseService,
    private upmsService: UserPreferenceProvider
  ) {
    this.reloginBppToCommand = this.reloginBppToCommand.bind(this);
    this.sessionLoggedIn = this.innerSessionLoggedIn.asObservable();

    this.commandService.register(this.commandService.API.BPP_AUTH_SEQUENCE, this.reloginBppToCommand);
  }

  /**
   * Performs needed operations for BPP authentication:
   * - initializes new promises needed for WhenSesionFactory;
   * - retrieves new temporary token from OpenApi;
   * - perform BPP authentication.
   * @return {Observable}
   */
  bppAuthSequence(): Observable<void> {
    this.userService.initProxyAuth();
    return this.getTempToken().pipe(
      concatMap(tokenData => {
        if (tokenData) {
          return this.bppLogin(tokenData);
        }
        return throwError('No Vanilla Temp Token');
      })
    );
  }

  getTempToken(token?: string): Observable<any> {
    return this.tempTokenService.fetchTemporaryToken().pipe(
      map((response: ITempTokenResponse) => {
        const tempToken = response && response.sessionToken;
        if (tempToken) {
          this.awsService.addAction('authService=>getTempToken=>Success', { tempToken: tempToken.substr(0, 7) });
          return {
            username: this.userService.username,
            tempToken
          };
        }
        this.awsService.addAction('authService=>getTempToken=>NoResponse', { response });
        console.warn('No Vanilla Temp Token');
        return;
      }),
      catchError(error => {
        this.awsService.addAction('authService=>getTempToken=>Error', { error });
        console.error('No Vanilla Temp Token');
        return of(error);
      })
    );
  }

  /**
   * Calls for oddspreference value from DB to set in localstorage to access in all browsers.
   * @param token Needed parameter for authentication: "token".
   */
  getOddspreference(token){
    this.upmsService.getOddsPreference(token).subscribe((data) => {
      if(data && data.preferences){
        this.userService.set({ oddsFormat: data.preferences.oddPreference });
        this.pubsub.publish(this.pubsub.API.SET_ODDS_FORMAT, data.preferences.oddPreference);
      }
    });
  }

  /**
   * Performs authentication to BPP with given "username" and "token".
   * @param {Object} params Needed parameters for BPP authentication: "username" and "token".
   * @return {Observable}
   */
  bppLogin(params: ITempToken): Observable<void> {
    const { tempToken, username } = params;
    const loginParams = { username, token: tempToken, channel: this.device.freeBetChannel };
    this.awsService.addAction('BPP Login=>Request', { tempToken: tempToken.substr(0, 7) });

    return this.bppAuthService.validate(loginParams)
      .pipe(
        map((res: IRespAccountValidate) => {
          if (res && !res.error) {
            this.awsService.addAction('BPP Login=>Success', { newBppToken: res.token.substr(0, 7) });
            const privateMarkets = res.privateMarkets ? res.privateMarkets.data : [];

            this.storage.set('previousBppUsername', this.userService.username);
            this.pubsub.publish(this.pubsub.API.STORE_FREEBETS, {...res.freeBets, isPageRefresh: true});
            this.drillDownToteFreebets(res.freeBets.data);
            this.pubsub.publishSync('STORE_PRIVATE_MARKETS', [privateMarkets]);

            this.userService.set({ bppToken: res.token });
            this.userService.set({ lastBet: res.lastBet });
            this.userService.set({ maxStakeScale: res.maxStakeScale });
            this.userService.set({ custId: res.custId });
            this.pubsub.publishSync('STORE_STAKE_FACTOR', [res.maxStakeScale]);
            this.pubsub.publish(this.pubsub.API.BPP_TOKEN_SET);
            this.proxyHeadersService.generateBppAuthHeaders();
            this.userService.resolveProxyAuth();
          } else {
            this.handleBppLoginError(res);
          }
          this.getOddspreference(res.token);

          return res;
        }),
        mergeMap((bppResponseData: IRespAccountValidate) => this.initOddsBoost(bppResponseData)),
        catchError((error) => {
          return this.handleBppLoginError(error);
        })
      ) as Observable<void>;
  }

  drillDownToteFreebets(data): void {
    this.toteFreeBets = [];
    this.toteBetPacks = [];
    data.forEach(freeBet => { 
      this.tokenPossibleBetsCheck(freeBet);
   });
    this.storage.set('toteFreeBets', this.toteFreeBets);
    this.storage.set('toteBetPacks', this.toteBetPacks);
  }

  tokenPossibleBetCheck(freeBet) : void {
    let betLevel, betPack ,betId;
     const tokenPossibleBet = freeBet.tokenPossibleBet;
    if(tokenPossibleBet) {
       betLevel = tokenPossibleBet.betLevel;
       betId = tokenPossibleBet.betId;
    }
     const freebetOfferType = freeBet.freebetOfferType;
     const inPlay = freeBet.tokenPossibleBet.inPlay;
     const freebetOfferCategories = freeBet.freebetOfferCategories;
     if(freebetOfferCategories) {
      const freebetOfferCategory = freebetOfferCategories.freebetOfferCategory;
      if(freebetOfferCategory === 'Bet Pack') {
        betPack = true;
      } else {
        betPack = false;
      }
     } else {
      betPack = false;
     }

     if(this.isTokenPossibleBet(betLevel, betId) && (freebetOfferType === '' || freebetOfferType === 'SGL') && inPlay !== 'Y' && !betPack) {
          this.toteFreeBets.push(freeBet);
     } else if(this.isTokenPossibleBet(betLevel, betId) && (freebetOfferType === '' || freebetOfferType === 'SGL') && inPlay !== 'Y' && betPack) {
          this.toteBetPacks.push(freeBet);
     }
     
  }
  
  tokenPossibleBetsCheck(freeBet): void {
    let betLevel, betPack ,betId, inPlay;
    const tokenPossibleBets = freeBet.tokenPossibleBets;
    if(tokenPossibleBets && tokenPossibleBets.length > 1) {
      tokenPossibleBets.forEach(item => {
        betLevel = item.betLevel;
        betId = item.betId;
        inPlay = item.inPlay;
        const freebetOfferType = freeBet.freebetOfferType;
        const freebetOfferCategories = freeBet.freebetOfferCategories;
        if(freebetOfferCategories) {
          const freebetOfferCategory = freebetOfferCategories.freebetOfferCategory;
          if(freebetOfferCategory === 'Bet Pack') {
            betPack = true;
          } else {
            betPack = false;
          }
          } else {
            betPack = false;
          }
     if(this.isTokenPossibleBets(betLevel, betId) && (freebetOfferType === '' || freebetOfferType === 'SGL') && inPlay !== 'Y' && !betPack) {
      this.toteFreeBets.push(freeBet);
      } else if(this.isTokenPossibleBets(betLevel, betId) && (freebetOfferType === '' || freebetOfferType === 'SGL') && inPlay !== 'Y' && betPack) {
      this.toteBetPacks.push(freeBet);
      }
      });
      this.toteFreeBets = _.uniq(this.toteFreeBets);
      this.toteBetPacks = _.uniq(this.toteBetPacks);
    } else {
      this.tokenPossibleBetCheck(freeBet);
    }
  }

  isTokenPossibleBet(betLevel, betId) : boolean {
    if((betLevel === 'ANY_POOLS' || betLevel === 'ANY') || (betLevel === 'CLASS' && betId === this.betIds.toteClassId) || (betLevel === 'CATEGORY' && betId === this.betIds.hrCategory)) {
      return true
    } else {
      return false
    }
  }

  isTokenPossibleBets(betLevel, betId): boolean {
    if((betLevel === 'ANY_POOLS' || betLevel === 'ANY') || (betLevel === 'CLASS' && (betId === this.betIds.toteClassId || betId === this.betIds.horseRacing)) || (betLevel === 'CATEGORY' && betId === this.betIds.hrCategory)) {
      return true
    } else {
      return false
    }
  }

  /**
   * Init oddsBoost
   * - with data => after auth/user response
   * - without data => on page refresh, when we need to call allFreebets request
   * @param res
   */
  initOddsBoost(res?: IRespAccountValidate): Observable<void | IFreebetToken[] | unknown> {
    return this.cmsService.getOddsBoost().pipe(
      mergeMap(config => {
        if (config.enabled) {
          const tokens = (res && !res.error && res.betBoosts) ? res.betBoosts.data : [];
          if (res) {
            return from(this.commandService.executeAsync(this.commandService.API.ODDS_BOOST_INIT, [tokens]));
          } else {
            return from(this.commandService.executeAsync(this.commandService.API.GET_ODDS_BOOST_TOKENS, [true]));
          }
        } else {
          return of(null);
        }
      })
    );
  }

  reLoginBpp(): Observable<any> {
    if (this.userService.proxyPromiseResolved()) {
      return this.bppAuthSequence();
    } else {
      return observableFrom(this.sessionService.whenProxySession());
    }
  }

  reLoginSequence(credentials, options = {}): Observable<void> {
    return of(null);
  }

  acceptTermsAndConditions(): Observable<void> {
    return of(null);
  }

  handleLogoutNotification(performRefresh: boolean): void {}

  loginSequence(credentials, options = {}, isUpgradedInShopUser = false): Observable<void> {
    return of(null);
  }

  logout(reason: string, showLogoutPopup: boolean = false): Observable<void> {
    return of(null);
  }

  mainInit(): void {}

  private handleBppLoginError(error: IRespAccountValidate): Observable<void> {
    this.userService.rejectProxyAuth();
    this.awsService.addAction('BPP Login=>Error', typeof error === 'string' ? { error } : error);
    // Proceed with login flow if BPP is unavailable.
    // User should stay logged in OpenAPI if auth to BPP failed.
    return throwError(error);
  }

  private reloginBppToCommand(): Promise<void> {
    return this.reLoginBpp().pipe(first()).toPromise();
  }
}
