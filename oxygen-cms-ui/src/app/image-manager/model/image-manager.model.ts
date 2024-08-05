import { Base } from '@app/client/private/models/base.model';
import { Filename } from '@app/client/public/models';

export interface IImageData extends Base {
  active: boolean;
  imageManagerSvg: string;
  sprite: string;
  imageSize: number | string;
  preview?: string;
  svgId: string;
  svg: string;
  svgFilename: Filename;
}
