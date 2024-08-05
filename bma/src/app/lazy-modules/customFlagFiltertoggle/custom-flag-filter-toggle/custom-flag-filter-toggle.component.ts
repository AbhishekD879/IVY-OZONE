import { Component, EventEmitter,Input,Output,ViewEncapsulation, SimpleChanges } from '@angular/core';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import environment from '@environment/oxygenEnvConfig';
import { LocaleService } from '@app/core/services/locale/locale.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { OnInit, OnChanges } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { WindowRefService } from '@core/services/windowRef/window-ref.service';
@Component({
  selector: "custom-flag-filter-toggle",
  templateUrl: "./custom-flag-filter-toggle.component.html",
  styleUrls: ["./custom-flag-filter-toggle.component.scss"],
  encapsulation: ViewEncapsulation.None,
})
export class CustomFlagFilterToggleComponent implements OnInit, OnChanges {
 _filters: any = [];
  @Input() set filters(value: []) {
    this._filters = value;
  }
  get filters() {
    return this._filters;
  }
  @Input() selectedFilter: any = "All";
  @Input() compName: string = "";
  @Input() moduleType: string = "";
  @Input() isLadsSideWidget = false;
  @Input() isNxtTabEnabled = false;
  @Output() filterChange: EventEmitter<any> = new EventEmitter<any>();
  isBrandLadbrokes: boolean;
  countries = {
    All: "All",
    "UK&IRE": "UK & Irish",
    INT: "International",
    VR: "Virtuals",
    FR: "France",
    AE : "UAE",
    ZA : "South Africa",
    IN : "India", 
    US : "USA",
    AU :"Australia",
    CL : "Chile"
   };
  countri: any;
  greyhoundstodayTab: string;
  landingPageGH: boolean;
  constructor(private locale: LocaleService, private gtmService: GtmService , private route: ActivatedRoute,
    private windowRef: WindowRefService) {}
  ngOnInit(): void {
  this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
    this.route.params.subscribe((params) => {
      this.greyhoundstodayTab = params['display'];
      this.landingPageGH = false;
      if(this.windowRef.nativeWindow.location.pathname ==='/greyhound-racing'){
        this.landingPageGH = !this.isNxtTabEnabled;
      }
    });

  }
  /**
   * Emits filter to the parent component
   * @param {any} filter
   */
  onFilterSelect(filter: any): void {
    this.gtmService.push('Event.Tracking', {
      "event" : 'Event.Tracking',
      "component.CategoryEvent" : 'sports lobby widgets',
      "component.LabelEvent" : 'sub navigation',
      "component.ActionEvent" : 'click',
      "component.PositionEvent" : this.compName, 
      "component.LocationEvent" : 'next races', 
      "component.EventDetails": this.countries[filter.flag].toLowerCase(), 
      "component.URLClicked": window.location.href
    });
    this.filterChange.emit(filter);
  } 

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.filters) {
      const hasSelected = this._filters.filter((data: any) => data.flag === this.selectedFilter);
      if(hasSelected.length === 0 && this._filters.length > 0){
        this.selectedFilter = 'All';
        this.onFilterSelect(this._filters[0]);
      }
    }
  }
}