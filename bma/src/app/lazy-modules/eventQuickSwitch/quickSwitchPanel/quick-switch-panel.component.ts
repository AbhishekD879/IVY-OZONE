import { ChangeDetectorRef, Component, EventEmitter, Input, OnInit, OnDestroy, Output, ElementRef } from '@angular/core';
import { CurrentMatchesService } from '@sb/services/currentMatches/current-matches.service';
import { ITypeSegment, IGroupedByDateObj, IGroupedByDateItem } from '@app/inPlay/models/type-segment.model';
import { Subscription } from 'rxjs';
import { ISwitcherConfig } from '@app/core/models/switcher-config.model';
import { FiltersService } from '@core/services/filters/filters.service';
import { ActivatedRoute } from '@angular/router';
import { GtmService } from '@core/services/gtm/gtm.service';
import { DeviceService } from '@core/services/device/device.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import environment from '@environment/oxygenEnvConfig';
import { RendererService } from '@app/shared/services/renderer/renderer.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { ITab } from '@app/shared/components/tabsPanel/tabs-panel.model';
import { GamingService } from '@app/core/services/sport/gaming.service';

@Component({
  selector: 'quick-switch-panel',
  templateUrl: './quick-switch-panel.component.html',
  styleUrls: ['./quick-switch-panel.component.scss']
})
export class QuickSwitchPanelComponent implements OnInit, OnDestroy {
  @Output() readonly closeQuickSwitchPanel: EventEmitter<void> = new EventEmitter();

  @Input() sport: GamingService;
  @Input() typeId: string;
  @Input() changeMatch: boolean;

  private getDataSubscription: Subscription;
  protected routeParamsListener: Subscription;
  sportId: string;
  isLoaded: boolean = false;
  isLazyComponentLoaded: boolean;
  isChildComponentLoaded: boolean = false;
  eventsByCategory: ITypeSegment;
  filteredQuickSwitchEvents: IGroupedByDateItem[] = [];
  indexPage: number;
  tab: string;
  showNoEvents: boolean = false;
  todayEvents: IGroupedByDateItem[] = [];
  tomorrowEvents: IGroupedByDateItem[] = [];
  futureEvents: IGroupedByDateItem[] = [];
  gtmInfo: string[] = ['close', 'click'];
  gtmTrack: string[] = ['not applicable', 'sub-navigation', 'matches overlay', 'change match']
  switchers: ISwitcherConfig[] | ITab[] | any = [
    {
      id: 'tab-today',
      name: 'today',
      label: 'Today'

    },
    {
      id: 'tab-tomorrow',
      name: 'tomorrow',
      label: 'Tomorrow'
    },
    {
      id: 'tab-future',
      name: 'future',
      label: 'Future'
    }
  ];
  activeTab: { id: string; name: string } = {
    id: 'tab-today',
    name: 'today'
  };
  window: any;
  element: any;
  interval: any;
  sticky: boolean = false;
  isActive: boolean = true;
  isMobile: boolean = false;
  isDesktop: boolean = false;
  isIosWrapper: boolean = false;
  isLadbrokes: boolean = false;
  isCoral: boolean = false;
  homeBody: Element;

  readonly TABLET_BOTTOM_MENU_HEIGHT: number = 52;
  readonly DASHBOARD_MIN_HEIGHT: number = 50;
  readonly DASHBOARD_MIN_HEIGHT_CORAL: number = 200;

  constructor(
    private windowRefService: WindowRefService,
    private elementRef: ElementRef,
    private domToolsService: DomToolsService,
    private currentMatchesService: CurrentMatchesService,
    private deviceService: DeviceService,
    private filterService: FiltersService,
    private changeDetectorRef: ChangeDetectorRef,
    private gtmService: GtmService,
    protected route: ActivatedRoute,
    private rendererService: RendererService,
    private pubSubService: PubSubService
  ) { 

    this.window = this.windowRefService.nativeWindow;
    this.element = this.elementRef.nativeElement;
    this.isMobile = deviceService.isMobileOrigin;
    this.isDesktop = deviceService.isDesktop;
    this.isIosWrapper = deviceService.isWrapper && deviceService.isIos;
    this.isLadbrokes = environment.brand === 'ladbrokes';
    this.isCoral = environment.brand === 'bma';
  }

  ngOnInit(): void {
    this.pubSubService.publish(this.pubSubService.API.QUICK_SWITCHER_ACTIVE, true);
    this.interval = this.windowRefService.nativeWindow.setInterval(() => {
      this.relocate();
    }, 0);
    this.gaTracking(this.gtmInfo[1], this.gtmTrack[0], this.gtmTrack[3]);
    this.sportId = this.sport.sportConfig.config.request.categoryId;
    if(this.isMobile) {
      this.homeBody =  this.windowRefService.document.querySelector('body');
      this.homeBody && this.rendererService.renderer.addClass(this.homeBody, 'quick-switch-scroll-overlay');
    }    
    this.loadCompetitionsData();
  }
  ngOnDestroy(): void {
    this.pubSubService.publish(this.pubSubService.API.QUICK_SWITCHER_ACTIVE, false);
    this.interval && clearInterval(this.interval);
    this.closeMenu();
    this.getDataSubscription && this.getDataSubscription.unsubscribe();
    this.routeParamsListener && this.routeParamsListener.unsubscribe();
    if (this.homeBody && this.isMobile) {      
      this.rendererService.renderer.removeClass(this.homeBody, 'quick-switch-scroll-overlay');
    }
  }
  closeMenu(fromClick?: boolean) {
    this.closeQuickSwitchPanel.emit();
    if (fromClick) {
      this.gaTracking(this.gtmInfo[0], this.gtmTrack[0], this.gtmTrack[2]);
    }
    if (this.homeBody && this.isMobile) {      
      this.rendererService.renderer.removeClass(this.homeBody, 'quick-switch-scroll-overlay');
    }
  }
  protected selectTab({ tab }: { id: string, tab: { name: string } | any }): void {
    this.activeTab.id = tab.id;
    this.activeTab.name = tab.name;
    if(tab.name === 'today') this.filteredQuickSwitchEvents = this.todayEvents;
    else if(tab.name === 'tomorrow') this.filteredQuickSwitchEvents = this.tomorrowEvents;
    else this.filteredQuickSwitchEvents = this.futureEvents;
    this.gaTracking(this.gtmInfo[1], this.gtmTrack[1], this.activeTab.name);
  }

