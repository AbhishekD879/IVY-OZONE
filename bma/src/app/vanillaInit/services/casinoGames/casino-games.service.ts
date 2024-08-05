import { Injectable } from '@angular/core';
import { UserService, ClaimsConfig } from '@frontend/vanilla/core';
import { CasinoGamesClientConfig } from '@app/client-config/bma-casino-games-config';
import { ProductHomepagesConfig } from '@frontend/vanilla/core';

@Injectable({
  providedIn: 'root'
})
export class CasinoGamesService {

  constructor(
    private user: UserService,
    private casinoGamesConfig: CasinoGamesClientConfig,
    private productHomepagesConfig: ProductHomepagesConfig,
    private claimsConfig: ClaimsConfig
  ) { }

  get isMiniGamesEnabled(): boolean {
    return this.casinoGamesConfig.miniGamesEnabled;
  }
  set isMiniGamesEnabled(value:boolean){}

  get miniGamesUrl(): string {
    return this.casinoGamesConfig.miniGamesHost + this.templateUrl;
  }
  set miniGamesUrl(value:string){}

  get isRecentlyPlayedGamesEnabled(): boolean {
    return this.casinoGamesConfig.recentlyPlayedGamesEnabled;
  }
  set isRecentlyPlayedGamesEnabled(value:boolean){}

  get recentlyPlayedGamesUrl(): string {
    return this.productHomepagesConfig.casino + this.casinoGamesConfig.recentlyPlayedGamesUrl;
  }
  set recentlyPlayedGamesUrl(value:string){}

  get isSeeAllEnabled(): boolean {
    return this.casinoGamesConfig.seeAllEnabled;
  }
  set isSeeAllEnabled(value:boolean){}

  get seeAllUrl(): string {
    return this.productHomepagesConfig.casino + this.casinoGamesConfig.seeAllUrl;
  }
  set seeAllUrl(value:string){}

  private get templateUrl(): string {
  const nameidentifier = 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier';

    return this.casinoGamesConfig.miniGamesTemplate
      .replace('$USERIP$', this.casinoGamesConfig.userHostAddress)
      .replace('$CURRENCY$', this.user.claims.get('currency'))
      .replace('$SESSION_KEY$', this.user.claims.get('ssotoken'))
      .replace('$HOSTURL$', this.productHomepagesConfig.sports)
      .replace('$accountName$', this.claimsConfig[nameidentifier]);
  }
  private set templateUrl(value:string){}
}
