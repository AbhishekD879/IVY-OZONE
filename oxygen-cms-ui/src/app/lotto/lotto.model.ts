import { Base } from '@app/client/private/models/base.model';
import {Filename} from '@app/client/public/models/filename.model';
export interface ILotto extends Base {
    globalBannerLink: string;
    globalBannerText: string;
    dayCount: number;
    svgId: string;
    lottoConfig: Array<ILottos>;
    ids: string[];
}
export interface ILottos extends Base {
    label: string;
    infoMessage: string;
    nextLink: string;
    bannerLink: string;
    bannerText: string;
    ssMappingId: string;
    svgId: string;
    sortOrder: number;
    svgFilename: Filename;
    enabled: boolean;
    maxPayOut: number;
}
export interface ILottoUpdate {
    globalBannerLink: string;
    globalBannerText: string;
    dayCount: number;
    ids: string[];
}