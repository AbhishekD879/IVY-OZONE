import { Base } from '@app/client/private/models/base.model';

export interface IFAQ extends Base {
    question: string;
    answer: string;
}
