import { forkJoin, Observable, of, ReplaySubject } from 'rxjs';
import { catchError, first, map, shareReplay } from 'rxjs/operators';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Inject, Injectable, OnDestroy } from '@angular/core';
import * as _ from 'underscore';
import environment from '@environment/oxygenEnvConfig';
import { PubSubService } from '../communication/pubsub/pubsub.service';
import { DeviceService } from '../device/device.service';
import { CmsToolsService } from './cms.tools';
import {
  IBybMarket,
  ICountryCode,
  IDesktopQuickLink,
  IEdpMarket,
  IFootball3DBanner,
  IFooterMenu,
  IHeaderSubMenu,
  IInitialData,
  IMaintenancePage,
  IOddsBoostConfig,
  IOffersList,
  IPromotionLiteList,
  IPromotionsList,
  IRetailMenu,
  ISeoPage,
  ISeoPagesPaths,
  ISportCategory,
  IStaticBlock,
  ISystemConfig,
  IWidget,
  IYourCallLeague,
  IYourCallStaticBlock,
  IOtfStaticContent,
  IOtfIosToggle,
  ISportConfig,
  IFormation,
  IQuizSettings,
  ISportTabs,
  ILeague
} from './models';
import { INavigationPoint } from '@core/services/cms/models';
import { ISvgItem } from '@core/services/cms/models/svg-item.model';
import { ICompetitionsConfig } from '@core/services/cms/models/system-config';
import {
  CONNECT_PROMOTION_CATEGORY_ID,
  FEATURE_TOGGLE_KEYS,
  global_stakes
} from '@core/services/cms/cms.constants'; // TODO: rename to retail after changes in cms.
import { ICouponSegment } from '@sb/components/couponsList/coupons-list.model';
import { ICouponMarketSelector } from '@shared/components/marketSelector/market-selector.model';
import { IFeaturedModule } from '@featured/components/featured-tab/featured-module.model';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { IEdpSurfaceBetDto } from '@core/services/cms/models/surface-bet-dto.model';
import { CasinoLinkService } from '@core/services/casinoLink/casino-link.service';
import { NativeBridgeService } from '@app/core/services/nativeBridge/native-bridge.service';
import { UserService } from '@core/services/user/user.service';
import { IQuizPopupSettings } from '@core/services/cms/models/quiz-settings.model';
import { ITimelineSettings } from '@core/services/cms/models/timeline-settings.model';
import { IVirtualSportAliasesDto, IVirtualSports } from '@core/services/cms/models/virtual-sports.model';
import { ITimelineDetails } from '@core/services/cms/models/timeline-tutorial.model';
import { IJourneyStaticBlocks } from '@core/services/cms/models/five-a-side-journey.model';
import { IMarketLinks } from '@core/services/cms/models/edp-market.model';
import { ILeagueLink } from '@core/services/cms/models/league-links.model';
import { IRacingEdpMarket } from '@core/services/cms/models/racing-edp-market.model';
import { IArcUserData } from '@app/lazy-modules/arcUser/model/arcUser-model';
import { SegmentEventManagerService } from '@lazy-modules/segmentEventManager/service/segment-event-manager.service';
import { SegmentedCMSService } from '@app/core/services/cms/segmented-cms.service';
import { IAutoSeoPages } from '@app/core/services/cms/models/seo/seo-pages-paths';
import { FanzoneClub, FanzoneDetails } from "@app/core/services/fanzone/models/fanzone.model";
import { FANZONE_CATEGORY_ID } from '@app/fanzone/constants/fanzoneconstants';
import { IOnboardingOverlay } from '@app/sb/components/couponsDetails/onboarding-coupon-stat-overlay.model';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';
import { NICMSConfig } from '@lazy-modules/networkIndicator/components/network-indicator/network-indicator.model';
import { RGYConfig, YellowFlagInfo } from '../user/yellow-flag.model';
import { IBetShare } from '@app/betHistory/models/bet-share.model';
import { ILottoCms} from '@app/lotto/models/lotto.model';
import { IFeaturedModel } from '@app/featured/models/featured.model';
import {IStatisticalContent} from '@core/services/cms/models/statistical-content-info.model';
import { IFanzoneComingBack } from '@app/lazy-modules/fanzone/models/fanzone-cb.model';
import { IFanzoneVacation } from '@app/fanzone/models/fanzone-vacation.model';

@Injectable({ providedIn: 'root' })
export class CmsService implements OnDestroy {

  initialData: IInitialData;
  initialRGYData: RGYConfig;
  lang: string = 'en-us';

  CMS_ENDPOINT: string;
  CMS_ROOT_URI: string;
  SURFACE_BETS_URL: string;

  brand: string = environment.brand;

  systemConfiguration: ISystemConfig;
  leaguesData: IYourCallLeague[];
  appBuildVersion: string;
  featureConfigMap: Map<string, Observable<ISystemConfig>> = new Map<string, Observable<ISystemConfig>>();
  cmsYellowFlagInfo: YellowFlagInfo[] = null;
  hasExtraNavPoints:boolean = false;

  private widgets: IWidget[];
  private initialData$: ReplaySubject<IInitialData>;
  private initialRGYData$: ReplaySubject<RGYConfig>;
  private readonly sportNameRegexp: RegExp = /\s|\/|\||\-/g;
  private readonly SEGMENT_STORE_KEYTEXT: string = 'Segment';
  betShareData: Observable<IBetShare>;

