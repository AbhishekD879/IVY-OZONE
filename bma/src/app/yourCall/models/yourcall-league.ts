import { IYourcallDsEventResponse } from '@yourcall/models/ds-events-response.model';

interface IYourcallLeagueOptions {
  byb?: boolean;
  id?: number;
}

export class YourCallLeague {
  obTypeId: number;
  title: string;
  status: number;
  ds: boolean;
  byb: boolean;
  id: number;
  expanded: boolean;
  forceExpand: boolean;
  isCustomVisible: boolean;

  normilized: boolean = false;
  categoryId: number = null;
  categoryName: string  = null;
  className: string  = null;
  typeName: string  = null;
  events: IYourcallDsEventResponse[];
  eventsLoaded: boolean = false;

  constructor(obTypeId, title, status = 1, options: IYourcallLeagueOptions = { byb: false, id: null }) {
    this.obTypeId = obTypeId;
    this.title = title;
    this.status = status;
    this.byb = options.byb;
    this.id = options.id;
  }
}
