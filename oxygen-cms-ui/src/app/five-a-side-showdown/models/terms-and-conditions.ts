import { Base } from '@app/client/private/models/base.model';

export interface ITermsAndConditions extends Base {
    text: string;
    title: string;
    url: string;
}
