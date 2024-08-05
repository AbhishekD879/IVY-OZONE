import { Base } from "@root/app/client/private/models/base.model";

export interface BybWidget extends Base {
  title: string;
  marketCardVisibleSelections: number;
  showAll: boolean;
  createdByUserName: any;
  updatedByUserName: any;
  data: []

}

export interface data extends Base {
  title: string;
  eventId: number;
  marketId: number;
  displayFrom: any;
  displayTo: any;
  locations: []
}


export interface bybwidgetData extends Base{
  title: string;
  eventId: number;
  marketId: number;
  displayFrom: any;
  displayTo: any;
  locations: []
  displayFrom1: string;
  displayTo1: string;
  fromTime: string;
  toTime: string;
  saved: boolean;
  showDate: boolean;
  fromdateChange: boolean;
  todateChange: boolean;
}

