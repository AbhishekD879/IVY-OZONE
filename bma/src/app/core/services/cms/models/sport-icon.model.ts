import { IProcessedRequestModel } from './process-request.model';

export interface ISportIcon extends IProcessedRequestModel {
  svg: string;
  svgId: string;
}
