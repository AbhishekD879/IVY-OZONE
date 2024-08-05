import { filter, finalize, tap } from 'rxjs/operators';
import { Component, ChangeDetectorRef, OnInit, OnDestroy } from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { MainLottoService } from '../../services/mainLotto/main-lotto.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { UserService } from '@core/services/user/user.service';
import { ILottonMenuItem, ILotteryMap, ILottoCms } from '../../models/lotto.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { LAZY_LOAD_ROUTE_PATHS } from '@bma/constants/lazyload-route-paths.constant';
import environment from '@environment/oxygenEnvConfig';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { LocaleService } from '@core/services/locale/locale.service';
@Component({
    selector: 'lotto-main',
    templateUrl: './lotto-main.component.html'
})
export class LottoMainComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  lottoData: ILotteryMap;
  svg: string;
  svgId: string;
  menuItems: ILottonMenuItem[];
  lottoMessage: { msg: string, type: string } = { msg: '', type: '' };
  currencySymbol: string;
  sessionStatus: boolean;
  currency: string;
  oddsFormat: number;
  userBalance: string | number;
  activeUrl: string;
  lottoPath: string;
  lottoMain=LAZY_LOAD_ROUTE_PATHS.home
  isLinesummaryPage: boolean;
  isLottoPage: boolean;
  lottoCmsBanner: ILottoCms;
  isBrandLadbrokes: boolean;

  constructor(
    private lottoService: MainLottoService,
    private user: UserService,
    private cmsService: CmsService,
    private changeDetector: ChangeDetectorRef,
    private pubSubService: PubSubService,
    private router: Router,
    private locale: LocaleService,
  ) {
    super()/* istanbul ignore next */;
    this._initChanges();
  }

  ngOnInit(): void {
    this.cmsService.getLottoBanner().subscribe((lottoBanner: ILottoCms) => {
      this.lottoCmsBanner = lottoBanner;
      this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
      this.lottoService.setLottoCmsBanner(lottoBanner);
      this.lottoService.getLotteriesByLotto().pipe(
      finalize(() => {
        this.hideSpinner();
      }))
      .subscribe((data: ILotteryMap) => {
        this.lottoData = data;
        this.init();
      }, () => {
        this.showError();
      });
    this.lottoPath = LAZY_LOAD_ROUTE_PATHS.lotto;  
  });
  }
  ngOnDestroy(): void {
    this.pubSubService.unsubscribe('lottoMainCtrl');
  }

  private _initChanges() {
    this.router.events
    .pipe(
      filter( event => event instanceof NavigationEnd),
      tap((event: any) => {
        const url = event.url.split('?');
           if(url.length > 0) {
          this.isLinesummaryPage = url[0].includes('linesummary');
          this.isLottoPage =  url[0].endsWith('lotto');
         }
       })
    ).subscribe()
  }

  private init(): void {
    this.cmsService.getItemSvg('Lotto')
      .subscribe((icon) => {
        this.svg = icon.svg;
        this.svgId = icon.svgId;
      });

    this.getSession();
    this.pubSubService.subscribe('lottoMainCtrl', this.pubSubService.API.USER_BALANCE_UPD, () => {
      this.getSession();
    });
    
    this.menuItems = this.lottoService.getMenuItems(this.lottoService.cmsLotto());
    this.pubSubService.subscribe('lottoMainCtrl', this.pubSubService.API.MSG_UPDATE, (data: { msg: string, type: string }) => {
      this.lottoMessage = data;
      this.changeDetector.detectChanges();
    });
    this.pubSubService.subscribe('lottoMainCtrl', this.pubSubService.API.MENU_UPDATE, (activeUrl: string) => {
      this.activeUrl = activeUrl;
      this.changeDetector.detectChanges();
    });
  }

  private getSession(): void {
    this.currencySymbol = this.user.currencySymbol;
    this.sessionStatus = this.user.status;
    this.currency = this.user.currency;
    this.oddsFormat = this.user.oddsFormat;
    this.userBalance = this.user.sportBalance;
  }
}
