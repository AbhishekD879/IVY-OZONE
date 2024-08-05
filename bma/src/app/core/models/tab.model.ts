export interface ITab {
  id: string;
  label: string;
  title: string;
  url: string;
  originalTitle: string;
  isFiveASideNewIconAvailable?: boolean;
  marketName?: string;
}

export interface ITabOlympic {
  id?: string;
  label?: string;
  title?: string;
  url?: string;
  market?: string;
  hidden?: boolean;
}
export interface ITabActive {
  id: string;
}
