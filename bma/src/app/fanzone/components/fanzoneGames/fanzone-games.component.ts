import { Component, OnInit, OnDestroy } from '@angular/core';
import { UserService as VanillaUserService, Page } from '@frontend/vanilla/core';
import { DeviceService } from '@app/core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { FanzoneHelperService } from '@app/core/services/fanzone/fanzone-helper.service';
import { FanzoneGamesService } from '@app/fanzone/services/fanzone-games.service';
import { CasinoGamesClientConfig } from '@app/client-config/bma-casino-games-config';
import { FanzoneSharedService } from '@app/lazy-modules/fanzone/services/fanzone-shared.service';
import { FANZONE_GAMES, GTM_DATA_FZ_GAMES } from '@lazy-modules/fanzone/fanzone.constant';
import { channelName } from '@app/fanzone/fanzone.constant';
import { FanzoneDetails } from '@app/core/services/fanzone/models/fanzone.model';
import { IFanzoneGamesSignPostingData, IFanzoneGame } from "@app/fanzone/models/fanzone-games.model";
import { UserService } from '@app/core/services/user/user.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';
@Component({
  selector: 'app-fanzone-games',
  template: ``,
})

export class FanzoneAppGamesComponent implements OnInit, OnDestroy {
  channelName = channelName;
  fanzoneGamesHost: string;
  fanzoneGames: IFanzoneGame[] = [];
  clientConfig;
  newSignPostingData: IFanzoneGamesSignPostingData;
  fanzoneDetails: FanzoneDetails;
  constructor(private windowRef: WindowRefService,
    private page: Page,
    private deviceService: DeviceService,
    private casinoGamesConfig: CasinoGamesClientConfig,
    private user: VanillaUserService,
    private userService: UserService,
    protected fanzoneGamesService: FanzoneGamesService,
    protected fanzoneSharedService: FanzoneSharedService,
    protected gtmService: GtmService,
    private fanzoneStorageService: FanzoneStorageService,
    protected pubSubService: PubSubService,
    protected fanzoneHelperService: FanzoneHelperService,
  ) { }

  /**
   * to do initializations
   * @returns {void}
   */
  ngOnInit(): void {
    this.pubSubService.subscribe(this.channelName, this.pubSubService.API.FANZONE_DATA, (fanzone: FanzoneDetails) => {
      this.fanzoneDetails = fanzone;
      this.fanzoneGames.length == 0 && this.buildFanzoneGamesData();
    });
    this.fanzoneDetails = this.fanzoneHelperService.selectedFanzone;

    this.getNewSignPostingData();
    this.getFanzoneGamesHost();
    this.fanzoneDetails && this.fanzoneGames.length == 0 && this.buildFanzoneGamesData();
    this.pubSubService.subscribe('fanzoneGamesSubscription', this.pubSubService.API.HIDE_FANZONE_GAMES_TAB, () => {
      this.fanzoneGames = [];
    });
  }

  /**
   * Gets newsignposting data from cms
   * @returns {void}
   */
  getNewSignPostingData(): void {
    this.fanzoneSharedService.getFanzoneNewSignPosting()
      .subscribe((res: IFanzoneGamesSignPostingData[]) => {
        this.newSignPostingData = res[0];
      });
  }

  /**
   * Gets fanzone games host from clientconfig
   * @returns {void}
   */
  getFanzoneGamesHost(): void {
    this.clientConfig = (this.windowRef.nativeWindow && this.windowRef.nativeWindow.clientConfig) || {};
    this.fanzoneGamesHost = this.casinoGamesConfig.miniGamesHost;
  }

  /**
   * Builds fanzone games Array
   * @returns {void}
   */
  buildFanzoneGamesData(): void {
    FANZONE_GAMES.SUPPORTED_GAMES.forEach((game) => {
      if (this.fanzoneDetails.fanzoneConfiguration[game.CMS_FLAG_NAME]) {
        this.fanzoneGames.push({
          gameName: game.GAME_NAME,
          gameDisplayName: game.GAME_DISPLAY_NAME,
          gameVariantName: game.GAME_VARIANT_NAME,
          gameThumbnailUrl: this.getThumbnailAndGameUrls(game.GAME_VARIANT_NAME).gameThumbnailUrl,
          gameLaunchUrl: this.getThumbnailAndGameUrls(game.GAME_VARIANT_NAME).gameLaunchUrl,
          showGame: this.suppressGameForRGYUsers(game.GAME_NAME)
        });
      }
    });
  }

  /**
   * Gets fanzone games thumbnail and game launch url
   * @returns {void}
   */
  getThumbnailAndGameUrls(gameName: string) {
    const urls = {
      gameThumbnailUrl: '',
      gameLaunchUrl: ''
    };
    const fanzoneTeam = this.fanzoneStorageService.get('fanzone');
    if (this.deviceService.isMobileOnly) {
      urls.gameThumbnailUrl = this.buildFanzoneGameImageUrl(this.casinoGamesConfig.fzGmImgMbUrl, gameName, fanzoneTeam);
      urls.gameLaunchUrl = this.buildFanzoneGameLaunchUrl(this.casinoGamesConfig.fzGmLaMbUrl, gameName, fanzoneTeam);
    } else {
      urls.gameThumbnailUrl = this.buildFanzoneGameImageUrl(this.casinoGamesConfig.fzGmImgDsUrl, gameName, fanzoneTeam);
      urls.gameLaunchUrl = this.buildFanzoneGameLaunchUrl(this.casinoGamesConfig.fzGmLaDsUrl, gameName, fanzoneTeam);     
    }
    return urls;
  }

