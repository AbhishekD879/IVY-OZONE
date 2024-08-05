import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { InspiredVirtualService } from './inspired-virtual.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { TempStorageService } from '@core/services/storage/temp-storage.service';
import { VirtualSharedService } from '@shared/services/virtual/virtual-shared.service';
import { from, Subscription } from 'rxjs';
import { ISportConfigTab } from '@app/core/services/cms/models/sport-config-tab.model';
import { VirtualEntryPointsService } from '@app/racing/services/virtual-entry-points.service';

@Component({
  selector: 'inspired-virtual-module',
  templateUrl: 'inspired-virtual.component.html'
})
export class InspiredVirtualComponent implements OnInit, OnDestroy {
  @Input() widget?: boolean;
  @Input() virtualsTitle: string;
  @Input() eventsData: Partial<ISportEvent>[];
  @Input() sportName: string;
  @Input() isVirtualHomePage:boolean;
  @Input() IsOnlyNextEventEnabled: boolean;

  eventsArray: ISportEvent[];
  isHovered = false;
  carouselName: string = 'inspired-virtual';
  isFirstTimeCollapsed: boolean = false;
  isExpanded: boolean;

  bannerBeforeAccorditionHeader : string = '';
  targetTab: ISportConfigTab | null = null;

  protected SECTION_FLAG: string = 'VRC';
  private loadDataSubscription: Subscription;

  constructor(
    protected inspiredVirtualService: InspiredVirtualService,
    protected router: Router,
    protected storage: TempStorageService,
    protected virtualSharedService: VirtualSharedService,
    protected vEPService : VirtualEntryPointsService
  ) {
    this.carouselName = 'inspired-virtual';
    this.isFirstTimeCollapsed = false;
  }

  ngOnInit(): void {
    const expandedState = this.storage.get(this.SECTION_FLAG);
    this.isExpanded = expandedState !== undefined ? this.storage.get(this.SECTION_FLAG) : true;

    if (this.eventsData[0] && this.eventsData[0].name === 'VRC') {
      this.loadDataSubscription = from(this.inspiredVirtualService.getEvents()).subscribe(data => {
        this.eventsArray = data;
      });
    } else {
      this.eventsArray = this.inspiredVirtualService.setupEvents(this.eventsData);
    }

    if((!this.eventsArray || (this.eventsArray && this.eventsArray.length == 0)) && this.isVirtualHomePage && this.IsOnlyNextEventEnabled) {
      this.router.navigate(['virtual-sports/sports']);
    }

    this.vEPService.bannerBeforeAccorditionHeader.subscribe((header: string) => {
      this.bannerBeforeAccorditionHeader = header;
    });
    this.vEPService.targetTab.subscribe((tab: ISportConfigTab | null) => {
      this.targetTab = tab;
    });
  }

  /**
   * ngFor trackBy function
   * @param {number} index
   * @param {ISportEvent} event
   * @return {string}
   */
  trackById(index: number, event: ISportEvent): string {
    return `${index}${event.id}`;
  }

  /**
   * Send GA on first collapse
   */
  sendCollapseGTM(): void {
    this.storage.set(this.SECTION_FLAG, !this.isExpanded);
    if (!this.isFirstTimeCollapsed) {
      this.inspiredVirtualService.sendGTMOnFirstTimeCollapse(this.sportName);
      this.isFirstTimeCollapsed = true;
    }
  }

  /**
   * Go to all HR Virtuals
   */
  viewAllVirtual(event: ISportEvent): void {
    const url = event ? this.virtualSharedService.formVirtualTypeUrl(event.classId) : 'virtual-sports/sports';
    this.router.navigateByUrl(url);
  }

  /**
   * Go to Live Virtual sport event
   */
  goToLiveEvent(event: ISportEvent): void {
    const url =  event ? this.virtualSharedService.formVirtualEventUrl(event) : 'virtual-sports/sports';
    if (this.isVirtualHomePage) {
      this.inspiredVirtualService.virtualsGTMEventTracker(url, event);
    } else {
      this.inspiredVirtualService.sendGTMOnGoToLiveEvent(this.sportName);
    }
    this.router.navigateByUrl(url);
  }

  /**
   * Get data format in hh:mm
   * @params {number} startTime(timestamp)
   */
  getStartTime(startTime: number): string {
    return this.inspiredVirtualService.getStartTime(startTime);
  }

  /**
   * onDestroy component
   */
  ngOnDestroy(): void {
    this.inspiredVirtualService.destroyTimers();
    if (this.loadDataSubscription) {
      this.loadDataSubscription.unsubscribe();
    }
  }


  isDisplayBanner(name) {
    return this.bannerBeforeAccorditionHeader?.toLowerCase() === name?.toLowerCase();
  }

}
