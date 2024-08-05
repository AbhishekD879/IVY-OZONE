import { IStructureData } from '@app/inPlay/models/structure.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IRibbonData } from '@app/inPlay/models/ribbon.model';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';

export type IResponseData = ISportEvent[] | IRibbonData | ISportSegment | IStructureData;
