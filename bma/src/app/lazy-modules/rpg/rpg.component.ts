import { Component, OnInit, Input, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { RPG_CONSTANTS } from './rpg.constants';
import { DeviceService } from '@app/core/services/device/device.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { HttpClient } from '@angular/common/http';
import { UserService, Page } from '@frontend/vanilla/core';
import { IRpgConfig, IRpgResponse, IGymlResponse, IRpgGameModel, IRpgPayload } from '@app/lazy-modules/rpg/rpg.model';
import { Observable } from 'rxjs';
import { StorageService } from '@app/core/services/storage/storage.service';
import { CasinoGamesClientConfig } from '@app/client-config/bma-casino-games-config';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';

@Component({
  selector: 'rpg',
  templateUrl: './rpg.component.html',
  styleUrls: ['./rpg.component.scss'],
})
export class RpgComponent implements OnInit, OnDestroy {
  @Input() rpgModule: IRpgConfig;
  @Input() userName: string;

  showContent: boolean = true;
  rpgGamesData: IRpgGameModel[] = [];
  categoryId: string;
  lobbyType: string;
  subCategoryId: string;
  maxTitleLength = RPG_CONSTANTS.maxTitleLength;
  isScrollDone: boolean = false;
  seeAllGaming = RPG_CONSTANTS.seeAllGaming;
  lastSetTimeout;
  clientConfig;
  brand: string;
  frontend: string;
  rpgUrl: string;
  rpgPayload: IRpgPayload;
  gymlUrl: string;

  constructor(
    private windowRef: WindowRefService,
    private deviceService: DeviceService,
    private page: Page,
    private gtmService: GtmService,
    private http: HttpClient,
    private storageService: StorageService,
    private casinoGamesConfig: CasinoGamesClientConfig,
    private user: UserService,
    private changeDetectorRef: ChangeDetectorRef,
    private awsFirehoseService: AWSFirehoseService,
  ) { }

  ngOnInit(): void {
    this.clientConfig = (this.windowRef.nativeWindow && this.windowRef.nativeWindow.clientConfig) || {};
    this.brand = this.clientConfig.vnAppInfo && this.clientConfig.vnAppInfo.brand;
    this.frontend = this.clientConfig.vnAppInfo && this.clientConfig.vnAppInfo.frontend;
    const storedRpgData: { filteredRpg: IRpgGameModel[], timestamp: number, username: string } = this.storageService.get('filteredRpgData');
    const currentTimestamp = new Date().getTime();

    if (!storedRpgData || currentTimestamp - storedRpgData.timestamp > this.casinoGamesConfig.rpgCacheExpiry * 60 * 1000
      || this.userName !== storedRpgData.username) {
      this.rpgUrl = this.casinoGamesConfig.recentlyPlayedGamesUrl;
      this.rpgPayload = this.casinoGamesConfig.rpgPayload;
      this.gymlUrl = this.casinoGamesConfig.gymlUrl;

      if (!this.gymlUrl || !this.rpgUrl || !this.rpgPayload)
        return;

      this.getCasinoData();
    } else {
      this.rpgGamesData = storedRpgData.filteredRpg;
      this.rpgGamesData = this.rpgGamesData.filter(game => !!(game.gamevariant && game.displayname && game.imageUrl));
      this.changeDetectorRef.detectChanges();
      this.setGATracking('contentView', 'load', 'not applicable', 'not applicable', 'not applicable');
      this.setCarouselScrollTrack();
    }
  }

  /**
   * Function is responsible generation of URL and navigate to it after GYML carousel click
   * @param {string} gameName
   * @param {number} carouselIndex
   * @returns {void}
   */
  rpgCarouselClick(gameName: string, carouselIndex: string): void {
    const url = this.casinoGamesConfig.miniGamesHost + this.casinoGamesConfig.gameLaunchUrl
      .replace('$GAMENAME$', gameName)
      .replace('$LANGID$', this.getPageCulture())
      .replace('$CHANNELID$', (this.deviceService.isIos) ? (this.deviceService.isWrapper ? RPG_CONSTANTS.ChannelIds.IN : RPG_CONSTANTS.ChannelIds.IOS)
        : (this.deviceService.isWrapper ? RPG_CONSTANTS.ChannelIds.AN : RPG_CONSTANTS.ChannelIds.Android))
      .replace('$ENV$', this.getEnvironment())
      .replace('$USERIP$', this.casinoGamesConfig.userHostAddress)
      .replace('$SESSIONKEY$', this.user.claims.get('ssotoken'))
      .replace('$LOBBYURL$', this.clientConfig && this.clientConfig.vnProductHomepages &&
        this.clientConfig.vnProductHomepages.sports)
      .replace('$pLANG$', this.clientConfig && this.clientConfig.vnUser && this.clientConfig.vnUser.lang)
      .replace('$USERTOKEN$', this.clientConfig && this.clientConfig.vnClaims['http://api.bwin.com/v3/user/usertoken'].toString())
      .replace('$SESSIONTOKEN$', this.clientConfig && this.clientConfig.vnClaims['http://api.bwin.com/v3/user/sessiontoken'].toString())
      .replace('$TIMESTAMP$', new Date().getTime().toString())
      .replace('$COLNUMBER$', (carouselIndex + 1).toString());

    this.setGATracking('trackEvent', 'cross sell - click', gameName, url.toString(), (carouselIndex + 1).toString());
    this.windowRef.nativeWindow && this.windowRef.nativeWindow.open(url, '_self');
  }

  /**
   * Function is responsible navigating to gaming URL after 'See All Gaming' click
   * @param {string} seeAllUrl
   * @returns {void}
   */
  seeMoreClick(seeAllUrl: string): void {
    this.setGATracking('trackEvent', 'see all - click', 'see all gaming', seeAllUrl, 'not applicable');
    this.windowRef.nativeWindow && this.windowRef.nativeWindow.open(seeAllUrl, '_self');
  }

  ngOnDestroy(): void {
    const carouselContainerElem = document.querySelector('.rpg-carousel-container');
    carouselContainerElem && carouselContainerElem.removeEventListener('scroll', this.scrollEventCallback);
  }

  /**
   * Function handles the callback on scroll in rpg module
   */
  private scrollEventCallback = () => {
    this.windowRef.nativeWindow && this.windowRef.nativeWindow.clearTimeout(this.lastSetTimeout);
    this.lastSetTimeout = this.windowRef.nativeWindow && this.windowRef.nativeWindow.setTimeout(() => {
      this.setGATracking('contentView', 'cross sell - scroll', 'scrolled horizontally',
        'not applicable', 'not applicable');
    }, 66);
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

    return envStr.includes('qa') ? 'QA' : (envStr.includes('test') ? 'FVT' : 'PROD');
  }

  /**
   * Function returns response of Http Rpg call.
   * @returns {Observable<IRpgResponse>}
   */
  private getRpgData(): Observable<IRpgResponse> {
    const payload = this.rpgPayload;
    payload.accountName = (this.brand === 'CORAL' ? 'cl' : 'ld') + `_${this.userName}`;
    payload.channelId = (this.deviceService.isIos) ? (this.deviceService.isWrapper ? RPG_CONSTANTS.ChannelIds.IN : RPG_CONSTANTS.ChannelIds.IOS)
        : (this.deviceService.isWrapper ? RPG_CONSTANTS.ChannelIds.AN : RPG_CONSTANTS.ChannelIds.Android);
    return this.http.post<IRpgResponse>(this.rpgUrl, payload);
  }

  /**
   * Function returns response of Http GYML call.
   * @returns {Observable<IGymlResponse>}
   */
  private getGymlData(): Observable<IGymlResponse>{
    return this.http.get<IGymlResponse>(this.gymlUrl);
  }

  /**
   * Function makes calls to get rpg, gyml and disabled games, to generate a carousel list of max. 10.
   * Only then shows RPG module in the UI.
   */
  private getCasinoData(): void {
    this.rpgUrl && this.getRpgData().subscribe((rpgData: IRpgResponse) => {
      this.awsFirehoseService.addAction(`RPG call to casino APIs triggered => userName: , ${ this.userName }`);
      if (rpgData && rpgData.status === 'Success' && rpgData.games && rpgData.games.length > 0) {
        this.rpgGamesData = rpgData.games;
        this.rpgGamesData = this.rpgGamesData.slice(0,this.rpgModule.gamesAmount);
        this.rpgGamesData.forEach(game => game.imageUrl = this.casinoGamesConfig.miniGamesHost + this.casinoGamesConfig.gameImageUrl.replace('{0}', game.gamevariant))
        this.rpgGamesData = this.rpgGamesData.map(game => {return {displayname: game.displayname, gamevariant: game.gamevariant, imageUrl: game.imageUrl}});
        this.setGATracking('contentView', 'load', 'not applicable', 'not applicable', 'not applicable');
   
        if (this.rpgGamesData.length < this.rpgModule.gamesAmount) {
          this.gymlUrl && this.getGymlData().subscribe((gymlData: IGymlResponse) => {
            this.awsFirehoseService.addAction(`GYML call to casino APIs triggered => userName: , ${ this.userName }`);
            const rpgGamevariantArr = this.rpgGamesData.map(game => game.gamevariant);
            let gymlGamesArr = gymlData.gamelist;
            // remove games from GYML that are already there in RPG
            gymlGamesArr = gymlGamesArr.filter(game => !rpgGamevariantArr.includes(game.game));

            for (let gameIndex = 0; gameIndex < gymlGamesArr.length; gameIndex++) {
              gymlGamesArr[gameIndex].gamevariant = gymlGamesArr[gameIndex].game;
              gymlGamesArr[gameIndex].displayname = gymlGamesArr[gameIndex].name;
              gymlGamesArr[gameIndex].imageUrl = this.casinoGamesConfig.miniGamesHost + this.casinoGamesConfig.gameImageUrl.replace('{0}', gymlGamesArr[gameIndex].gamevariant);
              this.rpgGamesData.push(gymlGamesArr[gameIndex]);
              if (this.rpgGamesData.length === this.rpgModule.gamesAmount)
                break;
            }
            this.rpgGamesData = this.rpgGamesData.map(game => {return {displayname: game.displayname, gamevariant: game.gamevariant, imageUrl: game.imageUrl}});
            this.changeDetectorRef.detectChanges();
            this.setScrollAndStoreRpgData(this.rpgGamesData);
          });
        } else {
          this.changeDetectorRef.detectChanges();
          this.setScrollAndStoreRpgData(this.rpgGamesData);
        }
      }
    });
  }

  /**
   * Function generates the GA tracking object and pushes data to it.
   * @param {string} eventType
   * @param {string} actionEvent
   * @param {string} eventDetails
   * @param {string} urlClicked
   * @param {string} modulePosition
   */
  private setGATracking(eventType: string, actionEvent: string, eventDetails: string, urlClicked: string,
    modulePosition: string): void {
    const gtmData = {
      event: eventType,
      'component.CategoryEvent': 'X- Sell',
      'component.LabelEvent': 'casino',
      'component.ActionEvent': actionEvent,
      'component.PositionEvent': 'not applicable',
      'component.LocationEvent': 'Games You Might Like',
      'component.EventDetails': eventDetails,
      'component.URLClicked': urlClicked,
      'component.moduleName': 'GYML Banner',
      'component.modulePosition': modulePosition,
      'component.moduleCustName': 'banner_top',
      'component.moduleSource': 'standard module',
      'component.pageLayout': 'HomeLobby'
    };
    this.gtmService.push(gtmData.event, gtmData);
  }

  /**
   * Function gets carousel container element and assigns scroll event listener to it.
   */
  private setCarouselScrollTrack(): void {
    const carouselContainerElem = document.querySelector('.rpg-carousel-container');
    carouselContainerElem && carouselContainerElem.addEventListener('scroll', this.scrollEventCallback, false);
  }

  /**
   * Function is responsible to store final rpgData array in local storage and call carousel scroll track.
   * @param {string} filteredRpg
   * @returns {void}
   */
  private setScrollAndStoreRpgData(filteredRpg: IRpgGameModel[]): void {
    this.storageService.set('filteredRpgData', {filteredRpg, timestamp: new Date().getTime(), username: this.userName});
    this.setCarouselScrollTrack();
  }
}
