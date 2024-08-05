import { MenuSection } from '@frontend/vanilla/core';

export interface IFreeBetsBadgeModel {
    section: MenuSection.Header | MenuSection.Menu;
    item: string;
    count: string | number;
    cssClass?: string;
    type?: string;
}
