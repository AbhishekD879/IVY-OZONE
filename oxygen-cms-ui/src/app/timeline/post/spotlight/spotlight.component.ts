import { Component, Input, OnInit, Output, EventEmitter, OnChanges, SimpleChanges } from '@angular/core';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { ActivatedRoute, Router } from '@angular/router';
import { PostApiService } from '@app/timeline/service/post-api.service';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { CampaignApiService } from '@app/timeline/service/campaign-api.service';
import { Campaign } from '@app/client/private/models/campaign.model';

import { SpotlightApiService } from '@app/timeline/service/spotlight-api.service';
import { SpotlightPerTypeEventData } from '@app/client/private/models/spotlightPerTypeEventData.model';
import { SpotlightEvent } from '@app/client/private/models/spotlightEvent.model';
import { SpotlightItem } from '@app/client/private/models/spotlightItem.model';
import { VerdictItem } from '@app/client/private/models/verdictItem.model';
import { FreeRideConstants } from '@root/app/app.constants';
import { PotCreation, PotCreationMarket } from '@root/app/client/private/models/freeRideCampaign.model';
import * as _ from 'lodash';


@Component({
  selector: 'spotlight',
  templateUrl: './spotlight.component.html',
  styleUrls: ['./spotlight.component.scss']
})
export class SpotlightComponent implements OnInit, OnChanges {
  /* For FreeRide */
  @Input() isFreeRidePot?: boolean = false;
  @Input() campaignEventData?;
  @Input() isPotsCreated?: boolean = false;
  @Input() isvalidDate?: boolean = true;
  @Input() dataChanged?: boolean = false;
  @Output() emitSelectedRaces = new EventEmitter<PotCreation>();
  @Output() emitCreatePotsEvent = new EventEmitter<boolean>();
  eventSeleted: boolean[];
  readonly freeRideConstants = FreeRideConstants;
  activeRaceArr: PotCreationMarket[] = [];
  selSingleEvent: boolean[][];

  public breadcrumbsData: Breadcrumb[];
  campaign: Campaign;
  searchField: string = '';
  getDataError: string;
  campaignId: string = '';
  spotlightRelatedEventsData: SpotlightPerTypeEventData;
  activeEvent: SpotlightEvent;
  spotlights: SpotlightItem[];
  verdict: VerdictItem;
  refreshEventsFrom: string = new Date().toISOString();
  private readonly DEFAULT_CLASS_IDS_STRING = '226';
  refreshEventsClassesString: string;
  restrictToUkAndIre: boolean = true;
  LOCAL_STORAGE_EVENT_ID_KEY = 'spotlight_event_id';
  LOCAL_STORAGE_CLASS_IDS_KEY = 'spotlight_class_ids';
  EVENT_TIME_FORMATTING_OPTIONS = { timeZone: 'Europe/London', hour: '2-digit', minute: '2-digit' };

  constructor(private dialogService: DialogService,
    private postApiService: PostApiService,
    private spotlightApiService: SpotlightApiService,
    private campaignApiService: CampaignApiService,
    private router: Router,
    private route: ActivatedRoute) { }

  ngOnInit() {
    this.refreshEventsClassesString = localStorage.getItem(this.LOCAL_STORAGE_CLASS_IDS_KEY);
    if (!this.refreshEventsClassesString) {
      this.refreshEventsClassesString = this.DEFAULT_CLASS_IDS_STRING;
    }
    if (!this.isFreeRidePot) {
      this.campaignId = this.route.snapshot.paramMap.get('campaignId');
      this.campaignApiService.getCampaign(this.campaignId).subscribe((campaign: any) => {
        this.campaign = campaign.body;
        this.breadcrumbsData = [{
          label: `Campaigns`,
          url: `/timeline/campaign`
        }, {
          label: `${this.campaign.name}`,
          url: `/timeline/campaign/edit/${this.campaignId}`
        }, {
          label: 'Spotlight',
          url: `/timeline/post/spotlight/by-campaign/${this.campaignId}`
        }];
      });
    }
    this.getRelatedEvents();
  }

  ngOnChanges(changes: SimpleChanges) {
    console.log(changes);
  }

  getRelatedEvents() {
    this.spotlightApiService.getSiteServeEvents(this.refreshEventsFrom,
      this.refreshEventsClassesString, this.restrictToUkAndIre, this.isFreeRidePot).subscribe(data => {
        this.spotlightRelatedEventsData = data.body;
        this.addProperTimeFormat();
        const eventIdStored = localStorage.getItem(this.LOCAL_STORAGE_EVENT_ID_KEY);
        if (eventIdStored && !this.isFreeRidePot) {
          for (const typeEventGroup of this.spotlightRelatedEventsData.typeEvents) {
            for (const event of typeEventGroup.events) {
              if (event.id === eventIdStored) {
                this.activeEvent = event;
                this.handleClickOnEvent(event, 0, null, 0);
                break;
              }
            }
          }
        }
      }, err => {

      }, () => {
        if (this.isFreeRidePot) {
          this.eventSeleted = new Array(this.spotlightRelatedEventsData.typeEvents.length).fill(false);
          this.filterFreeRideSelectedRace(this.spotlightRelatedEventsData);
        }
      });
  }

