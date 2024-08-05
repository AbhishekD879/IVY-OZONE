import { Base } from '@app/client/private/models/base.model';

export interface IMyStable extends Base {
    buttonText: string;
    imageUrl: string;
    isActive: boolean;
    fileName: string;
    onboardImageDetails:onboardImageDetailsModel;
}

export interface onboardImageDetailsModel {
    filename: string,
    originalname: string,
    path: string,
    filetype: string
    size?: number,
}