import {SvgFilename} from './svgfilename.model';
import {Filename} from './filename.model';
import { Base } from './base.model';

export interface FooterLogo extends Base {
  id: string;
  sortOrder: number;
  title: string;
  target: string;
  disabled: boolean;
  lang: string;
  svg: string;
  svgId: string;
  uriMedium: string;
  uriOriginal: string;
  svgFilename: SvgFilename;
  filename: Filename;
}
