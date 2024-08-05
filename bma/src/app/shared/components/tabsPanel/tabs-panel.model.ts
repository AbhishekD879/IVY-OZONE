export interface ITab {
  disabled?: boolean;
  hidden?: boolean;
  iconId?: string;
  id: number | string;
  label?: string;
  name?: string;
  marketName?: string;
  selected?: boolean;
  title?: string;
  url: string;
  isFiveASideNewIconAvailable: boolean;
}
