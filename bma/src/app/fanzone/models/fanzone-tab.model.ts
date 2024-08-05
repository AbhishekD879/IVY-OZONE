export interface IFanzoneTab {
  title?: string;
  id: string;
  url: string;
  visible?: boolean;
  showTabOn?: string;
  newSignPostingIcon?: boolean;
  tooltipConfig?: IFanzoneTooltipConfig;
}

export interface IFanzoneTooltipConfig {
  show: boolean;
  message: string;
} 