  constructor(
    protected pubsub: PubSubService,
    protected cmsTools: CmsToolsService,
    protected device: DeviceService,
    protected http: HttpClient,
    protected coreToolsService: CoreToolsService,
    protected fanzoneStorageService: FanzoneStorageService,
    protected casinoDecoratorService: CasinoLinkService,
    protected nativeBridgeService: NativeBridgeService,
    protected userService: UserService,
    protected segmentEventManagerService: SegmentEventManagerService,
    protected segmentedCMSService: SegmentedCMSService,
    @Inject('CMS_CONFIG') protected cmsInitConfigPromise: Promise<IInitialData>
  ) {
    this.CMS_ENDPOINT = environment.CMS_ENDPOINT;
    this.SURFACE_BETS_URL = environment.SURFACE_BETS_URL;
    this.pubsub.subscribe('cmsService', this.pubsub.API.INITIATE_RGY_CALL, () => {
      this.getCMSRGYconfigData();
    });
    this.pubsub.subscribe('cmsService', this.pubsub.API.SESSION_LOGOUT, () => {
      this.fanzoneStorageService.set('rgy_data', null);
      this.cmsYellowFlagInfo = null;
    });
  }

  ngOnDestroy(): void {
    if (this.initialData$) {
      this.initialData$.unsubscribe();
    }
    if (this.initialRGYData$) {
      this.initialRGYData$.unsubscribe();
    }
  }

  /**
   *To set user restriction when the user is yellow flag enabled
  */
  setCMSYellowFlagInfo(modulesData: YellowFlagInfo[]): void {
    this.cmsYellowFlagInfo = modulesData;
  }

  /**
   * @returns YellowFlagInfo
   */
  getCMSYellowFlagInfo(): YellowFlagInfo[] {
    if(!this.cmsYellowFlagInfo) {
      this.cmsYellowFlagInfo = this.fanzoneStorageService.get('rgy_data');
    }
    return this.cmsYellowFlagInfo ? this.cmsYellowFlagInfo : this.fanzoneStorageService.get('rgy_data');
  }

  getStaticBlock(serviceName: string, locale?: string): Observable<IStaticBlock> {
    return this.getData(locale ? `static-block/${serviceName}-${locale}` : `static-block/${serviceName}`)
      .pipe(
        map((data: HttpResponse<IStaticBlock>) => data.body)
      );
  }

  getSystemConfig(preventCache: boolean = false): Observable<ISystemConfig> {
    if (this.systemConfiguration && !preventCache) {
      return of(this.systemConfiguration);
    }

    return this.getInitialSystemConfig();
  }

  getFSC(sportId: string): Observable<IFeaturedModel> {
    return this.getData(`fsc/${sportId}`)
      .pipe(
        map((data: HttpResponse<IFeaturedModel>) => data.body)
      );
  }

  getFeatureConfig(featureName: string, preventCache: boolean = false, shouldHandleError?: boolean): Observable<ISystemConfig> {
    if (this.featureConfigMap.has(featureName) && !preventCache) {
      return shouldHandleError ? this.featureConfigMap.get(featureName).pipe(catchError(() => of({})))
        : this.featureConfigMap.get(featureName);
    }
    return shouldHandleError ?
      this.getFeatureConfigByName(featureName).pipe(catchError(() => of({}))) :
      this.getFeatureConfigByName(featureName);
  }

  getCompetitions(sportName: string = '', preventCache: boolean = false): Observable<ICompetitionsConfig> {
    const competitionsCategory =
      `Competitions${sportName.charAt(0).toUpperCase() + sportName.slice(1).toLowerCase()}`;

    return this.getSystemConfig(preventCache)
      .pipe(
        map((config: ISystemConfig) => config[competitionsCategory])
      ); }

  getToggleStatus(featureName: FEATURE_TOGGLE_KEYS, preventCache: boolean = false): Observable<boolean> {
    return (this.getSystemConfig(preventCache))
      .pipe(
        map((config: ISystemConfig) => featureName && config && config.FeatureToggle && config.FeatureToggle[featureName])
      );
  }

  getCmsCountries(): Observable<ICountryCode[]> {
    return this.getData(`countries-settings`)
      .pipe(
        map((data: HttpResponse<ICountryCode[]>) => data.body)
      );
  }

  getInitialSystemConfig(): Observable<ISystemConfig> {
    return this.getCmsInitData()
      .pipe(
        map((data: IInitialData) => data.systemConfiguration)
      );
  }

  triggerSystemConfigUpdate(): void {
    this.getSystemConfig(true)
      .subscribe((config: ISystemConfig) => {
        this.pubsub.publish(this.pubsub.API.SYSTEM_CONFIG_UPDATED, [config]);
      });
  }

  getRibbonModule(): Observable<any> {
    return this.getCmsCSPInitData()
      .pipe(
        map((data: IInitialData) => {
          const modularContent = this.filterScheduleTabs(data.modularContent);
          return ({ getRibbonModule: modularContent });
        })
      );
  }

  getQuizPopupSetting(): Observable<IQuizPopupSettings> {
    return this.getCmsInitData()
      .pipe(
        map((data: IInitialData) => data.quizPopupSetting)
      );
  }

  getTimelineSetting(): Observable<ITimelineSettings> {
    return this.getCmsInitData()
      .pipe(
        map((data: IInitialData) => data.timelineConfig)
      );
  }

  getVirtualSports(): Observable<IVirtualSports[]> {
    return this.getData('virtual-sports')
      .pipe(
        map((data: HttpResponse<IVirtualSports[]>) => data.body)
      );
  }

  getVirtualSportstoPromise(): Promise<IVirtualSports[]> {
    return this.getData('virtual-sports')
      .pipe(
        map((data: HttpResponse<IVirtualSports[]>) => data.body)
      ).toPromise();
  }

  getVirtualSportAliases(): Observable<IVirtualSportAliasesDto[]> {
    return this.getCmsInitData()
      .pipe(
        map((data: IInitialData) => data.vsAliases)
      );
  }

