import { IProcessedRequestModel } from '../process-request.model';
import { ISvgFilename } from '../svg-filename.model';
import { IBase } from '../base.model';
import { Observable } from 'rxjs';
import { IMenuActionResult } from './menu-action.model';
import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { FanzoneDetails } from '@app/fanzone/models/fanzone.model';

export interface IVerticalMenu extends IBase, IProcessedRequestModel {
  linkTitle: string;
  linkSubtitle: string;
  lang: string;
  svg: string;
  svgId: string;
  disabled: boolean;
  targetUri: string;
  svgFilename: ISvgFilename;
  qa: string;
  type: string;
  title: string;
  subtitle: string;
  action: () => Observable<IMenuActionResult>;
  hidden?: boolean;
  hasEvents?: boolean;
  selectedFanzone?: FanzoneDetails;
  categoryId?: number;
  sortOrder: number;
  fzDisabled?: boolean;
}

export interface IFreeBetConfig {
  data: IFreebetToken[];
  total: string;
  open:  boolean;
  item?: IVerticalMenu;
}