  /**
   * Builds Dynamic Game Thumbnail url
   * @returns {void}
   */
  buildFanzoneGameImageUrl(gameImageUrl: string, gameName: string, fanzoneTeam): string {
    return this.fanzoneGamesHost + gameImageUrl.replace('$GAMENAME$', `${gameName}_${fanzoneTeam.teamId}`);
  }

  /**
   * Builds Dynamic Game Launch url
   * @returns {void}
   */
  buildFanzoneGameLaunchUrl(gameLaunchUrl: string, gameName: string, fanzoneTeam): string {
    return this.fanzoneGamesHost + gameLaunchUrl
      .replace('$casinogamelang$', this.getPageCulture())
      .replace('$GAMENAME$', gameName)
      .replace('$LANGID$', this.getPageCulture())
      .replace('$CHANNELID$', (this.deviceService.isIos) ? (this.deviceService.isWrapper ? FANZONE_GAMES.CHANNELID.IN : FANZONE_GAMES.CHANNELID.IOS)
        : (this.deviceService.isWrapper ? FANZONE_GAMES.CHANNELID.AN : FANZONE_GAMES.CHANNELID.ANDROID))
      .replace('$ENV$', this.getEnvironment())
      .replace('$LOBBYURL$',this.windowRef.nativeWindow.location.href)
      .replace('$HOSTURL$', '')
      .replace('$SESSIONKEY$', this.user.claims.get('ssotoken'))
      .replace('$USERTOKEN$', this.clientConfig && this.clientConfig.vnClaims['http://api.bwin.com/v3/user/usertoken'].toString())
      .replace('$SESSIONTOKEN$', this.clientConfig && this.clientConfig.vnClaims['http://api.bwin.com/v3/user/sessiontoken'].toString())
      .replace('$pLANG$', this.clientConfig && this.clientConfig.vnUser && this.clientConfig.vnUser.lang)
      .replace('$TIMESTAMP$', new Date().getTime().toString())
      .replace('$CURRENCY$', this.clientConfig && this.clientConfig.vnClaims['http://api.bwin.com/v3/user/currency'])
      .replace('$USERIP$', this.casinoGamesConfig.userHostAddress)
      .replace('$TEAM_ID$', fanzoneTeam.teamId)
      .replace('$TEAM_NAME$', fanzoneTeam.teamName);
  }

  /**
   * Hiding Fanzone games for RGY users
   * @returns {void}
   */
  suppressGameForRGYUsers(gameName: string): boolean {
    let suppressGame = false;
    if (FANZONE_GAMES.SUPPRESS_GAMES_RGY_USERS.includes(gameName)) {
      suppressGame = this.userService.bonusSuppression;
    }
    return suppressGame;
  }

  /**
   * sets new date only when date is null or not in between cms start date and end date
   * @returns {void}
   */
  ngOnDestroy(): void {
    this.fanzoneGamesService.setNewSignPostingSeenDate(this.newSignPostingData);
    this.pubSubService.unsubscribe('fanzoneGamesSubscription');
  }

  /**
   * Launches Game on click of game image
   * @returns {void}
   */
  launchGame(gameDetails: IFanzoneGame, index: number, isGameImageClicked: boolean = true): void {
      if (this.deviceService.isMobileOnly) {
        this.windowRef.nativeWindow && this.windowRef.nativeWindow.open(gameDetails.gameLaunchUrl, '_self');
      } else {
        this.fanzoneSharedService.showGameLaunchPopup({
          gameLaunchUrl : gameDetails.gameLaunchUrl, 
          gameDisplayName : gameDetails.gameDisplayName
        });
      }
    this.setGtmData(index, gameDetails, isGameImageClicked);
  }

   /**
   * Launches Game on click of play now button
   * @returns {void}
   */
   playNow($event: Event, gameDetails: IFanzoneGame, index: number): void {
    $event.stopPropagation();
    this.launchGame(gameDetails, index, false);
  }

  /**
   * set GA tracking object
   * @param {position: number}
   * @returns {void}
   */
  setGtmData(position: number, gameDetails: IFanzoneGame, isGameImageClicked: boolean): void {
    const gtmData = {
      'component.CategoryEvent': GTM_DATA_FZ_GAMES.CATEGORY_EVENT,
      'component.LabelEvent': GTM_DATA_FZ_GAMES.LABEL_EVENT,
      'component.ActionEvent': GTM_DATA_FZ_GAMES.ACTION_EVENT,
      'component.PositionEvent': position+1,
      'component.LocationEvent': GTM_DATA_FZ_GAMES.LOCATION_NAMES[gameDetails.gameName],
      'component.EventDetails': isGameImageClicked ? GTM_DATA_FZ_GAMES.LOCATION_NAMES[gameDetails.gameName] : GTM_DATA_FZ_GAMES.CTA_NAME,
      'component.URLclicked': GTM_DATA_FZ_GAMES.URL_CLICKED
    };
    this.gtmService.push(GTM_DATA_FZ_GAMES.EVENT, gtmData);
  }

  /**
   * Function replaces '-' with '_' in the langId, during image click URL generation.
   * @returns {string}
   */
  private getPageCulture(): string {
    return this.page.culture && this.page.culture.replace('-', '_');
  }

  /**
   * Function gets the env. type from clientConfig object and returns it.
   * @returns {string}
   */
  private getEnvironment(): string {
    const envStr = this.clientConfig && this.clientConfig.vnProductHomepages &&
      this.clientConfig.vnProductHomepages.sports && this.clientConfig.vnProductHomepages.sports.substr(0,
        this.clientConfig.vnProductHomepages.sports.indexOf('sports'));
    if (envStr.includes('qa'))
      return 'QA';
    else if (envStr.includes('test'))
      return 'FVT';
    else if (envStr.includes('beta'))
      return 'BETA'
    else
      return 'PROD';
  }
}