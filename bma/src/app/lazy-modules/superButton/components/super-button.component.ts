import {
  Component,
  OnInit,
  OnChanges,
  Input,
  SimpleChanges,
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  OnDestroy
} from '@angular/core';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { INavigationPoint, ThemeArray } from '@core/services/cms/models/navigation-point.model';
import { NavigationService } from '@core/services/navigation/navigation.service';
import { DeviceService } from '@core/services/device/device.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { Subscription } from 'rxjs';
import { NavigationEnd, Router, Event } from '@angular/router';
import { RoutingState } from '@app/shared/services/routingState/routing-state.service';
import { FiltersService } from '@core/services/filters/filters.service';
import environment from '@environment/oxygenEnvConfig';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { LocaleService } from '@core/services/locale/locale.service';
import { CoralSportsSegmentProviderService } from '@lazy-modules/coralSportsSegmentProvider/service/coralsports-segment-provider.service';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';

@Component({
  selector: 'super-button',
  templateUrl: './super-button.component.html',
  styleUrls: ['./super-button.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class SuperButtonComponent implements OnInit, OnChanges, OnDestroy {
  @Input() type: string;
  @Input() homeTabUrl: string;
  @Input() competitionId: string;
  @Input() categoryId: number;

  public navPoint: INavigationPoint;
  public isShowNavPoint: boolean;
  public isAndroidExternalUrl: boolean;

  isBrandLadbrokes: boolean;
  themeArray: ThemeArray[] =  [];
  private ladbrokesCount: number = 4;
  private coralCount: number = 6;
  
  private data: INavigationPoint[];
  private title: string = 'super-button';
  private routeListener: Subscription;
  isCoral: boolean;

   isOTFAvailable;
  currentURL:string;
  constructor(
    private cmsService: CmsService,
    private gtmService: GtmService,
    private locale: LocaleService,
    private navigationService: NavigationService,
    private changeDetectorRef: ChangeDetectorRef,
    private deviceService: DeviceService,
    private pubSubService: PubSubService,
    private router: Router,
    private routingState: RoutingState,
    private coralSportsSegmentProviderService: CoralSportsSegmentProviderService,
    private filtersService: FiltersService,
    private bonusSuppressionService: BonusSuppressionService
  ) { }
  ngOnInit(): void {
    this.isCoral = environment && environment.brand === 'bma';
    this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
    this.onInit();
    this.pubSubService.subscribe(this.title, [this.pubSubService.API.SEGMENTED_INIT_FE_REFRESH,this.pubSubService.API.SESSION_LOGIN,this.pubSubService.API.SUCCESSFUL_LOGIN], () => {
      this.onInit();
    });

    this.coralSportsSegmentProviderService.isOTFAvailable.subscribe((isOTFAvailable) => {
      if(isOTFAvailable){
        this.onInit();
      }    })

    this.routeListener = this.router.events.subscribe((event: Event) => {
      if (event instanceof NavigationEnd) {
        this.currentURL = this.routingState.getCurrentUrl();
        const [baseURL] = this.currentURL.split('?');
        if (baseURL === '/' || baseURL.includes('/home')  || baseURL === ''|| baseURL.includes('/big-competition')) {
          this.onInit();
        }
      }
    });

  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.homeTabUrl && changes.homeTabUrl.currentValue) {
      this.showNavPoint();
    }
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.title);
  }
  /**
   * gets CMS config data on page load
   */
  onInit(): void {
    this.cmsService.getNavigationPoints([this.currentURL||this.homeTabUrl,this.competitionId,this.categoryId],this.type).subscribe((item: INavigationPoint[]) => {
      this.data = item.filter(point => {return this.bonusSuppressionService.checkIfYellowFlagDisabled(point.title)});
      this.showNavPoint();
    });
  }


  showNavPoint(): void {
    this.navPoint = this.pickNavigationPointFn()();
    this.themeArray = [];
    const themesCount:number = this.isBrandLadbrokes? this.ladbrokesCount : this.coralCount;
    const brandTheme= this.isBrandLadbrokes?  '' : 'coral-';
    const isCenterAlignment = this.navPoint && this.navPoint.ctaAlignment && this.navPoint.ctaAlignment === 'center';
    for (let i = 1; i <= themesCount; i++) {
      this.themeArray.push({ 
        caseVal: `theme_${i}`, 
        classVal: isCenterAlignment ? `nav-point-${brandTheme}theme${i}` : `row right-theme${i}-${brandTheme}top` , 
        descVal: isCenterAlignment ? `button btn-secondary-theme${i}` : `right-theme${i}-${brandTheme}btn`
      })
    }
    this.isShowNavPoint = !!this.navPoint;
    if (this.isShowNavPoint) {
      const isAndroidWrapper = this.deviceService.isAndroid && this.deviceService.isWrapper;

      // Due to issues with window.open, for android wrappers and for external links we will use A link with target blank
      this.isAndroidExternalUrl = isAndroidWrapper && !this.navigationService.isInternalUri(this.navPoint.targetUri);
    }

    this.changeDetectorRef.markForCheck();
  }

  goToUrl(): void {
    this.gtaTracking();
    if(this.navPoint.targetUri.includes('racingsuperseries')){
      this.filtersService.filterLinkforRSS(this.navPoint.targetUri).subscribe(data =>{
        this.navPoint.targetUri = data;
      })
     }   
    this.navigationService.openUrl(this.navPoint.targetUri, true);   
  }
   
  gtaTracking(){
    const position = this.routingState.getCurrentUrl();
    const location = (this.type === 'bigCompetition' ? 'BCH' : this.type);
    this.gtmService.push('Event.Tracking', {
      'component.CategoryEvent': 'sports banner',
      'component.LabelEvent': 'super button',
      'component.ActionEvent': 'click',
      'component.PositionEvent': position,
      'component.LocationEvent': location,  
      'component.EventDetails': this.navPoint.title,
      'component.URLClicked': this.navPoint.targetUri
    });
   }
  /*
   * Return function for component type attribute
   * @return {Function}
   * @private
   */
  private pickNavigationPointFn(): Function {
    return {
      bigCompetition: this.getCompetitionNavigationPoint.bind(this),
      homeTabs: this.getHomeTabsNavigationPoint.bind(this),
      sport: this.getSportNavigationPoint.bind(this)
    }[this.type];
  }

  /*
   * Find navigation point by url id for home tabs
   * @return {Object}
   * @private
   */
  private getHomeTabsNavigationPoint(): INavigationPoint {
    return this.data.find((point: INavigationPoint) => point.homeTabs.includes(this.homeTabUrl));
  }

  /*
   * Find navigation point by competition id for big competitions
   * @return {Object}
   * @private
   */
  private getCompetitionNavigationPoint(): INavigationPoint {
    return this.data.find((point: INavigationPoint) => point.competitionId.includes(this.competitionId));
  }

  /*
   * Find navigation point by category id for sport
   * @return {Object}
   * @private
   */
  private getSportNavigationPoint(): INavigationPoint {
    return this.data.find((point: INavigationPoint) => point.categoryId.includes(+this.categoryId));
  }
}
