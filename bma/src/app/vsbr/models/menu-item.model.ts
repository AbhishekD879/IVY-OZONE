export interface IVirtualSportsMenuItem {
  name: string;
  inApp: boolean;
  svgId: string;
  targetUri: string;
  targetUriSegment: string;
  priority: number;
  numberOfEvents?: number;
  showRunnerImages?: boolean;
  showRunnerNumber?: boolean;
  childMenuItems?: IVirtualSportsMenuItem[];
  label?: IVirtualSportsMenuItemLabel;
  displayOrder?: string | number;
  alias?: string;
  svg?: string;
  isActive?: boolean;
  streamUrl?: string;
}

export interface IVirtualSportsMenuItemLabel {
  className: string;
  text: string;
}
