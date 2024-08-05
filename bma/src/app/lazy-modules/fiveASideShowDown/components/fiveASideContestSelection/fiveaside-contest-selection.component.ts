import { ChangeDetectionStrategy, ChangeDetectorRef, Component, EventEmitter, Input, OnDestroy, OnInit, Output, SecurityContext
} from '@angular/core';
import { CarouselService } from '@app/shared/directives/ng-carousel/carousel.service';
import { Carousel } from '@app/shared/directives/ng-carousel/carousel.class';
import { CmsService } from '@app/core/services/cms/cms.service';
import { IStaticBlock } from '@app/core/services/cms/models/static-block.model';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { CONTEST_SELECTION as CS, ENTRY_CONFIRMATION } from '@app/fiveASideShowDown/constants/constants';
import { IAvailableContests } from '@app/fiveASideShowDown/models/available-contests.model';
import { Subscription } from 'rxjs';


@Component({
  selector: 'fiveaside-contest-selection.component',
  template: '',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FiveASideContestSelectionComponent implements OnInit, OnDestroy  {
  public canShowPrevious: boolean=false;
  public canShowNext: boolean=false;
  @Input() contests: IAvailableContests[];
  @Input() selectedContest: string;
  @Output() readonly selectedContestChange = new EventEmitter();

  public staticBlockContent: SafeHtml;
  public slideUpClass: string = '';
  public allContestConsts = CS;

  private readonly CAROUSAL_ID: string = CS.CAROUSAL_ID;
  private readonly STATIC_BLOCK_URL: string = CS.STATIC_BLOCK_URL;

  private staticBlockSubscription: Subscription;

  constructor(private carouselService: CarouselService,
    private cmsService:  CmsService,
    private domSanitizer: DomSanitizer,
    private changeDetectorRef: ChangeDetectorRef) { }

  ngOnInit(): void {
    this.initContestSelectionCarousel();
  }

  /**
   * returns { void }
   */
  ngOnDestroy(): void {
    this.staticBlockSubscription.unsubscribe();
  }

  /**
   * returns {void} used to initialise the carousel
   */
  initContestSelectionCarousel(): void {
    this.requestContestAndCarouselInit();
    this.getContestBetSlipToolTip();
    this.triggerSlideUp();
  }

   /*
   * @returns {void}
   */
  public requestContestAndCarouselInit(): void {
    this.canShowPrevious =false;
    this.canShowNext=true;
    if(this.selectedContest && this.contests?.length > 0) {
      const oldIndex = this.contests.findIndex(item => (item.contestId === this.selectedContest));
      this.contests.splice(0, 0, this.contests.splice(oldIndex,1)[0]);
    }
    this.selectedContest = this.selectedContest ? this.selectedContest.toString().trim() : 
                                                  (this.contests && this.contests.length > 0 ? this.contests[0].contestId : '');
    this.emitSelctedContest();
  }

  /*
  * Setting the active contest based on the user selection
  * @param {number} index - Selected contest index
  * @param {boolean} activeState - Contest selection status
  */
   public setActiveContest(id: string = '') {
      this.selectedContest = this.selectedContest === id ? '' : id;
      this.emitSelctedContest();
   }

   /*
   * Emits the contest ID everytime the selection changes
   * @returns {void}
   */
   public emitSelctedContest(): void {
      this.selectedContestChange.emit( this.selectedContest ? {id: this.selectedContest, name: this.findContestName()} :'');
   }

   /**
    * Returns the selected contest name by filtering the available contests using ID
    * @return { string } contest name
    */
   public findContestName(): string {
    const [ fileteredContest ] = this.contests.filter(contest => (contest.contestId === this.selectedContest));
    return fileteredContest.contestName;
   }


   /*
   * Call prevSlide() and to check the available previous slides
   * @returns {void}
   */
    prevSlide(): void {
      this.bannersCarousel.previous();
      this.slidesAvailable(this.bannersCarousel);
    }

    /*
     * Call next() and checking available to show
     * @returns { void }
     */
    nextSlide(): void {
      this.bannersCarousel.next();
      this.slidesAvailable(this.bannersCarousel);
    }

    /*
    * Checking if slides are available to show
    * @returns { void }
    */
  slidesAvailable(carousel): void {
    if (this.isSlidesAvailable(carousel)) {
      this.canShowPrevious = carousel.currentSlide > 0;
      this.canShowNext = carousel.currentSlide !== (carousel.slidesCount - 1);
      this.changeDetectorRef.markForCheck();
    }
  }

   /*
    * Validate if slides has to be updated on the prev and next operations
    * @param carousel
    */
   private isSlidesAvailable(carousel: Carousel): boolean {
     return (this.canShowPrevious !== carousel.currentSlide > 0) ||
       (this.canShowNext !== (carousel.currentSlide !== (carousel.slidesCount - 1)));
   }

   /**
    * Fetch Initial Data from CMS
    * @returns { void }
    */
   private getContestBetSlipToolTip(): void {
    this.staticBlockSubscription = this.cmsService.getStaticBlock(this.STATIC_BLOCK_URL)
       .subscribe((staticBlock: IStaticBlock) => {
         this.staticBlockContent = this.domSanitizer.sanitize(SecurityContext.NONE,
           this.domSanitizer.bypassSecurityTrustHtml(staticBlock.htmlMarkup));
        this.changeDetectorRef.markForCheck();
       });
   }

   /*
   * Get the Carousel Instance reference
   * @returns { Carousel }
   */
  public get bannersCarousel(): Carousel {
    return this.carouselService.get(this.CAROUSAL_ID);
  }

  /**
   * checks if any one of the contests is selected
   * @returns { string } returns 1 if selected else 0
   */
  private activeSelCount(): string {
    return this.selectedContest ? '1' : '0';
  }

  /**
   * Trigger the slide up animation after 500ms to update the slide up animation for 1s
   * @returns { void }
   */
  private triggerSlideUp(): void {
    this.slideUpClass = ENTRY_CONFIRMATION.contestSelectionClassname;
  }

  /*
  * Sorts the array based on prize hierarcy and returns the output based on toBeReturned value
  * @param {array} prizeArray - array of first prizes
  * @param {string} toBeReturned - might consist of prize type(cash/voucher/freebet) or prize value
  * @returns { string } or { boolean }
  */
  getPrizetypeIndex(prizeArray: any[], toBeReturned: string) {
    const prizeHierarchy = ['Cash', 'Voucher', 'FreeBet', 'Ticket'];
    prizeArray.sort((prizea, prizeb) => {
      const prizeaKey = prizeHierarchy.indexOf(prizea.type);
      const prizebKey = prizeHierarchy.indexOf(prizeb.type);
      return prizeaKey - prizebKey;
    });
    return toBeReturned === 'prizeValue' ? 
            (prizeArray[0].value < 1 ? (Number(prizeArray[0].value) * 100 + this.allContestConsts.PENCE) : prizeArray[0].value)
            : prizeArray[0].type === toBeReturned;
  }

  /*
  * Checks if the value can shown as a Euro or PENCE
  * @param {array} prizeArray - array of first prizes
  * @param {string} value - might consist of prize type(cash/voucher/freebet) or prize value
  * @returns { boolean }
  */
  checkPenceorEuro(prizeArray: any[], value: string) {
    return this.getPrizetypeIndex(prizeArray, value) >= 1;
  }

  /*
  * Conerts the value to pence if less than 1 euro
  * @param {string} minEntryStake - minimum stake amount
  * @returns { string }
  */
  getMinEntryCurrency(minEntryStake: string) {
    return Number(minEntryStake) < 1 ? (Number(minEntryStake) * 100 + this.allContestConsts.PENCE) : minEntryStake;
  }

}
