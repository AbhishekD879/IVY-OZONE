export interface ISportConfigurationTabs {
  name: string;
  subTabs?: ISportConfigurationSubTabs[];
  hidden?: boolean;
  label?: string;
}

export interface ISportConfigurationSubTabs {
  name: string;
}

export interface ISportConfiguration {
  config: any;
  filters: any;
  tabs: ISportConfigurationTabs[];
  order: any;
  sportConfig: { tabs: ISportConfigurationTabs[] };
}

export interface ISportViewByFiltersOrder {
  byLeagueEventsOrder: Array<string>;
  byTimeOrder: Array<string>;
}

export interface ISportTeamColors {
  teamName?:string;
  primaryColour?: string;
  secondaryColour?: string;
  teamsImage?: ITeamsImage;
  fiveASideToggle?: boolean;
  highlightCarouselToggle?: boolean;
}

export interface ITeamsImage extends File {
  originalname?: string;
  filename?: string;
  svg ?: string;
}
