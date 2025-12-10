import { useLocalStorage } from "@vueuse/core";
import { defineStore } from "pinia";
import { onMounted } from "vue";

export const useThemeStore = defineStore("theme", () => {
  type Theme = "system" | "light" | "dark";
  type Font = "large" | "standard";

  const theme = useLocalStorage<Theme>("theme", "system");
  const font = useLocalStorage<Font>("font", "standard");

  function updateThemeAttribute() {
    const root = document.documentElement;
    if (theme.value == "system") {
      delete root.dataset.theme;
    } else {
      root.dataset.theme = theme.value;
    }
  }

  function updateFontAttribute() {
    const root = document.documentElement;
    if (font.value == "standard") {
      delete root.dataset.largefont;
    } else {
      root.dataset.largefont = "";
    }
  }

  function setTheme(newTheme: Theme) {
    theme.value = newTheme;
    updateThemeAttribute();
  }

  function setFont(newFont: Font) {
    font.value = newFont;
    updateFontAttribute();
  }

  onMounted(() => {
    updateThemeAttribute();
    updateFontAttribute();
  });

  return {
    theme,
    font,
    setTheme,
    setFont,
  };
});
