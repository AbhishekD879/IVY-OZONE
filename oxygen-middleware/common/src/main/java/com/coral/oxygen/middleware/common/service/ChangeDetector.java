package com.coral.oxygen.middleware.common.service;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.IdHolder;
import com.coral.oxygen.middleware.pojos.model.cms.VirtualSportEvents;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class ChangeDetector {

  public static boolean changeDetected(Object actual, Object previous) {
    return changeDetected(actual, previous, false);
  }

  public static boolean changeDetected(Object actual, Object previous, boolean detectMinorChange) {
    if (previous == null) {
      return true;
    }
    Class<?> clazz = actual.getClass();
    if (!clazz.equals(previous.getClass())) {
      return true;
    }
    Method[] methods = clazz.getMethods();
    for (Method method : methods) {
      if (!Modifier.isStatic(method.getModifiers())
          && Modifier.isPublic(method.getModifiers())
          && method.getParameterCount() == 0
          && !method.getReturnType().equals(Void.TYPE)
          && processMethodResult(method, actual, previous, detectMinorChange)) {
        return true;
      }
    }
    return false;
  }

  private static boolean processMethodResult(
      Method method, Object actual, Object previous, boolean detectMinorChange) {
    ChangeDetect declaredAnnotation = method.getDeclaredAnnotation(ChangeDetect.class);
    if (shouldNotCompare(declaredAnnotation, detectMinorChange)) {
      return false;
    }
    try {
      Object actualValue = method.invoke(actual);
      Object previousValue = method.invoke(previous);
      if (becomeNull(actualValue, previousValue)) {
        log.debug(
            "Detected change in class {}, method {}, actual is NULL, previous {}",
            actual.getClass().getSimpleName(),
            method.getName(),
            previousValue);
        return true;
      }
      if (actualValue == null) {
        return false;
      }
      if (comparableAsCollection(actualValue, declaredAnnotation)) {
        if (collectionChangeDetected(
            (Collection) actualValue, (Collection) previousValue, detectMinorChange)) {
          log.debug(
              "Detected collection change in class {}, method {}",
              actual.getClass().getSimpleName(),
              method.getName());
          return true;
        }
      } else if (comparableAsList(actualValue, declaredAnnotation)) {
        if (listChangeDetected((List) actualValue, (List) previousValue, detectMinorChange)) {
          log.debug(
              "Detected list change in class {}, method {}",
              actual.getClass().getSimpleName(),
              method.getName());
          return true;
        }
      } else if (declaredAnnotation.compareNestedObject()) {
        if (changeDetected(actualValue, previousValue, detectMinorChange)) {
          log.debug(
              "Detected change in class {}, method {}",
              actual.getClass().getSimpleName(),
              method.getName());
          return true;
        }
      } else if (!actualValue.equals(previousValue)) {
        log.debug(
            "Detected change in class {}, method {}, actual {}, previous {}",
            actual.getClass().getSimpleName(),
            method.getName(),
            actualValue,
            previousValue);
        return true;
      }
    } catch (Exception e) {
      log.error("Failed retrieving value for comparison", e);
      return true;
    }
    return false;
  }

  private static boolean shouldNotCompare(
      ChangeDetect declaredAnnotation, boolean detectMinorChange) {
    return declaredAnnotation == null || !detectMinorChange && declaredAnnotation.minor();
  }

  private static boolean becomeNull(Object actualValue, Object previousValue) {
    return actualValue == null && previousValue != null;
  }

  private static boolean comparableAsCollection(Object value, ChangeDetect declaredAnnotation) {
    return value instanceof Collection && declaredAnnotation.compareCollection();
  }

  private static boolean comparableAsList(Object value, ChangeDetect declaredAnnotation) {
    return value instanceof List && declaredAnnotation.compareList();
  }

  private static boolean collectionChangeDetected(
      Collection<? extends IdHolder> actual,
      Collection<? extends IdHolder> previous,
      boolean detectMinorChange) {
    try {
      Map<String, ? extends IdHolder> actualMap = getIdToEntityMap(actual);
      Map<String, ? extends IdHolder> previousMap = getIdToEntityMap(previous);
      if (!actualMap.keySet().equals(previousMap.keySet())) {
        log.debug("Detected change of keySet");
        return true;
      }
      Optional<? extends Map.Entry<String, ? extends IdHolder>> any =
          actualMap.entrySet().stream()
              .filter(
                  entry ->
                      changeDetected(
                          entry.getValue(), previousMap.get(entry.getKey()), detectMinorChange))
              .findAny();
      boolean result = any.isPresent();
      if (result) {
        log.debug("Detected change in key {}", any.get().getKey());
      }
      return result;
    } catch (Exception e) {
      log.error("Error during collections comparison", e);
      return true;
    }
  }

  private static HashMap<String, IdHolder> getIdToEntityMap(
      Collection<? extends IdHolder> entities) {
    return entities.stream()
        .collect(
            Collectors.toMap(
                IdHolder::idForChangeDetection,
                Function.identity(),
                (k, v) -> logDuplicate(k),
                HashMap::new));
  }

  private static IdHolder logDuplicate(IdHolder duplicatedObj) {
    String detection = duplicatedObj.idForChangeDetection();
    log.error(
        "Found same entity {} with id {} in a collection",
        duplicatedObj.getClass().getSimpleName(),
        detection);
    return duplicatedObj;
  }

  private static boolean listChangeDetected(
      List<? extends IdHolder> actual,
      List<? extends IdHolder> previous,
      boolean detectMinorChange) {
    try {
      if (actual == null && previous == null) {
        log.info("actual and previous both are null");
        return false;
      } else if (previous == null || actual == null) {
        String collection = actual == null ? "actual" : "previous";
        log.info(collection + " is null");
        return true;
      } else if (actual.size() != previous.size()) {
        log.debug("Detected change in list Size {} vs {}", actual.size(), previous.size());
        return true;
      }
      for (int i = 0; i < actual.size(); i++) {
        if (changeDetected(actual.get(i), previous.get(i), detectMinorChange)) {
          log.debug("Detected change in list index {}", i);
          return true;
        }
      }
      return false;
    } catch (Exception e) {
      log.error("Error during collections comparison", e);
      return true;
    }
  }

  public static boolean isVirtualEventsChanged(
      List<VirtualSportEvents> previousList, List<VirtualSportEvents> currentList) {
    if (Objects.isNull(previousList) || Objects.isNull(currentList)) {
      return false;
    }

    return previousList.stream()
        .collect(
            Collectors.toMap(
                VirtualSportEvents::getSportName, VirtualSportEvents::getLiveEventCount))
        .equals(
            currentList.stream()
                .collect(
                    Collectors.toMap(
                        VirtualSportEvents::getSportName, VirtualSportEvents::getLiveEventCount)));
  }
}
