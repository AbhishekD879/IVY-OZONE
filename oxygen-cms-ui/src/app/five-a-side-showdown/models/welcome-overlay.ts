import { Base } from '@app/client/private/models/base.model';

export interface IWelcomeOverlay extends Base {
    headerTitle: string;
    videoURL: string;
    sectionTitle: string;
    previewTitle: string;
    plWelcomeTitle: string;
    plWelcomeContent: string;
    plWelcomeFooter: string;
    plPrizePoolInfo: string;
    plRulesEntryInfo: string;
    plBuildTeamInfo: string;
    plBuildAnotherTeamInfo: string;
    plBuildAnotherTeamHeader: string;
    plBuildAnotherTeamContent: string;
    plBulesButtonInfo: string;
    lobbyWelcomeHeader: string;
    lobbyWelcome1: string;
    lobbyWelcome2: string;
    lobbyWelcome3: string;
    lobbySignPostingsInfo: string;
    lobbyEntryInfo: string;
    lobbyShowdownCardInfo: string;
    overlayEnabled: boolean;
    liveHeaderTitle: string;
    liveSectionTitle: string;
    liveFooterTitle: string;
    liveMainPageHeaderTitle: string;
    liveMainPageSectionTitle: string;
    liveEntryTitle: string;
    liveStatTitle: string;
    liveProgressHeaderTitle: string;
    liveProgressFooterTitle: string;
    liveLeaderBoardEntriesTitle: string;
}