  getContactUs(): Observable<IStaticBlock> {
    return this.getData(`static-block/contact-us${this.lang ? `-${this.lang}` : ''}`)
      .pipe(
        map((data: HttpResponse<IStaticBlock>) => data.body)
      );
  }

  getPrivateMarketsTermsAndConditions(): Observable<IStaticBlock> {
    return this.getData(`static-block/private-markets-terms-and-conditions${this.lang ? `-${this.lang}` : ''}`)
      .pipe(
        map((data: HttpResponse<IStaticBlock>) => data.body)
      );
  }

  getFreebetsHelperText(): Observable<IStaticBlock> {
    return this.getData('static-block/freebets-helper-text')
      .pipe(
        map((data: HttpResponse<IStaticBlock>) => data.body)
      );
  }

  getStatisticalContent(eventId: string): Observable<IStatisticalContent[]> {
    return this.getData(`statistic-content/${eventId}`)
      .pipe(
        map((data: HttpResponse<IStatisticalContent[]>) => data.body.filter(content => this.isActiveRange(content.startTime, content.endTime)))
      );
  }

  /**
   * Method to check if fanzone system config is disabled
   * @returns - boolean
   */
  isFanzoneConfigDisabled(): Observable<boolean> {
    return this.getSystemConfig().pipe(map((data) => {
      if (data.Fanzone.enabled) {
        return false;
      }
      return true;
    }));
  }

  getMenuItems(appBuildVersion?: string, selectedTeam?: FanzoneDetails): Observable<ISportCategory[]> {
    const observableMenuItems = this.getCmsCSPInitData(false)
      .pipe(
        map((data: IInitialData) => {
          this.nativeBridgeService.isRemovingGamingEnabled
            && this.isGamingEnabled()
            && this.casinoDecoratorService.filterGamingLinkForIOSWrapper(data.sportCategories);
          const appMenuProperties = data.systemConfiguration.GamingEnabled;
          //Adding the team name dynamically for fanzone requirements
          this.getFanzoneSportCategories(data.sportCategories, selectedTeam);
          if (this.device.isWrapper && this.device.isIos && appBuildVersion && appMenuProperties.iosVersionBlackList
            && appMenuProperties.iosVersionBlackList.includes(appBuildVersion)) {
            this.appBuildVersion = appBuildVersion;
            const sportCategoriesHeaderMenu: ISportCategory[] = [];
            data.sportCategories.forEach((sportCategory: ISportCategory, categoryIndex: number) => {
              if (!appMenuProperties.hostMenuBlackList.some((domainName: string) => sportCategory.targetUri.includes(domainName))) {
                sportCategoriesHeaderMenu.push(sportCategory);
              }
            });
            data.sportCategories = sportCategoriesHeaderMenu;
          }
          return this.cmsTools.processResult(data.sportCategories);
        })
      );

    return observableMenuItems;
  }

  getSportCategoryById(categoryId: number | string): Observable<ISportCategory> {
    return this.getCmsInitData()
      .pipe(
        map((data: IInitialData) => {
          return this.cmsTools.processResult(data.sportCategories).find((sportCategory: ISportCategory) => {
            const id = sportCategory.categoryId;
            return id ? sportCategory.categoryId.toString() === categoryId.toString() : false;
          });
        })
      );
  }

  getSportCategoryByIds(categoryIds: number[]): Observable<ISportCategory[]> {
    return this.getCmsInitData()
      .pipe(
        map((data: IInitialData) => {
          return this.cmsTools.processResult(data.sportCategories).filter((sportCategory: ISportCategory) => {
            const id = sportCategory.categoryId;
            return id ? categoryIds.includes(sportCategory.categoryId) : false;
          });
        })
      );
  }

  getSportCategoryByName(categoryName: string): Observable<ISportCategory> {
    const sportName = categoryName === 'greyhound' ? 'greyhoundracing' :
      categoryName.toLowerCase().replace(this.sportNameRegexp, '');
    return this.getCmsInitData()
      .pipe(
        map((data: IInitialData) => {
          return this.cmsTools.processResult(data.sportCategories).find((sportCategory: ISportCategory) => {
            const sportCategoryName = sportCategory.sportName
              && sportCategory.sportName.split('/').pop().toLowerCase().replace(this.sportNameRegexp, '');
            return sportCategoryName === sportName;
          });
        })
      );
  }

  getSportCategoriesByName(categoryNames: string[]): Observable<ISportCategory[]> {
    const sportNames: string[] = categoryNames.map(categoryName =>
      categoryName === 'greyhound' ? 'greyhoundracing' : categoryName.toLowerCase().replace(this.sportNameRegexp, ''));

    return this.getCmsInitData()
      .pipe(
        map((data: IInitialData) => {
          return this.cmsTools.processResult(data.sportCategories).filter((sportCategory: ISportCategory) => {
            const sportCategoryName = sportCategory.sportName
              && sportCategory.sportName.split('/').pop().toLowerCase().replace(this.sportNameRegexp, '');
            return sportNames.includes(sportCategoryName);
          });
        })
      );
  }

  getSports(): Observable<ISportCategory[]> {
    return this.getCmsInitData()
      .pipe(
        map((data: IInitialData) => this.cmsTools.processResult(data.sports))
      );
  }

  getOddsBoost(): Observable<IOddsBoostConfig> {
    return this.getCmsInitData()
      .pipe(
        map((data: IInitialData) => {
          return data.oddsBoost || {} as IOddsBoostConfig;
        })
      );
  }

  getCouponSegment(): Observable<ICouponSegment[]> {
    return this.getData('coupon-segments')
      .pipe(
        map((data: HttpResponse<ICouponSegment[]>) => data.body)
      );
  }

  getCouponMarketSelector(): Observable<ICouponMarketSelector[]> {
    return this.getData('coupon-market-selector')
      .pipe(
        map((data: HttpResponse<ICouponMarketSelector[]>) => data.body)
      );
  }

