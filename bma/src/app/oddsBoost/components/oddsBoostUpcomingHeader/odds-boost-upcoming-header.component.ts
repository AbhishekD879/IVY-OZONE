import { formatDate } from '@angular/common';
import { ChangeDetectorRef, Component, EventEmitter, Input, OnChanges, OnDestroy, Output, SimpleChanges } from '@angular/core';
import { IFreebetExpiredTokenIds } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';

@Component({
  selector: 'odds-boost-upcoming-header',
  templateUrl: './odds-boost-upcoming-header.component.html',
  styleUrls: ['./odds-boost-upcoming-header.component.scss']
})
export class OddsBoostUpcomingHeaderComponent implements OnChanges, OnDestroy {
  @Input() countDownDate: Date;
  @Input() isLads:boolean;
  @Input() tab:boolean;
  @Input() list:boolean;
  @Input() sport:string;
  @Input() timerStart:string;
  @Input() sameTimeExpiry:number;
  @Input() freebetTokenId:string;
  @Input() type:string;

  countDown: string;
  currentDifference: string;
  timer:boolean = true;
  timerValue:number;
  headerTimeText:string;
  listTimeText:string;
  isDisplayedHeaderText: boolean = false;
  isDisplayedListText: string|boolean;
  isDisplayedHeaderTextAvailable: boolean;
  isDisplayedHeaderTextUpcoming: boolean;
  message: number;
  @Output() readonly expiredTokenIds: EventEmitter<IFreebetExpiredTokenIds> = new EventEmitter();


  constructor(private changeDetectorRef: ChangeDetectorRef,
              private windowRef: WindowRefService
    ) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.countDownDate && changes.countDownDate.currentValue) {
      this.clearTimer();
      this.initCountdown(changes.countDownDate.currentValue);
      this.nextCountDown(changes.countDownDate.currentValue);
      this.expireOrAvailable();
    }


    if(changes.type?.currentValue){
      this.windowRef.nativeWindow.clearTimeout(this.message);
      this.expireOrAvailableSameTimeExpiry();
      this.availableSameTime();
    }

  }

  ngOnDestroy(): void {
    this.windowRef.nativeWindow.clearTimeout(this.message);
    this.windowRef.nativeWindow.clearInterval(this.timerValue);
  }

  private initCountdown(date: Date): void {

    const countDownDate = date.getTime();
    const second = 1000;
    const minute = 1000 * 60;
    const hour = 1000 * 60 * 60;
      
      const now = new Date().getTime();
      const difference = countDownDate - now;
      this.checkTokenDate(now,countDownDate);
      if (difference > 0) {
        const hours = this.padNumber(Math.floor((difference % (hour * 24)) / hour));
        const minutes = this.padNumber(Math.floor((difference % hour) / minute));
        const seconds = this.padNumber(Math.floor((difference % minute) / second));
        this.currentDifference = `${hours}:${minutes}:${seconds}`;
        if (this.isLads) {
          const nowDate = formatDate(new Date(), 'dd/MM/yyyy', 'en-US');
          const countDownDateExpiry = formatDate(date, 'dd/MM/yyyy', 'en-US');
          if ((this.currentDifference < this.timerStart && countDownDateExpiry == nowDate) || !this.list) {
            this.countDown = `${hours}:${minutes}:${seconds}`;
            this.timer = true;
          } else {
            this.timer = false;
          }
        } else {
          this.countDown = `${hours}:${minutes}:${seconds}`;
        }
      } 
      else {
        this.clearTimer();
        this.countDown = '00:00:00';
      }
  }

  /* set time interval **/
  public nextCountDown(date:Date): void{
    this.timerValue = this.windowRef.nativeWindow.setInterval(() => {
    this.initCountdown(date);
    this.changeDetectorRef.detectChanges();
    },1000);
  }

  /* check expiry token **/
  public checkTokenDate(now,countDownDate){
    if(now >= countDownDate){
      const tokenDetails = {freebetTokenId : this.freebetTokenId,
        tokenExpire : true}
        this.expiredTokenIds.emit(tokenDetails)
      }
  }
  /* clear time interval **/
  public clearTimer(){
    clearInterval(this.timerValue);
  }

  public padNumber(number: number): string {
    return number < 10 ? `0${number}` : `${number}`;
  }
  
  /* expire or available list token message **/
  public expireOrAvailable() {
    this.isDisplayedListText = this.isLads && this.list && this.tab && this.timer;
  }

  /* expire or available header message **/
  public expireOrAvailableSameTimeExpiry() {
      if (this.type == 'Available') {
        this.isDisplayedHeaderTextAvailable = this.isLads && this.tab && !this.list && this.timer && this.type == 'Available';
      }
      if (this.type == 'Upcoming') {
        this.isDisplayedHeaderTextUpcoming = this.isLads && !this.tab && !this.list && this.timer && this.type == 'Upcoming';
      }
  }

  /* display available or upcoming message in header **/
  public availableSameTime(){
      if (this.sameTimeExpiry && this.isDisplayedHeaderTextAvailable) {
        this.headerTimeText = `${this.sameTimeExpiry} of your Odds Boosts will expire in`
      } else if(this.sameTimeExpiry && this.isDisplayedHeaderTextUpcoming){
        this.headerTimeText =`Your next ${this.sameTimeExpiry} Odds Boosts are available in`
      }else if((this.sport != 'MultiSport') && this.isDisplayedHeaderTextAvailable){
        this.headerTimeText =`One of your ${this.sport} Odds Boost will expire in`
      }else if((this.sport != 'MultiSport') && this.isDisplayedHeaderTextUpcoming){
        this.headerTimeText = `Your next ${this.sport} Odds Boost is available in`
      }else if(!this.sameTimeExpiry && this.sport == 'MultiSport' && this.isDisplayedHeaderTextAvailable){
        this.headerTimeText = `One of your Odds Boosts will expire in`
      }else if(!this.sameTimeExpiry && this.sport == 'MultiSport' && this.isDisplayedHeaderTextUpcoming){
        this.headerTimeText =`Your next Odds Boosts are available in`
      }
    if(this.headerTimeText){
    this.delayDisplay();
    }
  }

  delayDisplay(): void {
    this.message = this.windowRef.nativeWindow.setTimeout(() => {
      this.isDisplayedHeaderText = true;
      this.changeDetectorRef.detectChanges();
    }, 500);
  }
  
  /* return true for lads **/
  public headerText(){
    return this.isLads && this.headerTimeText;
  }
}
