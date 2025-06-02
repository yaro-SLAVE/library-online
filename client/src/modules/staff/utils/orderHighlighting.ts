import {
  addSeconds,
  parseISO,
  setHours,
  setMinutes,
  setSeconds,
  isBefore,
  getHours,
  getDay,
  getMinutes,
  getSeconds,
} from "date-fns";

const HIGHLIGHT_DURATION_SECONDS = 3600;
const WORKING_HOURS = {
  MONDAY_TO_FRIDAY_START_HOUR: 9,
  MONDAY_TO_FRIDAY_END_HOUR: 17,
  SATURDAY_START_HOUR: 9,
  SATURDAY_END_HOUR: 15,
};

const DAYS = {
  SUNDAY: 0,
  MONDAY: 1,
  TUESDAY: 2,
  WEDNESDAY: 3,
  THURSDAY: 4,
  FRIDAY: 5,
  SATURDAY: 6,
};

export function calculateHighlightTime(orderCreatedAt: string): Date | null {
  const createdAt = parseISO(orderCreatedAt);

  let effectiveCreationTime = new Date(createdAt.getTime());
  if (!isWorkingHour(effectiveCreationTime)) {
    const result = getNextWorkingHourStart(effectiveCreationTime);
    if (!result) return null;
    effectiveCreationTime = result;
  }

  const highlightTime = addWorkingSeconds(effectiveCreationTime, HIGHLIGHT_DURATION_SECONDS);

  if (!highlightTime || isBefore(highlightTime, createdAt)) {
    return null;
  }

  return highlightTime;
}

function isWorkingHour(date: Date): boolean {
  const day = getDay(date);
  const currentHour = getHours(date);

  if (day >= DAYS.MONDAY && day <= DAYS.FRIDAY) {
    if (
      currentHour >= WORKING_HOURS.MONDAY_TO_FRIDAY_START_HOUR &&
      currentHour < WORKING_HOURS.MONDAY_TO_FRIDAY_END_HOUR
    ) {
      return true;
    }
  } else if (day === DAYS.SATURDAY) {
    if (
      currentHour >= WORKING_HOURS.SATURDAY_START_HOUR &&
      currentHour < WORKING_HOURS.SATURDAY_END_HOUR
    ) {
      return true;
    }
  }
  return false;
}

function getNextWorkingHourStart(date: Date): Date | null {
  let nextWorkingTime = new Date(date.getTime());
  nextWorkingTime.setSeconds(0);
  nextWorkingTime.setMilliseconds(0);

  const currentDay = getDay(nextWorkingTime);
  const currentHour = getHours(nextWorkingTime);

  if (currentDay === DAYS.SUNDAY) {
    nextWorkingTime.setDate(nextWorkingTime.getDate() + 1);
    nextWorkingTime = setHours(nextWorkingTime, WORKING_HOURS.MONDAY_TO_FRIDAY_START_HOUR);
    nextWorkingTime = setMinutes(nextWorkingTime, 0);
    nextWorkingTime = setSeconds(nextWorkingTime, 0);
  } else if (currentDay === DAYS.SATURDAY) {
    if (currentHour >= WORKING_HOURS.SATURDAY_END_HOUR) {
      nextWorkingTime.setDate(nextWorkingTime.getDate() + 2);
      nextWorkingTime = setHours(nextWorkingTime, WORKING_HOURS.MONDAY_TO_FRIDAY_START_HOUR);
      nextWorkingTime = setMinutes(nextWorkingTime, 0);
      nextWorkingTime = setSeconds(nextWorkingTime, 0);
    } else {
      nextWorkingTime = setHours(nextWorkingTime, WORKING_HOURS.SATURDAY_START_HOUR);
      nextWorkingTime = setMinutes(nextWorkingTime, 0);
      nextWorkingTime = setSeconds(nextWorkingTime, 0);
    }
  } else if (currentDay >= DAYS.MONDAY && currentDay <= DAYS.FRIDAY) {
    if (currentHour >= WORKING_HOURS.MONDAY_TO_FRIDAY_END_HOUR) {
      nextWorkingTime.setDate(nextWorkingTime.getDate() + 1);
      if (getDay(nextWorkingTime) === DAYS.SATURDAY) {
        nextWorkingTime.setDate(nextWorkingTime.getDate() + 2);
      }
      nextWorkingTime = setHours(nextWorkingTime, WORKING_HOURS.MONDAY_TO_FRIDAY_START_HOUR);
      nextWorkingTime = setMinutes(nextWorkingTime, 0);
      nextWorkingTime = setSeconds(nextWorkingTime, 0);
    } else {
      nextWorkingTime = setHours(nextWorkingTime, WORKING_HOURS.MONDAY_TO_FRIDAY_START_HOUR);
      nextWorkingTime = setMinutes(nextWorkingTime, 0);
      nextWorkingTime = setSeconds(nextWorkingTime, 0);
    }
  }

  if (isBefore(nextWorkingTime, date)) {
    return null;
  }

  return nextWorkingTime;
}

function addWorkingSeconds(startDate: Date, secondsToAdd: number): Date {
  let current = new Date(startDate.getTime());
  let remainingSeconds = secondsToAdd;

  while (remainingSeconds > 0) {
    const day = getDay(current);
    let hour = getHours(current);
    let minutes = getMinutes(current);
    let seconds = getSeconds(current);

    let dayStartHour: number;
    let dayEndHour: number;

    if (day >= DAYS.MONDAY && day <= DAYS.FRIDAY) {
      dayStartHour = WORKING_HOURS.MONDAY_TO_FRIDAY_START_HOUR;
      dayEndHour = WORKING_HOURS.MONDAY_TO_FRIDAY_END_HOUR;
    } else if (day === DAYS.SATURDAY) {
      dayStartHour = WORKING_HOURS.SATURDAY_START_HOUR;
      dayEndHour = WORKING_HOURS.SATURDAY_END_HOUR;
    } else {
      current = getNextWorkingHourStart(current)!;
      continue;
    }

    if (hour < dayStartHour) {
      current = setHours(current, dayStartHour);
      current = setMinutes(current, 0);
      current = setSeconds(current, 0);
      hour = getHours(current);
      minutes = getMinutes(current);
      seconds = getSeconds(current);
    } else if (hour >= dayEndHour) {
      current = getNextWorkingHourStart(current)!;
      continue;
    }

    const secondsUntilEndOfDay =
      (dayEndHour - hour - 1) * 3600 + (60 - minutes - 1) * 60 + (60 - seconds);

    if (remainingSeconds <= secondsUntilEndOfDay) {
      current = addSeconds(current, remainingSeconds);
      remainingSeconds = 0;
    } else {
      current = addSeconds(current, secondsUntilEndOfDay);
      remainingSeconds -= secondsUntilEndOfDay;

      if (remainingSeconds > 0) {
        current = getNextWorkingHourStart(current)!;
      }
    }
  }
  return current;
}
