import { Input, Output, EventEmitter, Component, OnChanges, OnInit } from '@angular/core';

import { LocaleService } from '@core/services/locale/locale.service';
import { TempStorageService } from '@core/services/storage/temp-storage.service';

import { IRaceGridMeeting } from '@core/models/race-grid-meeting.model';
import { RacingService } from '@coreModule/services/sport/racing.service';
import { ISportConfigTab } from '@app/core/services/cms/models/sport-config-tab.model';
import { VirtualEntryPointsService } from '@app/racing/services/virtual-entry-points.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { DeviceService } from '@core/services/device/device.service';

@Component({
  selector: 'racing-events',
  templateUrl: './racing-events.component.html'
})
export class RacingEventsComponent implements OnChanges,OnInit {
  @Input() sportName: string;
  @Input() racing: IRaceGridMeeting;
  @Input() byTimeEvents;
  @Input() eventsOrder: string[];
  @Input() filter?: string;
  @Input() sectionTitle: Object;
  @Input() moduleTitle: string;
  @Input() display?: string;
  @Input() filterDay?:string;
  @Input() showSwitcher?: boolean = true;
  @Input() isEventOverlay?: boolean;
  @Input() showSignPost: boolean = false;
  @Input() quickNavigationTitles: {[key: string]: string};
  @Input() racingIndex: number;
  @Output() readonly gaTracking = new EventEmitter();
  bannerBeforeAccorditionHeader: string= '';
  targetTab: ISportConfigTab | null = null;
  lastBannerEnabled:boolean;
  accorditionNumber:number;

  titleMap: {[key: string]: string} = {};
  accordionsState: {[key: string]: boolean} = {};

  constructor(private locale: LocaleService, private storage: TempStorageService,
    protected racingService: RacingService, private windowRef: WindowRefService,
    protected gtm: GtmService, protected deviceService: DeviceService, protected vEPService : VirtualEntryPointsService) {
    }

  ngOnInit() {
    this.vEPService.lastRacingModuleIndex = this.racingIndex
    this.vEPService.bannerBeforeAccorditionHeader.subscribe((header: string) => {
      this.bannerBeforeAccorditionHeader = header;
    });

    this.vEPService.targetTab.subscribe((tab: ISportConfigTab | null) => {
      this.targetTab = tab;
    });
     
    this.lastBanner();
  
    this.vEPService.accorditionNumber.subscribe((accNum: number) => {
      this.accorditionNumber = accNum;
    });
  }
  
  ngOnChanges(change): void {
    if (change['moduleTitle']) {
      const moduleTitle = change['moduleTitle'].currentValue;
        this.racing && this.racing.groupedRacing.forEach((group) => {
          if (!this.showSwitcher) {
            this.titleMap = this.quickNavigationTitles;
            this.overlayAccordionHandler(group);
          } else {
            const isInStorage = this.storage.get(group.flag) !== undefined;
  
            this.accordionsState[group.flag] = isInStorage ? this.storage.get(group.flag) : true;
    
            if (group.flag === 'UK' || group.flag === 'INT' || group.flag === 'VR') {
              this.titleMap[group.flag] = moduleTitle;
            } else {
              this.titleMap[group.flag] = this.locale.getString(this.sectionTitle[group.flag]);
            }
          }
        });
    }

    if (change['racing']) {
      this.racing && this.racing.groupedRacing.forEach((group) => {
        group.data = this.racingService.filterRacingGroup(group.data);
        if (!this.showSwitcher) {this.overlayAccordionHandler(group);}
      });
    }
    //Added this logic for EDP meetings dropdown accordion handling
    if (this.isEventOverlay) {
      if(this.sportName === 'greyhound' && !this.filter) {
        this.filter = 'by-meeting';
      }
      if(this.deviceService.isDesktop ) {
        this.accordionsState[this.racing.groupedRacing[0].flag] = true;
      }
    }
  }

  lastBanner(){
    this.vEPService.lastBannerEnabled.subscribe((lbe: boolean) => {
      if(this.vEPService.lastRacingModuleIndex === this.racingIndex) {
        this.lastBannerEnabled = lbe;
      } else {
        this.lastBannerEnabled = false;
      }
    });
  }

  overlayAccordionHandler(group) {
      const storedValue = this.storage.get(`overlay-${this.sportName}-`+group.flag);
      const isInStorage = storedValue !== undefined;
      //Added isEventOverlay condition for EDP meetings dropdown accordion to close all by deault except one
      this.accordionsState[group.flag] = this.isEventOverlay && this.deviceService.isDesktop ? false : isInStorage ? storedValue : true;
  }

  trackModule(flag, moduleName) {
    const currentAccState = !this.accordionsState[flag];
    //Added this logic for EDP meetings dropdown  accordion handling
    if(this.isEventOverlay && this.deviceService.isDesktop) {
    Object.keys(this.accordionsState).forEach((type)=>{
      this.accordionsState[type] = (type === flag) ? !this.accordionsState[type] : false;
    })
    this.windowRef.nativeWindow.scrollTo(0, 100);
    }
    this.showSwitcher ? this.storage.set(flag, currentAccState) : this.storage.set(`overlay-${this.sportName}-`+flag, currentAccState);
    const overlayModule = (moduleName === 'horseracing') ? 'horse racing' : 'greyhounds';
    const listedData = this.isEventOverlay ? [overlayModule, this.accordionsState, flag, this.titleMap] : [this.sectionTitle[flag], moduleName];
    this.gaTracking.emit(listedData);
  }

  isDisplayBanner(name: string): boolean {
    return this.bannerBeforeAccorditionHeader?.toLowerCase() === name?.toLowerCase();
  }
}
