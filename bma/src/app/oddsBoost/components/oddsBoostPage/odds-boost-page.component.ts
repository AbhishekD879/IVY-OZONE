import { ChangeDetectorRef, Component, OnDestroy, OnInit } from '@angular/core';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { UserService } from '@core/services/user/user.service';
import { OddsBoostService } from '@oddsBoostModule/services/odds-boost.service';
import { IFreebetExpiredTokenIds, IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { IOddsBoostConfig } from '@core/services/cms/models';
import * as _ from 'underscore';
import { AbstractOutletComponent } from '@shared/components/abstractOutlet/abstract-outlet.component';
import { delay } from 'rxjs/operators';
import { Subscription, of, timer } from 'rxjs';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { ICompetitionFilter } from '@app/lazy-modules/competitionFilters/models/competition-filter';
import { formatDate } from '@angular/common';
import { TimeService } from '@core/services/time/time.service';

@Component({
  selector: 'odds-boost-page',
  templateUrl: './odds-boost-page.component.html',
  styleUrls: ['./odds-boost-page.component.scss']
})
export class OddsBoostPageComponent extends AbstractOutletComponent implements OnInit, OnDestroy {
  isLoggedIn: boolean;
  availableBoosts: IFreebetToken[] = [];
  upcomingBoosts: IFreebetToken[] = [];
  config: IOddsBoostConfig;
  pageTitle: string;
  loggedInHeaderText: SafeHtml;
  loggedOutHeaderText: SafeHtml;
  termsAndConditionsText: SafeHtml;
  noTokensText:SafeHtml;
  timerStart:string;
  nextBoostDate: Date;
  nextUpcomingBoostDate: Date;
  nextAvailableBoostDate: Date;
  oddsBoostsUpcomingToken:IFreebetToken;
  oddsBoostsAvailableToken:IFreebetToken;
  nextSport:string;
  isActive:boolean = true;
  isExpanded:boolean = true;
  enabled:boolean = true;
  canAnimate:boolean = true;
  noTokens:boolean = true;
  sameExpiry:number;
  startingAvailbleTokenNumber:number = 0;
  startingUpcomingTokenNumber:number = 0;
  availableCountDown: Subscription;
  upcomingCountDown: Subscription;
  tick = 300;
  oddsBoostToken:IFreebetToken;
  dateExpiryCountMap : Map<string, number> =  new Map<string, number>();
  sortedTokensData: IFreebetToken[] = [];
  sortedTokensArr: IFreebetToken[] = [];
  sportPills:ICompetitionFilter[] = [];
  isDefaultPillOnLoad:boolean = false;
  oddBoostAnimation: Subscription;

  public readonly title = 'oddsBoost';
  public oddsBoostSubscription: Subscription;
  expireTokenDetails: {[key: string]: boolean} = {};
  timerMessage: boolean = false;
  currentDifference: string;
  validDateToShow:boolean = false;

  constructor(
    public pubSubService: PubSubService,
    public userService: UserService,
    public oddsBoostService: OddsBoostService,
    public cmsService: CmsService,
    public locale: LocaleService,
    public domSanitizer: DomSanitizer,
    public windowRefService: WindowRefService,
    public changeDetector: ChangeDetectorRef,
    public gtmService: GtmService,
    public timeService: TimeService
  ) {
    super()/* istanbul ignore next */;
    this.isLoggedIn = userService.status;
    this.pubSubService.subscribe(
        this.title,
        [this.pubSubService.API.SUCCESSFUL_LOGIN, this.pubSubService.API.SESSION_LOGOUT],
        this.sessionStatusChange.bind(this)
    );
    this.pubSubService.subscribe(this.title, 'STORE_FREEBETS', this.getOddsBoosts.bind(this));
    this.pageTitle = this.locale.getString('oddsboost.page.title');
  }

  ngOnInit(): void {
    this.showSpinner();
    this.getContent();
    if (this.isLoggedIn) {
      this.getOddsBoosts();
    } else {
      this.hideSpinner();
    }
    this.disabledBoostIcon();
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.title);
    this.unsubscribeOddsBoost();
    this.availableCountDown && this.availableCountDown.unsubscribe();
    this.upcomingCountDown && this.upcomingCountDown.unsubscribe();
    this.oddBoostAnimation && this.oddBoostAnimation.unsubscribe();
  }

  openLoginDialog(): void {
    this.pubSubService.publish(this.pubSubService.API.OPEN_LOGIN_DIALOG, { moduleName: 'oddsboost' });
  }

  public unsubscribeOddsBoost(): void {
    this.oddsBoostSubscription && this.oddsBoostSubscription.unsubscribe();
  }

  public getContent(): void {
    this.cmsService.getOddsBoost().subscribe((config: IOddsBoostConfig) => {
      this.config = config;
      this.loggedInHeaderText = this.domSanitizer.bypassSecurityTrustHtml(this.config.loggedInHeaderText);
      this.loggedOutHeaderText = this.domSanitizer.bypassSecurityTrustHtml(this.config.loggedOutHeaderText);
      this.termsAndConditionsText = this.domSanitizer.bypassSecurityTrustHtml(this.config.termsAndConditionsText);
      this.noTokensText = this.domSanitizer.bypassSecurityTrustHtml(this.config.noTokensText);
      this.timerStart = this.config.countDownTimer;
    }, () => this.showError());
  }

  public sessionStatusChange(): void {
    this.isLoggedIn = this.userService.status;
    if (this.isLoggedIn) {
      this.disabledBoostIcon();
      this.getOddsBoosts();
    }
  }

  public getOddsBoosts(): void {
    this.unsubscribeOddsBoost();
    this.oddsBoostSubscription = this.oddsBoostService.getOddsBoostTokens().subscribe((data: IFreebetToken[]) => {
      const diffTimeInHrs = this.timeService.findDifferenceBetweenUTCAndBST();
      const timezone = this.resolvedTimeZone();
      const nowDate = new Date();
      const allOddsBoosts = _.partition(data, (oddBoost: IFreebetToken) => {
      const timeZonesGibIncluded = "Europe/Gibraltar,Europe/Vienna,Europe/Berlin";
      if((diffTimeInHrs || !diffTimeInHrs) && timeZonesGibIncluded.includes(timezone)){
        const expAddtime = new Date(new Date(oddBoost.freebetTokenExpiryDate).getTime()+this.timeService.refreshInterval);
        const startAddTime = new Date(new Date(oddBoost.freebetTokenStartDate).getTime()+this.timeService.refreshInterval);
        oddBoost.freebetTokenExpiryDate = this.formatDate(this.timeService.dateToString(expAddtime));
        oddBoost.freebetTokenStartDate = this.formatDate(this.timeService.dateToString(startAddTime));
      }else {
        oddBoost.freebetTokenExpiryDate = this.formatDate(oddBoost.freebetTokenExpiryDate);
        oddBoost.freebetTokenStartDate = this.formatDate(oddBoost.freebetTokenStartDate);
      }
        return nowDate > new Date(oddBoost.freebetTokenStartDate);
      });
      this.availableBoosts = allOddsBoosts[0];
      this.upcomingBoosts = allOddsBoosts[1];
      this.oddsBoostTokens();
      this.availableTokens(this.availableBoosts.length);
      this.upcomingTokens(this.upcomingBoosts.length);
      this.hideSpinner();
      this.setUpcomingBoostTimer();
      this.sendGTMData('load');
    }, () => this.showError());
  }

  resolvedTimeZone() {
    return Intl.DateTimeFormat().resolvedOptions().timeZone
  }

  private setUpcomingBoostTimer(): void {
    if (this.upcomingBoosts.length) {
      this.nextBoostDate = new Date(this.getNextUpcomingBoost(this.upcomingBoosts).freebetTokenStartDate);
    }
  }

  private getNextUpcomingBoost(oddsBoosts: IFreebetToken[]): IFreebetToken {
    let nextBoost = oddsBoosts[0];

    _.each(oddsBoosts, (oddsBoost: IFreebetToken) => {
      const oddsBoostStartDate = new Date(oddsBoost.freebetTokenStartDate);
      const nextBoostStartDate = new Date(nextBoost.freebetTokenStartDate);

      nextBoost = oddsBoostStartDate < nextBoostStartDate ? oddsBoost : nextBoost;
    });
    return nextBoost;
  }

  /* emit least token based on time **/
  public leastTimeToken(event:string){
    if(this.isActive){
      this.nextAvailableBoostDate = new Date(event);
    }else{
      this.nextUpcomingBoostDate = new Date(event);
    }
  }


  public formatDate(date: string): string {
    return date.replace(/-/g, '/');
  }

  /* oddsBoost icon animation **/
  public disabledBoostIcon(): void{
    if(this.enabled || this.isLoggedIn){
    this.enabled = true;
    this.oddBoostAnimation = of(true).pipe(delay(3000)).subscribe(()=>{
        this.enabled=false;
    });
   } 
  }
  
  /* number animation based on upcoming length **/
  public availableTokens(endingTokenNumber:number): void{
    if(endingTokenNumber && endingTokenNumber > 0){
    this.availableCountDown = timer(0, this.tick).subscribe((count) => {
      if (this.startingAvailbleTokenNumber == endingTokenNumber && count) {
        if (this.availableCountDown) {
          this.availableCountDown.unsubscribe();
        }
      } else {
        this.startingAvailbleTokenNumber++;
        this.changeDetector.detectChanges();
      }
    });
   }
  }

  /* number animation based on upcoming length **/
  public upcomingTokens(endingTokenNumber:number): void{
    if(endingTokenNumber && endingTokenNumber > 0){
    this.upcomingCountDown = timer(0, this.tick).subscribe((count) => {
      if (this.startingUpcomingTokenNumber == endingTokenNumber && count) {
        if (this.upcomingCountDown) {
          this.upcomingCountDown.unsubscribe();
        }
      } else {
        this.startingUpcomingTokenNumber++;
      }
    });
  }
  }

  /* set tab based on data **/
  public oddsBoostTokens(): void {
    if (this.availableBoosts.length > 0 && this.upcomingBoosts.length <= 0) {
      this.isActive = true;
    } else if (this.availableBoosts.length <= 0 && this.upcomingBoosts.length > 0) {
      this.isActive = false;
    } else if (this.availableBoosts.length <= 0 && this.upcomingBoosts.length <= 0) {
      this.noTokens = false;
    }
  }

  /* emited data from odds-boost-list **/
  public filterOddsboostTokens(tokensData: {[categoryId: string]: IFreebetToken[]}): void {
    this.loadSvg(tokensData);
    const reqTokensData = Object.values(tokensData).flat();
    this.sortOddsboostTokensInSpecificOrder(reqTokensData)
  }

  /* sorting the oddsboost tokens in specific order **/
  public sortOddsboostTokensInSpecificOrder(reqTokensData:IFreebetToken[]): void {
    const categoryOrder = ['All', 'Football', 'Horse Racing', 'A-Z'];
    const customSort = (a, b) => {
      const AcategoryName = a.categoryName ? a.categoryName : 'All';
      const BcategoryName = b.categoryName ? b.categoryName : 'All';
      const indexA = categoryOrder.indexOf(AcategoryName);
      const indexB = categoryOrder.indexOf(BcategoryName);
      if (indexA !== -1 && indexB !== -1) {
        return indexA - indexB;
      } else if (indexA !== -1) {
        return -1;
      } else if (indexB !== -1) {
        return 1;
      } else {
        return a.categoryName.localeCompare(b.categoryName);
      }
    };
    const sortedTokensData = [...reqTokensData].sort(customSort);
    this.sortedTokensArr = sortedTokensData;
    this.filterSportPillsFromOddsboostTokens(sortedTokensData);
  }

  /* filter the sport pills from available/upcoming oddsboost tokens **/
  public filterSportPillsFromOddsboostTokens(sortedTokensData:IFreebetToken[]): void {
    this.sportPills = [];
    const sportPillsObj = [];
    const defaultPillValue = {
      value: 1,
      name: 'All',
      id: '',
      type: 'sport',
      active: true,
    };
    sortedTokensData.forEach((sport:IFreebetToken) => {
      if (sport.categoryId !== undefined) {
        const pillsObj: ICompetitionFilter = {
          value: +sport.categoryId,
          name: sport.categoryName,
          id: sport.categoryId,
          type: 'sport',
          active: false,
        }
        sportPillsObj.push(pillsObj);
      }
    })
    if (!sportPillsObj.find(pill => pill.name === 'All')) {
      sportPillsObj.unshift(defaultPillValue);
    }
    const uniqueData = sportPillsObj.filter((sportPillItem, index, allSportPills) => {
      return (
        index ===
        allSportPills.findIndex(
          (i) => i.name === sportPillItem.name
        )
      );
    });
    this.sportPills = uniqueData;
    this.onSelectonOfSportPill(defaultPillValue);
  }

  /* When click on sport pill, Load the tokens corrresponding to that sport  **/
  public onSelectonOfSportPill(event: ICompetitionFilter): void {
    event.active = true;
    this.sportPills = this.sportPills.map((filter: ICompetitionFilter) => {
      if (filter.type === event.type && filter.id !== event.id) {
        filter.active = false;
      }
      return { ...filter };
    });
    const selectedPill = event;
    const selectedPillCategoryId = selectedPill.id;
    const pillName = selectedPill.name;
    if (pillName !== 'All') {
      const filteredTokensData = this.sortedTokensArr.filter(oddsboostToken => oddsboostToken.categoryId == selectedPillCategoryId || !oddsboostToken.categoryId);
      this.filterOddsboostTokensForSport(filteredTokensData);
    } else {
      this.filterOddsboostTokensForSport(this.sortedTokensArr);
    }
    if (this.isDefaultPillOnLoad) {
      this.sendGTMData(pillName);
    }
    this.isDefaultPillOnLoad = true;
  }

  /* forming the oddsboost tokens into array with specific format **/
  public filterOddsboostTokensForSport(value:IFreebetToken[]): void {
    const result = [];
    let currentCategory = null;
    let categoryItems = [];
    for (const key of value) {
      const { categoryId } = key;
      if (categoryId !== currentCategory) {
        if (categoryItems.length > 0) {
          result.push(categoryItems);
        }
        currentCategory = categoryId;
        categoryItems = [];
      }
      categoryItems.push(key);
    }
    if (categoryItems.length > 0) {
      result.push(categoryItems);
    }
    this.sortedTokensData = [...result];
  }

  /* assign sport related svgId **/
  public loadSvg(data: {[categoryId: string]: IFreebetToken[]}): {[categoryId: string]: IFreebetToken[]} {
    this.oddsBoostToken = null as IFreebetToken;
    this.dateExpiryCountMap = new Map<string, number>();
    const tokensData = data;
    for (const key in tokensData) {
      const sportTokens = tokensData[key];
      sportTokens.forEach((sportToken:IFreebetToken) => {
        this.cmsService.getSportCategoryById(key).subscribe(sportCategory => {
          sportToken.svgId = sportCategory?.svgId ? sportCategory.svgId : 'odds-boost-icon-lads';
          this.findTimer(sportToken);
          this.checkTokenDate(sportToken);
          this.validDate(sportToken);
        });
      });
    }
    this.tokenCount();
    return tokensData;
  }

  public validDate(oddBoost) {
    const date = this.isActive ? 'freebetTokenExpiryDate' : 'freebetTokenStartDate';
    const countDownDate = new Date(oddBoost[date]).getTime();
    const second = 1000;
    const minute = 1000 * 60;
    const hour = 1000 * 60 * 60;
    const now = new Date().getTime();
    const difference = countDownDate - now;
    const hours = this.padNumber(Math.floor((difference % (hour * 24)) / hour));
    const minutes = this.padNumber(Math.floor((difference % hour) / minute));
    const seconds = this.padNumber(Math.floor((difference % minute) / second));
    this.currentDifference = `${hours}:${minutes}:${seconds}`;
    const nowDate = formatDate(new Date(), 'dd/MM/yyyy', 'en-US');
    const countDownDateExpiry = formatDate(countDownDate, 'dd/MM/yyyy', 'en-US');
    if (this.currentDifference < this.timerStart && countDownDateExpiry == nowDate) {
       this.validDateToShow = true;
    }
  }

  public padNumber(number: number): string {
    return number < 10 ? `0${number}` : `${number}`;
  }

  /* filter same expired tokens **/
  public findTimer(oddsBoosts:IFreebetToken): void {
    const date = this.isActive ? 'freebetTokenExpiryDate' : 'freebetTokenStartDate';
    if (!this.oddsBoostToken) {
      this.oddsBoostToken = oddsBoosts;
    }
    const oddsBoostStartDate = new Date(oddsBoosts[date]);
    const nextBoostStartDate = new Date(this.oddsBoostToken[date]);
    const count = this.dateExpiryCountMap.get(oddsBoosts[date]);
    if (!!count) {
      this.dateExpiryCountMap.set(oddsBoosts[date], count + 1);
    } else {
      this.dateExpiryCountMap.set(oddsBoosts[date], 1);
    }
    this.oddsBoostToken = oddsBoostStartDate < nextBoostStartDate ? oddsBoosts : this.oddsBoostToken;
  }

  /* get same expiry or sport related tokens based on tab **/
  public tokenCount(): void {
    this.sameExpiry = 0;
    this.nextSport = "";
    this.timerMessage = true;
    const expiryTokens = this.dateExpiryCountMap.get(this.oddsBoostToken['freebetTokenExpiryDate']) ||
      this.dateExpiryCountMap.get(this.oddsBoostToken['freebetTokenStartDate']);
    if (expiryTokens > 1) {
      this.sameExpiry = expiryTokens;
    } else {
      this.nextSport = this.oddsBoostToken.categoryName || 'MultiSport';
    }
  }

  /* check expiry token **/
  public checkTokenDate(oddBoost:IFreebetToken){
    const date = this.isActive ? 'freebetTokenExpiryDate' : 'freebetTokenStartDate';
    const countDownDate = new Date(oddBoost[date]).getTime(); 
    const now = new Date().getTime();
    if(now >= countDownDate){
      const tokenDetails = {freebetTokenId : oddBoost.freebetTokenId,
        tokenExpire : true}
      this.expireTokenInfo(tokenDetails);
    }
  }
 
  /* total expiry tokens info **/
  expireTokenInfo(event:IFreebetExpiredTokenIds): void {
    const tokenExpire = event.freebetTokenId;
    this.expireTokenDetails[tokenExpire] = event.tokenExpire;
  }

  /* Send GA Tracking data **/
  public sendGTMData(value:string): void {
    const gtmData = {
      event: value == 'load' ? 'contentView' : 'Event.Tracking',
      'component.CategoryEvent': 'odds boost',
      'component.LabelEvent': 'oddset',
      'component.ActionEvent': value == 'load' ? 'load' : 'click',
      'component.PositionEvent': (value == 'available' || value == 'upcoming') ? (value == 'available' ? 'upcoming' : 'available') : (this.isActive ? 'available' : 'upcoming'),
      'component.LocationEvent': value == 'load' ? `upcoming-${this.upcomingBoosts.length}`: 'not applicable',
      'component.EventDetails': value == 'load' ? `available-${this.availableBoosts.length}` : value,
      'component.URLClicked': 'not applicable'
    }
    this.gtmService.push(gtmData.event, gtmData);
  }
}