  getQuizPopupSettingDetails(): Observable<IQuizSettings> {
    return this.getData(`quiz-popup-setting-details`)
      .pipe(
        map((data: HttpResponse<IQuizSettings>) => data.body)
      );
  }

  getTimelineTutorialDetails(): Observable<ITimelineDetails> {
    return this.getData(`timeline-splash-config`)
      .pipe(
        map((data: HttpResponse<ITimelineDetails>) => data.body)
      );
  }

  getOnboardingOverlay(requestParam): Observable<IOnboardingOverlay> {
    return (this.getData(requestParam))
        .pipe(
            map((data: HttpResponse<IOnboardingOverlay>) => data.body)
        );
  }

  /**
   * Extract svg icons from cms initial data
   */
  extractInitialIcons(): Observable<string> {
    return this.getCmsInitData().pipe(
      map((data: IInitialData) => data.svgSpriteContent)
    );
  }

  getItemSvg(name: string, id?: number): Observable<ISvgItem> {
    const searchParam = id ? { categoryId: id } : { imageTitle: name };
    return this.getMenuItems()
      .pipe(
        map((menuItems: ISportCategory[]) => {
          const menuItem = _.find(menuItems, searchParam);
          return menuItem ? _.pick(menuItem, 'svg', 'svgId') : { svg: null, svgId: null };
        })
      );
  }

  getLottoBanner(): Observable<ILottoCms> {
    return this.getData('lotto-configs')
    .pipe(
      map((data: HttpResponse<ILottoCms>) => data.body)
    )
  }


  getAllPromotions(): Observable<IPromotionsList> {
    return this.getPromotions();
  }

  getRetailPromotions(): Observable<IPromotionsList> {
    return this.getPromotions(CONNECT_PROMOTION_CATEGORY_ID, true); // TODO: rename to retail after changes in cms.
  }

  getGroupedPromotions(): Observable<IPromotionsList> {
    return this.getData('grouped-promotions')
      .pipe(
        map((res: HttpResponse<IPromotionsList>) => {
          res.body.promotionsBySection.forEach((group) => {
            this.cmsTools.processResult(group.promotions);
          });
          return res.body;
        })
      );
  }

  getSignpostingPromotionsLight(): Observable<IPromotionLiteList> {
    return this.getCmsInitData()
      .pipe(
        map((data: IInitialData) => {
          return {
            promotions: this.cmsTools.processResult(data.initSignposting)
          };
        })
      );
  }

  getDesktopQuickLinks(): Observable<IDesktopQuickLink[]> {
    return this.getData(`desktop-quick-links`)
      .pipe(
        map((data: HttpResponse<IDesktopQuickLink[]>) => {
          data.body?.forEach((links: IDesktopQuickLink, linkIndex: number) => {
            if (links.title === 'BetPack' && !this.systemConfiguration[links.title].enableBetPack) {
              data.body.splice(linkIndex, 1);
            }
          });
          return this.cmsTools.processResult(data.body);
        })
      );
  }

  getFooterMenu(appBuildVersion?: string): Observable<IFooterMenu[]> {
    return this.getCmsCSPInitData()
      .pipe(
        map((data: IInitialData) => {
          this.nativeBridgeService.isRemovingGamingEnabled
            && this.isGamingEnabled() && this.casinoDecoratorService.filterGamingLinkForIOSWrapper(data.footerMenu);
          const appMenuProperties = data.systemConfiguration.GamingEnabled;
          if (this.device.isWrapper && this.device.isIos && this.appBuildVersion && appMenuProperties.iosVersionBlackList
            && appMenuProperties.iosVersionBlackList.includes(this.appBuildVersion)) {
              const footerMenuData: IFooterMenu[] = [];
            data.footerMenu.forEach((footerMenu: IFooterMenu, footerIndex: number) => {
              if (!appMenuProperties.hostMenuBlackList.some((domainName: string) => footerMenu.targetUri.includes(domainName))) {
                footerMenuData.push(footerMenu);
              }
            });
            data.footerMenu = footerMenuData;
          }
          return this.cmsTools.processResult(data.footerMenu);
        })
      );
  }

  getHeaderSubMenu(selectedTeam?: any): Observable<IHeaderSubMenu[]> {
    return this.getData(`header-submenu`)
      .pipe(
        map((data: HttpResponse<IHeaderSubMenu[]>) => {
          data.body?.forEach((headers: IHeaderSubMenu, headerIndex: number) => {
            if (headers.linkTitle === 'BetPack' && !this.systemConfiguration[headers.linkTitle].enableBetPack) {
              data.body.splice(headerIndex, 1);
            }
          });
          this.getFanzoneSportCategories(data.body, selectedTeam);
          return this.cmsTools.processResult(data.body);
        })
      );
  }

  getFanzoneSportCategories(data, selectedTeam) {
    data.forEach((sportCategory: any) => {
      if (sportCategory.categoryId === FANZONE_CATEGORY_ID) {
        const fanzoneTeam = this.fanzoneStorageService.get('fanzone') || {};
        this.isFanzoneConfigDisabled().subscribe((isFzConfigDisabled) => {
          if (isFzConfigDisabled) {
            sportCategory.targetUri = sportCategory.targetUri.indexOf('/vacation') === -1 ? `/${sportCategory.targetUri}/vacation` : sportCategory.targetUri;
            return;
          } else {
            if (selectedTeam) {
              sportCategory.targetUri = sportCategory.targetUri.split('/').splice(0, 3).join('/'); //actual configured cms url
              fanzoneTeam['teamName'] = selectedTeam.name;
              this.fanzoneStorageService.set('fanzone', fanzoneTeam);
            }
            if (fanzoneTeam && !sportCategory.targetUri.includes('now-next') && !sportCategory.targetUri.includes('club') && !sportCategory.targetUri.includes('games')) {
              sportCategory.targetUri = `/${sportCategory.targetUri}/${fanzoneTeam.teamName}/${this.getFanzoneRouteName(selectedTeam)}`;
            }
          }
      });
      }
    });
  }

