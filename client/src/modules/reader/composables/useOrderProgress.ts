import { ref } from "vue";

export const useOrderProgress = () => {
  type ModalStep = {
    title: string;
    error: string;
    messages: string[] | null;
  };

  type ModalState = {
    isOpen: boolean;
    currentStep: number;
    steps: ModalStep[];
    isSuccess: boolean;
    isError: boolean;
  };

  const DEFAULT_STEPS: ModalStep[] = [
    {
      title: "Проверка авторизации",
      error: "Вы не авторизованы. Пожалуйста, войдите в аккаунт и попробуйте снова.",
      messages: null,
    },
    {
      title: "Проверка количества книг",
      error: "Вы выбрали слишком много книг. Уменьшите их количество для оформления заказа.",
      messages: null,
    },
    {
      title: "Проверка возвращаемых книг",
      error:
        "Необходимо отметить книги, которые вы обещаете вернуть. Пожалуйста, выберите их выше.",
      messages: null,
    },
    {
      title: "Проверка доступности книг",
      error:
        "Некоторые книги недоступны для заказа. Возможно, они уже находятся у вас на руках или заказаны ранее.",
      messages: null,
    },
    {
      title: "Проверка лимитов",
      error:
        "Вы превысили допустимое количество книг (в заказах и на руках). Уменьшите общее число книг.",
      messages: null,
    },
    {
      title: "Создание заказа",
      error: "Произошла ошибка при создании заказа. Попробуйте ещё раз позже.",
      messages: null,
    },
  ];

  const modalState = ref<ModalState>({
    isOpen: false,
    currentStep: 0,
    steps: DEFAULT_STEPS,
    isSuccess: false,
    isError: false,
  });

  const resetModalState = () => {
    modalState.value = {
      ...modalState.value,
      currentStep: 0,
      isSuccess: false,
      isError: false,
      steps: [...DEFAULT_STEPS],
    };
  };

  return {
    modalState,
    resetModalState,
  };
};
