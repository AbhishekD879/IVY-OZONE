import * as _ from 'underscore';
import {
  AfterViewInit,
  Component, ElementRef, EventEmitter, Input,
  OnChanges, OnDestroy, OnInit, Output, SimpleChanges
} from '@angular/core';
import { Router } from '@angular/router';

import { LocaleService } from '@core/services/locale/locale.service';
import { ITab } from './tabs-panel.model';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { NavigationService } from '@coreModule/services/navigation/navigation.service';
import { CasinoMyBetsIntegratedService } from '@app/betHistory/services/CasinoMyBetsIntegratedService/casino-mybets-integrated.service';

@Component({
  selector: 'tabs-panel',
  templateUrl: 'tabs-panel.component.html',
  styleUrls: ['tabs-panel.component.scss']
})
export class TabsPanelComponent implements OnChanges, OnDestroy, OnInit, AfterViewInit {
  @Output() readonly tpFunction?: EventEmitter<{ id: string; tab: ITab }> = new EventEmitter();

  @Input() tpTabs: ITab[];
  @Input() routerLinkDisable: boolean;
  @Input() tpActiveTab?: ITab;
  @Input() tbClass?: boolean;
  @Input() typeId?: string | null;
  @Input() tpFuncArr?: string;
  @Input() hidden?: boolean;
  @Input() detectGTMLocation?: string;
  @Input() maxElementsToDisplay?: number;

  setActiveTabForCasino: boolean = false;

  constructor(
    public elementRef: ElementRef,
    public locale: LocaleService,
    public router: Router,
    public gtmTrackingService: GtmTrackingService,
    public casinoMyBetsIntegratedService: CasinoMyBetsIntegratedService,
    protected navigationService: NavigationService
  ) { }

  /**
   * Tab Function
   * @param {ITab} tab
   * @param {MouseEvent} $event
   */
  clickFunction(tab: ITab, $event: MouseEvent): void {
    $event.preventDefault();

    this.detectActiveTab(tab);

    if (tab.url && !this.routerLinkDisable) {
      this.navigationService.openUrl(tab.url, true, true);
    }

    if (this.tpFunction.observers.length) {
      this.tpFunction.emit({ id: tab[this.tpFuncArr], tab: tab });
    }
  }

  /**
   * Check for 5ASide Tab
   * @param tab
   * @returns {boolean}
   */
  is5ASideTab(tab: ITab): boolean {
    return tab.marketName === '5-a-side';
  }

  ngOnInit(): void {
    if (this.tpTabs) {
      this.tpTabs = this.getTabsWithTitle(this.tpTabs);
      this.setActiveTabAsTpTabs(this.tpActiveTab);
      this.gtmTrackTabName();
    }
  }

  detectActiveTab(tab: ITab): void {
    if (this.detectGTMLocation && tab) {
      this.gtmTrackingService.setLocation(tab.title || tab.label || tab.name, this.detectGTMLocation);
    }
  }

  ngOnChanges(changesObj: SimpleChanges): void {
    if (changesObj.tpTabs && !changesObj.tpTabs.firstChange) {
      this.tpTabs = this.getTabsWithTitle(this.tpTabs);
      this.gtmTrackTabName();
    }
    if (changesObj.tpActiveTab && !changesObj.tpActiveTab.firstChange) {
      this.setActiveTabAsTpTabs(this.tpActiveTab);
    }
  }

  ngAfterViewInit(): void {
    if (this.casinoMyBetsIntegratedService.isMyBetsInCasino) {
      this.casinoMyBetsIntegratedService.bmaInit();
      this.setActiveTabForCasino = this.casinoMyBetsIntegratedService.getOpenBetTabActiveStatus();
      if (!!this.setActiveTabForCasino) {
        this.tpTabs.forEach((myBetsTab: ITab) => {
          if (myBetsTab.title === 'Open Bets') {
            myBetsTab.selected = true;
          }
        });
      }
    }
  }

  ngOnDestroy(): void {
    if (this.detectGTMLocation) {
      this.gtmTrackingService.clearLocation(this.detectGTMLocation);
    }
  }

  /**
   * Set Active Class
   * @param {ITab} tab
   * @returns {boolean}
   */
  setActiveClass(tab: ITab): boolean {
    return this.tpActiveTab ? tab.id === this.tpActiveTab.id : tab.selected;
  }

  /**
   * Set tpActiveTab as tpTabs if only 1 tab is being displayed
   * @param {ITab} tpActiveTab
   */
  private setActiveTabAsTpTabs(tpActiveTab: ITab): void {
    if (this.tpTabs && this.tpTabs.length === 1 && this.tpActiveTab !== undefined) {
      this.tpTabs = [tpActiveTab];
    }
  }

  /**
   * Get tabs list with translated title property
   * @param {ITab[]} tabs
   * @returns ITab[]
   */
  private getTabsWithTitle(tabs: ITab[]): ITab[] {
    const slicedTabs = this.maxElementsToDisplay ? tabs.slice(0, this.maxElementsToDisplay) : tabs;
    slicedTabs
      .forEach((tab: ITab) => {
        const title: string = tab.title || tab.label;
        tab.title = title && title.match(/\./) ? this.locale.getString(title) : title;
      });

    return slicedTabs;
  }

  private gtmTrackTabName(): void {
    const activeTab = _.find(this.tpTabs, (tab) => this.setActiveClass(tab));
    this.detectActiveTab(activeTab);
  }

}