  getFanzoneRouteName(selectedTeam): string {
    let routeName;
    if(selectedTeam && selectedTeam.fanzoneConfiguration) {
      if (selectedTeam.fanzoneConfiguration.showNowNext) {
        routeName = 'now-next';
      } else if (selectedTeam.fanzoneConfiguration.showStats) {
        routeName = 'stats';
      } else if (selectedTeam.fanzoneConfiguration.showClubs && !this.userService.bonusSuppression) { 
        routeName = 'club';
      } else if (selectedTeam.fanzoneConfiguration.showGames) {
        routeName = 'games';
      }
    }
    return routeName;
  }

  getRetailMenu(): Observable<IRetailMenu[]> {
    return this.getCmsInitData()
      .pipe(
        map((data: IInitialData) => {
          return this.cmsTools.processResult(data.connectMenu); // TODO: rename to retail after changes in cms.
        })
      );
  }

  /**
   * Set Device Type
   * Strange Data tructure it is an array of Offers lists. LIke group of lists.
   * @param {String} deviceType
   * @returns {IOffersList[]}
   */
  getOffers(deviceType: string): Observable<IOffersList[]> {
    return this.getV2Data(`offers/${deviceType}`)
      .pipe(
        map((data: HttpResponse<IOffersList[]>) => {
          const offersData = data.body;
          offersData.forEach((item: IOffersList) => this.cmsTools.processResult(item.offers));
          return offersData;
        })
      );
  }

  /**
   * if no widgets at the moment -
   *  get data from CMS
   * else - return widgets
   */
  getWidgets(): Observable<IWidget[]> {
    if (!this.widgets) {
      return this.getData(`widgets`)
        .pipe(
          map((data: HttpResponse<IWidget[]>) => {
            this.widgets = data.body;

            return this.widgets;
          })
        );
    }

    return of(this.coreToolsService.deepClone(this.widgets));
  }

  /**
   * get saved widgets
   * get saved system config
   * filter active widgets
   */
  getActiveWidgets(): Observable<IWidget[]> {
    return forkJoin(this.getWidgets(), this.getSystemConfig())
      .pipe(
        map(([widgets, sysConfig]: [IWidget[], ISystemConfig]) => {
          const activeWidgets = widgets.filter((widgetData) => {
            if (widgetData && widgetData.directiveName === 'favourites') {
              return this.checkFavouritesWidget(sysConfig);
            }
            return true;
          });

          return activeWidgets;
        })
      );
  }

  /**
   * check favourites widget
   * favourites widget can be activated for mobile, table, desktop
   */
  checkFavouritesWidget(sysConfig: ISystemConfig): boolean {
    if (this.device.strictViewType === 'mobile' && sysConfig.Favourites && sysConfig.Favourites.displayOnMobile) {
      return true;
    }
    if (this.device.strictViewType === 'tablet' && sysConfig.Favourites && sysConfig.Favourites.displayOnTablet) {
      return true;
    }
    return !!(this.device.strictViewType === 'desktop' && sysConfig.Favourites && sysConfig.Favourites.displayOnDesktop);
  }

  getSeoPage(id: string): Observable<ISeoPage> {
    return this.getData(`seo-page/${id}`)
      .pipe(
        map((data: HttpResponse<ISeoPage>) => data.body)
      );
  }

  getSportTabs(categoryId: string): Observable<ISportTabs> {
    return this.getData(`sport-tabs/${categoryId}`)
      .pipe(
        map((data: HttpResponse<ISportTabs>) => data.body)
      );
  }

  getSportConfig(categoryId: number): Observable<ISportConfig[]> {
    return this.getSportCategoryById(categoryId)
      .pipe(
        map((data: ISportCategory) => data ? [data.sportConfig] : [])
      );
  }

  getSportConfigs(categoryIds: number[]): Observable<ISportConfig[]> {
    return this.getSportCategoryByIds(categoryIds)
      .pipe(
        map((data: ISportCategory[]) => data ? data.map(el => el.sportConfig) : [])
      );
  }

  getSeoPagesPaths(): Observable<ISeoPagesPaths> {
    return this.getCmsInitData()
      .pipe(
        map((data: IInitialData) => data.seoPages)
      );
  }
  /**
   * @returns autoseopages object from getCmsInitData
   */
  getAutoSeoPages(): Observable<IAutoSeoPages> {
    return this.getCmsInitData().pipe(map((data: IInitialData) => data.seoAutoPages));
  }

  getFootball3DBanners(): Observable<IFootball3DBanner[]> {
    return this.getData(`3d-football-banners`)
      .pipe(
        map((data: HttpResponse<IFootball3DBanner[]>) => data.body)
      );
  }

  /**
   * get market links from cms
   * @returns {Observable<IMarketLinks[]>}
   */
  getMarketLinks(): Observable<IMarketLinks[]> {
    return this.getData(`market-links`)
      .pipe(
        map((data: HttpResponse<IMarketLinks[]>) => data.body)
      );
  }

 /**
   * Method to get Fanzone new season details
   * @returns - {Observable<IMarketLinks[]>}
   */
 getFanzoneNewSeason(): Observable<IFanzoneVacation[]> {
  return this.getData('fanzone-new-season')
    .pipe(
      map((fzData: HttpResponse<IFanzoneVacation[]>) => fzData.body)
    );
}

/**
 * Method to get Fanzone coming back details
 * @returns - {Observable<IMarketLinks[]>}
 */
getFanzoneComingBack(): Observable<IFanzoneComingBack[]> {
  return this.getData('fanzone-coming-back')
    .pipe(
      map((fzData: HttpResponse<IFanzoneComingBack[]>) => fzData.body)
    );
}