  private addProperTimeFormat() {
    for (const typeEventGroup of this.spotlightRelatedEventsData.typeEvents) {
      for (const event of typeEventGroup.events) {
        event.startTimeUkFormattedString =
          new Date(event.startTime).toLocaleTimeString('en-GB', this.EVENT_TIME_FORMATTING_OPTIONS);
      }
    }
  }

  refreshSpotlightData() {
    this.spotlights = [];
    this.activeEvent = undefined;
    this.verdict = undefined;
    localStorage.removeItem(this.LOCAL_STORAGE_EVENT_ID_KEY);
    this.spotlightApiService.getSiteServeEvents(this.refreshEventsFrom,
      this.refreshEventsClassesString, this.restrictToUkAndIre, this.isFreeRidePot).subscribe(data => {
        this.spotlightRelatedEventsData = data.body;
        if (this.isFreeRidePot) {
          this.activeRaceArr = [];
          if (this.campaignEventData && this.campaignEventData.marketPlace) {
            this.campaignEventData.marketPlace = [];
          }
          this.spotlightRelatedEventsData.typeEvents.map((race: any, i: number) => {
            this.selSingleEvent[i] = Array(race?.events.length).fill(false);
          });
          this.eventSeleted = Array(this.spotlightRelatedEventsData.typeEvents.length).fill(false);
        }
        this.addProperTimeFormat();
        localStorage.setItem(this.LOCAL_STORAGE_CLASS_IDS_KEY, this.refreshEventsClassesString);
          if (data.body && data.body.typeEvents.length) {
            this.dialogService.showNotificationDialog({
              title: 'Events data re-fetched',
              message: 'Successfully re-fetched Spotlight-related events from SiteServe!'
            });
          } else {
            this.dialogService.showNotificationDialog({
              title: 'Events data re-fetched',
              message: 'No events found!'
            });
          }
      });
  }

  handleClickOnEvent(event: any, i: number, raceData: any, j: number) {
    if (!this.isFreeRidePot) {
      this.activeEvent = event;
      this.spotlightApiService.getSpotlightsForEventId(event.id, this.campaignId).subscribe(data => {
        this.spotlights = data.body.horses;
        if (data.body.verdict && data.body.raceName) {
          this.verdict = { verdict: data.body.verdict, raceName: data.body.raceName };
        } else {
          this.verdict = undefined;
        }
      });
      localStorage.setItem(this.LOCAL_STORAGE_EVENT_ID_KEY, event.id);
    } else {
      this.handleClickOnEventFreeRide(event, i, raceData, j);
    }
  }

  createSpotlightPost(spotlightInfo) {
    this.router.navigateByUrl(`/timeline/post/by-campaign/${this.campaignId}/create`);
    this.postApiService.currentSpotlightData = {
      name: `[spotlight]${spotlightInfo.horseName}|${new Date().toUTCString()}`,
      headerText: spotlightInfo.horseName,
      text: spotlightInfo.spotlight,
      selectionId: spotlightInfo.selectionId,
      spotlightDetails: {
        dataType: 'spotlight',
        rpHorseId: spotlightInfo.rpHorseId,
        eventId: this.activeEvent.id,
        typeId: this.activeEvent.typeId,
      },
    };
  }

  createVerdictPost(verdictInfo) {
    this.router.navigateByUrl(`/timeline/post/by-campaign/${this.campaignId}/create`);
    this.postApiService.currentSpotlightData = {
      name: `[verdict]${verdictInfo.raceName}|${new Date().toUTCString()}`,
      headerText: verdictInfo.raceName,
      text: verdictInfo.verdict,
      spotlightDetails: {
        dataType: 'verdict',
        eventId: this.activeEvent.id,
        typeId: this.activeEvent.typeId,
      },
    };
  }

  handleEntryDeadline(date: any) {
    this.refreshEventsFrom = new Date(date).toISOString();
  }

