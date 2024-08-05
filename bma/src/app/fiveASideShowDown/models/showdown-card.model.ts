import { IContest } from '@app/core/services/cms/models/contest';
import { ITeamColor } from '@app/fiveASideShowDown/models/team-color';
import { IEventDetails } from './show-down';

export interface IShowdownCard extends IContest {
    eventDetails: IEventDetails;
    assets: ITeamColor[];
    showRoleContest?: boolean;
    prizeMap: any;
}
export interface IShowdownCardDetails {
    totalPrizes: string;
    entryStake: string;
    prizePoolSummary: string;
    contestSize: string;
    prizePoolTotalPrizes: string;
    teamsEntries: string;
    firstPlace: string;
    vouchers: string;
    tickets: string;
    freeBets: string;
}

export interface IShowdownCardSignPostings {
    summary: boolean;
    size: boolean;
    totalPrizes: boolean;
    teams: boolean;
    firstPlace: boolean;
    vouchers: boolean;
    tickets: boolean;
    freeBets: boolean;
}

