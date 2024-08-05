import {Base} from '@app/client/private/models/base.model';
import {SvgFilename} from '@app/client/private/models/svgfilename.model';

export interface OnBoardingGuide extends Base {
  svgFilename: SvgFilename;
  guideName: string;
  guidePath: string;
  enabled: boolean;
}
