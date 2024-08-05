import { Base } from "./base.model";

export interface ISegmentConfig {
    exclusionSegments: string;
    inclusionSegments: string;
    activeSegment: string;
}

export interface ISegmentModel {
    exclusionList?: string[],
    inclusionList?: string[],
    universalSegment?: boolean
}

export interface ISegment extends Base {
    name: string;
    selected?: boolean;
}

export interface ISegmentMsg {
    segmentModule: string;
    segmentValue: string;
}