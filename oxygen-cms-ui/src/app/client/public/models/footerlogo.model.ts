import {SvgFilename} from './svgfilename.model';
import {Filename} from './filename.model';

export interface FooterLogo {
  id: string;
  sortOrder: number;
  title: string;
  target: string;
  disabled: boolean;
  lang: string;
  brand: string;
  svg: string;
  svgId: string;
  uriMedium: string;
  uriOriginal: string;
  svgFilename: SvgFilename;
  filename: Filename;
}
