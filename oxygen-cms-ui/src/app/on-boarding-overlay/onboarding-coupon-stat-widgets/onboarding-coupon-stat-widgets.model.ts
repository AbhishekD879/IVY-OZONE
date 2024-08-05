import { Base } from '@app/client/private/models/base.model';

export interface ICouponStatWidget extends Base {
    imageLabel: string;
    buttonText: string;
    imageUrl: string;
    isEnable: boolean;
    directFileUrl: string;
    fileName: string;
}