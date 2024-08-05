import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { IRaceGridMeeting } from '@app/core/models/race-grid-meeting.model';
import { ISwitcherConfig } from '@app/core/models/switcher-config.model';
import { HorseracingService } from '@coreModule/services/racing/horseracing/horseracing.service';
import { HandleLiveServeUpdatesService } from '@app/core/services/handleLiveServeUpdates/handle-live-serve-updates.service';
import { CommandService } from '@core/services/communication/command/command.service';
import * as _ from 'underscore';
import { ITab } from '@app/core/models/tab.model';
import { AbstractOutletComponent } from '@app/shared/components/abstractOutlet/abstract-outlet.component';
import { GtmService } from '@coreModule/services/gtm/gtm.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DeviceService } from '@core/services/device/device.service';
import { NEXT_RACES_HOME_CONSTANTS } from '@app/lazy-modules/lazyNextRacesTab/constants/next-races-home.constants';
@Component({
  selector: 'racing-overlay-content',
  templateUrl: './racing-overlay-content.component.html',
  styleUrls: ['./racing-overlay-content.component.scss']
})
export class RacingOverlayContentComponent extends AbstractOutletComponent implements OnInit, OnChanges {

  @Input() racing: IRaceGridMeeting;
  @Input() sectionTitle: Object;
  @Input() responseError?;
  @Input() sportName: string;
  @Input() filter: string;
  @Input() display?: string;
  @Input() showMenu?: boolean;
  @Input() sportModule: string;
  @Input() displayNextRaces: boolean;
  @Input() showSwitcher?: boolean = true;
  @Input() isExtraPlaceAvailable: boolean;
  @Input() isEventOverlay?: boolean = false;
  @Input() offersAndFeaturedRacesTitle: string;
  @Input() items:any[];
  @Input() eventsOrder: string[];
  @Input() allEvents:ISportEvent[] = [];
  @Input() quickNavigationTitles: {[key: string]: string};
  @Input() eventEntity: ISportEvent;
  @Input() isEntityChanged: boolean = false;
  @Input() overlayContentData: ISportEvent[] = [];
  switchers: ISwitcherConfig[] | ITab[] | any = [];
  noEvents: boolean = false;
  liveServeChannels: any = [];
  raceMeetings: IRaceGridMeeting;
  isOverlayVisible:boolean = false;
  offersAndFeaturesEvents: ISportEvent[] = [];
  activeTab: string = 'racing.today';
  dayValueText: string = '';
  nextRacesDataLoaded: boolean = false;
  constructor(
    private horseRacingService: HorseracingService,
    private command: CommandService,
    private liveServeHandleUpdatesService: HandleLiveServeUpdatesService,
    private gtmService: GtmService,
    private locale: LocaleService,
    private windowRef: WindowRefService,
    protected deviceService: DeviceService
    ) {
      super();
    }

  ngOnInit() {
    this.dayValueText = this.sportModule == 'horseracing' ? 'correctedDayValue' : 'correctedDay';
    this.activeTab = this.eventEntity[this.dayValueText];
    // Opening connection to liveserve publisher.
    this.liveServeHandleUpdatesService.subscribe([], () => {});
    this.filterOffersAndFeatures();
    this.createSwitchers();
    //TODO for desktop added this conditon to load overlay
    this.nextRacesDataLoaded = this.deviceService.isDesktop;
    this.selectDay(this.activeTab, true);
  }

  ngOnChanges(changes: SimpleChanges) {
    this.showMenuHandler(changes);
  }

  showMenuHandler(changes) {

    if (changes.showMenu?.currentValue) {
      if(this.isEntityChanged) {
        this.ngOnInit();
      }
      !this.deviceService.isDesktop &&  this.windowRef.nativeWindow.setTimeout(() => {
        const elem = document.querySelector('.quick-section');
        elem.scrollIntoView();
      },100);
    } else if(changes.showMenu && !changes.showMenu.currentValue){ 
      this.nextRacesDataLoaded = this.deviceService.isDesktop;
     }
  }

