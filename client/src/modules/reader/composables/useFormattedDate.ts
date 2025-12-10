export const useFormattedDate = () => {
  const formatDate = (date: string | Date) => {
    return new Date(date).toLocaleDateString("ru-RU");
  };

  return { formatDate };
};
