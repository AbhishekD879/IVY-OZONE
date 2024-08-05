export interface SubMenuItem {
  label: string;
  path: string;
}

export interface MenuItem {
  id?: string;
  active: boolean;
  label: string;
  path: string;
  icon: string;
  displayOrder: number;
  'sub-menus': SubMenuItem[];
}
