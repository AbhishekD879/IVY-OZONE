import { ITab } from '@shared/components/tabsPanel/tabs-panel.model';

export interface IBreadcrumb {
  name: string;
  targetUri: string;
}

export interface IBreadcrumbConfig {
  sportName: string;
  tabs: ITab[];
  competitionName: string;
  isEDPPage: boolean;
  isOlympicsPage: boolean;
  isCompetitionPage: boolean;
  eventName: string;
  className: string;
  display: string;
  isFootballPage: boolean;
  isHorseRacingPage: boolean;
  isGreyhoundPage: boolean;
  isBuildYourRaceCardPage: boolean;
  isVirtual: boolean;
}
