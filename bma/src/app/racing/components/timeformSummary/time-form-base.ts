import { Component, OnInit } from '@angular/core';
import { GtmService } from '@core/services/gtm/gtm.service';
import { LocaleService } from '@core/services/locale/locale.service';
@Component({
  selector: 'time-form-base',
  template: ''
})
export class TimeFormBaseComponent implements OnInit {

  details = {
    text: '',
    expanded: false,
    expandable: true,
    expandedText: ''
  };
  summaryText: string;

  static get SUMMARY_MAX_LENGTH(): number {
    return 100;
  }

  static set SUMMARY_MAX_LENGTH(value:number){}

  constructor(
    protected gtmService: GtmService,
    protected locale: LocaleService,
  ) { }

  ngOnInit(): void {
    if (this.summaryText.length > TimeFormBaseComponent.SUMMARY_MAX_LENGTH) {
      this.details.text = this.truncateSummaryText(this.summaryText);
    } else {
      this.details.text = this.summaryText;
      this.details.expanded = true;
      this.details.expandable = false;
    }
    this.details.expandedText = this.getExpandedText(this.details.expanded);
  }

  /**
   * toggleSummary()
   */
  toggleSummary(): void {
    if (this.details.expanded) {
      this.details.text = this.truncateSummaryText(this.summaryText);
    } else {
      this.details.text = this.summaryText;
      this.gtmService.push('trackEvent', {
        eventCategory: 'greyhounds',
        eventAction: 'race card',
        eventLabel: 'show more'
      });
    }

    this.details.expanded = !this.details.expanded;
    this.details.expandedText = this.getExpandedText(this.details.expanded);
  }

  getExpandedText(expanded: boolean): string {
    return this.locale.getString(expanded ? 'racing.showLess' : 'racing.showMore');
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
   * truncateSummaryText()
   * @param {string} text
   * @returns {string}
   */
  protected truncateSummaryText(text: string): string {
    return `${text.substring(0, TimeFormBaseComponent.SUMMARY_MAX_LENGTH)}...`;
  }
}