  getLeagues(): Observable<ILeague[]> {
    return this.getData(`leagues`)
      .pipe(
        map((data: HttpResponse<ILeague[]>) => data.body)
      );
  }

  getCouponLeagueLinks(couponId: string): Observable<ILeagueLink[]> {
    return this.getData(`league-links/${couponId}`)
      .pipe(map((data: HttpResponse<ILeagueLink[]>) => data.body));
  }

  getCmsYourCallLeaguesConfig(): Observable<IYourCallLeague[]> {
    const request = this.leaguesData ? of(this.leaguesData) :
      this.getData(`yc-leagues`)
        .pipe(
          map((data: HttpResponse<IYourCallLeague[]>) => {
            this.leaguesData = data.body;
            return data.body;
          })
        );

    return request;
  }

  getYourCallStaticBlock(): Observable<IYourCallStaticBlock[]> {
    return this.getData(`yc-static-block`)
      .pipe(
        map((data: HttpResponse<IYourCallStaticBlock[]>) => data.body)
      );
  }

  getEDPMarkets(): Observable<IEdpMarket[]> {
    return this.getData(`edp-markets`)
      .pipe(
        map((data: HttpResponse<IEdpMarket[]>) => data.body)
      );
  }

  /**
   * To Fetch racing edp markets
   */
  getRacingEDPMarkets(): Observable<IRacingEdpMarket[]> {
    return this.getData(`racing-edp-markets`)
      .pipe(
        map((data: HttpResponse<IRacingEdpMarket[]>) => data.body)
      ).pipe(
        catchError(() => of([]))
      );
  }
  

  getEDPSurfaceBets(eventId: number): Observable<IEdpSurfaceBetDto[]> {
    return this.getSurfaceBetsData(`edp-surface-bets/${eventId}`)
      .pipe(
        map((data: HttpResponse<IEdpSurfaceBetDto[]>) => data.body)
      );
  }


  getTeamsColors(teamNames: Array<string>, sportId: string | number): Observable<any[]> {
    return this.getData('asset-management', { teamNames: teamNames.join(',').toUpperCase(), sportId })
      .pipe(
        map((data: HttpResponse<any[]>) => data.body)
      );
  }

  getYourCallBybMarkets(): Observable<IBybMarket[]> {
    return this.getData(`byb-markets`)
      .pipe(
        map((data: HttpResponse<IBybMarket[]>) => data.body)
      );
  }

  /**
   * Loads 1-2-Free static content from CMS
   * @returns Promise
   */
  getOTFStaticContent(): Observable<IOtfStaticContent[]> {
    return this.getData('one-two-free/static-texts')
      .pipe(
        map((data: HttpResponse<IOtfStaticContent[]>) => data.body)
      );
  }

  /**
   * Loads formations for Five A Side
   * @returns Observable
   */
  getFiveASideFormations(): Observable<IFormation[]> {
    return this.getData(`five-a-side-formations`)
      .pipe(
        map((data: HttpResponse<IFormation[]>) => data.body)
      );
  }

  /**
   * Loads 1-2-Free get IosToggle from CMS
   * @returns Observable
   */
  getOTFIosToggle(): Observable<IOtfIosToggle> {
    return this.getData('one-two-free/otf-ios-app-toggle')
      .pipe(
        map((data: HttpResponse<IOtfIosToggle>) => data.body)
      );
  }

  getMaintenancePage(): Observable<IMaintenancePage[]> {
    return this.getData(`maintenance-page/${this.device.requestPlatform}`)
      .pipe(
        map((data: HttpResponse<IMaintenancePage[]>) => data.body || [])
      );
  }

  /**
   * This function is used to valdate to sow/hide market switcher dropdown based on global flag and sport level flag
   * @param sportName
   */
  getMarketSwitcherFlagValue(sportName: string): Observable<boolean> {
    const marketSwitcherFlag = (this.getFeatureConfig('MarketSwitcher', false, true))
      .pipe(
        map((config: ISystemConfig) => {
          if (config && config.AllSports && config[sportName]) {
            return true;
          } else {
            return false;
          }
        })
      );
    return marketSwitcherFlag;
  }

  /**
   * This functions go throw params and replace htmlMarkup from CMS Static Blocks. Template for parameter - [['param1']].
   * @param content
   * @param params
   * @returns {String} htmlMarkup from CMS
   */
  parseContent(content: string, params: string[] | string): string {
    let modifiedContent = content;
    const paramsArray = typeof params === 'string' ? JSON.parse(params) : params;
    paramsArray.forEach((param: string, index: number) => {
      modifiedContent = modifiedContent
        .replace(`[['currency']]`, this.userService.currencySymbol)
        .replace(`[['param${(index + 1)}']]`, param);
    });
    return modifiedContent;
  }

  /**
   * Check if BogToggle is true/false on cms
   * @returns {Observable<boolean>}
   */
  isBogFromCms(): Observable<boolean> {
    return this.getSystemConfig().pipe(
      map((config: ISystemConfig) => config.BogToggle && config.BogToggle.bogToggle));
  }

  /**
   * Check if EDPLogs is enabled in cms
   * @returns {Observable<boolean>}
   */
  isEDPLogsEnabled(): Observable<boolean> {
    return this.getSystemConfig().pipe(
      map((config: ISystemConfig) => config.EDPLogs && config.EDPLogs.enabled));
  }

