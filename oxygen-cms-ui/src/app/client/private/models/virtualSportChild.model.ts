import {Base} from '@app/client/private/models/base.model';
import {Filename} from '@app/client/public/models/filename.model';

export interface VirtualSportChild extends Base {
  sportId: string;
  title: string;
  active: boolean;
  streamUrl: string;
  classId: string;
  typeIds: string;
  showRunnerNumber: boolean;
  showRunnerImages: boolean;
  runnerImages?: Filename[];
  eventRunnerImages?: { [event: string]: Filename[] };
  numberOfEvents: number;
}

export interface RemoveImageRequest {
  type: string;
  event?: string;
  filename?: string;
}

export enum RemoveImageRequestType {
  ALL_FOR_EVENT,
  SINGLE_FOR_EVENT,
  SINGLE_FOR_TRACK
}
