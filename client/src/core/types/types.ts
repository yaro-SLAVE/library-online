import type { FunctionalComponent } from "vue";

export interface Link {
  to: string;
  name: string;
}

export interface LinksConfig extends Link {
  hide?: boolean;
}

export interface SidebarLink {
  name: string;
  to: string;
  icon: FunctionalComponent;
}
