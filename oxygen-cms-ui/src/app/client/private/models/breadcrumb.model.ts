import { SportsModule } from '@app/client/private/models/homepage.model';
import { IEventHub } from '@app/sports-pages/event-hub/models/event-hub.model';
import { SportCategory } from '@app/client/private/models/sportcategory.model';

export interface Breadcrumb {
  label: string;
  url?: string;
}

export interface IBreadcrubmBuildParams {
  eventhub?: IEventHub;
  sportConfig?: SportCategory;
  module?: SportsModule;
  customBreadcrumbs?: Breadcrumb[];
}
