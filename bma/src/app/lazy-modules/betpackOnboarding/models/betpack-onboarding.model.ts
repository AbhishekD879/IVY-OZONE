export interface BetPackOnBoardingCMSConfig{
    id: string;
    createdBy: string;
    createdByUserName: string;
    updatedBy: string;
    updatedByUserName: string;
    createdAt: string;
    updatedAt: string;
    sortOrder: number;
    brand: string;
    isActive: boolean;
    images: OnBoardingImageCollection[];
}

export interface OnBoardingImageCollection{
    imageLabel: string;
    nextCTAButtonLabel: string;
    onboardImageDetails: OnBoardingImageDetails;
    imageType: string;
    id: string;
}

export interface OnBoardingImageDetails{
    filename: string;
    originalname: string;
    path: string;
    filetype: string;
}