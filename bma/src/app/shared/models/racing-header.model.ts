import { IBreadcrumb } from './breadcrumbs.model';
import { IGroupedSportEvent, ISportEvent } from '@core/models/sport-event.model';

export interface IRacingHeader {
    breadCrumbs: IBreadcrumb[];
    quickNavigationItems: IGroupedSportEvent[];
    eventEntity: ISportEvent;
    meetingsTitle: {[key: string]: string;};
    sportEventsData: ISportEvent[];
    isMarketAntepost: boolean;
}
