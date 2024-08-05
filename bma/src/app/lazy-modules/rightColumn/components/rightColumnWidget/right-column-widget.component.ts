import { map, concatMap } from 'rxjs/operators';
import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router, NavigationEnd, Event } from '@angular/router';
import { Subscription } from 'rxjs';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { VisEventService } from '@core/services/visEvent/vis-event.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { IWidget } from '@rightColumnModule/components/rightColumnWidget/widget.model';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { DeviceService } from '@core/services/device/device.service';
import { CROSSSELL_VALUES } from '@app/lazy-modules/arcUser/constants/arcUser-constants';

@Component({
  selector: 'right-column-widget',
  templateUrl: 'right-column-widget.component.html'
})
export class RightColumnWidgetComponent implements OnInit, OnDestroy {
  @Input() widgetColumn: string;
  @Input() widgetDataStore: IWidget[];

  directiveArr: string[];
  showMatchCentre: boolean;
  lastCheckedId: string;
  isAnotherPage: boolean;
  locationChangeListener: Subscription;
  widgets: IWidget[];
  deviceType: string;
  isDesktop: boolean;
  crossSellRemoval: boolean;
  crossSell: string[] = CROSSSELL_VALUES;

  constructor(
    protected pubSubService: PubSubService,
    protected visEventService: VisEventService,
    protected windowRefService: WindowRefService,
    protected router: Router,
    protected routingState: RoutingState,
    protected route: ActivatedRoute,
    protected deviceService: DeviceService
  ) { }

  ngOnInit(): void {
    this.isDesktop = this.deviceService.isDesktop;
    this.directiveArr = [];
    this.showMatchCentre = false;

    // If checkForEventsWithAvailableVisualization has already been done for this ID.
    this.lastCheckedId = '0';
    this.isAnotherPage = true;

    this.widgets = this.widgetDataStore;
    this.pubSubService.subscribe(this.crossSell[0], this.crossSell[1], (crossSellRemoval: boolean) => {
      if (crossSellRemoval) {
        this.widgets = this.widgetDataStore.filter((value) => value.directiveName !== this.crossSell[2]);
      } else {
        this.widgets = this.widgetDataStore;
      }
    });

    this.filterData();

    /**
     * Add directive names to Array if there are no events for them
     */
    this.pubSubService.subscribe(this.widgetColumn, this.pubSubService.API.SHOW_WIDGET, widget => {
      if (!widget.data || !widget.data.length) {
        this.directiveArr.push(widget.name);
        this.filterData();
      }
    });

    /**
     * Add directive names to Array if there are no events for them
     */
    this.pubSubService.subscribe(this.widgetColumn, this.pubSubService.API.DISPLAY_WIDGET, widget => {
      this.directiveArr = this.directiveArr.filter((directive: string) => directive !== widget.name);
      this.filterData();
      this.filterRequest(widget);
    });

    if (!this.isDesktop) {
      this.windowRefService.nativeWindow.addEventListener('resize', () => this.updateData());
    }

    this.locationChangeListener = this.router.events.subscribe((event: Event) => {
      if (event instanceof NavigationEnd) {
        this.filterData();
        this.filterRequest();
      }
    });
  }

  ngOnDestroy(): void {
    if (!this.isDesktop) {
      this.windowRefService.nativeWindow.removeEventListener('resize', () => this.updateData());
    }
    if (this.locationChangeListener) {
      this.locationChangeListener.unsubscribe();
    }

    this.pubSubService.unsubscribe(this.widgetColumn);
  }

  /**
   * ngFor trackBy directive name function
   * @param index
   * @param directive
   */
  trackByDirectiveName(index: number, directive: IWidget): string {
    return directive.directiveName;
  }

  isMatchCentreWidget(widget: IWidget): boolean {
    return widget.directiveName === 'match-centre' ? this.showMatchCentre : true;
  }

  /**
   * Check Match-Centre availability
   */
  private filterRequest(widget?: IWidget): void {
    this.isAnotherPage = this.lastCheckedId !== this.routingState.getRouteParam('id', this.route.snapshot);
    if (widget && widget.name === 'match-centre') {
      this.showMatchCentre = false;
    }
    if (this.checkSegmentContainment(['sport', 'eventMain']) && this.isAnotherPage) {
      // Save ID of this page, in order to prevent several requests for the
      // same url, with the same data.
      this.lastCheckedId = this.routingState.getRouteParam('id', this.route.snapshot);
      this.visEventService.checkForEventsWithAvailableVisualization(this.lastCheckedId).pipe(
        concatMap(() => this.visEventService.checkPreMatchWidgetAvailability(this.lastCheckedId)),
        map((arr) => {
          this.showMatchCentre = !!((arr[0] && arr[0].length) || arr[1]);
        }));
    }
  }

  /**
   * Update data if device resize/orientation changed.
   */
  private updateData(): void {
    if (this.deviceType !== this.windowRefService.nativeWindow.deviceType) {
      this.deviceType = this.windowRefService.nativeWindow.deviceType;
      this.filterData();
      this.filterRequest();
    }
  }

  /**
   * Show Column widgets for Devices and hide if no events
   */
  private filterData(): void {
    this.widgets = this.widgets
      .filter((item: IWidget) => this.byColumn(item))
      .filter((item: IWidget) => this.byDevice(item))
      .filter((item: IWidget) => this.byShowOnRules(item));
  }

  private byColumn(widget: IWidget): boolean {
    return widget.columns.includes(this.widgetColumn);
  }

  private byDevice({ publishedDevices, directiveName }: IWidget): boolean {
    const deviceType = this.isDesktop ? 'desktop' : this.windowRefService.nativeWindow.deviceType;
    const devLength = publishedDevices && publishedDevices.length ? publishedDevices.includes(deviceType) : false;

    return this.directiveArr.includes(directiveName) ? false : devLength;
  }

  private byShowOnRules({ showOn }: IWidget): boolean {
    return !showOn || (
      showOn &&
      this.checkSegmentContainment(showOn.routes.split('/')) &&
      this.checkSport(showOn.sports)
    );
  }

  private checkSegmentContainment(array: string[]): boolean {
    const segment = this.routingState.getCurrentSegment();
    return array.every((item: string) => segment.indexOf(item) !== -1);
  }

  private checkSport(sports: string[]): boolean {
    return sports.includes(this.routingState.getRouteParam('sport', this.route.snapshot));
  }
}
