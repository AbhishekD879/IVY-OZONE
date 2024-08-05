import { IVirtualChild, IVirtualSports } from '@core/services/cms/models/virtual-sports.model';
import { ISportEventEntity } from '@core/models/sport-event-entity.model';

export interface ICategoryAliases {
  parentAlias: string;
  childAlias: string;
}

export interface IVirtualChildCategory extends IVirtualChild {
  alias: string;
  targetUri?: string;
  timeLeft?: number;
  startTimeUnix?: number;
  events?: ISportEventEntity[];
  typeIds?: string;
}

export interface IVirtualCategoryStructure extends IVirtualSports {
  alias?: string;
  targetUri?: string;
  childs?: Map<string | number, IVirtualChildCategory>;
}
