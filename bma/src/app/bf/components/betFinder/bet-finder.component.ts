import { Component, OnInit, HostListener, ViewChild, ElementRef, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import * as _ from 'underscore';

import { LocaleService } from '@core/services/locale/locale.service';
import { StorageService } from '@core/services/storage/storage.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { BetFinderHelperService } from '@app/bf/services/bet-finder-helper.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';

import { IBFConstants } from '@app/bf/models/bf-constants.model';
import { IMeeting, IRacesListResponse, IRunner } from '@app/bf/models/races-list.model';
import { IFilters } from '@app/bf/models/filters.model';
import { IBFGtm } from '@app/bf/models/bf-gtm.model';

import { BF_CONSTANTS } from '@app/bf/constants/config';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

@Component({
  selector: 'bet-finder',
  templateUrl: 'bet-finder.component.html'
})
export class BetFinderComponent implements OnInit, OnDestroy {
  window: any;
  bfWidth: string;
  bfConstants: IBFConstants;
  stars: number[] = _.range(0, 5);
  disableSaveButton: boolean = false;
  disableSelectionButton: boolean = false;
  selectedButton: string = '';
  foundResult: string;
  filters: IFilters;
  defaultMeeting: IMeeting;
  meetings: IMeeting[] = [];
  selectedCourse: string;
  isActiveDropDown: boolean = false;
  runners: IRunner[] = [];
  computerButtonsSelector: { outputItem: (item: string) => void, values: { val: string; label: string; }[] };
  refreshRotate: boolean;
  formButtons: string[];
  computerButtons: string[];
  provenButtons: string[];
  oddsButtons: string[];

  headerElm: HTMLElement;
  footerElm: HTMLElement;
  bfElm: HTMLElement;
  cookieElm: HTMLElement;
  buttonsElm: HTMLElement;

  protected document: HTMLDocument;

  @ViewChild('bfFormContainer', {static: true}) private bfFormContainer: ElementRef;

  constructor(
    protected storageService: StorageService,
    protected domToolsService: DomToolsService,
    protected windowRefService: WindowRefService,
    protected localeService: LocaleService,
    protected gtm: GtmService,
    protected router: Router,
    protected betFinderHelperService: BetFinderHelperService,
    protected pubsub: PubSubService,
  ) {
    this.window = this.windowRefService.nativeWindow;
    this.document = this.windowRefService.document;
    this.bfConstants = BF_CONSTANTS;
  }

  ngOnInit(): void {
    this.filters = this.storageService.get('betFinderFilters') || {
      meetingShort: 'All',
      starSelection: 0,
      runnerName: ''
    };

    this.defaultMeeting = {
      course: this.localeService.getString('bf.allMeetings'),
      courseShort: 'All'
    };

    this.selectedCourse = this.defaultMeeting.course;

    this.computerButtonsSelector = {
      outputItem: (item: string) => {
        this.computerButtonsSelector.values.push({
          val: item,
          label: this.localeService.getString(`bf.${item}`)
        });

        this.selectedButton = this.filters[item] ? item : this.selectedButton;
      },
      values: []
    };

    this.provenButtons = this.bfConstants.provenButtons;
    this.formButtons = this.bfConstants.formButtons;
    this.computerButtons = this.bfConstants.computerButtons;
    this.oddsButtons = this.bfConstants.oddsButtons;
    this.computerButtons.forEach(this.computerButtonsSelector.outputItem);

    this.betFinderHelperService.getRacesList()
      .subscribe((res: IRacesListResponse) => this.parseResponse(res), err => console.error(err));

    this.bfElm = this.document.querySelector('.bet-finder-container');
    this.cookieElm = this.document.querySelector('#agreements');
    this.buttonsElm = this.document.querySelector('.bf-buttons');

    // Some elements are not yet ready. Wait until they are.
    this.windowRefService.nativeWindow.setTimeout(() => {
      this.headerElm = this.domToolsService.HeaderEl;
      this.footerElm = this.domToolsService.FooterEl;
    }, 1);

    this.setStickyFooterWidth();

    this.pubsub.subscribe('betFinderComponent', this.pubsub.API.RELOAD_COMPONENTS, () => {
      this.betFinderHelperService.getRacesList()
        .subscribe((res: IRacesListResponse) => this.parseResponse(res), err => console.error(err));
    });
  }

  ngOnDestroy(): void {
    this.pubsub.unsubscribe('betFinderComponent');
  }

  @HostListener('window:resize', [])
  onWindowResize(): void {
    this.setStickyFooterWidth();
  }

  @HostListener('window:scroll', [])
  onWindowScroll(): void {
    this.setStickyFooter();
  }

  /**
   * Track Events by index
   * @param {number} index
   * @returns {number}
   */
  trackByIndex(index: number): number {
    return index;
  }

  /**
   * Select Star.
   * Star selection handler.
   * @param {number} index - index of the star selected 1-5.
   */
  selectStar(index: number): void {
    this.filters.starSelection = this.filters.starSelection === index ? 0 : index;
    const plural = this.filters.starSelection === 1 ? '' : 's';

    this.filter();
    this.sendGTM('star rating', `${this.filters.starSelection} star${plural}`);
  }

  /**
   * Select Checkbox Button.
   * Checkbox button selection handler.
   * @param {string} item - selected button name.
   */
  selectButton(item: string): void {
    this.filters[item] = !this.filters[item];
    const select = this.filters[item] ? 'select' : 'deselect';
    const form = item.indexOf('odds') > -1 ? 'odds' : 'form';
    const action = item === 'provenGoing' ? 'going (ground type)' : form;
    const button = this.localeService.getString(`bf.${item}`).toLowerCase();

    this.filter();
    this.sendGTM(action, `${select} - ${button}`);
  }

  /**
   * onChange.
   * Call filter method and sendGTM on select change.
   *
   */
  onSelectChange(selectedMeeting?: IMeeting): void {
    this.isActiveDropDown = false;
    if (selectedMeeting) {
      this.filters.meetingShort = selectedMeeting.courseShort;
      this.selectedCourse = selectedMeeting.course;
    }
    const meeting: IMeeting = _.find(this.meetings, { courseShort: this.filters.meetingShort });
    this.filter();
    this.sendGTM('meetings', meeting ? meeting.course : 'All meetings');
  }

  /**
   * onClick.
   * use for active state of dropdown meeting
   *
   */
  onClickDropDown(): void {
    this.isActiveDropDown = !this.isActiveDropDown;
  }

  /**
   * onReset.
   * Reset button handler. Set all values to default state.
   *
   */
  onReset(): void {
    this.resetButtonValues(this.formButtons);
    this.resetButtonValues(this.computerButtons);
    this.resetButtonValues(this.provenButtons);
    this.resetButtonValues(this.oddsButtons);
    this.selectedCourse = this.defaultMeeting.course;
    this.filters.runnerName = '';
    this.filters.starSelection = 0;
    this.filters.meetingShort = 'All';
    this.selectedButton = '';

    this.storageService.set('betFinderFilters', this.filters);

    this.refreshRotate = true;
    setTimeout(() => {
      this.refreshRotate = false;
    }, 1000);

    this.filter();
    this.sendGTM('reset');
  }

  /**
   * Save Selection.
   * Save selection handler. Save selected filters into the LocalStorage.
   * In the future new functionality for saving named selections should be developed.
   *
   */
  onSaveSelection(): void {
    // TODO: Develop Save Selection functionality.
    this.storageService.set('betFinderFilters', this.filters);
    this.disableSelectionButton = true;
    this.sendGTM('save selection');
  }

  /**
   * Find Bets.
   * Find Bets handler. Save selected filters into the LocalStorage and switch to results page.
   *
   */
  onFindBets(): void {
    this.betFinderHelperService.setFilters(this.filters);
    this.storageService.set('betFinderFilters', this.filters);
    this.router.navigate(['bet-finder', 'results']);
    this.sendGTM('find bets', this.foundResult, true);
  }

  /**
   * Select Radio Button.
   * Radio Button selection handler.
   * @param {string} selectedItem - selected button name.
   */
  selectRadioButton(selectedItem: string): void {
    _.each(this.computerButtons, (item: string) => {
      this.filters[item] = item === selectedItem ? !this.filters[item] : false;
    });
    const select = this.filters[selectedItem] ? 'select' : 'deselect';
    const button = this.localeService.getString(`bf.${selectedItem}`).toLowerCase();
    this.selectedButton = select === 'select' ? selectedItem : '';

    this.filter();
    this.sendGTM('supercomputer filters', `${select} - ${button}`);
  }

  /**
   * Send GTM.
   * Send GTM information about the event.
   * @param {string} action - action made by user.
   * @param {string} label - value set by user.
   * @param {boolean} betsData - whether bets data should be sent to GMT.
   */
  private sendGTM(action: string, label?: string, betsData?: boolean): void {
    const gtmObject = <IBFGtm>{
      eventCategory: 'bet finder',
      eventAction: action,
      eventLabel: label || ''
    };

    if (betsData) {
      const starPlural = this.filters.starSelection === 1 ? '' : 's';
      const meeting = _.find(this.meetings, { courseShort: this.filters.meetingShort });

      gtmObject.betFinderSearch = this.filters.runnerName;
      gtmObject.betFinderOdds = this.selectedButtons(this.oddsButtons);
      gtmObject.betFinderForm = this.selectedButtons(this.formButtons);
      gtmObject.betFinderGoing = this.selectedButtons(this.provenButtons);
      gtmObject.betFinderSupercomputer = this.selectedButtons(this.computerButtons);
      gtmObject.betFinderStarRating = `${this.filters.starSelection} star${starPlural}`;
      gtmObject.betFinderMeetings = meeting ? meeting.course : 'All meetings';
    }

    this.gtm.push('trackEvent', gtmObject);
  }

  /**
   * Set Sticky Footer.
   * When bf footer is hidden add position fixed, so it would be visible.
   * @private
   */
  private setStickyFooter(): void {
    if (this.headerElm && this.footerElm) {
      const elmHeight = this.domToolsService.getOuterHeight(this.bfElm) +
                        (this.cookieElm ? this.domToolsService.getOuterHeight(this.cookieElm) : 0) +
                        this.domToolsService.getOuterHeight(this.headerElm) +
                        this.domToolsService.getOuterHeight(this.footerElm) + 40;
      const scroll = elmHeight - this.domToolsService.getHeight(this.window) - this.domToolsService.getScrollTop(this.window);

      this.domToolsService.toggleClass(this.buttonsElm, 'fixed', scroll > 0);
    }
  }

  /**
   * Set Sticky Footer Width.
   * Sticky footer width should be the same as the width of the widget.
   * @private
   */
  private setStickyFooterWidth(): void {
    setTimeout(() => {
      this.bfWidth = this.bfFormContainer.nativeElement.offsetWidth;
    }, 500);
  }

  /**
   * Parse Response.
   * Set initial data to the component after the response is received.
   * @param {object} res - response object.
   * @private
   */
  private parseResponse(res: IRacesListResponse): void {
    if (res.cypher) {
      res.cypher.meetings.unshift(_.clone(this.defaultMeeting));
      this.meetings = res.cypher.meetings;
      this.runners = res.cypher.runners;
      this.filters.meetingShort = this.getMeeting(res.cypher.meetings).courseShort;
    }

    this.filter();
  }

  /**
   * Get meeting.
   * If saved meeting still exists in the response return it, otherwise return defaul meeting.
   * @param {array} meeting - array of meetings available in the response.
   * @private
   */
  private getMeeting(meetings: IMeeting[]): IMeeting {
    const meeting = _.find(meetings, { courseShort: this.filters.meetingShort }) || this.defaultMeeting;
    this.selectedCourse = meeting.course;

    return meeting;
  }

  /**
   * Reset button values.
   * Set all button values to false.
   * @param {array} buttons - array of buttons to be reset.
   * @private
   */
  private resetButtonValues(buttons: string[]): void {
    _.each(buttons, (button: string) => {
      this.filters[button] = false;
    });
  }

  /**
   * Selected buttons.
   * Returns string of selected buttons delimited with ' | '.
   * @param {array} buttons - array of buttons to be checked.
   * @return {string}
   * @private
   */
  private selectedButtons(buttons: string[]): string {
    return _.compact(_.map(buttons, (button: string) =>
      this.filters[button] ? this.localeService.getString(`bf.${button}`).toLowerCase() : ''
    )).join(' | ');
  }

  /**
   * Set Selection Number.
   * Create a string that will be displayed on the "Find bets" button indicating a number of selections.
   * @param {number} len - number of filtered selections.
   * @private
   */
  private setSelectionsNumber(len: number): void {
    const selectStr = len === 0 ? this.localeService.getString('bf.noselection') : this.localeService.getString('bf.selection');
    const plural = len === 1 ? '' : 's';
    this.foundResult = `${len || ''} ${selectStr}${plural} ${this.localeService.getString('bf.found')} `;
  }

  /**
   * Filter.
   * Call factory method for filtering the runners.
   * @private
   */
  private filter(): void {
    const filteredRunners = this.betFinderHelperService.filterRunners(this.runners, this.filters);

    this.disableSaveButton = !filteredRunners.length;
    this.disableSelectionButton = false;

    this.setSelectionsNumber(filteredRunners.length);
  }
}