  filterOffersAndFeatures() {
    if(this.overlayContentData?.length) {
      this.offersAndFeaturesEvents = this.overlayContentData.slice();
    }
  }
  // Display switchers on top common for all the events in horse racing overlay.
  protected createSwitchers(): void {
    // displaying first two days irrespective of the data received.
    this.switchers = [];
    let uniqDays = [];
    if(this.overlayContentData && this.overlayContentData.length) {
      uniqDays = _.chain(this.overlayContentData).sortBy('startTime').pluck(this.dayValueText).uniq().value();
    }
    uniqDays = _.uniq([...uniqDays]).slice(0,3);
    this.switchers = [];
    _.each(uniqDays, (day: string) => {
      this.switchers.push({
        id: day,
        name: day,
        onClick: () => this.selectDay(day),
        viewByFilters: day,
        selected: day == this.activeTab
      });
    });
  }

  selectDay(day: string, skipDayGTM? : boolean): void {
    this.activeTab = day;
    this.noEvents = false;
    this.getRacesDataOnDayChange(day, skipDayGTM); 
  }


  getRacesDataOnDayChange(day, skipDayGTM? : boolean) {
    !skipDayGTM && this.gtmTrackingForDaySwitcher(day);
    this.isOverlayVisible = false;
    const events = this.overlayContentData ? this.overlayContentData.filter(res => res[this.dayValueText] == day) : [];
    if (events.length == 0) {
      this.noEvents = true;
      this.isOverlayVisible = true;
    }
    const races = this.horseRacingService.groupByFlagCodesAndClassesTypeNames(events) as any;
    /*
    * filtering data based upon selected day as buttons are common for all meetings.
    */
    this.raceMeetings = this.modifyRacesData(races);
  }

  gtmTrackingForDaySwitcher(day) {
    this.gtmService.push('trackEvent', {
      eventCategory: this.sportModule == 'horseracing' ? NEXT_RACES_HOME_CONSTANTS.HORSE_RACING_LOWERCASE : NEXT_RACES_HOME_CONSTANTS.GREYHOUNDS_LOWERCASE,
      eventAction: 'meetings',
      eventLabel: this.locale.getString(day)
    });
  }

  modifyRacesData(races) {
    if (races?.groupedRacing?.length) {
      races.groupedRacing.forEach(sportEvent => {
        if(sportEvent.data && sportEvent.data.length) {
          sportEvent.data = sportEvent.data.filter((race: ISportEvent) => {
            return race[this.dayValueText] === this.activeTab;
          });
        }
      });
      this.formLiveChannels(races.groupedRacing);
    }
    this.isOverlayVisible = true;
    return races;
  }

  private formLiveChannels(data) {
    if(this.liveServeChannels.length) {
      this.liveServeHandleUpdatesService.unsubscribe(this.liveServeChannels);
      this.liveServeChannels = [];
    }
    const sportEventsList = data.reduce((prev, cur)=>prev.concat(cur.data), []);
    sportEventsList.forEach(res => res.liveServChannels = res.liveServChannels.split(',')[0]);
    this.liveServeChannels = _.chain(sportEventsList).pluck('liveServChannels').uniq().value();
  }

  nextRacesLoaded() {
    this.windowRef.nativeWindow.setTimeout(() => {
      this.nextRacesDataLoaded = true;
    },175);
  }

  ngOnDestroy(): void {
    if(this.liveServeChannels.length) {
      this.liveServeHandleUpdatesService.unsubscribe(this.liveServeChannels);
    }
  }
  /**
   * Triggered whenever there is change in overlay toggle
   */
  trackModule(sportName: string, accordionsState: {[key: string]: string}, flag: string, titleMap: {[key: string]: string}): void {
    //Added this logic for EDP meetings dropdown  accordion handling
    const accordionStatus = accordionsState[flag] ? 'expand': 'collapse';
    const gtmData = {
      'event': 'trackEvent',
      'eventAction': 'meetings',
      'eventCategory': sportName,
      'eventLabel': accordionStatus,
      'eventDetails': titleMap[flag]
    }
    this.gtmService.push(gtmData.event, gtmData);
  }
}
