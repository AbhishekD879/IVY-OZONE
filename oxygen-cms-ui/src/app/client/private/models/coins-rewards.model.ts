import { Base } from "./base.model";

export interface RssRewards extends Base {
    enabled?: boolean;
    coins?: number;
    communicationType?: string;
    sitecoreTemplateId?: string;
    source?: string;
    subSource?: string;
    product?: string;
}
export interface FssRewards {
    value?: number;
    communicationType?: string;
    siteCoreId?: string;
}