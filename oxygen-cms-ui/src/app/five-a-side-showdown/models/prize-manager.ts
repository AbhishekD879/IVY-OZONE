import { Base } from '@app/client/private/models/base.model';

export interface IPrizeFile extends File {
    originalname?: string;
    svgId?: string;
    filename?: string;
}

export interface IPrize extends Base {
    type: string;
    value: string;
    text: string;
    icon: IPrizeFile;
    signPosting: IPrizeFile;
    percentageOfField: string;
    numberOfEntries: string;
    contestId?: string;
    prizeIcon?: File;
    prizeSignposting?: File;
    freebetOfferId?: string;
    defaultOfferIds?: any;
}
