import { computed } from 'vue';
import type { LinksConfig, Link } from '@core/types/types';

export function useLinksFilter(rawLinks: LinksConfig[]) {
  const links = computed(() => {
    return rawLinks
    .filter((x) => !x.hide)
    .map((x): Link => ({ to: x.to, name: x.name }));
  });
  
  return { links };
}