  /*
    Selection handling for free ride campaign pots creation on load
    */
  filterFreeRideSelectedRace(raceEventDat) {
    this.activeRaceArr = [];
    this.selSingleEvent = Array(raceEventDat.typeEvents.length).fill(false);
    raceEventDat.typeEvents.map((race: any, i: number) => {
      const j = this.campaignEventData?.marketPlace.findIndex(id => id.typeId === race.typeId);
      this.selSingleEvent[i] = Array(race?.events.length).fill(false);
      if (j > -1) {
        if (this.campaignEventData.marketPlace[j].events.length === race.events.length) {
          this.eventSeleted[i] = !this.eventSeleted[i];
          this.activeRaceArr.push(this.campaignEventData.marketPlace[j]);
          this.selSingleEvent[i] = Array(race.events.length).fill(true);
        } else {
          this.activeRaceArr[i] = ({ 'typeId': this.campaignEventData.marketPlace[j].typeId, 'typeName': this.campaignEventData.marketPlace[j].typeName, 'events': [] }); // Setting initial state of race array to make events slected only
          this.campaignEventData.marketPlace[j].events.filter((element) => {
            if (race.events.some(eveId => eveId.id === element.id)) { // removing expired events and adding selected events to racearray
              this.activeRaceArr[i].events.push({ 'id': element['id'], 'name': element['name'] });
              this.eventSeleted[i] = this.activeRaceArr[i].events.length === race.events.length ? true : false;
              this.selSingleEvent[i][race.events.findIndex((eve: any) => eve.id === element.id)] = true;
            }
          });
        }
      }
    });
    this.emitRaceDetails(this.activeRaceArr);
  }

  handleClickOnEventFreeRide(event: any, i: number, raceEvent: any, j: number) {
    if (this.isPotsCreated) {
      return false;
    } else {
      const iRace = this.activeRaceArr.findIndex(id => id?.typeId === raceEvent.typeId);
      if (iRace === -1) {
        this.activeRaceArr.push({ 'typeId': raceEvent.typeId, 'typeName': raceEvent.typeName, 'events': [{ 'id': event['id'], 'name': event['name'] }] });
        this.selSingleEvent[j][i] = true;
      } else {
        if (this.activeRaceArr[iRace].events.some(eve => eve.id === event.id)) {// remove event if already selected as deselected now
          this.activeRaceArr[iRace].events.splice(this.activeRaceArr[iRace].events.findIndex(eve => eve.id === event.id), 1);
          this.eventSeleted[j] = this.activeRaceArr[iRace].events.length === raceEvent.events.length ? true : false;
          this.activeRaceArr = this.activeRaceArr[iRace].events.length === 0 ? this.activeRaceArr.splice(iRace, 1) : this.activeRaceArr; // remove entire race if last event removed
          this.selSingleEvent[j][i] = false;
        } else {// add event to race obj if not present n now selected
          this.activeRaceArr[iRace].events.push({ 'id': event['id'], 'name': event['name'] });
          this.eventSeleted[j] = this.activeRaceArr[iRace].events.length === raceEvent.events.length ? true : false;
          this.selSingleEvent[j][i] = true;
        }
      }
      this.emitRaceDetails(this.activeRaceArr);
    }
  }


  getSelectedEvent(event: any, i?: number) {
    if (typeof (i) !== 'number') {
      const selectAll = this.eventSeleted.some((selEvt) => selEvt === false);
      event.forEach((evt, i) => {
        if (selectAll) {
          this.activeRaceArr = this.activeRaceArr.filter(raceData => {
            return raceData.typeId !== evt.typeId;
          });
          this.activeRaceArr.push({ 'typeId': evt.typeId, 'typeName': evt.typeName, 'events': this.formEventObj(evt.events) });
          this.eventSeleted[i] = true;
          this.selSingleEvent[i] = Array(event.length).fill(true);
        } else {
          this.activeRaceArr = [];
          this.eventSeleted[i] = false;
          this.selSingleEvent[i] = Array(event.length).fill(false);
        }
      });
    } else {
      if (!this.eventSeleted[i]) { // No event present and nothing selected
        this.activeRaceArr = this.activeRaceArr.filter(raceData => {
          return raceData.typeId !== event.typeId;
        }); // only if event selected remove and replace entire race
        this.eventSeleted[i] = !this.eventSeleted[i];
        this.activeRaceArr.push({ 'typeId': event.typeId, 'typeName': event.typeName, 'events': this.formEventObj(event.events) });
        this.selSingleEvent[i] = Array(event.events.length).fill(true);
      } else { // entire row deselect
        this.activeRaceArr.splice(this.activeRaceArr.findIndex(eve => event.typeId === eve.typeId), 1);
        this.eventSeleted[i] = !this.eventSeleted[i];
        this.selSingleEvent[i] = Array(event.events.length).fill(false);
      }
    }
    this.emitRaceDetails(this.activeRaceArr);
  }

  emitRaceDetails(data) {
    const raceData: PotCreation = {
      classId: null,
      marketPlace: [],
      categoryId: null
    };
    raceData.classId = Number(this.refreshEventsClassesString);
    raceData.categoryId = Number(this.spotlightRelatedEventsData.typeEvents[0]?.events[0].categoryId);
    raceData.marketPlace = data.filter(val => val !== null);
    this.emitSelectedRaces.emit(raceData);
  }

  formEventObj(arr: any) {
    console.log(arr);
    return arr.map((ar: any) => {
      return { 'id': ar['id'], 'name': ar['name'] };
    });
  }

  createCampaignLevelPots() {
    this.emitCreatePotsEvent.emit(true);
  }
}


