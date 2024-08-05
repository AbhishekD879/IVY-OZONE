import { Component, EventEmitter, Input, OnDestroy, OnInit, OnChanges, Output, SimpleChanges } from '@angular/core';
import { Router } from '@angular/router';
import * as _ from 'underscore';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { ITab } from '@shared/components/tabsPanel/tabs-panel.model';
import { LocaleService } from '@core/services/locale/locale.service';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { NavigationService } from '@coreModule/services/navigation/navigation.service';
import { IConstant } from '@app/core/services/models/constant.model';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { GA_TRACKING, GOLF_CONSTANTS, GOLF_CURRENT_TAB } from '@app/shared/constants/channel.constant';
import { IGATrackingModel } from '@app/core/models/gtm.event.model';
import { FiltersService } from '@core/services/filters/filters.service';
@Component({
  selector: 'switchers',
  templateUrl: 'switchers.component.html'
})

export class SwitchersComponent implements OnInit, OnDestroy, OnChanges {
  @Output() readonly switchAction?: EventEmitter<{ id: string; tab: ITab | {} }> = new EventEmitter();

  @Input() switchIdPropertyName?: string;
  @Input() type: string;
  @Input() switchers: ISwitcherConfig[] | ITab[] | any;
  @Input() filter: any;
  @Input() activeTab: ITab | IConstant;
  @Input() noPaddings: boolean;
  @Input() noMargin: boolean;
  @Input() detectGTMLocation?: string;
  @Input() preventRouteChange?: boolean;
  @Input() GATrackingModule?: string;
  @Input() GTMTrackingObj?: IGATrackingModel
  @Input() isOverlay?:boolean = false;
  @Input() preventReload?: boolean;
  @Input() sportName?:string ;
  readonly maxTabsForEqualColumns: number = 4;

  constructor(
    private locale: LocaleService,
    public router: Router,
    private gtmTrackingService: GtmTrackingService,
    private navigationService: NavigationService,
    private gtmService: GtmService,
    protected filtersService: FiltersService
  ) { }

  getTabName(tab: ISwitcherConfig | ITab) {
    const translationName = (tab as ITab).title || tab.label || (tab as ISwitcherConfig).name;
    return translationName && translationName.match(/\./) ? this.locale.getString(translationName)
      : translationName;
  }

  ngOnInit() {
    this.type = this.type || 'regular';
    this.gtmTrackTabName();
  }

  ngOnChanges(changes: SimpleChanges) {
    this.gtmTrackTabName();
    if(this.sportName=='golf'){
      if(changes.activeTab.currentValue && (changes.activeTab.previousValue && 
        (changes.activeTab.currentValue.id !== changes.activeTab.previousValue.id)) &&
        GOLF_CURRENT_TAB.prevActiveTab !== changes.activeTab.currentValue.id ){
          GOLF_CURRENT_TAB.activeTab = changes.activeTab.currentValue.id;
          const tab = changes.activeTab.currentValue;
          this.sendGTMDataOnTabClick(tab);
        }
        GOLF_CURRENT_TAB.prevActiveTab =  changes.activeTab.currentValue && changes.activeTab.currentValue.id;
    }
  }

  ngOnDestroy() {
    if (this.detectGTMLocation) {
      this.gtmTrackingService.clearLocation(this.detectGTMLocation);
    }
  }

  trackByLabel(index: number, value: ISwitcherConfig | ITab): string {
    return value.label;
  }

  /**
   * Set Active Class
   * @param {ITab} tab
   * @returns {boolean}
   */
  isActive(tab: ISwitcherConfig | ITab, switcherIndex?: number): boolean {
    if (this.filter || this.filter === 0) {
      return this.filter === (tab as ISwitcherConfig).viewByFilters || +this.filter === +switcherIndex;
    }
    return this.activeTab ? (tab as ITab).id === this.activeTab.id : (tab as ITab).selected;
  }

  /**
   * Tab Function
   * @param {ITab} tab
   * @param {MouseEvent} $event
   */
  clickFunction(tab: ISwitcherConfig | ITab, $event: MouseEvent, switchPos: number): void {
    $event.preventDefault();
    if (this.preventReload && ((this.activeTab && this.activeTab.id === (tab as ITab).id) || (this.filter>=0 && this.switchers[this.filter].url === (tab as ITab).url))) {
      return;
    }
    this.detectActiveTab(tab);

    if ((tab as ISwitcherConfig).onClick) {
      (tab as ISwitcherConfig).onClick((tab as ISwitcherConfig).viewByFilters);
      return;
    }

    if ((tab as ITab).url && !this.preventRouteChange) {
      this.navigationService.openUrl((tab as ITab).url, true, true);
    }

    if (this.switchAction.observers.length) {
      this.switchAction.emit({ id: tab[this.switchIdPropertyName], tab: (tab as ITab) });
    }
    if (this.GTMTrackingObj && this.GTMTrackingObj.isHomePage
      && (this.GATrackingModule == GA_TRACKING.moduleRibbon.moduleName || this.GATrackingModule == GA_TRACKING.sportsRibbon.moduleName)) {
      this.gtmTracker({ ...tab, position: switchPos });
    }
  }

  /**
   * GA Tracking click actions
   * @returns void
   */
  gtmTracker(switcher): void {
    const trackingObj = {
      eventAction: switcher.title,
      eventCategory: GA_TRACKING.moduleRibbon.eventCategory,
      eventLabel: switcher.url,
      position: switcher.position
    };
    this.gtmService.push('trackEvent', trackingObj);
  }

  isAutoSizable() {
    const displayedSwitchersCount = _.filter(this.switchers, (switcher: ISwitcherConfig | ITab) => !(switcher as ITab).hidden).length;
    return displayedSwitchersCount > this.maxTabsForEqualColumns;
  }

  detectActiveTab(tab: ISwitcherConfig | ITab | any): void {
    if (this.detectGTMLocation && tab) {
      this.gtmTrackingService.setLocation(this.getTabName(tab), this.detectGTMLocation);
    }
    if(this.isOverlay) {
      this.switchers.forEach(switcher => {
        switcher.selected = switcher.viewByFilters === tab.viewByFilters ? true : false;
      })
    }
  }

  private gtmTrackTabName(): void {
    let activeTab;

    if (!this.detectGTMLocation) {
      return;
    }
    this.filterLinks();
    if (this.type === 'links') {
      const filter = this.filter || 0;
      activeTab = this.switchers[filter] || null;
    } else {
      activeTab = _.find(this.switchers, (tab, index) => this.isActive(tab, Number(index)));
    }
    this.detectActiveTab(activeTab);
  }

  filterLinks(){
    this.switchers.map(tab =>{
      if(tab.url && tab.url.includes('racingsuperseries')){
        this.filtersService.filterLinkforRSS(tab.url).subscribe(data =>{
          tab.url = data;
        })
       
       }
    })
  }
  sendGTMDataOnTabClick(selectedTab){
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'navigation',
      'component.LabelEvent': 'golf',
      'component.ActionEvent': 'click',
      'component.PositionEvent': 'not applicable',
      'component.LocationEvent': GOLF_CONSTANTS[selectedTab.id],
      'component.EventDetails': GOLF_CONSTANTS[selectedTab.id],
      'component.URLClicked': 'Clicked URL'
    }
    this.gtmService.push(gtmData.event, gtmData);
  }
}
