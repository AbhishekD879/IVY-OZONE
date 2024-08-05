import { CurrencyPipe } from '@angular/common';
import { ChangeDetectorRef, Component, EventEmitter, Input, OnInit, Output, OnChanges } from '@angular/core';
import { BetpackCmsService } from '@app/lazy-modules/betpackPage/services/betpack-cms.service';
import { UserService } from '@core/services/user/user.service';
import { Filter, FilterModel } from '@app/betpackReview/components/betpack-review.model';
import { GtmService } from '@app/core/services/gtm/gtm.service';
@Component({
  selector: 'betpack-tab',
  templateUrl: './betpack-tab.component.html',
  styleUrls: ['./betpack-tab.component.scss'],
})
export class BetPackTabComponent implements OnInit, OnChanges {

  @Output() readonly tabChange: EventEmitter<Filter> = new EventEmitter<Filter>();
  tabs: Filter[] = [];
  @Input() filterValues;
  cmsFilterVal = [];
  filtersCount: number;
  activeFilter: any
  @Input() allFilterMsg: string
  @Input() allFilterMsgActive:boolean

  constructor(private betpackCmsService: BetpackCmsService,
    public currencyPipe: CurrencyPipe,
    public userService: UserService,
    public changeDetectorRef: ChangeDetectorRef,
    private gtmService: GtmService
  ) { }

  /**
   * @returns {void}
   */
  ngOnChanges(): void {
    this.tabsProcess();
  }

  /**
   * to init logic
   * @returns {void}
   */
  ngOnInit(): void {
    this.betpackCmsService.getBetPackFilters().subscribe((data: FilterModel[]) => {
      this.tabs = data;
      this.tabs.sort((a, b) => a.sortOrder < b.sortOrder ? -1 : a.sortOrder > b.sortOrder ? 1 : 0);
      this.tabsProcess();
    });
  }

  /**
   * to process the tab data
   * @returns {void}
   */
  tabsProcess(): void {
    this.tabs.forEach(element => {
      element.isVisible = true;
      element.filterActive = false;
      element.filterNameFrCurr = element.filterName;
      if (Number(element.filterNameFrCurr)) {
        element.filterNameFrCurr = this.currencyPipe.transform(Number(element.filterNameFrCurr).toFixed(2), this.userService.currencySymbol, 'code', '1.0-0');
      }
      this.cmsFilterVal.push(element.filterName);
      if (element.filterName === 'All') {
        element.isVisible = false;
      }
    });
    this.filterValues = [...this.filterValues];
    const intersection = this.cmsFilterVal.filter(x => !this.filterValues.includes(x));
    if (intersection.length != 0) {
      this.tabs.forEach(element => {
        if (intersection.includes(element.filterName)) {
          element.isVisible = false;
        }
      });
    }
    this.filtersCount = this.tabs.filter(ele => ele.isVisible === true).length;
    if (this.filtersCount > 0) {
      this.activeFilter = {
        filterName: 'All',
        filterNameFrCurr: 'All',
        filterActive: true,
        isVisible: true,
        isLinkedFilter: this.allFilterMsgActive,
        linkedFilterWarningText: this.allFilterMsg ? this.allFilterMsg : ''
      }
      this.tabs.unshift(this.activeFilter);
    }
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Emits tab to the parent component
   * @param {Filter} event
   * @returns {void}
   */
  onTabSelect(event: Filter): void {
    this.tabs.forEach((tab: Filter) => {
      if (event.filterName === tab.filterName) {
        this.activeFilter = event
        tab.filterActive = true;
      } else {
        tab.filterActive = false;
      }
    });
    this.tabChange.emit(event);
    const gtmData = {
      event: 'trackEvent',
      eventAction: 'bet bundles',
      eventCategory: 'bet bundles marketplace',
      eventLabel: 'filters',
      eventDetails: event.filterName
    };
    this.gtmService.push(gtmData.event, gtmData);
  }

}