  loadCompetitionsData(): void {
    this.currentMatchesService.getEventsByTypeWithMarketCounts(this.typeId, this.sport.sportConfig, true).then(events => {
      this.eventsByCategory = this.sport.arrangeEventsBySection(events, true)[0];
      // unsubscribe from previous competition events
      this.currentMatchesService.unSubscribeForUpdates();
      // subscribe LS Updates via WS;
      this.currentMatchesService.subscribeForUpdates(events);
      this.groupEvents();
      this.changeDetectorRef.detectChanges();
      return this.eventsByCategory;
    });
  }
  /**
   * 
   * Groups all the events into Today/Tomorrow/Future categories
   */
  groupEvents(): void {
    const groupedByDate: IGroupedByDateObj = this.eventsByCategory && this.eventsByCategory.groupedByDate;
    if (!groupedByDate) {
      this.filteredQuickSwitchEvents = [];
      this.showNoEvents = true;
      return;
    }
    const groups = [];
    Object.keys(groupedByDate).forEach((date: string) => {
      if (!groupedByDate[date].deactivated) {
        groupedByDate[date].events = this.filterService.orderBy(groupedByDate[date].events, ['startTime', 'displayOrder', 'name']);
        groups.push(groupedByDate[date]);
      }
    });
    groups.forEach((group: IGroupedByDateItem) => {
      if(group.title.toLowerCase() === 'today') {
        this.todayEvents.push(group);
      } else if(group.title.toLowerCase() === 'tomorrow') {
        this.tomorrowEvents.push(group);
      } else {
        this.futureEvents.push(group);
      }
    });
    
    const tabId = this.todayEvents.length>0 ? 'tab-today' : (this.tomorrowEvents.length>0 ? 'tab-tomorrow' : 'tab-future');
    const tabName = this.todayEvents.length>0 ? 'today' : (this.tomorrowEvents.length>0 ? 'tomorrow' : 'future');
    this.activeTab = {
      id: tabId,
      name: tabName
    };
    if(tabName === 'today') this.filteredQuickSwitchEvents = this.todayEvents;
    else if(tabName === 'tomorrow') this.filteredQuickSwitchEvents = this.tomorrowEvents;
    else this.filteredQuickSwitchEvents = this.futureEvents;
    this.isLoaded = true;
  }
  initLazyHandler(): void {
    this.isLazyComponentLoaded = true;
    this.isChildComponentLoaded = true;
  }
  /**
 * Recalculate dashboard position and dimensions
 */
  relocate(): void {
    if (this.deviceService.isMobileOrigin && !this.deviceService.isTablet) {
      return;
    }

    const container = this.element;
    const dashboard = container.querySelector('.quick-switch-section');
    const closeMenu = container.querySelector('.close-panel');
    const overlay = document.querySelector('.quick-switch-overlay-lads');
    if (!dashboard) {
      return;
    }

    const windowHeight = this.window.innerHeight || 0;
    const windowYOffset = this.window.pageYOffset || 0;
    const dashboardHeight = this.domToolsService.getHeight(dashboard) || (this.isLadbrokes ? this.DASHBOARD_MIN_HEIGHT : this.DASHBOARD_MIN_HEIGHT_CORAL);
    const dashboardOffset = this.domToolsService.getOffset(container).top || 0;
    const dashboardBottom = this.deviceService.isDesktop || this.deviceService.isMobile ? 0 : this.TABLET_BOTTOM_MENU_HEIGHT;
    const dashBoardWidth = this.domToolsService.getWidth(container.offsetParent) - (this.isLadbrokes ? 11.5 : 0);

    this.sticky = dashboardOffset + dashboardHeight + dashboardBottom - 340 > windowHeight + windowYOffset;
    
    if (this.sticky || this.domToolsService.getScrollTopPosition() == 0) {
      this.isActive = true;
      dashboard && this.domToolsService.css(dashboard, {
        position: 'fixed',
        left: container.getBoundingClientRect().left,
        bottom: dashboardBottom,
        width: dashBoardWidth
      });
      closeMenu && this.domToolsService.css(closeMenu, {
        position: 'fixed',
        left: container.getBoundingClientRect().left,
        bottom: dashboardBottom,
        width: dashBoardWidth
      });
      overlay && this.domToolsService.css(overlay, {
        width: dashBoardWidth
      });
    } else {
      this.isActive = false;
    }
  }
  /**
  * GATracking
  * @param  {string} action
  * @param  {string} track
  * @param  {string} data
  * @returns {void}
  */
  private gaTracking(action: string, track: string, data: string): void {
    const gtmData = {
      'event': "Event.Tracking",
      'component.CategoryEvent': "event switcher",
      'component.LabelEvent': "events",
      'component.ActionEvent': action,
      'component.PositionEvent': track,
      'component.LocationEvent': "edp",
      'component.EventDetails': data 
    }
    this.gtmService.push(gtmData.event, gtmData);
  }
}