  /**
   * Gets static blocks for 5-a-side journey, which are configured in CMS -> BYB -> BYB STATIC BLOCKS
   * and are active for 5-a-side
   * @returns {Observable<IJourneyStaticBlocks[]>}
   */
  getFiveASideStaticBlocks(): Observable<IJourneyStaticBlocks[]> {
    return this.getData(`5a-side-static-block`)
      .pipe(
        map((data: HttpResponse<IJourneyStaticBlocks[]>) => data.body)
      );
  }

  /*
   * Filter data from expired NavigationPoints and perform checks for OTF Extra Super Button
   * @param {Array} arr
   * @return {Array}
   * @private
   */
  getNavigationPoints(selectedModule?:Array<any>,type?:string): Observable<INavigationPoint[]> {
    return this.getCmsCSPInitData()
      .pipe(
        map((data: IInitialData) => {
          const extraNavigationPoints =  this.userService.username  && this.segmentedCMSService.getActiveExtraNavPoints(data,selectedModule,type);
          this.hasExtraNavPoints = extraNavigationPoints?.length > 0;
          if ( this.hasExtraNavPoints && this.fanzoneStorageService.get('OTF_SEGMENT') && this.fanzoneStorageService.get('OTF_SEGMENT').segment){
            return extraNavigationPoints;
          }else{
          return (data.navigationPoints || []).filter((point: INavigationPoint) => {
            return Date.now() < Date.parse(point.validityPeriodEnd) &&
              Date.now() > Date.parse(point.validityPeriodStart);
          });
        }
        })
      );
  }
  formArcData(reason: string, risk: string): Observable<IArcUserData> {
    return this.getArcData(reason, risk).pipe(map((arcCmsProfileConfig: HttpResponse<any>) => arcCmsProfileConfig.body));
  }
  /**
   * Makes Server call and returns RGYConfig observable by passing required parameters
   * @param  {string} reason
   * @param  {string} risk
   * @returns Observable
   */
  getCMSRGYconfig(reason: string, risk: string): Observable<RGYConfig> {
    return this.getRGYCMSdata().pipe(map((response: HttpResponse<RGYConfig>) => response.body));
  }

  /**
   * Checks local availability Returns RGYConfig observable by passing required parameters
   * @param  {string} reason
   * @param  {string} risk
   * @returns Observable
   */
  getCMSRGYconfigData(): Observable<RGYConfig | null> {
    this.initialRGYData$ = new ReplaySubject<RGYConfig>(1);
    if (this.userService.getPostLoginBonusSupValue() && !this.getCMSYellowFlagInfo()) {
      this.getRGYCMSdata().pipe(map((response: HttpResponse<RGYConfig[]>) => response.body))
        .subscribe((data: RGYConfig[]) => {
          this.releaseRGYDataSubject(data[0]);
          this.pubsub.publish(this.pubsub.API.RGY_DATA_LOADED, true);
        });
    } else {
      this.releaseRGYDataSubject(null);
    }

    return this.initialRGYData$.asObservable();
  }

  /**
   * Releases RGYConfig subject
   * @param  {RGYConfig} data
   * @returns void
   */
  protected releaseRGYDataSubject(data: RGYConfig): void {
    if (data) {
      this.initialRGYData = data;
      this.fanzoneStorageService.set('rgy_data', data.modules)
      this.setCMSYellowFlagInfo(data.modules);
    }
    this.initialRGYData$.next(this.initialRGYData);
    this.initialRGYData$.complete();
  }

  /**
   * Retrieves Network Indicator CMS Configuration
   * @returns Observable
   */
  getNetworkIndicatorConfig(): Observable<NICMSConfig> {
    return this.getData(`network-indicator`)
      .pipe(
        map((data: HttpResponse<NICMSConfig>) => data.body)
      );
  }

  /**
   * get segmented data from CMS
   * @returns {IInitialData}
   */
  protected getCmsCSPInitData(segmentMandate: boolean = true): Observable<IInitialData> {
    if (this.device.requestPlatform === 'mobile'
      && this.userService.username
      && this.segmentedCMSService.isInitialDataAvailable()
      && this.segmentEventManagerService.getSegmentDetails()
      && this.segmentEventManagerService.chkModuleForSegmentation(segmentMandate)
    ) {
      const data: Observable<IInitialData> = this.segmentedCMSService.getCmsInitData();
      data.subscribe((response: IInitialData) => {
        this.systemConfiguration = response.systemConfiguration;
        this.betpackValidInitialData(response);
        this.initialData = response;
      });
      return data;
    } else {
      return this.getCmsInitData();
    }
  }

  public getCmsInitData(): Observable<IInitialData> {
    if (this.initialData$) {
      return this.initialData$.asObservable();
    }

    this.initialData$ = new ReplaySubject<IInitialData>(1);
    if (this.cmsInitConfigPromise) {
      this.cmsInitConfigPromise.then((data: IInitialData) => {
        this.releaseSubject(data);
      });
    } else {
      const device = this.device.requestPlatform;

      this.getData(`initial-data/${device}`)
        .pipe(
          first(),
          map((response: HttpResponse<IInitialData>) => response.body)
        )
        .subscribe((data: IInitialData) => {
          this.releaseSubject(data);
        });
    }

    return this.initialData$.asObservable();
  }

  protected releaseSubject(data: IInitialData): void {
    this.systemConfiguration = data.systemConfiguration;
    this.betpackValidInitialData(data);
    this.initialData = data;

    this.initialData$.next(this.initialData);
    this.initialData$.complete();
  }
  betpackValidInitialData(data: IInitialData) {
    data.sportCategories?.forEach((sportCategory: ISportCategory, sportIndex: number) => {
      if (sportCategory.imageTitle === 'BetPack' && !this.systemConfiguration[sportCategory.imageTitle].enableBetPack) {
        data.sportCategories.splice(sportIndex, 1);
      }
    });
    data.footerMenu?.forEach((footerMenu: IFooterMenu, footerIndex: number) => {
      if((footerMenu.linkTitle && footerMenu.linkTitle === 'BetPack' && !this.systemConfiguration[footerMenu.linkTitle].enableBetPack)){
        data.footerMenu.splice(footerIndex, 1);
      }
    });
  }

