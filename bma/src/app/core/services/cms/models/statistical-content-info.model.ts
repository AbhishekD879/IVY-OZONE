import { IBase } from './base.model';
export interface IStatisticalContent extends IBase {
  content: string;
  title: string;
  marketType:string;
  eventId:string;
  marketId:string;
  startTime:string;
  endTime:string;
  enabled:boolean;
  marketDescription:string;
}
export enum EnumStatisticalFlags {
  'bma_MKTFLAG_PB' = 'OB',
  'bma_MKTFLAG_PR1' = 'BMOB',
  'ladbrokes_MKTFLAG_PB' = 'PB',
  'ladbrokes_MKTFLAG_PR1' = 'SPB'
}