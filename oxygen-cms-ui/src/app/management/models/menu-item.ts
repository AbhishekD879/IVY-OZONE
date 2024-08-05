interface SubMenuItem {
  label: string;
  path: string;
}

export interface MenuItem {
  active: boolean;
  label: string;
  path: string;
  icon: string;
  displayOrder?: number;
  'sub-menus': SubMenuItem[];
}