  protected getData<T>(url: string, params: any = {}): Observable<HttpResponse<T>> {
    return this.http.get<T>(`${this.CMS_ENDPOINT}/${this.brand}/${url}`, {
      observe: 'response',
      params: params
    });
  }

  protected getSurfaceBetsData<T>(url, params: any = {}): Observable<HttpResponse<T>> {
    return this.http.get<T>(`${this.SURFACE_BETS_URL}/${this.brand}/${url}`, {
      observe: 'response',
      params: params
    });
  }

  protected getPromotions(categoryId?: string, withV2?: boolean): Observable<IPromotionsList> {
    const promoUrl = categoryId ? `promotions/${categoryId}` : 'promotions';

    return (!withV2 ? this.getData(promoUrl) : this.getV2Data(`promotions/${categoryId}`))
      .pipe(
        map((data: HttpResponse<IPromotionsList>) => {
          const promotionsListData = data.body;
          promotionsListData.promotions = this.cmsTools.processResult(promotionsListData.promotions);
          return promotionsListData;
        })
      );
  }

  /**
   * This method is used to get the fanzone data
   * @returns fanzone
   */
   getFanzone(): Observable<FanzoneDetails[]> {
    return this.getData('fanzone').pipe(map((fanzoneData: HttpResponse<FanzoneDetails[]>) => _.sortBy(fanzoneData.body, 'name')));
  }

  /**
   * This method is used to get fanzone clubs data
   * @returns special-pages
   */
  getFanzoneClubs(): Observable<FanzoneClub[]> {
    return this.getData('fanzone-club').pipe(
      map((clubData: HttpResponse<FanzoneClub[]>) => clubData.body.filter(club => club.active && this.isActiveRange(club.validityPeriodStart, club.validityPeriodEnd)))
    );
  }

  /**
   * This method is used to get the first-bet placement data
   * @returns first-bet placement
   */
   getFirstBetDetails<T>(): Observable<HttpResponse<T>> {
    return this.getData('first-bet-place');
  }

  /**
   * @returns Observable
   */
  private getArcData<T>(reason: string, risk: string): Observable<HttpResponse<T>> {
    return this.http.get<T>(`${this.CMS_ENDPOINT}/${this.brand}/arc-profile/${risk}/${reason}`, {
      observe: 'response'
    });
  }

  private getRGYCMSdata<T>(): Observable<HttpResponse<T>> {
    return this.http.get<T>(`${this.CMS_ENDPOINT}/${this.brand}/rgy-config`, {
      observe: 'response',
    });
  }

  private getV2Data<T>(url, params: any = {}): Observable<HttpResponse<T>> {
    return this.http.get<T>(`${this.CMS_ENDPOINT}/v2/${this.brand}/${url}`, {
      observe: 'response',
      params: params
    });
  }

  private getFeatureConfigByName(feature: string): Observable<ISystemConfig> {
    const reqData = this.getData(`system-configurations/${feature}`)
      .pipe(
        map((data: HttpResponse<ISystemConfig>) => data.body),
        shareReplay(1)
      );
    this.featureConfigMap.set(feature, reqData);
    return reqData;
  }

  private isGamingEnabled(): boolean {
    return !!(this.systemConfiguration && this.systemConfiguration.GamingEnabled
      && !this.systemConfiguration.GamingEnabled.enabledGamingOverlay);
  }

  /**
   * valida scheduling for EventHub tabs and remove which are in not time range.
   * @param ribbonData
   */
  private filterScheduleTabs(ribbonData: IFeaturedModule[]): IFeaturedModule[] {
    return _.filter(ribbonData, (ribbon: IFeaturedModule) => {
      if (ribbon.directiveName && ribbon.directiveName.toLowerCase() === 'eventhub') {
        return this.isActiveRange(ribbon.displayFrom, ribbon.displayTo);
      }
      if (ribbon.title === 'BetPack') {
        return this.systemConfiguration[ribbon.title].enableBetPack;
      }
      return true;
    });
  }

  /**
   * Schedule time should be in present time range
   * @param displayFrom
   * @param displayTo
   */
  private isActiveRange(displayFrom: string, displayTo: string): boolean {
    const dateNow = (new Date()).getTime(),
      startTime = (new Date(displayFrom)).getTime(),
      endTime = (new Date(displayTo)).getTime();

    return startTime < dateNow && endTime > dateNow;
  }
  
  fetchBetShareConfigDetails(): Observable<IBetShare> {
    if (this.betShareData) {
      return this.betShareData;
    }
    this.betShareData = this.getData(`bet-sharing`)
    .pipe(
      map((data: HttpResponse<IBetShare>) => data.body)
      , shareReplay(1)
    );
    return this.betShareData;
  }
  
  /**
   * @param  {string} betslipType
   * @returns Observable
   */
  getQuickStakes(betslipType: string): Observable<any> {
    const predefinedStakes = this.getSystemConfig()
      .pipe(
        map((config: ISystemConfig) => {
          const definedStakes = this.getStakes(config.PredefinedStakes, betslipType);
          return definedStakes && definedStakes.length >= 4 ? definedStakes : this.getStakes(config.PredefinedStakes);
        })
      );
    return predefinedStakes;
  }
  getStakes(value: Object, betslipType: string = global_stakes): [] {
    if(value[betslipType] && value[betslipType].length){
      return value[betslipType].split(',').slice(0, 4);
    }
  }
}
