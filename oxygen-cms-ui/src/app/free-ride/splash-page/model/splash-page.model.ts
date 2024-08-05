import { Filename } from '@root/app/client/private/models';
export class FreeRideSplashPageModel {
    id?: string;
    createdBy?: string;
    createdByUserName?: string;
    updatedBy?: string;
    updatedByUserName?: string;
    createdAt?: string;
    updatedAt?: string;
    brand?: string;
    welcomeMsg: string;
    termsAndConditionLink: string;
    termsAndConditionHyperLinkText: string;
    buttonText: string;
    splashImage?: Filename;
    splashImageName?: string;
    bannerImage?: Filename;
    bannerImageFileName?: string;
    freeRideLogo?: Filename;
    freeRideLogoFileName?: string;
    termsAndCondition?: string;
    isHomePage?: boolean;
    isBetReceipt?: boolean;
    promoUrl?: string;
}
